---
name: SM_diff_viewer 사용자 매뉴얼
version: 1.0.0
---

# SM_diff_viewer 사용자 매뉴얼

## 개요

수정 전후 코드 차이를 비교하고 통계를 제공하는 MCP 서버이다.

## 설치 및 설정

opencode 설정 파일에 추가:

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

## 제공 도구

| 도구명 | 설명 |
|--------|------|
| get_diff | 파일별 차이 비교 |
| get_project_diff | 프로젝트 전체 변경 목록 |
| get_stat | 변경 통계 (추가/삭제/수정 라인) |

## 사용 예시

### SK_code_modify에서 자동 호출

```
/skill SK_code_modify --target_path ./src/auth
```

SK_code_modify가 내부적으로 SM_diff_viewer를 사용하여 diff를 생성한다.

### 직접 도구 호출

```
get_diff(file_path="./src/auth/login.java")
get_project_diff(project_path="./", base="HEAD~1")
get_stat(project_path="./", base="HEAD~1")
```

## 주의사항

- git이 초기화된 프로젝트에서 가장 정확하게 동작한다
- git이 없는 경우 파일 직접 비교 모드로 동작한다
