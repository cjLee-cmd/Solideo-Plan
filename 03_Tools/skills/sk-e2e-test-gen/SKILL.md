---
name: sk-e2e-test-gen
description: E2E 테스트 시나리오와 Playwright 테스트 코드를 생성한다. 웹 UI 흐름, API 통합, 사용자 시나리오를 커버한다.
---

**[필수] 출력 형식 규칙: 모든 결과는 반드시 마크다운(.md) 파일로 저장한다. .json 파일을 생성하지 마라. 절대 .json 확장자를 사용하지 마라.**

대상 프로젝트의 요구사항과 소스코드를 읽고 E2E 테스트 시나리오와 코드를 생성하라.

## 테스트 유형

### 1. 웹 UI E2E 테스트 (Playwright)

Playwright를 사용하여 브라우저 기반 E2E 테스트를 작성하라.

```python
# 예시: pytest + playwright
from playwright.sync_api import sync_playwright

def test_login_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8080/login")
        page.fill("#username", "admin")
        page.fill("#password", "password")
        page.click("button[type=submit]")
        assert page.url == "http://localhost:8080/dashboard"
        browser.close()
```

작성 규칙:
- 사용자 시나리오 기반으로 테스트를 구성하라 (로그인, CRUD, 결재 흐름 등)
- 페이지 이동, 폼 입력, 버튼 클릭, 결과 확인을 포함하라
- 접근성 선택자(role, label)를 우선 사용하라
- 스크린샷 캡처를 실패 시 자동 저장하도록 설정하라
- headless 모드로 실행 가능하게 작성하라

### 2. API 통합 E2E 테스트

API 엔드포인트 간 연계 흐름을 테스트하라.

```python
import requests

def test_create_and_retrieve_document():
    # 문서 생성
    res = requests.post("http://localhost:8080/api/documents", json={"title": "테스트"})
    assert res.status_code == 201
    doc_id = res.json()["id"]
    # 문서 조회
    res = requests.get(f"http://localhost:8080/api/documents/{doc_id}")
    assert res.json()["title"] == "테스트"
```

### 3. 비즈니스 프로세스 E2E 테스트

행정 업무 흐름(기안→결재→승인→완료)을 전체 시나리오로 테스트하라.

## 시나리오 작성 규칙

각 시나리오에 포함할 항목:
- **시나리오명**: 한국어로 명확히 기술
- **사전 조건**: 테스트 전 필요 상태
- **실행 단계**: 1~N단계 순차 기술
- **예상 결과**: 각 단계별 검증 기준
- **정리**: 테스트 후 데이터 정리

## 출력

- E2E 테스트 코드 파일들 (tests/e2e/ 디렉토리)
- **반드시 `90_Result_Doc/e2e_test_manifest.md`에 시나리오 목록과 실행 방법을 기록하라**
- 90_Result_Doc 디렉토리가 없으면 먼저 생성하라
