---
name: SM_diff_viewer
type: mcp
description: 수정 전후 코드 차이 비교 MCP 서버
version: 1.0.0
---

# SM_diff_viewer

## 목적

코드 수정 전후의 차이를 비교하고 통계를 제공하는 MCP 서버이다.

## 도구 정의

### get_diff

두 파일 또는 두 버전의 차이를 반환한다.

```json
{
  "name": "get_diff",
  "description": "두 파일 또는 두 버전의 코드 차이를 비교",
  "inputSchema": {
    "type": "object",
    "properties": {
      "file_path": {
        "type": "string",
        "description": "대상 파일 경로"
      },
      "original": {
        "type": "string",
        "description": "원본 내용 또는 파일 경로"
      },
      "modified": {
        "type": "string",
        "description": "수정본 내용 또는 파일 경로"
      },
      "context_lines": {
        "type": "integer",
        "default": 3,
        "description": "diff 컨텍스트 라인 수"
      }
    },
    "required": ["file_path"]
  }
}
```

### get_project_diff

프로젝트 전체의 변경 사항을 반환한다.

```json
{
  "name": "get_project_diff",
  "description": "프로젝트 전체의 변경 사항 목록 반환",
  "inputSchema": {
    "type": "object",
    "properties": {
      "project_path": {
        "type": "string",
        "description": "프로젝트 루트 경로"
      },
      "base": {
        "type": "string",
        "description": "비교 기준 (커밋 해시, 태그, 브랜치)"
      }
    },
    "required": ["project_path"]
  }
}
```

### get_stat

변경 통계를 반환한다.

```json
{
  "name": "get_stat",
  "description": "변경 통계 (추가/삭제/수정 라인 수, 파일 수)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "project_path": { "type": "string" },
      "base": { "type": "string" }
    },
    "required": ["project_path"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "files_changed": { "type": "integer" },
      "lines_added": { "type": "integer" },
      "lines_deleted": { "type": "integer" },
      "lines_modified": { "type": "integer" }
    }
  }
}
```

## 서버 설정

```json
{
  "mcpServers": {
    "SM_diff_viewer": {
      "command": "sm-diff-viewer",
      "args": ["--port", "3011"]
    }
  }
}
```
