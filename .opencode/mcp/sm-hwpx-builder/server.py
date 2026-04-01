"""SM_hwpx_builder MCP Server - HWPX 문서 빌드/변환/검증

이 서버는 폐쇄망 내부에서 hwpx 도구 라이브러리와 연동한다.
실제 변환 로직은 hwpx 파이썬 패키지(별도 설치 필요)를 사용한다.
"""

import json
import subprocess
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler


def convert_md_to_hwpx(md_path: str, output_path: str = "") -> dict:
    """마크다운 파일을 hwpx로 변환한다."""
    if not os.path.exists(md_path):
        return {"error": f"File not found: {md_path}"}
    if not output_path:
        output_path = md_path.rsplit(".", 1)[0] + ".hwpx"
    try:
        # hwpx CLI 도구 호출 (별도 설치 필요: pip install hwpx-converter)
        result = subprocess.run(
            ["python", "-m", "hwpx_converter", "convert", md_path, "-o", output_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return {"output_path": output_path, "success": True}
        return {"error": result.stderr, "success": False}
    except FileNotFoundError:
        return {"error": "hwpx-converter not installed. Run: pip install hwpx-converter", "success": False}


def analyze_hwpx(hwpx_path: str) -> dict:
    """hwpx 파일의 구조를 분석한다."""
    if not os.path.exists(hwpx_path):
        return {"error": f"File not found: {hwpx_path}"}
    try:
        result = subprocess.run(
            ["python", "-m", "hwpx_converter", "analyze", hwpx_path],
            capture_output=True, text=True, timeout=30
        )
        return {"analysis": result.stdout, "error": result.stderr if result.returncode != 0 else None}
    except FileNotFoundError:
        return {"error": "hwpx-converter not installed"}


def build_hwpx(source_dir: str, output_path: str) -> dict:
    """추출된 XML 소스로 hwpx를 빌드한다."""
    if not os.path.isdir(source_dir):
        return {"error": f"Directory not found: {source_dir}"}
    try:
        result = subprocess.run(
            ["python", "-m", "hwpx_converter", "build", source_dir, "-o", output_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return {"output_path": output_path, "success": True}
        return {"error": result.stderr, "success": False}
    except FileNotFoundError:
        return {"error": "hwpx-converter not installed"}


def validate_hwpx(hwpx_path: str) -> dict:
    """hwpx 문서의 구조적 유효성을 검증한다."""
    if not os.path.exists(hwpx_path):
        return {"error": f"File not found: {hwpx_path}"}
    try:
        result = subprocess.run(
            ["python", "-m", "hwpx_converter", "validate", hwpx_path],
            capture_output=True, text=True, timeout=30
        )
        return {"valid": result.returncode == 0, "message": result.stdout or result.stderr}
    except FileNotFoundError:
        return {"error": "hwpx-converter not installed"}


class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}
        method = body.get("method", "")
        params = body.get("params", {})

        if method == "tools/list":
            response = {"tools": [
                {"name": "convert_md_to_hwpx", "description": "마크다운을 hwpx로 변환",
                 "inputSchema": {"type": "object", "properties": {
                     "md_path": {"type": "string"}, "output_path": {"type": "string", "default": ""}
                 }, "required": ["md_path"]}},
                {"name": "analyze_hwpx", "description": "hwpx 구조 분석",
                 "inputSchema": {"type": "object", "properties": {"hwpx_path": {"type": "string"}}, "required": ["hwpx_path"]}},
                {"name": "build_hwpx", "description": "XML 소스로 hwpx 빌드",
                 "inputSchema": {"type": "object", "properties": {
                     "source_dir": {"type": "string"}, "output_path": {"type": "string"}
                 }, "required": ["source_dir", "output_path"]}},
                {"name": "validate_hwpx", "description": "hwpx 문서 검증",
                 "inputSchema": {"type": "object", "properties": {"hwpx_path": {"type": "string"}}, "required": ["hwpx_path"]}},
            ]}
        elif method == "tools/call":
            tool_name = params.get("name", "")
            args = params.get("arguments", {})
            handlers = {
                "convert_md_to_hwpx": lambda: convert_md_to_hwpx(args["md_path"], args.get("output_path", "")),
                "analyze_hwpx": lambda: analyze_hwpx(args["hwpx_path"]),
                "build_hwpx": lambda: build_hwpx(args["source_dir"], args["output_path"]),
                "validate_hwpx": lambda: validate_hwpx(args["hwpx_path"]),
            }
            result = handlers.get(tool_name, lambda: {"error": f"Unknown tool: {tool_name}"})()
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
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3012
    server = HTTPServer(("127.0.0.1", port), MCPHandler)
    print(f"SM_hwpx_builder MCP server running on port {port}", file=sys.stderr)
    server.serve_forever()
