"""SM_obsidian_sync MCP Server - Obsidian Vault 문서 저장/조회"""

import json
import os
import sys
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler


def save_document(vault_path: str, project_name: str, doc_type: str, file_name: str, content: str, tags: list = None) -> dict:
    """문서를 Obsidian Vault에 저장한다. YAML frontmatter를 자동 생성한다."""
    target_dir = os.path.join(vault_path, project_name, doc_type)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, file_name)

    frontmatter = f"""---
project: {project_name}
type: {doc_type}
created: {datetime.now().strftime('%Y-%m-%d')}
author: SolCode_Lab
tags: [{', '.join(tags or [])}]
---

"""
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

    return {"path": target_path, "success": True}


def list_documents(vault_path: str, project_name: str = "", doc_type: str = "") -> dict:
    """Vault 내 문서 목록을 반환한다."""
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
    """Vault에서 문서를 읽는다."""
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    with open(file_path, "r", encoding="utf-8") as f:
        return {"content": f.read(), "path": file_path}


def organize_vault(vault_path: str) -> dict:
    """빈 폴더를 정리한다."""
    removed = []
    for root, dirs, files in os.walk(vault_path, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                removed.append(os.path.relpath(dir_path, vault_path))
    return {"removed_empty_dirs": removed}


class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}
        method = body.get("method", "")
        params = body.get("params", {})

        if method == "tools/list":
            response = {"tools": [
                {"name": "save_document", "description": "문서를 Vault에 저장",
                 "inputSchema": {"type": "object", "properties": {
                     "vault_path": {"type": "string"}, "project_name": {"type": "string"},
                     "doc_type": {"type": "string"}, "file_name": {"type": "string"},
                     "content": {"type": "string"}, "tags": {"type": "array", "items": {"type": "string"}}
                 }, "required": ["vault_path", "project_name", "doc_type", "file_name", "content"]}},
                {"name": "list_documents", "description": "문서 목록 조회",
                 "inputSchema": {"type": "object", "properties": {
                     "vault_path": {"type": "string"}, "project_name": {"type": "string", "default": ""},
                     "doc_type": {"type": "string", "default": ""}
                 }, "required": ["vault_path"]}},
                {"name": "read_document", "description": "문서 읽기",
                 "inputSchema": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}},
                {"name": "organize_vault", "description": "Vault 폴더 정리",
                 "inputSchema": {"type": "object", "properties": {"vault_path": {"type": "string"}}, "required": ["vault_path"]}},
            ]}
        elif method == "tools/call":
            tool_name = params.get("name", "")
            args = params.get("arguments", {})
            handlers = {
                "save_document": lambda: save_document(args["vault_path"], args["project_name"], args["doc_type"], args["file_name"], args["content"], args.get("tags")),
                "list_documents": lambda: list_documents(args["vault_path"], args.get("project_name", ""), args.get("doc_type", "")),
                "read_document": lambda: read_document(args["file_path"]),
                "organize_vault": lambda: organize_vault(args["vault_path"]),
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
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3013
    server = HTTPServer(("127.0.0.1", port), MCPHandler)
    print(f"SM_obsidian_sync MCP server running on port {port}", file=sys.stderr)
    server.serve_forever()
