package com.frentis.demo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Spring AI Chat 데모 컨트롤러
 *
 * 핵심 포인트: ChatClient 하나로 어떤 LLM이든 동일하게 호출.
 * Ollama → OpenAI로 바꿔도 이 코드는 변경 없음.
 */
@RestController
public class ChatController {

    private final ChatClient chatClient;

    // Spring AI가 자동으로 Ollama ChatClient를 주입
    public ChatController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    // GET /chat?message=안녕하세요
    @GetMapping("/chat")
    public String chat(@RequestParam(defaultValue = "안녕하세요! 자기소개 해줘.") String message) {
        return chatClient.prompt()
                .user(message)
                .call()
                .content();
    }
}
