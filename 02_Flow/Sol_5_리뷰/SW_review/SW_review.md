---
name: SW_review
type: workflow
description: 코드 리뷰 - 보안 리뷰 - 종합 보고서 Workflow
version: 1.0.0
---

# SW_review

## 목적

코드 리뷰와 보안 리뷰를 수행하고 종합 보고서를 생성하는 전체 흐름을 관리한다.

## 워크플로우 단계

```
[시작]
  |
  v
[Step 1a] SK_code_review 실행 ──┐
  - 입력: target_path             │ 병렬 실행
[Step 1b] SK_security_review 실행 ┘
  - 입력: target_path
  |
  v
[병합] 양쪽 결과 수집
  |
  v
[판단] Critical 이슈 확인
  |
  +-- Critical 있음 --> 사용자 즉시 알림
  |
  +-- Critical 없음 --> 진행
  |
  v
[Step 2] SK_review_report 실행
  - 입력: review_issues + security_issues
  - 출력: review_report.md
  |
  v
[완료]
```

## 단계별 입출력 매핑

| 단계 | 입력 | 출력 | 다음 |
|------|------|------|------|
| Step 1a | target_path | review_issues, quality_score | 병합 |
| Step 1b | target_path | security_issues | 병합 |
| Step 2 | review_issues + security_issues | review_report.md | 완료 |

## 병렬 실행

- SK_code_review와 SK_security_review는 독립적이므로 병렬 실행 가능
- 두 결과가 모두 도착한 후 SK_review_report로 진행

## Critical 이슈 알림

- Critical 이슈 발견 시 워크플로우 완료 전에 즉시 사용자에게 알림
- 보고서 생성은 계속 진행 (알림과 보고서 작성은 독립)

## 사용 Agent

- SA_reviewer: 이 Workflow를 총괄 관리
- SSA_security_checker: Step 1b 보안 심층 분석 보조
