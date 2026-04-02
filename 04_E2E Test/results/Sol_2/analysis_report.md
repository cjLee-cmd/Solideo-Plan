# NTIS 식사관리(SNTFMW) 모듈 분석 보고서

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 프로젝트명 | NTIS (국가과학기술정보시스템) - SNTFMW 식사관리 모듈 |
| 소유 기관 | 행정안전부 (MOGAHA) |
| 분석일 | 2026-04-02 |
| 분석 대상 | 5개 Java 파일 (271 라인) |

**한 줄 요약**
행정안전부 NTIS 시스템의 식사관리 모듈로, EJB 2.x + Struts 1.x 기반의 전형적인 Java EE 레거시 3-tier 아키텍처를 따른다.

---

## 2. 기술스택

| 구분 | 항목 | 버전 추정 | 비고 |
|------|------|-----------|------|
| 언어 | Java | 1.4 ~ 5.0 | 제네릭 미사용, raw type 컬렉션 |
| 웹 프레임워크 | Apache Struts | 1.x | Action 기반 MVC |
| 비즈니스 계층 | EJB (Session Bean) | 2.x | Remote/Local 인터페이스 분리 |
| 서블릿 API | Java Servlet | 2.x | WAS 제공 |
| 빌드 도구 | - | - | 빌드 설정 파일 미포함 |
| 데이터베이스 | - | - | QueryService 간접 접근 |
| 미들웨어 | EJB 컨테이너 | - | JBoss/WebLogic/WebSphere 추정 |

---

## 3. 디렉토리 구조

```
e2e_sol2/
├── .git/                          # Git 저장소
├── 90_Result_Doc/                 # 분석 결과 저장 디렉토리
├── SNTFMWNewBusinPrnP.xrw         # XML 문서 파일 (바이너리 형식)
└── gov/
    └── mogaha/
        └── ntis/
            ├── web/               # 프레젠테이션 계층
            │   └── snt/
            │       ├── common/    # 공통 유틸리티 (참조만 됨)
            │       └── fod/
            │           └── action/
            │               └── SntFmwMealAction.java
            └── ejb/               # 비즈니스 계층
                └── snt/
                    └── fod/
                        ├── SntFmwMeal.java           # EJB Remote 인터페이스
                        ├── SntFmwMealLocal.java      # EJB Local 인터페이스
                        ├── SntFmwMealBean.java       # Session Bean 구현
                        └── SntFmwMealEJBDAO.java     # 데이터 접근 객체
```

| 디렉토리 | 역할 |
|----------|------|
| `web/snt/fod/action/` | Struts Action - HTTP 요청 처리 |
| `ejb/snt/fod/` | EJB Session Bean 및 DAO - 비즈니스 로직, 데이터 접근 |
| `web/snt/common/` | 공통 클래스 (DefaultParameters, QueryService, StringUtil 등) |

---

## 4. 아키텍처 분석

### 4.1 계층 구조

```
HTTP Request
    → SntFmwMealAction (Struts Action)
        → invokeLocal() → EJB Local Interface
            → SntFmwMealBean (Session Bean)
                → SntFmwMealEJBDAO (DAO)
                    → QueryService.find/update (SQL 실행)
```

### 4.2 주요 모듈 역할

| 모듈 | 계층 | 역할 |
|------|------|------|
| SntFmwMealAction | 웹 (프레젠테이션) | HTTP 요청 수신, EJB 호출, 결과 request 설정 |
| SntFmwMeal / SntFmwMealLocal | 인터페이스 | EJB Remote/Local 계약 정의 |
| SntFmwMealBean | 비즈니스 (EJB) | 트랜잭션 관리, 비즈니스 로직, 예외 처리 |
| SntFmwMealEJBDAO | 데이터 접근 | SQL 쿼리 실행, 암호화/복호화, 결과셋 파싱 |

### 4.3 데이터 흐름

- **조회**: Action → EJB Bean → DAO → QueryService.find → ResultSet 매핑 → Action → JSP
- **등록/수정/삭제**: Action → EJB Bean → DAO → QueryService.update → 트랜잭션 커밋/롤백

---

## 5. 의존성 분석

### 5.1 내부 모듈 관계

```
SntFmwMealAction
    ├── SntAction (공통 부모)
    ├── SSOSessionUtil (SSO 세션)
    ├── DefaultParameters (파라미터 DTO)
    └── SntFmwMeal (EJB Local 호출)

SntFmwMealBean
    ├── SntFmwMealEJBDAO (DAO 위임)
    ├── DefaultEJBException / SDBException (예외)
    └── SSOSessionUtil (세션 정보)

SntFmwMealEJBDAO
    ├── QueryService (쿼리 실행)
    ├── CCDEncryption (암호화)
    ├── StringUtil / Tokenizer / SaveResultSet (유틸리티)
    └── DefaultParameters (DTO)
```

### 5.2 외부 라이브러리

| 패키지명 | 버전 | 용도 | 라이선스 | 폐쇄망 호환 |
|----------|------|------|----------|-------------|
| org.apache.struts.* | 1.x | Web MVC | Apache 2.0 | ⚠️ JAR 내부 보관 필요 |
| javax.servlet.* | 2.x | HTTP 처리 | CDDL/GPL | ✅ WAS 제공 |
| javax.ejb.* | 2.x | EJB API | CDDL | ✅ WAS 제공 |
| java.rmi.* | JDK 표준 | RMI 통신 | Oracle BCL | ✅ JDK 포함 |
| Log 라이브러리 | - | 로깅 | - | ⚠️ JAR 내부 보관 필요 |

### 5.3 순환 의존성

- **없음**: 단방향 의존성 구조 (Action → EJB → DAO) 유지

### 5.4 참조되나 미포함 파일

| 클래스 | 용도 |
|--------|------|
| SntAction | Action 공통 부모 클래스 |
| SSOSessionUtil | SSO 세션 정보 조회 |
| DefaultParameters | 요청 파라미터 DTO |
| QueryService | SQL 쿼리 실행 서비스 |
| StringUtil | 문자열 처리 유틸리티 |
| CCDEncryption | 암호화/복호화 유틸리티 |
| SaveResultSet | CUD 결과셋 파싱 |
| Tokenizer | 문자열 토큰 분할 |
| DefaultEJBException | EJB 공통 예외 |
| SDBException | DB 접근 예외 |
| NTIS_COMMON_DEFINE | 공통 상수 정의 |

---

## 6. 코드 메트릭스

### 6.1 파일 및 라인 수

| 파일 | 라인 수 | 역할 |
|------|---------|------|
| SntFmwMealEJBDAO.java | 104 | DAO (가장 복잡) |
| SntFmwMealBean.java | 90 | Session Bean |
| SntFmwMealAction.java | 52 | Struts Action |
| SntFmwMeal.java | 13 | EJB Remote 인터페이스 |
| SntFmwMealLocal.java | 12 | EJB Local 인터페이스 |
| **합계** | **271** | |

### 6.2 언어별 비율

| 언어 | 파일 수 | 비율 |
|------|---------|------|
| Java | 5 | 100% |

### 6.3 복잡도 상위 파일

| 파일 | 복잡도 | 근거 |
|------|--------|------|
| SntFmwMealEJBDAO.java | 높음 | 5개 비즈니스 메서드, 암호화/복호화, SaveResultSet 파싱, 배치 업데이트 |
| SntFmwMealBean.java | 중간 | 4개 비즈니스 메서드, 트랜잭션 롤백, 예외 변환 |
| SntFmwMealAction.java | 낮음 | 4개 Action 메서드, 단순 EJB 호출 |

---

## 7. 폐쇄망 호환성 점검

### 7.1 외부 네트워크 호출 점검

| 점검 항목 | 결과 |
|----------|------|
| HTTP 외부 호출 | ❌ 없음 |
| REST API 호출 | ❌ 없음 |
| 외부 CDN 의존 | ❌ 없음 |
| 웹소켓/Socket 통신 | ❌ 없음 |

### 7.2 외부 의존성 조치 필요 사항

| 의존성 | 조치 방안 |
|--------|----------|
| Apache Struts 1.x | JAR 파일 내부 저장소 등록 |
| Log 라이브러리 | JAR 파일 내부 저장소 등록 |
| EJB Container (WAS) | WAS 설치본 내부 배포 |
| 빌드 설정 파일 | pom.xml 또는 build.xml 복구 필요 |

### 7.3 라이선스 확인 필요

| 라이브러리 | 라이선스 | 확인 사항 |
|-----------|---------|----------|
| Apache Struts | Apache License 2.0 | 라이선스 고지 필요 |
| Java Servlet API | CDDL/GPL | WAS 라이선스 확인 |
| EJB API | CDDL | WAS 라이선스 확인 |

### 7.4 폐쇄망 호환성 종합 평가

| 평가 항목 | 등급 | 비고 |
|----------|------|------|
| 외부 네트워크 호출 | ✅ 양호 | 외부 호출 없음 |
| 외부 API 의존 | ✅ 양호 | 외부 API 없음 |
| 서드파티 라이브러리 | ⚠️ 주의 | Struts JAR 내부 보관 필요 |
| 빌드 재현성 | ⚠️ 주의 | 빌드 설정 파일 미포함 |

---

## 8. 개선 제안

### 8.1 잠재적 버그

| 위치 | 이슈 | 심각도 |
|------|------|--------|
| SntFmwMealAction.java:35 | `request.setAttribute("", ...)` - 빈 키 사용 | 높음 |
| SntFmwMealAction.java:42 | 동일 이슈 (update 메서드) | 높음 |
| SntFmwMealAction.java:49 | 동일 이슈 (delete 메서드) | 높음 |
| SntFmwMealEJBDAO.java:92 | 하드코딩된 `"필드명"` 문자열 | 중간 |
| SntFmwMealAction.java:18-21 | raw type 컬렉션 사용 | 중간 |

### 8.2 구조적 개선점

| 항목 | 현황 | 개선 방향 |
|------|------|----------|
| 제네릭 미사용 | Java 1.4 스타일 raw type | Java 5+ 제네릭 도입 |
| 예외 처리 | NullPointerException 별도 catch | 일반 Exception으로 통합 |
| 매직 넘버 | `new Integer(0)` 반환 | 의미 있는 상태 코드/enum 사용 |
| 빌드 도구 | 미포함 | Maven/Gradle 빌드 설정 복구 |

### 8.3 기술 부채

- **Java 1.4 스타일 코드**: 제네릭, 향상된 for-loop, autoboxing 미사용
- **Struts 1.x**: EOL된 프레임워크, 보안 취약점 존재 가능
- **EJB 2.x**: 무거운 CMP/BMP 패턴, 현대적 ORM(JPA)으로 마이그레이션 고려
- **공통 클래스 누락**: 분석 대상 10여 개 공통 클래스 미포함으로 전체 영향도 파악 불가

### 8.4 우선순위별 권고사항

| 우선순위 | 항목 | 내용 |
|----------|------|------|
| 높음 | 빈 키 버그 수정 | `request.setAttribute("", ...)` 올바른 키로 변경 |
| 높음 | 빌드 설정 복구 | pom.xml 또는 build.xml 생성하여 빌드 재현성 확보 |
| 높음 | 공통 클래스 분석 | 참조된 10여 개 공통 클래스 추가 분석 |
| 중간 | Struts JAR 보관 | 폐쇄망 배포를 위한 의존성 JAR 내부 저장소 등록 |
| 중간 | 하드코딩 제거 | `"필드명"` 등 매직 스트링 상수화 |
| 낮음 | Java 버전 업그레이드 | 제네릭, 향상된 for-loop 등 현대 Java 문법 도입 검토 |
| 낮음 | 프레임워크 마이그레이션 | Struts → Spring MVC, EJB 2.x → JPA/Spring 장기 검토 |

---

## 9. 결론

본 프로젝트는 **행정안전부 NTIS 시스템의 식사관리(Food) 모듈**로, **EJB 2.x + Struts 1.x** 기반의 전형적인 Java EE 레거시 아키텍처를 따른다.

- **총 5개 Java 파일**, **271 라인**의 소스코드로 구성
- **3-tier 구조** (Action → Session Bean → DAO) 명확히 분리
- **주민번호 암호화** 등 보안 고려사항 포함
- **폐쇄망 배포 시** Struts JAR 및 빌드 설정 파일 보완 필요
- **분석 대상에 포함되지 않은 공통 클래스** 10여 개가 참조되어 있음 (전체 분석 시 추가 필요)
