# 데모: Spring AI + Ollama 챗

> LO: `LO-Spring AI 개요` | 예상 시간: 5분

## 시연 목표

"Java 코드 몇 줄로 AI 챗봇 — 모델을 바꿔도 코드는 그대로, 설정 1줄만 변경"

## 사전 체크리스트

```bash
# 1. Java 21+ 확인
java -version
# → openjdk version "21.x.x" 이상이어야 함
# 미설치 시: brew install openjdk@21

# 2. Ollama 실행 확인
curl -s http://localhost:11434/api/tags | head -1
# → {"models":[...]} 응답이 와야 함
# 미실행 시: ollama serve

# 3. 모델 다운로드 확인
ollama list | grep -E "qwen3:8b|gemma3:12b"
# → 두 모델 모두 보여야 함
# 미다운로드 시:
ollama pull qwen3:8b
ollama pull gemma3:12b

# 4. 포트 충돌 확인
lsof -i :8081 | grep LISTEN
# → 아무것도 안 나와야 함 (사용 중이면 해당 프로세스 종료)

# 5. Maven 의존성 사전 다운로드 (첫 실행 시 3~5분 소요)
cd src/spring-ai-chat
./mvnw dependency:resolve
# → BUILD SUCCESS 확인

# 6. 빌드 테스트
./mvnw compile
# → BUILD SUCCESS 확인
```

## 주요 파일 경로

```
src/spring-ai-chat/
├── src/main/java/com/frentis/demo/
│   ├── ChatController.java          ← 기본 챗 (4줄)
│   ├── StreamChatController.java    ← 스트리밍 SSE (실시간 출력)
│   ├── StructuredController.java    ← 구조화 출력 (JSON 자동 매핑)
│   ├── ExpertChatController.java    ← 시스템 프롬프트 (페르소나)
│   └── SpringAiChatApplication.java
├── src/main/resources/
│   └── application.yml              ← 모델 설정 (여기서 모델명 변경)
├── src/test/java/com/frentis/demo/
│   ├── SpringAiChatApplicationTests.java  ← ChatController 단위 테스트
│   ├── ExpertChatControllerTest.java      ← ExpertChat 단위 테스트
│   ├── StructuredControllerTest.java      ← Structured 단위 테스트
│   └── ChatIntegrationTest.java           ← 통합 테스트 (Ollama 필요)
├── pom.xml
└── mvnw / mvnw.cmd
```

## API 엔드포인트

| 엔드포인트 | 설명 | 핵심 Spring AI 기능 |
|-----------|------|-------------------|
| `GET /chat?message=` | 기본 챗 | `.call().content()` |
| `GET /chat/stream?message=` | 실시간 스트리밍 (SSE) | `.stream().content()` |
| `GET /chat/expert?role=&message=` | 페르소나 설정 | `.system()` |
| `GET /analyze?topic=` | JSON 구조화 출력 | `.entity(Record.class)` |

## 시연 순서

### Step 1: 코드 보여주기 (1분)

**ChatController.java를 열고:**

```java
@GetMapping("/chat")
public String chat(@RequestParam String message) {
    return chatClient.prompt()
            .user(message)
            .call()
            .content();
}
```

- "전체 AI 챗봇 코드가 이겁니다. 4줄."
- "ChatClient 하나로 어떤 LLM이든 동일하게 호출합니다"

**application.yml을 열고:**

```yaml
spring:
  ai:
    ollama:
      chat:
        options:
          model: qwen3:8b
```

- "어떤 모델을 쓸지는 설정 파일 1줄로 결정합니다"

### Step 2: 실행 + 질문 (1분)

```bash
cd src/spring-ai-chat
./mvnw spring-boot:run
```

다른 터미널에서:

```bash
curl -G "http://localhost:8081/chat" --data-urlencode "message=인공지능이 뭔지 한 줄로 설명해줘"
```

- 응답 확인
- "지금 Ollama의 Qwen3 8B가 로컬에서 답변했습니다. 외부 서버 아닙니다"

### Step 3: 스트리밍 — ChatGPT처럼 실시간 출력 (30초)

```bash
curl -N "http://localhost:8081/chat/stream?message=Spring+AI를+한+문단으로+설명해줘"
```

- 토큰이 하나씩 실시간으로 출력됨
- "ChatGPT처럼 글자가 타이핑되듯 나옵니다. `.stream()` 한 줄 차이입니다"

### Step 4: 구조화 출력 — AI가 JSON 객체를 반환 (30초)

```bash
curl -s "http://localhost:8081/analyze?topic=Spring+AI" | python3 -m json.tool
```

- AI가 `{topic, summary, score, pros, cons}` JSON으로 응답
- "AI 응답을 Java record로 자동 매핑합니다. JSON 파싱 코드 없음"

### Step 5: 시스템 프롬프트 — AI에게 역할 부여 (30초)

```bash
curl -G "http://localhost:8081/chat/expert" \
  --data-urlencode "role=보안 전문가" \
  --data-urlencode "message=SQL Injection이 뭐야?"
```

- 같은 질문이라도 역할에 따라 답변 스타일이 달라짐
- "`.system()` 한 줄로 AI의 전문 분야를 지정합니다"

### Step 6: 모델 교체 — 벤더 독립성 (1분)

앱 종료 후 `application.yml` 수정:

```yaml
# 변경 전
model: qwen3:8b

# 변경 후
model: gemma3:12b
```

다시 실행:

```bash
./mvnw spring-boot:run
```

같은 질문:

```bash
curl -G "http://localhost:8081/chat" --data-urlencode "message=인공지능이 뭔지 한 줄로 설명해줘"
```

- "모델이 바뀌었지만, Java 코드는 한 줄도 안 고쳤습니다"
- "이게 벤더 독립성입니다. 나중에 OpenAI로 바꿔도 코드는 그대로"

## 핵심 멘트

- "AI 챗봇 전체 코드가 4줄입니다"
- "스트리밍, 구조화 출력, 페르소나까지 — 각각 코드 1~2줄 추가"
- "모델 교체는 설정 1줄 — 코드 변경 없음"
- "기존 Spring Boot 프로젝트에 의존성 하나 추가하면 AI가 됩니다"
- "교육과정에서 여기서부터 RAG, Tool Calling, MCP Agent까지 확장합니다"

## 테스트 실행

```bash
cd src/spring-ai-chat

# 단위 테스트 (Ollama 없이도 통과)
./mvnw test
# → Tests run: 10, Failures: 0 (통합 4개는 Skipped)

# 통합 테스트 (Ollama 실행 중일 때)
OLLAMA_AVAILABLE=true ./mvnw test
# → Tests run: 10, Failures: 0, Skipped: 0
```

## 백업 플랜

| 실패 시나리오 | 대응 |
|-------------|------|
| Maven 빌드 실패 | 사전에 `./mvnw dependency:resolve` 완료 확인 필수 |
| Ollama 안 뜸 | `ollama serve` 재시작 |
| 응답 느림 | "실제 환경에서는 GPU가 있으면 훨씬 빠릅니다" |
| 전체 실패 | `output/sample-response.txt` 보여주며 "이런 결과가 나옵니다" |
