# 체크리스트 — API (API Design)

> **생성일**: 2026-04-02  
> **참조**: design.md §4, contracts/api-contracts.md

---

## API Completeness

- [ ] CHK-API-001 Are all CRUD operations defined for Document entity? [design.md §4.3: POST/GET/PUT/DELETE]
- [ ] CHK-API-002 Are approval action endpoints (approve/reject/return) defined? [design.md §4.3]
- [ ] CHK-API-003 Are inbox/outbox/referenced endpoints defined? [design.md §4.3]
- [ ] CHK-API-004 Are attachment upload/download/delete endpoints defined? [design.md §4.3]
- [ ] CHK-API-005 Are authentication endpoints (login/logout/refresh) defined? [design.md §4.3]
- [ ] CHK-API-006 Are organization lookup endpoints defined? [design.md §4.3: /departments, /users/search]
- [ ] CHK-API-007 Are admin sync endpoints defined? [design.md §4.3: /sync/hr, /sync/logs]

## API Consistency

- [ ] CHK-API-008 Is a consistent response format defined for all endpoints? [design.md §4.2]
- [ ] CHK-API-009 Is error response format specified with error codes? [design.md §4.2, §4.5]
- [ ] CHK-API-010 Is API versioning strategy specified? [design.md §4.1: URL Path /api/v1]
- [ ] CHK-API-011 Is pagination approach defined? [design.md §4.1: Spring Data Pageable]

## API Security

- [ ] CHK-API-012 Is authentication requirement specified for each endpoint? [design.md §4.3 Auth column]
- [ ] CHK-API-013 Are authorization roles mapped to each endpoint? [design.md §4.3]
- [ ] CHK-API-014 Is JWT token handling specified for API requests? [design.md §4.4]

## API Validation

- [ ] CHK-API-015 Are request validation rules defined for document creation? [design.md §4.3: title max 500, content required]
- [ ] CHK-API-016 Are file size limits specified for upload? [design.md §4.5: 50MB]
- [ ] CHK-API-017 Are required fields identified for each request? [contracts/api-contracts.md]
- [ ] CHK-API-018 Are state transition constraints defined for document operations? [design.md §1.4]

## API Error Handling

- [ ] CHK-API-019 Are error codes defined for all failure scenarios? [design.md §4.5: 15 error codes]
- [ ] CHK-API-020 Is HTTP status code mapping specified? [design.md §4.5]
- [ ] CHK-API-021 Are error response details specified? [design.md §4.2: code, message, details]
