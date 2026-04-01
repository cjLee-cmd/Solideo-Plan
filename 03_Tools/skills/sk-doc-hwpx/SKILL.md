---
name: sk-doc-hwpx
description: 마크다운 문서를 한글(hwpx) 형식으로 변환한다. 공문, 보고서, 회의록, 제안서 템플릿을 지원한다. sm-hwpx-builder MCP를 사용한다.
---

**[필수] 출력 형식 규칙: 모든 결과는 반드시 마크다운(.md) 파일로 저장한다. .json 파일을 생성하지 마라. 절대 .json 확장자를 사용하지 마라.**


마크다운 파일을 읽고 hwpx 형식으로 변환하라. sm-hwpx-builder MCP의 도구를 사용하라.

## 변환 방식

### 템플릿 미지정 시 (자동 변환)
sm-hwpx-builder의 convert_md_to_hwpx 도구를 호출하라.

### 템플릿 지정 시 (템플릿 기반)
1. analyze_hwpx로 템플릿 구조 분석
2. extract_hwpx_xml로 section0.xml 추출
3. 마크다운 내용을 section0.xml에 매핑 (lxml 사용)
4. build_hwpx로 최종 hwpx 빌드
5. validate_hwpx로 검증

## 지원 템플릿

- gonmun: 공문 양식
- report: 보고서 양식
- minutes: 회의록 양식
- proposal: 제안서 양식

## 주의사항

- .hwpx(오픈 XML)만 지원한다. .hwp(레거시 바이너리)는 미지원이다.
- 복잡한 표 레이아웃은 템플릿 기반 변환을 사용하라.

## 저장 경로

변환된 hwpx 파일을 `90_Result_Doc/` 디렉토리에 저장하라.
