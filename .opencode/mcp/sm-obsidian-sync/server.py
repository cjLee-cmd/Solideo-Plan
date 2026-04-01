"""SM_obsidian_sync MCP Server (stdio) - Obsidian Vault 문서 저장/조회"""

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_stdio import run_server


def save_document(vault_path: str, project_name: str, doc_type: str, file_name: str, content: str, tags: list = None) -> dict:
    target_dir = os.path.join(vault_path, project_name, doc_type)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, file_name)
    frontmatter = f"---\nproject: {project_name}\ntype: {doc_type}\ncreated: {datetime.now().strftime('%Y-%m-%d')}\nauthor: SolCode_Lab\ntags: [{', '.join(tags or [])}]\n---\n\n"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)
    return {"path": target_path, "success": True}


def list_documents(vault_path: str, project_name: str = "", doc_type: str = "") -> dict:
    search_path = vault_path
    if project_name:
        search_path = os.path.join(search_path, project_name)
    if doc_type:
        search_path = os.path.join(search_path, doc_type)
    if not os.path.isdir(search_path):
        return {"files": [], "error": f"Path not found: {search_path}"}
    files = []
    for root, _, fnames in os.walk(search_path):
        for fname in fnames:
            if fname.endswith(".md"):
                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, vault_path)
                files.append({"path": rel_path, "size": os.path.getsize(full_path),
                              "modified": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()})
    return {"files": files}


def read_document(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    with open(file_path, "r", encoding="utf-8") as f:
        return {"content": f.read(), "path": file_path}


def organize_vault(vault_path: str) -> dict:
    removed = []
    for root, dirs, files in os.walk(vault_path, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                removed.append(os.path.relpath(dir_path, vault_path))
    return {"removed_empty_dirs": removed}


TOOLS = [
    {"name": "save_document", "description": "문서를 Obsidian Vault에 저장 (YAML frontmatter 자동 생성)",
     "inputSchema": {"type": "object", "properties": {
         "vault_path": {"type": "string", "description": "Vault 루트 경로"},
         "project_name": {"type": "string", "description": "프로젝트명 (폴더명)"},
         "doc_type": {"type": "string", "description": "문서 유형 (design/analysis/test_report/review/minutes/proposal)"},
         "file_name": {"type": "string", "description": "파일명"},
         "content": {"type": "string", "description": "문서 내용"},
         "tags": {"type": "array", "items": {"type": "string"}, "description": "태그 목록"},
     }, "required": ["vault_path", "project_name", "doc_type", "file_name", "content"]}},
    {"name": "list_documents", "description": "Vault 내 문서 목록 조회",
     "inputSchema": {"type": "object", "properties": {
         "vault_path": {"type": "string"}, "project_name": {"type": "string", "default": ""}, "doc_type": {"type": "string", "default": ""}
     }, "required": ["vault_path"]}},
    {"name": "read_document", "description": "Vault에서 문서 읽기",
     "inputSchema": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}},
    {"name": "organize_vault", "description": "빈 폴더 정리",
     "inputSchema": {"type": "object", "properties": {"vault_path": {"type": "string"}}, "required": ["vault_path"]}},
]


def handle_tool(name: str, args: dict) -> dict:
    handlers = {
        "save_document": lambda: save_document(args["vault_path"], args["project_name"], args["doc_type"], args["file_name"], args["content"], args.get("tags")),
        "list_documents": lambda: list_documents(args["vault_path"], args.get("project_name", ""), args.get("doc_type", "")),
        "read_document": lambda: read_document(args["file_path"]),
        "organize_vault": lambda: organize_vault(args["vault_path"]),
    }
    handler = handlers.get(name)
    if handler:
        return handler()
    return {"error": f"Unknown tool: {name}"}


if __name__ == "__main__":
    run_server("sm-obsidian-sync", TOOLS, handle_tool)
