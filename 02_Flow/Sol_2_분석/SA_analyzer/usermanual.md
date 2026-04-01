---
name: SA_analyzer 사용자 매뉴얼
version: 1.0.0
---

# SA_analyzer 사용자 매뉴얼

## 개요

코드 분석을 총괄하는 Agent이다. 행정망 레거시 코드(Java, C#, JSP 등) 분석에 특화되어 있다.

## opencode에서 사용하기

### Agent 직접 호출

```
/agent SA_analyzer
```

### Workflow를 통한 호출

```
/workflow SW_analysis --project_path /path/to/project
```

## Agent가 수행하는 작업

1. 프로젝트의 빌드 설정과 설정 파일을 먼저 분석한다
2. SK_code_analyze를 실행하여 전체 구조를 파악한다
3. SSA_dep_scanner를 병렬로 실행하여 의존성을 상세 스캔한다
4. SK_analyze_doc을 실행하여 분석 보고서를 생성한다

## 대화 예시

```
사용자: /path/to/legacy-project 이 프로젝트를 분석해줘
SA_analyzer: 프로젝트 분석을 시작합니다.
  빌드 설정 확인 중... Maven 프로젝트(pom.xml) 확인
  기술스택: Java 8, Spring 4.3, MyBatis 3.4, Oracle 12c
  총 파일 수: 342개, 코드 라인: 48,230줄
  의존성 스캔 중... 외부 라이브러리 27개 식별
  [경고] 3개 라이브러리에서 외부 네트워크 호출 코드 발견
  상세 보고서를 analysis_report.md로 생성합니다.
```

## 주의사항

- 빌드 설정이 없는 프로젝트는 수동으로 기술스택을 지정해야 할 수 있다
- 폐쇄망 호환성 경고가 나오면 반드시 확인해야 한다
