import json
import os
from microCertiSec.core.node import CNode
from microCertiSec.core.edge import CEdge
from microCertiSec.core.model import CModel
from microSecFixer.core.stereotypes import ExternalEntity

def unparse_model(model: CModel) -> str:
    """
    Unparses the model into a JSON representation and writes to a file.

    Args:
        model (CModel): The model to unparse.

    Returns:
        str: The path to the output JSON file.
    """
    nodes: set[CNode] = model.nodes.nodes
    edges: set[CEdge] = model.edges.edges

    services = []
    external_entities = []
    information_flows = []
    nodes_to_services_or_external_entities(nodes, services, external_entities)
    edges_to_information_flows(edges, information_flows)

    new_dfd = {
        "services": services,
        "external_entities": external_entities,
        "information_flows": information_flows
    }
    
    output_path = f"/output/models/{model.name}"
    relative_output_path = f".{output_path}"
    os.makedirs(os.path.dirname(relative_output_path), exist_ok=True)
    with open(relative_output_path, 'w') as file:
        json.dump(new_dfd, file)
    return output_path


def nodes_to_services_or_external_entities(nodes: set['CNode'], services: list[dict], external_entities: list[dict]):
    """
    Separates nodes into services and external entities.

    Args:
        nodes (set[CNode]): Set of nodes in the model.
        services (list[dict]): List to store services.
        external_entities (list[dict]): List to store external entities.
    """
    for node in nodes:
        entity = {
            "name": node.name,
            "stereotypes": [st[0] for st in node.stereotypes],
            "tagged_values": node.tagged_values
        }
        
        if is_node_external_entity(node):
            external_entities.append(entity)
        else:
            services.append(entity)

def edges_to_information_flows(edges: set['CEdge'], information_flows: list[dict]):
    """
    Converts edges to information flows.

    Args:
        edges (set[CEdge]): Set of edges in the model.
        information_flows (list[dict]): List to store information flows.
    """
    for edge in edges:
        information_flow = {
            "sender": edge.sender.name,
            "receiver": edge.receiver.name,
            "stereotypes": remove_encrypted_stereotype(edge.stereotypes),
            "tagged_values": edge.tagged_values
        }
        information_flows.append(information_flow)

def is_node_external_entity(node: 'CNode') -> bool:
    """
    Checks if a node is an external entity.

    Args:
        node (CNode): The node to check.

    Returns:
        bool: True if the node is an external entity, False otherwise.
    """
    stereotypes = [st[0] for st in node.stereotypes]
    external_stereotypes = ExternalEntity.get_stereotypes()
    return external_stereotypes[0] in stereotypes

def remove_encrypted_stereotype(stereotypes: list[tuple]) -> list[str]:
    """
    Removes the 'encrypted' stereotype from the list.

    Args:
        stereotypes (List[tuple]): List of stereotypes as tuples.

    Returns:
        List[str]: List of stereotypes with 'encrypted' removed.
    """
    return [st[0] for st in stereotypes if st[0] != "encrypted"]