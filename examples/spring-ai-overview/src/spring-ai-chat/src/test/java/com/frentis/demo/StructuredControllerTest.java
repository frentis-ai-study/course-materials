package com.frentis.demo;

import org.junit.jupiter.api.Test;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(StructuredController.class)
class StructuredControllerTest {

    @TestConfiguration
    static class TestConfig {
        @Bean
        @SuppressWarnings("unchecked")
        ChatClient.Builder chatClientBuilder() {
            ChatClient chatClient = mock(ChatClient.class);
            ChatClient.ChatClientRequestSpec requestSpec = mock(ChatClient.ChatClientRequestSpec.class);
            ChatClient.CallResponseSpec callResponseSpec = mock(ChatClient.CallResponseSpec.class);

            var testAnalysis = new StructuredController.TechAnalysis(
                    "Spring AI", "AI 통합 프레임워크", 85,
                    new String[]{"벤더 독립", "Spring 생태계"},
                    new String[]{"학습 곡선"}
            );

            when(callResponseSpec.entity(any(Class.class))).thenReturn(testAnalysis);
            when(requestSpec.user(anyString())).thenReturn(requestSpec);
            when(requestSpec.call()).thenReturn(callResponseSpec);
            when(chatClient.prompt()).thenReturn(requestSpec);

            ChatClient.Builder builder = mock(ChatClient.Builder.class);
            when(builder.build()).thenReturn(chatClient);
            return builder;
        }
    }

    @Autowired
    private MockMvc mockMvc;

    @Test
    void analyzeReturnsStructuredJson() throws Exception {
        mockMvc.perform(get("/analyze").param("topic", "Spring AI"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.topic").value("Spring AI"))
                .andExpect(jsonPath("$.score").value(85))
                .andExpect(jsonPath("$.pros").isArray());
    }

    @Test
    void analyzeWithDefaultTopic() throws Exception {
        mockMvc.perform(get("/analyze"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.topic").exists());
    }
}
