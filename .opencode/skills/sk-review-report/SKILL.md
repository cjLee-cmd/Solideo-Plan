---
name: sk-review-report
description: 코드 리뷰와 보안 리뷰 결과를 종합하여 review_report.md를 작성한다. 이슈 ID를 부여하고 배포 가능 여부를 판정한다.
---

코드 리뷰 결과와 보안 리뷰 결과를 읽고 종합 보고서를 작성하라.

## 보고서 구성

1. **리뷰 요약** - 리뷰일, 대상 범위, 코드 품질 점수, 총 이슈 수(심각도별)
2. **코드 품질 이슈** - Critical/Major/Minor/Info 별로 정리 (이슈 ID: REV-001 형식)
3. **보안 취약점** - Critical~Low 별로 정리 (이슈 ID: SEC-001 형식, OWASP 분류 포함)
4. **조치 권고** - 즉시 수정(Critical/High), 수정 권장(Major/Medium), 개선 검토(Minor/Low)
5. **종합 평가** - 배포 가능 여부 판정

## 배포 판정 기준

- **배포 가능**: Critical/High 이슈 없음
- **조건부 배포**: Critical 없음, High 조치 계획 있음
- **배포 불가**: Critical 이슈 미해결

review_report.md로 저장하라.
