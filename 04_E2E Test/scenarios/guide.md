# E2E 테스트 실행 가이드

이 문서는 다른 Claude Code 세션에서 E2E 테스트를 실행하기 위한 가이드이다.

## 사전 조건

1. **opencode CLI** 설치 완료 (`which opencode` 확인)
2. **opencode 인증** 완료 (`opencode providers list`로 확인)
3. **opencode 스킬/에이전트/MCP** 전역 설치 완료 (`~/.config/opencode/` 하위)

## 실행 규칙

### 필수: git init

opencode run은 git 프로젝트 내에서만 파일 쓰기가 가능하다. `git init` 없이 실행하면 `external_directory` 권한 거부로 실패한다.

```bash
mkdir -p /tmp/e2e_test/90_Result_Doc && cd /tmp/e2e_test && git init
```

### 모델 지정

`-m` 옵션으로 모델을 반드시 지정한다. 미지정 시 기본 모델이 불확실하여 실패할 수 있다.

| 환경 | 모델 |
|------|------|
| 인터넷망 (무료) | `opencode/qwen3.6-plus-free` |
| 인터넷망 (GitHub Copilot) | `github-copilot/gpt-4o` |
| 폐쇄망 | oss-120b (opencode.json에 설정) |

### 실행 패턴

```bash
# 패턴 1: 스킬 단일 실행
opencode run --dir /tmp/e2e_test -m "모델명" "/sk-스킬명 [입력]"

# 패턴 2: 에이전트 실행
opencode run --dir /tmp/e2e_test -m "모델명" --agent sa-에이전트명 "[입력]"

# 패턴 3: 세션 이어가기 (멀티턴)
opencode run --dir /tmp/e2e_test -m "모델명" -c "[후속 입력]"

# 패턴 4: opencode TUI (대화형, MCP/Agent 권장)
cd /tmp/e2e_test && opencode
```

### 결과 검증 공통

```bash
# 산출물 존재 확인
ls 90_Result_Doc/

# json 파일 없는지 확인 (0이어야 정상)
find 90_Result_Doc/ -name "*.json" | wc -l

# 외부 URL 없는지 확인 (0이어야 정상)
grep -rlE "https?://" 90_Result_Doc/ | wc -l
```

---

## Sol_1 계획 (4 TC)

### TC-1.1: sk-design-spec

```bash
mkdir -p /tmp/e2e_sol1/90_Result_Doc && cd /tmp/e2e_sol1 && git init

opencode run --dir /tmp/e2e_sol1 -m "모델명" \
  "/sk-design-spec 프로젝트명: 내부결재시스템, 목적: 전자결재 자동화로 종이결재 대체, 기능요구사항: 1)기안작성 2)결재선지정 3)승인반려 4)이력조회, 기술스택: Java17/SpringBoot3.x, 배포환경: 폐쇄망, 연동시스템: 인사DB Oracle19c"
```

**검증:**
```bash
[ -f 90_Result_Doc/design.md ] && echo "✅ PASS" || echo "❌ FAIL"
grep -c "^## " 90_Result_Doc/design.md   # 8 이상
```

### TC-1.2: sk-design-review

```bash
opencode run --dir /tmp/e2e_sol1 -m "모델명" \
  "/sk-design-review 90_Result_Doc/design.md를 리뷰해줘. 아키텍처 설계 섹션에 캐시 레이어 추가 필요라고 수정 요청하고 나머지는 승인."
```

**검증:**
```bash
[ -f 90_Result_Doc/review_result.md ] && echo "✅ PASS" || echo "❌ FAIL"
grep -i "캐시" 90_Result_Doc/review_result.md
```

### TC-1.3: sa-architect (Speckit 8단계) — 멀티턴

```bash
mkdir -p /tmp/e2e_sol1_tc13/90_Result_Doc && cd /tmp/e2e_sol1_tc13 && git init

# Phase 1: Constitution
opencode run --dir . -m "모델명" --agent sa-architect \
  "새 프로젝트를 설계해줘. 프로젝트명: 출장관리시스템, 목적: 출장 신청~정산 자동화, 핵심 원칙: 외부통신 금지(NON-NEGOTIABLE), 보안 지침 준수(MANDATORY), 내부 저장소만 사용(MANDATORY), 테스트 100% 통과(MANDATORY)"

# Phase 2: Specify
opencode run --dir . -m "모델명" -c \
  "문제: 종이 결재 지연, 비즈니스 가치: 결재 50% 단축, P1: 직원 웹 출장신청→승인→정산, P2: 관리자 대시보드, P3: 출장비 초과 추가승인, 엣지: 대리결재, 출장 취소"

# Phase 3: Clarify (질문마다 1개씩 응답)
opencode run --dir . -m "모델명" -c "B — 건당 50만원, 초과 시 부서장 추가승인"
opencode run --dir . -m "모델명" -c "A — 직속 상위자 자동 이관"
# ... 질문이 끝날 때까지 반복 (최대 5개)

# Phase 4: Plan (자동 생성, 확인만)
opencode run --dir . -m "모델명" -c "좋습니다, 진행해주세요"

# Phase 5: Checklist (질문에 응답)
opencode run --dir . -m "모델명" -c "B — 보안과 결재 흐름에 집중"

# Phase 6: Tasks (자동 생성)
opencode run --dir . -m "모델명" -c "확인했습니다"

# Phase 7: Analyze
opencode run --dir . -m "모델명" -c "문제없습니다, 다음 단계로"

# Phase 8: Implement
opencode run --dir . -m "모델명" -c "체크리스트 미완료 무시하고 진행"
```

**검증:**
```bash
for f in constitution.md spec.md research.md data-model.md plan.md quickstart.md tasks.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f"
done
ls 90_Result_Doc/checklists/ 90_Result_Doc/contracts/ 2>/dev/null
```

### TC-1.4: SW_planning 통합

TC-1.3 완료 후:
```bash
opencode run --dir . -m "모델명" "/sk-design-review 90_Result_Doc/plan.md를 리뷰해줘"
```

---

## Sol_2 분석 (3 TC)

### 사전 준비

```bash
mkdir -p /tmp/e2e_sol2/90_Result_Doc
cp -r "04_E2E Test/testcode/02_samplecode/"* /tmp/e2e_sol2/
cd /tmp/e2e_sol2 && git init
```

### TC-2.1: sk-code-analyze

```bash
opencode run --dir /tmp/e2e_sol2 -m "모델명" "/sk-code-analyze 이 프로젝트를 분석해줘"
```

**검증:**
```bash
[ -f 90_Result_Doc/analysis_result.md ] && echo "✅ PASS" || echo "❌ FAIL"
grep -i "EJB\|Struts" 90_Result_Doc/analysis_result.md | head -3
```

### TC-2.2: sk-analyze-doc

```bash
opencode run --dir /tmp/e2e_sol2 -m "모델명" "/sk-analyze-doc analysis_result.md를 보고서로 작성해줘"
```

**검증:**
```bash
[ -f 90_Result_Doc/analysis_report.md ] && echo "✅ PASS" || echo "❌ FAIL"
```

### TC-2.3: sa-analyzer 통합

```bash
# 이전 결과 삭제
rm -rf /tmp/e2e_sol2/90_Result_Doc && mkdir /tmp/e2e_sol2/90_Result_Doc

opencode run --dir /tmp/e2e_sol2 -m "모델명" --agent sa-analyzer "이 프로젝트를 전체 분석해줘"
```

**검증:**
```bash
for f in analysis_result.md analysis_report.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f"
done
```

---

## Sol_3 생성 (5 TC) — 빌드 환경 필요

### 사전 준비

JDK 17 + Maven 3.9+ + Oracle 19c 필요.

```bash
mkdir -p /tmp/e2e_sol3/90_Result_Doc && cd /tmp/e2e_sol3 && git init
# Sol_1에서 생성된 design.md 복사
cp /path/to/design.md 90_Result_Doc/design.md
```

### TC-3.1 ~ TC-3.5

```bash
# TC-3.1
opencode run --dir . -m "모델명" "/sk-code-gen 90_Result_Doc/design.md를 기반으로 코드를 생성해줘"

# TC-3.2
opencode run --dir . -m "모델명" "/sk-test-gen 생성된 코드에 대한 테스트 코드를 작성해줘"

# TC-3.3
opencode run --dir . -m "모델명" "/sk-test-run 테스트를 실행해줘"

# TC-3.4
opencode run --dir . -m "모델명" "/sk-gen-report 생성 결과를 종합 보고서로 작성해줘"

# TC-3.5 (통합)
opencode run --dir . -m "모델명" --agent sa-generator "design.md 기반으로 전체 생성 워크플로우를 수행해줘"
```

---

## Sol_4 수정 (4 TC) — 빌드 환경 필요

### 사전 준비

```bash
mkdir -p /tmp/e2e_sol4/90_Result_Doc
cp -r "04_E2E Test/testcode/02_samplecode/"* /tmp/e2e_sol4/
cd /tmp/e2e_sol4 && git init
```

### TC-4.1 ~ TC-4.4

```bash
# TC-4.1
opencode run --dir . -m "모델명" \
  "/sk-code-modify SntFmwMealBean.java의 insertSNTFMWNewBusin01 메서드에 입력값 검증을 추가해줘"

# TC-4.2
opencode run --dir . -m "모델명" "/sk-impact-check 수정 영향 범위를 분석해줘"

# TC-4.3
opencode run --dir . -m "모델명" "/sk-modify-report 수정 결과를 종합 보고서로 작성해줘"

# TC-4.4 (통합, 멀티턴 가능)
opencode run --dir . -m "모델명" --agent sa-modifier "SntFmwMealBean.java에 입력값 검증 버그를 수정해줘"
# 고위험 발견 시:
opencode run --dir . -m "모델명" -c "진행해주세요"
```

---

## Sol_5 리뷰 (4 TC)

### 사전 준비

```bash
mkdir -p /tmp/e2e_sol5/90_Result_Doc
cp -r "04_E2E Test/testcode/02_samplecode/"* /tmp/e2e_sol5/
cd /tmp/e2e_sol5 && git init
```

### TC-5.1 ~ TC-5.4

```bash
# TC-5.1
opencode run --dir /tmp/e2e_sol5 -m "모델명" "/sk-code-review 이 프로젝트 코드를 리뷰해줘"

# TC-5.2
opencode run --dir /tmp/e2e_sol5 -m "모델명" "/sk-security-review 이 프로젝트의 보안 취약점을 점검해줘"

# TC-5.3
opencode run --dir /tmp/e2e_sol5 -m "모델명" "/sk-review-report 리뷰 결과를 종합 보고서로 작성해줘"

# TC-5.4 (통합)
opencode run --dir /tmp/e2e_sol5 -m "모델명" --agent sa-reviewer "이 프로젝트 전체를 리뷰해줘"
```

**검증:**
```bash
for f in code_review_result.md security_review_result.md review_report.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f"
done
grep -iE "점수|score" 90_Result_Doc/code_review_result.md | head -1
grep -iE "배포 금지|배포 불가" 90_Result_Doc/review_report.md | head -1
```

---

## Sol_6 E2E테스트 (4 TC) — Playwright + 웹서버 필요

### 사전 준비

```bash
mkdir -p /tmp/e2e_sol6/90_Result_Doc && cd /tmp/e2e_sol6 && git init

# 대상 앱 실행 (별도 터미널)
cd /path/to/target-app && ./mvnw spring-boot:run

# Playwright 설치
pip install pytest-playwright && playwright install chromium
```

### TC-6.1 ~ TC-6.4

```bash
# TC-6.1
opencode run --dir . -m "모델명" \
  "/sk-e2e-test-gen 출장관리시스템의 E2E 테스트를 생성해줘. 로그인→출장신청→승인 흐름 포함"

# TC-6.2
opencode run --dir . -m "모델명" "/sk-e2e-test-run E2E 테스트를 실행해줘"

# TC-6.3
opencode run --dir . -m "모델명" "/sk-e2e-report E2E 테스트 결과를 종합 보고서로 작성해줘"

# TC-6.4 (통합)
opencode run --dir . -m "모델명" --agent sa-e2e-tester "출장관리시스템의 전체 E2E 테스트를 수행해줘"
```

---

## Sol_7 문서생성 (5 TC) — HWPX는 MCP 필요

### 사전 준비

```bash
mkdir -p /tmp/e2e_sol7/90_Result_Doc && cd /tmp/e2e_sol7 && git init
# 원본 문서 복사 (Sol_5 결과 등)
cp /path/to/review_report.md 90_Result_Doc/
```

### TC-7.1 ~ TC-7.5

```bash
# TC-7.1
opencode run --dir . -m "모델명" "/sk-doc-md design.md를 기반으로 정식 설계서 문서를 작성해줘"

# TC-7.2
opencode run --dir . -m "모델명" "/sk-doc-md review_report.md를 기반으로 정식 테스트 보고서를 작성해줘"

# TC-7.3 (MCP 필요 — TUI 권장)
opencode
# > /sk-doc-hwpx 테스트 보고서를 hwpx로 변환해줘

# TC-7.4 (MCP 필요 — TUI 권장)
opencode
# > /sk-doc-hwpx 리뷰 보고서를 공문(gonmun) 양식으로 hwpx 변환해줘

# TC-7.5 (통합)
opencode run --dir . -m "모델명" --agent sa-documenter "design.md 기반으로 설계서를 작성하고 hwpx로도 변환해줘"
```

---

## 결과 저장

테스트 완료 후 결과를 프로젝트에 저장:

```bash
# Sol 번호에 맞게 변경 (예: Sol_3)
mkdir -p "04_E2E Test/results/Sol_3"
cp -r /tmp/e2e_sol3/90_Result_Doc/* "04_E2E Test/results/Sol_3/"
```

## 전체 한번에 실행 (Sol_2 + Sol_5 예시)

```bash
MODEL="opencode/qwen3.6-plus-free"
TESTCODE="04_E2E Test/testcode/02_samplecode"

# Sol_2
mkdir -p /tmp/e2e_sol2/90_Result_Doc && cp -r "$TESTCODE/"* /tmp/e2e_sol2/ && cd /tmp/e2e_sol2 && git init
opencode run --dir /tmp/e2e_sol2 -m "$MODEL" "/sk-code-analyze 이 프로젝트를 분석해줘"
opencode run --dir /tmp/e2e_sol2 -m "$MODEL" "/sk-analyze-doc analysis_result.md를 보고서로 작성해줘"

# Sol_5
mkdir -p /tmp/e2e_sol5/90_Result_Doc && cp -r "$TESTCODE/"* /tmp/e2e_sol5/ && cd /tmp/e2e_sol5 && git init
opencode run --dir /tmp/e2e_sol5 -m "$MODEL" "/sk-code-review 이 프로젝트 코드를 리뷰해줘"
opencode run --dir /tmp/e2e_sol5 -m "$MODEL" "/sk-security-review 이 프로젝트의 보안 취약점을 점검해줘"
opencode run --dir /tmp/e2e_sol5 -m "$MODEL" "/sk-review-report 리뷰 결과를 종합 보고서로 작성해줘"
```
