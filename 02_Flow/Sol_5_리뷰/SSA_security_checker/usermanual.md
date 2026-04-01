---
name: SSA_security_checker 사용자 매뉴얼
version: 1.0.0
---

# SSA_security_checker 사용자 매뉴얼

## 개요

보안 취약점을 심층 분석하는 Sub-Agent이다. SA_reviewer의 하위 에이전트로 동작한다.

## opencode에서 사용하기

### SA_reviewer를 통한 자동 호출

SW_review Workflow 실행 시 SK_security_review와 함께 자동 호출된다.

### 단독 호출

```
/sub-agent SSA_security_checker --target_path ./src
```

## 분석 방법

| 방법 | 설명 |
|------|------|
| 정적 분석 | 위험 패턴, 입력값 검증 누락, SQL 연결 |
| 데이터 흐름 분석 | 미검증 사용자 입력 경로, 민감 데이터 경로 |
| 설정 점검 | 디버그 모드, 기본 계정, CORS/CSRF |
| 행정망 점검 | 개인정보, 접근제어, 감사로그 |

## 출력 형식

각 취약점에 대해:
- 상세 설명
- 공격 시나리오
- 수정 전/후 코드 예시
- 참고 자료

## 주의사항

- SK_security_review의 결과를 보완하는 심층 분석 역할이다
- 수정 코드 예시는 참고용이며 프로젝트 맥락에 맞게 조정해야 한다
