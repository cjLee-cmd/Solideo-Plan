---
name: SM_test_runner
type: mcp
description: 테스트 프레임워크 실행 및 결과 반환 MCP 서버
version: 1.0.0
---

# SM_test_runner

## 목적

다양한 테스트 프레임워크를 실행하고 표준화된 결과를 반환하는 MCP 서버이다.

## 지원 프레임워크

| 언어 | 프레임워크 | 자동 감지 기준 |
|------|-----------|---------------|
| Java | JUnit 5 | pom.xml / build.gradle |
| Python | pytest | pyproject.toml / conftest.py |
| JavaScript | Jest | package.json (jest 의존성) |
| C# | NUnit | .csproj (NUnit 참조) |
| Go | go test | go.mod |

## 도구 정의

### run_tests

테스트를 실행한다.

```json
{
  "name": "run_tests",
  "description": "테스트 프레임워크를 실행하고 결과를 반환",
  "inputSchema": {
    "type": "object",
    "properties": {
      "project_path": {
        "type": "string",
        "description": "프로젝트 루트 경로"
      },
      "test_path": {
        "type": "string",
        "description": "테스트 파일/디렉토리 경로"
      },
      "framework": {
        "type": "string",
        "enum": ["auto", "junit", "pytest", "jest", "nunit", "gotest"],
        "default": "auto"
      },
      "filter": {
        "type": "string",
        "description": "테스트 필터 패턴 (선택)"
      }
    },
    "required": ["project_path"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "total": { "type": "integer" },
      "passed": { "type": "integer" },
      "failed": { "type": "integer" },
      "skipped": { "type": "integer" },
      "duration_ms": { "type": "integer" },
      "failures": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "test_name": { "type": "string" },
            "message": { "type": "string" },
            "stacktrace": { "type": "string" }
          }
        }
      }
    }
  }
}
```

### get_coverage

커버리지를 측정한다.

```json
{
  "name": "get_coverage",
  "description": "코드 커버리지를 측정하고 결과를 반환",
  "inputSchema": {
    "type": "object",
    "properties": {
      "project_path": { "type": "string" },
      "test_path": { "type": "string" }
    },
    "required": ["project_path"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "line_coverage": { "type": "number" },
      "branch_coverage": { "type": "number" },
      "uncovered_files": {
        "type": "array",
        "items": { "type": "string" }
      }
    }
  }
}
```

### get_test_detail

특정 테스트의 상세 정보를 반환한다.

```json
{
  "name": "get_test_detail",
  "description": "특정 테스트의 실행 상세 정보 반환",
  "inputSchema": {
    "type": "object",
    "properties": {
      "project_path": { "type": "string" },
      "test_name": { "type": "string" }
    },
    "required": ["project_path", "test_name"]
  }
}
```

## 서버 설정

```json
{
  "mcpServers": {
    "SM_test_runner": {
      "command": "sm-test-runner",
      "args": ["--port", "3010"],
      "env": {
        "JAVA_HOME": "/usr/lib/jvm/java-17",
        "PYTHON_PATH": "/usr/bin/python3"
      }
    }
  }
}
```
