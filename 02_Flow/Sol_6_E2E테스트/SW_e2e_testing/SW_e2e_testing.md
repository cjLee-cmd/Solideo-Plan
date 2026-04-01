---
name: SW_e2e_testing
type: workflow
description: E2E 테스트 시나리오 생성 → 실행 → 보고서 Workflow
version: 1.0.0
---

# SW_e2e_testing

## 워크플로우

```
[Step 1] SK_e2e_test_gen → 시나리오 + 테스트코드
[Step 2] SK_e2e_test_run → 실행 (실패 시 수정 후 재실행, 최대 3회)
[Step 3] SK_e2e_report → e2e_report.md
```

## 사용 Agent: SA_e2e_tester
