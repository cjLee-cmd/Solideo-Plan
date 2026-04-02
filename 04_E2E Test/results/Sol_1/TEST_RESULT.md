# Sol_1 계획 — 테스트 결과

실행일: 2026-04-02
모델: opencode/qwen3.6-plus-free
환경: macOS (인터넷망)

## 결과 요약

| TC | 테스트 | 결과 | 산출물 |
|----|--------|------|--------|
| TC-1.1 | sk-design-spec | ✅ PASS | design.md (8섹션, 41KB) |
| TC-1.2 | sk-design-review | ✅ PASS | review_result.md (조건부승인) |
| TC-1.3 | sa-architect (Speckit 8단계) | ⏳ 미실행 | constitution.md, spec.md 등 일부 생성 |
| TC-1.4 | SW_planning 통합 | ⏳ 미실행 | TC-1.3 선행 필요 |

## TC-1.1 상세

```bash
opencode run --dir /tmp/e2e_sol1 -m "opencode/qwen3.6-plus-free" \
  "/sk-design-spec 프로젝트명: 내부결재시스템, 목적: 전자결재 자동화..."
```

- design.md 8개 섹션 + 부록 정상 생성
- .json 파일 0개
- 외부 URL 0건
- 보안 설계(RBAC, AES-256, 감사로그) 포함

## TC-1.2 상세

```bash
opencode run --dir /tmp/e2e_sol1 -m "opencode/qwen3.6-plus-free" \
  "/sk-design-review 90_Result_Doc/design.md를 리뷰해줘..."
```

- 8개 섹션 순차 리뷰 수행
- 아키텍처 섹션: 캐시 레이어 추가 수정요청
- 나머지 7개 섹션: 승인
- 최종 판정: 조건부승인

## TC-1.3 미실행 사유

sa-architect Agent는 Speckit 8단계를 **멀티턴 대화**로 진행한다.
`opencode run`은 단일 턴이므로 Phase 1 입력 → Phase 2 질문 → Phase 2 입력... 을 `-c` (continue) 옵션으로 이어가야 한다.

### 로컬 실행 방법

```bash
mkdir -p /tmp/e2e_sol1_tc13/90_Result_Doc && cd /tmp/e2e_sol1_tc13 && git init

# Phase 1: Constitution
opencode run --dir . -m "모델명" --agent sa-architect \
  "새 프로젝트를 설계해줘. 프로젝트명: 출장관리시스템, 목적: 출장 신청~정산 자동화, 핵심 원칙: 외부통신 금지(NON-NEGOTIABLE), 보안 지침 준수(MANDATORY), 내부 저장소만 사용(MANDATORY), 테스트 100% 통과(MANDATORY)"

# Phase 2: Specify (세션 이어가기)
opencode run --dir . -m "모델명" -c \
  "문제: 종이 결재 지연, 비즈니스 가치: 결재 50% 단축, P1: 직원 웹 출장신청→승인→정산, P2: 관리자 대시보드, P3: 출장비 초과 추가승인, 엣지: 대리결재, 출장 취소"

# Phase 3: Clarify (1개씩 질문에 응답)
opencode run --dir . -m "모델명" -c "B — 건당 50만원, 초과 시 부서장 추가승인"
opencode run --dir . -m "모델명" -c "A — 직속 상위자 자동 이관"
# ... 질문이 끝날 때까지 반복

# Phase 4: Plan (자동 생성, 확인만)
opencode run --dir . -m "모델명" -c "좋습니다, 진행해주세요"

# Phase 5: Checklist (질문에 응답)
opencode run --dir . -m "모델명" -c "B — 보안과 결재 흐름에 집중"

# Phase 6: Tasks (자동 생성)
opencode run --dir . -m "모델명" -c "확인했습니다"

# Phase 7: Analyze (READ-ONLY 보고)
opencode run --dir . -m "모델명" -c "문제없습니다, 다음 단계로"

# Phase 8: Implement
opencode run --dir . -m "모델명" -c "체크리스트 미완료 무시하고 진행"
```

### 검증

```bash
# Phase별 산출물
for f in constitution.md spec.md research.md data-model.md plan.md quickstart.md tasks.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f"
done
ls 90_Result_Doc/checklists/ 2>/dev/null
ls 90_Result_Doc/contracts/ 2>/dev/null
find 90_Result_Doc/ -name "*.json" | wc -l
```

## TC-1.4 미실행 사유

TC-1.3 완료 후 설계 리뷰 → 수정 → 재리뷰 사이클을 실행해야 한다.
TC-1.3이 선행되어야 하므로 함께 미실행.

## 이 폴더의 파일 목록

TC-1.1, TC-1.2 실행 중 생성된 산출물 + TC-1.3 일부(qwen 모델이 자동 진행한 것):
- constitution.md, spec.md, data-model.md, quickstart.md, tasks.md, design.md
- review_result.md
- checklists/, contracts/
