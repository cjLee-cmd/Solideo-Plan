# Sol_6 E2E테스트 — 테스트 결과

실행일: 2026-04-02
환경: macOS (인터넷망)
상태: **전체 미실행**

## 미실행 사유

Sol_6(E2E테스트)은 **실행 중인 웹 서버 + Playwright 브라우저**가 필요하다.

| 요구사항 | 이유 |
|---------|------|
| 웹 서버 실행 (localhost:8080) | 웹 UI E2E 테스트 대상 |
| Playwright 브라우저 | `playwright install chromium` 필요 |
| Python + pytest | 테스트 코드 실행 |
| sm-playwright MCP | opencode에서 브라우저 직접 제어 |

## 로컬 실행 방법

### 사전 준비

```bash
# 1. 테스트 대상 웹 프로젝트 준비 (Spring Boot 등)
mkdir -p /tmp/e2e_sol6/90_Result_Doc
cd /tmp/e2e_sol6 && git init

# 2. 대상 앱 빌드 및 실행
# cd /path/to/target-app && ./mvnw spring-boot:run
# → http://localhost:8080 접속 가능 확인

# 3. Playwright 설치
pip install pytest-playwright
playwright install chromium
```

### 폐쇄망 필수 환경

| 항목 | 요구사항 |
|------|---------|
| Python | 3.9+ |
| Playwright | 오프라인 설치 (브라우저 바이너리 포함) |
| 대상 앱 | localhost:8080에서 실행 중 |
| npm | `@playwright/mcp` (sm-playwright MCP용) |

### TC-6.1: sk-e2e-test-gen

```bash
opencode run --dir . -m "모델명" \
  "/sk-e2e-test-gen 출장관리시스템의 E2E 테스트 시나리오와 코드를 생성해줘. 로그인→출장신청→승인 흐름 포함"

# 검증
find tests/e2e/ -name "*.py" -o -name "*.java" | sort
grep -rn "playwright\|page.goto\|page.fill\|page.click" tests/e2e/
grep -rn "requests.post\|requests.get" tests/e2e/
ls 90_Result_Doc/e2e_test_manifest.md
find 90_Result_Doc/ -name "*.json"
```

### TC-6.2: sk-e2e-test-run

```bash
# 대상 앱이 localhost:8080에서 실행 중이어야 함
opencode run --dir . -m "모델명" "/sk-e2e-test-run E2E 테스트를 실행해줘"

# 검증
ls 90_Result_Doc/e2e_test_result.md
grep -iE "통과|실패|스킵" 90_Result_Doc/e2e_test_result.md
```

### TC-6.3: sk-e2e-report

```bash
opencode run --dir . -m "모델명" \
  "/sk-e2e-report E2E 테스트 결과를 종합 보고서로 작성해줘"

# 검증
ls 90_Result_Doc/e2e_report.md
grep -c "^## " 90_Result_Doc/e2e_report.md   # 7 이상
grep -iE "배포 가능|배포 불가" 90_Result_Doc/e2e_report.md
```

### TC-6.4: sa-e2e-tester + Playwright MCP 통합

```bash
opencode run --dir . -m "모델명" --agent sa-e2e-tester \
  "출장관리시스템의 전체 E2E 테스트를 수행해줘"

# 검증
for f in e2e_test_manifest.md e2e_test_result.md e2e_report.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f"
done
find 90_Result_Doc/ -name "*.json"
```

### sm-playwright MCP 연동 테스트 (별도)

```bash
# opencode TUI에서 직접 테스트
opencode
# opencode 내에서:
# > sm-playwright로 http://localhost:8080에 접속하고 로그인 페이지를 확인해줘
```
