# E2E 테스트: Sol_1 계획

## 테스트 환경

| 항목 | 값 |
|------|-----|
| IDE | opencode CLI (`opencode run`) |
| 모델 (폐쇄망) | oss-120b |
| 모델 (인터넷망 테스트) | `opencode/qwen3.6-plus-free` 또는 `github-copilot/gpt-4o` |
| 테스트 디렉토리 | `/tmp/e2e_sol1` |

### 사전 준비 (필수)

```bash
# 디렉토리 생성 + git init (opencode가 프로젝트로 인식하려면 필수)
mkdir -p /tmp/e2e_sol1/90_Result_Doc && cd /tmp/e2e_sol1 && git init
```

### 실행 방법

```bash
# 스킬 실행 (단일 턴)
opencode run --dir /tmp/e2e_sol1 -m "모델명" "/sk-스킬명 [입력 메시지]"

# 에이전트 실행 (단일 턴)
opencode run --dir /tmp/e2e_sol1 -m "모델명" --agent sa-architect "[입력 메시지]"

# 세션 이어가기 (멀티턴 — Phase 3 Clarify 등)
opencode run --dir /tmp/e2e_sol1 -m "모델명" -c "[후속 입력]"
```

> **주의**: `git init` 없이 실행하면 `external_directory` 권한 거부로 파일 쓰기가 실패한다.

---

## TC-1.1: sk-design-spec (설계 문서 생성)

### 목적
사용자 요구사항을 수집하여 `90_Result_Doc/design.md`를 생성하는지 검증

### 실행

```
opencode> /sk-design-spec
```

### 테스트 입력

LLM이 순차적으로 질문하면 아래와 같이 응답:

| 순서 | 질문 항목 | 입력값 |
|------|-----------|--------|
| 1 | 프로젝트명 | 내부결재시스템 |
| 2 | 목적 및 배경 | 전자결재 자동화로 종이 결재 대체 |
| 3 | 기능 요구사항 | 1) 기안 작성 2) 결재선 지정 3) 승인/반려 4) 이력 조회 |
| 4 | 기술스택 | Java 17 / Spring Boot 3.x |
| 5 | 배포 환경 | 폐쇄망 |
| 6 | 연동 시스템 | 인사DB (Oracle 19c) |

### 검증 체크리스트

- [ ] **질문 수집**: 6개 항목을 빠짐없이 질문했는가
- [ ] **파일 생성**: `90_Result_Doc/design.md` 파일이 존재하는가
- [ ] **섹션 완전성**: 아래 8개 섹션이 모두 포함되었는가
  - [ ] 1. 프로젝트 개요
  - [ ] 2. 아키텍처 설계
  - [ ] 3. 모듈 구조
  - [ ] 4. API 설계
  - [ ] 5. DB 스키마
  - [ ] 6. 기술스택 결정
  - [ ] 7. 보안 설계
  - [ ] 8. 비기능 요구사항
- [ ] **폐쇄망 준수**: 외부 CDN, 외부 API, 외부 저장소 참조가 없는가
- [ ] **보안 포함**: 인증/인가, 암호화, 감사로그 항목이 있는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
# 파일 존재 확인
ls 90_Result_Doc/design.md

# 섹션 확인
grep -c "^## " 90_Result_Doc/design.md   # 8 이상이어야 함

# json 파일 확인 (없어야 정상)
find 90_Result_Doc/ -name "*.json"

# 외부 URL 참조 확인 (없어야 정상)
grep -iE "https?://" 90_Result_Doc/design.md
```

---

## TC-1.2: sk-design-review (설계 문서 리뷰)

### 목적
생성된 design.md를 섹션별로 검증하고 승인/반려 프로세스가 동작하는지 검증

### 사전 조건
- TC-1.1 완료 → `90_Result_Doc/design.md` 존재

### 실행

```
opencode> /sk-design-review
```

"90_Result_Doc/design.md를 리뷰해줘" 입력

### 테스트 입력

| 순서 | 섹션 리뷰 제시 시 | 입력값 |
|------|-------------------|--------|
| 1 | 프로젝트 개요 | 승인 |
| 2 | 아키텍처 설계 | "3-Tier 구성에 캐시 레이어 추가 필요" (수정요청) |
| 3 | 모듈 구조 | 승인 |
| 4 | API 설계 | 승인 |
| 5 | DB 스키마 | 승인 |
| 6 | 기술스택 결정 | 승인 |
| 7 | 보안 설계 | 승인 |
| 8 | 비기능 요구사항 | 승인 |

### 검증 체크리스트

- [ ] **섹션별 진행**: 8개 섹션을 순서대로 제시했는가
- [ ] **검증 항목 표시**: 적합/부적합/확인필요가 표시되었는가
- [ ] **사용자 입력 수집**: 각 섹션마다 승인/수정/의견을 요청했는가
- [ ] **수정요청 반영**: 아키텍처 섹션의 "캐시 레이어 추가" 피드백이 기록되었는가
- [ ] **결과 저장**: `90_Result_Doc/review_result.md`가 생성되었는가
- [ ] **최종 상태**: 조건부승인(수정요청 1건 포함)으로 결론지었는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
# 리뷰 결과 파일 확인
ls 90_Result_Doc/review_result.md

# 수정요청 사항 기록 확인
grep -i "캐시" 90_Result_Doc/review_result.md

# 최종 상태 확인
grep -iE "승인|반려" 90_Result_Doc/review_result.md
```

---

## TC-1.3: sa-architect Agent (Speckit 8단계 통합)

### 목적
sa-architect Agent가 Speckit 8단계 파이프라인을 순차 수행하며, 질문이 필요한 단계(1,2,3,5)에서만 사용자에게 질문하고, 자동 생성 단계(4,6)에서는 질문 없이 진행하는지 검증

### 사전 준비

```bash
mkdir -p /tmp/e2e_sol1_architect && cd /tmp/e2e_sol1_architect
```

### 실행

```
opencode> @sa-architect 새 프로젝트를 설계해줘
```

### 테스트 입력 (8단계)

#### Phase 1: Constitution (사용자 질문 있음)

**예상 질문**: 프로젝트명, 목적, 핵심 원칙(강제 수준별), 절대 제약조건

**입력**:
```
프로젝트명: 출장관리시스템
목적: 출장 신청~정산 자동화
핵심 원칙:
- 외부 네트워크 통신 금지 (NON-NEGOTIABLE)
- 행정망 보안 지침 준수: 인증/인가, 암호화, 감사로그 (MANDATORY)
- 내부 저장소 라이브러리만 사용 (MANDATORY)
- 테스트 100% 통과 게이트 (MANDATORY)
- SOLID 아키텍처 (RECOMMENDED)
절대 제약: 인터넷 접근 불가, Oracle 19c 사용 필수
```

**검증**:
- [ ] constitution.md에 Core Principles 섹션이 있고 각 원칙에 강제 수준(NON-NEGOTIABLE/MANDATORY/RECOMMENDED)이 명시되었는가
- [ ] Security Requirements 섹션이 있는가 (인증/인가, 데이터 보호, 감사로그)
- [ ] Compliance Standards 섹션이 있는가
- [ ] Performance & Scalability 섹션이 있는가
- [ ] Development Workflow 섹션이 있는가 (Git 전략, CI/CD)
- [ ] Governance 섹션이 있는가 (Constitution 권위, 개정 절차)
- [ ] 사용자 확인을 받은 후 Phase 2로 진행했는가

#### Phase 2: Specify (사용자 질문 있음)

**예상 질문**: 해결할 문제, 비즈니스 가치, 사용자 시나리오(P1/P2/P3), 엣지 케이스

**입력**:
```
문제: 종이 결재로 인한 출장 처리 지연, 정산 오류
비즈니스 가치: 결재 시간 50% 단축, 정산 오류 제거
시나리오(P1): 직원이 웹에서 출장 신청 → 팀장 승인 → 출장 → 정산 제출
시나리오(P2): 관리자가 출장 현황 대시보드 조회
시나리오(P3): 출장비 초과 시 부서장 추가 승인
엣지 케이스: 결재자 부재 시 대리결재, 출장 취소, 중복 신청 방지
```

**검증**:
- [ ] spec.md에 Problem Statement, Business Value가 있는가
- [ ] User Scenarios에 P1/P2/P3 우선순위가 구분되었는가
- [ ] Edge Cases 섹션이 있는가
- [ ] Functional Requirements + Key Entities가 있는가
- [ ] Success Criteria가 기술 비의존적이고 측정 가능한가 (예: "200ms 응답" ❌ → "사용자가 즉시 결과를 봄" ✅)
- [ ] **HOW(기술스택, API, 코드)가 포함되지 않았는가** (WHAT/WHY만)
- [ ] `[NEEDS CLARIFICATION]`이 최대 3개 이하인가
- [ ] `90_Result_Doc/checklists/requirements.md` 품질 체크리스트가 자동 생성되었는가

#### Phase 3: Clarify (사용자 질문 있음 — 1개씩 순차)

**예상 동작**: spec.md를 11개 카테고리로 스캔 후 Clear/Partial/Missing 분류, (Impact × Uncertainty) 순으로 최대 5개 질문

**검증**:
- [ ] **한 번에 정확히 1개만** 질문했는가 (여러 질문을 한꺼번에 제시하지 않았는가)
- [ ] 객관식인 경우 추천 옵션을 상단에 표시하고 Option A/B/C/Custom 테이블로 제시했는가
- [ ] 각 답변 수락 직후 spec.md에 즉시 반영했는가
- [ ] `## Clarifications > ### Session YYYY-MM-DD` 하위에 `- Q: → A:` 기록이 남았는가
- [ ] 질문 5개를 초과하지 않았는가
- [ ] 완료 후 커버리지 요약 테이블(Resolved/Deferred/Clear/Outstanding)이 제시되었는가

**입력 예시** (질문별 응답):
```
Q1 (출장비 한도): "B — 건당 50만원, 초과 시 부서장 추가승인"
Q2 (대리결재 범위): "A — 직속 상위자에게 자동 이관"
Q3 (해외출장 포함 여부): "Custom — 국내만, 해외는 Phase 2에서 추가"
```

#### Phase 4: Plan (사용자 질문 없음 — 자동 생성)

**예상 동작**: spec.md + constitution.md 기반 자동 생성. Phase 0(리서치) → Phase 1(설계/계약) 순서.

**검증**:
- [ ] **사용자에게 기술스택을 질문하지 않았는가** (자동 결정, 미확정 시에만 질문)
- [ ] `90_Result_Doc/research.md` 생성 — Decision / Rationale / Alternatives 형식
- [ ] `90_Result_Doc/data-model.md` 생성 — 엔티티, 필드, 관계, 검증 규칙, 상태 전이
- [ ] `90_Result_Doc/contracts/` 디렉토리 생성 — REST 엔드포인트 정의
- [ ] `90_Result_Doc/quickstart.md` 생성 — 프로젝트 셋업 가이드
- [ ] `90_Result_Doc/plan.md` 생성 — Summary, Architectural Vision, Technical Context, Constitution Check, Project Structure 포함
- [ ] Constitution Check가 2회(Phase 0 전/Phase 1 후) 수행되었는가
- [ ] plan.md를 사용자에게 제시하고 확인을 받았는가

#### Phase 5: Checklist (사용자 질문 있음 — 최대 3개 맞춤 질문)

**예상 동작**: 범위/리스크/깊이 확인을 위한 맞춤 질문 후 도메인별 체크리스트 생성

**검증**:
- [ ] 옵션 테이블(Option | Candidate | Why It Matters) 형식으로 질문했는가
- [ ] 질문이 최대 3개(+후속 2개)를 초과하지 않았는가
- [ ] `90_Result_Doc/checklists/` 하위에 도메인별 파일이 생성되었는가 (예: `security.md`, `api.md`, `ux.md`)
- [ ] 항목 형식이 `- [ ] CHK001 Are [requirements] defined for [scenario]?` 패턴인가
- [ ] 금지 패턴("Verify", "Test", "Click" 등 구현 테스트)이 없는가
- [ ] 80% 이상 항목에 추적성 참조(`[Spec section]`, `[Gap]` 등)가 있는가
- [ ] 소프트 캡 40항목을 초과하지 않았는가

**입력 예시**:
```
Q1: "B — 보안과 결재 흐름에 집중"
Q2: "A — 내부 사용자만"
Q3: "Custom — 성능보다 정확성 우선"
```

#### Phase 6: Tasks (사용자 질문 없음 — 자동 생성)

**예상 동작**: plan.md + spec.md 기반 자동 생성

**검증**:
- [ ] **사용자에게 우선순위/팀 규모를 질문하지 않았는가** (자동 생성)
- [ ] 태스크 형식이 `- [ ] [T001] [P] [US1] Description with file path`인가
  - [ ] `[T001]` 순차 ID
  - [ ] `[P]` 병렬 가능 표시 (해당 시)
  - [ ] `[US1]` 사용자 스토리 레이블 (해당 시)
  - [ ] 정확한 파일 경로 포함
- [ ] Phase 구조가 올바른가
  - [ ] Phase 1: Setup
  - [ ] Phase 2: Foundational (모든 스토리의 전제 조건)
  - [ ] Phase 3+: 사용자 스토리별 (P1→P2→P3 순)
  - [ ] Final Phase: Polish & Cross-cutting
- [ ] `90_Result_Doc/tasks.md`로 저장되었는가

#### Phase 7: Analyze (질문 없음 — READ-ONLY 분석)

**예상 동작**: spec.md + plan.md + tasks.md + constitution.md 교차 검증. 파일 수정 없음.

**검증**:
- [ ] **파일을 수정하지 않았는가** (STRICTLY READ-ONLY)
- [ ] 결과 테이블(ID, Category, Severity, Location, Summary, Recommendation)이 제시되었는가
- [ ] 심각도가 CRITICAL/HIGH/MEDIUM/LOW로 분류되었는가
- [ ] 탐지 항목: 중복, 모호성, 미명시, Constitution 위반, 커버리지 갭, 불일치
- [ ] 메트릭스(총 요구사항, 총 태스크, 커버리지 %, CRITICAL 수)가 포함되었는가
- [ ] **콘솔 출력만 했는가** (analysis.md 파일을 생성하지 않았는가)
- [ ] CRITICAL 이슈가 있으면 Phase 8 전 해결을 권고했는가
- [ ] "수정을 제안할까요?"라고 질문했는가

**입력**: "상위 2개 이슈에 대해 수정 제안해주세요" 또는 "문제없습니다, 다음 단계로"

#### Phase 8: Implement (코드 구현)

**예상 동작**: tasks.md의 태스크를 의존성 순서대로 실행하여 실제 코드 구현

**검증**:
- [ ] Phase 7(Analyze) 실행 여부를 확인했는가
- [ ] 체크리스트 미완료 항목을 확인하고 진행 여부를 질문했는가
- [ ] Setup → Tests → Core → Integration → Polish 순서로 구현했는가
- [ ] TDD 접근: 테스트 먼저 작성 → 구현 → 리팩토링
- [ ] 각 태스크 완료 시 tasks.md에서 `[ ]` → `[x]` 업데이트했는가
- [ ] **Test Gate**: 매 태스크 후 관련 테스트 실행, 100% 통과 확인했는가
- [ ] 테스트 실패 시 다음 태스크로 진행하지 않았는가
- [ ] 실제 소스코드 파일들이 생성되었는가

**입력**: "체크리스트 미완료 항목은 무시하고 진행해주세요"

### 전체 검증 명령어

```bash
# 전체 산출물 확인
ls -la 90_Result_Doc/
ls -la 90_Result_Doc/checklists/ 2>/dev/null
ls -la 90_Result_Doc/contracts/ 2>/dev/null

# Phase별 필수 파일 존재 여부
echo "--- Phase 1: Constitution ---"
[ -f "90_Result_Doc/constitution.md" ] && echo "✅ constitution.md" || echo "❌ constitution.md"

echo "--- Phase 2: Specify ---"
[ -f "90_Result_Doc/spec.md" ] && echo "✅ spec.md" || echo "❌ spec.md"
[ -f "90_Result_Doc/checklists/requirements.md" ] && echo "✅ checklists/requirements.md" || echo "❌ checklists/requirements.md"

echo "--- Phase 3: Clarify ---"
grep -c "## Clarifications" 90_Result_Doc/spec.md 2>/dev/null && echo "✅ Clarifications 섹션" || echo "❌ Clarifications 섹션 없음"

echo "--- Phase 4: Plan ---"
for f in plan.md research.md data-model.md quickstart.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f"
done
[ -d "90_Result_Doc/contracts" ] && echo "✅ contracts/" || echo "❌ contracts/"

echo "--- Phase 5: Checklist ---"
ls 90_Result_Doc/checklists/*.md 2>/dev/null | wc -l | xargs -I{} echo "체크리스트 파일 수: {}"
grep -r "CHK[0-9]" 90_Result_Doc/checklists/ 2>/dev/null | head -3

echo "--- Phase 6: Tasks ---"
[ -f "90_Result_Doc/tasks.md" ] && echo "✅ tasks.md" || echo "❌ tasks.md"
grep -c "\[T[0-9]" 90_Result_Doc/tasks.md 2>/dev/null | xargs -I{} echo "태스크 수: {}"

echo "--- Phase 7: Analyze ---"
echo "(콘솔 출력만, 파일 없어야 정상)"
[ ! -f "90_Result_Doc/analysis.md" ] && echo "✅ analysis.md 미생성 (정상)" || echo "❌ analysis.md 생성됨 (비정상)"

echo "--- Phase 8: Implement ---"
grep -c "\[x\]" 90_Result_Doc/tasks.md 2>/dev/null | xargs -I{} echo "완료 태스크 수: {}"
find src/ -name "*.java" 2>/dev/null | wc -l | xargs -I{} echo "생성된 Java 파일 수: {}"

echo "--- 공통 검증 ---"
find 90_Result_Doc/ -name "*.json" | wc -l | xargs -I{} echo "json 파일 수: {} (0이어야 정상)"
grep -rlE "https?://" 90_Result_Doc/ 2>/dev/null | wc -l | xargs -I{} echo "외부 URL 참조: {} (0이어야 정상)"
```

### Constitution 내용 검증 (상세)

```bash
# 6개 필수 섹션 존재 여부
for section in "Core Principles" "Security Requirements" "Compliance Standards" "Performance" "Development Workflow" "Governance"; do
  grep -q "$section" 90_Result_Doc/constitution.md 2>/dev/null && echo "✅ $section" || echo "❌ $section 누락"
done

# 강제 수준 표기 확인
grep -cE "NON-NEGOTIABLE|MANDATORY|RECOMMENDED" 90_Result_Doc/constitution.md 2>/dev/null | xargs -I{} echo "강제 수준 표기 수: {}"
```

### Spec 내용 검증 (상세)

```bash
# WHAT/WHY만 있고 HOW 없는지 확인
grep -iE "Spring Boot|Java 17|MyBatis|REST API" 90_Result_Doc/spec.md 2>/dev/null && echo "❌ HOW(기술스택) 포함됨" || echo "✅ HOW 미포함 (정상)"

# NEEDS CLARIFICATION 개수 확인 (3개 이하)
grep -c "NEEDS CLARIFICATION" 90_Result_Doc/spec.md 2>/dev/null | xargs -I{} echo "NEEDS CLARIFICATION: {}개 (3개 이하여야 정상)"
```

### Tasks 형식 검증 (상세)

```bash
# 태스크 형식 확인: [T001] [P] [US1] 패턴
grep -cE "^\- \[ \] \[T[0-9]+" 90_Result_Doc/tasks.md 2>/dev/null | xargs -I{} echo "올바른 형식 태스크: {}개"

# 파일 경로 포함 확인
grep -cE "\[T[0-9]+\].*\.(java|py|ts|xml|yml|md)" 90_Result_Doc/tasks.md 2>/dev/null | xargs -I{} echo "파일 경로 포함 태스크: {}개"
```

---

## TC-1.4: SW_planning 워크플로우 통합 테스트

### 목적
계획 단계 전체 흐름(Speckit 8단계 → 리뷰 → 수정 → 확정)이 연속적으로 동작하는지 검증

### 실행 순서

```
# Step 1: Speckit 8단계 설계
opencode> @sa-architect 새 프로젝트를 설계해줘
→ Phase 1~7 완료 후 plan.md, tasks.md 등 산출물 생성
→ Phase 8에서 코드 구현

# Step 2: 설계 리뷰
opencode> /sk-design-review
→ "90_Result_Doc/plan.md를 리뷰해줘"
→ 일부 섹션에 수정요청

# Step 3: 수정 반영
opencode> @sa-architect review_result.md의 수정요청 사항을 plan.md에 반영해줘
→ plan.md 업데이트

# Step 4: 재리뷰 및 확정
opencode> /sk-design-review
→ 전 섹션 승인
```

### 검증 체크리스트

- [ ] **사이클 완료**: Speckit 8단계 → 리뷰 → 수정 → 재리뷰가 완료되었는가
- [ ] **피드백 반영**: 리뷰 수정요청이 plan.md에 실제 반영되었는가
- [ ] **이력 보존**: review_result.md에 리뷰 이력이 기록되어 있는가
- [ ] **산출물 정합성**: constitution ↔ spec ↔ plan ↔ tasks 간 용어/내용이 일치하는가
- [ ] **출력 형식**: 전 과정에서 `.json` 파일이 생성되지 않았는가

---

## 결과 기록

| TC | 테스트명 | 결과 | 비고 |
|----|----------|------|------|
| TC-1.1 | sk-design-spec | ⬜ PASS / ⬜ FAIL | |
| TC-1.2 | sk-design-review | ⬜ PASS / ⬜ FAIL | |
| TC-1.3 | sa-architect (Speckit 8단계) | ⬜ PASS / ⬜ FAIL | |
| TC-1.4 | SW_planning 통합 | ⬜ PASS / ⬜ FAIL | |

테스트 일시: ____-__-__ __:__
테스터: __________
