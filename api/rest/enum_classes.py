import enum
import json

@enum.unique
class ThreatType(enum.Enum):
    HOST = "HOST"
    FILE = "FILE"
    USER_DEFINED = "USER_DEFINED"

    def toJson(self):
        return json.dumps(self, default= lambda o: o.value)

if __name__ == '__main__':
    q = ThreatType.HOST
    print(q.toJson())
