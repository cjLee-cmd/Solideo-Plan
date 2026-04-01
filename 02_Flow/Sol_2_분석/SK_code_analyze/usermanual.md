---
name: SK_code_analyze 사용자 매뉴얼
version: 1.0.0
---

# SK_code_analyze 사용자 매뉴얼

## 개요

기존 소스코드의 기술스택, 구조, 의존성, 코드 품질을 분석하는 Skill이다.

## opencode에서 사용하기

### 프로젝트 전체 분석

```
/skill SK_code_analyze --project_path /path/to/project
```

### 특정 모듈만 분석

```
/skill SK_code_analyze --project_path /path/to/project --scope module --target_module auth
```

### 단일 파일 분석

```
/skill SK_code_analyze --project_path /path/to/project --scope file --target_module src/main/App.java
```

## 분석 결과 항목

| 항목 | 설명 |
|------|------|
| 기술스택 | 언어, 프레임워크, 빌드도구, DB |
| 디렉토리 구조 | 트리 형식 구조도, 디렉토리별 역할 |
| 모듈 의존성 | 내부/외부 의존 관계, 순환 의존 여부 |
| 코드 메트릭스 | 파일 수, 라인 수, 복잡도 |
| 폐쇄망 호환성 | 외부 네트워크 의존 여부 |

## 출력물

- 분석 결과는 JSON 구조체로 반환된다
- SK_analyze_doc을 이어서 실행하면 마크다운 보고서로 변환된다

```
/skill SK_code_analyze --project_path ./my_project
/skill SK_analyze_doc --input analysis_result.json
```

## 주의사항

- 대규모 프로젝트(10만 라인 이상)는 scope를 module로 나누어 분석하는 것을 권장한다
- 바이너리 파일, 빌드 산출물 디렉토리는 자동 제외된다
- 폐쇄망 호환성 점검 결과에서 "외부 의존" 항목은 반드시 확인해야 한다
