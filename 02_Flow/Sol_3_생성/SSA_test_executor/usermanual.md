---
name: SSA_test_executor 사용자 매뉴얼
version: 1.0.0
---

# SSA_test_executor 사용자 매뉴얼

## 개요

테스트 실행과 실패 분석을 전담하는 Sub-Agent이다. SA_generator의 하위 에이전트로 동작한다.

## opencode에서 사용하기

### SA_generator를 통한 자동 호출

SW_generation Workflow 실행 시 자동으로 호출된다.

```
/workflow SW_generation --design_file design.md
```

### 단독 호출

```
/sub-agent SSA_test_executor --test_path ./test --project_path ./my_project
```

## 실행 흐름

1. SM_test_runner MCP로 테스트 실행
2. 실패 건 상세 분석
3. 실패 원인 분류 (코드오류/테스트오류/환경문제)
4. SA_generator에 수정 요청 또는 자체 재시도

## 실패 원인 분류

| 분류 | 설명 | 조치 |
|------|------|------|
| 코드 로직 오류 | 구현 코드의 버그 | SA_generator에 수정 요청 |
| 테스트 코드 오류 | 테스트 코드 자체 문제 | 테스트 수정 후 재실행 |
| 환경 설정 문제 | DB 연결, 설정 파일 오류 | 설정 수정 안내 |

## 주의사항

- SM_test_runner MCP가 실행 중이어야 한다
- 최대 3회 재시도 후 자동 중단된다
- 실패 분석 결과는 SA_generator에 자동 전달된다
