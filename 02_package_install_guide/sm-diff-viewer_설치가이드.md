# sm-diff-viewer 폐쇄망 설치 가이드

## 개요

sm-diff-viewer는 Git을 사용하여 코드 변경 전후의 차이를 비교하는 MCP 서버이다.
Git만 설치되어 있으면 동작한다.

## 사전 요구사항

- Python 3.9 이상 (MCP 서버 실행용)
- Git 2.x 이상

## Git 폐쇄망 설치

### Linux (RHEL/CentOS)

#### 인터넷망에서 RPM 다운로드

```bash
# 인터넷 PC에서 (동일 OS 버전)
yumdownloader --resolve --destdir=./offline_rpm git git-core
```

#### 폐쇄망에서 설치

```bash
sudo rpm -ivh ./offline_rpm/*.rpm
```

### Linux (Ubuntu/Debian)

#### 인터넷망에서 deb 다운로드

```bash
apt-get download git
# 의존성 포함 다운로드
apt-get download $(apt-cache depends --recurse --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances git | grep "^\w" | sort -u)
```

#### 폐쇄망에서 설치

```bash
sudo dpkg -i ./offline_deb/*.deb
```

### Windows

#### 인터넷망에서 설치 파일 다운로드

```
https://git-scm.com/download/win 에서 Portable 버전 다운로드
Git-2.x.x-64-bit.tar.bz2 (Portable)
```

#### 폐쇄망에서 설치

```
다운로드한 파일을 USB로 복사 후 압축 해제
PATH 환경변수에 git/bin 디렉토리 추가
```

### macOS

```bash
# Xcode Command Line Tools에 포함
xcode-select --install
# 또는 git-osx-installer에서 pkg 다운로드 후 USB 이동
```

## 설치 확인

```bash
git --version
# 출력 예: git version 2.43.0

# diff 기능 테스트
mkdir /tmp/test_git && cd /tmp/test_git
git init
echo "hello" > test.txt
git add test.txt && git commit -m "init"
echo "world" >> test.txt
git diff  # diff 출력 확인
rm -rf /tmp/test_git
```

## Git 폐쇄망 설정

```bash
# 외부 접근 차단 확인 (안전장치)
git config --global http.proxy ""
git config --global https.proxy ""

# 내부 Git 서버 사용 시
git config --global url."http://내부서버:3000/".insteadOf "https://github.com/"
```

## 주의사항

- sm-diff-viewer는 git이 초기화된 프로젝트(`.git` 디렉토리 존재)에서만 정상 동작한다
- git이 없는 프로젝트에서는 에러를 반환한다
