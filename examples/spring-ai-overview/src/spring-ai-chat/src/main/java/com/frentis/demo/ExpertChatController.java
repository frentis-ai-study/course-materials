package com.frentis.demo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 시스템 프롬프트 — AI에게 역할(페르소나)을 부여합니다.
 *
 * 핵심: .system() 한 줄로 AI의 전문 분야와 답변 스타일을 지정.
 */
@RestController
public class ExpertChatController {

    private final ChatClient chatClient;

    public ExpertChatController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    // GET /chat/expert?role=보안 전문가&message=SQL Injection이 뭐야?
    // curl -G "http://localhost:8081/chat/expert" \
    //   --data-urlencode "role=보안 전문가" \
    //   --data-urlencode "message=SQL Injection이 뭐야?"
    @GetMapping("/chat/expert")
    public String expert(
            @RequestParam(defaultValue = "Java 시니어 개발자") String role,
            @RequestParam(defaultValue = "Spring AI의 장점을 알려줘") String message) {
        return chatClient.prompt()
                .system("당신은 " + role + "입니다. 전문적이면서도 이해하기 쉽게 한국어로 답변하세요.")
                .user(message)
                .call()
                .content();
    }
}
