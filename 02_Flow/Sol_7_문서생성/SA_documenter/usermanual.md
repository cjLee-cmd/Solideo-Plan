---
name: SA_documenter 사용자 매뉴얼
version: 1.0.0
---

# SA_documenter 사용자 매뉴얼

## 개요

문서 생성을 총괄하는 Agent이다. 마크다운, hwpx 생성과 Vault 관리를 일괄 수행한다.

## opencode에서 사용하기

### Agent 직접 호출

```
/agent SA_documenter
```

### Workflow를 통한 호출

```
/workflow SW_documentation --doc_type report --source_data data.json
```

## Agent가 수행하는 작업

1. 문서 유형과 원본 데이터를 분석한다
2. SK_doc_md로 마크다운 문서를 생성한다
3. 필요시 SK_doc_hwpx로 hwpx 문서를 변환한다
4. SM_obsidian_sync로 Vault에 저장한다

## 대화 예시

```
사용자: 분석 결과를 보고서로 만들어줘
SA_documenter: 분석 결과를 확인합니다.
  - 문서 유형: analysis (분석 보고서)
  - 원본: analysis_result.json
  마크다운 보고서를 생성합니다...
  analysis_report.md 생성 완료 (48줄)
  hwpx 변환이 필요하십니까? (y/n)

사용자: 보고서 양식으로 hwpx도 만들어줘
SA_documenter: report 템플릿으로 hwpx 변환합니다...
  analysis_report.hwpx 생성 완료
  Vault에 저장합니다: 행정관리/analysis/analysis_report.md
  완료되었습니다.
```

## 주의사항

- 공문/제안서는 hwpx 변환을 기본으로 제안한다
- Vault 경로가 설정되어 있으면 자동 저장을 제안한다
- 행정 문서 양식을 정확히 따른다
