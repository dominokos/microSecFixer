from collections.abc import Iterable

# Node-specific stereotypes
class AllServices:
    nodes_stereotypes = ["service",
                         "local_logging",
                         "log_sanitization"]
    @staticmethod
    def get_stereotypes():
        return AllServices.nodes_stereotypes

class AllEntrypoints:
    entrypoints_stereotypes = ["entrypoint",
                               "authorization",
                               "authentication",
                               "circuit_breaker",
                               "load_balancer",
                               "login_attempts_regulation",
                               "infrastructural"]
    @staticmethod
    def get_stereotypes():
        return AllEntrypoints.entrypoints_stereotypes
    
    @staticmethod
    def get_forbidden_stereotypes():
        return merge_stereotypes(LoggingServer, MessageBroker, MonitoringDashboard, AuthService, ExternalEntity, Database)

class AllServiceRegistries:
    service_discovery_stereotypes = ["service_discovery",
                                     "validate_registration",
                                     "infrastructural"]
    @staticmethod
    def get_stereotypes():
        return AllServiceRegistries.service_discovery_stereotypes
    
    @staticmethod
    def get_forbidden_stereotypes():
        return merge_stereotypes(LoggingServer, MessageBroker, MonitoringDashboard, AuthService, ExternalEntity, Database)
    
class LoggingServer:
    logging_server_stereotypes = ["logging_server",
                                  "infrastructural"]
    @staticmethod
    def get_stereotypes():
        return LoggingServer.logging_server_stereotypes
    
    @staticmethod
    def get_forbidden_stereotypes():
        return merge_stereotypes(AllEntrypoints, MessageBroker, MonitoringDashboard, AuthService, ExternalEntity, Database)

class MessageBroker:
    message_broker_stereotypes = ["message_broker",
                                  "infrastructural"]
    @staticmethod
    def get_stereotypes():
        return MessageBroker.message_broker_stereotypes
    
    @staticmethod
    def get_forbidden_stereotypes():
        return merge_stereotypes(LoggingServer, AllEntrypoints, MonitoringDashboard, AuthService, ExternalEntity, Database)

class MonitoringDashboard:
    monitoring_dashboard_stereotypes = ["monitoring_dashboard",
                                        "infrastructural"]
    @staticmethod
    def get_stereotypes():
        return MonitoringDashboard.monitoring_dashboard_stereotypes
    
    @staticmethod
    def get_forbidden_stereotypes():
        return merge_stereotypes(LoggingServer, MessageBroker, AllEntrypoints, AuthService, ExternalEntity, Database)

class AuthService:
    auth_service_stereotypes = ["authorization_server",
                                "authentication_server",
                                "secret_manager",
                                "infrastructural"]
    @staticmethod
    def get_stereotypes():
        return AuthService.auth_service_stereotypes

    @staticmethod
    def get_forbidden_stereotypes():
        return merge_stereotypes(LoggingServer, MessageBroker, MonitoringDashboard, AllEntrypoints, ExternalEntity, Database)

class ExternalEntity:
    external_component_stereotypes = ["external_entity"]
    @staticmethod
    def get_stereotypes():
        return ExternalEntity.external_component_stereotypes
    
    @staticmethod
    def get_forbidden_stereotypes():
        return merge_stereotypes(LoggingServer, MessageBroker, MonitoringDashboard, AuthService, AllEntrypoints)

class Database:
    database_stereotypes = ["database"]
    @staticmethod
    def get_stereotypes():
        return Database.database_stereotypes
    
    @staticmethod
    def get_forbidden_stereotypes():
        return merge_stereotypes(LoggingServer, MessageBroker, MonitoringDashboard, AuthService, AllEntrypoints)

class BusinessFunctionality:
    functionality_stereotypes = ["administration_server",
                                "configuration_server",
                                "gateway",
                                "entrypoint",
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


def merge_stereotypes(*args) -> list[str]:
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

def remove_forbidden_stereotypes(stereotypes: set, node_class):
    filtered_stereotypes = set()
    forbidden_stereotypes = node_class.get_forbidden_stereotypes()
    for (stereotype, traceability) in stereotypes:
        if not stereotype in forbidden_stereotypes:
            filtered_stereotypes.add((stereotype, traceability))
    return filtered_stereotypes



def collect_distinct_stereotypes(actual_stereotypes: list[str], node_typical_stereotypes: list[str]) -> set:
    distinct_stereotypes = set(actual_stereotypes) - set(with_traceability(node_typical_stereotypes))
    return distinct_stereotypes

def merge_tagged_values(tagged_values: dict, to_merge: dict):
    for key, value in to_merge.items():
        if key in tagged_values:
            if not isinstance(tagged_values[key], list):
                tagged_values[key] = [tagged_values[key]]
            
            if isinstance(value, Iterable) and not isinstance(value, str):
                tagged_values[key].extend(value)
            else:
                tagged_values[key].append(value)
        else:
            tagged_values[key] = value