from microCertiSec.core.node import CNode
from microSecFixer.core.stereotypes import without_traceability


def find_node_with_stereotype(nodes: list[CNode], stereotype: str):
    for node in nodes:
        if stereotype in without_traceability(node.stereotypes):
            return node
    return None

def find_all_nodes_with_stereotype(nodes: list[CNode], stereotype: str):
    result: list[CNode] = []
    for node in nodes:
        if stereotype in without_traceability(node.stereotypes):
            result.append(node)
    return result

def node_is_connected_to(sender: CNode, receiver: CNode):
    return receiver in sender.connected_nodes
