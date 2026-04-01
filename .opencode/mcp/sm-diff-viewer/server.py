"""SM_diff_viewer MCP Server - 수정 전후 코드 차이 비교"""

import json
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler


def get_diff(project_path: str, file_path: str = "", base: str = "HEAD") -> dict:
    """파일 또는 프로젝트의 diff를 반환한다."""
    cmd = ["git", "diff", base]
    if file_path:
        cmd.extend(["--", file_path])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_path, timeout=30)
        return {"diff": result.stdout, "error": result.stderr if result.returncode != 0 else None}
    except Exception as e:
        return {"error": str(e)}


def get_project_diff(project_path: str, base: str = "HEAD~1") -> dict:
    """프로젝트 전체 변경 파일 목록을 반환한다."""
    cmd = ["git", "diff", "--name-status", base]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_path, timeout=30)
        files = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("\t")
                files.append({"status": parts[0], "file": parts[1] if len(parts) > 1 else ""})
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}


def get_stat(project_path: str, base: str = "HEAD~1") -> dict:
    """변경 통계를 반환한다."""
    cmd = ["git", "diff", "--stat", "--numstat", base]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_path, timeout=30)
        added, deleted, files_changed = 0, 0, 0
        for line in result.stdout.strip().split("\n"):
            parts = line.split("\t")
            if len(parts) >= 3:
                try:
                    added += int(parts[0])
                    deleted += int(parts[1])
                    files_changed += 1
                except ValueError:
                    pass
        return {"files_changed": files_changed, "lines_added": added, "lines_deleted": deleted}
    except Exception as e:
        return {"error": str(e)}


class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}
        method = body.get("method", "")
        params = body.get("params", {})

        if method == "tools/list":
            response = {"tools": [
                {"name": "get_diff", "description": "파일별 diff 비교",
                 "inputSchema": {"type": "object", "properties": {
                     "project_path": {"type": "string"}, "file_path": {"type": "string", "default": ""}, "base": {"type": "string", "default": "HEAD"}
                 }, "required": ["project_path"]}},
                {"name": "get_project_diff", "description": "프로젝트 전체 변경 목록",
                 "inputSchema": {"type": "object", "properties": {
                     "project_path": {"type": "string"}, "base": {"type": "string", "default": "HEAD~1"}
                 }, "required": ["project_path"]}},
                {"name": "get_stat", "description": "변경 통계",
                 "inputSchema": {"type": "object", "properties": {
                     "project_path": {"type": "string"}, "base": {"type": "string", "default": "HEAD~1"}
                 }, "required": ["project_path"]}},
            ]}
        elif method == "tools/call":
            tool_name = params.get("name", "")
            args = params.get("arguments", {})
            if tool_name == "get_diff":
                result = get_diff(args["project_path"], args.get("file_path", ""), args.get("base", "HEAD"))
            elif tool_name == "get_project_diff":
                result = get_project_diff(args["project_path"], args.get("base", "HEAD~1"))
            elif tool_name == "get_stat":
                result = get_stat(args["project_path"], args.get("base", "HEAD~1"))
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
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3011
    server = HTTPServer(("127.0.0.1", port), MCPHandler)
    print(f"SM_diff_viewer MCP server running on port {port}", file=sys.stderr)
    server.serve_forever()
