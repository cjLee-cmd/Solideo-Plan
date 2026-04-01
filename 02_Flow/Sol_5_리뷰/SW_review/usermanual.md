---
name: SW_review 사용자 매뉴얼
version: 1.0.0
---

# SW_review 사용자 매뉴얼

## 개요

코드 리뷰와 보안 리뷰를 병렬로 수행하고 종합 보고서를 생성하는 Workflow이다.

## opencode에서 사용하기

```
/workflow SW_review --target_path ./src
```

### 코딩 컨벤션/보안 정책 지정

```
/workflow SW_review --target_path ./src --convention coding_style.md --security_policy policy.md
```

## 워크플로우 진행

1. **Step 1a+1b**: 코드 리뷰와 보안 리뷰가 병렬 실행된다
2. **판단**: Critical 이슈 있으면 즉시 알림
3. **Step 2**: 종합 보고서 생성

## 산출물

| 파일 | 생성 시점 |
|------|-----------|
| review_issues.json | Step 1a |
| security_issues.json | Step 1b |
| review_report.md | Step 2 |

## 주의사항

- 코드 리뷰와 보안 리뷰는 병렬 실행되므로 순서와 무관하다
- Critical 이슈는 보고서 완성 전에 즉시 알린다
