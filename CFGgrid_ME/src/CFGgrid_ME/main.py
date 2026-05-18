import os
import re
from pathlib import Path
from typing import Dict

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

        block, metadata_dict, iterations, connected_layer_dict, function_names = self.create_block(cfggrind_model)
        layer_key_map = self.create_node(nodes, block, function_names)
        graph.nodes.extend(nodes)

        for node in graph.nodes:
            self.create_edges(node, block,graph)
            self.add_attributes(node, graph, metadata_dict)
            self.create_metadata(node, iterations)
            self.connect_layers(node, block, graph, connected_layer_dict, layer_key_map) if connected_layer_dict else None

        return {"graphs": graphs}
   
    def connect_layers(self, node, block, graph, connected_layer_dict, layer_key_map):
        """
        Creates edges between nodes in different layers (function calls).
        Connects a calling node to the first/entry node of the called function.
        Also resolves indirect calls (A->B->C) so A is connected to C as well.
        """

        def _add_edge(source_id, target_id):
            if source_id and target_id:
                edge = graph_builder.IncomingEdge(
                    sourceNodeId=source_id,
                    sourceNodeOutputId=source_id,
                    targetNodeInputId=target_id,
                )
                target_node = next((n for n in graph.nodes if n.id == target_id), None)
                if target_node is not None:
                    target_node.incomingEdges.append(edge)

        def _resolve_chain(source_id, visited):
            if source_id in visited:
                return
            visited.add(source_id)

            if source_id not in connected_layer_dict:
                return

            target_layers = connected_layer_dict[source_id]
            for target_layer in target_layers:
                # Get the first node id for this target layer
                if target_layer in layer_key_map:
                    target_node_id = layer_key_map[target_layer]
                    _add_edge(source_id, target_node_id)
                    _resolve_chain(target_node_id, visited)

        _resolve_chain(node.id, set())

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

    def create_node(self, nodes, block, function_names):
        layer_key_map = {}  # Maps layer_key to first node id of that layer
        for key in block:
            function_name = function_names.get(key, "")
            namespace_display = function_name if function_name else key.split(":")[0]
            layer_prefix = key.split(":")[0]

            for i, value in enumerate(block[key]):
                node = graph_builder.GraphNode(
                    id=value[0],
                    label=value[0],
                    namespace=namespace_display,
                )
                nodes.append(node)
                # Store the first node's id for this layer to help with lookups
                if i == 0:
                    layer_key_map[key] = node.id

        return layer_key_map

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

    def _extract_function_name(self, cfg_line: str) -> str:
        """
        Extracts the function name from a cfg header line.
        Example: /path/to/file::functionName(142) -> functionName
        """
        match = re.search(r'::(\w+)\(', cfg_line)
        return match.group(1) if match else ""

    def _parse_cfg_header(self, line):
        if "cfg" not in line:
            return None

        match = re.search(r"cfg\s+(\S+)", line)
        return match.group(1) if match else None

    def _is_layer_node_line(self, line, layer_prefix):
        return bool(layer_prefix and line.startswith("[node") and line.startswith(f"[node {layer_prefix}"))

    def _parse_node_line(self, line):
        edges, iterations = self.get_edges(line)
        op_name = None
        called_addresses = []

        op_match = re.match(r"^(?:\S+\s+){2}(\S+)", line)
        if op_match:
            op_name = op_match.group(1)
            called_part = parse_node_line(line, 6).replace("[", "").replace("]", "").strip()
            if called_part:
                called_addresses = [addr.split(":")[0] for addr in called_part.split() if addr.startswith("0x")]

        return op_name, edges, iterations, called_addresses

    def _resolve_connected_layers(self, connected_layers, layer_address_map):
        for op_name, addresses in list(connected_layers.items()):
            resolved = []
            for address in addresses:
                if address in layer_address_map:
                    resolved.append(layer_address_map[address])
                else:
                    resolved.append(address)
            connected_layers[op_name] = resolved
        return connected_layers

    def _collect_op_meta(self, op_meta, metadata_line, op_name):
        if op_name:
            op_meta.append(self.add_metadata(metadata_line, op_name))

    def create_block(self, cfggrind_model):
        block = {}
        op_meta = []
        current_layer = None
        layer_prefix = None
        connected_layers = {}
        layer_address_map = {}
        function_names = {}
        op_name = ""
        iterations = {}

        for line in cfggrind_model:
            header_layer = self._parse_cfg_header(line)
            if header_layer:
                current_layer = header_layer
                block[current_layer] = []
                layer_prefix = current_layer.split(":")[0]
                layer_address_map[layer_prefix] = current_layer
                function_name = self._extract_function_name(line)
                if function_name:
                    function_names[current_layer] = function_name
                continue

            if self._is_layer_node_line(line, layer_prefix):
                parsed_op_name, edges, line_iterations, called_addresses = self._parse_node_line(line)
                iterations.update(line_iterations)

                if parsed_op_name:
                    op_name = parsed_op_name
                    block[current_layer].append((op_name, edges))

                    if called_addresses:
                        connected_layers[op_name] = called_addresses
                continue

            self._collect_op_meta(op_meta, line, op_name)

        connected_layers = self._resolve_connected_layers(connected_layers, layer_address_map)

        return block, op_meta, iterations, connected_layers, function_names

    def add_metadata(self, metadata, operation):
        separated_metadata = {}
        op_meta_dict = {}
        metadata_list = metadata.split("',")

        for data in metadata_list:
            cleaned = data.replace("\\", "").replace("[", "").replace("]", "").strip()
            if ":" in cleaned:
                key, value = cleaned.split(":", 1)
                separated_metadata[key.strip()] = value.strip()
                op_meta_dict[operation] = separated_metadata

        return op_meta_dict
