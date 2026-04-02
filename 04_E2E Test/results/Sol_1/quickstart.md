# Quickstart Guide — 내부결재시스템

> **버전**: 1.0  
> **작성일**: 2026-04-02

---

## 1. 환경 요구사항

| 항목 | 버전 | 비고 |
|------|------|------|
| JDK | 17 | 폐쇄망 내부 JDK 미러에서 제공 |
| Maven | 3.9+ | settings.xml 에 내부 Nexus 설정 필수 |
| Oracle DB | 19c | 인사DB 연동용 별도 스키마 |
| OS | RHEL 8+ / Ubuntu 20.04+ | |

## 2. 프로젝트 설정

### 2.1 Clone
```bash
git clone <internal-repo-url>/approval-system.git
cd approval-system
```

### 2.2 Maven 설정 (폐쇄망 Nexus)
`~/.m2/settings.xml`:
```xml
<settings>
  <mirrors>
    <mirror>
      <id>internal-nexus</id>
      <mirrorOf>*</mirrorOf>
      <url>http://internal-nexus:8081/repository/maven-public/</url>
    </mirror>
  </mirrors>
</settings>
```

### 2.3 빌드
```bash
mvn clean package -DskipTests
```

### 2.4 테스트 실행
```bash
mvn test
```

## 3. 로컬 실행

### 3.1 환경변수 설정
```bash
export DB_URL=jdbc:oracle:thin:@localhost:1521:APPROVAL
export DB_USERNAME=approval_admin
export DB_PASSWORD=secure_password
export HR_DB_URL=jdbc:oracle:thin:@hr-db:1521:HRDB
export HR_DB_USERNAME=hr_reader
export HR_DB_PASSWORD=hr_password
export FILE_UPLOAD_PATH=/data/approval/uploads
export JWT_SECRET=your-256-bit-secret-key-here-min-32-chars
```

### 3.2 실행
```bash
java -jar target/approval-system-1.0.0.jar
```

### 3.3 접속
- API: `http://localhost:8080/api/v1`
- Swagger: `http://localhost:8080/swagger-ui.html`

## 4. DB 초기화

```sql
-- 스키마 생성
CREATE USER approval_admin IDENTIFIED BY secure_password;
GRANT CONNECT, RESOURCE TO approval_admin;

-- 테이블 생성 (schema.sql 실행)
@schema.sql

-- 초기 데이터 (data.sql 실행)
@data.sql
```

## 5. 프로젝트 구조
```
approval-system/
├── src/main/java/com/solideo/approval/
│   ├── ApprovalApplication.java
│   ├── config/          # 설정 클래스
│   ├── controller/      # REST 컨트롤러
│   ├── service/         # 비즈니스 로직
│   ├── repository/      # JPA Repository
│   ├── entity/          # JPA 엔티티
│   ├── dto/             # DTO
│   ├── security/        # 인증/인가
│   ├── scheduler/       # 스케줄러 (HR 동기화)
│   └── exception/       # 예외 처리
├── src/main/resources/
│   ├── application.yml
│   ├── schema.sql
│   └── data.sql
├── src/test/java/
└── pom.xml
```
