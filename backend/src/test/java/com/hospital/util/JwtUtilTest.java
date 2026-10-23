package com.hospital.util;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class JwtUtilTest {

    private static final String SECRET = "hospital-registration-jwt-secret-key-2024";

    @Test
    @DisplayName("签发的 token 可以解析出身份与角色")
    void issueAndParse() {
        JwtUtil jwtUtil = new JwtUtil(SECRET, 1);
        String token = jwtUtil.issue(42L, "USER");

        Claims claims = jwtUtil.parse(token);

        assertEquals("42", claims.getSubject());
        assertEquals("USER", claims.get("role", String.class));
    }

    @Test
    @DisplayName("使用不同密钥无法通过校验")
    void rejectsTokenSignedByAnotherSecret() {
        JwtUtil issuer = new JwtUtil(SECRET, 1);
        JwtUtil verifier = new JwtUtil("another-hospital-registration-secret-key", 1);
        String token = issuer.issue(1L, "ADMIN");

        assertThrows(JwtException.class, () -> verifier.parse(token));
    }
}
