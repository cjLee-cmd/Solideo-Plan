# SolCode_Lab 전체 설치 및 운영 가이드

## 1. 프로젝트 구조

```
01_plan_notion/
├── 01_Docs/                    # MCP 서버별 폐쇄망 의존성 설치 가이드
│   ├── sm-test-runner_설치가이드.md
│   ├── sm-diff-viewer_설치가이드.md
│   ├── sm-hwpx-builder_설치가이드.md
│   └── sm-obsidian-sync_설치가이드.md
├── 02_Flow/                    # Flow 요소 기획 문서 (Sol.1~6)
│   ├── Sol_1_계획/             # SK_design_spec 등 4개 요소
│   ├── Sol_2_분석/             # SK_code_analyze 등 5개 요소
│   ├── Sol_3_생성/             # SK_code_gen 등 8개 요소
│   ├── Sol_4_수정/             # SK_code_modify 등 7개 요소
│   ├── Sol_5_리뷰/             # SK_code_review 등 6개 요소
│   ├── Sol_6_문서생성/         # SK_doc_md 등 6개 요소
│   └── SETUP_GUIDE.md          # 이 문서
├── 03_Tools/                   # 폐쇄망 배포용 실행 파일 패키지
│   ├── skills/                 # opencode Skill 16개 (SKILL.md)
│   ├── agents/                 # opencode Agent 6개
│   ├── mcp_servers/            # MCP 서버 4개 (Python)
│   ├── md2hwpx/                # hwpx 변환기
│   ├── install.sh              # 원클릭 설치 스크립트
│   └── INSTALL_GUIDE.md        # 도구 설치 상세 가이드
├── jun.md                      # 프로젝트 기획서
└── CLAUDE.md                   # Claude Code 프로젝트 지침
```

## 2. 설치 순서

### 2.1 인터넷망에서 준비

1. 이 Git 저장소를 클론한다

```bash
git clone https://github.com/cjLee-cmd/Solideo-Plan.git
```

2. 외부 의존성 패키지를 오프라인으로 다운로드한다 (`01_Docs/` 가이드 참조)

| 의존성 | 필요 조건 | 가이드 문서 |
|--------|-----------|------------|
| pytest/JUnit/Jest | 테스트 실행 시 | 01_Docs/sm-test-runner_설치가이드.md |
| Git | 코드 diff 비교 시 | 01_Docs/sm-diff-viewer_설치가이드.md |
| Python 3.9+ | 필수 (모든 MCP 공통) | 01_Docs/sm-obsidian-sync_설치가이드.md |

3. 다운로드한 패키지와 이 저장소를 USB 등으로 폐쇄망에 복사한다

### 2.2 폐쇄망에서 설치

#### Step 1: 사전 요구사항 설치

```bash
# Python 3 설치 (01_Docs/sm-obsidian-sync_설치가이드.md 참조)
# Git 설치 (01_Docs/sm-diff-viewer_설치가이드.md 참조)
# 테스트 프레임워크 설치 (01_Docs/sm-test-runner_설치가이드.md 참조)
```

#### Step 2: opencode IDE 설치

```bash
# opencode 설치 파일을 USB로 복사 후 실행
# 설치 확인
opencode --version
```

#### Step 3: SolCode_Lab 도구 설치

```bash
cd 03_Tools
bash install.sh
```

또는 수동 설치: `03_Tools/INSTALL_GUIDE.md` 참조

#### Step 4: 설치 확인

```bash
# Skill 16개 확인
opencode debug skill | python3 -c "
import sys,json
skills = [s for s in json.load(sys.stdin) if s['name'].startswith('sk-')]
print(f'Skills: {len(skills)}개')
for s in skills:
    print(f'  {s[\"name\"]}: {s[\"description\"][:40]}...')
"

# Agent 6개 확인
opencode agent list 2>&1 | grep "sa-"

# MCP 4개 확인 (모두 connected 표시되어야 함)
opencode mcp list
```

## 3. 사용 방법

### 3.1 opencode 실행

```bash
cd /path/to/project    # 작업할 프로젝트 디렉토리로 이동
opencode               # TUI 실행
```

### 3.2 Skill 호출

opencode TUI에서 `/skill-name`으로 호출한다.

| 단계 | Skill 호출 | 산출물 |
|------|-----------|--------|
| 계획 | `/sk-design-spec` | 90_Result_Doc/design.md |
| 계획 검증 | `/sk-design-review` | 90_Result_Doc/review_result.md |
| 분석 | `/sk-code-analyze` | 90_Result_Doc/analysis_result.md |
| 분석 보고 | `/sk-analyze-doc` | 90_Result_Doc/analysis_report.md |
| 코드 생성 | `/sk-code-gen` | 소스코드 + 90_Result_Doc/file_manifest.md |
| 테스트 생성 | `/sk-test-gen` | 테스트코드 + 90_Result_Doc/test_manifest.md |
| 테스트 실행 | `/sk-test-run` | 90_Result_Doc/test_result.md |
| 생성 보고 | `/sk-gen-report` | 90_Result_Doc/generation_report.md |
| 코드 수정 | `/sk-code-modify` | 수정코드 + 90_Result_Doc/change_summary.md |
| 영향 분석 | `/sk-impact-check` | 90_Result_Doc/impact_report.md |
| 수정 보고 | `/sk-modify-report` | 90_Result_Doc/modification_report.md |
| 코드 리뷰 | `/sk-code-review` | 90_Result_Doc/code_review_result.md |
| 보안 리뷰 | `/sk-security-review` | 90_Result_Doc/security_review_result.md |
| 리뷰 보고 | `/sk-review-report` | 90_Result_Doc/review_report.md |
| 문서 생성 | `/sk-doc-md` | 90_Result_Doc/{문서유형}.md |
| hwpx 변환 | `/sk-doc-hwpx` | 90_Result_Doc/{파일명}.hwpx |

### 3.3 Agent 호출

Agent는 Workflow를 통합하고 있어 여러 Skill을 자동으로 순차 실행한다.

```
@sa-architect    # 계획: 설계 생성 → 검증 → 확정
@sa-analyzer     # 분석: 코드 분석 → 보고서 작성
@sa-generator    # 생성: 코드 생성 → 테스트 → 보고서
@sa-modifier     # 수정: 코드 수정 → 영향분석 → 테스트 → 보고서
@sa-reviewer     # 리뷰: 코드 리뷰 + 보안 리뷰 → 종합 보고서
@sa-documenter   # 문서: 마크다운 생성 → hwpx 변환 → 저장
```

### 3.4 MCP 도구 직접 사용

opencode TUI에서 `use mcp-name`으로 참조한다.

```
이 프로젝트의 테스트를 실행해줘. use sm-test-runner
마지막 커밋과 diff를 보여줘. use sm-diff-viewer
analysis_result.md를 hwpx로 변환해줘. use sm-hwpx-builder
이 문서를 Vault에 저장해줘. use sm-obsidian-sync
```

## 4. 워크플로우 파이프라인

전체 개발 흐름은 아래 순서로 진행된다.

```
[Sol.1 계획] @sa-architect
   design.md 생성 → 사용자 검증 → 확정
       |
       v
[Sol.3 생성] @sa-generator          [Sol.2 분석] @sa-analyzer
   코드 생성 → 테스트 → 보고서         기존 코드 분석 → 보고서
       |                                    |
       v                                    v
[Sol.4 수정] @sa-modifier
   코드 수정 → 영향분석 → 테스트 → 보고서
       |
       v
[Sol.5 리뷰] @sa-reviewer
   코드 리뷰 + 보안 리뷰 → 종합 보고서
       |
       v
[Sol.6 문서] @sa-documenter
   마크다운 → (필요시) hwpx → Vault 저장
```

## 5. 산출물 관리 규칙

- **저장 위치**: 프로젝트 내 `90_Result_Doc/` 디렉토리
- **파일 형식**: 마크다운(.md)만 사용. .json 생성 금지.
- **hwpx 파일**: 마크다운 원본과 함께 90_Result_Doc/에 저장
- **Obsidian Vault**: sm-obsidian-sync MCP를 통해 프로젝트별/문서유형별 폴더에 정리

## 6. 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| Skill이 안 보임 | 파일 경로 오류 | `opencode debug skill`로 경로 확인 |
| MCP failed 표시 | Python 경로 오류 | opencode.json의 command에서 python3 경로 확인 |
| hwpx 변환 실패 | md2hwpx.py 경로 | sm-hwpx-builder/server.py의 MD2HWPX 경로 확인 |
| .json 파일 생성됨 | LLM이 지시 무시 | opencode 재시작. opencode.md 글로벌 규칙 확인 |
| Skill 변경 미반영 | instructions 캐시 | opencode 재시작 필요 |
| Agent가 안 보임 | 파일명 오류 | ~/.config/opencode/agent/sa-*.md 확인 |
