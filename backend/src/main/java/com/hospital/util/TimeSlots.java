package com.hospital.util;

import java.time.LocalTime;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * 时段与具体就诊时间的唯一映射，避免各处硬编码 "08:00-12:00"。
 */
public final class TimeSlots {

    private static final Map<String, LocalTime[]> SLOTS;

    static {
        Map<String, LocalTime[]> map = new LinkedHashMap<>();
        map.put("上午", new LocalTime[]{LocalTime.of(8, 0), LocalTime.of(12, 0)});
        map.put("下午", new LocalTime[]{LocalTime.of(14, 0), LocalTime.of(18, 0)});
        map.put("晚上", new LocalTime[]{LocalTime.of(18, 0), LocalTime.of(21, 0)});
        SLOTS = Collections.unmodifiableMap(map);
    }

    private TimeSlots() {
    }

    public static boolean supported(String slot) {
        return slot != null && SLOTS.containsKey(slot);
    }

    public static List<String> all() {
        return Collections.unmodifiableList(Arrays.asList("上午", "下午", "晚上"));
    }

    public static LocalTime start(String slot) {
        LocalTime[] range = SLOTS.get(slot);
        return range == null ? LocalTime.of(8, 0) : range[0];
    }

    public static LocalTime end(String slot) {
        LocalTime[] range = SLOTS.get(slot);
        return range == null ? LocalTime.of(12, 0) : range[1];
    }
}
