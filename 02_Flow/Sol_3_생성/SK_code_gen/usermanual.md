---
name: SK_code_gen 사용자 매뉴얼
version: 1.0.0
---

# SK_code_gen 사용자 매뉴얼

## 개요

design.md 기반으로 전체 또는 부분 코드를 생성하는 Skill이다.

## opencode에서 사용하기

### 전체 프로젝트 생성

```
/skill SK_code_gen --design_file design.md
```

### 특정 모듈만 생성

```
/skill SK_code_gen --design_file design.md --scope module --target_module auth
```

### 언어/출력 경로 지정

```
/skill SK_code_gen --design_file design.md --language java --output_path ./backend/src
```

## 생성 규칙

- design.md의 아키텍처/모듈 구조를 정확히 따른다
- 코드 컨벤션(네이밍, 들여쓰기)을 일관 적용한다
- 보안 코드(입력검증, SQL 바인딩, 인증/인가)를 기본 포함한다
- 외부 네트워크 호출 코드를 포함하지 않는다

## 출력물

- 생성된 소스코드 파일들 (디렉토리 구조 포함)
- `file_manifest.md` -- 생성된 파일 목록 및 설명

## 후속 작업

```
/skill SK_test_gen --source_path ./src
```

생성된 코드에 대해 테스트 코드를 생성한다.

## 주의사항

- design.md가 SK_design_review를 통해 확정된 상태여야 한다
- 기존 파일이 있는 디렉토리에 생성 시 덮어쓰기 확인을 요청한다
- 대규모 프로젝트는 모듈별로 나누어 생성하는 것을 권장한다
