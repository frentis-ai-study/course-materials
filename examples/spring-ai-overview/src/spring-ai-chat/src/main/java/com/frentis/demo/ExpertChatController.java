package com.frentis.demo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 프롬프트 엔지니어링 Lab — 역할, 대상, 형식, 말투 조합으로 응답 변화를 확인합니다.
 *
 * 핵심: .system() 하나로 AI의 전체 행동을 제어. 같은 질문도 프롬프트에 따라 완전히 다른 답변.
 */
@RestController
public class ExpertChatController {

    private final ChatClient chatClient;

    public ExpertChatController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    @GetMapping("/chat/expert")
    public String expert(
            @RequestParam(defaultValue = "Java 시니어 개발자") String role,
            @RequestParam(defaultValue = "Spring AI의 장점을 알려줘") String message,
            @RequestParam(defaultValue = "") String audience,
            @RequestParam(defaultValue = "") String format,
            @RequestParam(defaultValue = "") String tone) {

        StringBuilder sb = new StringBuilder();
        sb.append(String.format("""
                당신은 '%s' 역할을 완벽히 연기합니다.
                반드시 그 역할의 관점, 전문 용어, 말투, 비유를 사용하세요.
                역할과 무관한 기술 용어는 절대 쓰지 마세요.
                한국어로 답변하세요.""", role));

        if (!audience.isEmpty()) {
            sb.append(String.format("\n설명 대상은 '%s'입니다. 이 대상의 수준에 맞춰 난이도를 조절하세요.", audience));
        }
        if (!format.isEmpty()) {
            sb.append(String.format("\n출력 형식: %s", format));
        }
        if (!tone.isEmpty()) {
            sb.append(String.format("\n말투: %s", tone));
        }

        return chatClient.prompt()
                .system(sb.toString())
                .user(message)
                .call()
                .content();
    }
}
