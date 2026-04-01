---
name: SK_code_review 사용자 매뉴얼
version: 1.0.0
---

# SK_code_review 사용자 매뉴얼

## 개요

코드 품질, 스타일, 로직을 리뷰하는 Skill이다.

## opencode에서 사용하기

### 전체 리뷰

```
/skill SK_code_review --target_path ./src
```

### 로직 집중 리뷰

```
/skill SK_code_review --target_path ./src/auth --focus logic
```

### 코딩 컨벤션 지정

```
/skill SK_code_review --target_path ./src --convention coding_style.md
```

## 리뷰 항목

| 항목 | 설명 |
|------|------|
| 코드 가독성 | 네이밍, 함수 길이, 주석 |
| 설계 원칙 | 단일 책임, 중복, 추상화 |
| 에러 처리 | 예외, 메시지, 리소스 해제 |
| 로직 정확성 | 경계값, null, 동시성 |
| 성능 | 불필요 루프, N+1, 메모리 |
| 로깅 | 로그 수준, 민감정보 |

## 이슈 심각도

| 등급 | 의미 |
|------|------|
| critical | 장애/보안 이슈, 즉시 수정 필요 |
| major | 품질 저하, 수정 권장 |
| minor | 경미한 개선 사항 |
| info | 참고 사항 |

## 출력물

- 이슈 목록 (심각도, 파일, 라인, 설명, 제안)
- 코드 품질 점수 (0-100)

## 주의사항

- SW_review Workflow에서 SK_security_review와 병렬 실행 가능
- critical 이슈가 있으면 즉시 사용자에게 알린다
