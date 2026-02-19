package com.frentis.demo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 구조화 출력 — AI 응답을 Java 객체로 자동 매핑합니다.
 *
 * 핵심: .entity(record.class) 한 줄로 JSON 파싱 없이 타입 안전한 객체 반환.
 */
@RestController
public class StructuredController {

    private final ChatClient chatClient;

    public StructuredController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    // AI가 반환할 구조체
    public record TechAnalysis(
            String topic,
            String summary,
            int score,
            String[] pros,
            String[] cons
    ) {}

    // GET /analyze?topic=Spring AI
    // curl -s "http://localhost:8081/analyze?topic=Spring+AI" | python3 -m json.tool
    @GetMapping("/analyze")
    public TechAnalysis analyze(
            @RequestParam(defaultValue = "Spring AI") String topic) {
        return chatClient.prompt()
                .user("'" + topic + "'에 대해 기술 분석해줘. 한국어로 작성해.")
                .call()
                .entity(TechAnalysis.class);
    }
}
