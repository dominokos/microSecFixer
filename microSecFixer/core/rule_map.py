import microSecFixer.core.fixing as fixer

"""Utility class containing maps useful for execution"""
class RuleMap:
    _rules = {
        1:  "r10",
        2:  "r11",
        3:  "r01",
        4:  "r08",
        5:  "r09",
        6:  "r16",
        7:  "r23",
        8:  "r25",
        9:  "r20",
        10: "r17",
        11: "r12",
        12: "r04",
        13: "r05",
        14: "r02",
        15: "r03",
        16: "r15",
        17: "r22",
        18: "r24",
        19: "r18",
        20: "r21",
        21: "r06",
        22: "r07",
        23: "r13",
        24: "r14",
        25: "r19"
    }

    _fixes = {
        "r01": fixer.r01_authorization_only,
        "r02": fixer.r02_authentication_only,
        "r03": fixer.r03_single_entry,
        "r04": fixer.r04_single_authorization,
        "r05": fixer.r05_single_authentication,
        "r06": fixer.r06_single_log_subsystem,
        "r07": fixer.r07_single_registry,
        "r08": fixer.r08_single_secret_store,
        "r09": fixer.r09_monitoring_dashboard,
        "r10": fixer.r10_message_broker,
        "r11": fixer.r11_limit_login_attempts,
        "r12": fixer.r12_entrypoint_authorization,
        "r13": fixer.r13_entrypoint_authentication,
        "r14": fixer.r14_entrypoint_circuit_breaker,
        "r15": fixer.r15_entrypoint_load_balancer,
        "r16": fixer.r16_services_logging,
        "r17": fixer.r17_services_sanitize_logs,
        "r18": fixer.r18_registry_validate,
        "r19": fixer.r19_logger_to_message_broker,
        "r20": fixer.r20_services_to_monitoring_dashboard,
        "r21": fixer.r21_connections_authorized,
        "r22": fixer.r22_connections_authenticated,
        "r23": fixer.r23_outer_connections_encrypted,
        "r24": fixer.r24_inner_connections_encrypted,
        "r25": fixer.r25_logging_system_disconnect
    }

    @staticmethod
    def get_rules():
        return RuleMap._rules
    
    @staticmethod
    def get_fixes():
        return RuleMap._fixes