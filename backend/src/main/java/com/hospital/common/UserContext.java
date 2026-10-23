package com.hospital.common;

/**
 * 当前请求的登录身份，由 AuthInterceptor 写入、请求结束后清理。
 * 业务层一律从这里取用户，不再信任请求参数中的 userId。
 */
public final class UserContext {

    private static final ThreadLocal<Principal> HOLDER = new ThreadLocal<>();

    private UserContext() {
    }

    public static void set(Long id, String role) {
        HOLDER.set(new Principal(id, role));
    }

    public static void clear() {
        HOLDER.remove();
    }

    public static Long userId() {
        Principal p = require();
        if (!Role.USER.equals(p.role)) {
            throw new BusinessException(403, "该操作需要患者身份");
        }
        return p.id;
    }

    public static Long adminId() {
        Principal p = require();
        if (!Role.ADMIN.equals(p.role)) {
            throw new BusinessException(403, "该操作需要管理员身份");
        }
        return p.id;
    }

    private static Principal require() {
        Principal p = HOLDER.get();
        if (p == null) {
            throw new BusinessException(401, "请先登录");
        }
        return p;
    }

    private static final class Principal {
        private final Long id;
        private final String role;

        private Principal(Long id, String role) {
            this.id = id;
            this.role = role;
        }
    }
}
