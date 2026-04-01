---
name: SA_reviewer 사용자 매뉴얼
version: 1.0.0
---

# SA_reviewer 사용자 매뉴얼

## 개요

코드 품질과 보안을 총괄 리뷰하는 Agent이다.

## opencode에서 사용하기

### Agent 직접 호출

```
/agent SA_reviewer
```

### Workflow를 통한 호출

```
/workflow SW_review --target_path ./src
```

## Agent가 수행하는 작업

1. SK_code_review와 SK_security_review를 병렬로 실행한다
2. Critical 이슈 발견 시 즉시 사용자에게 알린다
3. SSA_security_checker로 보안 심층 분석을 보조한다
4. SK_review_report로 종합 보고서를 생성한다

## 대화 예시

```
사용자: ./src 디렉토리의 코드를 리뷰해줘
SA_reviewer: 코드 리뷰를 시작합니다.
  코드 품질 리뷰와 보안 리뷰를 병렬로 진행합니다...

  [코드 리뷰 결과] 품질 점수: 72/100
  - Critical: 0건
  - Major: 3건 (중복 코드 2건, 에러 처리 미흡 1건)
  - Minor: 7건

  [보안 리뷰 결과]
  - Critical: 1건 (SQL Injection - UserDao.java:45)
  - High: 1건 (평문 비밀번호 저장 - AuthService.java:23)
  - Medium: 2건

  [긴급] SQL Injection 취약점이 발견되었습니다.
  수정 방법: PreparedStatement로 파라미터 바인딩 사용

  종합 보고서를 review_report.md로 생성합니다.
  판정: 배포 불가 (Critical 1건 미해결)
```

## 주의사항

- Critical 보안 이슈가 있으면 배포 불가로 판정한다
- 수정 코드 예시를 함께 제공한다
