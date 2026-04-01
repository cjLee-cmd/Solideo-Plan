---
name: SK_e2e_test_gen
type: skill
description: E2E 테스트 시나리오와 Playwright 테스트 코드를 생성한다
version: 1.0.0
---

# SK_e2e_test_gen

## 목적

웹 UI(Playwright), API 통합, 비즈니스 프로세스 E2E 테스트 시나리오와 코드를 생성한다.

## 테스트 유형

### 1. 웹 UI E2E (Playwright)
- 브라우저 기반 테스트 (로그인, CRUD, 결재 흐름)
- 접근성 선택자 우선, headless 모드 지원
- 실패 시 스크린샷 자동 캡처

### 2. API 통합 E2E
- 엔드포인트 간 연계 흐름 테스트

### 3. 비즈니스 프로세스 E2E
- 행정 업무 흐름 (기안→결재→승인→완료)

## 출력
- tests/e2e/ 디렉토리에 테스트 코드
- 90_Result_Doc/e2e_test_manifest.md
