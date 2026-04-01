"""SM_hwpx_builder MCP Server (stdio) - HWPX 문서 빌드/변환/검증

폐쇄망 내부에서 hwpx 변환 도구와 연동한다.
실제 변환은 python-hwp 또는 자체 hwpx 라이브러리를 사용한다.
"""

import json
import subprocess
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_stdio import run_server


def convert_md_to_hwpx(md_path: str, output_path: str = "") -> dict:
    if not os.path.exists(md_path):
        return {"error": f"File not found: {md_path}"}
    if not output_path:
        output_path = md_path.rsplit(".", 1)[0] + ".hwpx"
    try:
        result = subprocess.run(
            ["python", "-m", "hwpx_converter", "convert", md_path, "-o", output_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return {"output_path": output_path, "success": True}
        return {"error": result.stderr, "success": False}
    except FileNotFoundError:
        return {"error": "hwpx_converter 미설치. 폐쇄망 내부 패키지 저장소에서 설치 필요.", "success": False}


def analyze_hwpx(hwpx_path: str) -> dict:
    if not os.path.exists(hwpx_path):
        return {"error": f"File not found: {hwpx_path}"}
    try:
        result = subprocess.run(
            ["python", "-m", "hwpx_converter", "analyze", hwpx_path],
            capture_output=True, text=True, timeout=30
        )
        return {"analysis": result.stdout, "error": result.stderr if result.returncode != 0 else None}
    except FileNotFoundError:
        return {"error": "hwpx_converter 미설치"}


def build_hwpx(source_dir: str, output_path: str) -> dict:
    if not os.path.isdir(source_dir):
        return {"error": f"Directory not found: {source_dir}"}
    try:
        result = subprocess.run(
            ["python", "-m", "hwpx_converter", "build", source_dir, "-o", output_path],
            capture_output=True, text=True, timeout=30
        )
        return {"output_path": output_path, "success": result.returncode == 0, "error": result.stderr if result.returncode != 0 else None}
    except FileNotFoundError:
        return {"error": "hwpx_converter 미설치"}


def validate_hwpx(hwpx_path: str) -> dict:
    if not os.path.exists(hwpx_path):
        return {"error": f"File not found: {hwpx_path}"}
    try:
        result = subprocess.run(
            ["python", "-m", "hwpx_converter", "validate", hwpx_path],
            capture_output=True, text=True, timeout=30
        )
        return {"valid": result.returncode == 0, "message": result.stdout or result.stderr}
    except FileNotFoundError:
        return {"error": "hwpx_converter 미설치"}


TOOLS = [
    {"name": "convert_md_to_hwpx", "description": "마크다운을 hwpx로 변환",
     "inputSchema": {"type": "object", "properties": {
         "md_path": {"type": "string", "description": "마크다운 파일 경로"},
         "output_path": {"type": "string", "description": "출력 hwpx 경로 (선택)", "default": ""},
     }, "required": ["md_path"]}},
    {"name": "analyze_hwpx", "description": "hwpx 파일 구조 분석",
     "inputSchema": {"type": "object", "properties": {"hwpx_path": {"type": "string"}}, "required": ["hwpx_path"]}},
    {"name": "build_hwpx", "description": "XML 소스로 hwpx 빌드",
     "inputSchema": {"type": "object", "properties": {
         "source_dir": {"type": "string"}, "output_path": {"type": "string"}
     }, "required": ["source_dir", "output_path"]}},
    {"name": "validate_hwpx", "description": "hwpx 문서 구조 검증",
     "inputSchema": {"type": "object", "properties": {"hwpx_path": {"type": "string"}}, "required": ["hwpx_path"]}},
]


def handle_tool(name: str, args: dict) -> dict:
    handlers = {
        "convert_md_to_hwpx": lambda: convert_md_to_hwpx(args["md_path"], args.get("output_path", "")),
        "analyze_hwpx": lambda: analyze_hwpx(args["hwpx_path"]),
        "build_hwpx": lambda: build_hwpx(args["source_dir"], args["output_path"]),
        "validate_hwpx": lambda: validate_hwpx(args["hwpx_path"]),
    }
    handler = handlers.get(name)
    if handler:
        return handler()
    return {"error": f"Unknown tool: {name}"}


if __name__ == "__main__":
    run_server("sm-hwpx-builder", TOOLS, handle_tool)
