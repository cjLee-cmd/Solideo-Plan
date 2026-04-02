# Tasks — 내부결재시스템

> **생성일**: 2026-04-02  
> **참조**: design.md, spec.md, plan.md

---

## Phase 1: Setup

- [ ] [T001] [P] 프로젝트 초기화 — Maven pom.xml 생성 (Spring Boot 3.2.x, Java 17, Oracle, JPA, Security, jjwt, SpringDoc)
- [ ] [T002] [P] application.yml 설정 — DB 연결, JWT, 파일저장경로, 프로파일별 설정 (dev/prod)
- [ ] [T003] [P] 패키지 구조 생성 — config, security, controller, service, repository, entity, dto, exception, audit, scheduler, file
- [ ] [T004] [P] 데이터베이스 스키마 생성 — schema.sql 작성 (TB_USER, TB_DEPARTMENT, TB_POSITION, TB_DOCUMENT, TB_APPROVAL_LINE, TB_APPROVAL_HISTORY, TB_ATTACHMENT, TB_AUDIT_LOG, TB_SYNC_LOG, TB_DOCUMENT_TEMPLATE)

## Phase 2: Foundational

- [ ] [T005] [P] [US5] JPA Entity 생성 — User, Department, Position 엔티티 (src/main/java/com/solideo/approval/entity/)
- [ ] [T006] [P] [US5] JPA Repository 생성 — UserRepository, DepartmentRepository, PositionRepository
- [ ] [T007] [P] [US5] SecurityConfig 설정 — Spring Security 6.x, JWT 필터 체인, CORS/CSRF 설정
- [ ] [T008] [P] [US5] JwtTokenProvider 구현 — 토큰 생성, 검증, 파싱 (jjwt 기반)
- [ ] [T009] [P] [US5] JwtAuthenticationFilter 구현 — HTTP 요청에서 JWT 추출 및 인증
- [ ] [T010] [P] [US5] CustomUserDetailsService 구현 — 사번 기반 UserDetails 로드
- [ ] [T011] [P] 전역 예외 처리 — GlobalExceptionHandler, 커스텀 예외 클래스들 (ApprovalException, DocumentNotFoundException, InvalidApprovalStateException, FileStorageException)
- [ ] [T012] [P] 공통 응답 DTO — ApiResponse<T>, PageResponse<T> (src/main/java/com/solideo/approval/dto/response/)
- [ ] [T013] [P] FileStorageConfig 및 FileStorageService 구현 — 로컬 파일 저장/조회/삭제
- [ ] [T014] [P] AuditLogAspect 및 AuditLogService 구현 — AOP 기반 감사로그 자동 기록

## Phase 3: US1 — 기안작성

- [ ] [T015] [US1] Document, Attachment JPA Entity 생성
- [ ] [T016] [US1] DocumentRepository, AttachmentRepository 생성
- [ ] [T017] [US1] DTO 생성 — DocumentCreateRequest, DocumentResponse (src/main/java/com/solideo/approval/dto/)
- [ ] [T018] [US1] DocumentService 구현 — 문서 생성(TEMP), 수정, 삭제, 상태 전이 검증
- [ ] [T019] [US1] DocumentController 구현 — POST/GET/PUT/DELETE /api/v1/documents
- [ ] [T020] [US1] AttachmentController 구현 — 첨부파일 업로드/다운로드/삭제
- [ ] [T021] [US1] 단위테스트 — DocumentServiceTest (생성, 수정, 삭제, 상태전이에러)
- [ ] [T022] [US1] 단위테스트 — DocumentControllerTest (REST API 검증)

## Phase 4: US2 — 결재선지정

- [ ] [T023] [US2] ApprovalLine JPA Entity 생성
- [ ] [T024] [US2] ApprovalLineRepository 생성
- [ ] [T025] [US2] DTO 생성 — DocumentSubmitRequest, ApprovalLineResponse
- [ ] [T026] [US2] DocumentService.submit() 구현 — 결재선 지정 및 상신 (스냅샷 방식)
- [ ] [T027] [US2] 결재선 검증 로직 — 순환 참조 감지, 중복 결재자 체크, 퇴사자 체크
- [ ] [T028] [US2] 단위테스트 — DocumentService.submit() 테스트 (결재선 검증 포함)

## Phase 5: US3 — 승인반려

- [ ] [T029] [US3] ApprovalHistory JPA Entity 생성
- [ ] [T030] [US3] ApprovalHistoryRepository 생성
- [ ] [T031] [US3] DTO 생성 — ApprovalActionRequest
- [ ] [T032] [US3] ApprovalService 구현 — 승인, 반려, 반려취소(수거) 처리
- [ ] [T033] [US3] ApprovalController 구현 — POST /api/v1/documents/{docId}/approve, /reject, /return
- [ ] [T034] [US3] 결재 상태 전이 로직 — IN_PROGRESS → APPROVED/REJECTED, REJECTED → RETURNED
- [ ] [T035] [US3] 동시성 제어 — SELECT FOR UPDATE 기반 비관적 락
- [ ] [T036] [US3] 단위테스트 — ApprovalServiceTest (승인, 반려, 상태전이, 동시성)
- [ ] [T037] [US3] 단위테스트 — ApprovalControllerTest (REST API 검증)

## Phase 6: US4 — 이력조회

- [ ] [T038] [US4] DTO 생성 — DocumentListResponse, DocumentSearchRequest
- [ ] [T039] [US4] DocumentService.search() 구현 — 상태/기안자/기간/키워드 필터링 + 페이징
- [ ] [T040] [US4] ApprovalService.getHistory() 구현 — 결재 이력 타임라인 조회
- [ ] [T041] [US4] ApprovalService.getApprovalLine() 구현 — 결재선 현황 조회
- [ ] [T042] [US4] DocumentController 구현 — GET /api/v1/documents (검색)
- [ ] [T043] [US4] InboxController 구현 — GET /api/v1/inbox, /outbox, /referenced
- [ ] [T044] [US4] 단위테스트 — DocumentService.search() 테스트 (필터링, 페이징)

## Phase 7: US5 — 인사DB 연동

- [ ] [T045] [US5] HR DataSource 설정 — 별도 DataSource (읽기전용)
- [ ] [T046] [US5] HrSyncService 구현 — 인사DB에서 조직/직원 정보 조회 및 로컬 DB 반영
- [ ] [T047] [US5] HrSyncScheduler 구현 — @Scheduled 기반 매일 02:00 자동 동기화
- [ ] [T048] [US5] SyncLog Entity 및 Repository 생성
- [ ] [T049] [US5] SyncController 구현 — POST /api/v1/sync/hr (수동), GET /api/v1/sync/logs
- [ ] [T050] [US5] OrganizationController 구현 — GET /api/v1/departments, /api/v1/users/search
- [ ] [T051] [US5] 단위테스트 — HrSyncServiceTest (동기화 로직)

## Phase 8: US6 — 결재 문서 템플릿 (P3)

- [ ] [T052] [US6] DocumentTemplate Entity 및 Repository 생성
- [ ] [T053] [US6] Template CRUD Service 및 Controller 구현

## Phase 9: Polish & Cross-cutting

- [ ] [T054] SwaggerConfig 설정 — SpringDoc OpenAPI 설정, API 문서 자동 생성
- [ ] [T055] 통합테스트 — AuthControllerTest (로그인/로그아웃/토큰재발급)
- [ ] [T056] 통합테스트 — 전체 API 플로우 테스트 (기안 → 상신 → 승인 → 완료)
- [ ] [T057] application-dev.yml, application-prod.yml 환경별 설정 분리
- [ ] [T058] data.sql 초기 데이터 — 테스트용 사용자, 부서, 직급 데이터
- [ ] [T059] 로깅 설정 — Logback 파일 롤링 (일별, 30일 보관, 100MB 제한)
- [ ] [T060] Actuator 설정 — /actuator/health, /actuator/metrics 헬스체크 및 메트릭
