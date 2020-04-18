import enum

@enum.unique
class ThreatType(enum.Enum):
    HOST = "HOST"
    FILE = "FILE"
    USER_DEFINED = "USER_DEFINED"
