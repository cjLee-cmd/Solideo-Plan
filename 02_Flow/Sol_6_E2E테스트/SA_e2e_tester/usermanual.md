---
name: SA_e2e_tester 사용자 매뉴얼
version: 1.0.0
---

# SA_e2e_tester 사용자 매뉴얼

```
@sa-e2e-tester
```

## Agent 작업 흐름
1. SK_e2e_test_gen으로 시나리오/코드 생성
2. SK_e2e_test_run으로 실행 (실패 시 수정+재실행, 최대 3회)
3. SK_e2e_report로 종합 보고서 생성
4. sm-playwright MCP로 탐색적 테스트 가능
