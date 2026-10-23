package com.hospital.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.hospital.common.R;
import com.hospital.common.Role;
import com.hospital.common.UserContext;
import com.hospital.util.JwtUtil;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 * 接口鉴权：
 * 1. 白名单接口（登录、科室/医生/排班查询、导诊）直接放行；
 * 2. /api/admin/** 以及科室/医生/排班的写接口要求 ADMIN；
 * 3. 其余接口要求 USER，并把身份写入 UserContext。
 */
@RequiredArgsConstructor
public class AuthInterceptor implements HandlerInterceptor {

    private static final Set<String> PUBLIC_POST = new HashSet<>(Arrays.asList(
            "/api/user/login", "/api/admin/login", "/api/guidance/triage"));

    private static final Set<String> PUBLIC_GET = new HashSet<>(Arrays.asList(
            "/api/department/list", "/api/department/detail",
            "/api/doctor/list", "/api/doctor/search", "/api/doctor/detail",
            "/api/schedule/list", "/api/schedule/dates", "/api/schedule/detail"));

    private static final String BEARER = "Bearer ";

    private final JwtUtil jwtUtil;
    private final ObjectMapper objectMapper;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws IOException {
        String method = request.getMethod();
        if ("OPTIONS".equalsIgnoreCase(method)) {
            return true;
        }

        String path = request.getRequestURI();
        if (isPublic(path, method)) {
            return true;
        }

        String header = request.getHeader("Authorization");
        if (header == null || !header.startsWith(BEARER)) {
            return deny(response, 401, "请先登录");
        }

        Claims claims;
        try {
            claims = jwtUtil.parse(header.substring(BEARER.length()).trim());
        } catch (JwtException | IllegalArgumentException e) {
            return deny(response, 401, "登录已过期，请重新登录");
        }

        String role = claims.get("role", String.class);
        if (needAdmin(path, method) && !Role.ADMIN.equals(role)) {
            return deny(response, 403, "无权访问该功能");
        }

        try {
            UserContext.set(Long.valueOf(claims.getSubject()), role);
        } catch (NumberFormatException e) {
            return deny(response, 401, "登录已过期，请重新登录");
        }
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response,
                                Object handler, Exception ex) {
        UserContext.clear();
    }

    private boolean isPublic(String path, String method) {
        if ("GET".equalsIgnoreCase(method)) {
            return PUBLIC_GET.contains(path);
        }
        if ("POST".equalsIgnoreCase(method)) {
            return PUBLIC_POST.contains(path);
        }
        return false;
    }

    private boolean needAdmin(String path, String method) {
        if (path.startsWith("/api/admin/")) {
            return true;
        }
        boolean write = !"GET".equalsIgnoreCase(method);
        return write && (path.startsWith("/api/department/")
                || path.startsWith("/api/doctor/")
                || path.startsWith("/api/schedule/"));
    }

    private boolean deny(HttpServletResponse response, int code, String message) throws IOException {
        response.setStatus(code);
        response.setCharacterEncoding(StandardCharsets.UTF_8.name());
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.getWriter().write(objectMapper.writeValueAsString(R.fail(code, message)));
        return false;
    }
}
