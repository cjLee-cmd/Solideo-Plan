# E2E 테스트: Sol_3 생성

## 테스트 환경

| 항목 | 값 |
|------|-----|
| IDE | opencode CLI (`opencode run`) |
| 모델 (폐쇄망) | oss-120b |
| 모델 (인터넷망 테스트) | `opencode/qwen3.6-plus-free` 또는 `github-copilot/gpt-4o` |
| 테스트 디렉토리 | `/tmp/e2e_sol3` |

### 사전 준비: design.md 생성

```bash
mkdir -p /tmp/e2e_sol3/90_Result_Doc && cd /tmp/e2e_sol3 && git init

cat > 90_Result_Doc/design.md << 'MD'
# 출장관리시스템 설계서

## 1. 프로젝트 개요
- 프로젝트명: 출장관리시스템
- 목적: 출장 신청~정산 자동화
- 배포 환경: 폐쇄망

## 2. 아키텍처 설계
- 3-Tier: Presentation(Thymeleaf) → Business(Spring Boot) → Data(MyBatis+Oracle)
- 통신: REST API (내부망 전용)

## 3. 모듈 구조
- com.example.trip.controller — REST API 컨트롤러
- com.example.trip.service — 비즈니스 로직
- com.example.trip.repository — DB 접근 (MyBatis Mapper)
- com.example.trip.domain — 엔티티/DTO
- com.example.trip.config — 보안/DB 설정

## 4. API 설계
| Method | Path | 설명 |
|--------|------|------|
| POST | /api/trips | 출장 신청 |
| GET | /api/trips/{id} | 출장 상세 조회 |
| PUT | /api/trips/{id}/approve | 출장 승인 |
| PUT | /api/trips/{id}/reject | 출장 반려 |
| GET | /api/trips/my | 내 출장 목록 |

## 5. DB 스키마
- TRIP: id, applicant_id, destination, start_date, end_date, purpose, status, created_at
- TRIP_APPROVAL: id, trip_id, approver_id, action(APPROVE/REJECT), comment, acted_at
- TRIP_EXPENSE: id, trip_id, item, amount, receipt_path

## 6. 기술스택
- Java 17, Spring Boot 3.2, MyBatis 3, Oracle 19c, Thymeleaf

## 7. 보안 설계
- Spring Security 기반 인증/인가
- 비밀번호 BCrypt 암호화
- 감사로그 AOP 적용

## 8. 비기능 요구사항
- 동시 사용자 100명, 응답시간 2초 이내
MD
```

---

## TC-3.1: sk-code-gen (소스코드 생성)

### 목적
design.md 기반으로 소스코드를 생성하고 파일 매니페스트를 작성하는지 검증

### 실행

```
opencode> /sk-code-gen
```

"90_Result_Doc/design.md를 기반으로 코드를 생성해줘" 입력

### 검증 체크리스트

- [ ] **디렉토리 구조**: design.md의 모듈 구조대로 패키지가 생성되었는가
  - [ ] controller/ 패키지
  - [ ] service/ 패키지
  - [ ] repository/ 패키지
  - [ ] domain/ 패키지
  - [ ] config/ 패키지
- [ ] **API 구현**: 5개 엔드포인트가 모두 구현되었는가
- [ ] **설정 파일**: application.yml이 생성되었는가
- [ ] **보안 코드**: Spring Security 설정, BCrypt, 감사로그 AOP가 포함되었는가
- [ ] **입력값 검증**: @Valid, @NotNull 등 검증 코드가 있는가
- [ ] **SQL 바인딩**: MyBatis 매퍼에서 파라미터 바인딩(#{})을 사용하는가
- [ ] **한국어 주석**: 주요 로직에 한국어 주석이 포함되었는가
- [ ] **외부 호출 없음**: 외부 URL/API 호출 코드가 없는가
- [ ] **매니페스트**: `90_Result_Doc/file_manifest.md`가 생성되었는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
# 생성된 파일 목록
find src/ -name "*.java" | sort

# API 엔드포인트 확인
grep -rn "@GetMapping\|@PostMapping\|@PutMapping" src/

# 보안 코드 확인
grep -rn "BCrypt\|@PreAuthorize\|AuditLog" src/

# 외부 URL 확인 (없어야 정상)
grep -rnE "https?://" src/

# 매니페스트 확인
ls 90_Result_Doc/file_manifest.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-3.2: sk-test-gen (테스트 코드 생성)

### 목적
생성된 소스코드에 대한 단위/통합 테스트 코드를 자동 생성하는지 검증

### 사전 조건
- TC-3.1 완료 → 소스코드 존재

### 실행

```
opencode> /sk-test-gen
```

"생성된 코드에 대한 테스트 코드를 작성해줘" 입력

### 검증 체크리스트

- [ ] **프레임워크 감지**: pom.xml에서 JUnit 5를 감지했는가
- [ ] **단위 테스트**: Service/Repository 각 public 메서드에 테스트가 있는가
- [ ] **통합 테스트**: 5개 API 엔드포인트 테스트가 있는가
- [ ] **테스트 패턴**: Given-When-Then 패턴을 사용하는가
- [ ] **케이스 범위**: 정상/경계값/예외 케이스가 포함되었는가
- [ ] **한국어 테스트명**: 테스트명이 한국어로 의미가 명확한가
- [ ] **테스트 설정**: 테스트용 설정 파일(application-test.yml 등)이 있는가
- [ ] **매니페스트**: `90_Result_Doc/test_manifest.md`가 생성되었는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
# 테스트 파일 목록
find src/test/ -name "*Test.java" | sort

# Given-When-Then 패턴 확인
grep -rn "given\|when\|then\|Given\|When\|Then" src/test/

# 한국어 테스트명 확인
grep -rn "@DisplayName" src/test/

ls 90_Result_Doc/test_manifest.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-3.3: sk-test-run (테스트 실행)

### 목적
테스트를 실행하고 결과/커버리지를 수집하는지 검증

### 사전 조건
- TC-3.2 완료 → 테스트 코드 존재

### 실행

```
opencode> /sk-test-run
```

"테스트를 실행해줘" 입력

### 검증 체크리스트

- [ ] **빌드 시스템 감지**: Maven을 감지하고 `mvn test`를 실행했는가
- [ ] **결과 수집**: 아래 항목이 포함되었는가
  - [ ] 총 테스트 수
  - [ ] 통과/실패/스킵 수
  - [ ] 커버리지 비율
  - [ ] 실행 시간
- [ ] **실패 상세**: 실패 테스트가 있으면 원인/스택트레이스가 기록되었는가
- [ ] **판정**: 성공/실패/경고 판정이 명확한가
- [ ] **파일 생성**: `90_Result_Doc/test_result.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/test_result.md
grep -iE "통과|실패|커버리지" 90_Result_Doc/test_result.md
find 90_Result_Doc/ -name "*.json"
```

> **참고**: 폐쇄망에서 Maven/Oracle이 없을 수 있으므로 빌드 실패 시 sk-test-run이 실패 원인을 정확히 보고하는지도 검증 대상임

---

## TC-3.4: sk-gen-report (종합 보고서)

### 목적
코드 생성 + 테스트 결과를 종합한 보고서가 작성되는지 검증

### 사전 조건
- TC-3.1~3.3 완료

### 실행

```
opencode> /sk-gen-report
```

"생성 결과를 종합 보고서로 작성해줘" 입력

### 검증 체크리스트

- [ ] **보고서 구조**: 6개 섹션이 포함되었는가
  - [ ] 1. 생성 요약
  - [ ] 2. 생성 파일 목록 (표)
  - [ ] 3. 설계 대비 구현 현황
  - [ ] 4. 테스트 결과
  - [ ] 5. 미해결 사항
  - [ ] 6. 다음 단계
- [ ] **설계 대비**: design.md 항목 대비 구현 완료/미완료가 매핑되었는가
- [ ] **파일 생성**: `90_Result_Doc/generation_report.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/generation_report.md
grep -c "^## " 90_Result_Doc/generation_report.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-3.5: sa-generator Agent (생성 워크플로우 통합)

### 목적
sa-generator가 4개 Skill을 순차 호출하고, 테스트 실패 시 자동 수정/재실행하는지 검증

### 사전 준비

```bash
rm -rf /tmp/e2e_sol3/src /tmp/e2e_sol3/90_Result_Doc/file_manifest.md /tmp/e2e_sol3/90_Result_Doc/test_*.md /tmp/e2e_sol3/90_Result_Doc/generation_report.md
cd /tmp/e2e_sol3
```

### 실행

```
opencode> @sa-generator design.md 기반으로 전체 생성 워크플로우를 수행해줘
```

### 검증 체크리스트

- [ ] **Step 순서**: code-gen → test-gen → test-run → gen-report 순서로 진행되었는가
- [ ] **테스트 재시도**: 테스트 실패 시 코드 수정 후 재실행했는가 (최대 3회)
- [ ] **산출물 전체**: 아래 파일이 모두 존재하는가
  - [ ] `90_Result_Doc/file_manifest.md`
  - [ ] `90_Result_Doc/test_manifest.md`
  - [ ] `90_Result_Doc/test_result.md`
  - [ ] `90_Result_Doc/generation_report.md`
- [ ] **SM_test_runner MCP**: 테스트 실행 시 sm-test-runner MCP가 사용되었는가 (선택적)
- [ ] **보안 코드**: 생성 코드에 보안 요소가 포함되었는가
- [ ] **출력 형식**: 전 과정에서 `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls -la 90_Result_Doc/

for f in file_manifest.md test_manifest.md test_result.md generation_report.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f 없음"
done

find . -name "*.json" | grep -v node_modules
```

---

## 결과 기록

| TC | 테스트명 | 결과 | 비고 |
|----|----------|------|------|
| TC-3.1 | sk-code-gen | ⬜ PASS / ⬜ FAIL | |
| TC-3.2 | sk-test-gen | ⬜ PASS / ⬜ FAIL | |
| TC-3.3 | sk-test-run | ⬜ PASS / ⬜ FAIL | |
| TC-3.4 | sk-gen-report | ⬜ PASS / ⬜ FAIL | |
| TC-3.5 | sa-generator 통합 | ⬜ PASS / ⬜ FAIL | |

테스트 일시: ____-__-__ __:__
테스터: __________
