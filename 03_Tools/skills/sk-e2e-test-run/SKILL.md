---
name: sk-e2e-test-run
description: E2E 테스트를 실행하고 결과를 수집한다. Playwright 웹 테스트와 API 통합 테스트를 모두 지원한다.
---

**[필수] 출력 형식 규칙: 모든 결과는 반드시 마크다운(.md) 파일로 저장한다. .json 파일을 생성하지 마라. 절대 .json 확장자를 사용하지 마라.**

E2E 테스트를 실행하고 결과를 수집하라.

## 실행 절차

### 1. 환경 확인

테스트 실행 전 아래를 확인하라:
- 대상 애플리케이션이 실행 중인지 (로컬 서버 URL 접근 가능 여부)
- Playwright 브라우저가 설치되어 있는지 (`playwright install` 실행 여부)
- 테스트 DB가 초기화되어 있는지

### 2. Playwright 웹 E2E 실행

```bash
# pytest + playwright
python -m pytest tests/e2e/ --headed --slowmo=500 --screenshot=only-on-failure

# headless (CI/폐쇄망 서버)
python -m pytest tests/e2e/ --screenshot=only-on-failure
```

### 3. API E2E 실행

```bash
python -m pytest tests/e2e/api/ -v
```

### 4. Playwright MCP를 통한 실행

sm-playwright MCP가 연결된 경우:
- `use sm-playwright`로 브라우저를 직접 제어하여 수동 E2E 테스트 수행 가능
- 접근성 스냅샷 기반으로 페이지 구조를 파악하고 상호작용

## 결과 수집

- 총 시나리오 수, 통과/실패/스킵 수
- 실패 시나리오별 상세 (단계, 스크린샷, 에러 메시지)
- 실행 시간

## 판정

- 전체 통과 → 성공
- Critical 시나리오 실패 → 실패 (배포 차단)
- Non-critical 실패 → 경고

## 출력

**반드시 `90_Result_Doc/e2e_test_result.md`에 마크다운 형식으로 저장하라.**
- 90_Result_Doc 디렉토리가 없으면 먼저 생성하라
