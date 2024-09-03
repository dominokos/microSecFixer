from microCertiSec.core.node import CNode

# Node-specific stereotypes
class AllServices:
    nodes_stereotypes = ["service",
                         "local_logging",
                         "log_sanitization",
                         "internal"]
    @staticmethod
    def get_stereotypes():
        return AllServices.nodes_stereotypes

class AllEntrypoints:
    entrypoints_stereotypes = ["entrypoint",
                               "authorization",
                               "authentication",
                               "circuit_breaker",
                               "load_balancer",
                               "login_attempts_regulation"]
    @staticmethod
    def get_stereotypes():
        return AllEntrypoints.entrypoints_stereotypes

class AllServiceRegistries:
    service_discovery_stereotypes = ["service_discovery",
                                     "validate_registration"]
    @staticmethod
    def get_stereotypes():
        return AllServiceRegistries.service_discovery_stereotypes
    
class LoggingServer:
    logging_server_stereotypes = ["logging_server"]
    @staticmethod
    def get_stereotypes():
        return LoggingServer.logging_server_stereotypes

class MessageBroker:
    message_broker_stereotypes = ["message_broker"]
    @staticmethod
    def get_stereotypes():
        return MessageBroker.message_broker_stereotypes

class MonitoringDashboard:
    monitoring_dashboard_stereotypes = ["monitoring_dashboard"]
    @staticmethod
    def get_stereotypes():
        return MonitoringDashboard.monitoring_dashboard_stereotypes

class AuthService:
    auth_service_stereotypes = ["authorization_server",
                                "authentication_server",
                                "secret_manager"]
    @staticmethod
    def get_stereotypes():
        return AuthService.auth_service_stereotypes

class ExternalEntity:
    external_component_stereotypes = ["external_entity"]
    @staticmethod
    def get_stereotypes():
        return ExternalEntity.external_component_stereotypes

class Database:
    database_stereotypes = ["database"]
    @staticmethod
    def get_stereotypes():
        return Database.database_stereotypes

class BusinessFunctionality:
    functionality_stereotypes = ["administration_server",
                                "configuration_server",
                                "gateway",
                                "message_broker",
                                "service_discovery",
                                "search_engine",
                                "web_application",
                                "web_server",
                                "logging_server",
                                "metrics_server",
                                "monitoring_dashboard",
                                "monitoring_server",
                                "tracing_server"]
    @staticmethod
    def get_stereotypes():
        return BusinessFunctionality.functionality_stereotypes


# Edge-specific stereotypes
class AllConnections:
    connection_stereotypes = ["authorized",
                              "authenticated",
                              "encrypted"]
    @staticmethod
    def get_stereotypes():
        return AllConnections.connection_stereotypes


def merge_stereotypes(*args):
    merged_stereotypes = set()
    for arg in args:
        merged_stereotypes.update(arg.get_stereotypes())
    return list(merged_stereotypes)

def without_traceability(stereotype_tuples: list) -> list[str]:
    return [stuple[0] for stuple in stereotype_tuples]

def with_traceability(stereotypes) -> list:
    stuples = []
    if isinstance(stereotypes, list) or isinstance(stereotypes, set):
        for stereotype in stereotypes:
            tuple = (stereotype, "traceability")
            stuples.append(tuple)
    else:
        tuple = (stereotypes, "traceability")
        stuples.append(tuple)
    return stuples

def collect_distinct_stereotypes(actual_stereotypes: list, node_typical_stereotypes: list[str]) -> list:
    distinct_stereotypes = set(actual_stereotypes) - set(with_traceability(node_typical_stereotypes))
    return list(distinct_stereotypes)