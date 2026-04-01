"""SM_hwpx_builder MCP Server (stdio) - HWPX 문서 빌드/변환/검증

~/tools/md2hwpx/md2hwpx.py 변환기를 사용한다.
"""

import json
import subprocess
import os
import sys
import zipfile

sys.path.insert(0, "/Users/cjlee/.config/opencode/mcp")
from mcp_stdio import run_server

MD2HWPX = os.path.expanduser("~/tools/md2hwpx/md2hwpx.py")
SKELETON = os.path.expanduser("~/tools/md2hwpx/Skeleton.hwpx")


def convert_md_to_hwpx(md_path: str, output_path: str = "", title: str = "", author: str = "") -> dict:
    if not os.path.exists(md_path):
        return {"error": f"File not found: {md_path}"}
    if not os.path.exists(MD2HWPX):
        return {"error": f"md2hwpx.py not found at {MD2HWPX}"}
    if not output_path:
        output_path = md_path.rsplit(".", 1)[0] + ".hwpx"

    cmd = ["python3", MD2HWPX, md_path, output_path, "--skeleton", SKELETON]
    if title:
        cmd.extend(["--title", title])
    if author:
        cmd.extend(["--author", author])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and os.path.exists(output_path):
            size = os.path.getsize(output_path)
            return {"output_path": output_path, "success": True, "size_bytes": size, "message": result.stdout.strip()}
        return {"error": result.stderr.strip() or result.stdout.strip(), "success": False}
    except subprocess.TimeoutExpired:
        return {"error": "변환 시간 초과 (60초)", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}


def analyze_hwpx(hwpx_path: str) -> dict:
    if not os.path.exists(hwpx_path):
        return {"error": f"File not found: {hwpx_path}"}
    try:
        info = {"files": [], "total_size": os.path.getsize(hwpx_path)}
        with zipfile.ZipFile(hwpx_path, 'r') as z:
            for f in z.namelist():
                fi = z.getinfo(f)
                info["files"].append({"name": f, "size": fi.file_size, "compressed": fi.compress_size})
        return info
    except Exception as e:
        return {"error": str(e)}


def validate_hwpx(hwpx_path: str) -> dict:
    if not os.path.exists(hwpx_path):
        return {"error": f"File not found: {hwpx_path}"}
    try:
        with zipfile.ZipFile(hwpx_path, 'r') as z:
            names = z.namelist()
            has_mimetype = "mimetype" in names
            has_content = any("Contents/" in n for n in names)
            has_section = any("section" in n for n in names)
            errors = []
            if not has_mimetype:
                errors.append("mimetype 파일 없음")
            if not has_content:
                errors.append("Contents/ 디렉토리 없음")
            if not has_section:
                errors.append("section XML 없음")
            return {"valid": len(errors) == 0, "files_count": len(names), "errors": errors}
    except zipfile.BadZipFile:
        return {"valid": False, "errors": ["유효한 ZIP/HWPX 파일이 아님"]}
    except Exception as e:
        return {"valid": False, "errors": [str(e)]}


TOOLS = [
    {"name": "convert_md_to_hwpx", "description": "마크다운 파일을 hwpx(한글)로 변환. ~/tools/md2hwpx/md2hwpx.py 사용.",
     "inputSchema": {"type": "object", "properties": {
         "md_path": {"type": "string", "description": "마크다운 파일 경로"},
         "output_path": {"type": "string", "description": "출력 hwpx 경로 (선택, 미지정 시 입력 파일명.hwpx)", "default": ""},
         "title": {"type": "string", "description": "문서 제목 (선택)", "default": ""},
         "author": {"type": "string", "description": "작성자 (선택)", "default": ""},
     }, "required": ["md_path"]}},
    {"name": "analyze_hwpx", "description": "hwpx 파일 내부 구조(ZIP) 분석",
     "inputSchema": {"type": "object", "properties": {"hwpx_path": {"type": "string"}}, "required": ["hwpx_path"]}},
    {"name": "validate_hwpx", "description": "hwpx 문서 구조 유효성 검증",
     "inputSchema": {"type": "object", "properties": {"hwpx_path": {"type": "string"}}, "required": ["hwpx_path"]}},
]


def handle_tool(name: str, args: dict) -> dict:
    handlers = {
        "convert_md_to_hwpx": lambda: convert_md_to_hwpx(args["md_path"], args.get("output_path", ""), args.get("title", ""), args.get("author", "")),
        "analyze_hwpx": lambda: analyze_hwpx(args["hwpx_path"]),
        "validate_hwpx": lambda: validate_hwpx(args["hwpx_path"]),
    }
    handler = handlers.get(name)
    if handler:
        return handler()
    return {"error": f"Unknown tool: {name}"}


if __name__ == "__main__":
    run_server("sm-hwpx-builder", TOOLS, handle_tool)
