from typing import Dict
from model_explorer import Adapter, AdapterMetadata, ModelExplorerGraphs, graph_builder

class MyAdapter(Adapter):

  metadata = AdapterMetadata(id='my_adapter',
                             name='My first adapter',
                             description='My first adapter!',
                             source_repo='https://github.com/user/my_adapter',
                             fileExts=['test'])

  # Required.
  def __init__(self):
    super().__init__()

  def convert(self, model_path: str, settings: Dict) -> ModelExplorerGraphs:
    return {'graphs': []}
