#!/bin/bash
# SolCode_Lab opencode 도구 폐쇄망 설치 스크립트
# 이 스크립트를 03_Tools/ 디렉토리에서 실행한다.
# 사용법: bash install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OPENCODE_DIR="$HOME/.config/opencode"
TOOLS_DIR="$HOME/tools"

echo "=== SolCode_Lab opencode 도구 설치 ==="
echo "설치 경로: $OPENCODE_DIR"
echo ""

# 1. Skills 설치
echo "[1/5] Skills 설치 (16개)..."
mkdir -p "$OPENCODE_DIR/skills"
cp -r "$SCRIPT_DIR/skills/"* "$OPENCODE_DIR/skills/"
echo "  -> $(ls "$OPENCODE_DIR/skills/" | wc -l)개 설치됨"

# 2. Agents 설치
echo "[2/5] Agents 설치..."
mkdir -p "$OPENCODE_DIR/agent"
cp "$SCRIPT_DIR/agents/"*.md "$OPENCODE_DIR/agent/"
echo "  -> $(ls "$OPENCODE_DIR/agent/"sa-*.md 2>/dev/null | wc -l)개 설치됨"

# 3. md2hwpx 변환기 설치
echo "[3/5] md2hwpx 변환기 설치..."
mkdir -p "$TOOLS_DIR/md2hwpx"
cp "$SCRIPT_DIR/md2hwpx/md2hwpx.py" "$TOOLS_DIR/md2hwpx/"
cp "$SCRIPT_DIR/md2hwpx/Skeleton.hwpx" "$TOOLS_DIR/md2hwpx/"
cp "$SCRIPT_DIR/md2hwpx/hwpx-format.md" "$TOOLS_DIR/md2hwpx/"
echo "  -> $TOOLS_DIR/md2hwpx/ 설치됨"

# 4. MCP 서버 설치
echo "[4/5] MCP 서버 설치 (4개)..."
mkdir -p "$OPENCODE_DIR/mcp"
cp "$SCRIPT_DIR/mcp_servers/mcp_stdio.py" "$OPENCODE_DIR/mcp/"
for srv in sm-test-runner sm-diff-viewer sm-hwpx-builder sm-obsidian-sync; do
  mkdir -p "$OPENCODE_DIR/mcp/$srv"
  cp "$SCRIPT_DIR/mcp_servers/$srv/server.py" "$OPENCODE_DIR/mcp/$srv/"
done
# mcp_stdio.py import 경로를 설치 경로로 수정
for srv in sm-test-runner sm-diff-viewer sm-hwpx-builder sm-obsidian-sync; do
  sed -i "s|sys.path.insert(0, .*)|sys.path.insert(0, \"$OPENCODE_DIR/mcp\")|" "$OPENCODE_DIR/mcp/$srv/server.py" 2>/dev/null || \
  sed -i '' "s|sys.path.insert(0, .*)|sys.path.insert(0, \"$OPENCODE_DIR/mcp\")|" "$OPENCODE_DIR/mcp/$srv/server.py"
done
# sm-hwpx-builder의 md2hwpx 경로 수정
sed -i "s|MD2HWPX = .*|MD2HWPX = os.path.expanduser(\"$TOOLS_DIR/md2hwpx/md2hwpx.py\")|" "$OPENCODE_DIR/mcp/sm-hwpx-builder/server.py" 2>/dev/null || \
sed -i '' "s|MD2HWPX = .*|MD2HWPX = os.path.expanduser(\"$TOOLS_DIR/md2hwpx/md2hwpx.py\")|" "$OPENCODE_DIR/mcp/sm-hwpx-builder/server.py"
sed -i "s|SKELETON = .*|SKELETON = os.path.expanduser(\"$TOOLS_DIR/md2hwpx/Skeleton.hwpx\")|" "$OPENCODE_DIR/mcp/sm-hwpx-builder/server.py" 2>/dev/null || \
sed -i '' "s|SKELETON = .*|SKELETON = os.path.expanduser(\"$TOOLS_DIR/md2hwpx/Skeleton.hwpx\")|" "$OPENCODE_DIR/mcp/sm-hwpx-builder/server.py"
echo "  -> 4개 MCP 서버 설치됨"

# 5. opencode.json에 MCP 서버 등록
echo "[5/5] opencode.json MCP 등록..."
PYTHON_CMD="python3"
command -v python3 >/dev/null 2>&1 || PYTHON_CMD="python"

if [ -f "$OPENCODE_DIR/opencode.json" ]; then
  # 기존 설정에 MCP 추가 (python으로 JSON 병합)
  $PYTHON_CMD -c "
import json, os
config_path = '$OPENCODE_DIR/opencode.json'
with open(config_path) as f:
    config = json.load(f)
mcp = config.setdefault('mcp', {})
for srv in ['sm-test-runner', 'sm-diff-viewer', 'sm-hwpx-builder', 'sm-obsidian-sync']:
    mcp[srv] = {
        'type': 'local',
        'command': ['$PYTHON_CMD', '$OPENCODE_DIR/mcp/' + srv + '/server.py'],
        'enabled': True
    }
config.setdefault('instructions', ['~/.config/opencode/opencode.md'])
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('  -> opencode.json 업데이트됨')
"
else
  cat > "$OPENCODE_DIR/opencode.json" << JSONEOF
{
  "\$schema": "https://opencode.ai/config.json",
  "instructions": ["~/.config/opencode/opencode.md"],
  "mcp": {
    "sm-test-runner": {"type": "local", "command": ["$PYTHON_CMD", "$OPENCODE_DIR/mcp/sm-test-runner/server.py"], "enabled": true},
    "sm-diff-viewer": {"type": "local", "command": ["$PYTHON_CMD", "$OPENCODE_DIR/mcp/sm-diff-viewer/server.py"], "enabled": true},
    "sm-hwpx-builder": {"type": "local", "command": ["$PYTHON_CMD", "$OPENCODE_DIR/mcp/sm-hwpx-builder/server.py"], "enabled": true},
    "sm-obsidian-sync": {"type": "local", "command": ["$PYTHON_CMD", "$OPENCODE_DIR/mcp/sm-obsidian-sync/server.py"], "enabled": true}
  }
}
JSONEOF
  echo "  -> opencode.json 새로 생성됨"
fi

echo ""
echo "=== 설치 완료 ==="
echo "opencode를 재시작하면 적용됩니다."
echo ""
echo "검증:"
echo "  opencode debug skill    # Skill 목록 확인"
echo "  opencode mcp list       # MCP 서버 확인"
echo "  opencode agent list     # Agent 목록 확인"
