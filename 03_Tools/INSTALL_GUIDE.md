# SolCode_Lab opencode 도구 설치 가이드

## 사전 요구사항

- Python 3.9 이상
- opencode IDE 설치 완료
- (선택) Git 2.x 이상 -- sm-diff-viewer 사용 시 필요

## 빠른 설치

```bash
cd 03_Tools
bash install.sh
```

설치 스크립트가 아래 5단계를 자동 수행한다.

## 수동 설치

### 1단계: Skills 설치 (16개)

```bash
cp -r 03_Tools/skills/* ~/.config/opencode/skills/
```

설치 경로: `~/.config/opencode/skills/<skill-name>/SKILL.md`

| Skill | 설명 |
|-------|------|
| sk-design-spec | Speckit 기반 설계 문서 생성 |
| sk-design-review | 설계 문서 검증/승인 |
| sk-code-analyze | 소스코드 분석 |
| sk-analyze-doc | 분석 결과 보고서 작성 |
| sk-code-gen | design.md 기반 코드 생성 |
| sk-test-gen | 테스트 코드 생성 |
| sk-test-run | 테스트 실행/결과 수집 |
| sk-gen-report | 코드 생성 종합 보고서 |
| sk-code-modify | 소스코드 수정 |
| sk-impact-check | 수정 영향범위 검토 |
| sk-modify-report | 수정 종합 보고서 |
| sk-code-review | 코드 품질 리뷰 |
| sk-security-review | 보안 취약점 점검 |
| sk-review-report | 리뷰 종합 보고서 |
| sk-doc-md | 마크다운 문서 생성 |
| sk-doc-hwpx | hwpx(한글) 변환 |

### 2단계: Agents 설치 (6개)

```bash
cp 03_Tools/agents/sa-*.md ~/.config/opencode/agent/
```

설치 경로: `~/.config/opencode/agent/<agent-name>.md`

| Agent | 역할 | 통합된 Workflow |
|-------|------|----------------|
| sa-architect | 설계 총괄 | SW_planning |
| sa-analyzer | 코드 분석 총괄 | SW_analysis |
| sa-generator | 코드 생성 총괄 | SW_generation |
| sa-modifier | 코드 수정 총괄 | SW_modification |
| sa-reviewer | 코드 리뷰 총괄 | SW_review |
| sa-documenter | 문서 생성 총괄 | SW_documentation |

### 3단계: md2hwpx 변환기 설치

```bash
mkdir -p ~/tools/md2hwpx
cp 03_Tools/md2hwpx/* ~/tools/md2hwpx/
```

설치 파일:
- `md2hwpx.py` -- 마크다운 → hwpx 변환기 (Python 표준 라이브러리만 사용)
- `Skeleton.hwpx` -- hwpx 기본 템플릿
- `hwpx-format.md` -- hwpx 포맷 참고 문서

### 4단계: MCP 서버 설치 (4개)

```bash
mkdir -p ~/.config/opencode/mcp
cp 03_Tools/mcp_servers/mcp_stdio.py ~/.config/opencode/mcp/
for srv in sm-test-runner sm-diff-viewer sm-hwpx-builder sm-obsidian-sync; do
  mkdir -p ~/.config/opencode/mcp/$srv
  cp 03_Tools/mcp_servers/$srv/server.py ~/.config/opencode/mcp/$srv/
done
```

설치 후 각 서버의 `server.py`에서 `sys.path.insert` 경로를 실제 설치 경로로 수정해야 한다:

```python
# 수정 전
sys.path.insert(0, "/Users/cjlee/.config/opencode/mcp")
# 수정 후 (본인 환경에 맞게)
sys.path.insert(0, "/home/사용자/.config/opencode/mcp")
```

sm-hwpx-builder의 `MD2HWPX`, `SKELETON` 경로도 수정한다:

```python
MD2HWPX = os.path.expanduser("~/tools/md2hwpx/md2hwpx.py")
SKELETON = os.path.expanduser("~/tools/md2hwpx/Skeleton.hwpx")
```

| MCP 서버 | 역할 | 외부 의존성 |
|----------|------|------------|
| sm-test-runner | 테스트 실행/결과 수집 | pytest/JUnit/Jest 등 (프레임워크별) |
| sm-diff-viewer | 코드 diff 비교 | Git |
| sm-hwpx-builder | hwpx 변환/검증 | 없음 (md2hwpx.py 사용) |
| sm-obsidian-sync | Obsidian Vault 관리 | 없음 |

### 5단계: opencode.json에 MCP 등록

`~/.config/opencode/opencode.json`의 `mcp` 섹션에 추가:

```json
{
  "instructions": ["~/.config/opencode/opencode.md"],
  "mcp": {
    "sm-test-runner": {
      "type": "local",
      "command": ["python3", "~/.config/opencode/mcp/sm-test-runner/server.py"],
      "enabled": true
    },
    "sm-diff-viewer": {
      "type": "local",
      "command": ["python3", "~/.config/opencode/mcp/sm-diff-viewer/server.py"],
      "enabled": true
    },
    "sm-hwpx-builder": {
      "type": "local",
      "command": ["python3", "~/.config/opencode/mcp/sm-hwpx-builder/server.py"],
      "enabled": true
    },
    "sm-obsidian-sync": {
      "type": "local",
      "command": ["python3", "~/.config/opencode/mcp/sm-obsidian-sync/server.py"],
      "enabled": true
    }
  }
}
```

## 설치 확인

```bash
# Skill 확인 (16개)
opencode debug skill | python3 -c "import sys,json; print(len([s for s in json.load(sys.stdin) if s['name'].startswith('sk-')]))"

# Agent 확인
opencode agent list 2>&1 | grep "sa-"

# MCP 확인 (4개 connected)
opencode mcp list
```

## 산출물 저장 규칙

모든 Skill/Agent의 산출물은 아래 규칙을 따른다:

- **저장 경로**: 프로젝트 내 `90_Result_Doc/` 디렉토리
- **파일 형식**: 마크다운(.md)만 사용. .json 파일 생성 금지.
- 디렉토리가 없으면 자동 생성됨

## 문제 해결

### MCP 서버 연결 실패

```bash
# 개별 서버 동작 테스트
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python3 ~/.config/opencode/mcp/sm-obsidian-sync/server.py
```

### python3 명령을 찾을 수 없음

opencode.json의 `command`에서 `python3`을 `python`으로 변경하라.

### Skill이 로딩되지 않음

opencode를 재시작하라. Skill 파일은 호출 시 읽히지만, instructions는 세션 시작 시 한 번만 로딩된다.
