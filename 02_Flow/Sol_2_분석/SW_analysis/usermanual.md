---
name: SW_analysis 사용자 매뉴얼
version: 1.0.0
---

# SW_analysis 사용자 매뉴얼

## 개요

코드 분석에서 문서화까지의 전체 분석 Workflow이다.

## opencode에서 사용하기

### 전체 분석 실행

```
/workflow SW_analysis --project_path /path/to/project
```

### 특정 모듈만 분석

```
/workflow SW_analysis --project_path /path/to/project --scope module --target_module auth
```

## 워크플로우 진행

1. **Step 1**: SK_code_analyze가 프로젝트를 분석한다 (SSA_dep_scanner가 의존성 병렬 스캔)
2. **Step 2**: SK_analyze_doc이 분석 결과를 보고서로 변환한다

## 산출물

| 파일 | 생성 시점 | 설명 |
|------|-----------|------|
| analysis_result.json | Step 1 완료 | 구조화된 분석 결과 |
| analysis_report.md | Step 2 완료 | 마크다운 분석 보고서 |

## 주의사항

- 대규모 프로젝트는 모듈별로 나누어 분석하는 것을 권장한다
- 분석 결과는 Sol.3 생성, Sol.4 수정의 참고 자료로 활용된다
