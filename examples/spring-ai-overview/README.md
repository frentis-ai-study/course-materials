# 데모: Spring AI + Ollama 챗

> LO: `LO-Spring AI 개요` | 예상 시간: 3분

## 시연 목표

"Java 코드 몇 줄로 AI 챗봇 — 모델을 바꿔도 코드는 그대로, 설정 1줄만 변경"

## 사전 요구사항

- Java 21+ 설치
- Maven 설치
- Ollama 설치 및 실행 중 (`ollama serve`)
- 모델 2개 다운로드 완료

```bash
# 사전 준비 (시연 전 완료)
ollama pull qwen3:8b
ollama pull gemma3:12b

# Maven 의존성 미리 다운로드 (시연 중 대기 방지)
cd src/spring-ai-chat
./mvnw dependency:resolve
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

## 백업 플랜

| 실패 시나리오 | 대응 |
|-------------|------|
| Maven 빌드 실패 | 사전에 `./mvnw dependency:resolve` 완료 확인 필수 |
| Ollama 안 뜸 | `ollama serve` 재시작 |
| 응답 느림 | "실제 환경에서는 GPU가 있으면 훨씬 빠릅니다" |
| 전체 실패 | `output/sample-response.txt` 보여주며 "이런 결과가 나옵니다" |
