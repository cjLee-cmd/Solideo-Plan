---
name: SSA_dep_scanner 사용자 매뉴얼
version: 1.0.0
---

# SSA_dep_scanner 사용자 매뉴얼

## 개요

프로젝트의 의존성/라이브러리를 스캔하여 폐쇄망 호환성을 판별하는 Sub-Agent이다. SA_analyzer의 하위 에이전트로 동작한다.

## opencode에서 사용하기

### SA_analyzer를 통한 자동 호출

SW_analysis Workflow 또는 SA_analyzer 실행 시 자동으로 호출된다.

```
/workflow SW_analysis --project_path /path/to/project
```

### 단독 호출

```
/sub-agent SSA_dep_scanner --project_path /path/to/project
```

## 스캔 대상

| 빌드 시스템 | 설정 파일 |
|-------------|-----------|
| Maven | pom.xml |
| Gradle | build.gradle |
| Python | requirements.txt, pyproject.toml |
| Node.js | package.json |
| .NET | .csproj, packages.config |

## 출력 예시

```json
[
  {
    "package_name": "spring-boot-starter-web",
    "version": "2.7.18",
    "license": "Apache-2.0",
    "purpose": "웹 애플리케이션 프레임워크",
    "compatibility": "호환",
    "note": ""
  },
  {
    "package_name": "aws-sdk-java",
    "version": "1.12.500",
    "license": "Apache-2.0",
    "purpose": "AWS 서비스 연동",
    "compatibility": "비호환",
    "note": "AWS API 직접 호출 필수. 대안: 로컬 스토리지 사용"
  }
]
```

## 호환성 등급

| 등급 | 의미 | 조치 |
|------|------|------|
| 호환 | 폐쇄망에서 정상 동작 | 없음 |
| 조건부호환 | 설정 변경으로 사용 가능 | 설정 변경 가이드 확인 |
| 비호환 | 폐쇄망 사용 불가 | 대안 라이브러리로 교체 필요 |

## 주의사항

- 코드 내에서 직접 URL을 호출하는 경우도 감지한다
- 라이선스 정보는 빌드 설정 기준이며, 정확한 확인은 별도 필요하다
