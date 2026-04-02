# 체크리스트 — 보안 (Security)

> **생성일**: 2026-04-02  
> **참조**: design.md §7, constitution.md §2

---

## 인증 (Authentication)

- [ ] CHK-SEC-001 Are authentication requirements defined for login flow? [design.md §7.1.1]
- [ ] CHK-SEC-002 Is JWT token expiration quantified with specific time values? [design.md §7.1.3: Access 30분, Refresh 8시간]
- [ ] CHK-SEC-003 Are password storage requirements specified with hashing algorithm? [design.md §7.1.1: BCrypt 12 Round]
- [ ] CHK-SEC-004 Are account lockout requirements defined with specific thresholds? [design.md §7.1.4: 5회 실패 시 30분 잠금]
- [ ] CHK-SEC-005 Is session timeout quantified? [design.md §7.1.4: 30분]
- [ ] CHK-SEC-006 Are token refresh requirements defined? [design.md §7.1.3, §4.4]

## 인가 (Authorization)

- [ ] CHK-SEC-007 Are role definitions specified with specific permissions per role? [design.md §7.2.1]
- [ ] CHK-SEC-008 Is API-level authorization specified for each endpoint? [design.md §4.3 Auth column]
- [ ] CHK-SEC-009 Are data-level access control rules defined per entity? [design.md §7.2.3]
- [ ] CHK-SEC-010 Is the authorization implementation approach specified? [design.md §7.2.2: @PreAuthorize]

## 데이터 보호 (Data Protection)

- [ ] CHK-SEC-011 Is encryption scope clearly defined per data type? [design.md §7.3.1]
- [ ] CHK-SEC-012 Is password encryption algorithm specified? [design.md §7.3.1: BCrypt]
- [ ] CHK-SEC-013 Are DB credential protection requirements defined? [design.md §7.3.1: Jasypt/환경변수]
- [ ] CHK-SEC-014 Is transmission security specified? [design.md §7.3.2: TLS 1.2+]
- [ ] CHK-SEC-015 Is JWT secret key protection defined? [design.md §7.3.1: 환경변수/KMS]

## 감사로그 (Audit Log)

- [ ] CHK-SEC-016 Are audit log recording targets fully specified? [design.md §7.4.1]
- [ ] CHK-SEC-017 Is audit log storage protection defined (INSERT-only)? [design.md §7.4.2]
- [ ] CHK-SEC-018 Is audit log retention period quantified? [design.md §7.4.2: 5년]
- [ ] CHK-SEC-019 Is the audit log implementation approach specified? [design.md §7.4.3: AOP + Async]

## 취약점 대응 (Vulnerability Mitigation)

- [ ] CHK-SEC-020 Are SQL injection countermeasures specified? [design.md §7.5: JPA Parameterized Query]
- [ ] CHK-SEC-021 Are file upload vulnerability countermeasures defined? [design.md §7.5: 확장자/MIME 검증, UUID 저장명]
- [ ] CHK-SEC-022 Are IDOR countermeasures specified? [design.md §7.5: 소유자/권한 검증]
- [ ] CHK-SEC-023 Is CSRF handling defined? [design.md §7.5: 세션리스 JWT → 불필요]
- [ ] CHK-SEC-024 Are rate limiting requirements defined? [design.md §7.5: Nginx/Spring Filter]
