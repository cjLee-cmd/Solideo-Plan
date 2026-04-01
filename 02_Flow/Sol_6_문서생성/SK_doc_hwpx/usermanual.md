---
name: SK_doc_hwpx 사용자 매뉴얼
version: 1.0.0
---

# SK_doc_hwpx 사용자 매뉴얼

## 개요

마크다운 문서를 한글(hwpx) 형식으로 변환하거나 직접 생성하는 Skill이다.

## opencode에서 사용하기

### 자동 변환 (템플릿 없이)

```
/skill SK_doc_hwpx --input report.md
```

### 템플릿 기반 변환

```
/skill SK_doc_hwpx --input report.md --template report
```

### 공문 양식으로 변환

```
/skill SK_doc_hwpx --input notice.md --template gonmun --output_path ./output/notice.hwpx
```

## 지원 템플릿

| 템플릿 | 양식 | 용도 |
|--------|------|------|
| gonmun | 공문 | 공식 문서, 통보문 |
| report | 보고서 | 기술 보고서, 분석 보고서 |
| minutes | 회의록 | 회의 기록 |
| proposal | 제안서 | 사업 제안, 기술 제안 |

## 변환 방식

| 방식 | 조건 | 설명 |
|------|------|------|
| 자동 변환 | 템플릿 미지정 | md → hwpx 직접 변환 |
| 템플릿 기반 | 템플릿 지정 | 양식에 맞춰 내용 배치 |

## 출력물

- `.hwpx` 파일 (한글 오픈 XML 문서)

## 주의사항

- SM_hwpx_builder MCP가 실행 중이어야 한다
- .hwp(레거시) 형식은 지원하지 않으며 .hwpx만 지원한다
- 복잡한 표 레이아웃은 템플릿 기반 변환을 권장한다
