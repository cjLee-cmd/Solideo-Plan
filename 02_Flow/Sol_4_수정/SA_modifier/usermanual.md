---
name: SA_modifier 사용자 매뉴얼
version: 1.0.0
---

# SA_modifier 사용자 매뉴얼

## 개요

코드 수정을 총괄하는 Agent이다. 행정망 레거시 코드의 안전한 수정에 특화되어 있다.

## opencode에서 사용하기

### Agent 직접 호출

```
/agent SA_modifier
```

### Workflow를 통한 호출

```
/workflow SW_modification --target_path ./src --requirement "요구사항"
```

## Agent가 수행하는 작업

1. 수정 요구사항을 분석하고 전략을 수립한다
2. SK_code_modify로 코드를 수정한다
3. SK_impact_check + SSA_impact_analyzer로 영향을 분석한다
4. 고위험 발견 시 사용자에게 확인을 요청한다
5. SK_test_gen/SK_test_run으로 테스트를 실행한다
6. SK_modify_report로 보고서를 생성한다

## 대화 예시

```
사용자: login.java에서 비밀번호 5회 실패 시 계정 잠금 기능을 추가해줘
SA_modifier: 수정 전략을 수립합니다.
  - 수정 유형: feature (기능 추가)
  - 대상 파일: login.java
  - 영향 예상: UserService, LoginController, user_account 테이블
  수정을 시작합니다...
  [영향분석] 3개 파일 직접 영향, DB 컬럼 추가 필요
  [경고] user_account 테이블에 login_fail_count, locked_until 컬럼 추가
  마이그레이션 스크립트를 포함합니다. 진행하시겠습니까?
```

## 주의사항

- 최소 변경 원칙을 따르며 불필요한 리팩토링을 하지 않는다
- 고위험 변경은 반드시 사용자 확인을 받는다
- DB 스키마 변경 시 마이그레이션 스크립트를 자동 생성한다
