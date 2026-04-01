---
name: SM_test_runner 사용자 매뉴얼
version: 1.0.0
---

# SM_test_runner 사용자 매뉴얼

## 개요

테스트 프레임워크를 실행하고 결과를 반환하는 MCP 서버이다.

## 설치 및 설정

opencode 설정 파일에 아래를 추가한다:

```json
{
  "mcpServers": {
    "SM_test_runner": {
      "command": "sm-test-runner",
      "args": ["--port", "3010"]
    }
  }
}
```

## 제공 도구

| 도구명 | 설명 |
|--------|------|
| run_tests | 테스트 실행 및 결과 반환 |
| get_coverage | 커버리지 측정 |
| get_test_detail | 특정 테스트 상세 정보 |

## 사용 예시

### SK_test_run에서 자동 호출

```
/skill SK_test_run --test_path ./test
```

SK_test_run이 내부적으로 SM_test_runner의 도구를 호출한다.

### 직접 MCP 도구 호출

```
run_tests(project_path="./my_project", test_path="./test")
get_coverage(project_path="./my_project")
get_test_detail(project_path="./my_project", test_name="test_login_success")
```

## 지원 프레임워크

| 언어 | 프레임워크 |
|------|-----------|
| Java | JUnit 5 |
| Python | pytest |
| JavaScript | Jest |
| C# | NUnit |
| Go | go test |

## 주의사항

- 폐쇄망 내부에서 실행되므로 외부 테스트 서비스 연동 불가
- 테스트 실행에 필요한 런타임(JDK, Python, Node.js)이 설치되어 있어야 한다
- 대규모 테스트 실행 시 타임아웃 설정을 확인한다
