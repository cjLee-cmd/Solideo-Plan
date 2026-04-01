---
name: SK_analyze_doc 사용자 매뉴얼
version: 1.0.0
---

# SK_analyze_doc 사용자 매뉴얼

## 개요

SK_code_analyze의 분석 결과를 마크다운 보고서로 변환하는 Skill이다.

## opencode에서 사용하기

### 기본 호출

```
/skill SK_analyze_doc --input analysis_result.json
```

### 출력 경로 지정

```
/skill SK_analyze_doc --input analysis_result.json --output_path ./docs/report.md
```

### SW_analysis Workflow 내에서 자동 호출

```
/workflow SW_analysis --project_path /path/to/project
```

Workflow 실행 시 SK_code_analyze → SK_analyze_doc이 자동으로 순차 실행된다.

## 보고서 구성

| 섹션 | 내용 |
|------|------|
| 프로젝트 개요 | 프로젝트명, 분석일, 범위, 요약 |
| 기술스택 | 언어, 프레임워크, DB 등 표 정리 |
| 디렉토리 구조 | 트리 구조, 디렉토리별 역할 |
| 아키텍처 분석 | 계층 구조, 모듈 역할, 데이터 흐름 |
| 의존성 분석 | 내부/외부 의존 관계 |
| 코드 메트릭스 | 파일 수, 라인 수, 복잡도 |
| 폐쇄망 호환성 | 외부 의존 항목, 조치 필요 사항 |
| 개선 제안 | 구조 개선, 기술 부채, 권고사항 |

## 출력물

- `analysis_report.md` -- 마크다운 형식의 분석 보고서

## 주의사항

- 입력이 유효한 분석 결과 JSON이 아니면 오류를 반환한다
- 보고서는 한국어로 작성된다
