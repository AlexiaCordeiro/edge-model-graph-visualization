from model_explorer import(
        Adapter,
        AdapterMetadata,
        ModelExplorerGraphs,
        graph_builder
        )
from typing import Dict, List
import re

class CFGgridME(Adapter):
    metadata = AdapterMetadata(
        id='CFGgrid-ME',
        name='CFGgrind Adapter',
        description='TCC PROJECT',
        source_repo='https://github.com/user/my_adapter',
        fileExts=['cfg']
    )

    def convert(self, model_path: str, settings: Dict) -> ModelExplorerGraphs:
        try:
            with open(model_path, 'r') as f:
                cfggrind_model = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading file: {e}")
            return {'graphs': []}

        if not cfggrind_model:
            return {'graphs': []}

        graph = graph_builder.Graph(id="cfg_graph")
        graphs = [graph]
        nodes = []
        
        current_namespace = "default"

        for line in cfggrind_model:
            if "cfg" in line:
                layers = re.findall(r'cfg\s+(\S+)', line)
            op_match = re.match(r'^(?:\S+\s+){2}(\S+)', line)
            if not op_match:
                continue
                
            op_name = op_match.group(1)
            if op_name == '"signal::main(11)"':
                continue

            clean_op_name = op_name.strip('"')
            
            node_id = op_name 
            node = graph_builder.GraphNode(
                id=node_id,
                label=clean_op_name,
                namespace=str(layers[0]),
            )
            nodes.append(node)

        graph.nodes.extend(nodes)
        return {'graphs': graphs}
