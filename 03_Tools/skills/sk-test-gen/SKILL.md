---
name: sk-test-gen
description: 소스코드에 대한 단위 테스트와 통합 테스트 코드를 자동 생성한다. JUnit, pytest, Jest, NUnit을 지원한다.
---

**[필수] 출력 형식 규칙: 모든 결과는 반드시 마크다운(.md) 파일로 저장한다. .json 파일을 생성하지 마라. 절대 .json 확장자를 사용하지 마라.**


대상 소스코드를 읽고 테스트 코드를 생성하라.

## 테스트 프레임워크 자동 감지

- Java: pom.xml/build.gradle → JUnit 5
- Python: pyproject.toml/requirements.txt → pytest
- JavaScript: package.json → Jest
- C#: .csproj → NUnit

## 단위 테스트 규칙

- 각 public 메서드/함수에 대해 최소 1개 이상의 테스트를 작성하라
- 정상 케이스, 경계값, 예외 케이스를 포함하라
- 테스트명은 한국어로 의미를 명확히 기술하라
- Given-When-Then 패턴을 사용하라

## 통합 테스트 규칙

- 주요 API 엔드포인트에 대해 요청/응답 테스트를 작성하라
- DB 연동 테스트 (테스트 DB 사용)
- 인증/인가 흐름 테스트
- 에러 응답 테스트

## 출력

- 테스트 코드 파일들
- 테스트용 설정 파일
- `90_Result_Doc/test_manifest.md`에 테스트 목록과 실행 방법을 기록하라
