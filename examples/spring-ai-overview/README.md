# 데모: Spring AI + Ollama 챗

> LO: `LO-Spring AI 개요` | 예상 시간: 3분

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
│   ├── ChatController.java          ← 핵심 코드 (4줄)
│   └── SpringAiChatApplication.java
├── src/main/resources/
│   └── application.yml              ← 모델 설정 (여기서 모델명 변경)
├── src/test/java/com/frentis/demo/
│   ├── SpringAiChatApplicationTests.java  ← 단위 테스트
│   └── ChatIntegrationTest.java           ← 통합 테스트 (Ollama 필요)
├── pom.xml
└── mvnw / mvnw.cmd
```

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

### Step 3: 모델 교체 — 벤더 독립성 (1분)

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
- "모델 교체는 설정 1줄 — 코드 변경 없음"
- "기존 Spring Boot 프로젝트에 의존성 하나 추가하면 AI가 됩니다"
- "교육과정에서 여기서부터 RAG, Tool Calling, MCP Agent까지 확장합니다"

## 테스트 실행

```bash
cd src/spring-ai-chat

# 단위 테스트 (Ollama 없이도 통과)
./mvnw test
# → Tests run: 4, Failures: 0 (통합 2개는 Skipped)

# 통합 테스트 (Ollama 실행 중일 때)
OLLAMA_AVAILABLE=true ./mvnw test
# → Tests run: 4, Failures: 0, Skipped: 0
# → 약 25초 소요 (Ollama 응답 생성 시간 포함)
```

## 백업 플랜

| 실패 시나리오 | 대응 |
|-------------|------|
| Maven 빌드 실패 | 사전에 `./mvnw dependency:resolve` 완료 확인 필수 |
| Ollama 안 뜸 | `ollama serve` 재시작 |
| 응답 느림 | "실제 환경에서는 GPU가 있으면 훨씬 빠릅니다" |
| 전체 실패 | `output/sample-response.txt` 보여주며 "이런 결과가 나옵니다" |
