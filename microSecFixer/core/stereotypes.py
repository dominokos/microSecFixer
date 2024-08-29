# Node-specific stereotypes
class AllNodes:
    nodes_stereotypes = ["local_logging",
                         "log_sanitization"]
    @staticmethod
    def get_stereotypes():
        return AllNodes.nodes_stereotypes

class AllEntrypoints:
    entrypoints_stereotypes = ["entrypoint",
                               "authorization",
                               "authentication",
                               "load_balancer",
                               "circuit_breaker",
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
    
class Service:
    service_stereotypes = ["service"]
    @staticmethod
    def get_stereotypes():
        return Service.service_stereotypes

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
                                "authorization_server",
                                "authentication_server",
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
    merged_tuples = []
    for stereotype in merged_stereotypes:
        tuple = (stereotype, "traceability")
        merged_tuples.append(tuple)
    return merged_tuples