package com.frentis.demo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 감성 분석 — AI가 텍스트를 분석하여 구조화된 감성 데이터를 반환합니다.
 *
 * 핵심: AI 응답 → Java record → JSON → 프론트엔드 시각화. 파싱 코드 없음.
 */
@RestController
public class SentimentController {

    private final ChatClient chatClient;

    public SentimentController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    public enum Sentiment { POSITIVE, NEUTRAL, NEGATIVE }

    public record SentimentResult(
            Sentiment sentiment,
            int score,
            String summary,
            String[] keywords
    ) {}

    @GetMapping("/sentiment")
    public SentimentResult analyze(
            @RequestParam String text) {
        return chatClient.prompt()
                .system("""
                        당신은 감성 분석 엔진입니다.
                        주어진 텍스트의 감성을 분석하세요.
                        sentiment: POSITIVE, NEUTRAL, NEGATIVE 중 하나.
                        score: 0(매우 부정)~100(매우 긍정) 사이 정수.
                        summary: 분석 요약 한 문장 (한국어).
                        keywords: 감성을 드러내는 핵심 키워드 3~5개 (한국어).""")
                .user(text)
                .call()
                .entity(SentimentResult.class);
    }
}
