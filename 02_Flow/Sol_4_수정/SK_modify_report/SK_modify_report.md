---
name: SK_modify_report
type: skill
description: 수정 내용, 영향분석, 테스트 결과 종합 문서화
version: 1.0.0
---

# SK_modify_report

## 목적

코드 수정 과정의 변경 사항, 영향분석, 테스트 결과를 종합하여 보고서(modification_report.md)를 작성한다.

## 입력 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| change_summary | Y | SK_code_modify의 변경 요약 |
| impact_report | Y | SK_impact_check의 영향분석 결과 |
| test_result | Y | SK_test_run의 테스트 결과 |
| verify_file | N | 검증 기준 문서(verify.md) |

## 실행 프롬프트

```
당신은 기술 문서 작성 전문가입니다.
수정 결과를 종합 보고서로 작성하십시오.

[입력 데이터]
- 변경 요약: {change_summary}
- 영향분석: {impact_report}
- 테스트 결과: {test_result}
- 검증 기준: {verify_file}

[보고서 구성]

# 코드 수정 보고서

## 1. 수정 요약
- 수정일, 수정 유형, 요구사항 요약

## 2. 변경 파일 목록
| 파일 경로 | 변경 유형 | 변경 라인 수 | 설명 |

## 3. 변경 상세 (Diff)
파일별 주요 변경 내용 발췌

## 4. 영향분석 결과
| 영향 유형 | 대상 | 위험도 | 조치 상태 |

## 5. 테스트 결과
- 실행 결과 요약
- 실패 항목 및 조치

## 6. 검증 상태
verify.md 기준 대비 검증 통과 여부

## 7. 잔여 리스크
- 미검증 항목
- 추가 모니터링 필요 사항
```

## 출력

| 산출물 | 형식 | 설명 |
|--------|------|------|
| modification_report.md | Markdown | 수정 종합 보고서 |
