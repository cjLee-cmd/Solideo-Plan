---
name: SK_doc_md 사용자 매뉴얼
version: 1.0.0
---

# SK_doc_md 사용자 매뉴얼

## 개요

다양한 유형의 마크다운 문서를 생성하는 Skill이다.

## opencode에서 사용하기

### 설계서 생성

```
/skill SK_doc_md --doc_type design --source_data design_data.json --project_name "행정관리시스템"
```

### 회의록 생성

```
/skill SK_doc_md --doc_type minutes --source_data "회의 내용 텍스트"
```

### 사용자 정의 템플릿 사용

```
/skill SK_doc_md --doc_type custom --source_data data.json --template my_template.md
```

## 지원 문서 유형

| 유형 | 설명 |
|------|------|
| design | 설계서 |
| analysis | 분석서 |
| test_report | 테스트 보고서 |
| minutes | 회의록 |
| proposal | 제안서 |
| manual | 사용자 매뉴얼 |
| custom | 사용자 정의 |

## 출력물

- 지정된 유형의 마크다운 문서 파일

## 후속 작업

hwpx 형식이 필요하면 SK_doc_hwpx로 변환한다.

```
/skill SK_doc_hwpx --input design.md --template report
```

## 주의사항

- 모든 문서는 한국어로 작성된다
- custom 유형 사용 시 template 파라미터가 필요하다
