# 체크리스트 — 요구사항 품질 (Requirements Quality)

> **생성일**: 2026-04-02  
> **참조**: spec.md, design.md, constitution.md

---

## Requirement Completeness

- [ ] CHK-REQ-001 Are all functional requirements from spec.md covered in design.md? [spec.md §5.1 FR-01~FR-13 → design.md §4.3]
- [ ] CHK-REQ-002 Are all user scenarios from spec.md addressed in API design? [spec.md §3 US1~US6 → design.md §4.3]
- [ ] CHK-REQ-003 Are all edge cases from spec.md addressed in design? [spec.md §4 E1~E8 → design.md §8.5, §7.5]
- [ ] CHK-REQ-004 Are success criteria from spec.md measurable in design? [spec.md §6 → design.md §8.1]

## Requirement Clarity

- [ ] CHK-REQ-005 Is "2초 이내" page response quantified with measurement method? [design.md §8.1: APM P95]
- [ ] CHK-REQ-006 Is "200명 동시 사용자" translated to system capacity? [design.md §8.1: 일일 3,000건 처리량]
- [ ] CHK-REQ-007 Is "100KB 이내" 기안문 크기 enforced in API? [design.md §4.5: VALIDATION_ERROR]

## Requirement Consistency

- [ ] CHK-REQ-008 Are document status values consistent between spec.md and design.md? [spec.md Clarifications vs design.md §1.4]
- [ ] CHK-REQ-009 Is the approval line structure consistent (단일 결재선)? [spec.md Clarifications → design.md §1.2 Out-of-Scope]
- [ ] CHK-REQ-010 Are search/filter conditions consistent between spec and API? [spec.md Clarifications → design.md §4.3 GET /documents]

## Acceptance Criteria Quality

- [ ] CHK-REQ-011 Are acceptance criteria technology-independent? [spec.md §6: 기술 비의존적 지표]
- [ ] CHK-REQ-012 Are acceptance criteria measurable? [spec.md §6: 70% 단축, 99.9%, 4.0/5.0 등]

## Scenario Coverage

- [ ] CHK-REQ-013 Are P1 scenarios fully covered (US1~US3)? [design.md §4.3: documents, approve, reject APIs]
- [ ] CHK-REQ-014 Are P2 scenarios fully covered (US4~US5)? [design.md §4.3: search, sync APIs]
- [ ] CHK-REQ-015 Are P3 scenarios addressed (US6)? [design.md §1.2: Out-of-Scope 명시]

## Edge Case Coverage

- [ ] CHK-REQ-016 Is long-term absence handling defined? [design.md §1.2: 대체결재자 - 향후 확장]
- [ ] CHK-REQ-017 Is system failure during approval handled? [design.md §8.5: Graceful Degradation]
- [ ] CHK-REQ-018 Is concurrent approval handling defined? [design.md §7.5: 비관적 락 언급 필요 - Gap]
- [ ] CHK-REQ-019 Is deceased employee in approval line handled? [design.md §8.5: HR 동기화 실패 대응]
- [ ] CHK-REQ-020 Is file size limit enforced? [design.md §4.5: FILE_SIZE_EXCEEDED, 50MB]
- [ ] CHK-REQ-021 Is circular approval line detection defined? [design.md §4.5: CIRCULAR_APPROVAL_LINE]
- [ ] CHK-REQ-022 Is HR DB disconnection handled? [design.md §8.5: Graceful Degradation]

## Non-Functional Requirements

- [ ] CHK-REQ-023 Are performance targets quantified? [design.md §8.1: P95 2초, P99 3초]
- [ ] CHK-REQ-024 Is availability target quantified? [design.md §8.1: 99.9% SLA]
- [ ] CHK-REQ-025 Is scalability approach defined? [design.md §8.4: Stateless 수평 확장]
- [ ] CHK-REQ-026 Is graceful degradation strategy defined? [design.md §8.5]

## Dependencies & Assumptions

- [ ] CHK-REQ-027 Are all external dependencies identified? [design.md §6.1: Oracle 19c, 내부 Nexus]
- [ ] CHK-REQ-028 Are closed-network compatibility checks documented? [design.md §6.3: 8개 항목 체크리스트]
- [ ] CHK-REQ-029 Are assumptions about HR DB availability documented? [design.md §8.5: HR DB 연결 끊김 시나리오]

## Ambiguities & Conflicts

- [ ] CHK-REQ-030 Is "단일 결재선" clearly distinguished from future multi-step? [design.md §1.2: Out-of-Scope 명시]
- [ ] CHK-REQ-031 Is the boundary between API-only and frontend clearly defined? [design.md §1.2: 프론트엔드 별도 프로젝트]
- [ ] CHK-REQ-032 Is "결재문서 내용 암호화 불필요" justified? [design.md §7.3.1: 접근제어로 대체]
