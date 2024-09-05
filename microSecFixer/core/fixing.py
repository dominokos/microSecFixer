from microCertiSec.core.node import CNode
from microCertiSec.core.edge import CEdge
from microCertiSec.core.model import CModel
from microSecFixer.core.stereotypes import merge_stereotypes, collect_distinct_stereotypes, remove_forbidden_stereotypes, without_traceability, with_traceability, BusinessFunctionality, LoggingServer, AllConnections, AllEntrypoints, AllServices, AllServiceRegistries, AuthService, MessageBroker, MonitoringDashboard
from microSecFixer.core.unparse import unparse_model
from microSecFixer.core.edge_utils import create_edge, handle_edges, remove_edge, remove_edges_in_both, find_all_edges_with_receiver, find_all_edges_with_sender
from microSecFixer.core.node_utils import find_all_nodes_with_stereotype, find_node_with_stereotype, node_is_connected_to


def r01_authorization_only(model: CModel) -> str:
    """
    No service that performs authorization should perform any other business functionality.
    """
    nodes: set[CNode] = model.nodes.nodes
    for node in nodes:
        node_is_service = AllServices.get_stereotypes()[0]
        service_is_authorization_server = AuthService.get_stereotypes()[0] in without_traceability(node.stereotypes)
        if node_is_service and service_is_authorization_server:
            intersection = list(set(with_traceability(BusinessFunctionality.get_stereotypes())) & set(node.stereotypes))
            node.stereotypes = node.stereotypes - intersection
    return unparse_model(model)

def r02_authentication_only(model: CModel) -> str:
    """
    No service that performs authentication should perform any other business functionality.
    """
    nodes: set[CNode] = model.nodes.nodes
    for node in nodes:
        node_is_service = AllServices.get_stereotypes()[0]
        service_is_authentication_server = AuthService.get_stereotypes()[1] in without_traceability(node.stereotypes)
        if node_is_service and service_is_authentication_server:
            intersection = list(set(with_traceability(BusinessFunctionality.get_stereotypes())) & set(node.stereotypes))
            node.stereotypes = node.stereotypes - intersection
    unparse_model(model)

def r03_logging_system_disconnect(model: CModel) -> str:
    """
    No service that performs logging should be connected to a central logging subsystem.
    """
    nodes: set[CNode] = model.nodes.nodes
    edges: set[CEdge] = model.edges.edges
    logging_servers: list[CNode] = list(find_all_nodes_with_stereotype(nodes, LoggingServer.get_stereotypes()[0]))
    for node in nodes:
        node_is_message_broker = MessageBroker.get_stereotypes()[0] in without_traceability(node.stereotypes)
        if not node_is_message_broker:
            for con_node in node.connected_nodes:
                if con_node in logging_servers:
                    index = logging_servers.index(con_node)
                    edges = remove_edge(node, logging_servers[index], edges)
                    node.connected_nodes.remove(con_node)
    return unparse_model(model)

def r04_single_entry(model: CModel) -> str:
    """
    There should be a single service as entry point.
    """
    nodes: set[CNode] = model.nodes.nodes
    entrypoints: set[CNode] = find_all_nodes_with_stereotype(nodes, AllEntrypoints.get_stereotypes()[0])
    distinct_stereotypes = set()
    tagged_values: dict = {}
    edges_from_entrypoints: set[CNode] = set()
    edges_to_entrypoints: set[CNode] = set()
    edges: set[CEdge] = model.edges.edges
    if entrypoints:
        for entrypoint in entrypoints:
            distinct_stereotypes.update(collect_distinct_stereotypes(entrypoint.stereotypes, merge_stereotypes(AllEntrypoints, AllServices)))
            tagged_values.update(entrypoint.tagged_values)
            edges_from_entrypoints.update(find_all_edges_with_sender(entrypoint, edges))
            edges_to_entrypoints.update(find_all_edges_with_receiver(entrypoint, edges))
            nodes.remove(entrypoint)
    remove_edges_in_both(edges, edges_from_entrypoints, edges_to_entrypoints)
    distinct_stereotypes = remove_forbidden_stereotypes(distinct_stereotypes, AllEntrypoints)
    node_traceability = "traceability"
    merged_entrypoint = CNode(AllEntrypoints.get_stereotypes()[0], with_traceability(merge_stereotypes(AllEntrypoints, AllServices)) + list(distinct_stereotypes), node_traceability, [], tagged_values)
    handle_edges(edges, edges_from_entrypoints, edges_to_entrypoints, merged_entrypoint)
    nodes.add(merged_entrypoint)
    return unparse_model(model)

def r05_single_authorization(model: CModel) -> str:
    """
    There should be a single authorization service.
    """
    nodes: set[CNode] = model.nodes.nodes
    authorization_servers: set[CNode] = find_all_nodes_with_stereotype(nodes, AuthService.get_stereotypes()[0])
    distinct_stereotypes = set()
    tagged_values: dict = {}
    edges_from_authorization_servers: set[CNode] = set()
    edges_to_authorization_servers: set[CNode] = set()
    edges: set[CEdge] = model.edges.edges
    if authorization_servers:
        for auth in authorization_servers:
            distinct_stereotypes.update(collect_distinct_stereotypes(auth.stereotypes, merge_stereotypes(AuthService, AllServices)))
            tagged_values.update(auth.tagged_values)
            edges_from_authorization_servers.update(find_all_edges_with_sender(auth, edges))
            edges_to_authorization_servers.update(find_all_edges_with_receiver(auth, edges))
            nodes.remove(auth)
    remove_edges_in_both(edges, edges_from_authorization_servers, edges_to_authorization_servers)
    distinct_stereotypes = remove_forbidden_stereotypes(distinct_stereotypes, AuthService)
    node_traceability = "traceability"
    merged_authorization_server = CNode(AuthService.get_stereotypes()[0], with_traceability(merge_stereotypes(AuthService, AllServices)) + list(distinct_stereotypes), node_traceability, [], tagged_values)
    handle_edges(edges, edges_from_authorization_servers, edges_to_authorization_servers, merged_authorization_server)
    nodes.add(merged_authorization_server)
    return unparse_model(model)

def r06_single_authentication(model: CModel) -> str:
    """
    There should be a single authentication service.
    """
    nodes: set[CNode] = model.nodes.nodes
    authentication_servers: set[CNode] = find_all_nodes_with_stereotype(nodes, AuthService.get_stereotypes()[1])
    distinct_stereotypes = set()
    tagged_values: dict = {}
    edges_from_authentication_servers: set[CNode] = set()
    edges_to_authentication_servers: set[CNode] = set()
    edges: set[CEdge] = model.edges.edges
    if authentication_servers:
        for auth in authentication_servers:
            distinct_stereotypes.update(collect_distinct_stereotypes(auth.stereotypes, merge_stereotypes(AuthService, AllServices)))
            tagged_values.update(auth.tagged_values)
            edges_from_authentication_servers.update(find_all_edges_with_sender(auth, edges))
            edges_to_authentication_servers.update(find_all_edges_with_receiver(auth, edges))
            nodes.remove(auth)
    remove_edges_in_both(edges, edges_from_authentication_servers, edges_to_authentication_servers)
    distinct_stereotypes = remove_forbidden_stereotypes(distinct_stereotypes, AuthService)
    node_traceability = "traceability"
    merged_authentication_server = CNode(AuthService.get_stereotypes()[1], with_traceability(merge_stereotypes(AuthService, AllServices)) + list(distinct_stereotypes), node_traceability, [], tagged_values)
    handle_edges(edges, edges_from_authentication_servers, edges_to_authentication_servers, merged_authentication_server)
    nodes.add(merged_authentication_server)
    return unparse_model(model)

def r07_single_log_subsystem(model: CModel) -> str:
    """
    There should be a single central logging subsystem.
    """
    nodes: set[CNode] = model.nodes.nodes
    logging_servers: set[CNode] = find_all_nodes_with_stereotype(nodes, LoggingServer.get_stereotypes()[0])
    distinct_stereotypes = set()
    tagged_values: dict = {}
    edges_from_logging_servers: set[CNode] = set()
    edges_to_logging_servers: set[CNode] = set()
    edges: set[CEdge] = model.edges.edges
    if logging_servers:
        for logging_server in logging_servers:
            distinct_stereotypes.update(collect_distinct_stereotypes(logging_server.stereotypes, merge_stereotypes(LoggingServer, AllServices)))
            tagged_values.update(logging_server.tagged_values)
            edges_from_logging_servers.update(find_all_edges_with_sender(logging_server, edges))
            edges_to_logging_servers.update(find_all_edges_with_receiver(logging_server, edges))
            nodes.remove(logging_server)
    remove_edges_in_both(edges, edges_from_logging_servers, edges_to_logging_servers)
    distinct_stereotypes = remove_forbidden_stereotypes(distinct_stereotypes, LoggingServer)
    node_traceability = "traceability"
    merged_logging_server = CNode(LoggingServer.get_stereotypes()[0], with_traceability(merge_stereotypes(LoggingServer, AllServices)) + list(distinct_stereotypes), node_traceability, [], tagged_values)
    handle_edges(edges, edges_from_logging_servers, edges_to_logging_servers, merged_logging_server)
    nodes.add(merged_logging_server)
    return unparse_model(model)


def r08_single_registry(model: CModel) -> str:
    """
    There should be a single service registry.
    """
    nodes: set[CNode] = model.nodes.nodes
    registries: set[CNode] = find_all_nodes_with_stereotype(nodes, AllServiceRegistries.get_stereotypes()[0])
    distinct_stereotypes = set()
    tagged_values: dict = {}
    edges_from_registries: set[CNode] = set()
    edges_to_registries: set[CNode] = set()
    edges: set[CEdge] = model.edges.edges
    if registries:
        for registry in registries:
            distinct_stereotypes.update(collect_distinct_stereotypes(registry.stereotypes, merge_stereotypes(AllServiceRegistries, AllServices)))
            tagged_values.update(registry.tagged_values)
            edges_from_registries.update(find_all_edges_with_sender(registry, edges))
            edges_to_registries.update(find_all_edges_with_receiver(registry, edges))
            nodes.remove(registry)
    remove_edges_in_both(edges, edges_from_registries, edges_to_registries)
    distinct_stereotypes = remove_forbidden_stereotypes(distinct_stereotypes, AllServiceRegistries)
    node_traceability = "traceability"
    merged_registry = CNode(AllServiceRegistries.get_stereotypes()[0], with_traceability(merge_stereotypes(AllServiceRegistries, AllServices)) + list(distinct_stereotypes), node_traceability, [], tagged_values)
    handle_edges(edges, edges_from_registries, edges_to_registries, merged_registry)

    nodes.add(merged_registry)
    return unparse_model(model)

def r09_single_secret_store(model: CModel) -> str:
    """
    There should be a single central secret store.
    """
    nodes: set[CNode] = model.nodes.nodes
    auth_found = False
    for node in nodes:
        node_is_authorization_server = AuthService.get_stereotypes()[0] in without_traceability(node.stereotypes)
        node_is_authentication_server = AuthService.get_stereotypes()[1] in without_traceability(node.stereotypes)
        if  node_is_authorization_server or node_is_authentication_server:
            node.stereotypes.extend(with_traceability(AuthService.get_stereotypes()[2]))
            auth_found = True
    if not auth_found:
        return r05_single_authorization(model)
    return unparse_model(model)
    

def r10_monitoring_dashboard(model: CModel) -> str:
    """
    There should be a monitoring dashboard.
    """
    nodes: set[CNode] = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(MonitoringDashboard.get_stereotypes()[0], with_traceability(merge_stereotypes(MonitoringDashboard, AllServices)), node_traceability))
    return unparse_model(model)

def r11_message_broker(model: CModel) -> str:
    """
    There should be a message broker.
    """
    nodes: set[CNode] = model.nodes.nodes
    node_traceability = "traceability"
    nodes.add(CNode(MessageBroker.get_stereotypes()[0], with_traceability(merge_stereotypes(MessageBroker, AllServices)), node_traceability))
    return unparse_model(model)

def r12_single_login_attempt_limiter(model: CModel) -> str:
    """
    There should be a service limiting the number of login attempts.
    """
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        node_is_entrypoint = AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes)
        if node_is_entrypoint:
            entrypoint_does_limit_attempts = AllEntrypoints.get_stereotypes()[5] in without_traceability(node.stereotypes)
            if not entrypoint_does_limit_attempts:
                node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[5]))
            entrypoint_found = True
    if not entrypoint_found:
        return r04_single_entry(model)
    return unparse_model(model)

def r13_entrypoint_authorization(model: CModel) -> str:
    """
    All entry points should perform authorization.
    """
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        node_is_entrypoint = AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes)
        if node_is_entrypoint:
            entrypoint_has_authorization = AllEntrypoints.get_stereotypes()[1] in without_traceability(node.stereotypes)
            if not entrypoint_has_authorization:
                node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[1]))
            entrypoint_found = True
    if not entrypoint_found:
        return r04_single_entry(model)
    return unparse_model(model)

def r14_entrypoint_authentication(model: CModel) -> str:
    """
    All entry points should perform authentication.
    """
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        node_is_entrypoint = AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes)
        entrypoint_has_authentication = AllEntrypoints.get_stereotypes()[2] in without_traceability(node.stereotypes)
        if node_is_entrypoint:
            entrypoint_has_authentication = AllEntrypoints.get_stereotypes()[2] in without_traceability(node.stereotypes)
            if not entrypoint_has_authentication:
                node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[2]))
            entrypoint_found = True
    if not entrypoint_found:
        return r04_single_entry(model)
    return unparse_model(model)

def r15_entrypoint_circuit_breaker(model: CModel) -> str:
    """
    All entry points should have a circuit breaker.
    """
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        node_is_entrypoint = AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes)
        if node_is_entrypoint:
            entrypoint_has_circuitbreaker = AllEntrypoints.get_stereotypes()[3] in without_traceability(node.stereotypes)
            if not entrypoint_has_circuitbreaker:
                node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[3]))
            entrypoint_found = True
    if not entrypoint_found:
        return r04_single_entry(model)
    return unparse_model(model)

def r16_entrypoint_load_balancer(model: CModel) -> str:
    """
    All entry points should have a load balancer.
    """
    nodes: set[CNode] = model.nodes.nodes
    entrypoint_found = False
    for node in nodes:
        node_is_entrypoint = AllEntrypoints.get_stereotypes()[0] in without_traceability(node.stereotypes)
        entrypoint_has_loadbalancer = AllEntrypoints.get_stereotypes()[4] in without_traceability(node.stereotypes)
        if node_is_entrypoint:
            entrypoint_has_loadbalancer = AllEntrypoints.get_stereotypes()[4] in without_traceability(node.stereotypes)
            if not entrypoint_has_loadbalancer:
                node.stereotypes.extend(with_traceability(AllEntrypoints.get_stereotypes()[4]))
            entrypoint_found = True
    if not entrypoint_found:
        return r04_single_entry(model)
    return unparse_model(model)

def r17_services_logging(model: CModel) -> str:
    """
    All services should perform logging.
    """
    nodes: set[CNode] = model.nodes.nodes
    for node in nodes:
        node_is_service = AllServices.get_stereotypes()[0] in without_traceability(node.stereotypes)
        service_does_logging = AllServices.get_stereotypes()[1] in without_traceability(node.stereotypes)
        if node_is_service and not service_does_logging:
            node.stereotypes.extend(with_traceability(AllServices.get_stereotypes()[1]))
    return unparse_model(model)

def r18_services_sanitize_logs(model: CModel) -> str:
    """
    All services should sanitize logs.
    """
    nodes: set[CNode] = model.nodes.nodes
    for node in nodes:
        node_is_service = AllServices.get_stereotypes()[0] in without_traceability(node.stereotypes)
        node_does_sanitization = AllServices.get_stereotypes()[2] in without_traceability(node.stereotypes)
        if node_is_service and not node_does_sanitization :
            node.stereotypes.extend(with_traceability(AllServices.get_stereotypes()[2]))
    return unparse_model(model)

def r19_registry_validate(model: CModel) -> str:
    """
    All service registries should have validation checks for incoming requests.
    """
    nodes: set[CNode] = model.nodes.nodes
    registry_found = False
    for node in nodes:
        node_is_service_registry = AllServiceRegistries.get_stereotypes()[0] in without_traceability(node.stereotypes)
        if node_is_service_registry:
            is_registry_validated = AllServiceRegistries.get_stereotypes()[1] in without_traceability(node.stereotypes)
            if not is_registry_validated:
                node.stereotypes.extend(with_traceability(AllServiceRegistries.get_stereotypes()[1]))
            registry_found = True
    if not registry_found:
        node_traceability = "traceability"
        nodes.add(CNode(AllServiceRegistries.get_stereotypes()[0], with_traceability(merge_stereotypes(AllServiceRegistries, AllServices)), node_traceability))
    return unparse_model(model)

def r20_logger_to_message_broker(model: CModel) -> str:
    """
    All services that perform logging should be connected to a message broker.
    """
    nodes: set[CNode] = model.nodes.nodes
    edges: set[CEdge] = model.edges.edges
    message_broker = find_node_with_stereotype(nodes, MessageBroker.get_stereotypes()[0])
    if not message_broker:
        r11_message_broker(model)
        message_broker = find_node_with_stereotype(nodes, MessageBroker.get_stereotypes()[0])
    logging_server = find_node_with_stereotype(nodes, LoggingServer.get_stereotypes()[0])
    if not logging_server:
        r07_single_log_subsystem(model)
        logging_server = find_node_with_stereotype(nodes, LoggingServer.get_stereotypes()[0])
    for node in nodes:
        node_is_service = AllServices.get_stereotypes()[0] in without_traceability(node.stereotypes)
        service_does_logging = AllServices.get_stereotypes()[1] in without_traceability(node.stereotypes)
        service_is_message_broker = node == message_broker
        if node_is_service and service_does_logging and not service_is_message_broker and not node_is_connected_to(node, message_broker) :
            edge: CEdge = create_edge(node, message_broker)
            edges.add(edge)
            node.connected_nodes.append(message_broker)
    if not node_is_connected_to(message_broker, logging_server):
        logging_edge = create_edge(message_broker, logging_server)
        message_broker.connected_nodes.append(logging_server)
        edges.add(logging_edge)
    return unparse_model(model)
            

def r21_services_to_monitoring_dashboard(model: CModel) -> str:
    """
    All services should be connected to a monitoring dashboard.
    """
    nodes: set[CNode] = model.nodes.nodes
    edges: set[CEdge] = model.edges.edges
    monitoring_dashboard = find_node_with_stereotype(nodes, MonitoringDashboard.get_stereotypes()[0])
    if not monitoring_dashboard:
        r10_monitoring_dashboard(model)
        monitoring_dashboard = find_node_with_stereotype(nodes, MonitoringDashboard.get_stereotypes()[0])
    for node in nodes:
        node_is_service = AllServices.get_stereotypes()[0] in without_traceability(node.stereotypes)
        service_is_monitoring_dashboard = node == monitoring_dashboard
        if node_is_service and not service_is_monitoring_dashboard and not node_is_connected_to(node, monitoring_dashboard):
            edge: CEdge = create_edge(node, monitoring_dashboard)
            edges.add(edge)
            node.connected_nodes.append(monitoring_dashboard)
    return unparse_model(model)

def r22_connections_authorized(model: CModel) -> str:
    """
    All connections between services should be authorized.
    """
    edges: set[CEdge] = model.edges.edges
    for edge in edges:
        edge_is_authorized = AllConnections.get_stereotypes()[0] in without_traceability(edge.stereotypes)
        sender_and_receiver_internal = AllServices.get_stereotypes()[3] in without_traceability(edge.sender.stereotypes) and AllServices.get_stereotypes()[3] in without_traceability(edge.receiver.stereotypes)
        if sender_and_receiver_internal and not edge_is_authorized:
            edge.stereotypes.extend(with_traceability(AllConnections.get_stereotypes()[0]))
    return unparse_model(model)

def r23_connections_authenticated(model: CModel) -> str:
    """
    All connections between services should be authenticated.
    """
    edges: set[CEdge] = model.edges.edges
    for edge in edges:
        edge_is_authenticated = AllConnections.get_stereotypes()[1] in without_traceability(edge.stereotypes)
        sender_and_receiver_internal = AllServices.get_stereotypes()[3] in without_traceability(edge.sender.stereotypes) and AllServices.get_stereotypes()[3] in without_traceability(edge.receiver.stereotypes)
        if sender_and_receiver_internal and not edge_is_authenticated:
            edge.stereotypes.extend(with_traceability(AllConnections.get_stereotypes()[1]))
    return unparse_model(model)

def r24_outer_connections_encrypted(model: CModel) -> str:
    """
    All connections between a service and an external entity should be encrypted.
    """
    edges: set[CEdge] = model.edges.edges
    for edge in edges:
        edge_is_encrypted = AllConnections.get_stereotypes()[2] in without_traceability(edge.stereotypes)
        if not edge_is_encrypted:
            edge.stereotypes.extend(with_traceability(AllConnections.get_stereotypes()[2]))
    return unparse_model(model)

def r25_inner_connections_encrypted(model: CModel) -> str:
    """
    All connections between two services should be encrypted.
    """
    edges: set[CEdge] = model.edges.edges
    for edge in edges:
        edge_is_encrypted = AllConnections.get_stereotypes()[2] in without_traceability(edge.stereotypes)
        if not edge_is_encrypted:
            edge.stereotypes.extend(with_traceability(AllConnections.get_stereotypes()[2]))
    return unparse_model(model)