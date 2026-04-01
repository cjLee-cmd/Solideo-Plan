"""MCP stdio transport 공통 모듈. 각 서버에서 import하여 사용한다."""

import json
import sys


def send_response(id, result):
    """JSON-RPC 응답을 stdout으로 전송한다."""
    msg = json.dumps({"jsonrpc": "2.0", "id": id, "result": result}, ensure_ascii=False)
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def send_error(id, code, message):
    """JSON-RPC 에러를 stdout으로 전송한다."""
    msg = json.dumps({"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}}, ensure_ascii=False)
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def run_server(server_name: str, tools: list, tool_handler):
    """
    stdio 기반 MCP 서버 메인 루프.

    Args:
        server_name: 서버 이름 (로깅용)
        tools: tools/list 응답에 포함할 도구 정의 리스트
        tool_handler: tools/call 시 호출되는 함수. (tool_name, arguments) -> dict
    """
    sys.stderr.write(f"{server_name} MCP server started (stdio)\n")
    sys.stderr.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        id = msg.get("id")
        method = msg.get("method", "")

        if method == "initialize":
            send_response(id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": server_name, "version": "1.0.0"},
            })
        elif method == "notifications/initialized":
            pass  # 알림이므로 응답 불필요
        elif method == "tools/list":
            send_response(id, {"tools": tools})
        elif method == "tools/call":
            params = msg.get("params", {})
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            try:
                result = tool_handler(tool_name, arguments)
                text = json.dumps(result, ensure_ascii=False, indent=2)
                send_response(id, {"content": [{"type": "text", "text": text}]})
            except Exception as e:
                send_response(id, {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True})
        elif method == "ping":
            send_response(id, {})
        else:
            if id is not None:
                send_error(id, -32601, f"Method not found: {method}")
