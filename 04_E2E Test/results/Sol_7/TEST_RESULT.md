# Sol_7 문서생성 — 테스트 결과

실행일: 2026-04-02
모델: opencode/qwen3.6-plus-free
환경: macOS (인터넷망)

## 결과 요약

| TC | 테스트 | 결과 | 산출물 |
|----|--------|------|--------|
| TC-7.1 | sk-doc-md (설계서) | ⏳ 미실행 | design.md 원본 필요 |
| TC-7.2 | sk-doc-md (테스트보고서) | ✅ PASS | test_report.md (10섹션, 표 169줄) |
| TC-7.3 | sk-doc-hwpx (자동 변환) | ⏳ 미실행 | sm-hwpx-builder MCP 필요 |
| TC-7.4 | sk-doc-hwpx (공문 템플릿) | ⏳ 미실행 | sm-hwpx-builder MCP 필요 |
| TC-7.5 | sa-documenter 통합 | ⏳ 미실행 | HWPX + Agent 멀티턴 |

## TC-7.2 상세

```bash
opencode run --dir /tmp/e2e_sol7 -m "opencode/qwen3.6-plus-free" \
  "/sk-doc-md review_report.md를 기반으로 정식 테스트 보고서를 작성해줘"
```

- Sol_5의 review_report.md를 원본으로 사용
- 10개 섹션 생성, 표 169줄
- 문서 유형 "테스트 보고서"로 판별
- 42/100 점수, D등급, 배포 불가 판정 반영
- .json 파일 0개

## TC-7.1 미실행 사유

설계서 유형 문서 생성 테스트. Sol_1에서 생성된 design.md를 원본으로 사용하면 된다.

### 로컬 실행 방법

```bash
mkdir -p /tmp/e2e_sol7_tc71/90_Result_Doc && cd /tmp/e2e_sol7_tc71 && git init
cp /path/to/design.md 90_Result_Doc/design.md

opencode run --dir . -m "모델명" \
  "/sk-doc-md design.md를 기반으로 정식 설계서 문서를 작성해줘"

# 검증
ls 90_Result_Doc/*설계*.md 2>/dev/null || ls 90_Result_Doc/*design*.md
find 90_Result_Doc/ -name "*.json"
```

## TC-7.3, TC-7.4 미실행 사유

HWPX 변환은 **sm-hwpx-builder MCP 서버가 연결**되어 있어야 한다.
opencode run 단일 명령에서 MCP 서버 연결이 보장되지 않음.

### 로컬 실행 방법 (opencode TUI 권장)

```bash
# sm-hwpx-builder MCP가 정상 연결된 상태에서 실행
mkdir -p /tmp/e2e_sol7_hwpx/90_Result_Doc && cd /tmp/e2e_sol7_hwpx && git init
cp /path/to/test_report.md 90_Result_Doc/test_report.md

# TC-7.3: 자동 변환
opencode run --dir . -m "모델명" \
  "/sk-doc-hwpx 테스트 보고서를 hwpx로 변환해줘"

# 검증
find 90_Result_Doc/ -name "*.hwpx"
find 90_Result_Doc/ -name "*.json"

# TC-7.4: 공문 템플릿 변환 (opencode TUI 권장)
opencode
# opencode 내에서:
# > /sk-doc-hwpx 리뷰 보고서를 공문(gonmun) 양식으로 hwpx 변환해줘
```

### sm-hwpx-builder MCP 연결 확인

```bash
# opencode TUI에서 MCP 상태 확인
opencode
# opencode 내에서:
# > /mcp
# sm-hwpx-builder가 connected 상태인지 확인
```

## TC-7.5 미실행 사유

sa-documenter Agent가 문서 유형 판별 → sk-doc-md → sk-doc-hwpx → 저장 흐름을 자동으로 진행하는지 검증 필요. HWPX 변환 포함이므로 MCP 연결 + Agent 멀티턴 필요.

### 로컬 실행 방법

```bash
mkdir -p /tmp/e2e_sol7_tc75/90_Result_Doc && cd /tmp/e2e_sol7_tc75 && git init
cp /path/to/design.md 90_Result_Doc/design.md

opencode run --dir . -m "모델명" --agent sa-documenter \
  "design.md 기반으로 설계서를 작성하고 hwpx로도 변환해줘"

# 검증
find 90_Result_Doc/ -name "*.md" | head -10
find 90_Result_Doc/ -name "*.hwpx"
find 90_Result_Doc/ -name "*.json"
```
