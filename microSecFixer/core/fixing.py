from microCertiSec.core.node import CNode
from microCertiSec.core.edge import CEdge
from microCertiSec.core.nodes import CNodes
from microCertiSec.core.edges import CEdges
from microCertiSec.core.model import CModel
from microCertiSec import microCertiSec
from microSecFixer.core.stereotypes import merge_stereotypes, BusinessFunctionality, LoggingServer, AllConnections, AllEntrypoints, AllNodes, AllServiceRegistries, AuthService, MessageBroker, MonitoringDashboard, Service, ExternalEntity, Database
from microSecFixer.core.unparse import unparse_model

def get_model(model_path: str) -> CModel:
    return microCertiSec.model_api(model_path, None)

def r01_authorization_only(model_path: str) -> str:
    pass

def r02_authentication_only(model_path: str) -> str:
    pass

def r03_logging_system_disconnect(model_path: str) -> str:
    pass

def r04_single_entry(model_path: str) -> str:
    pass

def r05_single_authorization(model_path: str) -> str:
    pass

def r06_single_authentication(model_path: str) -> str:
    pass

def r07_single_log_subsystem(model_path: str) -> str:
    model = get_model(model_path)
    nodes = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(LoggingServer.get_stereotypes()[0], merge_stereotypes(LoggingServer, AllNodes), node_traceability, {}))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)


def r08_single_registry(model_path: str) -> str:
    pass

def r09_single_secret_store(model_path: str) -> str:
    pass

def r10_single_monitoring_dashboard(model_path: str) -> str:
    pass

def r11_single_message_broker(model_path: str) -> str:
    pass

def r12_single_login_attempt_limiter(model_path: str) -> str:
    pass

def r13_entrypoint_authorization(model_path: str) -> str:
    pass

def r14_entrypoint_authentication(model_path: str) -> str:
    pass

def r15_entrypoint_circuit_breaker(model_path: str) -> str:
    pass

def r16_entrypoint_load_balancer(model_path: str) -> str:
    pass

def r17_all_logging(model_path: str) -> str:
    pass

def r18_all_sanitize_logs(model_path: str) -> str:
    pass

def r19_registry_validate(model_path: str) -> str:
    pass

def r20_logger_to_message_broker(model_path: str) -> str:
    pass

def r21_all_to_monitoring_dashboard(model_path: str) -> str:
    pass

def r22_connections_authorized(model_path: str) -> str:
    pass

def r23_connections_authenticated(model_path: str) -> str:
    pass

def r24_outer_connections_encrypted(model_path: str) -> str:
    pass

def r25_inner_connections_encrypted(model_path: str) -> str:
    pass