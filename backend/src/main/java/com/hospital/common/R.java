package com.hospital.common;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Getter;

/**
 * 统一响应体。HTTP 状态码与 code 保持一致，前端只需判断一次。
 */
@Getter
@JsonInclude(JsonInclude.Include.NON_NULL)
public class R<T> {

    private final int code;
    private final String message;
    private final T data;

    private R(int code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    public static <T> R<T> ok(T data) {
        return new R<>(200, "成功", data);
    }

    public static R<Void> ok() {
        return new R<>(200, "成功", null);
    }

    public static <T> R<T> fail(int code, String message) {
        return new R<>(code, message, null);
    }

    public static <T> R<T> fail(String message) {
        return new R<>(400, message, null);
    }
}
