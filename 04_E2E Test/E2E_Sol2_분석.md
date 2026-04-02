# E2E 테스트: Sol_2 분석

## 테스트 환경

| 항목 | 값 |
|------|-----|
| IDE | opencode CLI (`opencode run`) |
| 모델 (폐쇄망) | oss-120b |
| 모델 (인터넷망 테스트) | `opencode/qwen3.6-plus-free` 또는 `github-copilot/gpt-4o` |
| 테스트 디렉토리 | `/tmp/e2e_sol2` |

### 사전 준비: 분석 대상 샘플 프로젝트 생성

```bash
mkdir -p /tmp/e2e_sol2/src/main/java/com/example/controller
mkdir -p /tmp/e2e_sol2/src/main/java/com/example/service
mkdir -p /tmp/e2e_sol2/src/main/java/com/example/repository
mkdir -p /tmp/e2e_sol2/src/main/resources
cd /tmp/e2e_sol2 && git init

# pom.xml
cat > /tmp/e2e_sol2/pom.xml << 'XML'
<?xml version="1.0" encoding="UTF-8"?>
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>admin-system</artifactId>
  <version>1.0.0</version>
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
  </parent>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.mybatis.spring.boot</groupId>
      <artifactId>mybatis-spring-boot-starter</artifactId>
      <version>3.0.3</version>
    </dependency>
    <dependency>
      <groupId>com.oracle.database.jdbc</groupId>
      <artifactId>ojdbc11</artifactId>
      <scope>runtime</scope>
    </dependency>
  </dependencies>
</project>
XML

# Controller
cat > /tmp/e2e_sol2/src/main/java/com/example/controller/UserController.java << 'JAVA'
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
    @GetMapping
    public List<?> getUsers() { return userService.findAll(); }
    @PostMapping
    public void createUser(@RequestBody Object user) { userService.save(user); }
}
JAVA

# Service
cat > /tmp/e2e_sol2/src/main/java/com/example/service/UserService.java << 'JAVA'
package com.example.service;
import com.example.repository.UserRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class UserService {
    private final UserRepository userRepository;
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    public List<?> findAll() { return userRepository.selectAll(); }
    public void save(Object user) { userRepository.insert(user); }
}
JAVA

# Repository
cat > /tmp/e2e_sol2/src/main/java/com/example/repository/UserRepository.java << 'JAVA'
package com.example.repository;
import org.apache.ibatis.annotations.Mapper;
import java.util.List;

@Mapper
public interface UserRepository {
    List<?> selectAll();
    void insert(Object user);
}
JAVA

# application.yml
cat > /tmp/e2e_sol2/src/main/resources/application.yml << 'YML'
spring:
  datasource:
    url: jdbc:oracle:thin:@localhost:1521:ORCL
    username: admin
    password: admin123
mybatis:
  mapper-locations: classpath:mapper/*.xml
YML

cd /tmp/e2e_sol2
```

---

## TC-2.1: sk-code-analyze (소스코드 분석)

### 목적
프로젝트의 기술스택, 구조, 의존성, 메트릭스를 분석하고 폐쇄망 호환성을 점검하는지 검증

### 실행

```
opencode> /sk-code-analyze
```

"이 프로젝트를 분석해줘" 입력

### 검증 체크리스트

- [ ] **기술스택 식별**: Java, Spring Boot 3.2.0, MyBatis, Oracle이 식별되었는가
- [ ] **디렉토리 매핑**: controller/service/repository 구조가 매핑되었는가
- [ ] **의존성 분석**: pom.xml의 3개 dependency가 분석되었는가
- [ ] **코드 메트릭스**: 파일 수(4개 .java + 1 yml + 1 pom.xml), 라인 수가 포함되었는가
- [ ] **폐쇄망 호환성**: 각 라이브러리의 폐쇄망 호환 여부가 표시되었는가
- [ ] **파일 생성**: `90_Result_Doc/analysis_result.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/analysis_result.md
grep -i "spring boot" 90_Result_Doc/analysis_result.md
grep -i "mybatis" 90_Result_Doc/analysis_result.md
grep -i "oracle" 90_Result_Doc/analysis_result.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-2.2: sk-analyze-doc (분석 보고서 생성)

### 목적
analysis_result.md를 읽기 쉬운 보고서(analysis_report.md)로 변환하는지 검증

### 사전 조건
- TC-2.1 완료 → `90_Result_Doc/analysis_result.md` 존재

### 실행

```
opencode> /sk-analyze-doc
```

"analysis_result.md를 보고서로 작성해줘" 입력

### 검증 체크리스트

- [ ] **보고서 구조**: 아래 8개 섹션이 포함되었는가
  - [ ] 1. 프로젝트 개요
  - [ ] 2. 기술스택 (표 형식)
  - [ ] 3. 디렉토리 구조 (트리 형식)
  - [ ] 4. 아키텍처 분석
  - [ ] 5. 의존성 분석 (내부 모듈 + 외부 라이브러리 표)
  - [ ] 6. 코드 메트릭스
  - [ ] 7. 폐쇄망 호환성 점검
  - [ ] 8. 개선 제안
- [ ] **한국어**: 보고서가 한국어로 작성되었는가
- [ ] **표/목록 활용**: 표와 목록이 적극 사용되었는가
- [ ] **파일 생성**: `90_Result_Doc/analysis_report.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/analysis_report.md
grep -c "^## " 90_Result_Doc/analysis_report.md   # 8 이상
grep -c "|" 90_Result_Doc/analysis_report.md       # 표 존재 확인
find 90_Result_Doc/ -name "*.json"
```

---

## TC-2.3: sa-analyzer Agent (분석 워크플로우 통합)

### 목적
sa-analyzer가 sk-code-analyze → sk-analyze-doc 순서로 자동 호출하고 의존성 심층 분석(SSA_dep_scanner 역할)을 수행하는지 검증

### 사전 준비

```bash
# 이전 결과 삭제
rm -rf /tmp/e2e_sol2/90_Result_Doc
cd /tmp/e2e_sol2
```

### 실행

```
opencode> @sa-analyzer 이 프로젝트를 전체 분석해줘
```

### 검증 체크리스트

- [ ] **Step 1 실행**: sk-code-analyze가 먼저 실행되었는가
- [ ] **의존성 심층 분석**: 외부 라이브러리별 폐쇄망 호환성이 점검되었는가
  - [ ] spring-boot-starter-web → 호환 여부
  - [ ] mybatis-spring-boot-starter → 호환 여부
  - [ ] ojdbc11 → 호환 여부
- [ ] **Step 2 실행**: sk-analyze-doc가 이어서 실행되었는가
- [ ] **산출물 생성**: 아래 파일이 모두 존재하는가
  - [ ] `90_Result_Doc/analysis_result.md`
  - [ ] `90_Result_Doc/analysis_report.md`
- [ ] **빌드 설정 우선**: pom.xml을 먼저 확인했는가
- [ ] **객관적 근거**: 분석 결과에 파일 경로/코드 라인이 명시되었는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
# 산출물 전체 확인
ls -la 90_Result_Doc/

for f in analysis_result.md analysis_report.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f 없음"
done

# 폐쇄망 호환성 점검 포함 여부
grep -i "폐쇄망" 90_Result_Doc/analysis_report.md

find 90_Result_Doc/ -name "*.json"
```

---

## 결과 기록

| TC | 테스트명 | 결과 | 비고 |
|----|----------|------|------|
| TC-2.1 | sk-code-analyze | ⬜ PASS / ⬜ FAIL | |
| TC-2.2 | sk-analyze-doc | ⬜ PASS / ⬜ FAIL | |
| TC-2.3 | sa-analyzer 통합 | ⬜ PASS / ⬜ FAIL | |

테스트 일시: ____-__-__ __:__
테스터: __________
