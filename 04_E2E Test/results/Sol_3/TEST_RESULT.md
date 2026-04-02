# Sol_3 생성 — 테스트 결과

실행일: 2026-04-02
환경: macOS (인터넷망)
상태: **전체 미실행**

## 미실행 사유

Sol_3(생성)은 design.md 기반으로 **실제 소스코드를 생성하고 빌드/테스트를 실행**해야 한다.
- sk-code-gen: 코드 생성 자체는 가능하나, 생성된 코드의 품질 검증이 필요
- sk-test-gen: 테스트 코드 생성
- sk-test-run: **빌드 환경(Maven/Gradle, JDK)이 필요** → 무료 모델 환경에서 실행 불가
- sk-gen-report: 테스트 결과가 있어야 보고서 생성 가능
- sa-generator: 위 4개 스킬을 순차 호출 + 테스트 실패 시 자동 수정/재시도

## 로컬 실행 방법

### 사전 준비

```bash
# 디렉토리 + design.md 준비 (Sol_1 결과 활용)
mkdir -p /tmp/e2e_sol3/90_Result_Doc && cd /tmp/e2e_sol3 && git init

# design.md 복사 (Sol_1에서 생성된 것 또는 직접 작성)
cp /path/to/design.md 90_Result_Doc/design.md
```

### 폐쇄망 필수 환경

| 항목 | 요구사항 |
|------|---------|
| JDK | Java 17 |
| 빌드 | Maven 3.9+ 또는 Gradle 8+ |
| DB | Oracle 19c (테스트용) |
| 내부 저장소 | Maven 미러 (폐쇄망 내) |

### TC-3.1: sk-code-gen

```bash
opencode run --dir . -m "모델명" \
  "/sk-code-gen 90_Result_Doc/design.md를 기반으로 코드를 생성해줘"

# 검증
find src/ -name "*.java" | sort                          # 파일 목록
grep -rn "@GetMapping\|@PostMapping\|@PutMapping" src/   # API 엔드포인트
grep -rn "BCrypt\|@PreAuthorize\|AuditLog" src/          # 보안 코드
grep -rnE "https?://" src/                                # 외부 URL (없어야)
ls 90_Result_Doc/file_manifest.md                         # 매니페스트
find 90_Result_Doc/ -name "*.json"                        # json (없어야)
```

### TC-3.2: sk-test-gen

```bash
opencode run --dir . -m "모델명" \
  "/sk-test-gen 생성된 코드에 대한 테스트 코드를 작성해줘"

# 검증
find src/test/ -name "*Test.java" | sort
grep -rn "@DisplayName" src/test/                         # 한국어 테스트명
ls 90_Result_Doc/test_manifest.md
```

### TC-3.3: sk-test-run

```bash
# Maven 빌드 환경 필요
opencode run --dir . -m "모델명" "/sk-test-run 테스트를 실행해줘"

# 검증
ls 90_Result_Doc/test_result.md
grep -iE "통과|실패|커버리지" 90_Result_Doc/test_result.md
```

### TC-3.4: sk-gen-report

```bash
opencode run --dir . -m "모델명" \
  "/sk-gen-report 생성 결과를 종합 보고서로 작성해줘"

# 검증
ls 90_Result_Doc/generation_report.md
grep -c "^## " 90_Result_Doc/generation_report.md   # 6 이상
```

### TC-3.5: sa-generator 통합

```bash
opencode run --dir . -m "모델명" --agent sa-generator \
  "design.md 기반으로 전체 생성 워크플로우를 수행해줘"

# 검증
for f in file_manifest.md test_manifest.md test_result.md generation_report.md; do
  [ -f "90_Result_Doc/$f" ] && echo "✅ $f" || echo "❌ $f"
done
find . -name "*.json" | grep -v node_modules
```
