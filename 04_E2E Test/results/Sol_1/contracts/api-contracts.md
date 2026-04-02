# API Contracts — 내부결재시스템

> **버전**: 1.0  
> **작성일**: 2026-04-02  
> **Base URL**: `/api/v1`

---

## 1. 인증 API

### POST /auth/login
- **설명**: 사번/비밀번호로 로그인
- **Request Body**:
  ```json
  { "empNo": "string", "password": "string" }
  ```
- **Response 200**:
  ```json
  { "accessToken": "string", "refreshToken": "string", "expiresIn": 1800, "user": { "empNo": "string", "empName": "string", "deptCode": "string", "roles": ["string"] } }
  ```
- **Response 401**: `{ "code": "AUTH_FAILED", "message": "사번 또는 비밀번호가 올바르지 않습니다." }`
- **Response 423**: `{ "code": "ACCOUNT_LOCKED", "message": "계정이 잠겼습니다.", "unlockTime": "2026-04-02T10:30:00" }`

### POST /auth/logout
- **설명**: 로그아웃 (토큰 무효화)
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: `{ "message": "로그아웃되었습니다." }`

### POST /auth/refresh
- **설명**: 토큰 재발급
- **Request Body**: `{ "refreshToken": "string" }`
- **Response 200**: `{ "accessToken": "string", "expiresIn": 1800 }`

---

## 2. 결재 문서 API

### POST /documents
- **설명**: 결재 문서 생성 (임시저장)
- **Auth**: DRAFTER 이상
- **Request Body**:
  ```json
  {
    "title": "string (required, max 500)",
    "content": "string (required, max CLOB)",
    "docType": "string (required)",
    "deptCode": "string (required)"
  }
  ```
- **Response 201**: `{ "docId": "DOC-20260402-000001", "status": "TEMP", "createdAt": "..." }`

### GET /documents/{docId}
- **설명**: 문서 상세 조회
- **Auth**: 기안자, 결재자, 참조자, VIEWER 이상
- **Response 200**: Document 상세 + ApprovalLine 목록 + Attachment 목록

### PUT /documents/{docId}
- **설명**: 문서 수정 (TEMP, DRAFT, RETURNED 상태만)
- **Auth**: 기안자
- **Request Body**: POST /documents 와 동일
- **Response 200**: `{ "docId": "string", "status": "string", "updatedAt": "..." }`

### DELETE /documents/{docId}
- **설명**: 문서 삭제 (TEMP 상태만)
- **Auth**: 기안자
- **Response 204**: No Content

### POST /documents/{docId}/submit
- **설명**: 문서 상신
- **Auth**: 기안자
- **Request Body**:
  ```json
  {
    "approvalLine": [
      { "lineType": "APPROVER", "empNo": "string", "lineOrder": 1 }
    ],
    "refereeLine": [
      { "lineType": "REFEREE", "empNo": "string" }
    ]
  }
  ```
- **Response 200**: `{ "docId": "string", "status": "IN_PROGRESS", "submittedAt": "..." }`

### POST /documents/{docId}/cancel
- **설명**: 문서 취소 (상신 후 즉시)
- **Auth**: 기안자
- **Response 200**: `{ "docId": "string", "status": "CANCELLED" }`

### GET /documents
- **설명**: 문서 목록 조회 (검색/필터)
- **Auth**: 인증 사용자
- **Query Parameters**:
  - `status`: 결재 상태 (optional)
  - `draftEmpNo`: 기안자 사번 (optional)
  - `startDate`: 시작일 (YYYY-MM-DD, optional)
  - `endDate`: 종료일 (YYYY-MM-DD, optional)
  - `keyword`: 제목 키워드 (optional)
  - `page`: 페이지 번호 (default: 0)
  - `size`: 페이지 크기 (default: 20, max: 100)
- **Response 200**:
  ```json
  {
    "content": [{ "docId": "string", "title": "string", "status": "string", "docType": "string", "draftEmpName": "string", "submittedAt": "..." }],
    "totalElements": 150,
    "totalPages": 8,
    "page": 0,
    "size": 20
  }
  ```

---

## 3. 결재 처리 API

### POST /documents/{docId}/approve
- **설명**: 결재 승인
- **Auth**: 현재 순서의 결재자 (APPROVER)
- **Request Body**: `{ "comment": "string (optional, max 2000)" }`
- **Response 200**: `{ "docId": "string", "status": "APPROVED" | "IN_PROGRESS", "processedAt": "..." }`

### POST /documents/{docId}/reject
- **설명**: 결재 반려
- **Auth**: 현재 순서의 결재자 (APPROVER)
- **Request Body**: `{ "comment": "string (required, max 2000)" }`
- **Response 200**: `{ "docId": "string", "status": "REJECTED", "processedAt": "..." }`

### POST /documents/{docId}/return
- **설명**: 반려 문서 수거 (기안자가 수정하기 위해)
- **Auth**: 기안자
- **Response 200**: `{ "docId": "string", "status": "RETURNED" }`

---

## 4. 결재함 API

### GET /inbox
- **설명**: 내가 결재할 문서 목록 (대기 중)
- **Auth**: 인증 사용자
- **Query**: `page`, `size`
- **Response 200**: Paginated Document 목록

### GET /outbox
- **설명**: 내가 기안한 문서 목록
- **Auth**: 인증 사용자
- **Query**: `status`, `startDate`, `endDate`, `keyword`, `page`, `size`
- **Response 200**: Paginated Document 목록

### GET /referenced
- **설명**: 참조된 문서 목록
- **Auth**: 인증 사용자
- **Query**: `page`, `size`
- **Response 200**: Paginated Document 목록

---

## 5. 결재 이력 API

### GET /documents/{docId}/history
- **설명**: 문서별 결재 이력 타임라인
- **Auth**: 문서 접근 권한자
- **Response 200**:
  ```json
  [
    { "historyId": "string", "empName": "string", "action": "SUBMIT", "comment": null, "createdAt": "..." },
    { "historyId": "string", "empName": "string", "action": "APPROVE", "comment": "확인했습니다.", "createdAt": "..." }
  ]
  ```

### GET /documents/{docId}/approval-line
- **설명**: 문서별 결재선 현황
- **Auth**: 문서 접근 권한자
- **Response 200**:
  ```json
  [
    { "lineId": "string", "lineType": "APPROVER", "lineOrder": 1, "empName": "string", "status": "APPROVED", "processedAt": "..." },
    { "lineId": "string", "lineType": "REFEREE", "empName": "string", "status": "PENDING" }
  ]
  ```

---

## 6. 첨부파일 API

### POST /documents/{docId}/attachments
- **설명**: 첨부파일 업로드
- **Auth**: 기안자
- **Content-Type**: multipart/form-data
- **Request**: `file` (max 50MB)
- **Response 201**: `{ "attachId": "string", "originalName": "string", "fileSize": 102400 }`

### DELETE /documents/{docId}/attachments/{attachId}
- **설명**: 첨부파일 삭제
- **Auth**: 기안자
- **Response 204**: No Content

### GET /documents/{docId}/attachments/{attachId}/download
- **설명**: 첨부파일 다운로드
- **Auth**: 문서 접근 권한자
- **Response 200**: 파일 스트림

---

## 7. 조직/사용자 조회 API

### GET /departments
- **설명**: 부서 목록 조회 (트리 구조)
- **Auth**: 인증 사용자
- **Response 200**: 부서 트리 배열

### GET /users/search
- **설명**: 사용자 검색 (결재선 지정용)
- **Auth**: 인증 사용자
- **Query**: `keyword` (이름/사번), `deptCode`
- **Response 200**: `{ "empNo": "string", "empName": "string", "deptName": "string", "positionName": "string" }` 배열

---

## 8. 동기화 API (관리자)

### POST /sync/hr
- **설명**: 인사DB 수동 동기화
- **Auth**: SYSTEM_ADMIN
- **Response 200**: `{ "syncId": "string", "status": "COMPLETED", "recordCount": 150 }`

### GET /sync/logs
- **설명**: 동기화 이력 조회
- **Auth**: SYSTEM_ADMIN
- **Response 200**: 동기화 이력 목록

---

## 9. 인증/인가 규칙 요약

| API 그룹 | 최소 역할 | 비고 |
|----------|-----------|------|
| /auth/* | PUBLIC | 로그인/로그아웃 |
| /documents (POST) | DRAFTER | 기안 권한 |
| /documents/{id} (GET) | 문서 관련자 | 기안자/결재자/참조자 |
| /documents/{id} (PUT/DELETE) | 기안자 | 상태 제한 있음 |
| /documents/{id}/submit | 기안자 | TEMP/DRAFT/RETURNED 상태만 |
| /documents/{id}/approve, /reject | 현재 결재자 | 본인 순서일 때만 |
| /inbox, /outbox, /referenced | 인증 사용자 | 본인 데이터만 |
| /departments, /users/search | 인증 사용자 | 조직도 조회 |
| /sync/* | SYSTEM_ADMIN | 관리자 전용 |
