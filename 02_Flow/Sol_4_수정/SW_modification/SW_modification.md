---
name: SW_modification
type: workflow
description: 코드 수정 - 영향분석 - 테스트 - 문서화 Workflow
version: 1.0.0
---

# SW_modification

## 목적

기존 소스코드 수정의 전체 흐름을 관리한다. 수정, 영향분석, 테스트, 문서화를 순차적으로 진행한다.

## 워크플로우 단계

```
[시작]
  |
  v
[Step 1] SK_code_modify 실행
  - 입력: 수정 대상, 요구사항, verify.md
  - 출력: 수정된 코드, change_summary.md
  |
  v
[Step 2] SK_impact_check 실행
  - 입력: change_summary.md, 프로젝트 경로
  - 출력: impact_report
  |
  v
[판단 1] 고위험 영향 확인
  |
  +-- 고위험 있음 --> 사용자 확인 요청
  |   +-- 승인 --> [Step 3]
  |   +-- 거부 --> [Step 1]로 회귀 또는 [중단]
  |
  +-- 고위험 없음 --> [Step 3]
  |
  v
[Step 3] SK_test_gen + SK_test_run 실행 (Sol.3 재사용)
  - 입력: 수정된 코드, 영향 범위
  - 출력: test_result
  |
  v
[판단 2] 테스트 결과 확인
  |
  +-- 전체 통과 --> [Step 4]
  +-- 실패 있음 --> [Step 1]로 회귀 (최대 3회)
  +-- 3회 초과 --> [Step 4] (실패 포함)
  |
  v
[Step 4] SK_modify_report 실행
  - 입력: change_summary + impact_report + test_result
  - 출력: modification_report.md
  |
  v
[완료]
```

## 단계별 입출력 매핑

| 단계 | 입력 | 출력 | 다음 |
|------|------|------|------|
| Step 1 | target, requirement, verify.md | change_summary.md | Step 2 |
| Step 2 | change_summary, project_path | impact_report | 판단 1 |
| Step 3 | 수정코드, 영향범위 | test_result | 판단 2 |
| Step 4 | 전체 결과 | modification_report.md | 완료 |

## Sol.3 재사용 요소

- SK_test_gen (Sol.3): 테스트 코드 생성
- SK_test_run (Sol.3): 테스트 실행
- SM_test_runner (Sol.3): 테스트 MCP

## 사용 Agent

- SA_modifier: 이 Workflow를 총괄 관리
- SSA_impact_analyzer: Step 2 심층 분석 보조
