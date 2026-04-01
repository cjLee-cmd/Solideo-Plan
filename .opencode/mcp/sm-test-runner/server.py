"""SM_test_runner MCP Server - 테스트 프레임워크 실행 및 결과 반환"""

import json
import subprocess
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler


def detect_framework(project_path: str) -> str:
    """프로젝트의 테스트 프레임워크를 자동 감지한다."""
    checks = {
        "pytest": ["pyproject.toml", "conftest.py", "setup.py"],
        "junit": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "jest": ["package.json"],
        "nunit": [],
        "gotest": ["go.mod"],
    }
    for fw, files in checks.items():
        for f in files:
            if os.path.exists(os.path.join(project_path, f)):
                if fw == "jest":
                    pkg = os.path.join(project_path, "package.json")
                    with open(pkg) as fh:
                        content = json.load(fh)
                    deps = {**content.get("dependencies", {}), **content.get("devDependencies", {})}
                    if "jest" in deps:
                        return "jest"
                elif fw == "nunit":
                    for root, _, fnames in os.walk(project_path):
                        for fname in fnames:
                            if fname.endswith(".csproj"):
                                with open(os.path.join(root, fname)) as fh:
                                    if "NUnit" in fh.read():
                                        return "nunit"
                else:
                    return fw
    return "unknown"


def run_tests(project_path: str, test_path: str = "", framework: str = "auto", filter_pattern: str = "") -> dict:
    """테스트를 실행하고 결과를 반환한다."""
    if framework == "auto":
        framework = detect_framework(project_path)

    commands = {
        "pytest": ["python", "-m", "pytest", "--tb=short", "-q", "--json-report", "--json-report-file=-"],
        "junit": ["mvn", "test", "-pl", ".", "-q"] if os.path.exists(os.path.join(project_path, "pom.xml"))
                 else ["gradle", "test", "--quiet"],
        "jest": ["npx", "jest", "--json", "--silent"],
        "gotest": ["go", "test", "-json", "./..."],
        "nunit": ["dotnet", "test", "--verbosity", "minimal"],
    }

    cmd = commands.get(framework, [])
    if not cmd:
        return {"error": f"Unknown framework: {framework}", "total": 0, "passed": 0, "failed": 0, "skipped": 0}

    if test_path:
        cmd.append(test_path)
    if filter_pattern and framework == "pytest":
        cmd.extend(["-k", filter_pattern])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_path, timeout=300)
        return parse_result(framework, result)
    except subprocess.TimeoutExpired:
        return {"error": "Test execution timed out (300s)", "total": 0, "passed": 0, "failed": 0, "skipped": 0}
    except FileNotFoundError as e:
        return {"error": f"Command not found: {e}", "total": 0, "passed": 0, "failed": 0, "skipped": 0}


def parse_result(framework: str, result: subprocess.CompletedProcess) -> dict:
    """프레임워크별 테스트 결과를 파싱한다."""
    output = result.stdout + result.stderr
    base = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "duration_ms": 0, "failures": [], "raw_output": output[:2000]}

    if framework == "pytest":
        try:
            data = json.loads(result.stdout)
            summary = data.get("summary", {})
            base["total"] = summary.get("total", 0)
            base["passed"] = summary.get("passed", 0)
            base["failed"] = summary.get("failed", 0)
            base["skipped"] = summary.get("skipped", 0)
            base["duration_ms"] = int(summary.get("duration", 0) * 1000)
            for t in data.get("tests", []):
                if t.get("outcome") == "failed":
                    base["failures"].append({
                        "test_name": t.get("nodeid", ""),
                        "message": t.get("call", {}).get("longrepr", "")[:500],
                    })
        except (json.JSONDecodeError, KeyError):
            base["error"] = "Failed to parse pytest output"

    elif framework == "jest":
        try:
            data = json.loads(result.stdout)
            base["total"] = data.get("numTotalTests", 0)
            base["passed"] = data.get("numPassedTests", 0)
            base["failed"] = data.get("numFailedTests", 0)
            base["skipped"] = data.get("numPendingTests", 0)
            for suite in data.get("testResults", []):
                for t in suite.get("testResults", []):
                    if t.get("status") == "failed":
                        base["failures"].append({
                            "test_name": t.get("fullName", ""),
                            "message": "\n".join(t.get("failureMessages", []))[:500],
                        })
        except (json.JSONDecodeError, KeyError):
            base["error"] = "Failed to parse jest output"
    else:
        base["error"] = f"Parser not implemented for {framework}. Raw output included."

    return base


def get_coverage(project_path: str, test_path: str = "") -> dict:
    """커버리지를 측정한다."""
    framework = detect_framework(project_path)
    if framework == "pytest":
        cmd = ["python", "-m", "pytest", "--cov", "--cov-report=json", "-q"]
        if test_path:
            cmd.append(test_path)
        try:
            subprocess.run(cmd, capture_output=True, text=True, cwd=project_path, timeout=300)
            cov_file = os.path.join(project_path, "coverage.json")
            if os.path.exists(cov_file):
                with open(cov_file) as f:
                    data = json.load(f)
                totals = data.get("totals", {})
                return {
                    "line_coverage": totals.get("percent_covered", 0),
                    "branch_coverage": totals.get("percent_covered_branches", 0),
                    "uncovered_files": [f for f, d in data.get("files", {}).items() if d.get("summary", {}).get("percent_covered", 100) < 50],
                }
        except Exception as e:
            return {"error": str(e)}
    return {"error": f"Coverage not implemented for {framework}"}


# --- MCP Protocol Handler ---

class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}

        method = body.get("method", "")
        params = body.get("params", {})

        if method == "tools/list":
            response = {"tools": [
                {"name": "run_tests", "description": "테스트 프레임워크를 실행하고 결과를 반환",
                 "inputSchema": {"type": "object", "properties": {
                     "project_path": {"type": "string"}, "test_path": {"type": "string", "default": ""},
                     "framework": {"type": "string", "default": "auto"}, "filter": {"type": "string", "default": ""}
                 }, "required": ["project_path"]}},
                {"name": "get_coverage", "description": "코드 커버리지를 측정",
                 "inputSchema": {"type": "object", "properties": {
                     "project_path": {"type": "string"}, "test_path": {"type": "string", "default": ""}
                 }, "required": ["project_path"]}},
            ]}
        elif method == "tools/call":
            tool_name = params.get("name", "")
            args = params.get("arguments", {})
            if tool_name == "run_tests":
                result = run_tests(args["project_path"], args.get("test_path", ""), args.get("framework", "auto"), args.get("filter", ""))
            elif tool_name == "get_coverage":
                result = get_coverage(args["project_path"], args.get("test_path", ""))
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            response = {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}
        else:
            response = {"error": f"Unknown method: {method}"}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"jsonrpc": "2.0", "id": body.get("id"), "result": response}).encode())

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3010
    server = HTTPServer(("127.0.0.1", port), MCPHandler)
    print(f"SM_test_runner MCP server running on port {port}", file=sys.stderr)
    server.serve_forever()
