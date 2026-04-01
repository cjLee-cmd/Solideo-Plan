---
name: SK_design_spec 사용자 매뉴얼
version: 1.0.0
---

# SK_design_spec 사용자 매뉴얼

## 개요

Speckit 기반으로 신규 소프트웨어 설계 문서(design.md)를 생성하는 Skill이다.

## opencode에서 사용하기

### 기본 호출

```
/skill SK_design_spec
```

### 파라미터 지정 호출

```
/skill SK_design_spec --project_name "행정관리시스템" --purpose "내부 행정업무 전산화" --requirements "requirements.md"
```

### 대화형 호출

파라미터 없이 호출하면 대화형으로 정보를 수집한다.

```
/skill SK_design_spec
> 프로젝트명을 입력하세요: 행정관리시스템
> 프로젝트 목적을 입력하세요: 내부 행정업무 전산화
> 기능 요구사항 파일 경로 또는 직접 입력: requirements.md
> 기술스택 제약조건 (없으면 Enter): Java, Spring Boot, PostgreSQL
> 배포 환경 (기본: 폐쇄망): 폐쇄망
> 연동 대상 시스템 (없으면 Enter): 인사시스템, 결재시스템
```

## 입력 파라미터

| 파라미터 | 필수 | 형식 | 설명 |
|----------|------|------|------|
| project_name | Y | 문자열 | 프로젝트명 |
| purpose | Y | 문자열 | 프로젝트 목적 |
| requirements | Y | 파일경로 또는 문자열 | 기능 요구사항 |
| tech_constraints | N | 문자열 | 기술스택 제약 |
| target_env | N | 문자열 | 배포 환경 (기본: 폐쇄망) |
| existing_systems | N | 문자열 | 연동 시스템 목록 |

## 출력물

- `design.md` -- 현재 작업 디렉토리에 생성
- 포함 섹션: 프로젝트 개요, 아키텍처 설계, 모듈 구조, API 설계, DB 스키마, 기술스택, 보안 설계, 비기능 요구사항

## 후속 작업

생성된 design.md는 SK_design_review를 통해 사용자 검증을 진행한다.

```
/skill SK_design_review --input design.md
```

## 주의사항

- 폐쇄망 환경을 전제하므로 외부 API, CDN 의존 요소는 자동 배제된다
- 기술스택 제약을 지정하지 않으면 행정망 표준 스택(Java/Spring)을 기본 제안한다
