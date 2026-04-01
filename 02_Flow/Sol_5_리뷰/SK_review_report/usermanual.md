---
name: SK_review_report 사용자 매뉴얼
version: 1.0.0
---

# SK_review_report 사용자 매뉴얼

## 개요

코드 리뷰와 보안 리뷰 결과를 종합 보고서로 작성하는 Skill이다.

## opencode에서 사용하기

```
/skill SK_review_report --review_issues review_issues.json --security_issues security_issues.json
```

## 보고서 구성

| 섹션 | 내용 |
|------|------|
| 리뷰 요약 | 대상, 품질 점수, 이슈 수 |
| 코드 품질 이슈 | 심각도별 이슈 목록 |
| 보안 취약점 | OWASP 분류별 취약점 |
| 조치 권고 | 우선순위별 수정 사항 |
| 종합 평가 | 배포 가능 여부 판정 |

## 이슈 ID 체계

- 코드 리뷰 이슈: `REV-001`, `REV-002`, ...
- 보안 취약점: `SEC-001`, `SEC-002`, ...

## 배포 판정

| 판정 | 조건 |
|------|------|
| 배포 가능 | Critical/High 이슈 없음 |
| 조건부 배포 | Critical 없음, High 조치 계획 있음 |
| 배포 불가 | Critical 이슈 미해결 |

## 주의사항

- SW_review Workflow의 마지막 단계에서 자동 호출된다
- Critical 이슈가 1건이라도 있으면 배포 불가로 판정한다
