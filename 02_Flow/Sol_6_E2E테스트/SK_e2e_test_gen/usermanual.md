---
name: SK_e2e_test_gen 사용자 매뉴얼
version: 1.0.0
---

# SK_e2e_test_gen 사용자 매뉴얼

## opencode에서 사용하기

```
/sk-e2e-test-gen
```

## Playwright 웹 테스트 예시

```python
from playwright.sync_api import sync_playwright

def test_login_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8080/login")
        page.fill("#username", "admin")
        page.click("button[type=submit]")
        assert page.url.endswith("/dashboard")
```

## 주의사항
- headless 모드로 작성하라
- 접근성 선택자(role, label)를 우선 사용하라
