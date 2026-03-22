import os
import re
from pathlib import Path
from typing import Dict, List

from model_explorer import (Adapter, AdapterMetadata, ModelExplorerGraphs,
                            graph_builder)

from .get_nodes import parse_node_line


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

        block, metadata_dict, iterations, connected_layer_dict = self.create_block(cfggrind_model)
        self.create_node(nodes, block)
        graph.nodes.extend(nodes)

        for node in graph.nodes:
            self.create_edges(node, block,graph)
            self.add_attributes(node, graph, metadata_dict)
            self.create_metadata(node, iterations)
            self.connect_layers(node, block, graph, connected_layer_dict) if connected_layer_dict else None
        
        return {"graphs": graphs}
   
    def connect_layers(self, node, block, graph, connected_layer_dict):
        """
        Creates edges between nodes in different layers (function calls).
        Connects a calling node to the first/entry node of the called function.
        """
        if node.id in connected_layer_dict:
            target_layer_namespace = connected_layer_dict[node.id]
            target_node = next(
                (n for n in graph.nodes if n.namespace == target_layer_namespace), None
            )
            if target_node:
                edge = graph_builder.IncomingEdge(
                    sourceNodeId=node.id,
                    sourceNodeOutputId=node.id,
                    targetNodeInputId=target_node.id,
                )
                target_node.incomingEdges.append(edge)

    def create_metadata(self, node, iterations):
        if node.id not in iterations:
            iterations[node.id] = '1'
        for operation, iteration in iterations.items():
            if operation == node.id:
                node.outputsMetadata.append(
                    graph_builder.MetadataItem(
                        id=node.id,
                        attrs=[
                                graph_builder.KeyValue(
                                    key='iteration',
                                    value=iteration
                                )]
                            )
                        )

    def add_attributes(self, node, graph, metadata_dict):
        for item in metadata_dict:
            for operation, meta_list in item.items():
                for value in meta_list:
                    if operation == node.id:
                        key = self.clean_data(value)
                        value = self.clean_data(meta_list.get(value))

                        node.attrs.append(graph_builder.KeyValue(
                            key = key,
                            value = value
                        ))
                    

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
            else:
                iteration[edge[0]] = "1"

        return edges, iteration

    def create_block(self, cfggrind_model):
        block = {}
        op_meta = []
        current_layer = ""
        layer = ""
        connected_layers = {}
        layer_address_map = {}
        op_name = ""
        iterations = {}
        for i, line in enumerate(cfggrind_model):
            if (
                "cfg" in line
            ):
                match = re.search(r"cfg\s+(\S+)", line)
                if match:
                    current_layer = match.group(1)
                    block[current_layer] = []
                    layer = current_layer.split(":")
                    layer_address_map[layer[0]] = current_layer

            elif layer and line.startswith("[node"):
                if line.startswith(f"[node {layer[0]}"):
                    edges, iterations = self.get_edges(line)
                    op_match = re.match(r"^(?:\S+\s+){2}(\S+)", line)
                    if op_match:
                        op_name = op_match.group(1)
                        block[current_layer].append((op_name, edges))
                        called_address = parse_node_line(line, 6).replace("[", "").replace("]", "").split(":")[0]
                        if called_address.startswith("0x"):
                            connected_layers[op_name] = called_address
            else:
                if op_name:
                    op_meta.append(self.add_metadata(line, op_name))
        
        for op_name, address in connected_layers.items():
            if address in layer_address_map:
                connected_layers[op_name] = layer_address_map[address]
        
        return block, op_meta, iterations, connected_layers


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
