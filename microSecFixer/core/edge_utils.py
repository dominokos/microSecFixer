from microCertiSec.core.node import CNode
from microCertiSec.core.edge import CEdge
from microSecFixer.core.stereotypes import with_traceability, AllConnections


def create_edge(sender: CNode, receiver: CNode) -> CEdge:
    edge_traceability = "traceability"
    return CEdge(sender, receiver, with_traceability(AllConnections.get_stereotypes()), edge_traceability)

def remove_edge(sender: CNode, receiver: CNode, edges: set[CEdge]) -> set[CEdge]:
    for edge in edges:
        if edge.sender == sender and edge.receiver == receiver:
            edges.remove(edge)
            return edges

def edges_switch_receiver(edges: set[CEdge] = {}, receiver: CNode = None) -> set[CNode]:
    for edge in edges:
        edge.receiver = receiver
        edge.sender.connected_nodes.append(receiver)
    return edges

def edges_switch_sender(edges: set[CEdge] = {}, sender: CNode = None) -> set[CNode]:
    for edge in edges:
        edge.sender = sender
        sender.connected_nodes.append(edge.receiver)
    return edges    

def find_all_edges_with_sender(sender: CNode, edges: set[CEdge]) -> set[CEdge]:
    result_edges = {}
    for edge in edges:
        if sender == edge.sender:
            result_edges.add(edge)
    return result_edges

def find_all_edges_with_receiver(receiver:CNode, edges: set[CEdge]) -> set[CEdge]:
    result_edges = {}
    for edge in edges:
        if receiver == edge.receiver:
            result_edges.add(edge)
    return result_edges