---
name: SM_obsidian_sync
type: mcp
description: Obsidian Vault 폴더 구조에 문서 저장/조회 MCP 서버
version: 1.0.0
---

# SM_obsidian_sync

## 목적

Obsidian Vault 폴더 구조에 문서를 저장하고 조회하는 MCP 서버이다. 폐쇄망 내부 문서 관리를 위한 것이다.

## 도구 정의

### save_document

문서를 Vault에 저장한다.

```json
{
  "name": "save_document",
  "description": "문서를 Obsidian Vault에 저장",
  "inputSchema": {
    "type": "object",
    "properties": {
      "vault_path": {
        "type": "string",
        "description": "Obsidian Vault 루트 경로"
      },
      "project_name": {
        "type": "string",
        "description": "프로젝트명 (폴더명)"
      },
      "doc_type": {
        "type": "string",
        "enum": ["design", "analysis", "test_report", "review", "minutes", "proposal", "manual", "etc"],
        "description": "문서 유형 (폴더 분류)"
      },
      "file_name": {
        "type": "string",
        "description": "파일명"
      },
      "content": {
        "type": "string",
        "description": "문서 내용 (마크다운)"
      },
      "tags": {
        "type": "array",
        "items": { "type": "string" },
        "description": "태그 목록"
      }
    },
    "required": ["vault_path", "project_name", "doc_type", "file_name", "content"]
  }
}
```

### list_documents

Vault 내 문서 목록을 반환한다.

```json
{
  "name": "list_documents",
  "description": "프로젝트/유형별 문서 목록 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "vault_path": { "type": "string" },
      "project_name": { "type": "string" },
      "doc_type": { "type": "string" }
    },
    "required": ["vault_path"]
  }
}
```

### read_document

Vault에서 문서를 읽는다.

```json
{
  "name": "read_document",
  "description": "Vault에서 문서 내용 읽기",
  "inputSchema": {
    "type": "object",
    "properties": {
      "file_path": {
        "type": "string",
        "description": "문서 파일 전체 경로"
      }
    },
    "required": ["file_path"]
  }
}
```

### organize_vault

Vault 폴더 구조를 정리한다.

```json
{
  "name": "organize_vault",
  "description": "Vault 폴더 구조 자동 정리 (빈 폴더 정리, 미분류 파일 이동)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "vault_path": { "type": "string" }
    },
    "required": ["vault_path"]
  }
}
```

## 폴더링 규칙

```
{vault_path}/
  {project_name}/
    design/          -- 설계 문서
    analysis/        -- 분석 문서
    test_report/     -- 테스트 보고서
    review/          -- 리뷰 보고서
    minutes/         -- 회의록
    proposal/        -- 제안서
    manual/          -- 사용자 매뉴얼
    etc/             -- 기타
```

## YAML Frontmatter

저장 시 자동 생성:

```yaml
---
project: {project_name}
type: {doc_type}
created: {날짜}
author: SolCode_Lab
tags: [{tags}]
---
```

## 서버 설정

```json
{
  "mcpServers": {
    "SM_obsidian_sync": {
      "command": "sm-obsidian-sync",
      "args": ["--port", "3013", "--vault", "/path/to/vault"]
    }
  }
}
```
