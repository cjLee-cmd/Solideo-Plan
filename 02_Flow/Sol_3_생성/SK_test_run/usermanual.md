---
name: SK_test_run 사용자 매뉴얼
version: 1.0.0
---

# SK_test_run 사용자 매뉴얼

## 개요

테스트 코드를 실행하고 결과를 수집하는 Skill이다. SM_test_runner MCP를 통해 실행한다.

## opencode에서 사용하기

### 기본 호출

```
/skill SK_test_run --test_path ./test
```

### 커버리지 비활성화

```
/skill SK_test_run --test_path ./test --coverage false
```

## 결과 항목

| 항목 | 설명 |
|------|------|
| total | 총 테스트 수 |
| passed | 통과 수 |
| failed | 실패 수 |
| skipped | 스킵 수 |
| coverage_line | 라인 커버리지 (%) |
| coverage_branch | 브랜치 커버리지 (%) |
| duration | 실행 시간 |
| failures | 실패 테스트 상세 목록 |

## 결과 판정

| 상태 | 조건 | 후속 |
|------|------|------|
| 성공 | 모든 통과 + 커버리지 달성 | SK_gen_report로 문서화 |
| 실패 | 1건 이상 실패 | 코드 수정 후 재실행 |
| 경고 | 통과하나 커버리지 미달 | 추가 테스트 생성 |

## 주의사항

- SM_test_runner MCP가 실행 중이어야 한다
- 테스트 환경(DB, 설정)이 올바르게 구성되어야 한다
- Sol.3(생성)과 Sol.4(수정) 모두에서 사용된다
