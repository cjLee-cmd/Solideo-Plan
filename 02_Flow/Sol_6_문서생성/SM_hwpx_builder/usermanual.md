---
name: SM_hwpx_builder 사용자 매뉴얼
version: 1.0.0
---

# SM_hwpx_builder 사용자 매뉴얼

## 개요

한글(hwpx) 문서를 빌드, 변환, 검증하는 MCP 서버이다.

## 설치 및 설정

```json
{
  "mcpServers": {
    "SM_hwpx_builder": {
      "command": "sm-hwpx-builder",
      "args": ["--port", "3012"]
    }
  }
}
```

## 제공 도구

| 도구명 | 설명 |
|--------|------|
| convert_md_to_hwpx | 마크다운 → hwpx 변환 |
| analyze_hwpx | hwpx 구조 분석 |
| build_hwpx | 템플릿 기반 hwpx 빌드 |
| validate_hwpx | hwpx 문서 검증 |
| extract_text_hwpx | hwpx 텍스트 추출 |

## 사용 예시

### SK_doc_hwpx에서 자동 호출

```
/skill SK_doc_hwpx --input report.md --template report
```

### 직접 도구 호출

```
convert_md_to_hwpx(md_path="./report.md", output_path="./report.hwpx")
validate_hwpx(hwpx_path="./report.hwpx")
```

## 지원 템플릿

| 템플릿 | 양식 |
|--------|------|
| gonmun | 공문 |
| report | 보고서 |
| minutes | 회의록 |
| proposal | 제안서 |

## 주의사항

- .hwpx(오픈 XML)만 지원, .hwp(레거시 바이너리) 미지원
- 템플릿 기반 빌드 시 section0.xml 편집은 lxml 사용 권장
