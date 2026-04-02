# E2E 테스트: Sol_5 리뷰

## 테스트 환경

| 항목 | 값 |
|------|-----|
| IDE | opencode CLI (`opencode run`) |
| 모델 (폐쇄망) | oss-120b |
| 모델 (인터넷망 테스트) | `opencode/qwen3.6-plus-free` 또는 `github-copilot/gpt-4o` |
| 테스트 디렉토리 | `/tmp/e2e_sol5` |

### 사전 준비: 리뷰 대상 프로젝트 생성

```bash
mkdir -p /tmp/e2e_sol5/src/main/java/com/example/{controller,service,repository}
mkdir -p /tmp/e2e_sol5/90_Result_Doc
cd /tmp/e2e_sol5 && git init

# 의도적으로 품질/보안 이슈를 포함한 코드

# Controller (보안 이슈: 인가 없음, 입력 검증 없음)
cat > src/main/java/com/example/controller/UserController.java << 'JAVA'
package com.example.controller;
import com.example.service.UserService;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // 인가 체크 없음
    @GetMapping
    public List<?> getAllUsers() {
        return userService.findAll();
    }

    // 입력 검증 없음
    @PostMapping
    public void createUser(@RequestBody Object user) {
        userService.save(user);
    }

    // SQL Injection 가능: id를 문자열로 받아 직접 전달
    @GetMapping("/search")
    public Object searchUser(@RequestParam String query) {
        return userService.search(query);
    }
}
JAVA

# Service (품질 이슈: 너무 긴 함수, 예외 처리 부실)
cat > src/main/java/com/example/service/UserService.java << 'JAVA'
package com.example.service;
import com.example.repository.UserRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class UserService {
    private final UserRepository repo;
    public UserService(UserRepository repo) { this.repo = repo; }

    public List<?> findAll() { return repo.selectAll(); }
    public void save(Object user) { repo.insert(user); }

    // 쿼리를 직접 전달 (SQL Injection 위험)
    public Object search(String query) {
        return repo.searchByRawQuery(query);
    }
}
JAVA

# Repository (보안 이슈: Raw SQL)
cat > src/main/java/com/example/repository/UserRepository.java << 'JAVA'
package com.example.repository;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface UserRepository {
    List<?> selectAll();
    void insert(Object user);

    // SQL Injection 취약: ${} 사용
    @Select("SELECT * FROM users WHERE name = '${query}'")
    Object searchByRawQuery(String query);
}
JAVA
```

---

## TC-5.1: sk-code-review (코드 품질 리뷰)

### 목적
코드의 품질/스타일/로직 이슈를 심각도별로 식별하고 품질 점수를 산출하는지 검증

### 실행

```
opencode> /sk-code-review
```

"이 프로젝트 코드를 리뷰해줘" 입력

### 검증 체크리스트

- [ ] **리뷰 항목 완전성**: 6개 항목(가독성/설계/에러처리/로직/성능/로깅)이 모두 점검되었는가
- [ ] **이슈 식별**: 아래 이슈가 탐지되었는가
  - [ ] Object 타입 사용 → 타입 안전성 문제 (major)
  - [ ] 입력 검증 없음 (major)
  - [ ] Raw 쿼리 전달 (critical)
  - [ ] 예외 처리 부재 (major)
- [ ] **심각도 분류**: critical/major/minor/info로 분류되었는가
- [ ] **위치 명시**: 파일 경로 + 라인 번호가 포함되었는가
- [ ] **개선 제안**: 각 이슈에 구체적 수정 방안이 제시되었는가
- [ ] **품질 점수**: 0-100 점수가 산출되었는가
- [ ] **파일 생성**: `90_Result_Doc/code_review_result.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/code_review_result.md
grep -iE "critical|major|minor" 90_Result_Doc/code_review_result.md
grep -iE "점수|score" 90_Result_Doc/code_review_result.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-5.2: sk-security-review (보안 리뷰)

### 목적
OWASP Top 10 + 행정망 보안 가이드라인 기준으로 보안 취약점을 식별하는지 검증

### 실행

```
opencode> /sk-security-review
```

"이 프로젝트의 보안 취약점을 점검해줘" 입력

### 검증 체크리스트

- [ ] **OWASP 점검**: 10개 카테고리가 점검되었는가
- [ ] **취약점 식별**: 아래 취약점이 탐지되었는가
  - [ ] A01 접근제어: 인가 없는 API 엔드포인트 (critical)
  - [ ] A03 주입공격: `${query}` SQL Injection (critical)
  - [ ] A07 인증실패: 인증 설정 미존재 (high)
  - [ ] A09 로깅실패: 감사로그 부재 (medium)
- [ ] **행정망 추가 점검**: 개인정보보호, 접근제어, 감사로그, 암호화가 점검되었는가
- [ ] **수정 가이드**: critical/high 취약점에 구체적 수정 코드가 제시되었는가
- [ ] **배포 판정**: critical 있으므로 "배포 금지" 판정인가
- [ ] **파일 생성**: `90_Result_Doc/security_review_result.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/security_review_result.md
grep -i "SQL Injection\|A03\|injection" 90_Result_Doc/security_review_result.md
grep -i "접근제어\|A01" 90_Result_Doc/security_review_result.md
grep -iE "배포 금지|배포 불가" 90_Result_Doc/security_review_result.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-5.3: sk-review-report (종합 리뷰 보고서)

### 목적
코드 리뷰 + 보안 리뷰 결과를 종합하고 이슈 ID를 부여하여 배포 가능 여부를 판정하는지 검증

### 사전 조건
- TC-5.1, TC-5.2 완료

### 실행

```
opencode> /sk-review-report
```

"리뷰 결과를 종합 보고서로 작성해줘" 입력

### 검증 체크리스트

- [ ] **보고서 구조**: 5개 섹션이 포함되었는가
  - [ ] 1. 리뷰 요약 (품질 점수, 총 이슈 수)
  - [ ] 2. 코드 품질 이슈 (REV-001 형식)
  - [ ] 3. 보안 취약점 (SEC-001 형식, OWASP 분류)
  - [ ] 4. 조치 권고 (즉시/권장/검토)
  - [ ] 5. 종합 평가
- [ ] **이슈 ID**: REV-XXX, SEC-XXX 형식으로 부여되었는가
- [ ] **배포 판정**: Critical 이슈 존재 → "배포 불가" 판정인가
- [ ] **파일 생성**: `90_Result_Doc/review_report.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/review_report.md
grep -E "REV-[0-9]+" 90_Result_Doc/review_report.md
grep -E "SEC-[0-9]+" 90_Result_Doc/review_report.md
grep -iE "배포 불가|배포 가능|조건부" 90_Result_Doc/review_report.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-5.4: sa-reviewer Agent (리뷰 워크플로우 통합)

### 목적
sa-reviewer가 코드 리뷰 + 보안 리뷰 → 종합 보고서 순서로 진행하고, Critical 이슈를 즉시 보고하는지 검증

### 사전 준비

```bash
rm -rf /tmp/e2e_sol5/90_Result_Doc
mkdir -p /tmp/e2e_sol5/90_Result_Doc
cd /tmp/e2e_sol5
```

### 실행

```
opencode> @sa-reviewer 이 프로젝트 전체를 리뷰해줘
```

### 검증 체크리스트

- [ ] **Step 1 동시 실행**: sk-code-review와 sk-security-review가 모두 실행되었는가
- [ ] **Critical 즉시 보고**: SQL Injection 등 Critical 이슈를 발견 즉시 사용자에게 보고했는가
- [ ] **Step 2 실행**: sk-review-report로 종합 보고서가 생성되었는가
- [ ] **긍정적 피드백**: 잘 작성된 부분에 대한 긍정적 코멘트가 있는가
- [ ] **수정 코드 예시**: 보안 취약점에 수정 코드가 함께 제시되었는가
- [ ] **산출물 전체**: 아래 파일이 모두 존재하는가
  - [ ] `90_Result_Doc/code_review_result.md`
  - [ ] `90_Result_Doc/security_review_result.md`
  - [ ] `90_Result_Doc/review_report.md`
- [ ] **출력 형식**: 전 과정에서 `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls -la 90_Result_Doc/

for f in code_review_result.md security_review_result.md review_report.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f 없음"
done

find 90_Result_Doc/ -name "*.json"
```

---

## 결과 기록

| TC | 테스트명 | 결과 | 비고 |
|----|----------|------|------|
| TC-5.1 | sk-code-review | ⬜ PASS / ⬜ FAIL | |
| TC-5.2 | sk-security-review | ⬜ PASS / ⬜ FAIL | |
| TC-5.3 | sk-review-report | ⬜ PASS / ⬜ FAIL | |
| TC-5.4 | sa-reviewer 통합 | ⬜ PASS / ⬜ FAIL | |

테스트 일시: ____-__-__ __:__
테스터: __________
