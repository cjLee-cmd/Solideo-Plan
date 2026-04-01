---
name: SW_documentation
type: workflow
description: 문서 유형 판별 - 생성 - 변환 - 저장 Workflow
version: 1.0.0
---

# SW_documentation

## 목적

문서 유형을 판별하고, 마크다운 생성, 필요시 hwpx 변환, Obsidian Vault 저장까지의 전체 흐름을 관리한다.

## 워크플로우 단계

```
[시작]
  |
  v
[Step 1] 문서 유형 판별
  - 입력: doc_type, source_data
  |
  v
[Step 2] SK_doc_md 실행
  - 입력: doc_type, source_data
  - 출력: {doc_type}.md
  |
  v
[판단] hwpx 변환 필요?
  |
  +-- 필요 --> [Step 3] SK_doc_hwpx 실행
  |             - 입력: {doc_type}.md, template
  |             - 출력: {doc_type}.hwpx
  |             |
  |             v
  +-- 불필요 --+
               |
               v
[Step 4] SM_obsidian_sync로 Vault 저장
  - 입력: 생성된 문서 (md, hwpx)
  - 출력: 저장 확인
  |
  v
[완료]
```

## 단계별 입출력 매핑

| 단계 | 입력 | 출력 | 다음 |
|------|------|------|------|
| Step 1 | doc_type, source_data | 판별 결과 | Step 2 |
| Step 2 | doc_type, source_data | .md 파일 | 판단 |
| Step 3 | .md 파일, template | .hwpx 파일 | Step 4 |
| Step 4 | .md (.hwpx) 파일 | 저장 확인 | 완료 |

## hwpx 변환 조건

- 사용자가 hwpx를 명시적으로 요청한 경우
- doc_type이 공문(gonmun), 제안서(proposal)인 경우 기본 변환

## 사용 Agent

- SA_documenter: 이 Workflow를 총괄 관리
