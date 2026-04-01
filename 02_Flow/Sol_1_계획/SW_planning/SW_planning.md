---
name: SW_planning
type: workflow
description: 설계 생성 - 사용자 검증 - 확정의 전체 계획 Workflow
version: 1.0.0
---

# SW_planning

## 목적

신규 소프트웨어 개발을 위한 전체 계획 워크플로우를 정의한다.
설계 문서 생성부터 사용자 검증, 최종 확정까지의 흐름을 관리한다.

## 워크플로우 단계

```
[시작]
  |
  v
[Step 1] SK_design_spec 실행
  - 입력: 프로젝트 요구사항
  - 출력: design.md
  |
  v
[Step 2] SK_design_review 실행
  - 입력: design.md
  - 출력: review_result.md
  |
  v
[판단] 검토 결과 확인
  |
  +-- 승인 --> [Step 3] 설계 확정 --> [완료]
  |
  +-- 조건부승인 --> [Step 2-1] 경미한 수정 반영 --> [Step 3]
  |
  +-- 반려 --> [Step 1]로 회귀 (최대 3회)
  |
  +-- 3회 초과 반려 --> [중단] 사용자에게 수동 개입 요청
```

## 단계별 입출력 매핑

| 단계 | 입력 | 출력 | 다음 단계 |
|------|------|------|-----------|
| Step 1 | 프로젝트 요구사항 | design.md | Step 2 |
| Step 2 | design.md | review_result.md | 판단 |
| Step 2-1 | review_result.md + design.md | design.md (수정) | Step 3 |
| Step 3 | design.md (확정) | design_final.md | 완료 |

## 회귀 조건

- 검토 결과 "반려" 시 Step 1로 회귀
- 회귀 시 이전 review_result.md의 수정 사유를 SK_design_spec에 전달
- 최대 회귀 횟수: 3회
- 3회 초과 시 워크플로우 중단 및 사용자 수동 개입 요청

## 완료 조건

- SK_design_review에서 "승인" 또는 "조건부승인(수정완료)"
- design_final.md가 생성되고 프로젝트 디렉토리에 저장

## 사용 Agent

- SA_architect: 이 Workflow를 총괄 관리하는 Agent
