# Data Model — 내부결재시스템

> **버전**: 1.0  
> **작성일**: 2026-04-02

---

## 1. 엔티티 정의

### 1.1 TB_USER (사용자)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| EMP_NO | VARCHAR2(20) | PK | 사원번호 |
| EMP_NAME | VARCHAR2(100) | NOT NULL | 이름 |
| DEPT_CODE | VARCHAR2(20) | NOT NULL, FK | 부서코드 |
| POSITION_CODE | VARCHAR2(20) | NOT NULL | 직급코드 |
| EMAIL | VARCHAR2(100) | | 이메일 |
| PHONE | VARCHAR2(20) | | 연락처 |
| STATUS | VARCHAR2(10) | NOT NULL, DEFAULT 'ACTIVE' | 상태 (ACTIVE/INACTIVE/ON_LEAVE) |
| LOGIN_FAIL_COUNT | NUMBER(3) | DEFAULT 0 | 로그인 실패 횟수 |
| LOGIN_LOCK_TIME | TIMESTAMP | | 계정 잠금 시간 |
| CREATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 생성일시 |
| UPDATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 수정일시 |

**검증 규칙**:
- STATUS: 'ACTIVE', 'INACTIVE', 'ON_LEAVE' 중 하나
- LOGIN_FAIL_COUNT >= 5 시 LOGIN_LOCK_TIME 설정

---

### 1.2 TB_DEPARTMENT (부서)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| DEPT_CODE | VARCHAR2(20) | PK | 부서코드 |
| DEPT_NAME | VARCHAR2(100) | NOT NULL | 부서명 |
| PARENT_DEPT_CODE | VARCHAR2(20) | FK (self) | 상위부서코드 |
| USE_YN | CHAR(1) | NOT NULL, DEFAULT 'Y' | 사용여부 (Y/N) |
| SORT_ORDER | NUMBER(5) | DEFAULT 0 | 정렬순서 |
| CREATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 생성일시 |
| UPDATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 수정일시 |

---

### 1.3 TB_POSITION (직급)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| POSITION_CODE | VARCHAR2(20) | PK | 직급코드 |
| POSITION_NAME | VARCHAR2(100) | NOT NULL | 직급명 |
| POSITION_LEVEL | NUMBER(3) | NOT NULL | 직급 레벨 (높을수록 상위) |
| USE_YN | CHAR(1) | NOT NULL, DEFAULT 'Y' | 사용여부 |

---

### 1.4 TB_DOCUMENT (결재 문서)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| DOC_ID | VARCHAR2(30) | PK | 문서ID (DOC-YYYYMMDD-XXXXXX) |
| TITLE | VARCHAR2(500) | NOT NULL | 제목 |
| CONTENT | CLOB | NOT NULL | 내용 |
| DOC_TYPE | VARCHAR2(50) | NOT NULL | 문서종류 (품의서/출장신청/지출결의서 등) |
| STATUS | VARCHAR2(20) | NOT NULL | 문서상태 |
| DRAFTER_EMP_NO | VARCHAR2(20) | NOT NULL, FK | 기안자 사번 |
| DEPT_CODE | VARCHAR2(20) | NOT NULL, FK | 기안 부서코드 |
| SUBMITTED_AT | TIMESTAMP | | 상신 일시 |
| COMPLETED_AT | TIMESTAMP | | 완료 일시 |
| CREATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 생성일시 |
| UPDATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 수정일시 |

**문서상태 (STATUS) 값**:
- `TEMP`: 임시저장
- `DRAFT`: 기안 (작성완료, 미상신)
- `SUBMITTED`: 상신 (결재선으로 전송됨)
- `IN_PROGRESS`: 결재진행 중
- `APPROVED`: 승인 (완료)
- `REJECTED`: 반려
- `RETURNED`: 반려취소 (기안자가 반려문서 수거)
- `CANCELLED`: 취소

**상태 전이 규칙**:
```
TEMP → DRAFT → SUBMITTED → IN_PROGRESS → APPROVED (완료)
                        ↓
                     REJECTED → RETURNED → DRAFT → 재상신
SUBMITTED → CANCELLED (기안자만, 상신 후 즉시)
```

---

### 1.5 TB_APPROVAL_LINE (결재선)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| LINE_ID | VARCHAR2(30) | PK | 결재선ID |
| DOC_ID | VARCHAR2(30) | NOT NULL, FK | 문서ID |
| LINE_TYPE | VARCHAR2(10) | NOT NULL | 라인유형 (APPROVER/REFEREE) |
| LINE_ORDER | NUMBER(5) | NOT NULL | 순서 (1부터 시작) |
| EMP_NO | VARCHAR2(20) | NOT NULL, FK | 결재자/참조자 사번 |
| STATUS | VARCHAR2(20) | NOT NULL, DEFAULT 'PENDING' | 처리상태 |
| PROCESSED_AT | TIMESTAMP | | 처리일시 |
| COMMENT | VARCHAR2(2000) | | 의견 |
| CREATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 생성일시 |

**처리상태 (STATUS) 값**:
- `PENDING`: 대기 중
- `APPROVED`: 승인
- `REJECTED`: 반려

**검증 규칙**:
- LINE_TYPE = 'APPROVER' 인 경우 LINE_ORDER 순서대로 처리
- LINE_TYPE = 'REFEREE' 는 순서 없음 (동시 참조)
- 동일 문서에 동일 EMP_NO 중복 불가

---

### 1.6 TB_APPROVAL_HISTORY (결재 이력)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| HISTORY_ID | VARCHAR2(30) | PK | 이력ID |
| DOC_ID | VARCHAR2(30) | NOT NULL, FK | 문서ID |
| EMP_NO | VARCHAR2(20) | NOT NULL, FK | 처리자 사번 |
| ACTION | VARCHAR2(20) | NOT NULL | 처리결과 |
| COMMENT | VARCHAR2(2000) | | 의견 |
| CREATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 처리일시 |

**처리결과 (ACTION) 값**:
- `SUBMIT`: 상신
- `APPROVE`: 승인
- `REJECT`: 반려
- `RETURN`: 반려취소 (수거)
- `CANCEL`: 취소
- `REFER`: 참조전송

---

### 1.7 TB_ATTACHMENT (첨부파일)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| ATTACH_ID | VARCHAR2(30) | PK | 첨부파일ID |
| DOC_ID | VARCHAR2(30) | NOT NULL, FK | 문서ID |
| ORIGINAL_NAME | VARCHAR2(500) | NOT NULL | 원본파일명 |
| STORED_NAME | VARCHAR2(500) | NOT NULL | 저장파일명 (UUID) |
| FILE_PATH | VARCHAR2(1000) | NOT NULL | 저장경로 |
| FILE_SIZE | NUMBER(10) | NOT NULL | 파일크기 (bytes) |
| CONTENT_TYPE | VARCHAR2(100) | | MIME 타입 |
| CREATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 업로드일시 |

**검증 규칙**:
- FILE_SIZE <= 52,428,800 (50MB)

---

### 1.8 TB_AUDIT_LOG (감사 로그)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| LOG_ID | VARCHAR2(30) | PK | 로그ID |
| EMP_NO | VARCHAR2(20) | | 사용자 사번 (시스템 작업 시 NULL) |
| ACTION_TYPE | VARCHAR2(30) | NOT NULL | 작업유형 |
| TARGET_TYPE | VARCHAR2(30) | NOT NULL | 대상유형 |
| TARGET_ID | VARCHAR2(30) | | 대상ID |
| BEFORE_VALUE | CLOB | | 변경 전 값 (JSON) |
| AFTER_VALUE | CLOB | | 변경 후 값 (JSON) |
| IP_ADDRESS | VARCHAR2(45) | | 접속 IP |
| CREATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 작업일시 |

**작업유형 (ACTION_TYPE) 값**:
- `LOGIN`, `LOGOUT`, `LOGIN_FAIL`
- `DOC_CREATE`, `DOC_UPDATE`, `DOC_DELETE`
- `DOC_SUBMIT`, `DOC_APPROVE`, `DOC_REJECT`, `DOC_RETURN`, `DOC_CANCEL`
- `LINE_CREATE`, `LINE_UPDATE`
- `FILE_UPLOAD`, `FILE_DELETE`
- `SYNC_START`, `SYNC_COMPLETE`, `SYNC_FAIL`

**보안 규칙**:
- INSERT 전용 (UPDATE/DELETE 권한 차단)
- 5년 보관 후 아카이브

---

### 1.9 TB_SYNC_LOG (동기화 이력)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| SYNC_ID | VARCHAR2(30) | PK | 동기화ID |
| SYNC_TYPE | VARCHAR2(20) | NOT NULL | 동기화유형 (USER/DEPARTMENT/POSITION) |
| START_TIME | TIMESTAMP | NOT NULL | 시작일시 |
| END_TIME | TIMESTAMP | | 종료일시 |
| RECORD_COUNT | NUMBER(10) | | 처리 건수 |
| SUCCESS_YN | CHAR(1) | NOT NULL | 성공여부 (Y/N) |
| ERROR_MSG | VARCHAR2(2000) | | 오류메시지 |

---

### 1.10 TB_DOCUMENT_TEMPLATE (결재 양식 템플릿)

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| TEMPLATE_ID | VARCHAR2(30) | PK | 템플릿ID |
| TEMPLATE_NAME | VARCHAR2(200) | NOT NULL | 템플릿명 |
| DOC_TYPE | VARCHAR2(50) | NOT NULL | 문서종류 |
| FORM_SCHEMA | CLOB | NOT NULL | 양식 스키마 (JSON) |
| USE_YN | CHAR(1) | NOT NULL, DEFAULT 'Y' | 사용여부 |
| CREATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 생성일시 |
| UPDATED_AT | TIMESTAMP | NOT NULL, DEFAULT SYSTIMESTAMP | 수정일시 |

---

## 2. 관계 정의

```
TB_DEPARTMENT 1 ──< TB_USER >── 1 TB_POSITION
                       │
                       └──< TB_DOCUMENT >── 1 TB_DEPARTMENT (기안부서)
                              │
                              ├──< TB_APPROVAL_LINE >── TB_USER (결재자)
                              ├──< TB_APPROVAL_HISTORY >── TB_USER (처리자)
                              └──< TB_ATTACHMENT
```

## 3. 인덱스 전략

| 테이블 | 인덱스명 | 컬럼 | 목적 |
|--------|----------|------|------|
| TB_DOCUMENT | IDX_DOC_DRAFTER | DRAFTER_EMP_NO | 기안자별 조회 |
| TB_DOCUMENT | IDX_DOC_STATUS | STATUS | 상태별 조회 |
| TB_DOCUMENT | IDX_DOC_SUBMITTED | SUBMITTED_AT | 기간별 조회 |
| TB_DOCUMENT | IDX_DOC_SEARCH | STATUS, DRAFTER_EMP_NO, SUBMITTED_AT | 복합 검색 |
| TB_APPROVAL_LINE | IDX_LINE_DOC | DOC_ID | 문서별 결재선 조회 |
| TB_APPROVAL_LINE | IDX_LINE_EMP | EMP_NO, STATUS | 사용자별 대기 결재 |
| TB_APPROVAL_HISTORY | IDX_HIST_DOC | DOC_ID, CREATED_AT | 문서별 이력 타임라인 |
| TB_AUDIT_LOG | IDX_AUDIT_EMP | EMP_NO, CREATED_AT | 사용자별 감사로그 |
| TB_AUDIT_LOG | IDX_AUDIT_ACTION | ACTION_TYPE, CREATED_AT | 작업유형별 조회 |
| TB_ATTACHMENT | IDX_ATTACH_DOC | DOC_ID | 문서별 첨부파일 조회 |
