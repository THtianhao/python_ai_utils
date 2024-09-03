import json
from enum import Enum


class Version(Enum):
    V1_1: str = "25d5086bd791050a945ff4c02d"


class Member(Enum):
    tianhao: str = "1442608589321888"
    zhiaoda: str = "209209509802420981"
    wangleiyun: str = "202386109976300484"
    xiaofeiyu: str = "208517709976317222"
    wangbochao: str = "1096757492690461"
    penglun: str = "1578560662229926"
    douweixiang: str = "209623414124867984"


class Operator(Enum):
    CONTAINS: str = "CONTAINS"


class Field(Enum):
    ASSIGNED_TO: str = "assignedTo"
    SPRINT: str = "sprint"


class ClassName(Enum):
    USER: str = "user"
    SPRINT: str = "sprint"


class Condition:
    def __init__(self, filed: Field, operator: Operator, class_name: ClassName, values: list[str]):
        self.filed = filed.value
        self.operator = operator.value
        self.class_name = class_name.value
        self.values = values

    def build(self):
        condition = {
            "fieldIdentifier": self.filed,
            "operator": self.operator,
            "value": self.values,
            "toValue": None,
            "className": self.class_name,
            "format": "list"
        }
        return condition


class ConditionBuilder:
    def __init__(self, conditions: list):
        self.conditions = conditions

    def build(self):
        result = {
            "conditionGroups": [
                [

                ]
            ]
        }
        result["conditionGroups"][0].extend(self.conditions)
        return json.dumps(result)


def get_back_condition(version: Version):
    condition_member = Condition(Field.ASSIGNED_TO, Operator.CONTAINS, ClassName.USER,
                                 [Member.wangleiyun.value, Member.zhiaoda.value]).build()
    condition_version = Condition(Field.SPRINT, Operator.CONTAINS, ClassName.SPRINT, [version.value]).build()
    return ConditionBuilder([condition_member, condition_version]).build()


def get_front_condition(version: Version):
    condition_member = Condition(Field.ASSIGNED_TO, Operator.CONTAINS, ClassName.USER,
                                 [Member.douweixiang.value]).build()
    condition_version = Condition(Field.SPRINT, Operator.CONTAINS, ClassName.SPRINT, [version.value]).build()
    return ConditionBuilder([condition_member, condition_version]).build()
