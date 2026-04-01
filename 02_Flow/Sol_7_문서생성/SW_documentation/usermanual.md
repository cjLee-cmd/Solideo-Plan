---
name: SW_documentation 사용자 매뉴얼
version: 1.0.0
---

# SW_documentation 사용자 매뉴얼

## 개요

문서 생성부터 변환, Vault 저장까지의 전체 문서생성 Workflow이다.

## opencode에서 사용하기

### 마크다운 문서만 생성

```
/workflow SW_documentation --doc_type design --source_data design_data.json
```

### hwpx 변환 포함

```
/workflow SW_documentation --doc_type report --source_data data.json --hwpx true --template report
```

### Vault 저장 포함

```
/workflow SW_documentation --doc_type analysis --source_data analysis_result.json --vault /path/to/vault --project_name "행정관리"
```

## 워크플로우 진행

1. **Step 1**: 문서 유형 판별
2. **Step 2**: SK_doc_md로 마크다운 문서 생성
3. **Step 3**: (필요시) SK_doc_hwpx로 hwpx 변환
4. **Step 4**: SM_obsidian_sync로 Vault에 저장

## 산출물

| 파일 | 조건 |
|------|------|
| {doc_type}.md | 항상 생성 |
| {doc_type}.hwpx | hwpx 요청 시 |

## 주의사항

- Vault 경로를 지정하지 않으면 현재 디렉토리에 파일만 생성한다
- 공문/제안서는 hwpx 변환이 기본 활성화된다
