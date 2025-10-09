from model_explorer import Adapter, AdapterMetadata, ModelExplorerGraphs, graph_builder
from typing import Dict, List
import re
from pathlib import Path


class CFGgridME(Adapter):
    metadata = AdapterMetadata(
        id="CFGgrid-ME",
        name="CFGgrind Adapter",
        description="TCC PROJECT",
        source_repo="https://github.com/user/my_adapter",
        fileExts=["cfg"],
    )

    def convert(self, model_path: str, settings: Dict) -> ModelExplorerGraphs:
        try:
            with open(model_path, "r") as f:
                file_name = Path(model_path).stem
                cfggrind_model = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading file: {e}")
            return {"graphs": []}

        if not cfggrind_model:
            return {"graphs": []}

        graph = graph_builder.Graph(id=file_name)
        graphs = [graph]
        nodes = []
        edges_connection = {}
        edges = []
        layers = "default"
        for line in cfggrind_model:
            if "cfg" in line:
                layers = re.findall(r"cfg\s+(\S+)", line)
            else:
                edges = self.get_edges(line)
            op_match = re.match(r"^(?:\S+\s+){2}(\S+)", line)

            if not op_match:
                continue
            op_name = op_match.group(1)

            if op_name == '"signal::main(11)"':
                continue

            if "cfg" not in line:
                edges_connection[op_name] = edges
            else:
                edges_connection[op_name] = "None"

            self.create_node(op_name, layers[0], nodes)

        graph.nodes.extend(nodes)
        for node in graph.nodes:
            self.create_edges(node, edges_connection, graph)
        return {"graphs": graphs}

    def create_node(self, op_name, layers, nodes):
        node = graph_builder.GraphNode(
            id=op_name,
            label=op_name.strip('"'),
            namespace=str(layers),
        )
        nodes.append(node)

        return nodes

    def create_edges(self, node, edges_connection, graph):
        node_edges = edges_connection.get(node.id, [])
        for edge in node_edges:

            target_node = next((n for n in graph.nodes if n.id == edge), None)
            if target_node:
                target_node.incomingEdges.append(
                    graph_builder.IncomingEdge(
                        sourceNodeId=node.id,
                        sourceNodeOutputId=node.id,
                        targetNodeInputId=target_node.id,
                    )
                )
        return node

    def get_edges(self, line):
        op_match = re.findall(r"(?<=\[)(.*?)(?=\])", line)
        edges = []
        values = op_match[-1].split(" ")

        for edge in values:
            edge = edge.replace("[", "").replace("]", "").split(":")
            edges.append(edge[0])
        
        return edges

