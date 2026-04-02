# 04_E2E Test

SolCode_Lab의 각 Flow(Sol_1 ~ Sol_7)를 opencode 환경에서 실제 실행하여 검증하는 E2E 테스트 시나리오 모음.

## 테스트 실행 결과 (2026-04-02)

| Flow | TC | PASS | FAIL | 미실행 | 비고 |
|------|----|------|------|--------|------|
| Sol_1 계획 | 4 | 2 | 0 | 2 | TC-1.3,1.4 멀티턴 Agent |
| Sol_2 분석 | 3 | 2 | 0 | 1 | TC-2.3 Agent 통합 |
| Sol_3 생성 | 5 | 0 | 0 | 5 | 빌드 환경(Maven/JDK) 필요 |
| Sol_4 수정 | 4 | 0 | 0 | 4 | 빌드 환경 필요 |
| Sol_5 리뷰 | 4 | 3 | 0 | 1 | TC-5.4 Agent 통합 |
| Sol_6 E2E | 4 | 0 | 0 | 4 | Playwright + 웹서버 필요 |
| Sol_7 문서 | 5 | 1 | 0 | 4 | HWPX MCP 연결 필요 |
| **합계** | **29** | **8** | **0** | **21** | |

미실행 TC의 로컬 실행 방법은 `results/Sol_*/TEST_RESULT.md`에 상세 기술.

## 테스트 시나리오 목록

| 파일 | 대상 Flow | TC 수 | 핵심 검증 |
|------|-----------|-------|-----------|
| [E2E_Sol1_계획.md](E2E_Sol1_계획.md) | Sol_1 계획 | 4 | sk-design-spec, sk-design-review, sa-architect(Speckit 8단계), SW_planning 통합 |
| [E2E_Sol2_분석.md](E2E_Sol2_분석.md) | Sol_2 분석 | 3 | sk-code-analyze, sk-analyze-doc, sa-analyzer 통합 |
| [E2E_Sol3_생성.md](E2E_Sol3_생성.md) | Sol_3 생성 | 5 | sk-code-gen, sk-test-gen, sk-test-run, sk-gen-report, sa-generator 통합 |
| [E2E_Sol4_수정.md](E2E_Sol4_수정.md) | Sol_4 수정 | 4 | sk-code-modify, sk-impact-check, sk-modify-report, sa-modifier 통합 |
| [E2E_Sol5_리뷰.md](E2E_Sol5_리뷰.md) | Sol_5 리뷰 | 4 | sk-code-review, sk-security-review, sk-review-report, sa-reviewer 통합 |
| [E2E_Sol6_E2E테스트.md](E2E_Sol6_E2E테스트.md) | Sol_6 E2E테스트 | 4 | sk-e2e-test-gen, sk-e2e-test-run, sk-e2e-report, sa-e2e-tester+Playwright 통합 |
| [E2E_Sol7_문서생성.md](E2E_Sol7_문서생성.md) | Sol_7 문서생성 | 5 | sk-doc-md(설계서/보고서), sk-doc-hwpx(자동/템플릿), sa-documenter 통합 |

**총 29개 테스트 케이스**

## 테스트 환경

| 항목 | 인터넷망 (검증용) | 폐쇄망 (실제) |
|------|-------------------|---------------|
| IDE | opencode CLI (`opencode run`) | opencode TUI/CLI |
| 모델 | `opencode/qwen3.6-plus-free` | oss-120b |
| 인프라 | macOS | H100 x 4 EA |
| MCP | sm-hwpx-builder 등 (일부 미연결) | 전체 연결 |

## 실행 방법

### 사전 준비 (필수)

```bash
# 1. 테스트 디렉토리 생성 + git init (opencode 프로젝트 인식 필수)
mkdir -p /tmp/e2e_test/90_Result_Doc && cd /tmp/e2e_test && git init

# 2. 테스트 대상 코드 복사 (Sol_2, 4, 5용)
cp -r testcode/02_samplecode/* /tmp/e2e_test/
```

### opencode run CLI (비대화형)

```bash
# 스킬 실행
opencode run --dir /tmp/e2e_test -m "모델명" "/sk-스킬명 [입력 메시지]"

# 에이전트 실행
opencode run --dir /tmp/e2e_test -m "모델명" --agent sa-에이전트명 "[입력 메시지]"

# 세션 이어가기 (멀티턴 대화)
opencode run --dir /tmp/e2e_test -m "모델명" -c "[후속 입력]"
```

> **주의**: `git init` 없이 실행하면 `external_directory` 권한 거부로 파일 쓰기가 실패한다.

### opencode TUI (대화형 — Agent/MCP 테스트 권장)

```bash
cd /tmp/e2e_test && opencode
# opencode 내에서 직접 /sk-*, @sa-* 명령 입력
```

## 공통 검증 기준

| 항목 | 기준 |
|------|------|
| Skill 인식 | opencode가 `/sk-*` 명령을 인식하고 실행 |
| Agent 인식 | opencode가 `@sa-*` 명령을 인식하고 실행 |
| 출력 파일 | `90_Result_Doc/`에 .md 파일 생성 |
| JSON 금지 | `.json` 파일 생성 없음 |
| MCP 연결 | sm-* MCP 서버가 stdio로 응답 |
| 폐쇄망 준수 | 외부 네트워크 호출 없음 |

## 미실행 TC 유형별 필요 환경

| 유형 | 해당 TC | 필요 환경 |
|------|---------|-----------|
| 멀티턴 Agent | TC-1.3, 1.4, 2.3, 5.4 | opencode TUI 또는 `-c` 세션 이어가기 |
| 빌드 환경 | TC-3.1~3.5, 4.1~4.4 | JDK 17 + Maven + Oracle 19c |
| Playwright | TC-6.1~6.4 | Python + Playwright + 실행 중인 웹서버 |
| HWPX MCP | TC-7.3, 7.4, 7.5 | sm-hwpx-builder MCP 연결 상태 |

## 폴더 구조

```
04_E2E Test/
├── README.md                     ← 이 파일
├── testcode/02_samplecode/       ← 테스트 대상 코드 (행정망 EJB/Struts)
├── E2E_Sol1_계획.md ~ E2E_Sol7_문서생성.md  ← 시나리오 문서
└── results/
    ├── Sol_1/TEST_RESULT.md + 산출물
    ├── Sol_2/TEST_RESULT.md + 산출물
    ├── Sol_3/TEST_RESULT.md (미실행, 로컬 실행 방법)
    ├── Sol_4/TEST_RESULT.md (미실행, 로컬 실행 방법)
    ├── Sol_5/TEST_RESULT.md + 산출물
    ├── Sol_6/TEST_RESULT.md (미실행, 로컬 실행 방법)
    └── Sol_7/TEST_RESULT.md + 산출물
```
