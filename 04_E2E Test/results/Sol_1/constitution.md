# Constitution — 내부결재시스템

> **버전**: 1.0  
> **작성일**: 2026-04-02  
> **적용 범위**: 내부결재시스템 전 개발 라이프사이클

---

## 1. Core Principles

| 원칙명 | 강제 수준 | 상세 규칙 | 근거 (Rationale) |
|--------|-----------|-----------|-------------------|
| 외부 네트워크 차단 | NON-NEGOTIABLE | 모든 외부 HTTP/HTTPS/TCP 통신 금지. 외부 API 호출, 외부 CDN, 외부 패키지 저장소(maven central 등) 사용 불가 | 폐쇄망 환경의 물리적/정책적 제약. 위반 시 보안 사고 |
| 행정망 보안 지침 준수 | MANDATORY | 모든 API는 인증/인가 검증 필수. 민감 데이터는 암호화 저장. 모든 CRUD 작업에 감사로그 기록 | 행정정보통신망 보안 지침 제15조(접근통제), 제18조(암호화) |
| 내부 저장소 라이브러리만 사용 | MANDATORY | 모든 의존성은 내부 Nexus/Artifactory에서만 제공. 외부 Maven Central 의존성 금지 | 폐쇄망에서 빌드/배포 가능해야 함 |
| 테스트 통과 게이트 | MANDATORY | 모든 PR은 단위테스트 100% 통과 필수. 통합테스트 주요 시나리오 커버리지 80% 이상 | 결함 없는 결재 시스템 운영 보장 |
| TDD 접근 | RECOMMENDED | 핵심 비즈니스 로직(결재 상태 전이, 결재선 검증)은 테스트 먼저 작성 | 상태 전이 버그는 치명적 결재 오류로 이어짐 |
| SOLID 원칙 | RECOMMENDED | 단일 책임, 개방-폐쇄 원칙 준수. 특히 Service 계층은 인터페이스 기반 분리 | 유지보수성, 테스트 용이성 확보 |

---

## 2. Security Requirements

### 2.1 인증 (Authentication)
- **방식**: JWT (JSON Web Token) 기반 세션리스 인증
- **토큰 만료**: Access Token 30분, Refresh Token 8시간
- **비밀번호 정책**: 8자 이상, 영문+숫자+특수문자 조합, 90일 주기 변경
- **로그인 실패 잠금**: 5회 연속 실패 시 30분 계정 잠금
- **대체 인증**: 행정망 공동인증서(구 공인인증서) 기반 인증 지원 (선택)

### 2.2 인가 (Authorization)
- **RBAC (Role-Based Access Control)** 적용
- **역할 정의**: `SYSTEM_ADMIN`, `ORG_ADMIN`, `APPROVER`, `DRAFTER`, `VIEWER`
- **엔드포인트 수준 인가**: `@PreAuthorize` 어노테이션으로 API 단위 접근 제어
- **데이터 수준 인가**: 결재 문서는 기안자/결재자/조회권한자만 접근 가능

### 2.3 데이터 보호 (Encryption)
- **저장 데이터 암호화**: 개인정보(사번, 이름, 연락처)는 AES-256 암호화
- **전송 데이터 암호화**: 폐쇄망 내부 TLS 1.2 이상 (내부망이라도 구간 암호화)
- **DB 암호화**: Oracle TDE (Transparent Data Encryption) 활용
- **키 관리**: 내부 KMS (Key Management System)에서 키 순환 관리

### 2.4 테넌트 격리
- 단일 기관 전용 시스템이므로 테넌트 격리 불필요
- 조직별 데이터 접근은 부서 코드 기반으로 제어

### 2.5 보안 테스트
- 정적 분석 (SonarQube) — Critical/Blocker 이슈 0건
- 의존성 취약점 스캔 (OWASP Dependency-Check) — High 이상 0건
- 침투 테스트 연 1회 (행정망 보안 점검 주기 준수)

---

## 3. Compliance Standards

### 3.1 감사추적 (Audit Trail)
- **대상**: 로그인/로그아웃, 문서 생성/수정/삭제, 결재 승인/반려/회수, 결재선 변경
- **저장 정보**: 사용자 ID, 작업 일시, 작업 유형, 대상 ID, 변경 전/후 값, IP 주소
- **보존 기간**: 5년 (행정기록물 관리 기준)
- **위변조 방지**: 감사로그 테이블은 INSERT 전용, UPDATE/DELETE 권한 차단

### 3.2 개인정보보호
- 행정안전부 「개인정보 보호 지침」 준수
- 불필요한 개인정보 수집 금지 (결재 목적 최소 정보만)
- 개인정보 영향평가(PIA) 실시

### 3.3 라이선스 정책
- 모든 의존성은 Apache 2.0, MIT, BSD 등 허용 라이선스만 사용
- GPL 라이선스 라이브러리 사용 금지 (소스 공개 의무)
- 라이선스 고지서 자동 생성 및 보관

---

## 4. Performance & Scalability

### 4.1 성능 목표
| 지표 | 목표값 | 측정 방법 |
|------|--------|-----------|
| API 응답시간 (P95) | 2초 이내 | APM 측정 |
| API 응답시간 (P99) | 3초 이내 | APM 측정 |
| 동시 사용자 | 200명 | 부하 테스트 |
| 일일 결재 처리량 | 3,000건 | 로그 집계 |
| 시스템 가용성 (SLA) | 99.9% (연간 8.76시간 이하 다운) | 모니터링 |

### 4.2 확장성 요구
- 수평 확장: Stateless API 서버, 다중 인스턴스 배포 가능
- DB: Oracle RAC 또는 Data Guard 구성 (기관 규모에 따라)
- 세션: JWT 기반으로 서버 확장 시 세션 공유 불필요

### 4.3 리소스 제한
- JVM Heap: 2GB ~ 4GB (인스턴스당)
- DB Connection Pool: 최대 50 (HikariCP)
- 스레드 풀: Tomcat 기본 (200), 결재 알림용 별도 스레드 풀 (50)

---

## 5. Development Workflow

### 5.1 Git 전략
- **브랜치 모델**: GitFlow (main ← develop ← feature/*)
- **커밋 메시지**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`)
- **PR 규칙**: 최소 1인 승인 필수, CI 통과 필수

### 5.2 CI/CD 파이프라인
```
빌드 → 단위테스트 → 정적분석 → 통합테스트 → 패키지(JAR) → 내부 저장소 배포
```
- 빌드 도구: Maven (폐쇄망 내부 Nexus 미러 설정)
- CI 서버: 내부 Jenkins / GitLab Runner
- 모든 파이프라인 단계는 외부 네트워크 접근 없이 동작

### 5.3 코드 리뷰 체크리스트
- [ ] 보안 취약점 없음 (SQL Injection, XSS 등)
- [ ] 감사로그 기록 누락 없음
- [ ] 예외 처리 적절함
- [ ] 테스트 코드 포함
- [ ] API 문서 업데이트
- [ ] DB 마이그레이션 스크립트 포함

---

## 6. Governance

### 6.1 Constitution 권위
- 이 Constitution은 모든 설계/구현 문서보다 우선한다
- 위반 사항 발견 시 즉시 수정 조치

### 6.2 개정 절차
- 개정 제안 → 아키텍트 검토 → 팀 승인 → 버전 업데이트
- 주요 개정 시 변경 이력 기록

### 6.3 준수 검증 방법
- Phase 7 (Analyze)에서 Constitution 정합성 자동 검증
- 코드 리뷰 시 Constitution 체크리스트 항목 확인
- 분기별 보안 준수 점검
