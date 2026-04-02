# E2E 테스트: Sol_7 문서생성

## 테스트 환경

| 항목 | 값 |
|------|-----|
| IDE | opencode CLI (`opencode run`) |
| 모델 (폐쇄망) | oss-120b |
| 모델 (인터넷망 테스트) | `opencode/qwen3.6-plus-free` 또는 `github-copilot/gpt-4o` |
| 테스트 디렉토리 | `/tmp/e2e_sol7` |

### 사전 준비: 문서 생성 원본 데이터

```bash
mkdir -p /tmp/e2e_sol7/90_Result_Doc
cd /tmp/e2e_sol7 && git init

# 이전 단계 산출물(요약본) 준비 — 문서 생성의 원본 데이터
cat > 90_Result_Doc/design.md << 'MD'
# 출장관리시스템 설계서
## 1. 프로젝트 개요
- 프로젝트명: 출장관리시스템
- 목적: 출장 신청~정산 자동화
## 2. 아키텍처 설계
- 3-Tier: Spring Boot + MyBatis + Oracle
## 3. API 설계
| Method | Path | 설명 |
|--------|------|------|
| POST | /api/trips | 출장 신청 |
| GET | /api/trips/{id} | 출장 조회 |
| PUT | /api/trips/{id}/approve | 승인 |
MD

cat > 90_Result_Doc/test_result.md << 'MD'
# 테스트 결과
- 총 테스트: 24개
- 통과: 22개
- 실패: 2개
- 커버리지: 78%
## 실패 항목
| 테스트 | 원인 |
|--------|------|
| test_approve_without_auth | 인가 체크 미구현 |
| test_date_validation | 날짜 검증 누락 |
MD

cat > 90_Result_Doc/review_report.md << 'MD'
# 리뷰 보고서
- 코드 품질 점수: 72/100
- Critical 이슈: 1건 (SQL Injection)
- 배포 판정: 배포 불가
MD
```

---

## TC-7.1: sk-doc-md — 설계서 문서 생성

### 목적
설계 데이터를 기반으로 정식 설계서 마크다운 문서를 생성하는지 검증

### 실행

```
opencode> /sk-doc-md
```

"design.md를 기반으로 정식 설계서 문서를 작성해줘" 입력

### 검증 체크리스트

- [ ] **문서 유형 판별**: "설계서(design)" 유형으로 인식했는가
- [ ] **구성 완전성**: 아래 섹션이 포함되었는가
  - [ ] 문서 정보 (작성일, 버전, 작성자)
  - [ ] 프로젝트 개요
  - [ ] 아키텍처 설계
  - [ ] 모듈 구조
  - [ ] API 설계
  - [ ] DB 스키마
  - [ ] 기술스택
  - [ ] 보안 설계
  - [ ] 변경 이력
- [ ] **한국어**: 한국어로 작성되었는가
- [ ] **표/목록**: 표와 목록이 적극 사용되었는가
- [ ] **파일 생성**: `90_Result_Doc/` 하위에 .md 파일로 저장되었는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/*설계*.md 2>/dev/null || ls 90_Result_Doc/*design*.md 2>/dev/null
find 90_Result_Doc/ -name "*.json"
```

---

## TC-7.2: sk-doc-md — 테스트 보고서 문서 생성

### 목적
테스트 결과 데이터를 기반으로 정식 테스트 보고서를 생성하는지 검증

### 실행

```
opencode> /sk-doc-md
```

"test_result.md를 기반으로 테스트 보고서를 작성해줘" 입력

### 검증 체크리스트

- [ ] **문서 유형**: "테스트 보고서(test-report)"로 인식했는가
- [ ] **구성**: 문서 정보, 테스트 개요, 환경, 결과 요약, 상세 결과, 실패 분석, 커버리지, 결론
- [ ] **데이터 정확성**: 총 24개/통과 22개/실패 2개/커버리지 78%가 반영되었는가
- [ ] **실패 분석**: 2건의 실패 항목에 대한 분석이 포함되었는가
- [ ] **파일 생성**: `90_Result_Doc/` 하위에 .md 파일로 저장되었는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/*테스트*.md 2>/dev/null || ls 90_Result_Doc/*test_report*.md 2>/dev/null
grep "24\|22\|78" 90_Result_Doc/*test*.md 2>/dev/null | head -5
find 90_Result_Doc/ -name "*.json"
```

---

## TC-7.3: sk-doc-hwpx (HWPX 변환)

### 목적
마크다운 문서를 한글(hwpx) 형식으로 변환하는지 검증

### 사전 조건
- TC-7.1 완료 → 설계서 .md 존재
- sm-hwpx-builder MCP 연결 상태

### 실행

```
opencode> /sk-doc-hwpx
```

"설계서 문서를 hwpx로 변환해줘" 입력

### 검증 체크리스트

- [ ] **MCP 호출**: sm-hwpx-builder의 convert_md_to_hwpx 도구가 호출되었는가
- [ ] **변환 성공**: .hwpx 파일이 생성되었는가
- [ ] **저장 경로**: `90_Result_Doc/` 하위에 저장되었는가
- [ ] **내용 보존**: 원본 마크다운의 제목, 표, 목록이 hwpx에 포함되었는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

> **MCP 미연결 시**: "sm-hwpx-builder에 연결할 수 없습니다"와 같은 명확한 안내가 나오는지 검증

### 검증 명령어

```bash
find 90_Result_Doc/ -name "*.hwpx"
find 90_Result_Doc/ -name "*.json"
```

---

## TC-7.4: sk-doc-hwpx — 템플릿 기반 변환 (공문)

### 목적
gonmun(공문) 템플릿을 사용한 hwpx 변환이 동작하는지 검증

### 실행

```
opencode> /sk-doc-hwpx
```

"리뷰 보고서를 공문(gonmun) 양식으로 hwpx 변환해줘" 입력

### 검증 체크리스트

- [ ] **템플릿 인식**: gonmun 템플릿이 선택되었는가
- [ ] **5단계 실행**: analyze → extract → 매핑 → build → validate 순서인가
- [ ] **구조 분석**: analyze_hwpx로 공문 구조가 분석되었는가
- [ ] **내용 매핑**: 리뷰 보고서 내용이 공문 양식에 매핑되었는가
- [ ] **검증**: validate_hwpx로 최종 검증이 수행되었는가
- [ ] **파일 생성**: `90_Result_Doc/` 하위에 .hwpx 파일로 저장되었는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
find 90_Result_Doc/ -name "*공문*.hwpx" -o -name "*gonmun*.hwpx"
find 90_Result_Doc/ -name "*.json"
```

---

## TC-7.5: sa-documenter Agent (문서생성 워크플로우 통합)

### 목적
sa-documenter가 문서 유형 판별 → MD 생성 → HWPX 변환 → 저장 흐름을 자동 관리하는지 검증

### 사전 준비

```bash
cd /tmp/e2e_sol7
# design.md, test_result.md, review_report.md는 유지
```

### 실행

```
opencode> @sa-documenter design.md 기반으로 설계서를 작성하고 hwpx로도 변환해줘
```

### 검증 체크리스트

- [ ] **문서 유형 판별**: "설계서(design)" 유형으로 판별했는가
- [ ] **Step 2 실행**: sk-doc-md로 마크다운 설계서가 생성되었는가
- [ ] **HWPX 제안**: 공문/제안서가 아니더라도 사용자 요청에 따라 변환을 수행했는가
- [ ] **Step 3 실행**: sk-doc-hwpx로 hwpx 변환이 수행되었는가
- [ ] **SM_hwpx_builder MCP**: sm-hwpx-builder MCP가 사용되었는가
- [ ] **SM_obsidian_sync MCP**: Obsidian Vault 저장이 시도되었는가 (선택적)
- [ ] **산출물**: 아래 파일이 존재하는가
  - [ ] `90_Result_Doc/` 하위 .md 문서
  - [ ] `90_Result_Doc/` 하위 .hwpx 문서
- [ ] **출력 형식**: 전 과정에서 `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls -la 90_Result_Doc/

# md와 hwpx 모두 존재 확인
find 90_Result_Doc/ -name "*.md" | head -10
find 90_Result_Doc/ -name "*.hwpx"
find 90_Result_Doc/ -name "*.json"
```

---

## 결과 기록

| TC | 테스트명 | 결과 | 비고 |
|----|----------|------|------|
| TC-7.1 | sk-doc-md (설계서) | ⬜ PASS / ⬜ FAIL | |
| TC-7.2 | sk-doc-md (테스트보고서) | ⬜ PASS / ⬜ FAIL | |
| TC-7.3 | sk-doc-hwpx (자동 변환) | ⬜ PASS / ⬜ FAIL | |
| TC-7.4 | sk-doc-hwpx (공문 템플릿) | ⬜ PASS / ⬜ FAIL | |
| TC-7.5 | sa-documenter 통합 | ⬜ PASS / ⬜ FAIL | |

테스트 일시: ____-__-__ __:__
테스터: __________
