# E2E 테스트: Sol_6 E2E테스트

## 테스트 환경

| 항목 | 값 |
|------|-----|
| IDE | opencode CLI (`opencode run`) |
| 모델 (폐쇄망) | oss-120b |
| 모델 (인터넷망 테스트) | `opencode/qwen3.6-plus-free` 또는 `github-copilot/gpt-4o` |
| 테스트 디렉토리 | `/tmp/e2e_sol6` |

### 사전 준비: E2E 테스트 대상 웹 프로젝트

```bash
mkdir -p /tmp/e2e_sol6/src/main/java/com/example/{controller,service,domain}
mkdir -p /tmp/e2e_sol6/src/main/resources/templates
mkdir -p /tmp/e2e_sol6/90_Result_Doc
cd /tmp/e2e_sol6 && git init

# 간단한 Spring Boot + Thymeleaf 웹 앱 (출장 관리)

# Controller (웹 UI + API)
cat > src/main/java/com/example/controller/TripController.java << 'JAVA'
package com.example.controller;
import com.example.domain.Trip;
import com.example.service.TripService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class TripController {
    private final TripService tripService;
    public TripController(TripService tripService) { this.tripService = tripService; }

    @GetMapping("/login")
    public String loginPage() { return "login"; }

    @PostMapping("/login")
    public String login(@RequestParam String username, @RequestParam String password) {
        return "redirect:/trips";
    }

    @GetMapping("/trips")
    public String listTrips(Model model) {
        model.addAttribute("trips", tripService.findAll());
        return "trips";
    }

    @GetMapping("/trips/new")
    public String newTripForm() { return "trip_form"; }

    @PostMapping("/trips")
    public String createTrip(@ModelAttribute Trip trip) {
        tripService.applyTrip(trip);
        return "redirect:/trips";
    }

    @PostMapping("/trips/{id}/approve")
    public String approve(@PathVariable Long id) {
        tripService.approve(id);
        return "redirect:/trips";
    }
}
JAVA

# Service
cat > src/main/java/com/example/service/TripService.java << 'JAVA'
package com.example.service;
import com.example.domain.Trip;
import org.springframework.stereotype.Service;
import java.util.*;

@Service
public class TripService {
    private final List<Trip> trips = new ArrayList<>();
    private long seq = 1;

    public List<Trip> findAll() { return trips; }

    public void applyTrip(Trip trip) {
        trip.setId(seq++);
        trip.setStatus("PENDING");
        trips.add(trip);
    }

    public void approve(Long id) {
        trips.stream().filter(t -> t.getId().equals(id))
             .findFirst().ifPresent(t -> t.setStatus("APPROVED"));
    }
}
JAVA

# API Controller
cat > src/main/java/com/example/controller/TripApiController.java << 'JAVA'
package com.example.controller;
import com.example.domain.Trip;
import com.example.service.TripService;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/trips")
public class TripApiController {
    private final TripService tripService;
    public TripApiController(TripService tripService) { this.tripService = tripService; }

    @GetMapping
    public List<Trip> list() { return tripService.findAll(); }

    @PostMapping
    public Trip create(@RequestBody Trip trip) {
        tripService.applyTrip(trip);
        return trip;
    }

    @PostMapping("/{id}/approve")
    public void approve(@PathVariable Long id) { tripService.approve(id); }
}
JAVA
```

> **참고**: 실제 테스트 시에는 이 프로젝트를 `./mvnw spring-boot:run`으로 실행한 상태에서 E2E 테스트를 수행해야 함 (localhost:8080)

---

## TC-6.1: sk-e2e-test-gen (E2E 테스트 시나리오/코드 생성)

### 목적
웹 UI(Playwright), API 통합, 비즈니스 프로세스 E2E 테스트 코드를 생성하는지 검증

### 실행

```
opencode> /sk-e2e-test-gen
```

"출장관리시스템의 E2E 테스트 시나리오와 코드를 생성해줘. 로그인→출장신청→승인 흐름 포함" 입력

### 검증 체크리스트

**웹 UI 테스트 (Playwright)**
- [ ] Playwright 기반 테스트 코드가 생성되었는가
- [ ] 로그인 → 출장 목록 → 신규 신청 → 승인 시나리오가 포함되었는가
- [ ] `page.goto`, `page.fill`, `page.click`, `assert` 등 Playwright API 사용
- [ ] 접근성 선택자(role, label)가 우선 사용되었는가
- [ ] headless 모드로 실행 가능한가
- [ ] 실패 시 스크린샷 캡처 설정이 있는가

**API 통합 테스트**
- [ ] POST /api/trips → GET /api/trips → POST /{id}/approve 연계 테스트가 있는가
- [ ] 응답 상태코드 및 본문 검증이 포함되었는가

**비즈니스 프로세스 테스트**
- [ ] 기안→결재→승인→완료 전체 흐름이 테스트되는가

**공통**
- [ ] 테스트 파일이 `tests/e2e/` 디렉토리에 생성되었는가
- [ ] 각 시나리오에 시나리오명/사전조건/실행단계/예상결과/정리가 기술되었는가
- [ ] `90_Result_Doc/e2e_test_manifest.md`가 생성되었는가
- [ ] `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
# 테스트 파일 확인 (Python 또는 Java)
find tests/e2e/ -name "*.py" -o -name "*.java" | sort

# Playwright API 사용 확인 (Python)
grep -rn "playwright\|page.goto\|page.fill\|page.click" tests/e2e/

# API 테스트 확인 (Python 또는 Java)
grep -rn "requests.post\|requests.get\|RestTemplate\|WebTestClient" tests/e2e/

# 매니페스트 확인
ls 90_Result_Doc/e2e_test_manifest.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-6.2: sk-e2e-test-run (E2E 테스트 실행)

### 목적
E2E 테스트를 실행하고 결과를 수집하는지 검증

### 사전 조건
- TC-6.1 완료
- 대상 애플리케이션 실행 중 (localhost:8080)
- Playwright 브라우저 설치 (`playwright install chromium`)

### 실행

```
opencode> /sk-e2e-test-run
```

"E2E 테스트를 실행해줘" 입력

### 검증 체크리스트

- [ ] **환경 확인**: 실행 전 서버 접근/브라우저 설치를 확인했는가
- [ ] **Playwright 실행**: headless 모드로 웹 E2E가 실행되었는가
- [ ] **API 테스트 실행**: API 통합 테스트가 실행되었는가
- [ ] **결과 수집**: 아래 항목이 포함되었는가
  - [ ] 총 시나리오 수
  - [ ] 통과/실패/스킵 수
  - [ ] 실패 시나리오 상세 (에러 메시지, 스크린샷 경로)
  - [ ] 실행 시간
- [ ] **실패 시 재시도**: 실패 테스트의 원인 분석 + 코드 수정 + 재실행 (최대 3회)
- [ ] **파일 생성**: `90_Result_Doc/e2e_test_result.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

> **환경 미비 시**: 서버가 실행 중이지 않으면 "서버에 접근할 수 없습니다"와 같은 명확한 오류 보고가 나오는지도 검증

### 검증 명령어

```bash
ls 90_Result_Doc/e2e_test_result.md
grep -iE "통과|실패|스킵" 90_Result_Doc/e2e_test_result.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-6.3: sk-e2e-report (E2E 종합 보고서)

### 목적
테스트 시나리오, 실행 결과, 실패 분석을 종합한 보고서가 작성되는지 검증

### 사전 조건
- TC-6.1, TC-6.2 완료

### 실행

```
opencode> /sk-e2e-report
```

"E2E 테스트 결과를 종합 보고서로 작성해줘" 입력

### 검증 체크리스트

- [ ] **보고서 구조**: 7개 섹션이 포함되었는가
  - [ ] 1. 테스트 요약
  - [ ] 2. 시나리오 목록 (표: 시나리오명/유형/결과/실행시간)
  - [ ] 3. 웹 UI 테스트 결과
  - [ ] 4. API 통합 테스트 결과
  - [ ] 5. 실패 분석
  - [ ] 6. 배포 판정
  - [ ] 7. 개선 제안
- [ ] **시나리오 유형 분류**: 웹UI / API / 비즈니스로 분류되었는가
- [ ] **배포 판정**: Critical 시나리오 통과 여부에 따른 판정이 있는가
- [ ] **파일 생성**: `90_Result_Doc/e2e_report.md`가 존재하는가
- [ ] **출력 형식**: `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls 90_Result_Doc/e2e_report.md
grep -c "^## " 90_Result_Doc/e2e_report.md   # 7 이상
grep -iE "배포 가능|배포 불가" 90_Result_Doc/e2e_report.md
find 90_Result_Doc/ -name "*.json"
```

---

## TC-6.4: sa-e2e-tester Agent + SM_playwright MCP 통합

### 목적
sa-e2e-tester가 3개 Skill을 순차 호출하고, sm-playwright MCP를 활용한 브라우저 제어가 가능한지 검증

### 사전 준비

```bash
rm -rf /tmp/e2e_sol6/tests /tmp/e2e_sol6/90_Result_Doc
mkdir -p /tmp/e2e_sol6/90_Result_Doc
cd /tmp/e2e_sol6
```

### 실행

```
opencode> @sa-e2e-tester 출장관리시스템의 전체 E2E 테스트를 수행해줘
```

### 검증 체크리스트

- [ ] **Step 순서**: e2e-test-gen → e2e-test-run → e2e-report 순서로 진행되었는가
- [ ] **Playwright MCP**: sm-playwright MCP 연결을 시도했는가
  - [ ] 연결 성공 시: 접근성 스냅샷으로 페이지 구조 파악 (비전 모델 불필요)
  - [ ] 연결 실패 시: "sm-playwright에 연결할 수 없습니다" 안내 후 코드 기반 테스트로 대체
- [ ] **실패 시 재시도**: 최대 3회 수정/재실행이 시도되었는가
- [ ] **산출물 전체**: 아래 파일이 모두 존재하는가
  - [ ] `90_Result_Doc/e2e_test_manifest.md`
  - [ ] `90_Result_Doc/e2e_test_result.md`
  - [ ] `90_Result_Doc/e2e_report.md`
- [ ] **Critical 판정**: Critical 시나리오 실패 시 배포 불가로 판정했는가
- [ ] **출력 형식**: 전 과정에서 `.json` 파일이 생성되지 않았는가

### 검증 명령어

```bash
ls -la 90_Result_Doc/

for f in e2e_test_manifest.md e2e_test_result.md e2e_report.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f 없음"
done

find 90_Result_Doc/ -name "*.json"
```

---

## 결과 기록

| TC | 테스트명 | 결과 | 비고 |
|----|----------|------|------|
| TC-6.1 | sk-e2e-test-gen | ⬜ PASS / ⬜ FAIL | |
| TC-6.2 | sk-e2e-test-run | ⬜ PASS / ⬜ FAIL | |
| TC-6.3 | sk-e2e-report | ⬜ PASS / ⬜ FAIL | |
| TC-6.4 | sa-e2e-tester + Playwright MCP 통합 | ⬜ PASS / ⬜ FAIL | |

테스트 일시: ____-__-__ __:__
테스터: __________
