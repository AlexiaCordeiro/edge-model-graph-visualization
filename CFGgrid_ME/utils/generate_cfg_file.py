import sys
from pathlib import Path

# Add src directory to path
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from CFGgrid_ME.generate_cfg_file import *
