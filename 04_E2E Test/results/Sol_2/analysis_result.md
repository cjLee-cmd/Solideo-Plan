# 코드 분석 결과 (Analysis Result)

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 프로젝트명 | NTIS (국가과학기술정보시스템) - SNTFMW 식사관리 모듈 |
| 소유 기관 | 행정안전부 (MOGAHA - Ministry of Government Administration and Home Affairs) |
| 프로젝트 경로 | `/private/tmp/e2e_sol2` |
| 분석 대상 파일 수 | 5개 (Java) |
| 분석 일시 | 2026-04-02 |

---

## 2. 기술스택 식별

### 2.1 프로그래밍 언어

| 언어 | 버전 추정 | 근거 |
|------|-----------|------|
| Java | 1.4 ~ 5.0 | `Integer` 래퍼 클래스 사용, 제네릭 미사용, raw type 컬렉션 |

### 2.2 프레임워크 및 라이브러리

| 프레임워크/라이브러리 | 용도 | 근거 (import 문) |
|----------------------|------|-----------------|
| Apache Struts 1.x | Web MVC 프레임워크 | `javax.servlet.http.HttpServletRequest`, `org.apache.struts.action.ActionMapping` |
| EJB 2.x (Session Bean) | 비즈니스 로직 계층 | `javax.ejb.SessionBean`, `javax.ejb.EJBLocalObject`, `javax.ejb.EJBObject` |
| Java Servlet API | HTTP 요청/응답 처리 | `javax.servlet.http.HttpServletRequest`, `HttpServletResponse` |

### 2.3 빌드 도구

- **식별되지 않음**: `pom.xml`, `build.gradle`, `Ant build.xml` 등 빌드 설정 파일이 프로젝트에 포함되지 않음
- `.xrw` 파일(SNTFMWNewBusinPrnP.xrw) 존재: XML 문서이나 바이너리 형식으로 내용 확인 불가

### 2.4 데이터베이스

- **직접 식별 불가**: `QueryService`를 통한 간접 DB 접근 패턴 사용
- SQL은 외부 XML 매핑 파일에서 관리되는 것으로 추정 (`SntFmwMealEJBDAO.selectListSNTFMWNewBusin01` 등 쿼리 ID 패턴)

### 2.5 미들웨어

| 미들웨어 | 추정 근거 |
|----------|----------|
| EJB 컨테이너 (JBoss/WebLogic/WebSphere 등) | EJB 2.x Session Bean 패턴 사용 |
| Apache Tomcat 또는 WAS 내장 서블릿 컨테이너 | Struts Action 기반 웹 계층 |

---

## 3. 디렉토리 구조 매핑

### 3.1 디렉토리 트리

```
e2e_sol2/
├── .git/                          # Git 저장소
├── 90_Result_Doc/                 # 분석 결과 저장 디렉토리 (비어있음)
├── SNTFMWNewBusinPrnP.xrw         # XML 문서 파일 (바이너리/암호화 형식)
└── gov/
    └── mogaha/
        └── ntis/
            ├── web/
            │   └── snt/
            │       ├── common/    # 공통 유틸리티 클래스 (미포함, 참조만 됨)
            │       └── fod/
            │           └── action/
            │               └── SntFmwMealAction.java      # 웹 계층 (Struts Action)
            └── ejb/
                └── snt/
                    └── fod/
                        ├── SntFmwMeal.java                # EJB Remote 인터페이스
                        ├── SntFmwMealLocal.java           # EJB Local 인터페이스
                        ├── SntFmwMealBean.java            # EJB Session Bean 구현
                        └── SntFmwMealEJBDAO.java          # 데이터 접근 객체
```

### 3.2 디렉토리별 역할

| 디렉토리 | 역할 |
|----------|------|
| `gov/mogaha/ntis/web/` | 프레젠테이션 계층 (Struts Action, 공통 유틸리티) |
| `gov/mogaha/ntis/ejb/` | 비즈니스 계층 (EJB Session Bean, DAO) |
| `gov/mogaha/ntis/web/snt/common/` | 공통 클래스 (DefaultParameters, QueryService, StringUtil, SSOSessionUtil 등) |
| `gov/mogaha/ntis/web/snt/fod/action/` | FOD(Food) 도메인 Action 클래스 |
| `gov/mogaha/ntis/ejb/snt/fod/` | FOD 도메인 EJB 및 DAO |

### 3.3 주요 파일 목록

| 파일 | 경로 | 역할 |
|------|------|------|
| SntFmwMealAction.java | `web/snt/fod/action/` | Struts Action - HTTP 요청 처리 |
| SntFmwMeal.java | `ejb/snt/fod/` | EJB Remote 인터페이스 (RMI) |
| SntFmwMealLocal.java | `ejb/snt/fod/` | EJB Local 인터페이스 |
| SntFmwMealBean.java | `ejb/snt/fod/` | Session Bean 구현체 - 비즈니스 로직 |
| SntFmwMealEJBDAO.java | `ejb/snt/fod/` | 데이터 접근 객체 - 쿼리 실행 |

---

## 4. 모듈 의존성 분석

### 4.1 내부 모듈 간 의존 관계

```
SntFmwMealAction (Web/Action)
    ├── SntAction (공통 Action 부모 클래스)
    ├── SSOSessionUtil (SSO 세션 유틸리티)
    ├── DefaultParameters (파라미터 DTO)
    ├── SntFmwMeal (EJB Remote 인터페이스)
    └── invokeLocal() → EJB Local 호출

SntFmwMealBean (EJB Session Bean)
    ├── SntFmwMealEJBDAO (DAO 위임)
    ├── DefaultEJBException (공통 예외)
    ├── SDBException (DB 예외)
    ├── SSOSessionUtil (SSO 세션)
    └── SessionContext (EJB 컨텍스트)

SntFmwMealEJBDAO (DAO)
    ├── QueryService (쿼리 실행 서비스)
    ├── CCDEncryption (암호화 유틸리티)
    ├── StringUtil (문자열 유틸리티)
    ├── SaveResultSet (저장 결과셋)
    ├── Tokenizer (파싱 유틸리티)
    └── DefaultParameters (파라미터 DTO)
```

### 4.2 계층 간 호출 흐름

```
HTTP Request
    → SntFmwMealAction (Struts Action)
        → invokeLocal() → EJB Local Interface
            → SntFmwMealBean (Session Bean)
                → SntFmwMealEJBDAO (DAO)
                    → QueryService.find/update (SQL 실행)
```

### 4.3 외부 라이브러리 의존성

| 라이브러리 | 패키지 | 폐쇄망 호환 |
|-----------|--------|------------|
| Apache Struts | `org.apache.struts.*` | ⚠️ 외부 의존 (JAR 필요) |
| Java Servlet API | `javax.servlet.*` | ✅ WAS 제공 |
| EJB API | `javax.ejb.*` | ✅ WAS 제공 |
| RMI | `java.rmi.*` | ✅ JDK 표준 |

### 4.4 순환 의존성

- **식별되지 않음**: 단방향 의존성 구조 (Action → EJB → DAO)

### 4.5 참조되지만 분석 대상에 없는 파일

| 클래스 | 추정 위치 | 용도 |
|--------|----------|------|
| SntAction | `web/snt/common/` | Action 공통 부모 클래스 |
| SSOSessionUtil | `web/snt/common/` | SSO 세션 정보 조회 |
| DefaultParameters | `web/snt/common/` | 요청 파라미터 DTO |
| QueryService | `web/snt/common/` | SQL 쿼리 실행 서비스 |
| StringUtil | `web/snt/common/` | 문자열 처리 유틸리티 |
| CCDEncryption | `web/snt/common/` | 암호화/복호화 유틸리티 |
| SaveResultSet | `web/snt/common/` | CUD 결과셋 파싱 |
| Tokenizer | `web/snt/common/` | 문자열 토큰 분할 |
| DefaultEJBException | `web/snt/common/` | EJB 공통 예외 |
| SDBException | `web/snt/common/` | DB 접근 예외 |
| NTIS_COMMON_DEFINE | `web/snt/common/` | 공통 상수 정의 |
| Log | 외부 라이브러리 | 로깅 유틸리티 |

---

## 5. 코드 메트릭스

### 5.1 파일 및 라인 수

| 파일 | 라인 수 | 역할 |
|------|---------|------|
| SntFmwMealEJBDAO.java | 104 | DAO (가장 복잡) |
| SntFmwMealBean.java | 90 | Session Bean |
| SntFmwMealAction.java | 52 | Struts Action |
| SntFmwMeal.java | 13 | EJB Remote 인터페이스 |
| SntFmwMealLocal.java | 12 | EJB Local 인터페이스 |
| **합계** | **271** | |

### 5.2 언어별 비율

| 언어 | 파일 수 | 비율 |
|------|---------|------|
| Java | 5 | 100% |

### 5.3 복잡도 분석

| 파일 | 복잡도 | 근거 |
|------|--------|------|
| SntFmwMealEJBDAO.java | **높음** | 5개 비즈니스 메서드, 암호화/복호화 로직, SaveResultSet 파싱, 배치 업데이트 |
| SntFmwMealBean.java | **중간** | 4개 비즈니스 메서드, 트랜잭션 롤백 처리, 예외 변환 |
| SntFmwMealAction.java | **낮음** | 4개 Action 메서드, 단순 EJB 호출 및 request 설정 |
| SntFmwMeal.java | **매우 낮음** | 인터페이스 정의만 |
| SntFmwMealLocal.java | **매우 낮음** | 인터페이스 정의만 |

---

## 6. 비즈니스 기능 분석

### 6.1 도메인: 식사관리 (Meal / Food Domain)

| 기능 | 메서드 | 설명 |
|------|--------|------|
| 신규사업 목록 조회 | selectListSNTFMWNewBusin | `mw_take_no` 기준 사업 신청 목록 조회 |
| 신규사업 등록 | insertSNTFMWNewBusin01 | 사업 유형, 신청 건수, 주민번호(암호화), 전화번호 저장 |
| 신규사업 수정 | updateSNTFMWNewBusin01 | 기존 사업 정보 업데이트 |
| 신규사업 삭제 | deleteSNTFMWNewBusin01 | `mw_take_no` 기준 삭제 |
| 상세 정보 CUD | insertSNTFMWNewMealDetailIP01 | 일괄 등록/수정/삭제 (CUD 패턴) |

### 6.2 보안 관련

| 항목 | 내용 |
|------|------|
| 주민번호 암호화 | `CCDEncryption.sntEncrypt()` 사용 |
| 조회 시 복호화 | `CCDEncryption.sntDecryptCol()` 사용 |
| SSO 연동 | `SSOSessionUtil.getUserID()`, `getDeptID()` |
| 트랜잭션 관리 | EJB 컨테이너 관리 트랜잭션 (예외 시 롤백) |

---

## 7. 폐쇄망 호환성 점검

### 7.1 외부 네트워크 호출

| 점검 항목 | 결과 |
|----------|------|
| HTTP 외부 호출 코드 | ❌ 식별되지 않음 |
| REST API 호출 | ❌ 식별되지 않음 |
| 외부 CDN 의존 | ❌ 식별되지 않음 |
| 웹소켓/Socket 통신 | ❌ 식별되지 않음 |

### 7.2 외부 의존성

| 의존성 | 폐쇄망 대응 방안 |
|--------|-----------------|
| Apache Struts 1.x | JAR 파일 내부 저장소 등록 필요 |
| EJB Container (WAS) | WAS 설치본 내부 배포 |
| Java 표준 라이브러리 | JDK 내부 배포로 해결 |
| Log 라이브러리 | JAR 파일 내부 저장소 등록 필요 |

### 7.3 라이선스 확인 필요 항목

| 라이브러리 | 라이선스 | 확인 필요 |
|-----------|---------|----------|
| Apache Struts | Apache License 2.0 | ✅ 라이선스 고지 필요 |
| Java Servlet API | CDDL/GPL | ✅ WAS 라이선스 확인 |
| EJB API | CDDL | ✅ WAS 라이선스 확인 |

### 7.4 폐쇄망 호환성 종합 평가

| 평가 항목 | 등급 | 비고 |
|----------|------|------|
| 외부 네트워크 호출 | ✅ 양호 | 없음 |
| 외부 API 의존 | ✅ 양호 | 없음 |
| 서드파티 라이브러리 | ⚠️ 주의 | Struts JAR 내부 보관 필요 |
| 빌드 재현성 | ⚠️ 주의 | 빌드 설정 파일 미포함 |

---

## 8. 코드 이슈 및 개선 포인트

### 8.1 잠재적 버그

| 위치 | 이슈 | 심각도 |
|------|------|--------|
| SntFmwMealAction.java:35 | `request.setAttribute("", ...)` - 빈 키 사용 | 높음 |
| SntFmwMealAction.java:42 | 동일 이슈 - update 메서드 | 높음 |
| SntFmwMealAction.java:49 | 동일 이슈 - delete 메서드 | 높음 |
| SntFmwMealAction.java:18-21 | `HashMap`, `Collection`, `ArrayList` raw type 사용 | 중간 |
| SntFmwMealEJBDAO.java:92 | 하드코딩된 `"필드명"` 문자열 | 중간 |

### 8.2 코드 스타일

| 이슈 | 설명 |
|------|------|
| 제네릭 미사용 | Java 1.4 스타일 raw type 컬렉션 |
| 예외 처리 | `NullPointerException`을 별도 catch - 일반 `Exception`으로 통합 가능 |
| 매직 넘버 | `new Integer(0)` 반환 - 의미 있는 상태 코드 사용 권장 |

---

## 9. 결론

본 프로젝트는 **행정안전부 NTIS 시스템의 식사관리(Food) 모듈**로, **EJB 2.x + Struts 1.x** 기반의 전형적인 Java EE 레거시 아키텍처를 따른다.

- **총 5개 Java 파일**, **271 라인**의 소스코드로 구성
- **3-tier 구조** (Action → Session Bean → DAO) 명확히 분리
- **주민번호 암호화** 등 보안 고려사항 포함
- **폐쇄망 배포 시** Struts JAR 및 빌드 설정 파일 보완 필요
- **분석 대상에 포함되지 않은 공통 클래스** 10여 개가 참조되어 있음 (전체 분석 시 추가 필요)
