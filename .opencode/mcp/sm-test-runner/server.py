"""SM_test_runner MCP Server (stdio) - 테스트 프레임워크 실행 및 결과 반환"""

import json
import subprocess
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_stdio import run_server


def detect_framework(project_path: str) -> str:
    checks = {
        "pytest": ["pyproject.toml", "conftest.py", "setup.py"],
        "junit": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "jest": ["package.json"],
        "gotest": ["go.mod"],
    }
    for fw, files in checks.items():
        for f in files:
            if os.path.exists(os.path.join(project_path, f)):
                if fw == "jest":
                    try:
                        with open(os.path.join(project_path, "package.json")) as fh:
                            content = json.load(fh)
                        deps = {**content.get("dependencies", {}), **content.get("devDependencies", {})}
                        if "jest" in deps:
                            return "jest"
                    except Exception:
                        pass
                else:
                    return fw
    return "unknown"


def run_tests(project_path: str, test_path: str = "", framework: str = "auto", filter_pattern: str = "") -> dict:
    if framework == "auto":
        framework = detect_framework(project_path)

    commands = {
        "pytest": ["python", "-m", "pytest", "--tb=short", "-q"],
        "junit": ["mvn", "test", "-q"] if os.path.exists(os.path.join(project_path, "pom.xml"))
                 else ["gradle", "test", "--quiet"],
        "jest": ["npx", "jest", "--json", "--silent"],
        "gotest": ["go", "test", "-v", "./..."],
        "nunit": ["dotnet", "test", "--verbosity", "minimal"],
    }

    cmd = commands.get(framework)
    if not cmd:
        return {"error": f"Unknown framework: {framework}", "total": 0, "passed": 0, "failed": 0, "skipped": 0}

    if test_path:
        cmd.append(test_path)
    if filter_pattern and framework == "pytest":
        cmd.extend(["-k", filter_pattern])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_path, timeout=300)
        return {
            "framework": framework,
            "exit_code": result.returncode,
            "stdout": result.stdout[:3000],
            "stderr": result.stderr[:1000],
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"error": "Test execution timed out (300s)"}
    except FileNotFoundError as e:
        return {"error": f"Command not found: {e}"}


def get_coverage(project_path: str, test_path: str = "") -> dict:
    framework = detect_framework(project_path)
    if framework == "pytest":
        cmd = ["python", "-m", "pytest", "--cov", "--cov-report=term-missing", "-q"]
        if test_path:
            cmd.append(test_path)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_path, timeout=300)
            return {"coverage_output": result.stdout[:3000], "success": result.returncode == 0}
        except Exception as e:
            return {"error": str(e)}
    return {"error": f"Coverage not implemented for {framework}"}


TOOLS = [
    {"name": "run_tests", "description": "테스트 프레임워크를 실행하고 결과를 반환",
     "inputSchema": {"type": "object", "properties": {
         "project_path": {"type": "string", "description": "프로젝트 루트 경로"},
         "test_path": {"type": "string", "description": "테스트 경로 (선택)", "default": ""},
         "framework": {"type": "string", "description": "auto/pytest/junit/jest/gotest/nunit", "default": "auto"},
         "filter": {"type": "string", "description": "테스트 필터 패턴", "default": ""},
     }, "required": ["project_path"]}},
    {"name": "get_coverage", "description": "코드 커버리지를 측정",
     "inputSchema": {"type": "object", "properties": {
         "project_path": {"type": "string", "description": "프로젝트 루트 경로"},
         "test_path": {"type": "string", "description": "테스트 경로 (선택)", "default": ""},
     }, "required": ["project_path"]}},
]


def handle_tool(name: str, args: dict) -> dict:
    if name == "run_tests":
        return run_tests(args["project_path"], args.get("test_path", ""), args.get("framework", "auto"), args.get("filter", ""))
    elif name == "get_coverage":
        return get_coverage(args["project_path"], args.get("test_path", ""))
    return {"error": f"Unknown tool: {name}"}


if __name__ == "__main__":
    run_server("sm-test-runner", TOOLS, handle_tool)
