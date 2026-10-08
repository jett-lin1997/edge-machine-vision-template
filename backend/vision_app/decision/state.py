from enum import StrEnum


class InspectionState(StrEnum):
    IDLE = "IDLE"
    READY = "READY"
    JUDGING = "JUDGING"
    PASS = "PASS"
    FAIL = "FAIL"
