---
name: SM_obsidian_sync 사용자 매뉴얼
version: 1.0.0
---

# SM_obsidian_sync 사용자 매뉴얼

## 개요

Obsidian Vault 폴더 구조에 문서를 저장/조회하는 MCP 서버이다. 폐쇄망 내부 문서 관리용이다.

## 설치 및 설정

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

## 제공 도구

| 도구명 | 설명 |
|--------|------|
| save_document | 문서를 Vault에 저장 |
| list_documents | 문서 목록 조회 |
| read_document | 문서 내용 읽기 |
| organize_vault | 폴더 구조 자동 정리 |

## 폴더 구조

```
Vault/
  프로젝트A/
    design/
    analysis/
    test_report/
    review/
    ...
  프로젝트B/
    ...
```

## 사용 예시

### SW_documentation Workflow에서 자동 호출

```
/workflow SW_documentation --doc_type design --source_data design.md --vault /path/to/vault
```

### 직접 도구 호출

```
save_document(vault_path="/vault", project_name="행정관리", doc_type="design", file_name="design_v1.md", content="...")
list_documents(vault_path="/vault", project_name="행정관리")
```

## 주의사항

- Vault 경로는 폐쇄망 내부 경로여야 한다
- 저장 시 YAML frontmatter가 자동 추가된다
- Obsidian에서 바로 열어볼 수 있는 마크다운 형식으로 저장된다
