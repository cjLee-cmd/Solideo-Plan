---
name: SW_analysis
type: workflow
description: 코드 분석에서 문서화까지의 전체 분석 Workflow
version: 1.0.0
---

# SW_analysis

## 목적

기존 소스코드 프로젝트를 분석하고 결과를 문서화하는 전체 워크플로우를 정의한다.

## 워크플로우 단계

```
[시작]
  |
  v
[Step 1] SK_code_analyze 실행
  - 입력: 프로젝트 경로, 분석 범위
  - 내부: SSA_dep_scanner를 서브태스크로 호출
  - 출력: analysis_result (JSON)
  |
  v
[Step 2] SK_analyze_doc 실행
  - 입력: analysis_result
  - 출력: analysis_report.md
  |
  v
[완료] 보고서 저장
```

## 단계별 입출력 매핑

| 단계 | 입력 | 출력 | 다음 단계 |
|------|------|------|-----------|
| Step 1 | project_path, scope | analysis_result.json | Step 2 |
| Step 1-sub | project_path | dependency_list.json | Step 1에 병합 |
| Step 2 | analysis_result.json | analysis_report.md | 완료 |

## 서브태스크

- Step 1 내에서 SSA_dep_scanner가 의존성 상세 스캔을 병렬 수행
- 결과는 SK_code_analyze의 의존성 분석 섹션에 병합

## 사용 Agent

- SA_analyzer: 이 Workflow를 총괄 관리하는 Agent
