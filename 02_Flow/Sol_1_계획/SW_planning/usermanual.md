---
name: SW_planning 사용자 매뉴얼
version: 1.0.0
---

# SW_planning 사용자 매뉴얼

## 개요

설계 생성부터 사용자 검증, 최종 확정까지의 전체 계획 Workflow이다.

## opencode에서 사용하기

### 전체 워크플로우 실행

```
/workflow SW_planning --project_name "행정관리시스템" --purpose "내부 행정업무 전산화" --requirements "requirements.md"
```

### 특정 단계부터 재개

```
/workflow SW_planning --resume --from step2 --input design.md
```

## 워크플로우 진행

1. **Step 1**: SK_design_spec이 실행되어 design.md를 생성한다
2. **Step 2**: SK_design_review가 실행되어 사용자에게 검토를 요청한다
3. **판단**: 검토 결과에 따라 분기한다
   - 승인: design_final.md로 확정
   - 조건부승인: 경미한 수정 후 확정
   - 반려: Step 1로 회귀 (최대 3회)

## 산출물

| 파일 | 생성 시점 | 설명 |
|------|-----------|------|
| design.md | Step 1 완료 | 초안 설계 문서 |
| review_result.md | Step 2 완료 | 검토 결과 |
| design_final.md | 워크플로우 완료 | 확정된 설계 문서 |

## 중단 및 재개

- 워크플로우 중간에 중단하면 현재 단계와 산출물이 보존된다
- `--resume` 옵션으로 중단 지점부터 재개할 수 있다

## 주의사항

- 3회 반려 시 자동 중단되며, 요구사항 자체를 재검토해야 한다
- design_final.md는 Sol.3 생성 단계의 입력으로 사용된다
