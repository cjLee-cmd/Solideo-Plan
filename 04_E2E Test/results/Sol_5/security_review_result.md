# 보안 취약점 점검 보고서

**프로젝트**: gov.mogaha.ntis (NTIS 신규사업 관리 모듈)
**점검일**: 2026-04-02
**점검 기준**: OWASP Top 10 (2021) + 행정망 보안 가이드라인
**대상 파일**: 5개 Java 소스
**판정**: 🔴 배포 금지 — critical/high 취약점 존재

---

## 1. 점검 요약

| 심각도 | 건수 | 주요 분류 |
|--------|------|-----------|
| critical | 2 | A01 접근제어, A03 주입공격 |
| high | 3 | A02 암호화, A09 로깅, A04 설계 |
| medium | 4 | A07 세션, A05 구성, 입력검증 |
| low | 2 | A08 역직렬화, 정보노출 |

---

## 2. 상세 취약점 목록

### [SEC-001] critical — 인가 검증 전무 (A01: Broken Access Control)

**위치**: `SntFmwMealAction.java:17-51` 전 메서드

**위험 시나리오**:
- `selectListSNTFMWNewBusin`, `insertSNTFMWNewBusin01`, `updateSNTFMWNewBusin01`, `deleteSNTFMWNewBusin01` 모든 액션 메서드에서 `invokeLocal(request)`를 호출하기 전 아무런 권한 검증이 없음
- 인증된 사용자라면 누구나 타인의 데이터 조회/수정/삭제 가능
- 역할(Role) 기반 접근제어가 전혀 구현되어 있지 않음

**수정 가이드**:
```java
// 각 액션 메서드 시작 부분에 권한 검증 추가
public ActionForward insertSNTFMWNewBusin01(...) throws Exception {
    // 1. 인증 확인
    String userId = SSOSessionUtil.getUserID(request);
    if (userId == null) {
        return mapping.findForward("login");
    }
    // 2. 인가 확인 (역할 기반)
    if (!hasPermission(userId, "NTIS_NEWBUSIN_WRITE")) {
        response.sendError(HttpServletResponse.SC_FORBIDDEN);
        return null;
    }
    // 3. 데이터 소유권 확인 (자신 데이터만 수정/삭제)
    ...
}
```

---

### [SEC-002] critical — SQL Injection 취약점 가능성 (A03: Injection)

**위치**: `SntFmwMealEJBDAO.java:28-29, 53, 72, 80, 98-100`

**위험 시나리오**:
- `QueryService.find()` / `update()` / `batchUpdate()`에 전달되는 파라미터가 `new String[]{mw_take_no}` 형태로 직접 전달됨
- `cud_data` 파라미터가 `Tokenizer.getSaveResultSet()`에서 `^`, `|` 구분자로 파싱되는데, 이 데이터가 사용자 입력인 경우 SQL Injection 가능
- Named Query를 사용하지만, 파라미터 바인딩 방식이 아닌 문자열 배열 전달 방식이라 쿼리 내부에서 문자열 연결이 발생할 경우 Injection 취약

**수정 가이드**:
- `QueryService` 구현부에서 PreparedStatement 파라미터 바인딩을 사용하는지 확인
- `cud_data` 파싱 결과에 대해 화이트리스트 검증 추가
```java
// smode 값 검증 강화
String smode = rs.get("smode");
if (!Arrays.asList("i", "u", "d").contains(smode)) {
    throw new SecurityException("Invalid smode value: " + smode);
}
```

---

### [SEC-003] high — 개인정보 암호화 취약점 (A02: Cryptographic Failures)

**위치**: `SntFmwMealEJBDAO.java:15, 30, 49, 67`

**위험 시나리오**:
- `CCDEncryption`이라는 커스텀 암호화 클래스 사용 — 표준 알고리즘(AES-256-GCM) 사용 여부 불명
- 주민등록번호(ssn_no) 암호화는 insert/update 시 적용되나, 조회 시 `sntDecryptCol()`로 복호화하여 컬렉션 전체에 적용 (라인 30)
- 복호화된 데이터가 HashMap에 담겨 Action 계층까지 전달 — 메모리 상에 평문으로 노출
- 암호화 키 관리 방식 불명 (하드코딩 가능성)

**수정 가이드**:
- KISA 표준 암호화 모듈(KISA 암호화 라이브러리) 사용
- 암호화 키는 KMS(Key Management System)에서 관리
- 조회 시 필요한 필드만 부분 복호화, 불필요 시 암호화 상태 유지
- 전송 구간 암호화(TLS 1.2+) 필수 적용

---

### [SEC-004] high — 감사로그 부재 (A09: Security Logging & Monitoring Failures)

**위치**: `SntFmwMealAction.java:26-27`, `SntFmwMealBean.java:35-81`

**위험 시나리오**:
- Action 계층의 에러 로깅이 `"NPE"`, `"ERR"`라는 의미 없는 메시지만 기록 (라인 26-27)
- Bean 계층에서 예외 발생 시 에러 코드만 전달, 실제 예외 컨텍스트 로깅 안 함
- CRUD 작업에 대한 감사로그(누가, 언제, 무엇을) 전혀 기록되지 않음
- 개인정보(SSN) 접근/조회 이력 추적 불가 — 개인정보보호법 위반 소지

**수정 가이드**:
```java
// 감사로그 AOP 또는 인터셉터 적용
@AuditLog(action = "INSERT", target = "SNTFMWNewBusin")
public Integer insertSNTFMWNewBusin01(DefaultParameters param) {
    auditLogger.info("User {} inserted record mw_take_no={}", 
        SSOSessionUtil.getUserID(), param.getParameter("mw_take_no"));
    ...
}
```
- 개인정보 접근로그: 조회자ID, 조회시간, 조회대상, 조회사유 기록
- 개인정보보호법 제35조(열람요구) 대응을 위한 접근이력 1년 이상 보관

---

### [SEC-005] high — 불안전한 비즈니스 로직 설계 (A04: Insecure Design)

**위치**: `SntFmwMealEJBDAO.java:84-103`

**위험 시나리오**:
- `insertSNTFMWNewMealDetailIP01` 메서드에서 `cud_data` 파라미터를 파싱하여 일괄 CUD(Create/Update/Delete) 처리
- 사용자가 전송한 문자열 데이터(`^`, `|` 구분)를 직접 파싱하여 DB 작업 수행
- 트랜잭션 경계가 불명확 — 일부 insert 성공 후 update 실패 시 데이터 불일치 가능
- 대량 삭제 시 롤백 메커니즘 미비

**수정 가이드**:
- `cud_data` 형식을 JSON 등 구조화된 포맷으로 변경
- 서버 측에서 작업 건수 제한 (예: 최대 100건)
- 명시적 트랜잭션 경계 설정
```java
UserTransaction ut = ...;
try {
    ut.begin();
    // batch operations
    ut.commit();
} catch (Exception e) {
    ut.rollback();
    throw e;
}
```

---

### [SEC-006] medium — 세션 관리 미흡 (A07: Authentication Failures)

**위치**: `SntFmwMealAction.java:33-49`, `SntFmwMealBean.java` 전역

**위험 시나리오**:
- `SSOSessionUtil.getUserID(request)`로 사용자 ID를 가져오지만, 세션 유효성 검증 로직이 Action에 명시되지 않음
- 세션 타임아웃 설정 여부 불명
- 동시 세션 제한 없음 — 동일 계정 다중 로그인 가능
- 세션 고정 공격(Session Fixation) 대비책 불명

**수정 가이드**:
- 모든 Action 진입점에서 세션 유효성 검증 필터 적용
- 세션 타임아웃: 15분 (행정망 기준)
- 동시 세션 제한: 1개
- 로그인 시 세션 ID 재생성

---

### [SEC-007] medium — 입력값 검증 부재 (A05: Security Misconfiguration)

**위치**: `SntFmwMealEJBDAO.java:26-27, 39-43, 58-62, 77`

**위험 시나리오**:
- `StringUtil.isNullTrim()`은 null/공백 처리만 수행, 실제 입력값 검증(길이, 형식, 특수문자) 미수행
- `ssn_no` (주민등록번호) 형식 검증 없이 바로 암호화 시도
- `telno` (전화번호) 형식 검증 없음
- XSS 방지를 위한 HTML Escape 처리 안 함 (JSP 렌더링 시 취약)

**수정 가이드**:
```java
// 입력값 검증 추가
public Integer insertSNTFMWNewBusin01(DefaultParameters param) throws Exception {
    String ssn_no = param.getParameter("ssn_no");
    if (!ssn_no.matches("\\d{6}-?\\d{7}")) {
        throw new ValidationException("Invalid SSN format");
    }
    
    String telno = param.getParameterNoTrim("telno");
    if (telno.length() > 15) {
        throw new ValidationException("Telephone number too long");
    }
    ...
}
```

---

### [SEC-008] medium — CSRF 보호 미구현 (A08: Software & Data Integrity Failures)

**위치**: `SntFmwMealAction.java:32-51`

**위험 시나리오**:
- Struts 1.x 기반 액션에 CSRF 토큰 검증이 없음
- insert/update/delete 작업이 GET/POST 구분 없이 처리될 수 있음
- 악성 사이트에서 위조 요청으로 데이터 변조 가능

**수정 가이드**:
- Struts Token Processor 사용 또는 CSRF 토큰 필터 적용
```java
// Struts Action에서 토큰 검증
if (!isTokenValid(request)) {
    saveToken(request);
    return mapping.findForward("error");
}
```

---

### [SEC-009] medium — 개인정보 처리 lifecycle 미비 (A01 + 행정망)

**위치**: `SntFmwMealEJBDAO.java:42-43, 49, 61, 67`

**위험 시나리오**:
- 주민등록번호(ssn_no) 수집·저장 — 개인정보보호법상 주민등록번호 처리 제한 위반 소지
- 암호화된 SSN이 DB에 저장되나, 파기 정책/절차 불명
- 전화번호(telno)는 암호화 없이 저장 가능성 (`getParameterNoTrim`으로 직접 전달)

**수정 가이드**:
- 주민등록번호 대신 CI/DI 또는 가상식별자 사용 검토
- 수집하는 개인정보 항목 최소화 (Privacy by Design)
- 개인정보 파기 정책 수립 및 자동 파기 구현
- 전화번호도 암호화 저장 적용

---

### [SEC-010] low — Raw 타입 사용으로 인한 타입 안전성 문제 (A08)

**위치**: `SntFmwMeal.java:9-12`, `SntFmwMealAction.java:20-25`

**위험 시나리오**:
- `HashMap`, `Collection`, `ArrayList` 등 Raw 타입 사용 — 타입 캐스팅 시 ClassCastException 가능
- Action에서 `(ArrayList) res1` 캐스팅 시 NPE 처리가 try-catch로 우회됨 (라인 23-27)
- 역직렬화 공격 가능성 (EJB RMI 통신)

**수정 가이드**:
- 제네릭 타입 적용: `HashMap<String, Collection<DTO>>`
- RMI 통신 구간 암호화 및 인증 적용

---

### [SEC-011] low — 에러 정보 노출 가능성 (A05)

**위치**: `SntFmwMealBean.java:87-89`, `SntFmwMealAction.java:26-27`

**위험 시나리오**:
- `processException`이 원래 예외(ex)를 포함하는 `DefaultEJBException`을 생성 — 스택 트레이스가 클라이언트에 노출될 수 있음
- Action에서 `return null`로 응답 — Struts 설정에 따라 에러 페이지가 기본 스택 트레이스를 보여줄 수 있음

**수정 가이드**:
- 예외 래핑 시 스택 트레이스 제거 또는 마스킹
- 글로벌 에러 핸들러에서 사용자 친화적 에러 페이지 포워딩

---

## 3. 행정망 보안 가이드라인 준수 여부

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

## 4. 사용 컴포넌트 보안 현황

| 컴포넌트 | 버전 | 상태 |
|----------|------|------|
| EJB 2.x | Legacy | EOL — 알려진 취약점 다수 |
| Struts 1.x | Legacy | EOL (2013년 지원 종료) — CVE 다수 |
| RMI | JDK 내장 | 암호화 미적용 시 도청 가능 |
| CCDEncryption | Custom | 검증되지 않은 커스텀 암호화 |

---

## 5. 종합 판정

### 🔴 배포 금지

**사유**:
1. **critical 수준 2건** — 인가 검증 전무로 무단 데이터 접근/변조 가능
2. **high 수준 3건** — 개인정보 암호화 취약, 감사로그 부재로 개인정보보호법 위반 소지
3. **EJB 2.x + Struts 1.x** — EOL 컴포넌트로 알려진 취약점 패치 불가

**배포 전 필수 조치 사항**:
1. [SEC-001] 전 액션에 RBAC 기반 인가 검증 구현
2. [SEC-003] KISA 표준 암호화 모듈로 교체, 키 관리 체계 구축
3. [SEC-004] CRUD 작업 감사로그 및 개인정보 접근이력 기록 구현
4. [SEC-007] 입력값 검증 (형식, 길이, 특수문자) 서버 측 구현
5. [SEC-008] CSRF 토큰 검증 구현
6. EJB 2.x → Spring Boot 등 현대적 프레임워크 마이그레이션 검토
7. Struts 1.x → Spring MVC 등 현대적 프레임워크 마이그레이션 검토
