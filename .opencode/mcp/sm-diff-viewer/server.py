"""SM_diff_viewer MCP Server (stdio) - 수정 전후 코드 차이 비교"""

import json
import subprocess
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_stdio import run_server


def get_diff(project_path: str, file_path: str = "", base: str = "HEAD") -> dict:
    cmd = ["git", "diff", base]
    if file_path:
        cmd.extend(["--", file_path])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_path, timeout=30)
        return {"diff": result.stdout[:5000], "error": result.stderr if result.returncode != 0 else None}
    except Exception as e:
        return {"error": str(e)}


def get_project_diff(project_path: str, base: str = "HEAD~1") -> dict:
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
    cmd = ["git", "diff", "--numstat", base]
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


TOOLS = [
    {"name": "get_diff", "description": "파일별 diff 비교",
     "inputSchema": {"type": "object", "properties": {
         "project_path": {"type": "string"}, "file_path": {"type": "string", "default": ""}, "base": {"type": "string", "default": "HEAD"}
     }, "required": ["project_path"]}},
    {"name": "get_project_diff", "description": "프로젝트 전체 변경 파일 목록",
     "inputSchema": {"type": "object", "properties": {
         "project_path": {"type": "string"}, "base": {"type": "string", "default": "HEAD~1"}
     }, "required": ["project_path"]}},
    {"name": "get_stat", "description": "변경 통계 (추가/삭제 라인, 파일 수)",
     "inputSchema": {"type": "object", "properties": {
         "project_path": {"type": "string"}, "base": {"type": "string", "default": "HEAD~1"}
     }, "required": ["project_path"]}},
]


def handle_tool(name: str, args: dict) -> dict:
    if name == "get_diff":
        return get_diff(args["project_path"], args.get("file_path", ""), args.get("base", "HEAD"))
    elif name == "get_project_diff":
        return get_project_diff(args["project_path"], args.get("base", "HEAD~1"))
    elif name == "get_stat":
        return get_stat(args["project_path"], args.get("base", "HEAD~1"))
    return {"error": f"Unknown tool: {name}"}


if __name__ == "__main__":
    run_server("sm-diff-viewer", TOOLS, handle_tool)
