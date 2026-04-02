# 체크리스트 — DB 스키마 (Database Schema)

> **생성일**: 2026-04-02  
> **참조**: design.md §5, data-model.md

---

## Schema Completeness

- [ ] CHK-DB-001 Are all entities from spec.md represented as tables? [data-model.md: 10 tables]
- [ ] CHK-DB-002 Are all required columns defined with data types? [design.md §5.2]
- [ ] CHK-DB-003 Are primary keys defined for all tables? [design.md §5.2]
- [ ] CHK-DB-004 Are foreign key constraints defined for relationships? [design.md §5.2]
- [ ] CHK-DB-005 Are check constraints defined for enum-like columns? [design.md §5.2: CHK_DOC_STATUS, CHK_LINE_TYPE, etc.]

## Schema Consistency

- [ ] CHK-DB-006 Are column types consistent between related tables? [design.md §5.2: EMP_NO VARCHAR2(20) consistent]
- [ ] CHK-DB-007 Are timestamp columns consistent across tables? [design.md §5.2: CREATED_AT/UPDATED_AT pattern]
- [ ] CHK-DB-008 Are status values consistent between entity definition and DDL? [design.md §1.4 vs §5.2]

## Index Strategy

- [ ] CHK-DB-009 Are indexes defined for frequently queried columns? [design.md §5.4: 10 indexes]
- [ ] CHK-DB-010 Are composite indexes defined for multi-column searches? [design.md §5.4: IDX_DOC_SEARCH]
- [ ] CHK-DB-011 Is the index design rationale documented? [design.md §5.4: 읽기 중심 워크로드]

## Data Integrity

- [ ] CHK-DB-012 Are NOT NULL constraints applied to required fields? [design.md §5.2]
- [ ] CHK-DB-013 Are unique constraints defined where needed? [design.md §5.2: UQ_LINE_DOC_EMP]
- [ ] CHK-DB-014 Is the audit log table protected from modification? [design.md §5.2: INSERT-only 권한]

## Performance

- [ ] CHK-DB-015 Is the connection pool size specified? [design.md §8.2: HikariCP 최대 50]
- [ ] CHK-DB-016 Are sequences defined for ID generation? [design.md §5.5]
