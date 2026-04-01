---
name: SA_generator 사용자 매뉴얼
version: 1.0.0
---

# SA_generator 사용자 매뉴얼

## 개요

코드 생성을 총괄하는 Agent이다. 설계 문서 기반 코드 생성, 테스트, 문서화를 일괄 관리한다.

## opencode에서 사용하기

### Agent 직접 호출

```
/agent SA_generator
```

### Workflow를 통한 호출

```
/workflow SW_generation --design_file design.md
```

## Agent가 수행하는 작업

1. design.md를 읽고 생성 전략을 수립한다
2. SK_code_gen으로 소스코드를 생성한다
3. SK_test_gen으로 테스트 코드를 생성한다
4. SSA_test_executor를 통해 테스트를 실행한다
5. 실패 시 원인 분석 후 코드를 수정한다 (최대 3회)
6. SK_gen_report로 종합 보고서를 생성한다

## 대화 예시

```
사용자: design.md를 기반으로 코드를 생성해줘
SA_generator: design.md를 분석합니다.
  - 아키텍처: Spring Boot + MyBatis + PostgreSQL
  - 모듈 5개: auth, user, document, approval, common
  코드 생성을 시작합니다...
  [1/5] auth 모듈 생성 완료 (12개 파일)
  [2/5] user 모듈 생성 완료 (8개 파일)
  ...
  테스트 코드 생성 및 실행 중...
  테스트 결과: 45/47 통과 (2개 실패)
  실패 원인 분석 후 수정합니다...
  재실행: 47/47 통과 (커버리지 83%)
  generation_report.md를 생성합니다.
```

## 주의사항

- 보안 관련 코드(인증, 암호화, 감사로그)는 자동 포함된다
- 외부 네트워크 호출은 자동 배제된다
