# E2E 테스트: Sol_4 수정

## 테스트 환경

| 항목 | 값 |
|------|-----|
| IDE | opencode CLI (`opencode run`) |
| 모델 (폐쇄망) | oss-120b |
| 모델 (인터넷망 테스트) | `opencode/qwen3.6-plus-free` 또는 `github-copilot/gpt-4o` |
| 테스트 디렉토리 | `/tmp/e2e_sol4` |

### 사전 준비: 수정 대상 프로젝트 생성

```bash
mkdir -p /tmp/e2e_sol4/src/main/java/com/example/{controller,service,repository,domain}
mkdir -p /tmp/e2e_sol4/src/main/resources
mkdir -p /tmp/e2e_sol4/90_Result_Doc
cd /tmp/e2e_sol4 && git init

# pom.xml
cat > pom.xml << 'XML'
<?xml version="1.0" encoding="UTF-8"?>
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>trip-system</artifactId>
  <version>1.0.0</version>
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
  </parent>
  <dependencies>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
    <dependency><groupId>org.mybatis.spring.boot</groupId><artifactId>mybatis-spring-boot-starter</artifactId><version>3.0.3</version></dependency>
  </dependencies>
</project>
XML

# Domain
cat > src/main/java/com/example/domain/Trip.java << 'JAVA'
package com.example.domain;
import java.time.LocalDate;

public class Trip {
    private Long id;
    private String applicantId;
    private String destination;
    private LocalDate startDate;
    private LocalDate endDate;
    private String purpose;
    private String status; // DRAFT, PENDING, APPROVED, REJECTED
    // getter/setter 생략
}
JAVA

# Service (버그 포함: 날짜 검증 누락)
cat > src/main/java/com/example/service/TripService.java << 'JAVA'
package com.example.service;
import com.example.domain.Trip;
import com.example.repository.TripRepository;
import org.springframework.stereotype.Service;

@Service
public class TripService {
    private final TripRepository tripRepository;
    public TripService(TripRepository tripRepository) {
        this.tripRepository = tripRepository;
    }

    // BUG: startDate > endDate 검증 누락
    public void applyTrip(Trip trip) {
        trip.setStatus("PENDING");
        tripRepository.insert(trip);
    }

    public Trip getTrip(Long id) {
        return tripRepository.selectById(id);
    }
}
JAVA

# Controller
cat > src/main/java/com/example/controller/TripController.java << 'JAVA'
package com.example.controller;
import com.example.domain.Trip;
import com.example.service.TripService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/trips")
public class TripController {
    private final TripService tripService;
    public TripController(TripService tripService) { this.tripService = tripService; }

    @PostMapping
    public void apply(@RequestBody Trip trip) { tripService.applyTrip(trip); }

    @GetMapping("/{id}")
    public Trip get(@PathVariable Long id) { return tripService.getTrip(id); }
}
JAVA

# Repository
cat > src/main/java/com/example/repository/TripRepository.java << 'JAVA'
package com.example.repository;
import com.example.domain.Trip;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface TripRepository {
    void insert(Trip trip);
    Trip selectById(Long id);
}
JAVA
```

---

## TC-4.1: sk-code-modify (코드 수정)

### 목적
버그 수정 요구사항에 따라 최소 범위로 코드를 수정하고 변경 기록을 남기는지 검증

### 실행

```
opencode> /sk-code-modify
```

"TripService.applyTrip에 startDate > endDate일 때 예외를 던지도록 버그 수정해줘" 입력

### 검증 체크리스트

- [ ] **최소 변경**: TripService.java만 수정되었는가 (불필요한 파일 변경 없음)
- [ ] **버그 수정**: startDate > endDate 검증 로직이 추가되었는가
- [ ] **스타일 유지**: 기존 코드 스타일(네이밍, 포맷)이 유지되었는가
- [ ] **변경 추적**: 변경 전/후가 기록되었는가
- [ ] **주석**: 변경 이유가 주석으로 남겨졌는가
- [ ] **하위 호환성**: applyTrip() 메서드 시그니처가 변경되지 않았는가
- [ ] **보안 유지**: 기존 보안 로직이 우회되지 않았는가
- [ ] **파일 생성**: `90_Result_Doc/change_summary.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
# 변경된 파일 확인 (TripService.java만 변경되어야 함)
grep -rn "startDate\|endDate" src/main/java/com/example/service/TripService.java

# 변경 기록 확인
ls 90_Result_Doc/change_summary.md
cat 90_Result_Doc/change_summary.md

find 90_Result_Doc/ -name "*.json"
```

---

## TC-4.2: sk-impact-check (영향 범위 분석)

### 목적
코드 수정 후 영향받는 다른 코드 영역을 파악하고 위험도를 평가하는지 검증

### 사전 조건
- TC-4.1 완료 → `90_Result_Doc/change_summary.md` 존재

### 실행

```
opencode> /sk-impact-check
```

"수정 영향 범위를 분석해줘" 입력

### 검증 체크리스트

- [ ] **직접 영향 식별**: TripService를 호출하는 TripController가 식별되었는가
- [ ] **간접 영향**: TripRepository 등 관련 모듈이 분석되었는가
- [ ] **API 영향**: applyTrip 시그니처 미변경이므로 "영향 없음" 판정인가
- [ ] **위험도 평가**: 높음/중간/낮음으로 평가되었는가
- [ ] **표 형식**: 영향 유형/파일/위험도/설명/조치 표가 포함되었는가
- [ ] **파일 생성**: `90_Result_Doc/impact_report.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/impact_report.md
grep -iE "높음|중간|낮음" 90_Result_Doc/impact_report.md
grep -i "TripController" 90_Result_Doc/impact_report.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-4.3: sk-modify-report (수정 종합 보고서)

### 목적
변경 사항, 영향분석, 테스트 결과를 종합한 보고서가 작성되는지 검증

### 사전 조건
- TC-4.1, TC-4.2 완료

### 실행

```
opencode> /sk-modify-report
```

"수정 결과를 종합 보고서로 작성해줘" 입력

### 검증 체크리스트

- [ ] **보고서 구조**: 7개 섹션이 포함되었는가
  - [ ] 1. 수정 요약
  - [ ] 2. 변경 파일 목록 (표)
  - [ ] 3. 변경 상세 (Diff 발췌)
  - [ ] 4. 영향분석 결과
  - [ ] 5. 테스트 결과
  - [ ] 6. 검증 상태
  - [ ] 7. 잔여 리스크
- [ ] **수정 유형**: bugfix로 분류되었는가
- [ ] **Diff 포함**: 변경 전/후 코드가 발췌되었는가
- [ ] **파일 생성**: `90_Result_Doc/modification_report.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/modification_report.md
grep -c "^## " 90_Result_Doc/modification_report.md   # 7 이상
grep -i "bugfix\|버그" 90_Result_Doc/modification_report.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-4.4: sa-modifier Agent (수정 워크플로우 통합)

### 목적
sa-modifier가 수정 → 영향분석 → 테스트 → 보고서 순서로 진행하고, 고위험 시 사용자 확인을 요청하는지 검증

### 사전 준비

```bash
# 이전 결과 삭제, 원본 코드 복원
rm -rf /tmp/e2e_sol4/90_Result_Doc
mkdir -p /tmp/e2e_sol4/90_Result_Doc
# TripService.java를 원래 버그 포함 코드로 복원
cd /tmp/e2e_sol4
```

### 실행

```
opencode> @sa-modifier TripService.applyTrip에 날짜 검증 버그를 수정해줘
```

### 테스트 입력

| 상황 | 예상 동작 | 사용자 입력 |
|------|-----------|-------------|
| 고위험 영향 발견 시 | 사용자 확인 요청 | "진행해주세요" |
| 테스트 실패 시 | 수정 후 재실행 (최대 3회) | (자동) |

### 검증 체크리스트

- [ ] **Step 순서**: modify → impact-check → test → report 순서로 진행되었는가
- [ ] **고위험 확인**: 고위험 항목 발견 시 사용자에게 확인을 요청했는가
- [ ] **테스트 재시도**: 실패 시 코드 수정 후 재실행했는가
- [ ] **SM_diff_viewer MCP**: diff 비교 시 sm-diff-viewer가 사용되었는가 (선택적)
- [ ] **산출물 전체**: 아래 파일이 모두 존재하는가
  - [ ] `90_Result_Doc/change_summary.md`
  - [ ] `90_Result_Doc/impact_report.md`
  - [ ] `90_Result_Doc/modification_report.md`
- [ ] **최소 변경**: 불필요한 파일이 수정되지 않았는가
- [ ] **출력 형식**: 전 과정에서 `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls -la 90_Result_Doc/

for f in change_summary.md impact_report.md modification_report.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f 없음"
done

find . -name "*.json" | grep -v node_modules
```

---

## 결과 기록

| TC | 테스트명 | 결과 | 비고 |
|----|----------|------|------|
| TC-4.1 | sk-code-modify | ⬜ PASS / ⬜ FAIL | |
| TC-4.2 | sk-impact-check | ⬜ PASS / ⬜ FAIL | |
| TC-4.3 | sk-modify-report | ⬜ PASS / ⬜ FAIL | |
| TC-4.4 | sa-modifier 통합 | ⬜ PASS / ⬜ FAIL | |

테스트 일시: ____-__-__ __:__
테스터: __________
