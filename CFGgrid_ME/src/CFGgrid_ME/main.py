from model_explorer import Adapter, AdapterMetadata, ModelExplorerGraphs, graph_builder
from typing import Dict, List
import re
from pathlib import Path
import os


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

        block, metadata_dict, iterations = self.create_block(cfggrind_model)
        self.create_node(nodes, block)
        graph.nodes.extend(nodes)
        for node in graph.nodes:
            self.create_edges(node, block,graph)  
            self.create_metadata(node, graph, metadata_dict, iterations)
        return {"graphs": graphs}
   
    def create_metadata(self, node, graph, metadata_dict, iterations):
        for item in metadata_dict:
            for operation, meta_list in item.items():
                for i, value in enumerate(meta_list):
                    if operation == node.id:
                        key = self.clean_data(value)
                        value = self.clean_data(meta_list.get(value))
                        if str(node.id) not in iterations:
                            iterations[str(node.id)] = '1'
                        node.outputsMetadata.append(
                            graph_builder.MetadataItem(
                                id=i,
                                attrs=[
                                    graph_builder.KeyValue(
                                        key=key, 
                                        value=value,
                                    )]
                                )
                            )

    def 

    def clean_data(self, line: str):
       clean_line =  line.replace("\\", '').replace("'", '').replace("[", '').replace("]", '')
       return clean_line

    def create_node(self, nodes, block):
        for key in block:
            for value in block[key]:
                node = graph_builder.GraphNode(
                    id=value[0],
                    label=value[0],
                    namespace=key,
                )
                nodes.append(node)

        return nodes

    def create_edges(self, node, block, graph):
        node_edges_map = {}
        for cfg_id, nodes_list in block.items():
            for node_addr, edges in nodes_list:
                node_edges_map[node_addr] = edges

        if node.id in node_edges_map:
            target_nodes = node_edges_map[node.id]

            for target_node_id in target_nodes:
                if target_node_id == "exit":
                    continue

                target_node = next(
                    (n for n in graph.nodes if n.id == target_node_id), None
                )
                if target_node:
                    edge = graph_builder.IncomingEdge(
                        sourceNodeId=node.id,
                        sourceNodeOutputId=node.id,
                        targetNodeInputId=target_node.id,
                    )
                    target_node.incomingEdges.append(edge)

        return node

    def get_edges(self, line):
        op_match = re.findall(r"(?<=\[)(.*?)(?=\])", line)
        edges = []
        values = op_match[-1].split(" ")
        iteration = {}

        for edge in values:
            edge = edge.replace("[", "").replace("]", "").split(":")
            edges.append(edge[0])
            if len(edge) > 1 and 'x' in edge[0]:
                iteration[edge[0]] = edge[1]
                print("iteration", iteration)
            else:
                iteration[edge[0]] = "1"

        return edges, iteration

    def create_block(self, cfggrind_model):
        block = {}
        op_meta = []
        current_layer = ""
        layer = ""
        op_name = ""
        for line in cfggrind_model:
            if (
                "cfg" in line
                and "unknown" not in line
                and "#" not in line
                and "below" not in line

            ):
                match = re.search(r"cfg\s+(\S+)", line)
                if match:
                    current_layer = match.group(1)
                    block[current_layer] = []
                    layer = current_layer.split(":")

            elif layer and line.startswith("[node"):
                if line.startswith(f"[node {layer[0]}"):
                    edges, iterations = self.get_edges(line)
                    op_match = re.match(r"^(?:\S+\s+){2}(\S+)", line)
                    op_name = op_match.group(1)
                    block[current_layer].append((op_name, edges))
            else:
                if op_name:
                    op_meta.append(self.add_metadata(line, op_name))
        return block, op_meta, iterations

    def add_metadata(self, metadata, operation):
        separated_metadata = {} 
        op_meta_dict = {}
        metadata_list = metadata.split("',")
        for data in metadata_list:
            data.replace("\\", "").replace("[", "")
            if ":" in data:
                key, value = data.split(":")
                separated_metadata[key] = value
                op_meta_dict[operation] = separated_metadata
        return op_meta_dict
