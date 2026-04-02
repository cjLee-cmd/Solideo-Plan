# 코드 리뷰 종합 보고서

## 1. 리뷰 개요

| 항목 | 내용 |
|------|------|
| **프로젝트** | gov.mogaha.ntis (NTIS 신규사업 관리 모듈) |
| **리뷰 대상** | SNTFMW Meal 모듈 (EJB + Struts Action) |
| **리뷰일** | 2026-04-02 |
| **대상 파일** | 5개 Java 소스 |
| **기술 스택** | EJB 2.x, Struts 1.x, Java |
| **아키텍처** | EJB Session Bean + DAO + Struts Action |
| **점검 기준** | OWASP Top 10 (2021) + 행정망 보안 가이드라인 |

---

## 2. 종합 점수 및 판정

### 코드 품질 점수: 42 / 100

| 평가 영역 | 점수 | 비고 |
|-----------|------|------|
| 코드 가독성 | 35/100 | 네이밍 불일치, Raw Type 범용, 누락된 import |
| 설계 원칙 | 40/100 | 클래스명-기능 불일치, 중복 코드, 책임 분리 미흡 |
| 에러 처리 | 45/100 | 롤백 처리는 양호하나, NPE 처리 및 예외 메시지 부적절 |
| 로직 정확성 | 35/100 | Null DAO 참조, 빈 문자열 키, 하드코딩 한글 |
| 성능 | 60/100 | 배치 처리 사용은 양호, 불필요한 객체 생성 존재 |
| 보안 | 50/100 | 암호화 적용은 양호, 민감정보 로깅 가능성 |

### 배포 판정: 🔴 배포 불가

**사유**: Critical 수준 이슈 6건 (코드 4건 + 보안 2건) 미해결

---

## 3. 이슈 통계

### 심각도별 분포

| 심각도 | 코드 리뷰 | 보안 리뷰 | 합계 |
|--------|-----------|-----------|------|
| Critical | 4 | 2 | **6** |
| High | - | 3 | **3** |
| Major | 9 | - | **9** |
| Medium | - | 4 | **4** |
| Minor | 4 | 2 | **6** |
| **총계** | **17** | **11** | **28** |

---

## 4. Critical 이슈 (즉시 수정 필요)

### [REV-001] DAO에서 QueryService가 null 상태로 초기화되지 않음

- **출처**: 코드 리뷰 CR-01
- **파일**: `gov/mogaha/ntis/ejb/snt/fod/SntFmwMealEJBDAO.java:28`
- **설명**: `queryservice` 필드가 `null`로 선언되고 초기화되지 않음. 모든 메서드에서 NPE 발생
- **조치**: 생성자 또는 DI를 통해 QueryService 인스턴스 초기화

### [REV-002] Action에서 빈 문자열을 request attribute 키로 사용

- **출처**: 코드 리뷰 CR-02
- **파일**: `gov/mogaha/ntis/web/snt/fod/action/SntFmwMealAction.java:35,42,49`
- **설명**: `request.setAttribute("", invokeLocal(request))` — 빈 키로 인해 뷰에 데이터 전달 불가
- **조치**: 의미 있는 키 이름으로 변경 (예: `"result"`)

### [REV-003] 필수 import 문 누락

- **출처**: 코드 리뷰 CR-03, CR-04
- **파일**: `SntFmwMealAction.java:18-27`, `SntFmwMealLocal.java:8`
- **설명**: `HashMap`, `Collection`, `ArrayList`, `Log`, `NTIS_COMMON_DEFINE`, `DefaultParameters` import 누락
- **조치**: 누락된 import문 추가

### [REV-004] 인가 검증 전무 (Broken Access Control)

- **출처**: 보안 리뷰 SEC-001
- **OWASP**: A01:2021 - Broken Access Control
- **파일**: `SntFmwMealAction.java:17-51` 전 메서드
- **설명**: 모든 CRUD 액션 메서드에서 권한 검증 없이 `invokeLocal()` 호출. 인증된 사용자라면 누구나 타인의 데이터 조회/수정/삭제 가능
- **조치**: 각 액션 메서드 시작 부분에 인증 확인 + 역할(Role) 기반 인가 검증 추가

### [REV-005] SQL Injection 취약점 가능성

- **출처**: 보안 리뷰 SEC-002
- **OWASP**: A03:2021 - Injection
- **파일**: `SntFmwMealEJBDAO.java:28-29, 53, 72, 80, 98-100`
- **설명**: `QueryService.find()` / `update()`에 전달되는 파라미터가 문자열 배열로 직접 전달. `cud_data` 파싱 데이터가 사용자 입력인 경우 SQL Injection 가능
- **조치**: PreparedStatement 파라미터 바인딩 확인, `smode` 값 화이트리스트 검증 추가

---

## 5. High 이슈 (수정 권장)

### [REV-006] 개인정보 암호화 취약점

- **출처**: 보안 리뷰 SEC-003
- **OWASP**: A02:2021 - Cryptographic Failures
- **파일**: `SntFmwMealEJBDAO.java:15, 30, 49, 67`
- **설명**: 커스텀 `CCDEncryption` 사용 — 표준 알고리즘 여부 불명. 복호화된 데이터가 HashMap에 담겨 메모리 상 평문 노출. 암호화 키 관리 방식 불명
- **조치**: KISA 표준 암호화 모듈 사용, KMS에서 키 관리, 필요한 필드만 부분 복호화

### [REV-007] 감사로그 부재

- **출처**: 보안 리뷰 SEC-004
- **OWASP**: A09:2021 - Security Logging & Monitoring Failures
- **파일**: `SntFmwMealAction.java:26-27`, `SntFmwMealBean.java:35-81`
- **설명**: 에러 로깅이 `"NPE"`, `"ERR"`만 기록. CRUD 작업에 대한 감사로그(누가, 언제, 무엇을) 전혀 없음. 개인정보(SSN) 접근 이력 추적 불가 — 개인정보보호법 위반 소지
- **조치**: 감사로그 AOP 적용, 개인정보 접근로그 기록(조회자ID, 시간, 대상, 사유), 접근이력 1년 이상 보관

### [REV-008] 불안전한 비즈니스 로직 설계

- **출처**: 보안 리뷰 SEC-005
- **OWASP**: A04:2021 - Insecure Design
- **파일**: `SntFmwMealEJBDAO.java:84-103`
- **설명**: `cud_data` 문자열을 직접 파싱하여 DB 작업. 트랜잭션 경계 불명확 — 일부 성공 후 실패 시 데이터 불일치 가능
- **조치**: JSON 등 구조화된 포맷으로 변경, 작업 건수 제한, 명시적 트랜잭션 경계 설정

---

## 6. Major 이슈 (수정 권장)

### [REV-009] 클래스명과 실제 기능 불일치

- **출처**: 코드 리뷰 MJ-01
- **파일**: 전 파일
- **설명**: 클래스명 `SntFmwMeal` (식사 관련) vs 메서드/쿼리 `NewBusin` (신규사업). 도메인 혼란 초래
- **조치**: 클래스명을 실제 기능에 맞게 변경 (`SntFmwNewBusin`) 또는 메서드/쿼리명 수정

### [REV-010] Raw Type 사용 (제네릭 미사용)

- **출처**: 코드 리뷰 MJ-02, 보안 리뷰 SEC-010
- **파일**: 전 파일
- **설명**: `HashMap`, `Collection`, `ArrayList`이 raw type으로 사용. 타입 안정성 저하 및 ClassCastException 위험
- **조치**: 제네릭 적용 (`HashMap<String, Collection<?>>`)

### [REV-011] 의미 없는 리턴값 (항상 Integer(0))

- **출처**: 코드 리뷰 MJ-03
- **파일**: `SntFmwMealEJBDAO.java:54,73,81,102`
- **설명**: insert/update/delete 메서드가 항상 `new Integer(0)` 반환. 처리 결과를 알 수 없음
- **조치**: 실제 처리 결과(영향받은 행 수) 반환 또는 void로 변경

### [REV-012] 하드코딩된 한글 문자열

- **출처**: 코드 리뷰 MJ-04
- **파일**: `SntFmwMealEJBDAO.java:92`
- **설명**: `rs.get("필드명")` — 한글 문자열 하드코딩. 유지보수 및 인코딩 이슈 발생 가능
- **조치**: 상수 정의 또는 프로퍼티 파일로 분리

### [REV-013] 임시 쿼리명 사용 (XXX placeholder)

- **출처**: 코드 리뷰 MJ-05
- **파일**: `SntFmwMealEJBDAO.java:98-100`
- **설명**: `insertXXX`, `updateXXX`, `deleteXXX` — 미완성 placeholder 쿼리명
- **조치**: 실제 쿼리명으로 변경 또는 미완성 메서드 제거/주석 처리

### [REV-014] 중복된 예외 처리 패턴

- **출처**: 코드 리뷰 MJ-06
- **파일**: `SntFmwMealBean.java:35-81`
- **설명**: select/insert/update/delete 4개 메서드가 완전히 동일한 try-catch 패턴 반복. DRY 원칙 위반
- **조치**: 템플릿 메서드 패턴 또는 AOP로 공통화

### [REV-015] 부적절한 예외 로그 메시지

- **출처**: 코드 리뷰 MJ-07
- **파일**: `SntFmwMealAction.java:26-27`
- **설명**: NPE 발생 시 `"NPE"`, 기타 예외 시 `"ERR"`만 로깅. 디버깅에 무용
- **조치**: 예외 메시지와 스택 트레이스 포함

### [REV-016] Struts Action이 null 반환

- **출처**: 코드 리뷰 MJ-08
- **파일**: `SntFmwMealAction.java:29,36,43,50`
- **설명**: 모든 Action 메서드가 `return null`. Struts에서 적절한 forward를 찾지 못해 예외 발생 가능
- **조치**: 적절한 `ActionForward` 반환

### [REV-017] processException 메서드의 불필요한 래핑

- **출처**: 코드 리뷰 MJ-09
- **파일**: `SntFmwMealBean.java:87-89`
- **설명**: `processException`이 단순히 생성자 호출만 래핑. 추가 로직 없음
- **조치**: 인라인 처리 또는 로깅 등 부가 기능 추가

---

## 7. Medium 이슈 (개선 검토)

### [REV-018] 세션 관리 미흡

- **출처**: 보안 리뷰 SEC-006
- **OWASP**: A07:2021 - Authentication Failures
- **파일**: `SntFmwMealAction.java:33-49`, `SntFmwMealBean.java` 전역
- **설명**: `SSOSessionUtil.getUserID()` 사용 but 세션 유효성 검증 로직 없음. 세션 타임아웃 설정 여부 불명. 동시 세션 제한 없음
- **조치**: 세션 유효성 검증 필터 적용, 타임아웃 15분, 동시 세션 1개 제한, 로그인 시 세션 ID 재생성

### [REV-019] 입력값 검증 부재

- **출처**: 보안 리뷰 SEC-007
- **OWASP**: A05:2021 - Security Misconfiguration
- **파일**: `SntFmwMealEJBDAO.java:26-27, 39-43, 58-62, 77`
- **설명**: `StringUtil.isNullTrim()`은 null/공백 처리만 수행. 주민등록번호 형식 검증 없음. XSS 방지를 위한 HTML Escape 처리 안 함
- **조치**: 입력값 검증 추가 (길이, 형식, 특수문자), 서버 측 화이트리스트 검증

### [REV-020] CSRF 보호 미구현

- **출처**: 보안 리뷰 SEC-008
- **OWASP**: A08:2021 - Software & Data Integrity Failures
- **파일**: `SntFmwMealAction.java:32-51`
- **설명**: Struts 1.x 기반 액션에 CSRF 토큰 검증 없음. insert/update/delete가 위조 요청으로 변조 가능
- **조치**: Struts Token Processor 사용 또는 CSRF 토큰 필터 적용

### [REV-021] 개인정보 처리 lifecycle 미비

- **출처**: 보안 리뷰 SEC-009
- **OWASP**: A01 + 행정망 가이드라인
- **파일**: `SntFmwMealEJBDAO.java:42-43, 49, 61, 67`
- **설명**: 주민등록번호 수집·저장 — 개인정보보호법상 처리 제한 위반 소지. 암호화된 SSN 저장되나 파기 정책 불명. 전화번호는 암호화 없이 저장 가능성
- **조치**: CI/DI 또는 가상식별자 사용 검토, 개인정보 항목 최소화, 파기 정책 수립, 전화번호 암호화 저장

---

## 8. Minor 이슈 (경미한 개선)

### [REV-022] new Integer() 대신 Integer.valueOf() 사용 권장

- **출처**: 코드 리뷰 MN-01
- **파일**: `SntFmwMealEJBDAO.java:54,73,81,102`
- **설명**: `new Integer(0)`은 매번 새 객체 생성
- **조치**: `Integer.valueOf(0)` 또는 자동 박싱 활용

### [REV-023] SSOSessionUtil 중복 호출

- **출처**: 코드 리뷰 MN-02
- **파일**: `SntFmwMealAction.java:33-34`
- **설명**: insert/update/delete 각 메서드에서 `getUserID`, `getDeptID` 별도 호출
- **조치**: private helper 메서드로 추출

### [REV-024] EJB 2.x 레거시 아키텍처

- **출처**: 코드 리뷰 MN-03
- **파일**: 전 파일
- **설명**: EJB 2.x는 현대 Java EE에서 더 이상 사용되지 않음. 유지보수 인력 확보 어려움
- **조치**: 장기적으로 EJB 3.x 또는 Spring Framework로 마이그레이션 검토

### [REV-025] 메서드명 네이밍 컨벤션 불일치

- **출처**: 코드 리뷰 MN-04
- **파일**: 전 파일
- **설명**: `selectListSNTFMWNewBusin` vs `insertSNTFMWNewBusin01` — 일관성 없는 네이밍
- **조치**: 일관된 번호 체계 적용 또는 제거

### [REV-026] 에러 정보 노출 가능성

- **출처**: 보안 리뷰 SEC-011
- **OWASP**: A05:2021 - Security Misconfiguration
- **파일**: `SntFmwMealBean.java:87-89`, `SntFmwMealAction.java:26-27`
- **설명**: `processException`이 원래 예외를 포함하는 Exception 생성 — 스택 트레이스 클라이언트 노출 가능
- **조치**: 예외 래핑 시 스택 트레이스 제거 또는 마스킹, 글로벌 에러 핸들러 적용

---

## 9. 행정망 보안 가이드라인 준수 현황

| 항목 | 준수 여부 | 비고 |
|------|-----------|------|
| 개인정보 수집·이용 동의 관리 | ❌ 미구현 | 동의 이력 저장 로직 없음 |
| 개인정보 암호화 저장 | ⚠️ 부분 | SSN은 암호화, telno는 불명 |
| 접근통제 (RBAC) | ❌ 미구현 | 역할 기반 권한 검증 없음 |
| 감사로그 (접근/변경/삭제) | ❌ 미구현 | CRUD 작업 로깅 없음 |
| 개인정보 접근이력 관리 | ❌ 미구현 | 조회 이력 기록 없음 |
| 세션 타임아웃 | ❌ 불명 | 설정 파일 없음 |
| CSRF 보호 | ❌ 미구현 | 토큰 검증 없음 |
| 입력값 서버 검증 | ❌ 미구현 | 형식 검증 없음 |
| 데이터 전송 암호화 | ❌ 불명 | TLS 설정 파일 없음 |
| 보안패치 관리 | ❌ 불명 | EJB 2.x / Struts 1.x EOL 컴포넌트 |

---

## 10. 사용 컴포넌트 보안 현황

| 컴포넌트 | 버전 | 상태 |
|----------|------|------|
| EJB 2.x | Legacy | EOL — 알려진 취약점 다수 |
| Struts 1.x | Legacy | EOL (2013년 지원 종료) — CVE 다수 |
| RMI | JDK 내장 | 암호화 미적용 시 도청 가능 |
| CCDEncryption | Custom | 검증되지 않은 커스텀 암호화 |

---

## 11. 조치 권고 및 우선순위

### 1단계: 즉시 수정 (Critical) — 배포 전 필수

| 이슈 ID | 내용 | 예상 소요 |
|---------|------|-----------|
| REV-001 | QueryService null 초기화 | 1시간 |
| REV-002 | 빈 문자열 attribute 키 수정 | 30분 |
| REV-003 | 누락된 import 추가 | 30분 |
| REV-004 | RBAC 기반 인가 검증 구현 | 4시간 |
| REV-005 | SQL Injection 방어 (파라미터 바인딩 확인 + smode 검증) | 2시간 |

### 2단계: 수정 권장 (High) — 1스프린트 내 완료

| 이슈 ID | 내용 | 예상 소요 |
|---------|------|-----------|
| REV-006 | KISA 표준 암호화 모듈 교체 | 8시간 |
| REV-007 | CRUD 감사로그 및 개인정보 접근이력 기록 | 8시간 |
| REV-008 | 트랜잭션 경계 명확화 + cud_data 구조화 | 4시간 |

### 3단계: 개선 검토 (Major/Medium) — 다음 스프린트

| 이슈 ID | 내용 | 예상 소요 |
|---------|------|-----------|
| REV-009 | 클래스명-기능 정합성 맞추기 | 2시간 |
| REV-010 | 제네릭 타입 적용 | 4시간 |
| REV-011 | 리턴값 의미화 | 1시간 |
| REV-012 | 하드코딩 한글 상수화 | 1시간 |
| REV-013 | placeholder 쿼리 정리 | 1시간 |
| REV-014 | 중복 예외 처리 패턴 리팩토링 | 2시간 |
| REV-015 | 예외 로그 개선 | 1시간 |
| REV-016 | ActionForward 반환 | 1시간 |
| REV-017 | processException 개선 | 30분 |
| REV-018 | 세션 관리 강화 | 4시간 |
| REV-019 | 입력값 검증 구현 | 4시간 |
| REV-020 | CSRF 토큰 검증 | 2시간 |
| REV-021 | 개인정보 lifecycle 관리 | 8시간 |

### 4단계: 장기 개선 (Minor) — 기술 부채 관리

| 이슈 ID | 내용 | 예상 소요 |
|---------|------|-----------|
| REV-022 | Integer.valueOf() 변경 | 30분 |
| REV-023 | SSOSessionUtil helper 추출 | 30분 |
| REV-024 | EJB 2.x → Spring Boot 마이그레이션 검토 | 별도 계획 |
| REV-025 | 네이밍 컨벤션 통일 | 1시간 |
| REV-026 | 에러 정보 마스킹 | 1시간 |

---

## 12. 종합 평가

### 판정: 🔴 배포 불가

현재 코드베이스는 프로덕션 배포가 불가능한 수준입니다. 다음 근거에 기반합니다:

1. **컴파일 불가 상태**: import 누락, null DAO 참조로 인해 빌드 자체가 실패
2. **인가 검증 전무**: 인증된 모든 사용자가 CRUD 작업 가능 — 무단 접근/변조 위험
3. **개인정보보호법 위반 소지**: 감사로그 부재, 암호화 취약, 접근이력 미관리
4. **EOL 컴포넌트**: EJB 2.x + Struts 1.x는 보안 패치가 제공되지 않음

### 배포 가능 조건

다음 조건이 모두 충족되어야 배포 검토가 가능합니다:

- [ ] 모든 Critical 이슈 (REV-001 ~ REV-005) 해결
- [ ] 모든 High 이슈 (REV-006 ~ REV-008) 해결 또는 우회 조치 계획 수립
- [ ] RBAC 기반 접근제어 구현 완료
- [ ] 개인정보 감사로그 시스템 구축
- [ ] KISA 표준 암호화 모듈 적용
- [ ] 입력값 검증 및 CSRF 보호 구현
- [ ] 보안 재검토 통과

### 권장 전략

1. **단기**: Critical/High 이슈 수정으로 최소 보안 요구사항 충족
2. **중기**: Major/Medium 이슈 리팩토링으로 코드 품질 및 유지보수성 개선
3. **장기**: EJB 2.x + Struts 1.x → Spring Boot + Spring MVC 마이그레이션 추진

---

*보고서 작성일: 2026-04-02*
*리뷰 기준: OWASP Top 10 (2021) + 행정망 보안 가이드라인*
