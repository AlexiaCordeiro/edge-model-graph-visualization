# Re-export from src/CFGgrid_ME
import sys
from pathlib import Path

# Add src directory to path so imports work
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from CFGgrid_ME.generate_cfg_file import (add_metadata_in_cfg, connect_blocks,
                                          generate_files)
from CFGgrid_ME.get_nodes import (check_if_layer_called,
                                  get_correct_block_via_func_name,
                                  get_correct_block_via_layer, parse_node_line)
from CFGgrid_ME.treat_data import treat_metadata

__all__ = [
    'generate_files',
    'connect_blocks',
    'add_metadata_in_cfg',
    'parse_node_line',
    'get_correct_block_via_func_name',
    'get_correct_block_via_layer',
    'check_if_layer_called',
    'treat_metadata'
]
