import microSecFixer.core.fixing as fixer

"""Utility class containing maps useful for execution"""
class RuleMap:
    _rules = {
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
        12: "r12",
        13: "r04",
        14: "r05",
        15: "r02",
        16: "r03",
        17: "r15",
        18: "r22",
        19: "r24",
        20: "r18",
        21: "r21",
        22: "r06",
        23: "r07",
        24: "r13",
        25: "r14"
    }

    _fixes = {
        "r01":  fixer.r01_authorization_only,
        "r02":  fixer.r02_authentication_only,
        "r03":  fixer.r03_logging_system_disconnect,
        "r04":  fixer.r04_single_entry,
        "r05":  fixer.r05_single_authorization,
        "r06":  fixer.r06_single_authentication,
        "r07":  fixer.r07_single_log_subsystem,
        "r08":  fixer.r08_single_registry,
        "r09":  fixer.r09_single_secret_store,
        "r10": fixer.r10_single_monitoring_dashboard,
        "r11": fixer.r11_single_message_broker,
        "r12": fixer.r12_single_login_attempt_limiter,
        "r13": fixer.r13_entrypoint_authorization,
        "r14": fixer.r14_entrypoint_authentication,
        "r15": fixer.r15_entrypoint_circuit_breaker,
        "r16": fixer.r16_entrypoint_load_balancer,
        "r17": fixer.r17_all_logging,
        "r18": fixer.r18_all_sanitize_logs,
        "r19": fixer.r19_registry_validate,
        "r20": fixer.r20_logger_to_message_broker,
        "r21": fixer.r21_all_to_monitoring_dashboard,
        "r22": fixer.r22_connections_authorized,
        "r23": fixer.r23_connections_authenticated,
        "r24": fixer.r24_outer_connections_encrypted,
        "r25": fixer.r25_inner_connections_encrypted
    }

    @staticmethod
    def get_rules():
        return RuleMap._rule
    
    @staticmethod
    def get_fixes():
        return RuleMap._fixes