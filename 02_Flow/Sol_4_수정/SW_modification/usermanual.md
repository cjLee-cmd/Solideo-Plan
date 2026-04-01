---
name: SW_modification 사용자 매뉴얼
version: 1.0.0
---

# SW_modification 사용자 매뉴얼

## 개요

코드 수정부터 영향분석, 테스트, 문서화까지의 전체 수정 Workflow이다.

## opencode에서 사용하기

### 기본 실행

```
/workflow SW_modification --target_path ./src/auth --requirement "로그인 5회 실패 시 계정 잠금"
```

### 검증 기준 포함

```
/workflow SW_modification --target_path ./src --requirement "요구사항.md" --verify_file verify.md
```

## 워크플로우 진행

1. **Step 1**: 코드 수정
2. **Step 2**: 영향범위 검토 (고위험 시 사용자 확인)
3. **Step 3**: 테스트 생성 및 실행 (Sol.3 재사용)
4. **Step 4**: 종합 보고서 생성

## 산출물

| 파일 | 생성 시점 |
|------|-----------|
| change_summary.md | Step 1 |
| impact_report | Step 2 |
| test_result.json | Step 3 |
| modification_report.md | Step 4 |

## 주의사항

- 고위험 영향이 발견되면 사용자 확인 전까지 진행 중단된다
- 테스트 3회 실패 시 자동 중단된다
- Sol.3의 SK_test_gen, SK_test_run을 재사용한다
