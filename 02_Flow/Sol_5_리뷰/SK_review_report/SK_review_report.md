---
name: SK_review_report
type: skill
description: 코드 리뷰 + 보안 리뷰 결과 종합 문서화
version: 1.0.0
---

# SK_review_report

## 목적

SK_code_review와 SK_security_review의 결과를 종합하여 리뷰 보고서를 작성한다.

## 입력 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| review_issues | Y | SK_code_review 결과 |
| security_issues | Y | SK_security_review 결과 |
| quality_score | N | 코드 품질 점수 |

## 실행 프롬프트

```
당신은 기술 문서 작성 전문가입니다.
코드 리뷰와 보안 리뷰 결과를 종합 보고서로 작성하십시오.

[입력 데이터]
- 코드 리뷰 결과: {review_issues}
- 보안 리뷰 결과: {security_issues}
- 품질 점수: {quality_score}

[보고서 구성]

# 코드 리뷰 보고서

## 1. 리뷰 요약
- 리뷰일, 대상 범위
- 코드 품질 점수
- 총 이슈 수 (심각도별)

## 2. 코드 품질 이슈
### Critical
### Major
### Minor
### Info
각 이슈: ID, 파일, 라인, 설명, 개선 제안

## 3. 보안 취약점
### Critical / High
### Medium
### Low
각 취약점: ID, OWASP 분류, 파일, 설명, 수정 가이드

## 4. 조치 권고
- 즉시 수정 필요 (Critical/High)
- 수정 권장 (Major/Medium)
- 개선 검토 (Minor/Low)

## 5. 종합 평가
- 배포 가능 여부 판정
- 조건부 배포 시 필수 조치 사항

[이슈 추적]
각 이슈에 고유 ID 부여 (REV-001, SEC-001 형식)
```

## 출력

| 산출물 | 형식 | 설명 |
|--------|------|------|
| review_report.md | Markdown | 리뷰 종합 보고서 |
