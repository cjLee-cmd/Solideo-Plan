# sm-obsidian-sync 폐쇄망 설치 가이드

## 개요

sm-obsidian-sync는 Obsidian Vault 폴더 구조에 문서를 저장하고 조회하는 MCP 서버이다.
Python 표준 라이브러리만 사용하므로 추가 패키지 설치가 필요 없다.

## 사전 요구사항

- Python 3.9 이상 (유일한 요구사항)

## Python 3 폐쇄망 설치

sm-obsidian-sync 뿐 아니라 모든 MCP 서버가 Python 3을 필요로 하므로, 이 섹션은 공통 설치 가이드이다.

### Linux (RHEL/CentOS)

#### 인터넷망에서 RPM 다운로드

```bash
yumdownloader --resolve --destdir=./offline_rpm python3 python3-libs python3-pip
```

#### 폐쇄망에서 설치

```bash
sudo rpm -ivh ./offline_rpm/*.rpm
```

### Linux (Ubuntu/Debian)

#### 인터넷망에서 deb 다운로드

```bash
apt-get download python3 python3-minimal python3-pip
```

#### 폐쇄망에서 설치

```bash
sudo dpkg -i ./offline_deb/*.deb
```

### Windows

#### 인터넷망에서 설치 파일 다운로드

```
https://www.python.org/downloads/ 에서 Windows installer 다운로드
python-3.12.x-amd64.exe
```

#### 폐쇄망에서 설치

```
다운로드한 exe를 USB로 복사 후 실행
"Add Python to PATH" 체크 필수
```

### macOS

```bash
# Homebrew 사용 (인터넷 필요)
brew install python3
# 또는 python.org에서 pkg 다운로드 후 USB 이동
```

---

## Obsidian 폐쇄망 설치

### 인터넷망에서 다운로드

```
https://obsidian.md/download 에서 OS에 맞는 설치 파일 다운로드
- Linux: Obsidian-x.x.x.AppImage
- Windows: Obsidian-x.x.x.exe
- macOS: Obsidian-x.x.x-universal.dmg
```

### 폐쇄망에서 설치

```
USB로 설치 파일을 복사 후 실행하여 설치
```

### Vault 초기 설정

```bash
# Vault 디렉토리 생성 (sm-obsidian-sync가 사용할 경로)
mkdir -p /path/to/vault

# Obsidian에서 "Open folder as vault" 선택 후 위 경로 지정
```

---

## sm-obsidian-sync 폴더 구조

서버가 자동으로 아래 구조를 생성한다:

```
/path/to/vault/
├── 프로젝트A/
│   ├── design/          # 설계 문서
│   ├── analysis/        # 분석 문서
│   ├── test_report/     # 테스트 보고서
│   ├── review/          # 리뷰 보고서
│   ├── minutes/         # 회의록
│   ├── proposal/        # 제안서
│   └── manual/          # 사용자 매뉴얼
├── 프로젝트B/
│   └── ...
```

## 설치 확인

```bash
# Python 확인
python3 --version

# MCP 서버 동작 확인
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python3 .opencode/mcp/sm-obsidian-sync/server.py
# 정상 출력: {"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2024-11-05", ...}}

# Vault 경로 쓰기 권한 확인
touch /path/to/vault/test_write && rm /path/to/vault/test_write && echo "OK"
```

## 주의사항

- Vault 경로에 대한 읽기/쓰기 권한이 필요하다
- 저장 시 YAML frontmatter(project, type, created, author, tags)가 자동 추가된다
- Obsidian에서 바로 열어볼 수 있는 표준 마크다운 형식으로 저장된다
- 이 서버는 외부 패키지 의존성이 없으므로 Python 3만 있으면 즉시 사용 가능하다
