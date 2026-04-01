# sm-test-runner 폐쇄망 설치 가이드

## 개요

sm-test-runner는 프로젝트의 테스트 프레임워크를 실행하고 결과를 수집하는 MCP 서버이다.
지원하는 테스트 프레임워크별로 런타임과 패키지를 폐쇄망에 설치해야 한다.

## 사전 요구사항

- Python 3.9 이상 (MCP 서버 실행용, 모든 MCP 공통)

## 프레임워크별 설치

### 1. pytest (Python 프로젝트)

#### 인터넷망에서 패키지 다운로드

```bash
# 인터넷 연결된 PC에서 실행
mkdir -p offline_packages/pytest
pip download pytest pytest-cov pytest-json-report -d offline_packages/pytest
```

#### 폐쇄망으로 이동 후 설치

```bash
# USB 등으로 offline_packages/ 디렉토리를 폐쇄망에 복사 후
pip install --no-index --find-links=offline_packages/pytest pytest pytest-cov pytest-json-report
```

#### 설치 확인

```bash
python3 -m pytest --version
```

---

### 2. JUnit 5 (Java/Maven 프로젝트)

#### 인터넷망에서 Maven 로컬 저장소 구성

```bash
# 테스트 대상 프로젝트의 pom.xml이 있는 디렉토리에서
mvn dependency:go-offline -Dmaven.repo.local=./offline_repo
# 또는 전체 의존성 포함
mvn dependency:copy-dependencies -DoutputDirectory=./offline_libs
```

#### 폐쇄망 Maven 설정

```xml
<!-- 폐쇄망 PC의 ~/.m2/settings.xml -->
<settings>
  <localRepository>/path/to/offline_repo</localRepository>
  <mirrors>
    <mirror>
      <id>local-repo</id>
      <mirrorOf>*</mirrorOf>
      <url>file:///path/to/offline_repo</url>
    </mirror>
  </mirrors>
</settings>
```

#### Gradle 프로젝트의 경우

```groovy
// build.gradle에 로컬 저장소 추가
repositories {
    maven { url "file:///path/to/offline_repo" }
}
```

#### 설치 확인

```bash
mvn --version
java -version
```

---

### 3. Jest (JavaScript/Node.js 프로젝트)

#### 인터넷망에서 npm 패키지 다운로드

```bash
# 방법 1: npm pack으로 tgz 다운로드
mkdir -p offline_packages/jest
cd offline_packages/jest
npm pack jest
npm pack @jest/core

# 방법 2: 프로젝트 디렉토리에서 node_modules 통째로 복사
npm install
tar czf node_modules_backup.tar.gz node_modules/
```

#### 폐쇄망에서 설치

```bash
# 방법 1: tgz에서 설치
npm install --offline ./offline_packages/jest/*.tgz

# 방법 2: node_modules 복원
tar xzf node_modules_backup.tar.gz
```

#### npm 오프라인 레지스트리 구성 (권장)

```bash
# 인터넷망에서 verdaccio 로컬 레지스트리 구축 후 패키지 동기화
# 폐쇄망에 verdaccio 서버를 설치하고 동기화된 패키지 배포
npm config set registry http://localhost:4873
```

#### 설치 확인

```bash
node --version
npx jest --version
```

---

### 4. go test (Go 프로젝트)

#### 인터넷망에서 모듈 캐시 다운로드

```bash
# 프로젝트 디렉토리에서
go mod download
# 모듈 캐시 복사
cp -r $GOPATH/pkg/mod ./offline_gomod
# 또는 vendor 디렉토리 생성
go mod vendor
```

#### 폐쇄망에서 설정

```bash
# GOFLAGS로 vendor 모드 강제
export GOFLAGS="-mod=vendor"
# 또는 GOPATH에 오프라인 모듈 배치
export GOPATH=/path/to/offline_gomod
export GONOSUMCHECK=*
export GONOSUMDB=*
export GOFLAGS="-mod=mod"
```

#### 설치 확인

```bash
go version
go test ./... 2>&1 | head -5
```

---

### 5. NUnit (.NET 프로젝트)

#### 인터넷망에서 NuGet 패키지 다운로드

```bash
# 프로젝트 디렉토리에서
dotnet restore --packages ./offline_nuget
```

#### 폐쇄망 NuGet 설정

```xml
<!-- nuget.config -->
<configuration>
  <packageSources>
    <clear />
    <add key="local" value="/path/to/offline_nuget" />
  </packageSources>
</configuration>
```

#### 설치 확인

```bash
dotnet --version
dotnet test --list-tests
```

---

## 공통 주의사항

1. 모든 패키지 다운로드는 **폐쇄망과 동일한 OS/아키텍처**의 인터넷 PC에서 수행해야 한다
2. Python 패키지는 wheel 형식(.whl)으로 다운로드해야 컴파일 없이 설치 가능하다
3. 다운로드한 패키지의 **해시 검증**을 수행하여 무결성을 확인하라
4. 사용하는 프레임워크만 설치하면 된다. 전체를 설치할 필요 없다
