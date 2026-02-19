package com.frentis.demo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

/**
 * 스트리밍 챗 — ChatGPT처럼 토큰이 실시간으로 출력됩니다.
 *
 * 핵심: .stream().content() 한 줄 차이로 일반 호출이 스트리밍으로 변경.
 */
@RestController
public class StreamChatController {

    private final ChatClient chatClient;

    public StreamChatController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    // GET /chat/stream?message=Spring AI가 뭔지 설명해줘
    // curl -N "http://localhost:8081/chat/stream?message=Spring+AI가+뭔지+설명해줘"
    @GetMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> stream(
            @RequestParam(defaultValue = "Spring AI를 한 문단으로 설명해줘") String message) {
        return chatClient.prompt()
                .user(message)
                .stream()
                .content();
    }
}
