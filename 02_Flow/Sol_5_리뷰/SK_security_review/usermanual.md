---
name: SK_security_review 사용자 매뉴얼
version: 1.0.0
---

# SK_security_review 사용자 매뉴얼

## 개요

코드의 보안 취약점을 OWASP Top 10과 행정망 기준으로 점검하는 Skill이다.

## opencode에서 사용하기

### 기본 점검

```
/skill SK_security_review --target_path ./src
```

### 보안 정책 파일 지정

```
/skill SK_security_review --target_path ./src --security_policy security_policy.md
```

## 점검 기준

### OWASP Top 10

| 코드 | 항목 |
|------|------|
| A01 | 접근제어 결함 |
| A02 | 암호화 실패 |
| A03 | 주입 공격 (SQL, Command) |
| A04 | 불안전한 설계 |
| A05 | 보안 구성 오류 |
| A06 | 취약한 컴포넌트 |
| A07 | 인증 실패 |
| A08 | 데이터 무결성 실패 |
| A09 | 로깅/모니터링 실패 |
| A10 | SSRF |

### 행정망 추가 점검

- 개인정보보호법 준수
- 접근제어 정책 (역할 기반, 최소 권한)
- 감사로그 (접근/변경/삭제 기록)
- 데이터 암호화 (전송/저장)

## 취약점 심각도

| 등급 | 의미 |
|------|------|
| critical | 즉시 악용 가능, 긴급 수정 |
| high | 공격 시나리오 존재, 조속 수정 |
| medium | 조건부 악용 가능 |
| low | 경미한 보안 개선 사항 |

## 출력물

- 취약점 목록 (OWASP 분류, 심각도, 파일, 수정 가이드 포함)

## 주의사항

- critical/high 취약점은 수정 전까지 배포하지 않는다
- SSA_security_checker가 심층 분석을 보조한다
