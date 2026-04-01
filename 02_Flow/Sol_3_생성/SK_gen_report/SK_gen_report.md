---
name: SK_gen_report
type: skill
description: 코드 생성 및 테스트 결과 종합 문서화
version: 1.0.0
---

# SK_gen_report

## 목적

코드 생성 과정과 테스트 결과를 종합하여 보고서(generation_report.md)를 작성한다.

## 입력 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| file_manifest | Y | SK_code_gen의 file_manifest.md 경로 |
| test_result | Y | SK_test_run의 테스트 결과 (JSON 또는 파일 경로) |
| design_file | N | 원본 design.md (대조용) |
| output_path | N | 출력 경로 (기본: ./generation_report.md) |

## 실행 프롬프트

```
당신은 기술 문서 작성 전문가입니다.
코드 생성 및 테스트 결과를 종합 보고서로 작성하십시오.

[입력 데이터]
- 파일 매니페스트: {file_manifest}
- 테스트 결과: {test_result}
- 설계 문서: {design_file}

[보고서 구성]

# 코드 생성 보고서

## 1. 생성 요약
- 생성일, 설계 문서 기준, 생성 범위
- 총 생성 파일 수, 총 코드 라인 수

## 2. 생성 파일 목록
| 파일 경로 | 유형 | 라인 수 | 설명 |
표 형식

## 3. 설계 대비 구현 현황
| 설계 항목 | 구현 상태 | 비고 |
design.md 대비 구현 완료/미완료 항목

## 4. 테스트 결과
### 4.1 요약
- 총 테스트 / 통과 / 실패 / 스킵
- 커버리지

### 4.2 실패 테스트 상세
| 테스트명 | 실패 원인 | 조치 필요 |

## 5. 미해결 사항
- 구현되지 않은 항목
- 추가 작업 필요 사항
- 알려진 제한사항

## 6. 다음 단계
- 권장 후속 작업
```

## 출력

| 산출물 | 형식 | 설명 |
|--------|------|------|
| generation_report.md | Markdown | 코드 생성 종합 보고서 |
