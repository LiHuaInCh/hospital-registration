package com.hospital.util;

import com.hospital.common.BusinessException;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.time.format.ResolverStyle;
import java.util.regex.Pattern;

/**
 * 就诊人信息的格式校验（前端只做格式提示，这里才是权威校验）。
 */
public final class Ids {

    private static final Pattern ID_CARD = Pattern.compile("\\d{17}[\\dXx]");
    private static final Pattern PHONE = Pattern.compile("1[3-9]\\d{9}");
    private static final int[] WEIGHTS = {7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2};
    private static final char[] CHECK_CODES = {'1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'};
    private static final DateTimeFormatter BIRTH = DateTimeFormatter.ofPattern("uuuuMMdd")
            .withResolverStyle(ResolverStyle.STRICT);

    private Ids() {
    }

    public static void checkIdCard(String idCard) {
        if (idCard == null || !ID_CARD.matcher(idCard.trim()).matches()) {
            throw new BusinessException("身份证号应为 18 位");
        }
        String value = idCard.trim().toUpperCase();
        try {
            LocalDate birth = LocalDate.parse(value.substring(6, 14), BIRTH);
            if (birth.isAfter(LocalDate.now())) {
                throw new BusinessException("身份证号中的出生日期不合法");
            }
        } catch (DateTimeParseException e) {
            throw new BusinessException("身份证号中的出生日期不合法");
        }
        int sum = 0;
        for (int i = 0; i < 17; i++) {
            sum += (value.charAt(i) - '0') * WEIGHTS[i];
        }
        if (CHECK_CODES[sum % 11] != value.charAt(17)) {
            throw new BusinessException("身份证号校验位不正确，请核对");
        }
    }

    public static void checkPhone(String phone) {
        if (phone == null || !PHONE.matcher(phone.trim()).matches()) {
            throw new BusinessException("手机号格式不正确");
        }
    }
}
