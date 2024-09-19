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

def remove_edges_between(edges: set[CNode], edges_from_nodes: set[CNode], edges_to_nodes: set[CNode]):
    to_remove = edges_from_nodes & edges_to_nodes
    edges_from_nodes.difference_update(to_remove)
    edges_to_nodes.difference_update(to_remove)
    edges.difference_update(to_remove)

def merge_duplicate_edges(edges: set[CNode]):
    unique_edges_map = {}
    for edge in edges:
        key = (edge.sender, edge.receiver)
        if key in unique_edges_map:
            existing_edge = unique_edges_map[key]
            set(existing_edge.stereotypes).update(edge.stereotypes)
            for tag, value in edge.tagged_values.items():
                if tag not in existing_edge.tagged_values:
                    existing_edge.tagged_values[tag] = value
        else:
            unique_edges_map[key] = edge
    edges.intersection_update(set(unique_edges_map.values()))
            

def edges_switch_receiver(edges: set[CEdge] = set(), receiver: CNode = None) -> set[CNode]:
    for edge in edges:
        edge.receiver = receiver
        if receiver not in edge.sender.connected_nodes:
            edge.sender.connected_nodes.append(receiver)
    return edges

def edges_switch_sender(edges: set[CEdge] = set(), sender: CNode = None) -> set[CNode]:
    for edge in edges:
        edge.sender = sender
        if edge.receiver not in sender.connected_nodes:
            sender.connected_nodes.append(edge.receiver)
    return edges    

def find_all_edges_with_sender(sender: CNode, edges: set[CEdge]) -> set[CEdge]:
    result_edges = set()
    for edge in edges:
        if sender == edge.sender:
            result_edges.add(edge)
    return result_edges

def find_all_edges_with_receiver(receiver:CNode, edges: set[CEdge]) -> set[CEdge]:
    result_edges = set()
    for edge in edges:
        if receiver == edge.receiver:
            result_edges.add(edge)
    return result_edges

def fix_dangling_edges(edges: set[CNode], edges_from_nodes: set[CNode], edges_to_nodes: set[CNode], merged_node: CNode):
    edges_switch_receiver(edges_to_nodes, merged_node)
    edges_switch_sender(edges_from_nodes, merged_node)
    merge_duplicate_edges(edges)