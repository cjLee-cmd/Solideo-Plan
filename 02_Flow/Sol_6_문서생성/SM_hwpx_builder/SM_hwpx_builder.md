---
name: SM_hwpx_builder
type: mcp
description: HWPX 문서 빌드/변환/검증 MCP 서버
version: 1.0.0
---

# SM_hwpx_builder

## 목적

한글(hwpx) 문서를 빌드, 변환, 검증하는 MCP 서버이다.

## 도구 정의

### convert_md_to_hwpx

마크다운 파일을 hwpx로 직접 변환한다.

```json
{
  "name": "convert_md_to_hwpx",
  "description": "마크다운 파일을 hwpx 형식으로 변환",
  "inputSchema": {
    "type": "object",
    "properties": {
      "md_path": {
        "type": "string",
        "description": "마크다운 파일 경로"
      },
      "output_path": {
        "type": "string",
        "description": "출력 hwpx 파일 경로"
      }
    },
    "required": ["md_path"]
  }
}
```

### analyze_hwpx

hwpx 문서의 구조를 분석한다.

```json
{
  "name": "analyze_hwpx",
  "description": "hwpx 파일의 구조 분석",
  "inputSchema": {
    "type": "object",
    "properties": {
      "hwpx_path": {
        "type": "string",
        "description": "hwpx 파일 경로"
      }
    },
    "required": ["hwpx_path"]
  }
}
```

### build_hwpx

템플릿 기반으로 hwpx 문서를 빌드한다.

```json
{
  "name": "build_hwpx",
  "description": "수정된 XML로 hwpx 문서 빌드",
  "inputSchema": {
    "type": "object",
    "properties": {
      "source_dir": {
        "type": "string",
        "description": "추출된 hwpx 소스 디렉토리"
      },
      "output_path": {
        "type": "string",
        "description": "출력 hwpx 파일 경로"
      }
    },
    "required": ["source_dir"]
  }
}
```

### validate_hwpx

생성된 hwpx 문서의 구조적 유효성을 검증한다.

```json
{
  "name": "validate_hwpx",
  "description": "hwpx 문서 구조 검증",
  "inputSchema": {
    "type": "object",
    "properties": {
      "hwpx_path": { "type": "string" }
    },
    "required": ["hwpx_path"]
  }
}
```

### extract_text_hwpx

hwpx 문서에서 텍스트를 추출한다.

```json
{
  "name": "extract_text_hwpx",
  "description": "hwpx 문서에서 텍스트 내용 추출",
  "inputSchema": {
    "type": "object",
    "properties": {
      "hwpx_path": { "type": "string" }
    },
    "required": ["hwpx_path"]
  }
}
```

## 서버 설정

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
