---
name: SK_security_review
type: skill
description: 코드 보안 취약점 점검 (OWASP + 행정망 보안 지침)
version: 1.0.0
---

# SK_security_review

## 목적

코드의 보안 취약점을 점검한다. OWASP Top 10과 행정망 보안 가이드라인을 기준으로 한다.

## 입력 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| target_path | Y | 점검 대상 코드 경로 |
| security_policy | N | 보안 정책 파일 경로 |

## 실행 프롬프트

```
당신은 소프트웨어 보안 전문가입니다.
아래 코드의 보안 취약점을 점검하십시오.

[점검 대상]
경로: {target_path}

[보안 정책]
{security_policy}

[점검 항목]

1. OWASP Top 10
   A01 접근제어 결함 - 인가 우회, 권한 상승 가능 여부
   A02 암호화 실패 - 평문 저장, 약한 암호화 알고리즘
   A03 주입 공격 - SQL Injection, Command Injection, LDAP Injection
   A04 불안전한 설계 - 비즈니스 로직 결함
   A05 보안 구성 오류 - 디버그 모드, 기본 계정, 불필요 포트
   A06 취약한 컴포넌트 - 알려진 취약점 있는 라이브러리
   A07 인증 실패 - 세션 관리, 비밀번호 정책
   A08 데이터 무결성 실패 - 검증 없는 역직렬화
   A09 로깅/모니터링 실패 - 감사로그 부재
   A10 SSRF - 서버 측 요청 위조

2. 행정망 특수 요구사항
   - 개인정보보호법 준수 (개인정보 수집/처리/저장/파기)
   - 접근제어 정책 (역할 기반, 최소 권한)
   - 감사로그 (접근, 변경, 삭제 기록)
   - 데이터 암호화 (전송 중, 저장 시)
   - 세션 관리 (타임아웃, 동시 세션 제한)

3. 입력값 검증
   - 모든 사용자 입력에 대한 서버 측 검증 여부
   - 파일 업로드 검증 (확장자, 크기, MIME 타입)
   - URL 파라미터 검증

[출력 형식]
취약점별로 아래 정보를 포함:
- vuln_id: 고유 ID
- owasp_category: OWASP 분류 (A01~A10)
- severity: critical/high/medium/low
- file: 파일 경로
- line: 라인 번호
- description: 취약점 설명
- risk: 위험 시나리오
- remediation: 수정 가이드
```

## 출력

| 산출물 | 형식 | 설명 |
|--------|------|------|
| security_issues | JSON | 보안 취약점 목록 |
