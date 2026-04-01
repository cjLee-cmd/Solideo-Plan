---
name: SK_modify_report 사용자 매뉴얼
version: 1.0.0
---

# SK_modify_report 사용자 매뉴얼

## 개요

수정 내용, 영향분석, 테스트 결과를 종합 보고서로 작성하는 Skill이다.

## opencode에서 사용하기

```
/skill SK_modify_report --change_summary change_summary.md --impact_report impact_report.md --test_result test_result.json
```

### 검증 기준 포함

```
/skill SK_modify_report --change_summary change_summary.md --impact_report impact_report.md --test_result test_result.json --verify_file verify.md
```

## 보고서 구성

| 섹션 | 내용 |
|------|------|
| 수정 요약 | 수정일, 유형, 요구사항 |
| 변경 파일 목록 | 파일별 변경 유형/라인 수 |
| 변경 상세 | 주요 Diff 발췌 |
| 영향분석 결과 | 영향 대상, 위험도, 조치 |
| 테스트 결과 | 통과/실패, 커버리지 |
| 검증 상태 | verify.md 기준 통과 여부 |
| 잔여 리스크 | 미검증/모니터링 필요 항목 |

## 출력물

- `modification_report.md` -- 종합 보고서

## 주의사항

- SW_modification Workflow의 마지막 단계에서 자동 호출된다
- verify.md를 지정하면 검증 기준 대비 상태를 자동 판정한다
