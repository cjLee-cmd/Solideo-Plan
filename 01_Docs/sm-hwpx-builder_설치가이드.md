# sm-hwpx-builder 폐쇄망 설치 가이드

## 개요

sm-hwpx-builder는 마크다운 문서를 한글(hwpx) 형식으로 변환하는 MCP 서버이다.
Python hwpx 변환 라이브러리가 필요하며, 폐쇄망에서 사전 설치해야 한다.

## 사전 요구사항

- Python 3.9 이상
- lxml 라이브러리 (XML 처리용)

## 설치 방법

### 방법 1: python-hwp 패키지 사용

python-hwp는 hwp/hwpx 파일을 처리하는 오픈소스 라이브러리이다.

#### 인터넷망에서 다운로드

```bash
mkdir -p offline_packages/hwpx
pip download python-hwp lxml -d offline_packages/hwpx
```

#### 폐쇄망에서 설치

```bash
pip install --no-index --find-links=offline_packages/hwpx python-hwp lxml
```

### 방법 2: pyhwpx 패키지 사용

pyhwpx는 hwpx(Open XML) 형식 전용 처리 라이브러리이다.

#### 인터넷망에서 다운로드

```bash
mkdir -p offline_packages/hwpx
pip download pyhwpx lxml -d offline_packages/hwpx
```

#### 폐쇄망에서 설치

```bash
pip install --no-index --find-links=offline_packages/hwpx pyhwpx lxml
```

### 방법 3: 자체 hwpx_converter 구축 (권장)

hwpx는 ZIP 압축된 Open XML 형식이므로, lxml과 zipfile만으로 직접 처리할 수 있다.

#### 인터넷망에서 다운로드

```bash
mkdir -p offline_packages/hwpx
pip download lxml -d offline_packages/hwpx
```

#### 폐쇄망에서 설치

```bash
pip install --no-index --find-links=offline_packages/hwpx lxml
```

#### hwpx 파일 구조 (참고)

```
document.hwpx (ZIP 파일)
├── META-INF/
│   └── container.xml
├── Contents/
│   ├── content.hpf        # 문서 매니페스트
│   ├── header.xml          # 문서 설정
│   └── section0.xml        # 본문 내용
├── Preview/
│   └── PrvText.txt         # 미리보기 텍스트
└── mimetype                # application/hwp+zip
```

#### 핵심 변환 로직 (section0.xml 편집)

```python
from lxml import etree
import zipfile
import os

def md_to_hwpx(md_path: str, template_path: str, output_path: str):
    """마크다운을 hwpx로 변환한다."""
    # 1. 템플릿 hwpx를 압축 해제
    with zipfile.ZipFile(template_path, 'r') as z:
        z.extractall('/tmp/hwpx_work')

    # 2. section0.xml 파싱
    tree = etree.parse('/tmp/hwpx_work/Contents/section0.xml')
    root = tree.getroot()

    # 3. 마크다운 파싱 후 XML 요소로 변환
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    # ... 마크다운 → hwpx XML 변환 로직 ...

    # 4. 수정된 XML 저장
    tree.write('/tmp/hwpx_work/Contents/section0.xml',
               xml_declaration=True, encoding='utf-8')

    # 5. hwpx로 재압축
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root_dir, dirs, files in os.walk('/tmp/hwpx_work'):
            for file in files:
                file_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(file_path, '/tmp/hwpx_work')
                z.write(file_path, arcname)
```

---

## lxml 컴파일 설치 (wheel 없는 환경)

lxml은 C 확장 모듈이므로 컴파일 환경이 필요할 수 있다.

### Linux

```bash
# 빌드 도구 설치 (인터넷망에서 RPM/deb 다운로드 후 폐쇄망 설치)
# RHEL/CentOS:
sudo yum install gcc libxml2-devel libxslt-devel python3-devel
# Ubuntu/Debian:
sudo apt install gcc libxml2-dev libxslt1-dev python3-dev

# wheel 파일로 다운로드하면 컴파일 불필요 (권장)
pip download --only-binary=:all: lxml -d offline_packages/hwpx
```

### Windows

```bash
# wheel 파일로 다운로드 (컴파일 불필요)
pip download --only-binary=:all: --platform win_amd64 lxml -d offline_packages/hwpx
```

## hwpx 템플릿 파일 준비

공문, 보고서, 회의록, 제안서 양식의 hwpx 템플릿 파일을 준비하여 아래 경로에 배치한다:

```
.opencode/mcp/sm-hwpx-builder/templates/
├── gonmun.hwpx       # 공문 양식
├── report.hwpx       # 보고서 양식
├── minutes.hwpx      # 회의록 양식
└── proposal.hwpx     # 제안서 양식
```

템플릿은 한글 프로그램에서 양식을 만들고 hwpx로 저장하면 된다.

## 설치 확인

```bash
python3 -c "from lxml import etree; print('lxml OK:', etree.LXML_VERSION)"
python3 -c "import zipfile; print('zipfile OK')"
```

## 주의사항

- .hwp(레거시 바이너리)는 지원하지 않는다. .hwpx(Open XML)만 지원한다
- 템플릿 기반 변환 시 한글 프로그램에서 만든 hwpx 템플릿이 필요하다
- lxml은 반드시 **동일 OS/Python 버전**의 wheel을 다운로드해야 한다
