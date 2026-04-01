# SolCode_Lab 교육 매뉴얼

## 1. 프로젝트 개요

### 1.1 SolCode_Lab이란

SolCode_Lab은 **(주)솔리데오**가 구축하는 **폐쇄망 AI 코딩 환경**이다.
행정망 소프트웨어를 개발하는 개발자가 폐쇄망 내부에서 **AI 기반 바이브코딩**으로 개발할 수 있도록 도구와 워크플로우를 제공한다.

### 1.2 왜 필요한가

| 현재 | SolCode_Lab 도입 후 |
|------|---------------------|
| 폐쇄망에서 AI 코딩 불가 | opencode IDE + oss-120b 모델로 AI 코딩 |
| 개발자마다 다른 방식 | 표준화된 7단계 Workflow로 일관된 개발 |
| 설계/코드/문서가 분리 | Skill이 설계→코드→테스트→문서를 자동 연결 |
| 반복 작업에 시간 소모 | Agent가 반복 작업을 자동 수행 |

### 1.3 폐쇄망 내부 구성

```
┌─────────────────────────────────────┐
│           폐쇄망 서버               │
│  ┌───────────┐  ┌────────────────┐  │
│  │ oss-120b  │  │ opencode IDE   │  │
│  │ LLM 모델  │←→│ + Skill/Agent  │  │
│  │ (H100x4)  │  │ + MCP 서버     │  │
│  └───────────┘  └────────────────┘  │
│                        ↕            │
│              ┌─────────────────┐    │
│              │ Obsidian Vault  │    │
│              │ (문서 관리)      │    │
│              └─────────────────┘    │
└─────────────────────────────────────┘
```

---

## 2. 핵심 개념

### 2.1 구성 요소 4종류

SolCode_Lab은 4종류의 구성 요소로 이루어져 있다.

| 구분 | 접두사 | 역할 | 비유 |
|------|--------|------|------|
| **Skill** | SK_ | 하나의 작업을 수행하는 명령어 | 도구 (망치, 드라이버) |
| **Workflow** | SW_ | 여러 Skill을 순서대로 실행하는 흐름 | 작업 절차서 |
| **Agent** | SA_ | Workflow를 총괄 관리하는 AI 담당자 | 현장 감독 |
| **MCP** | SM_ | 외부 도구를 연결하는 서버 | 장비 연결 어댑터 |

추가로 **Sub-Agent(SSA_)** 는 Agent의 보조 역할을 한다.

### 2.2 사용 방법

opencode TUI에서:

```
/sk-code-analyze          ← Skill 직접 호출
@sa-architect             ← Agent 호출 (Workflow 자동 실행)
use sm-playwright         ← MCP 도구 사용
```

### 2.3 산출물 규칙

- 모든 결과물은 프로젝트 내 `90_Result_Doc/` 폴더에 저장된다
- 파일 형식은 **마크다운(.md)만** 사용한다 (.json 금지)
- hwpx(한글 문서)는 마크다운 원본과 함께 저장된다

---

## 3. 7단계 개발 워크플로우

SolCode_Lab의 개발 흐름은 7단계로 구성된다. 각 단계는 독립적으로도 사용 가능하고, 순서대로 연결하여 전체 파이프라인으로도 사용 가능하다.

### 전체 흐름도

```
[Sol.1 계획]
  @sa-architect (Speckit 8단계)
  사용자와 대화하며 설계 문서 완성
      │
      ▼
[Sol.2 분석]              [Sol.3 생성]
  @sa-analyzer              @sa-generator
  기존 코드 분석              신규 코드 생성
      │                        │
      ▼                        ▼
[Sol.4 수정]
  @sa-modifier
  기존 코드 수정 + 영향 분석
      │
      ▼
[Sol.5 리뷰]
  @sa-reviewer
  코드 품질 + 보안 리뷰
      │
      ▼
[Sol.6 E2E 테스트]
  @sa-e2e-tester
  Playwright 웹 + API + 비즈니스 프로세스 테스트
      │
      ▼
[Sol.7 문서 생성]
  @sa-documenter
  마크다운 → hwpx 변환 → Vault 저장
```

---

### Sol.1 계획 — 설계

**담당 Agent**: `@sa-architect`

사용자와 대화하면서 Speckit 8단계 파이프라인으로 설계를 완성한다.

| 단계 | 사용자에게 묻는 내용 | 산출물 |
|------|---------------------|--------|
| Phase 1 Constitution | 프로젝트 원칙, 제약조건 | constitution.md |
| Phase 2 Specify | 기능 설명, 문제, 시나리오 | spec.md |
| Phase 3 Clarify | 모호한 부분 5개 질문 | spec.md 업데이트 |
| Phase 4 Plan | 기술스택, 연동 시스템 | plan.md |
| Phase 5 Checklist | (자동 생성) | checklist.md |
| Phase 6 Tasks | 작업 우선순위 | tasks.md |
| Phase 7 Analyze | (자동 검증) | analysis.md |
| Phase 8 Design | 최종 확인 | design_final.md |

**사용 예시**:
```
@sa-architect 행정 문서관리 시스템을 설계해줘
```

Agent가 단계별로 질문하며 진행한다.

---

### Sol.2 분석 — 기존 코드 분석

**담당 Agent**: `@sa-analyzer`

| Skill | 역할 | 산출물 |
|-------|------|--------|
| /sk-code-analyze | 기술스택, 구조, 의존성 분석 | analysis_result.md |
| /sk-analyze-doc | 분석 결과를 보고서로 정리 | analysis_report.md |

**Sub-Agent**: SSA_dep_scanner — 의존성 스캔 및 폐쇄망 호환성 판별

**사용 예시**:
```
@sa-analyzer /path/to/legacy-project 분석해줘
```

---

### Sol.3 생성 — 신규 코드 생성

**담당 Agent**: `@sa-generator`

| Skill | 역할 | 산출물 |
|-------|------|--------|
| /sk-code-gen | design.md 기반 코드 생성 | 소스코드 + file_manifest.md |
| /sk-test-gen | 단위/통합 테스트 생성 | 테스트코드 + test_manifest.md |
| /sk-test-run | 테스트 실행 | test_result.md |
| /sk-gen-report | 종합 보고서 | generation_report.md |

**MCP**: SM_test_runner — 테스트 프레임워크(pytest/JUnit/Jest) 실행
**Sub-Agent**: SSA_test_executor — 테스트 실행/실패 분석 전담

**자동 워크플로우**: 코드 생성 → 테스트 생성 → 실행 → 실패 시 수정 → 재실행 (최대 3회) → 보고서

---

### Sol.4 수정 — 기존 코드 수정

**담당 Agent**: `@sa-modifier`

| Skill | 역할 | 산출물 |
|-------|------|--------|
| /sk-code-modify | 코드 수정 (최소 변경 원칙) | 수정코드 + change_summary.md |
| /sk-impact-check | 수정 영향범위 검토 | impact_report.md |
| /sk-modify-report | 종합 보고서 | modification_report.md |

**MCP**: SM_diff_viewer — 수정 전후 diff 비교
**Sub-Agent**: SSA_impact_analyzer — 영향범위 심층 분석

**핵심 규칙**:
- 최소 변경 원칙: 필요한 부분만 수정
- 고위험 영향 발견 시 사용자 확인 후 진행
- DB 스키마 변경 시 마이그레이션 스크립트 포함

---

### Sol.5 리뷰 — 코드 품질/보안 검증

**담당 Agent**: `@sa-reviewer`

| Skill | 역할 | 산출물 |
|-------|------|--------|
| /sk-code-review | 코드 품질 리뷰 (점수 0-100) | code_review_result.md |
| /sk-security-review | OWASP Top 10 + 행정망 보안 점검 | security_review_result.md |
| /sk-review-report | 종합 보고서 + 배포 판정 | review_report.md |

**Sub-Agent**: SSA_security_checker — 보안 심층 분석, 수정 코드 예시 제공

**배포 판정 기준**:

| 판정 | 조건 |
|------|------|
| 배포 가능 | Critical/High 이슈 없음 |
| 조건부 배포 | Critical 없음, High 조치 계획 있음 |
| 배포 불가 | Critical 미해결 |

---

### Sol.6 E2E 테스트 — 전체 시스템 테스트

**담당 Agent**: `@sa-e2e-tester`

| Skill | 역할 | 산출물 |
|-------|------|--------|
| /sk-e2e-test-gen | E2E 시나리오/코드 생성 | tests/e2e/ + e2e_test_manifest.md |
| /sk-e2e-test-run | E2E 테스트 실행 | e2e_test_result.md |
| /sk-e2e-report | 종합 보고서 | e2e_report.md |

**MCP**: SM_playwright — Playwright 브라우저 자동화 (Microsoft 공식)

**3가지 테스트 유형**:

1. **웹 UI E2E** (Playwright) — 로그인, CRUD, 화면 흐름
2. **API 통합 E2E** — 엔드포인트 간 연계 검증
3. **비즈니스 프로세스 E2E** — 기안→결재→승인→완료 전체 흐름

---

### Sol.7 문서 생성 — 산출물 문서화

**담당 Agent**: `@sa-documenter`

| Skill | 역할 | 산출물 |
|-------|------|--------|
| /sk-doc-md | 마크다운 문서 생성 | {유형}.md |
| /sk-doc-hwpx | hwpx(한글) 변환 | {파일명}.hwpx |

**MCP**:
- SM_hwpx_builder — 마크다운 → hwpx 변환 (md2hwpx.py 사용)
- SM_obsidian_sync — Obsidian Vault에 문서 정리/저장

**지원 문서 유형**: 설계서, 분석서, 테스트보고서, 회의록, 제안서, 매뉴얼

---

## 4. 프로젝트 폴더 구조

```
01_plan_notion/
├── 01_Manual/                  ← 이 매뉴얼
├── 02_Flow/                    ← Flow 요소 기획 문서
│   ├── Sol_1_계획/             4개 요소 (Speckit 8단계)
│   ├── Sol_2_분석/             5개 요소
│   ├── Sol_3_생성/             8개 요소
│   ├── Sol_4_수정/             7개 요소
│   ├── Sol_5_리뷰/             6개 요소
│   ├── Sol_6_E2E테스트/        6개 요소 (Playwright)
│   ├── Sol_7_문서생성/         6개 요소
│   └── SETUP_GUIDE.md          설치 및 운영 가이드
├── 02_package_install_guide/   ← MCP 서버별 폐쇄망 의존성 설치 가이드
├── 03_Tools/                   ← 폐쇄망 배포용 실행 파일 패키지
│   ├── skills/                 opencode Skill 19개
│   ├── agents/                 opencode Agent 7개
│   ├── mcp_servers/            MCP 서버 4개 (Python)
│   ├── md2hwpx/                hwpx 변환기
│   ├── speckit/                Speckit 템플릿/스크립트
│   └── install.sh              원클릭 설치 스크립트
├── jun.md                      프로젝트 기획서
└── CLAUDE.md                   AI 도구 프로젝트 지침
```

---

## 5. 전체 요소 현황표

### Skill (19개)

| # | Skill | 단계 | 역할 |
|---|-------|------|------|
| 1 | sk-design-spec | Sol.1 | 설계 문서 생성 |
| 2 | sk-design-review | Sol.1 | 설계 문서 검증/승인 |
| 3 | sk-code-analyze | Sol.2 | 소스코드 분석 |
| 4 | sk-analyze-doc | Sol.2 | 분석 보고서 작성 |
| 5 | sk-code-gen | Sol.3 | 코드 생성 |
| 6 | sk-test-gen | Sol.3 | 테스트 코드 생성 |
| 7 | sk-test-run | Sol.3 | 테스트 실행 |
| 8 | sk-gen-report | Sol.3 | 생성 보고서 |
| 9 | sk-code-modify | Sol.4 | 코드 수정 |
| 10 | sk-impact-check | Sol.4 | 영향범위 검토 |
| 11 | sk-modify-report | Sol.4 | 수정 보고서 |
| 12 | sk-code-review | Sol.5 | 코드 품질 리뷰 |
| 13 | sk-security-review | Sol.5 | 보안 취약점 점검 |
| 14 | sk-review-report | Sol.5 | 리뷰 보고서 |
| 15 | sk-e2e-test-gen | Sol.6 | E2E 시나리오/코드 생성 |
| 16 | sk-e2e-test-run | Sol.6 | E2E 테스트 실행 |
| 17 | sk-e2e-report | Sol.6 | E2E 보고서 |
| 18 | sk-doc-md | Sol.7 | 마크다운 문서 생성 |
| 19 | sk-doc-hwpx | Sol.7 | hwpx 변환 |

### Agent (7개)

| Agent | 단계 | 역할 |
|-------|------|------|
| sa-architect | Sol.1 | 설계 총괄 (Speckit 8단계) |
| sa-analyzer | Sol.2 | 코드 분석 총괄 |
| sa-generator | Sol.3 | 코드 생성 총괄 |
| sa-modifier | Sol.4 | 코드 수정 총괄 |
| sa-reviewer | Sol.5 | 코드 리뷰 총괄 |
| sa-e2e-tester | Sol.6 | E2E 테스트 총괄 |
| sa-documenter | Sol.7 | 문서 생성 총괄 |

### MCP (5개)

| MCP | 역할 | 외부 의존성 |
|-----|------|------------|
| sm-test-runner | 테스트 프레임워크 실행 | pytest/JUnit/Jest |
| sm-diff-viewer | 코드 diff 비교 | Git |
| sm-hwpx-builder | hwpx 변환 | 없음 (md2hwpx.py) |
| sm-obsidian-sync | Vault 문서 관리 | 없음 |
| sm-playwright | 브라우저 자동화 | @playwright/mcp |

---

## 6. 빠른 시작 가이드

### 6.1 설치 (최초 1회)

```bash
cd 03_Tools
bash install.sh
```

### 6.2 새 프로젝트 시작

```bash
cd /path/to/new-project
opencode
```

opencode TUI에서:

```
@sa-architect 행정 결재 시스템을 설계해줘
```

Agent가 8단계로 질문하며 design_final.md를 완성한다.

### 6.3 기존 코드 분석

```
@sa-analyzer /path/to/legacy 분석해줘
```

### 6.4 코드 생성 → 테스트 → 리뷰 → E2E → 문서화

```
@sa-generator design_final.md로 코드 생성해줘
@sa-reviewer 생성된 코드를 리뷰해줘
@sa-e2e-tester E2E 테스트를 수행해줘
@sa-documenter 보고서를 hwpx로 변환해줘
```

### 6.5 기존 코드 수정

```
@sa-modifier ./src/auth/login.java에서 로그인 5회 실패 시 계정 잠금 추가해줘
```

---

## 7. 자주 묻는 질문

**Q: 모든 단계를 순서대로 해야 하나요?**
A: 아닙니다. 각 단계는 독립적으로 사용 가능합니다. 코드 리뷰만 하고 싶으면 `@sa-reviewer`만 호출하면 됩니다.

**Q: Agent와 Skill의 차이는?**
A: Skill은 단일 작업(예: 코드 분석), Agent는 여러 Skill을 조합하여 전체 흐름을 관리합니다. Agent를 호출하면 내부적으로 필요한 Skill들을 자동 실행합니다.

**Q: 폐쇄망에서 Playwright가 동작하나요?**
A: 네. 인터넷망에서 브라우저 바이너리를 사전 다운로드하여 폐쇄망에 복사하면 됩니다. `02_package_install_guide/`의 가이드를 참조하세요.

**Q: 결과물이 .json으로 저장되면?**
A: opencode를 재시작하세요. 글로벌 instructions에 `.json 금지` 규칙이 있으며, 세션 시작 시 로딩됩니다.

**Q: 설계 없이 바로 코드를 생성할 수 있나요?**
A: `/sk-code-gen`을 직접 호출하면 됩니다. 다만 design.md가 없으면 구조화된 코드 생성이 어렵습니다. `@sa-architect`로 설계를 먼저 하는 것을 권장합니다.
