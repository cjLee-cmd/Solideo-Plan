---
name: SK_gen_report 사용자 매뉴얼
version: 1.0.0
---

# SK_gen_report 사용자 매뉴얼

## 개요

코드 생성 및 테스트 결과를 종합 보고서로 작성하는 Skill이다.

## opencode에서 사용하기

### 기본 호출

```
/skill SK_gen_report --file_manifest file_manifest.md --test_result test_result.json
```

### 설계 대비 구현 현황 포함

```
/skill SK_gen_report --file_manifest file_manifest.md --test_result test_result.json --design_file design.md
```

## 보고서 구성

| 섹션 | 내용 |
|------|------|
| 생성 요약 | 생성일, 파일 수, 라인 수 |
| 파일 목록 | 생성된 전체 파일 표 |
| 설계 대비 현황 | design.md 대비 구현 상태 |
| 테스트 결과 | 통과/실패/커버리지 |
| 미해결 사항 | 미구현, 제한사항 |
| 다음 단계 | 권장 후속 작업 |

## 출력물

- `generation_report.md` -- 종합 보고서

## 주의사항

- SW_generation Workflow의 마지막 단계에서 자동 호출된다
- design_file을 지정하면 설계 대비 구현율을 정확히 산출한다
