---
name: SSA_impact_analyzer 사용자 매뉴얼
version: 1.0.0
---

# SSA_impact_analyzer 사용자 매뉴얼

## 개요

코드 변경의 파급 효과를 심층 분석하는 Sub-Agent이다. SA_modifier의 하위 에이전트로 동작한다.

## opencode에서 사용하기

### SA_modifier를 통한 자동 호출

SW_modification Workflow 실행 시 SK_impact_check와 함께 자동 호출된다.

### 단독 호출

```
/sub-agent SSA_impact_analyzer --change_diff changes.diff --project_path ./
```

## 분석 방법

| 방법 | 설명 |
|------|------|
| 호출 그래프 추적 | 변경 함수 호출 경로 3단계 추적 |
| 데이터 흐름 분석 | 변경 데이터 구조의 전파 경로 |
| 설정 영향 분석 | 설정 변경의 Bean/컴포넌트 영향 |
| DB 영향 분석 | 스키마 변경의 쿼리/매퍼 영향 |

## 출력

- 영향 파일 목록 (직접/간접)
- 위험도 등급
- 필수 테스트 대상 파일 목록
- 권고 조치 사항

## 주의사항

- SK_impact_check의 결과를 보완하는 심층 분석 역할이다
- 대규모 프로젝트에서는 분석에 시간이 소요될 수 있다
