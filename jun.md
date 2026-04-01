# (주)솔리데오 페쇄망 LLM 구축(SolCode_Lab)

## 1. 목적

주로 행정망 소프트웨어를 작성하는 회사 업쿠 특성에 맞는 하드웨어와 LLM을 구축하여 폐쇄망에서 운영 가능한 바이브코딩 환경을 구축한다.
이 프로젝트의 이름은 'SolCode_Lab'으로 한다.

### 1.1 폐쇄망 내부 구성

- opencode IDE
- oss-120b 모델
- H100 x 4 EA

## 2. 목표

페쇄망 내부에서 소프트웨어 개발자가 Claude Code로 개발하는 것 처럼 개발할 수 있는 환경을 구축한다.
현업에서 바이브코딩에 익숙하지 않은 개발자들이 지정된 Workflow에서 개발 하도록 아래 내용을 개발하여 제공한다.

### 2.1 공급 범위

- Local MCP
  - 'SM_'(Soldeo MCP)로 시작되도록 명명 함.
- Skill
  - 'SK_'(Solideo Skills)로 시작되도록 명명 함.
- Workflow
  - 'SW_'(Solideo Workflow)로 시작되도록 명명 함.
- Agent, Sub-Agent
  - 'SA_'(Solideo Agent)로 시작되도록 명명 함.
  - 'SSA_'(Solideo Sub Agent)로 시작되도록 명명 함.

### 2.2 개발 적용

sol. 1. 계획
    - Speckit을 이용한 신규 소프트웨어 디자인 설계
    - 설계 문서를 사용자가 검증하고 생성
sol. 2. 분석
    - 기존 소스코드 분석
    - 분석내용 문서화
sol. 3. 생성
    - 설계 문서에 따라 신규 소프트웨어 생성
    - 생성된 코드 테스트 코드 생성 및 테스트 실행
    - 테스트 실행후 결과 문서화
sol. 4. 수정
    - 기존 소스코드 수정
    - 수정후 영향을 주는 다른 부분 검토
    - 수정후 테스트 코드 생성 및 테스트 실행
    - 테스트 실행후 결과 문서화
sol. 5. 리뷰
    - 생성된 코드 리뷰
sol. 5.5. E2E 테스트
    - Playwright 기반 웹 UI E2E 테스트
    - API 통합 E2E 테스트
    - 비즈니스 프로세스 E2E 테스트 (기안→결재→승인→완료)
    - 테스트 실행 후 결과 문서화

sol. 6. 관련 문서 생성

### 2.3 필요 Flow(SM, SK, SW, SA, SSA)

#### Sol. 1 계획

- SK_design_spec — Speckit 기반 설계 문서(design.md) 생성 Skill
- SK_design_review — 생성된 설계 문서를 사용자에게 제시하고 검증/승인 받는 Skill
- SW_planning — 설계 생성 → 사용자 검증 → 확정의 전체 계획 Workflow
- SA_architect — 소프트웨어 아키텍처 설계를 수행하는 Agent

#### Sol. 2 분석

- SK_code_analyze — 기존 소스코드의 기술스택, 구조, 의존성 분석 Skill
- SK_analyze_doc — 분석 결과를 마크다운 문서로 출력하는 Skill
- SW_analysis — 코드 분석 → 문서화의 전체 분석 Workflow
- SA_analyzer — 코드 분석을 수행하는 Agent
- SSA_dep_scanner — 의존성/라이브러리 스캔 Sub-Agent

#### Sol. 3 생성

- SK_code_gen — design.md 기반 전체/부분 코드 생성 Skill
- SK_test_gen — 생성된 코드에 대한 테스트 코드 생성 Skill
- SK_test_run — 테스트 실행 및 결과 수집 Skill
- SK_gen_report — 생성/테스트 결과 문서화 Skill
- SM_test_runner — 테스트 프레임워크 실행 및 결과 반환 MCP
- SW_generation — 코드 생성 → 테스트 생성 → 테스트 실행 → 결과 문서화 Workflow
- SA_generator — 코드 생성을 총괄하는 Agent
- SSA_test_executor — 테스트 실행/결과 수집 Sub-Agent

#### Sol. 4 수정

- SK_code_modify — 기존 소스코드 수정 Skill
- SK_impact_check — 수정 후 영향받는 코드 영역 검토 Skill
- SK_modify_report — 수정/테스트 결과 문서화 Skill
- SM_diff_viewer — 수정 전후 차이점 비교 MCP
- SW_modification — 코드 수정 → 영향분석 → 테스트 → 문서화 Workflow
- SA_modifier — 코드 수정을 총괄하는 Agent
- SSA_impact_analyzer — 수정 영향범위 분석 Sub-Agent

#### Sol. 5 리뷰

- SK_code_review — 코드 품질/스타일/로직 리뷰 Skill
- SK_security_review — 보안 취약점 점검 Skill
- SK_review_report — 리뷰 결과 및 이슈사항 문서화 Skill
- SW_review — 코드 리뷰 → 보안 리뷰 → 이슈 저장 Workflow
- SA_reviewer — 코드 리뷰를 총괄하는 Agent
- SSA_security_checker — 보안 검증 Sub-Agent

#### Sol. E2E 테스트

- SK_e2e_test_gen — E2E 테스트 시나리오/코드 생성 Skill (Playwright 웹 + API + 비즈니스)
- SK_e2e_test_run — E2E 테스트 실행 및 결과 수집 Skill
- SK_e2e_report — E2E 테스트 종합 보고서 Skill
- SM_playwright — Playwright 브라우저 자동화 MCP (Microsoft 공식 @playwright/mcp)
- SW_e2e_testing — 시나리오 생성 → 실행 → 보고서 Workflow
- SA_e2e_tester — E2E 테스트를 총괄하는 Agent

#### Sol. 6 관련 문서 생성

- SK_doc_md — 마크다운 문서 생성 Skill
- SK_doc_hwpx — 한글(hwpx) 문서 변환/생성 Skill
- SM_hwpx_builder — hwpx 빌드/변환 MCP
- SM_obsidian_sync — Obsidian Vault 폴더 구조에 문서 저장/동기화 MCP
- SW_documentation — 문서 유형 판별 → 생성 → 저장 Workflow
- SA_documenter — 문서 생성을 총괄하는 Agent

## 3. 관리

### 3.1 문서관리

- 폐쇄망 내부 환경 구축을 위하여 외부에서 개발되는 내용은 모두 아래 노션사이트에 조직화 하여 관리한다.

  - https://www.notion.so/powersolution/3357ece7e00580e98470fc614c962ea0?source=copy_link
- 폐쇄망 내부에서 개발되는 내용은 폐쇄망 내부에 Obsidian Vault에 조직화 하여 관리한다.

### 3.2 컨텍스트 관리

- 폐쇄망 내부에서 개발되는 컨텍스트는 폐쇄망 내부에 별도의 서버를 구축하지 않고, 폴더링하여 관리한다.
