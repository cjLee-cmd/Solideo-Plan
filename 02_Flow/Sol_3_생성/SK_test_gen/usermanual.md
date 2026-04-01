---
name: SK_test_gen 사용자 매뉴얼
version: 1.0.0
---

# SK_test_gen 사용자 매뉴얼

## 개요

소스코드에 대한 단위/통합 테스트 코드를 자동 생성하는 Skill이다.

## opencode에서 사용하기

### 기본 호출

```
/skill SK_test_gen --source_path ./src
```

### 프레임워크 지정

```
/skill SK_test_gen --source_path ./src --test_framework junit --coverage_target 90
```

### 단위 테스트만 생성

```
/skill SK_test_gen --source_path ./src --test_type unit
```

## 지원 테스트 프레임워크

| 언어 | 프레임워크 | 자동 감지 |
|------|-----------|-----------|
| Java | JUnit 5 | pom.xml / build.gradle |
| Python | pytest | pyproject.toml / requirements.txt |
| JavaScript | Jest | package.json |
| C# | NUnit | .csproj |

## 출력물

- 테스트 코드 파일들 (test/ 디렉토리)
- 테스트 설정 파일
- `test_manifest.md` -- 테스트 목록 및 실행 방법

## 후속 작업

```
/skill SK_test_run --test_path ./test
```

## 주의사항

- test_framework=auto이면 빌드 설정에서 자동 감지한다
- 기존 테스트 파일이 있으면 병합 여부를 확인한다
- Sol.3(생성)과 Sol.4(수정) 모두에서 사용된다
