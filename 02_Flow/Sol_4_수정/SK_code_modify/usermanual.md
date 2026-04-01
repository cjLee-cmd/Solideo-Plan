---
name: SK_code_modify 사용자 매뉴얼
version: 1.0.0
---

# SK_code_modify 사용자 매뉴얼

## 개요

기존 소스코드를 요구사항에 따라 수정하는 Skill이다.

## opencode에서 사용하기

### 버그 수정

```
/skill SK_code_modify --target_path ./src/auth/login.java --requirement "로그인 실패 시 5회 초과하면 계정 잠금" --modify_type bugfix
```

### 기능 추가

```
/skill SK_code_modify --target_path ./src/user/ --requirement "사용자 목록 CSV 내보내기 기능 추가" --modify_type feature
```

### 검증 기준 포함

```
/skill SK_code_modify --target_path ./src --requirement "요구사항.md" --verify_file verify.md
```

## 수정 유형

| 유형 | 설명 |
|------|------|
| bugfix | 기존 기능의 오류 수정 |
| feature | 새 기능 추가 |
| refactor | 구조 개선 (동작 변경 없음) |
| auto | 요구사항에서 자동 판별 |

## 출력물

- 수정된 소스코드 파일들
- `change_summary.md` -- 변경 사항 요약 (diff 포함)

## 후속 작업

```
/skill SK_impact_check --changes change_summary.md --project_path ./
```

수정 후 영향범위를 반드시 검토한다.

## 주의사항

- 최소 변경 원칙을 따른다 (필요한 부분만 수정)
- 기존 API 시그니처 변경은 사전 확인 후 진행한다
- DB 스키마 변경 시 마이그레이션 스크립트가 자동 포함된다
