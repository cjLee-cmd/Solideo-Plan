---
name: SK_e2e_test_run
type: skill
description: E2E 테스트를 실행하고 결과를 수집한다
version: 1.0.0
---

# SK_e2e_test_run

## 목적
E2E 테스트를 실행하고 결과(통과/실패, 스크린샷)를 수집한다.

## 실행 방법
- Playwright 웹: `pytest tests/e2e/ --screenshot=only-on-failure`
- API: `pytest tests/e2e/api/`
- sm-playwright MCP로 탐색적 테스트 가능

## 판정
- Critical 시나리오 실패 → 배포 차단
- Non-critical 실패 → 경고

## 출력
- 90_Result_Doc/e2e_test_result.md
