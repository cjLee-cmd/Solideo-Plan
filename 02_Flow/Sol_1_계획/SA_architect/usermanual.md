---
name: SA_architect 사용자 매뉴얼
version: 1.0.0
---

# SA_architect 사용자 매뉴얼

## 개요

소프트웨어 아키텍처 설계를 총괄하는 Agent이다. 계획 Workflow를 관리하고, 설계 Skill들을 조율한다.

## opencode에서 사용하기

### Agent 직접 호출

```
/agent SA_architect
```

호출 후 대화형으로 프로젝트 요구사항을 전달하면 된다.

### Workflow를 통한 호출

```
/workflow SW_planning
```

SW_planning 실행 시 SA_architect가 자동으로 총괄 Agent로 동작한다.

## Agent가 수행하는 작업

1. 사용자로부터 프로젝트 요구사항을 수집한다
2. SK_design_spec을 호출하여 설계 문서를 생성한다
3. SK_design_review를 호출하여 사용자 검토를 진행한다
4. 피드백을 반영하여 설계를 수정한다
5. 최종 확정된 design_final.md를 산출한다

## 대화 예시

```
사용자: 내부 문서관리 시스템을 설계해줘
SA_architect: 문서관리 시스템 설계를 시작하겠습니다.
  몇 가지 확인이 필요합니다.
  1. 관리할 문서 유형은 무엇입니까? (공문, 보고서, 회의록 등)
  2. 예상 사용자 수는 몇 명입니까?
  3. 기존에 사용 중인 시스템이 있습니까?
  4. 특별히 선호하는 기술스택이 있습니까?

사용자: 공문과 보고서, 사용자 50명, 기존 전자결재 연동 필요, Java 선호

SA_architect: 확인했습니다. SK_design_spec을 실행하여 설계 문서를 생성합니다...
```

## 주의사항

- SA_architect는 보안 요구사항을 절대 생략하지 않는다
- 폐쇄망 호환성을 자동으로 검증한다
- 불명확한 요구사항은 반드시 사용자에게 되묻는다
