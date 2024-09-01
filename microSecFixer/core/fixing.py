from microCertiSec.core.node import CNode
from microCertiSec.core.edge import CEdge
from microCertiSec.core.model import CModel
from microSecFixer.core.stereotypes import merge_stereotypes, without_traceability, with_traceability, BusinessFunctionality, LoggingServer, AllConnections, AllEntrypoints, AllNodes, AllServiceRegistries, AuthService, MessageBroker, MonitoringDashboard, Service, ExternalEntity, Database
from microSecFixer.core.unparse import unparse_model


def r01_authorization_only(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    for node in nodes:
        if AuthService.get_stereotypes()[0] in without_traceability(node.stereotypes):
            intersection = list(set(with_traceability(BusinessFunctionality.get_stereotypes())) & set(node.stereotypes))
            node.stereotypes = node.stereotypes - intersection
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r02_authentication_only(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    for node in nodes:
        if AuthService.get_stereotypes()[1] in without_traceability(node.stereotypes):
            intersection = list(set(with_traceability(BusinessFunctionality.get_stereotypes())) & set(node.stereotypes))
            node.stereotypes = node.stereotypes - intersection
    model.nodes.update_nodes(nodes)
    unparse_model(model)

def r03_logging_system_disconnect(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    edges: set[CEdge] = model.edges.edges
    logging_server: CNode = get_node_with_stereotype(nodes, LoggingServer.get_stereotypes()[0])
    for node in nodes:
        node_is_message_broker = MessageBroker.get_stereotypes()[0] in without_traceability(node.stereotypes)
        if not node_is_message_broker:
            for con_node in node.connected_nodes:
                if con_node == logging_server:
                    edges = remove_edge(node, logging_server, edges)
                    node.connected_nodes.remove(con_node)
    model.edges.update_edges(edges)
    return unparse_model(model)

def r04_single_entry(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(AllEntrypoints.get_stereotypes()[0], with_traceability(merge_stereotypes(AllEntrypoints, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r05_single_authorization(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(AuthService.get_stereotypes()[0], with_traceability(merge_stereotypes(AuthService, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r06_single_authentication(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(AuthService.get_stereotypes()[1], with_traceability(merge_stereotypes(AuthService, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r07_single_log_subsystem(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(LoggingServer.get_stereotypes()[0], with_traceability(merge_stereotypes(LoggingServer, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)


def r08_single_registry(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(AllServiceRegistries.get_stereotypes()[0], with_traceability(merge_stereotypes(AllServiceRegistries, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r09_single_secret_store(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    auth_found = False
    for node in nodes:
        if node.name == AuthService.get_stereotypes()[0] or node.name == AuthService.get_stereotypes()[1] or AuthService.get_stereotypes()[0] in without_traceability(node.stereotypes) or AuthService.get_stereotypes()[1] in without_traceability(node.stereotypes):
            node.stereotypes.extend(with_traceability(AuthService.get_stereotypes()[2]))
            auth_found = True
    if not auth_found:
        node_traceability = "traceability"
        nodes.add(CNode(AuthService.get_stereotypes()[0], with_traceability(merge_stereotypes(AuthService, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)
    

def r10_single_monitoring_dashboard(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(MonitoringDashboard.get_stereotypes()[0], with_traceability(merge_stereotypes(MonitoringDashboard, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r11_single_message_broker(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(MessageBroker.get_stereotypes()[0], with_traceability(merge_stereotypes(MessageBroker, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r12_single_login_attempt_limiter(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        if node.name == AllEntrypoints.get_stereotypes()[0] or AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes):
            node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[5]))
            entrypoint_found = True
    if not entrypoint_found:
        node_traceability = "traceability"
        nodes.add(CNode(AllEntrypoints.get_stereotypes()[0], with_traceability(merge_stereotypes(AllEntrypoints, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r13_entrypoint_authorization(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        if node.name == AllEntrypoints.get_stereotypes()[0] or AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes):
            node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[1]))
            entrypoint_found = True
    if not entrypoint_found:
        node_traceability = "traceability"
        nodes.add(CNode(AllEntrypoints.get_stereotypes()[0], with_traceability(merge_stereotypes(AllEntrypoints, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r14_entrypoint_authentication(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        if node.name == AllEntrypoints.get_stereotypes()[0] or AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes):
            node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[2]))
            entrypoint_found = True
    if not entrypoint_found:
        node_traceability = "traceability"
        nodes.add(CNode(AllEntrypoints.get_stereotypes()[0], with_traceability(merge_stereotypes(AllEntrypoints, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r15_entrypoint_circuit_breaker(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        if node.name == AllEntrypoints.get_stereotypes()[0] or AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes):
            node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[3]))
            entrypoint_found = True
    if not entrypoint_found:
        node_traceability = "traceability"
        nodes.add(CNode(AllEntrypoints.get_stereotypes()[0], with_traceability(merge_stereotypes(AllEntrypoints, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r16_entrypoint_load_balancer(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        if node.name == AllEntrypoints.get_stereotypes()[0] or AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes):
            node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[4]))
            entrypoint_found = True
    if not entrypoint_found:
        node_traceability = "traceability"
        nodes.add(CNode(AllEntrypoints.get_stereotypes()[0], with_traceability(merge_stereotypes(AllEntrypoints, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r17_all_logging(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    for node in nodes:
        if not AllNodes.get_stereotypes()[0] in without_traceability(node.stereotypes):
            node.stereotypes.extend(with_traceability(AllNodes.get_stereotypes()[0]))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r18_all_sanitize_logs(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    for node in nodes:
        if not AllNodes.get_stereotypes()[1] in without_traceability(node.stereotypes):
            node.stereotypes.extend(with_traceability(AllNodes.get_stereotypes()[1]))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r19_registry_validate(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    registry_found = False
    for node in nodes:
        if node.name == AllServiceRegistries.get_stereotypes()[0] or AllServiceRegistries.get_stereotypes()[0] in without_traceability(node.stereotypes):
            if not AllServiceRegistries.get_stereotypes()[1] in without_traceability(node.stereotypes):
                node.stereotypes.extend(with_traceability(AllServiceRegistries.get_stereotypes()[1]))
            registry_found = True
    if not registry_found:
        node_traceability = "traceability"
        nodes.add(CNode(AllServiceRegistries.get_stereotypes()[0], with_traceability(merge_stereotypes(AllServiceRegistries, AllNodes, Service)), node_traceability))
    model.nodes.update_nodes(nodes)
    return unparse_model(model)

def r20_logger_to_message_broker(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    edges: set[CEdge] = model.edges.edges
    for node in nodes:
        node_is_message_broker = MessageBroker.get_stereotypes()[0] in without_traceability(node.stereotypes)
        if AllNodes.get_stereotypes()[0] in without_traceability(node.stereotypes) and not node_is_message_broker:
            message_broker = get_node_with_stereotype(nodes, MessageBroker.get_stereotypes()[0])
            if not message_broker:
                r11_single_message_broker(model)
                message_broker = get_node_with_stereotype(nodes, MessageBroker.get_stereotypes()[0])
            edge: CEdge = create_edge(node, message_broker)
            edges.add(edge)
    model.edges.update_edges(edges)
    return unparse_model(model)
            

def r21_services_to_monitoring_dashboard(model: CModel) -> str:
    nodes: set[CNode] = model.nodes.nodes
    edges: set[CEdge] = model.edges.edges
    for node in nodes:
        node_is_monitoring_dashboard = MonitoringDashboard.get_stereotypes()[0] in without_traceability(node.stereotypes)
        if Service.get_stereotypes()[0] in without_traceability(node.stereotypes) and not node_is_monitoring_dashboard:
            monitoring_dashboard = get_node_with_stereotype(nodes, MonitoringDashboard.get_stereotypes()[0])
            if not monitoring_dashboard:
                r10_single_monitoring_dashboard(model)
                monitoring_dashboard = get_node_with_stereotype(nodes, MonitoringDashboard.get_stereotypes()[0])
            edge: CEdge = create_edge(node, monitoring_dashboard)
            edges.add(edge)
    model.edges.update_edges(edges)
    return unparse_model(model)

def r22_connections_authorized(model: CModel) -> str:
    edges: set[CEdge] = model.edges.edges
    for edge in edges:
        if not AllConnections.get_stereotypes()[0] in without_traceability(edge.stereotypes):
            edge.stereotypes.extend(with_traceability(AllConnections.get_stereotypes()[0]))
    model.edges.update_nodes(edges)
    return unparse_model(model)

def r23_connections_authenticated(model: CModel) -> str:
    edges: set[CEdge] = model.edges.edges
    for edge in edges:
        if not AllConnections.get_stereotypes()[1] in without_traceability(edge.stereotypes):
            edge.stereotypes.extend(with_traceability(AllConnections.get_stereotypes()[1]))
    model.edges.update_edges(edges)
    return unparse_model(model)

def r24_outer_connections_encrypted(model: CModel) -> str:
    edges: set[CEdge] = model.edges.edges
    for edge in edges:
        if not AllConnections.get_stereotypes()[2] in without_traceability(edge.stereotypes):
            edge.stereotypes.extend(with_traceability(AllConnections.get_stereotypes()[2]))
    model.edges.update_edges(edges)
    return unparse_model(model)

def r25_inner_connections_encrypted(model: CModel) -> str:
    edges: set[CEdge] = model.edges.edges
    for edge in edges:
        if not AllConnections.get_stereotypes()[2] in without_traceability(edge.stereotypes):
            edge.stereotypes.extend(with_traceability(AllConnections.get_stereotypes()[2]))
    model.edges.update_edges(edges)
    return unparse_model(model)

def get_node_with_stereotype(nodes: list[CNode], stereotype: str):
    for node in nodes:
        if stereotype in without_traceability(node.stereotypes):
            return node
    return None

def create_edge(sender: CNode, receiver: CNode) -> CEdge:
    edge_traceability = "traceability"
    return CEdge(sender, receiver, with_traceability(AllConnections.get_stereotypes()), edge_traceability)

def remove_edge(sender: CNode, receiver: CNode, edges: set[CEdge]) -> set[CEdge]:
    for edge in edges:
        if edge.sender == sender and edge.receiver == receiver:
            edges.remove(edge)
            return edges
