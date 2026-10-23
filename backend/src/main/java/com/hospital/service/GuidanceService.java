package com.hospital.service;

import com.hospital.vo.TriageVO;

public interface GuidanceService {

    TriageVO triage(String symptoms);
}
