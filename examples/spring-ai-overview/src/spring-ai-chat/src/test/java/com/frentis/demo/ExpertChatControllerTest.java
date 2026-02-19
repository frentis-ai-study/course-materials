package com.frentis.demo;

import org.junit.jupiter.api.Test;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ExpertChatController.class)
class ExpertChatControllerTest {

    @TestConfiguration
    static class TestConfig {
        @Bean
        ChatClient.Builder chatClientBuilder() {
            ChatClient chatClient = mock(ChatClient.class);
            ChatClient.ChatClientRequestSpec requestSpec = mock(ChatClient.ChatClientRequestSpec.class);
            ChatClient.CallResponseSpec callResponseSpec = mock(ChatClient.CallResponseSpec.class);

            when(callResponseSpec.content()).thenReturn("전문가 응답입니다");
            when(requestSpec.system(anyString())).thenReturn(requestSpec);
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
    void expertEndpointReturnsResponse() throws Exception {
        mockMvc.perform(get("/chat/expert")
                        .param("role", "보안 전문가")
                        .param("message", "SQL Injection이 뭐야?"))
                .andExpect(status().isOk())
                .andExpect(content().string("전문가 응답입니다"));
    }

    @Test
    void expertEndpointWithDefaults() throws Exception {
        mockMvc.perform(get("/chat/expert"))
                .andExpect(status().isOk())
                .andExpect(content().string("전문가 응답입니다"));
    }
}
