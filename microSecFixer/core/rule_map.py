class RuleMap:
    _mapping = {
        1:  "r10",
        2:  "r11",
        3:  "r19",
        4:  "r01",
        5:  "r08",
        6:  "r09",
        7:  "r16",
        8:  "r23",
        9:  "r25",
        10: "r20",
        11: "r17",
        12: "r04",
        13: "r05",
        14: "r15",
        15: "r18",
        16: "r21",
        17: "r02",
        18: "r03",
        19: "r22",
        20: "r24",
        21: "r12",
        22: "r06",
        23: "r07",
        24: "r13",
        25: "r14"
    }

    @staticmethod
    def get_mapping():
        return RuleMap._mapping