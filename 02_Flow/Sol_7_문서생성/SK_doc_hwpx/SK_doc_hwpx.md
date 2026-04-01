---
name: SK_doc_hwpx
type: skill
description: 마크다운 문서를 한글(hwpx) 형식으로 변환/생성
version: 1.0.0
---

# SK_doc_hwpx

## 목적

마크다운 문서를 한글(hwpx) 형식으로 변환하거나, 한글 문서를 직접 생성한다. SM_hwpx_builder MCP를 통해 실제 변환을 수행한다.

## 입력 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| input | Y | 마크다운 파일 경로 또는 문서 내용 |
| template | N | hwpx 템플릿 (gonmun/report/minutes/proposal). 기본: 없음(자동 변환) |
| output_path | N | 출력 hwpx 파일 경로 |

## 실행 프롬프트

```
당신은 한글(hwpx) 문서 변환 전문가입니다.
마크다운 문서를 hwpx 형식으로 변환하십시오.

[입력 문서]
{input}

[변환 템플릿]
{template}

[변환 절차]

1. 템플릿 미지정 시 (자동 변환)
   - SM_hwpx_builder의 convert_md_to_hwpx 도구 사용
   - 마크다운 → hwpx 직접 변환
   - 제목, 표, 코드블록, 목록, 인용 등 자동 변환

2. 템플릿 지정 시 (템플릿 기반)
   - SM_hwpx_builder의 analyze_hwpx로 템플릿 구조 분석
   - extract_hwpx_xml로 section0.xml 추출
   - 마크다운 내용을 section0.xml에 매핑
   - build_hwpx로 최종 hwpx 빌드
   - validate_hwpx로 검증

[사용 가능 템플릿]
- gonmun: 공문 양식
- report: 보고서 양식
- minutes: 회의록 양식
- proposal: 제안서 양식

[SM_hwpx_builder MCP 도구]
- convert_md_to_hwpx: 마크다운 → hwpx 직접 변환
- analyze_hwpx: hwpx 구조 분석
- extract_hwpx_xml: XML 추출
- build_hwpx: hwpx 빌드
- validate_hwpx: 문서 검증
```

## 출력

| 산출물 | 형식 | 설명 |
|--------|------|------|
| output.hwpx | HWPX | 생성된 한글 문서 |
