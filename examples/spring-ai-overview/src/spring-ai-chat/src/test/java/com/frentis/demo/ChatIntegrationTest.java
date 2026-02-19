package com.frentis.demo;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.EnabledIfEnvironmentVariable;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * 통합 테스트 — 실제 Ollama 연결 검증.
 *
 * Ollama가 실행 중일 때만 동작합니다:
 *   OLLAMA_AVAILABLE=true ./mvnw test
 */
@SpringBootTest
@AutoConfigureMockMvc
@EnabledIfEnvironmentVariable(named = "OLLAMA_AVAILABLE", matches = "true")
class ChatIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void chatReturnsNonEmptyResponse() throws Exception {
        mockMvc.perform(get("/chat").param("message", "1+1은?"))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.not(org.hamcrest.Matchers.emptyString())));
    }

    @Test
    void chatHandlesKoreanMessage() throws Exception {
        mockMvc.perform(get("/chat").param("message", "안녕하세요"))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.not(org.hamcrest.Matchers.emptyString())));
    }

    @Test
    void expertEndpointWithRole() throws Exception {
        mockMvc.perform(get("/chat/expert")
                        .param("role", "Java 개발자")
                        .param("message", "record가 뭐야?"))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.not(org.hamcrest.Matchers.emptyString())));
    }

    @Test
    void analyzeReturnsJson() throws Exception {
        mockMvc.perform(get("/analyze").param("topic", "Java"))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("topic")));
    }
}
