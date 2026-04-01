---
name: SW_generation
type: workflow
description: 코드 생성 - 테스트 생성 - 테스트 실행 - 결과 문서화 Workflow
version: 1.0.0
---

# SW_generation

## 목적

설계 문서 기반 코드 생성부터 테스트 실행, 결과 문서화까지의 전체 흐름을 관리한다.

## 워크플로우 단계

```
[시작]
  |
  v
[Step 1] SK_code_gen 실행
  - 입력: design.md, scope, language
  - 출력: 소스코드 파일들, file_manifest.md
  |
  v
[Step 2] SK_test_gen 실행
  - 입력: 생성된 소스코드 경로
  - 출력: 테스트 코드 파일들, test_manifest.md
  |
  v
[Step 3] SK_test_run 실행 (SM_test_runner MCP 사용)
  - 입력: 테스트 코드 경로
  - 출력: test_result (JSON)
  |
  v
[판단] 테스트 결과 확인
  |
  +-- 전체 통과 --> [Step 4] SK_gen_report --> [완료]
  |
  +-- 실패 있음 --> [Step 1-fix] 코드 수정 --> [Step 3] 재실행
  |                  (최대 3회)
  +-- 3회 초과 실패 --> [Step 4] SK_gen_report (실패 포함) --> [완료-경고]
```

## 단계별 입출력 매핑

| 단계 | 입력 | 출력 | 다음 단계 |
|------|------|------|-----------|
| Step 1 | design.md | 소스코드, file_manifest.md | Step 2 |
| Step 2 | 소스코드 경로 | 테스트 코드, test_manifest.md | Step 3 |
| Step 3 | 테스트 코드 경로 | test_result.json | 판단 |
| Step 1-fix | test_result + 소스코드 | 수정된 소스코드 | Step 3 |
| Step 4 | file_manifest + test_result | generation_report.md | 완료 |

## 회귀 조건

- 테스트 실패 시 Step 1-fix에서 실패 원인 기반 코드 수정
- 최대 회귀 횟수: 3회
- 3회 초과 시 실패 포함 보고서 생성 후 사용자에게 수동 개입 요청

## 사용 Agent

- SA_generator: 이 Workflow를 총괄 관리
- SSA_test_executor: Step 3 테스트 실행 전담
