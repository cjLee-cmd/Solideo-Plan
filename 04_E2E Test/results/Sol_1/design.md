# 설계 문서 (design.md) — 내부결재시스템

> **버전**: 1.0  
> **작성일**: 2026-04-02  
> **작성자**: Solideo AI Architect  
> **승인**: _미정_  
> **상태**: Final Draft

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [아키텍처 설계](#2-아키텍처-설계)
3. [모듈 구조](#3-모듈-구조)
4. [API 설계](#4-api-설계)
5. [DB 스키마](#5-db-스키마)
6. [기술스택 결정](#6-기술스택-결정)
7. [보안 설계](#7-보안-설계)
8. [비기능 요구사항](#8-비기능-요구사항)

---

## 1. 프로젝트 개요

### 1.1 프로젝트 정보

| 항목 | 내용 |
|------|------|
| **프로젝트명** | 내부결재시스템 (Internal Approval System) |
| **목적** | 전자결재 자동화를 통한 종이결재 대체 및 업무 효율화 |
| **개발언어** | Java 17 |
| **프레임워크** | Spring Boot 3.x |
| **데이터베이스** | Oracle 19c |
| **배포환경** | 폐쇄망 (외부 네트워크 차단) |

### 1.2 프로젝트 범위

**포함 (In-Scope)**:
- 결재 문서 작성 (기안) 및 임시저장
- 기안자에 의한 결재선 직접 지정 (결재자 1인 + 참조자 N명)
- 결재자의 승인/반려 처리
- 결재 이력 조회 및 검색 (상태, 기안자, 기간, 키워드)
- 인사DB (Oracle 19c) 연동을 통한 조직/직원 정보 동기화
- 첨부파일 관리 (로컬 파일시스템 저장, 50MB 제한)
- REST API 제공 (프론트엔드는 별도 프로젝트)
- 감사로그 기록 (DB 저장)

**제외 (Out-of-Scope)**:
- 프론트엔드 UI 개발 (별도 프로젝트)
- 다단계 결재선 (향후 확장 고려, 현재는 단일 결재자)
- 모바일 네이티브 앱
- 결재선 템플릿 자동 적용 (수동 지정만 지원, 템플릿은 향후 확장)
- 외부 이메일/SMS 알림 (폐쇄망 제약)
- 결재문서 내용 암호화 (접근제어로 대체)

### 1.3 용어 정의

| 용어 | 정의 |
|------|------|
| **기안** | 결재 문서를 작성하는 행위 및 작성자 |
| **상신** | 작성된 결재 문서를 결재선으로 공식 제출하는 행위 |
| **결재선** | 결재 문서에 적용될 결재자 및 참조자 순서 목록 |
| **결재자** | 문서를 승인/반려할 권한을 가진 사람 (1인, 순차적) |
| **참조자** | 결재 결과를 참조만 하는 사람 (N명, 순서 없음) |
| **승인** | 결재자가 문서에 동의하는 처리 |
| **반려** | 결재자가 문서를 거부하고 기안자에게 반환하는 처리 |
| **반려취소(수거)** | 기안자가 반려된 문서를 가져와 수정 후 재상신하는 행위 |
| **감사로그** | 시스템 내 모든 주요 작업의 추적 기록 (위변조 방지) |

### 1.4 결재 상태 전이

```
                    ┌──────────────────────────────────────────┐
                    │                                          │
    [시작] ──→ TEMP ──→ DRAFT ──→ SUBMITTED ──→ IN_PROGRESS ──→ APPROVED [완료]
                    │              │              │
                    │              ↓              ↓
                    │         CANCELLED      REJECTED
                    │                             │
                    │                             ↓
                    └─────────────────────── RETURNED ──→ DRAFT (재상신)
```

| 상태 | 코드 | 설명 | 전이 가능 대상 |
|------|------|------|----------------|
| 임시저장 | `TEMP` | 작성 중, 미제출 | DRAFT, 삭제 |
| 기안 | `DRAFT` | 작성완료, 미상신 | SUBMITTED, TEMP |
| 상신 | `SUBMITTED` | 결재선으로 전송됨 | IN_PROGRESS, CANCELLED |
| 결재진행 | `IN_PROGRESS` | 결재자가 처리 중 | APPROVED, REJECTED |
| 승인 | `APPROVED` | 최종 승인 완료 | - (종단) |
| 반려 | `REJECTED` | 결재자 반려 | RETURNED |
| 반려취소 | `RETURNED` | 기안자가 반려문서 수거 | DRAFT |
| 취소 | `CANCELLED` | 기안자 취소 | - (종단) |

---

## 2. 아키텍처 설계

### 2.1 시스템 구성도

```
┌─────────────────────────────────────────────────────────────────────┐
│                        폐  쇄  망  환  경                          │
│                                                                     │
│  ┌──────────────┐      ┌──────────────────────────────────────┐    │
│  │  Web Server   │      │        Application Server            │    │
│  │  (Nginx/Apache)│─────▶│  Spring Boot 3.x (JAR)              │    │
│  │  Reverse Proxy │      │  - REST API                         │    │
│  │  TLS Terminate │      │  - JWT 인증                         │    │
│  └──────────────┘      │  - 비즈니스 로직                      │    │
│                         │  - HR 동기화 스케줄러                │    │
│                         └──────────┬───────────────────────────┘    │
│                                    │ JDBC                           │
│                         ┌──────────▼───────────────────────────┐    │
│                         │         Database Server               │    │
│                         │  Oracle 19c                           │    │
│                         │  - 결재 DB (approval_admin)           │    │
│                         │  - 인사 DB (hr_reader, 읽기전용)      │    │
│                         └───────────────────────────────────────┘    │
│                                    │                                 │
│                         ┌──────────▼───────────────────────────┐    │
│                         │       File Storage (로컬)             │    │
│                         │  /data/approval/uploads/              │    │
│                         │  - 첨부파일 저장                      │    │
│                         └───────────────────────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 계층 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                    Presentation Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ REST        │  │ Exception   │  │ Interceptor             │ │
│  │ Controller  │  │ Handler     │  │ (JWT 검증, 로깅)        │ │
│  └──────┬──────┘  └─────────────┘  └─────────────────────────┘ │
├─────────┼───────────────────────────────────────────────────────┤
│                    Business Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Document    │  │ Approval    │  │ Sync                    │ │
│  │ Service     │  │ Service     │  │ Service                 │ │
│  │             │  │             │  │ (HR DB 연동)            │ │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘ │
│         │                │                       │              │
│  ┌──────▼────────────────▼───────────────────────▼────────────┐ │
│  │              Domain Model / Entity                         │ │
│  │  Document, ApprovalLine, ApprovalHistory, User, ...        │ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Data Access Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ JPA         │  │ Query       │  │ File                    │ │
│  │ Repository  │  │ (Native)    │  │ Storage                 │ │
│  │ (결재 DB)   │  │ (복잡조회)  │  │ (첨부파일)              │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Infrastructure                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Oracle 19c  │  │ JWT         │  │ Scheduler               │ │
│  │ (결재+인사) │  │ Provider    │  │ (HR 동기화)             │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 통신 방식

| 통신 경로 | 프로토콜 | 설명 |
|-----------|----------|------|
| Web Server → App Server | HTTP/1.1 (내부망) | Reverse Proxy 경유 |
| App Server → 결재 DB | JDBC (Oracle Thin) | HikariCP Connection Pool |
| App Server → 인사 DB | JDBC (Oracle Thin, 읽기전용) | 별도 DataSource, 읽기 전용 계정 |
| Client → Web Server | HTTPS (TLS 1.2+) | 외부 진입점 TLS 암호화 |
| App Server → File Storage | 로컬 파일 I/O | NIO 기반 비동기 읽기/쓰기 |

---

## 3. 모듈 구조

### 3.1 모듈 목록 및 역할

| 모듈 | 패키지 | 역할 |
|------|--------|------|
| **config** | `com.solideo.approval.config` | Spring 설정 (Security, JPA, Web, Swagger, File) |
| **security** | `com.solideo.approval.security` | JWT 인증, 인가, 필터, 토큰 관리 |
| **controller** | `com.solideo.approval.controller` | REST API 엔드포인트, 요청/응답 매핑 |
| **service** | `com.solideo.approval.service` | 비즈니스 로직, 트랜잭션 관리 |
| **repository** | `com.solideo.approval.repository` | JPA Repository, Native Query |
| **entity** | `com.solideo.approval.entity` | JPA 엔티티, DB 매핑 |
| **dto** | `com.solideo.approval.dto` | 요청/응답 DTO, 검증 어노테이션 |
| **exception** | `com.solideo.approval.exception` | 전역 예외 처리, 커스텀 예외 |
| **scheduler** | `com.solideo.approval.scheduler` | HR DB 동기화 스케줄러 |
| **audit** | `com.solideo.approval.audit` | 감사로그 기록 (AOP 기반) |
| **file** | `com.solideo.approval.file` | 첨부파일 저장/조회/삭제 |

### 3.2 모듈 간 의존성

```
controller ──▶ service ──▶ repository ──▶ entity
     │              │
     │              ├──▶ audit (AOP)
     │              ├──▶ file
     │              └──▶ scheduler
     │
     └──▶ security (JWT 필터)
          └──▶ dto (요청/응답)
```

**의존성 규칙**:
- controller → service (단방향)
- service → repository, audit, file (단방향)
- repository → entity (단방향)
- 상위 계층은 하위 계층에만 의존 (의존성 역전 원칙)
- 순환 의존 금지

### 3.3 디렉토리 구조

```
approval-system/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/com/solideo/approval/
│   │   │   ├── ApprovalApplication.java
│   │   │   ├── config/
│   │   │   │   ├── SecurityConfig.java
│   │   │   │   ├── JpaConfig.java
│   │   │   │   ├── WebConfig.java
│   │   │   │   ├── SwaggerConfig.java
│   │   │   │   └── FileStorageConfig.java
│   │   │   ├── security/
│   │   │   │   ├── JwtTokenProvider.java
│   │   │   │   ├── JwtAuthenticationFilter.java
│   │   │   │   ├── CustomUserDetailsService.java
│   │   │   │   └── SecurityConstants.java
│   │   │   ├── controller/
│   │   │   │   ├── AuthController.java
│   │   │   │   ├── DocumentController.java
│   │   │   │   ├── ApprovalController.java
│   │   │   │   ├── InboxController.java
│   │   │   │   ├── AttachmentController.java
│   │   │   │   ├── OrganizationController.java
│   │   │   │   └── SyncController.java
│   │   │   ├── service/
│   │   │   │   ├── AuthService.java
│   │   │   │   ├── DocumentService.java
│   │   │   │   ├── ApprovalService.java
│   │   │   │   ├── HrSyncService.java
│   │   │   │   └── UserService.java
│   │   │   ├── repository/
│   │   │   │   ├── DocumentRepository.java
│   │   │   │   ├── ApprovalLineRepository.java
│   │   │   │   ├── ApprovalHistoryRepository.java
│   │   │   │   ├── UserRepository.java
│   │   │   │   ├── DepartmentRepository.java
│   │   │   │   ├── AuditLogRepository.java
│   │   │   │   ├── AttachmentRepository.java
│   │   │   │   └── SyncLogRepository.java
│   │   │   ├── entity/
│   │   │   │   ├── Document.java
│   │   │   │   ├── ApprovalLine.java
│   │   │   │   ├── ApprovalHistory.java
│   │   │   │   ├── User.java
│   │   │   │   ├── Department.java
│   │   │   │   ├── Position.java
│   │   │   │   ├── AuditLog.java
│   │   │   │   ├── Attachment.java
│   │   │   │   └── SyncLog.java
│   │   │   ├── dto/
│   │   │   │   ├── request/
│   │   │   │   │   ├── LoginRequest.java
│   │   │   │   │   ├── DocumentCreateRequest.java
│   │   │   │   │   ├── DocumentSubmitRequest.java
│   │   │   │   │   ├── ApprovalActionRequest.java
│   │   │   │   │   └── DocumentSearchRequest.java
│   │   │   │   └── response/
│   │   │   │       ├── LoginResponse.java
│   │   │   │       ├── DocumentResponse.java
│   │   │   │       ├── DocumentListResponse.java
│   │   │   │       ├── ApprovalLineResponse.java
│   │   │   │       └── PageResponse.java
│   │   │   ├── exception/
│   │   │   │   ├── GlobalExceptionHandler.java
│   │   │   │   ├── ApprovalException.java
│   │   │   │   ├── DocumentNotFoundException.java
│   │   │   │   ├── InvalidApprovalStateException.java
│   │   │   │   └── FileStorageException.java
│   │   │   ├── audit/
│   │   │   │   ├── AuditLogAspect.java
│   │   │   │   ├── AuditLogService.java
│   │   │   │   └── AuditAction.java
│   │   │   ├── scheduler/
│   │   │   │   └── HrSyncScheduler.java
│   │   │   └── file/
│   │   │       ├── FileStorageService.java
│   │   │       └── FileStorageProperties.java
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       ├── application-prod.yml
│   │       ├── schema.sql
│   │       └── data.sql
│   └── test/
│       └── java/com/solideo/approval/
│           ├── service/
│           │   ├── DocumentServiceTest.java
│           │   └── ApprovalServiceTest.java
│           ├── controller/
│           │   └── DocumentControllerTest.java
│           └── ApprovalApplicationTests.java
├── docs/
│   ├── design.md
│   ├── data-model.md
│   └── api-contracts.md
└── scripts/
    ├── deploy.sh
    └── db-migrate.sh
```

---

## 4. API 설계

### 4.1 API 개요

| 항목 | 내용 |
|------|------|
| **Base URL** | `/api/v1` |
| **포맷** | JSON (UTF-8) |
| **인증** | JWT Bearer Token (`Authorization: Bearer <token>`) |
| **페이징** | Spring Data Pageable (`page`, `size`, `sort`) |
| **버저닝** | URL Path (`/api/v1/...`) |

### 4.2 공통 응답 포맷

**성공 응답**:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

**에러 응답**:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_STATE",
    "message": "현재 상태에서 해당 작업을 수행할 수 없습니다.",
    "details": "문서 상태: REJECTED, 허용 상태: [TEMP, DRAFT, RETURNED]"
  }
}
```

### 4.3 엔드포인트 목록

| Method | Endpoint | 설명 | Auth |
|--------|----------|------|------|
| **인증** | | | |
| POST | `/api/v1/auth/login` | 로그인 (사번/비밀번호) | Public |
| POST | `/api/v1/auth/logout` | 로그아웃 | Bearer |
| POST | `/api/v1/auth/refresh` | 토큰 재발급 | Public |
| **결재 문서** | | | |
| POST | `/api/v1/documents` | 문서 생성 (임시저장) | DRAFTER+ |
| GET | `/api/v1/documents/{docId}` | 문서 상세 조회 | 접근권한자 |
| PUT | `/api/v1/documents/{docId}` | 문서 수정 | 기안자 |
| DELETE | `/api/v1/documents/{docId}` | 문서 삭제 | 기안자 (TEMP만) |
| POST | `/api/v1/documents/{docId}/submit` | 문서 상신 | 기안자 |
| POST | `/api/v1/documents/{docId}/cancel` | 문서 취소 | 기안자 |
| GET | `/api/v1/documents` | 문서 목록 검색 | 인증사용자 |
| **결재 처리** | | | |
| POST | `/api/v1/documents/{docId}/approve` | 결재 승인 | 현재결재자 |
| POST | `/api/v1/documents/{docId}/reject` | 결재 반려 | 현재결재자 |
| POST | `/api/v1/documents/{docId}/return` | 반려문서 수거 | 기안자 |
| **결재함** | | | |
| GET | `/api/v1/inbox` | 내가 결재할 문서 | 인증사용자 |
| GET | `/api/v1/outbox` | 내가 기안한 문서 | 인증사용자 |
| GET | `/api/v1/referenced` | 참조된 문서 | 인증사용자 |
| **이력** | | | |
| GET | `/api/v1/documents/{docId}/history` | 결재 이력 타임라인 | 접근권한자 |
| GET | `/api/v1/documents/{docId}/approval-line` | 결재선 현황 | 접근권한자 |
| **첨부파일** | | | |
| POST | `/api/v1/documents/{docId}/attachments` | 파일 업로드 | 기안자 |
| DELETE | `/api/v1/documents/{docId}/attachments/{attachId}` | 파일 삭제 | 기안자 |
| GET | `/api/v1/documents/{docId}/attachments/{attachId}/download` | 파일 다운로드 | 접근권한자 |
| **조직** | | | |
| GET | `/api/v1/departments` | 부서 목록 (트리) | 인증사용자 |
| GET | `/api/v1/users/search` | 사용자 검색 | 인증사용자 |
| **동기화** | | | |
| POST | `/api/v1/sync/hr` | 인사DB 수동 동기화 | ADMIN |
| GET | `/api/v1/sync/logs` | 동기화 이력 | ADMIN |

### 4.4 인증/인가 방식

**인증 플로우**:
1. 클라이언트가 `POST /api/v1/auth/login` 으로 사번/비밀번호 전송
2. 서버가 인사DB에서 사번/비밀번호 검증 (BCrypt 해시 비교)
3. 검증 성공 시 JWT Access Token (30분) + Refresh Token (8시간) 발급
4. 이후 요청은 `Authorization: Bearer <accessToken>` 헤더 포함
5. Access Token 만료 시 `POST /api/v1/auth/refresh` 로 재발급
6. 로그아웃 시 토큰 블랙리스트 등록 (Redis 또는 DB)

**인가 규칙**:
- `@PreAuthorize("hasRole('DRAFTER')")` — 역할 기반 API 접근 제어
- 데이터 수준 인가: Service 레이어에서 기안자/결재자/참조자 여부 검증
- 감사로그: 모든 WRITE 작업은 AOP 기반 AuditLogAspect에서 자동 기록

### 4.5 에러 코드 정의

| HTTP 상태 | 에러 코드 | 설명 |
|-----------|-----------|------|
| 400 | `VALIDATION_ERROR` | 요청 데이터 검증 실패 |
| 400 | `INVALID_STATE` | 현재 상태에서 작업 불가 |
| 400 | `FILE_SIZE_EXCEEDED` | 첨부파일 용량 초과 (50MB) |
| 400 | `CIRCULAR_APPROVAL_LINE` | 결재선 순환 참조 감지 |
| 401 | `AUTH_FAILED` | 인증 실패 (사번/비밀번호 불일치) |
| 401 | `TOKEN_EXPIRED` | 토큰 만료 |
| 401 | `TOKEN_INVALID` | 유효하지 않은 토큰 |
| 403 | `ACCESS_DENIED` | 접근 권한 없음 |
| 403 | `NOT_APPROVER` | 현재 결재자가 아님 |
| 404 | `DOCUMENT_NOT_FOUND` | 문서 없음 |
| 404 | `USER_NOT_FOUND` | 사용자 없음 |
| 409 | `DUPLICATE_APPROVER` | 결재선 중복 |
| 423 | `ACCOUNT_LOCKED` | 계정 잠금 |
| 500 | `INTERNAL_ERROR` | 내부 서버 오류 |
| 503 | `HR_DB_UNAVAILABLE` | 인사DB 연결 불가 |

---

## 5. DB 스키마

### 5.1 테이블 정의

> 전체 테이블 정의는 `90_Result_Doc/data-model.md` 참조. 아래는 핵심 테이블의 DDL 요약.

### 5.2 핵심 테이블 DDL

#### TB_DOCUMENT (결재 문서)
```sql
CREATE TABLE TB_DOCUMENT (
    DOC_ID          VARCHAR2(30)    CONSTRAINT PK_DOCUMENT PRIMARY KEY,
    TITLE           VARCHAR2(500)   NOT NULL,
    CONTENT         CLOB            NOT NULL,
    DOC_TYPE        VARCHAR2(50)    NOT NULL,
    STATUS          VARCHAR2(20)    NOT NULL,
    DRAFTER_EMP_NO  VARCHAR2(20)    NOT NULL,
    DEPT_CODE       VARCHAR2(20)    NOT NULL,
    SUBMITTED_AT    TIMESTAMP,
    COMPLETED_AT    TIMESTAMP,
    CREATED_AT      TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    UPDATED_AT      TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    CONSTRAINT FK_DOC_DRAFTER FOREIGN KEY (DRAFTER_EMP_NO) REFERENCES TB_USER(EMP_NO),
    CONSTRAINT FK_DOC_DEPT FOREIGN KEY (DEPT_CODE) REFERENCES TB_DEPARTMENT(DEPT_CODE),
    CONSTRAINT CHK_DOC_STATUS CHECK (STATUS IN ('TEMP','DRAFT','SUBMITTED','IN_PROGRESS','APPROVED','REJECTED','RETURNED','CANCELLED'))
);
```

#### TB_APPROVAL_LINE (결재선)
```sql
CREATE TABLE TB_APPROVAL_LINE (
    LINE_ID         VARCHAR2(30)    CONSTRAINT PK_APPROVAL_LINE PRIMARY KEY,
    DOC_ID          VARCHAR2(30)    NOT NULL,
    LINE_TYPE       VARCHAR2(10)    NOT NULL,
    LINE_ORDER      NUMBER(5)       NOT NULL,
    EMP_NO          VARCHAR2(20)    NOT NULL,
    STATUS          VARCHAR2(20)    DEFAULT 'PENDING' NOT NULL,
    PROCESSED_AT    TIMESTAMP,
    COMMENT         VARCHAR2(2000),
    CREATED_AT      TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    CONSTRAINT FK_LINE_DOC FOREIGN KEY (DOC_ID) REFERENCES TB_DOCUMENT(DOC_ID),
    CONSTRAINT FK_LINE_EMP FOREIGN KEY (EMP_NO) REFERENCES TB_USER(EMP_NO),
    CONSTRAINT CHK_LINE_TYPE CHECK (LINE_TYPE IN ('APPROVER','REFEREE')),
    CONSTRAINT CHK_LINE_STATUS CHECK (STATUS IN ('PENDING','APPROVED','REJECTED')),
    CONSTRAINT UQ_LINE_DOC_EMP UNIQUE (DOC_ID, EMP_NO)
);
```

#### TB_APPROVAL_HISTORY (결재 이력)
```sql
CREATE TABLE TB_APPROVAL_HISTORY (
    HISTORY_ID      VARCHAR2(30)    CONSTRAINT PK_APPROVAL_HISTORY PRIMARY KEY,
    DOC_ID          VARCHAR2(30)    NOT NULL,
    EMP_NO          VARCHAR2(20)    NOT NULL,
    ACTION          VARCHAR2(20)    NOT NULL,
    COMMENT         VARCHAR2(2000),
    CREATED_AT      TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    CONSTRAINT FK_HIST_DOC FOREIGN KEY (DOC_ID) REFERENCES TB_DOCUMENT(DOC_ID),
    CONSTRAINT FK_HIST_EMP FOREIGN KEY (EMP_NO) REFERENCES TB_USER(EMP_NO),
    CONSTRAINT CHK_HIST_ACTION CHECK (ACTION IN ('SUBMIT','APPROVE','REJECT','RETURN','CANCEL','REFER'))
);
```

#### TB_AUDIT_LOG (감사 로그) — INSERT 전용
```sql
CREATE TABLE TB_AUDIT_LOG (
    LOG_ID          VARCHAR2(30)    CONSTRAINT PK_AUDIT_LOG PRIMARY KEY,
    EMP_NO          VARCHAR2(20),
    ACTION_TYPE     VARCHAR2(30)    NOT NULL,
    TARGET_TYPE     VARCHAR2(30)    NOT NULL,
    TARGET_ID       VARCHAR2(30),
    BEFORE_VALUE    CLOB,
    AFTER_VALUE     CLOB,
    IP_ADDRESS      VARCHAR2(45),
    CREATED_AT      TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL
);

-- 감사로그 전용 권한 (INSERT만 허용)
-- GRANT INSERT ON TB_AUDIT_LOG TO approval_app;
-- GRANT SELECT ON TB_AUDIT_LOG TO approval_admin;
```

### 5.3 관계 정의

```
TB_DEPARTMENT (1) ────< (N) TB_USER (N) >──── (1) TB_POSITION
                            │
                            └───< (N) TB_DOCUMENT (N) >──── (1) TB_DEPARTMENT (기안부서)
                                   │
                                   ├──< (N) TB_APPROVAL_LINE >── TB_USER (결재자/참조자)
                                   ├──< (N) TB_APPROVAL_HISTORY >── TB_USER (처리자)
                                   ├──< (N) TB_ATTACHMENT
                                   └──< (N) TB_AUDIT_LOG (간접)
```

### 5.4 인덱스 전략

| 테이블 | 인덱스명 | 컬럼 | 유형 | 목적 |
|--------|----------|------|------|------|
| TB_DOCUMENT | IDX_DOC_DRAFTER | DRAFTER_EMP_NO | B-Tree | 기안자별 조회 최적화 |
| TB_DOCUMENT | IDX_DOC_STATUS | STATUS | B-Tree | 상태별 필터링 |
| TB_DOCUMENT | IDX_DOC_SUBMITTED | SUBMITTED_AT | B-Tree | 기간별 조회 |
| TB_DOCUMENT | IDX_DOC_SEARCH | STATUS, DRAFTER_EMP_NO, SUBMITTED_AT DESC | 복합 | 검색 쿼리 커버링 |
| TB_APPROVAL_LINE | IDX_LINE_DOC | DOC_ID | B-Tree | 문서별 결재선 조회 |
| TB_APPROVAL_LINE | IDX_LINE_EMP_STATUS | EMP_NO, STATUS | 복합 | 사용자별 대기 결재 |
| TB_APPROVAL_HISTORY | IDX_HIST_DOC_TIME | DOC_ID, CREATED_AT DESC | 복합 | 타임라인 조회 |
| TB_AUDIT_LOG | IDX_AUDIT_EMP_TIME | EMP_NO, CREATED_AT DESC | 복합 | 사용자별 감사조회 |
| TB_AUDIT_LOG | IDX_AUDIT_ACTION_TIME | ACTION_TYPE, CREATED_AT DESC | 복합 | 작업유형별 조회 |
| TB_ATTACHMENT | IDX_ATTACH_DOC | DOC_ID | B-Tree | 문서별 첨부파일 |

**인덱스 설계 원칙**:
- 읽기 중심 워크로드에 최적화 (결재 시스템 특성상 READ > WRITE)
- 복합 인덱스는 선택도가 높은 컬럼을 앞에 배치
- TB_AUDIT_LOG는 INSERT 전용이므로 인덱스를 최소한으로 유지
- 파티셔닝: TB_AUDIT_LOG는 월간 RANGE 파티셔닝 고려 (5년 보관 시)

### 5.5 시퀀스 (ID 생성)

```sql
-- 문서 ID용 시퀀스 (DOC-YYYYMMDD-XXXXXX 형식은 Application에서 생성)
CREATE SEQUENCE SEQ_DOCUMENT NOCACHE;
CREATE SEQUENCE SEQ_APPROVAL_LINE NOCACHE;
CREATE SEQUENCE SEQ_APPROVAL_HISTORY NOCACHE;
CREATE SEQUENCE SEQ_AUDIT_LOG NOCACHE;
CREATE SEQUENCE SEQ_ATTACHMENT NOCACHE;
CREATE SEQUENCE SEQ_SYNC_LOG NOCACHE;
```

---

## 6. 기술스택 결정

### 6.1 기술스택 목록

| 분류 | 기술 | 버전 | 선정 사유 | 폐쇄망 호환성 |
|------|------|------|-----------|---------------|
| **언어** | Java | 17 (LTS) | 장기지원 버전, Spring Boot 3.x 호환, 행정망 표준 | ✅ 내부 JDK 제공 |
| **프레임워크** | Spring Boot | 3.2.x | 생산성, 생태계, 행정망 표준 | ✅ 내부 Nexus 제공 |
| **보안** | Spring Security | 6.x (Boot 동봉) | JWT 통합 용이, RBAC 지원 | ✅ |
| **ORM** | Spring Data JPA (Hibernate) | 6.x | 생산성, 타입 안전성, 감사로그 연동 | ✅ |
| **DB** | Oracle | 19c | 기존 인사DB와 동일, 기관 표준 | ✅ 기존 인프라 |
| **JDBC Driver** | ojdbc11 | 19.x | Oracle 19c 공식 드라이버 | ✅ 내부 저장소 |
| **Connection Pool** | HikariCP | 5.x (Boot 동봉) | 성능 우수, 기본 풀 | ✅ |
| **JWT** | jjwt (JSON Web Token) | 0.12.x | 경량, 유지보수 활발, Apache 2.0 | ✅ 내부 저장소 |
| **API 문서** | SpringDoc OpenAPI | 2.x | Swagger UI 자동 생성, MIT | ✅ |
| **파일 처리** | Spring MVC Multipart | (Boot 동봉) | 표준 파일 업로드 | ✅ |
| **PDF 생성** | OpenPDF | 2.x | LGPL/MPL, iText 포크, 폐쇄망 적합 | ✅ 내부 저장소 |
| **빌드** | Maven | 3.9+ | 행정망 표준, 의존성 관리 | ✅ 내부 Nexus |
| **테스트** | JUnit 5 + Mockito | 5.x / 5.x | 표준 테스트 프레임워크 | ✅ |
| **로그** | Logback | 1.4.x (Boot 동봉) | 기본 로깅, 파일 롤링 | ✅ |
| **스케줄링** | Spring @Scheduled | (Boot 동봉) | 내부 스케줄러, 외부 의존 없음 | ✅ |

### 6.2 선정 사유 상세

**Java 17**:
- LTS(Long Term Support) 버전으로 2029년까지 지원
- Spring Boot 3.x 최소 요구사항
- Record, Sealed Class, Pattern Matching 등 생산성 향상 기능 포함
- 폐쇄망 내부 JDK 17 빌드 제공 확인 필요

**Spring Boot 3.x**:
- Java 17 기반, Jakarta EE 9+ 마이그레이션 완료
- Auto-configuration으로 설정 최소화
- Actuator로 헬스체크, 메트릭 제공
- 내부 Nexus에 Spring Boot BOM 제공 확인 필요

**jjwt (JWT)**:
- Apache 2.0 라이선스 (GPL 아님)
- HS256/RS256 지원
- 경량 라이브러리, 의존성 최소화
- 폐쇄망 내부 Maven 미러에서 제공 가능

**OpenPDF (PDF 출력)**:
- iText의 LGPL/MPL 포크 버전
- 한글 폰트 지원 (폰트 파일 경로 설정)
- 상업적 사용 가능 (MPL 2.0)
- 폐쇄망 내부 저장소에 배포 가능

### 6.3 폐쇄망 호환성 확인 체크리스트

- [ ] Java 17 JDK 내부 저장소 존재 확인
- [ ] Spring Boot 3.2.x BOM 내부 Nexus 존재 확인
- [ ] ojdbc11 드라이버 내부 저장소 존재 확인
- [ ] jjwt 0.12.x 내부 Nexus 존재 확인
- [ ] SpringDoc OpenAPI 2.x 내부 Nexus 존재 확인
- [ ] OpenPDF 2.x 내부 Nexus 존재 확인
- [ ] JUnit 5, Mockito 내부 저장소 존재 확인
- [ ] Maven settings.xml 내부 Nexus 미러 설정

---

## 7. 보안 설계

### 7.1 인증 (Authentication)

#### 7.1.1 인증 방식
- **사번 기반 인증**: 인사DB의 사원번호 + 비밀번호로 인증
- **비밀번호 저장**: BCrypt (Salt + 12 Round)
- **세션 관리**: JWT 기반 세션리스 (Stateless)

#### 7.1.2 JWT 토큰 구조
```json
{
  "header": { "alg": "HS256", "typ": "JWT" },
  "payload": {
    "sub": "EMP001234",
    "empName": "홍길동",
    "deptCode": "DEPT001",
    "roles": ["DRAFTER", "APPROVER"],
    "iat": 1712000000,
    "exp": 1712001800
  }
}
```

#### 7.1.3 토큰 관리
| 토큰 | 만료시간 | 저장 위치 | 용도 |
|------|----------|-----------|------|
| Access Token | 30분 | 클라이언트 메모리 | API 요청 인증 |
| Refresh Token | 8시간 | 클라이언트 HttpOnly Cookie | Access Token 재발급 |

#### 7.1.4 로그인 보안
- 로그인 실패 5회 시 계정 30분 잠금
- 잠금 해제 시간 자동 관리 (`LOGIN_LOCK_TIME`)
- 비밀번호 90일 주기 변경 강제 (향후 구현)
- 세션 타임아웃: 30분 (Access Token 만료와 동일)

### 7.2 인가 (Authorization)

#### 7.2.1 역할 정의

| 역할 | 코드 | 권한 |
|------|------|------|
| 시스템 관리자 | `SYSTEM_ADMIN` | 전체 시스템 관리, 동기화, 사용자 관리 |
| 조직 관리자 | `ORG_ADMIN` | 부서/결재선 템플릿 관리 |
| 결재자 | `APPROVER` | 결재 승인/반려, 본인 문서 조회 |
| 기안자 | `DRAFTER` | 문서 작성/상신/수정, 본인 문서 조회 |
| 조회자 | `VIEWER` | 문서 조회만 (결재 권한 없음) |

#### 7.2.2 인가 구현
- **API 수준**: `@PreAuthorize("hasRole('APPROVER')")`
- **데이터 수준**: Service 레이어에서 문서 접근 권한 검증
  ```java
  // 예: 문서 조회 시 권한 확인
  if (!document.isAccessibleBy(currentEmpNo)) {
      throw new AccessDeniedException();
  }
  ```

#### 7.2.3 데이터 접근 제어 규칙
| 데이터 | 접근 가능자 |
|--------|-------------|
| 결재 문서 | 기안자, 결재자, 참조자, SYSTEM_ADMIN |
| 결재 이력 | 문서 접근 권한자 |
| 첨부파일 | 문서 접근 권한자 |
| 조직도 | 모든 인증 사용자 |
| 감사로그 | SYSTEM_ADMIN만 |

### 7.3 데이터 보호

#### 7.3.1 암호화 범위
| 데이터 | 암호화 여부 | 방식 | 비고 |
|--------|-------------|------|------|
| 비밀번호 | ✅ | BCrypt (Salt + 12 Round) | 단방향 해시 |
| 결재문서 내용 | ❌ | 암호화 불필요 | 접근제어로 보호 |
| 개인정보 (연락처) | ✅ | AES-256 (필요 시) | 기관 정책 따름 |
| 첨부파일 | ❌ | 파일시스템 권한으로 보호 | 접근제어로 충분 |
| JWT Secret | ✅ | 환경변수/설정파일 암호화 | KMS 연동 권장 |
| DB 연결 정보 | ✅ | Jasypt 또는 환경변수 | 설정 파일 평문 금지 |

#### 7.3.2 전송 보안
- Web Server 진입점: TLS 1.2+ (HTTPS)
- 내부 App Server ↔ DB: Oracle Net 암호화 (선택, 기관 정책 따름)
- JWT: 서명 검증으로 위변조 방지

### 7.4 감사 로그 정책

#### 7.4.1 기록 대상
| 작업 유형 | 기록 항목 |
|-----------|-----------|
| 로그인/로그아웃 | 사번, IP, 일시, 성공/실패 |
| 문서 CRUD | 문서ID, 작업자, 일시, 변경 전/후 |
| 결재 처리 | 문서ID, 결재자, 처리결과, 의견, 일시 |
| 결재선 변경 | 문서ID, 작업자, 변경 결재선, 일시 |
| 파일 업로드/삭제 | 문서ID, 파일명, 작업자, 일시 |
| HR 동기화 | 동기화ID, 처리건수, 성공/실패, 일시 |

#### 7.4.2 감사로그 보호
- **INSERT 전용**: TB_AUDIT_LOG 테이블에 UPDATE/DELETE 권한 부여 금지
- **DB 권한 분리**: 애플리케이션 계정은 INSERT만, 감사전용 계정은 SELECT
- **보존 기간**: 5년 (행정기록물 관리 기준)
- **아카이브**: 5년 경과 데이터는 별도 아카이브 테이블로 이동

#### 7.4.3 구현 방식
- **AOP 기반**: `@AuditLog` 어노테이션이 붙은 Service 메서드 자동 로깅
- **Async 처리**: 감사로그 기록은 별도 스레드 풀에서 비동기 처리 (성능 영향 최소화)
- **IP 주소**: `HttpServletRequest.getRemoteAddr()` 에서 추출

### 7.5 보안 취약점 대응

| 취약점 | 대응 방안 |
|--------|-----------|
| SQL Injection | JPA Parameterized Query 사용, Native Query 시 Named Parameter |
| XSS | REST API이므로 응답 JSON에 HTML 인코딩 불필요. 프론트엔드에서 처리 |
| CSRF | 세션리스 JWT 방식이므로 CSRF 토큰 불필요 |
| IDOR | 모든 문서 접근 API에서 소유자/권한 검증 |
| 파일 업로드 취약점 | 파일 확장자 검증, MIME 타입 검증, 저장명 UUID 랜덤화 |
| 과도한 요청 | Rate Limiting (Nginx 수준 또는 Spring Filter) |
| 로그 인젝션 | 로그 기록 시 개행문자 제거, 파라미터화 |

---

## 8. 비기능 요구사항

### 8.1 성능 목표

| 지표 | 목표값 | 측정 방법 | 비고 |
|------|--------|-----------|------|
| API 응답시간 (P95) | 2초 이내 | APM (Spring Boot Actuator + Micrometer) | 사용자 요구사항 반영 |
| API 응답시간 (P99) | 3초 이내 | APM | |
| 동시 사용자 | 200명 | 부하 테스트 (Gatling / JMeter) | 전사 1,000명 중 |
| 일일 결재 처리량 | 3,000건 | 로그 집계 | 동시 200명 기준 |
| 시스템 가용성 (SLA) | 99.9% | 모니터링 (월간 업타임) | 연간 8.76시간 이하 |
| 대용량 기안문 | 100KB 이내 | 요청 크기 검증 | CONTENT CLOB로 처리 |

### 8.2 성능 최적화 전략

| 영역 | 전략 |
|------|------|
| **DB 쿼리** | N+1 문제 방지 (JOIN FETCH, EntityGraph), 인덱스 활용 |
| **커넥션 풀** | HikariCP 최대 50, 최소 10, 유휴 타임아웃 10분 |
| **페이징** | 대용량 목록 조회 시 Cursor-based 또는 Offset 페이징 |
| **캐시** | 부서/직급 마스터 데이터는 애플리케이션 캐시 (Caffeine, TTL 1시간) |
| **파일 I/O** | NIO 기반 비동기 읽기, 청크 전송 (대용량 다운로드) |
| **감사로그** | Async 스레드 풀 (5개)에서 비동기 기록 |

### 8.3 가용성

| 항목 | 전략 |
|------|------|
| **무중단 배포** | Blue-Green 또는 Rolling Update (운영환경 구성에 따름) |
| **헬스체크** | Spring Boot Actuator `/actuator/health` |
| **DB 장애** | Oracle Data Guard (Standby DB) — 기관 인프라에 따름 |
| **파일 저장소** | 로컬 디스크 RAID 구성, 정기 백업 |
| **모니터링** | Actuator + Prometheus + Grafana (내부 구축) |

### 8.4 확장성

| 영역 | 확장 방안 |
|------|-----------|
| **API 서버** | Stateless 설계로 수평 확장 가능 (다중 인스턴스) |
| **DB** | Oracle RAC / Data Guard — 기관 규모에 따라 |
| **파일 저장소** | 향후 NFS/SAN 공유 저장소로 이전 가능 |
| **결재선** | 현재 단일 결재자, 향후 다단계 결재선 확장 가능 (LINE_ORDER 기반) |

### 8.5 Graceful Degradation (점진적 기능 저하)

| 장애 시나리오 | 대응 전략 |
|---------------|-----------|
| **인사DB 연결 끊김** | 마지막 동기화 데이터로 운영. 결재선 지정 시 로컬 캐시 사용자 목록 사용. 연결 복구 후 자동 재동기화 |
| **파일 저장소 장애** | 첨부파일 없이 결재 진행 가능. 업로드 시 에러 메시지 반환 |
| **DB 읽기 지연** | 읽기 전용 복제 DB 활용 (구성 시). 캐시된 마스터 데이터 활용 |

### 8.6 운영 요구사항

| 항목 | 요구사항 |
|------|----------|
| **로그 관리** | 애플리케이션 로그: 파일 롤링 (일별, 30일 보관), 크기 제한 100MB |
| **백업** | DB: 일일 전체 백업 + 아카이브 로그. 파일: 일일 증분 백업 |
| **모니터링** | CPU, Memory, Disk, DB 커넥션, API 응답시간, 에러율 |
| **알림** | 시스템 장애 시 관리자 이메일/메신저 알림 (내부 연동) |
| **문서 보관** | 완료된 결재 문서 10년 보관 (행정기록물 기준) |

---

## 부록 A: 결재 상태 전이표

| 현재 상태 | 상신 | 승인 | 반려 | 취소 | 수거 | 수정 | 비고 |
|-----------|------|------|------|------|------|------|------|
| TEMP | → DRAFT | - | - | - | - | ✅ | 임시저장 중 |
| DRAFT | → SUBMITTED | - | - | - | - | ✅ | 작성완료 |
| SUBMITTED | - | → IN_PROGRESS | - | → CANCELLED | - | - | 상신됨 |
| IN_PROGRESS | - | → APPROVED | → REJECTED | - | - | - | 결재진행 중 |
| APPROVED | - | - | - | - | - | - | 완료 (종단) |
| REJECTED | - | - | - | - | → RETURNED | - | 반려됨 |
| RETURNED | → DRAFT | - | - | - | - | ✅ | 수거됨 |
| CANCELLED | - | - | - | - | - | - | 취소 (종단) |

## 부록 B: 환경변수 목록

| 변수명 | 설명 | 예시 | 필수 |
|--------|------|------|------|
| `DB_URL` | 결재 DB JDBC URL | `jdbc:oracle:thin:@db-host:1521:APPROVAL` | ✅ |
| `DB_USERNAME` | 결재 DB 사용자 | `approval_admin` | ✅ |
| `DB_PASSWORD` | 결재 DB 비밀번호 | `***` | ✅ |
| `HR_DB_URL` | 인사 DB JDBC URL | `jdbc:oracle:thin:@hr-host:1521:HRDB` | ✅ |
| `HR_DB_USERNAME` | 인사 DB 읽기전용 사용자 | `hr_reader` | ✅ |
| `HR_DB_PASSWORD` | 인사 DB 비밀번호 | `***` | ✅ |
| `JWT_SECRET` | JWT 서명 키 (32자 이상) | `my-secret-key-must-be-at-least-32-characters` | ✅ |
| `JWT_ACCESS_EXPIRATION` | Access Token 만료 (ms) | `1800000` (30분) | |
| `JWT_REFRESH_EXPIRATION` | Refresh Token 만료 (ms) | `28800000` (8시간) | |
| `FILE_UPLOAD_PATH` | 첨부파일 저장 경로 | `/data/approval/uploads` | ✅ |
| `FILE_MAX_SIZE` | 최대 파일 크기 (bytes) | `52428800` (50MB) | |
| `HR_SYNC_CRON` | HR 동기화 Cron 표현식 | `0 0 2 * * *` (매일 02:00) | |
| `SERVER_PORT` | 애플리케이션 포트 | `8080` | |
| `LOG_LEVEL` | 로그 레벨 | `INFO` | |

## 부록 C: 개정 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| 1.0 | 2026-04-02 | 초기 설계 문서 작성 | Solideo AI Architect |
