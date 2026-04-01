# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

이 디렉토리는 **(주)솔리데오 폐쇄망 LLM 구축 프로젝트(SolCode_Lab)**의 기획/문서 관리 워크스페이스이다. 코드 리포지토리가 아닌 **계획 문서와 Notion 연동** 중심의 프로젝트 관리 공간이다.

- **프로젝트명**: SolCode_Lab
- **목적**: 행정망 소프트웨어 개발 회사 특성에 맞는 폐쇄망 내 바이브코딩 환경 구축
- **폐쇄망 내부 구성**: opencode IDE + oss-120b 모델 + H100 x 4 EA

## Notion 연동

프로젝트 계획/관리 문서는 아래 Notion 사이트에서 조직화하여 관리한다:
- **반영계획 페이지**: `https://www.notion.so/powersolution/3357ece7e00580e98470fc614c962ea0`
- **상위 프로젝트**: `Solideo-Local AI System` (Notion Projects DB 내)

Notion 페이지를 조회/수정할 때는 `mcp__claude_ai_Notion__notion-fetch` 등 Notion MCP 도구를 사용한다.

## 공급 범위 (개발 산출물)

SolCode_Lab에서 폐쇄망 개발자에게 제공할 항목:
1. **Local MCP** — 폐쇄망 내부 MCP 서버
2. **Skill** — 워크플로우 단계별 재사용 가능한 skill 모듈
3. **Workflow** — 계획 → 분석 → 생성 → 수정 → 리뷰 → 문서생성 파이프라인
4. **Agent / Sub-Agent** — 작업별 전문 에이전트

## 워크플로우 파이프라인

| 단계 | 핵심 도구/파일 | 설명 |
|------|---------------|------|
| 계획 | Speckit | 신규 소프트웨어 디자인 설계, 사용자 검증 후 생성 |
| 분석 | - | 기존 소스코드 분석 및 문서화 |
| 생성 | design.md | 설계문서 기반 코드 생성, 테스트 코드 생성/실행, 결과 문서화 |
| 수정 | verify.md | 코드 수정, 영향범위 검토, 테스트 실행, 결과 문서화 |
| 리뷰 | - | 보안 등 문서기반 검증 후 이슈사항 저장 |
| 문서생성 | md, hwpx | 마크다운 및 한글(hwpx) 문서 생성 |

## 문서 관리 구조

- **외부 (인터넷망)**: 이 디렉토리 + Notion에서 계획/설계 문서 관리
- **내부 (폐쇄망)**: Obsidian Vault에 개발 문서 조직화
- **컨텍스트 관리**: 별도 서버 없이 폴더링 구조로 관리

## 이 디렉토리에서의 작업 시 유의사항

- 이 디렉토리는 기획 문서 중심이므로 코드 빌드/테스트 명령은 없다
- Notion 페이지 내용과 `jun.md`의 내용을 동기화 상태로 유지할 것
- 새 문서 작성 시 마크다운 형식 사용, 필요시 `/md2hwpx`로 hwpx 변환
- 폐쇄망 환경 제약(인터넷 불가)을 항상 고려하여 설계할 것
