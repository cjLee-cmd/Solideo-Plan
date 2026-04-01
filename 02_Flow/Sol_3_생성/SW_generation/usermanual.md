---
name: SW_generation 사용자 매뉴얼
version: 1.0.0
---

# SW_generation 사용자 매뉴얼

## 개요

코드 생성부터 테스트, 문서화까지의 전체 생성 Workflow이다.

## opencode에서 사용하기

### 전체 프로젝트 생성

```
/workflow SW_generation --design_file design.md
```

### 특정 모듈만 생성

```
/workflow SW_generation --design_file design.md --scope module --target_module auth
```

## 워크플로우 진행

1. **Step 1**: design.md 기반 코드 생성
2. **Step 2**: 테스트 코드 자동 생성
3. **Step 3**: 테스트 실행 및 결과 수집
4. **판단**: 실패 시 코드 수정 후 재실행 (최대 3회)
5. **Step 4**: 종합 보고서 생성

## 산출물

| 파일 | 생성 시점 |
|------|-----------|
| 소스코드 파일들 | Step 1 |
| file_manifest.md | Step 1 |
| 테스트 코드 파일들 | Step 2 |
| test_result.json | Step 3 |
| generation_report.md | Step 4 |

## 주의사항

- design.md가 SK_design_review를 통해 확정된 상태여야 한다
- SM_test_runner MCP가 실행 중이어야 한다
- 3회 실패 시 자동 중단되며, 실패 내역이 보고서에 포함된다
