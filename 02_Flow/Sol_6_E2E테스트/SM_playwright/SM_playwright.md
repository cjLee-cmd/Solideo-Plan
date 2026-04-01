---
name: SM_playwright
type: mcp
description: Playwright 브라우저 자동화 MCP (Microsoft 공식 @playwright/mcp)
version: 1.0.0
---

# SM_playwright

## 목적
LLM이 브라우저를 직접 제어하여 웹 페이지와 상호작용하는 MCP 서버이다.
접근성 스냅샷 기반으로 동작하므로 비전 모델이 불필요하다.

## 특징
- Microsoft 공식 패키지: @playwright/mcp
- 접근성 트리 기반 (텍스트만으로 동작)
- oss-120b 모델에서 사용 가능
- 폐쇄망: npm 패키지 + 브라우저 바이너리 사전 다운로드 필요

## 서버 설정
```json
{"mcpServers":{"sm-playwright":{"type":"local","command":["npx","@playwright/mcp@latest"]}}}
```
