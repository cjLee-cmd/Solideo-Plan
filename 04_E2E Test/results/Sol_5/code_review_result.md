# 코드 리뷰 보고서: SNTFMW Meal 모듈

## 개요

| 항목 | 내용 |
|------|------|
| 리뷰 대상 | gov.mogaha.ntis (EJB + Struts Action) |
| 파일 수 | 5개 (Java) |
| 기술 스택 | EJB 2.x, Struts 1.x, Java |
| 아키텍처 | EJB Session Bean + DAO + Struts Action |

---

## 코드 품질 점수: 42 / 100

| 평가 영역 | 점수 | 비고 |
|-----------|------|------|
| 코드 가독성 | 35/100 | 네이밍 불일치, Raw Type 범용, 누락된 import |
| 설계 원칙 | 40/100 | 클래스명-기능 불일치, 중복 코드, 책임 분리 미흡 |
| 에러 처리 | 45/100 | 롤백 처리는 양호하나, NPE 처리 및 예외 메시지 부적절 |
| 로직 정확성 | 35/100 | Null DAO 참조, 빈 문자열 키, 하드코딩 한글 |
| 성능 | 60/100 | 배치 처리 사용은 양호, 불필요한 객체 생성 존재 |
| 보안 | 50/100 | 암호화 적용은 양호, 민감정보 로깅 가능성 |

---

## 상세 이슈 목록

### Critical (즉시 수정 필요)

#### CR-01: DAO에서 QueryService가 null 상태로 초기화되지 않음

- **심각도**: critical
- **파일**: `gov/mogaha/ntis/ejb/snt/fod/SntFmwMealEJBDAO.java:28`
- **설명**: `queryservice` 필드가 `null`로 선언되고 생성자나 초기화 블록에서 초기화되지 않음. 모든 메서드에서 `getQueryservice().find()` 또는 `getQueryservice().update()` 호출 시 즉시 NPE 발생
- **제안**: 생성자 또는 의존성 주입을 통해 QueryService 인스턴스를 초기화해야 함
```java
public SntFmwMealEJBDAO() {
    this.queryservice = new QueryService(); // 또는 DI 컨테이너에서 주입
}
```

#### CR-02: Action에서 빈 문자열을 request attribute 키로 사용

- **심각도**: critical
- **파일**: `gov/mogaha/ntis/web/snt/fod/action/SntFmwMealAction.java:35,42,49`
- **설명**: `request.setAttribute("", invokeLocal(request))` — 빈 문자열("")을 키로 사용. 이는 의도되지 않은 코드이며, 실제 결과 데이터를 뷰에 전달할 수 없음
- **제안**: 의미 있는 키 이름으로 변경
```java
request.setAttribute("result", invokeLocal(request));
```

#### CR-03: 필수 import 문 누락 (Action)

- **심각도**: critical
- **파일**: `gov/mogaha/ntis/web/snt/fod/action/SntFmwMealAction.java:18-27`
- **설명**: `HashMap`, `Collection`, `ArrayList`, `Log`, `NTIS_COMMON_DEFINE` 클래스가 사용되었으나 import문이 없음. 컴파일 오류 발생
- **제안**: 누락된 import 추가
```java
import java.util.HashMap;
import java.util.Collection;
import java.util.ArrayList;
import gov.mogaha.ntis.web.snt.common.Log;
import gov.mogaha.ntis.web.snt.common.NTIS_COMMON_DEFINE;
```

#### CR-04: Local Interface에서 DefaultParameters import 누락

- **심각도**: critical
- **파일**: `gov/mogaha/ntis/ejb/snt/fod/SntFmwMealLocal.java:8`
- **설명**: 메서드 시그니처에 `DefaultParameters`가 사용되었으나 import문이 없음
- **제안**: import 추가
```java
import gov.mogaha.ntis.web.snt.common.DefaultParameters;
```

---

### Major (수정 권장)

#### MJ-01: 클래스명과 실제 기능 불일치

- **심각도**: major
- **파일**: 전 파일
- **설명**: 클래스명은 `SntFmwMeal` (식사 관련)이지만, 메서드명과 쿼리는 `NewBusin` (신규사업) 관련 기능을 처리함. 도메인 혼란 초래
- **제안**: 클래스명을 실제 기능에 맞게 변경 (예: `SntFmwNewBusin`) 또는 기능이 식사 관련이면 메서드/쿼리명 수정

#### MJ-02: Raw Type 사용 (제네릭 미사용)

- **심각도**: major
- **파일**: 전 파일
- **설명**: `HashMap`, `Collection`, `ArrayList` 등이 raw type으로 사용됨. 타입 안정성 저하 및 런타임 ClassCastException 위험
- **제안**: 제네릭 적용
```java
// Before
public HashMap selectListSNTFMWNewBusin(DefaultParameters param)
// After
public HashMap<String, Collection<?>> selectListSNTFMWNewBusin(DefaultParameters param)
```

#### MJ-03: 의미 없는 리턴값 (항상 Integer(0))

- **심각도**: major
- **파일**: `gov/mogaha/ntis/ejb/snt/fod/SntFmwMealEJBDAO.java:54,73,81,102`
- **설명**: insert/update/delete 메서드가 항상 `new Integer(0)`을 반환. 처리 결과(영향받은 행 수 등)를 알 수 없음
- **제안**: 실제 처리 결과 반환 또는 void로 변경
```java
int rows = getQueryservice().update("...", params);
return Integer.valueOf(rows);
```

#### MJ-04: 하드코딩된 한글 문자열

- **심각도**: major
- **파일**: `gov/mogaha/ntis/ejb/snt/fod/SntFmwMealEJBDAO.java:92`
- **설명**: `rs.get("필드명")` — 한글 문자열이 하드코딩됨. 유지보수 및 인코딩 이슈 발생 가능
- **제안**: 상수 정의 또는 프로퍼티 파일로 분리
```java
private static final String FIELD_SMODE = "smode";
private static final String FIELD_TARGET = "필드명"; // 또는 영문 키로 변경
```

#### MJ-05: 임시 쿼리명 사용 (XXX placeholder)

- **심각도**: major
- **파일**: `gov/mogaha/ntis/ejb/snt/fod/SntFmwMealEJBDAO.java:98-100`
- **설명**: `insertXXX`, `updateXXX`, `deleteXXX` — 완성되지 않은 placeholder 쿼리명. 미완성 코드가 프로덕션에 포함됨
- **제안**: 실제 쿼리명으로 변경 또는 미완성 메서드 제거/주석 처리

#### MJ-06: 중복된 예외 처리 패턴

- **심각도**: major
- **파일**: `gov/mogaha/ntis/ejb/snt/fod/SntFmwMealBean.java:35-81`
- **설명**: select/insert/update/delete 4개 메서드가 완전히 동일한 try-catch 패턴을 반복. DRY 원칙 위반
- **제안**: 템플릿 메서드 패턴 또는 AOP로 공통화
```java
private <T> T executeWithTx(Supplier<T> operation) throws DefaultEJBException {
    try {
        return operation.get();
    } catch (SDBException ex) {
        getSessionContext().setRollbackOnly();
        throw processException("SNTE6010", ex);
    } catch (Exception ex) {
        getSessionContext().setRollbackOnly();
        throw processException("NTIS0001", ex);
    }
}
```

#### MJ-07: 부적절한 예외 로그 메시지

- **심각도**: major
- **파일**: `gov/mogaha/ntis/web/snt/fod/action/SntFmwMealAction.java:26-27`
- **설명**: NPE 발생 시 `"NPE"`, 기타 예외 시 `"ERR"`만 로깅. 디버깅에 전혀 도움이 되지 않음. 실제 예외 객체가 로그에 포함되지 않음
- **제안**: 예외 메시지와 스택 트레이스 포함
```java
catch (NullPointerException ex) {
    Log.error(NTIS_COMMON_DEFINE.SNTLOG, "Null pointer in selectList", ex);
}
catch (Exception e) {
    Log.error(NTIS_COMMON_DEFINE.SNTLOG, "Error in selectList: " + e.getMessage(), e);
}
```

#### MJ-08: Struts Action이 null 반환

- **심각도**: major
- **파일**: `gov/mogaha/ntis/web/snt/fod/action/SntFmwMealAction.java:29,36,43,50`
- **설명**: 모든 Action 메서드가 `return null`을 반환. Struts에서 적절한 forward를 찾지 못해 예외 발생 가능
- **제안**: 적절한 ActionForward 반환
```java
return mapping.findForward("success");
```

#### MJ-09: processException 메서드의 불필요한 래핑

- **심각도**: major
- **파일**: `gov/mogaha/ntis/ejb/snt/fod/SntFmwMealBean.java:87-89`
- **설명**: `processException` 메서드가 단순히 생성자 호출만 래핑함. 추가 로직이 없어 불필요한 추상화
- **제안**: 인라인 처리 또는 로깅 등 부가 기능 추가
```java
private DefaultEJBException processException(String errorCode, Exception ex) {
    Log.error(LOG_CATEGORY, "Error [" + errorCode + "]", ex);
    return new DefaultEJBException(errorCode, ex);
}
```

---

### Minor (경미한 개선)

#### MN-01: new Integer() 대신 Integer.valueOf() 사용 권장

- **심각도**: minor
- **파일**: `gov/mogaha/ntis/ejb/snt/fod/SntFmwMealEJBDAO.java:54,73,81,102`
- **설명**: `new Integer(0)`은 매번 새 객체 생성. `Integer.valueOf(0)`은 캐시 활용
- **제안**: `Integer.valueOf(0)` 또는 Java 5+라면 자동 박싱 활용

#### MN-02: SSOSessionUtil 중복 호출

- **심각도**: minor
- **파일**: `gov/mogaha/ntis/web/snt/fod/action/SntFmwMealAction.java:33-34`
- **설명**: insert/update/delete 각 메서드에서 `getUserID`, `getDeptID`를 별도로 호출. 공통 메서드로 추출 가능
- **제안**: private helper 메서드로 추출
```java
private void setSessionAttributes(HttpServletRequest request) {
    request.setAttribute("getUserID", SSOSessionUtil.getUserID(request));
    request.setAttribute("getDeptID", SSOSessionUtil.getDeptID(request));
}
```

#### MN-03: EJB 2.x 레거시 아키텍처

- **심각도**: minor (info)
- **파일**: 전 파일
- **설명**: EJB 2.x (SessionBean, EJBObject, EJBLocalObject)는 현대 Java EE에서 더 이상 사용되지 않음. 유지보수 인력 확보 어려움
- **제안**: 장기적으로 EJB 3.x (Annotation 기반) 또는 Spring Framework로 마이그레이션 검토

#### MN-04: 메서드명 네이밍 컨벤션 불일치

- **심각도**: minor
- **파일**: 전 파일
- **설명**: `selectListSNTFMWNewBusin` (접미사 없음) vs `insertSNTFMWNewBusin01` (접미사 01). 일관성 없는 네이밍
- **제안**: 모든 메서드에 일관된 번호 체계 적용 또는 제거

---

## 보안 검토

| 항목 | 상태 | 비고 |
|------|------|------|
| 개인정보 암호화 | 양호 | `CCDEncryption.sntEncrypt()`로 주민번호 암호화 |
| 암호화 복호화 | 주의 | `sntDecryptCol()`로 복호화 후 컬렉션에 저장 — 메모리 상 평문 노출 가능 |
| SQL Injection | 확인 필요 | QueryService를 통한 간접 쿼리 실행이나, 파라미터 전달 방식 확인 필요 |
| 세션 관리 | 확인 필요 | `SSOSessionUtil` 사용 중이지만, 세션 타임아웃/재인증 로직 확인 필요 |
| 민감정보 로깅 | 주의 | Log.error 호출 시 파라미터 내용이 포함되지 않도록 확인 필요 |

---

## 요약 및 우선순위

| 우선순위 | 이슈 수 | 주요 조치 |
|----------|---------|-----------|
| Critical | 4 | Null DAO 초기화, 빈 문자열 키, import 누락 수정 |
| Major | 9 | 클래스명 변경, 제네릭 적용, 예외 처리 개선, placeholder 쿼리 정리 |
| Minor | 4 | Integer.valueOf, 중복 코드 제거, 네이밍 일관성 |

### 권장 개선 순서

1. **1단계 (Critical)**: 컴파일 오류 수정 (import 누락), Null DAO 초기화, 빈 문자열 키 수정
2. **2단계 (Major)**: placeholder 쿼리명 완성 또는 메서드 제거, 예외 로그 개선, 제네릭 적용
3. **3단계 (Major)**: 클래스명-기능 정합성 맞추기, 중복 예외 처리 패턴 리팩토링
4. **4단계 (Minor)**: 코드 스타일 개선, 네이밍 컨벤션 통일
