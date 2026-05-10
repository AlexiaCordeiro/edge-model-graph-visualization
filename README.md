# Edge Model Graph Visualization

Edge Model Graph Visualization is an adapter that brings [CFGgrind](https://github.com/rimsa/CFGgrind) control-flow graphs (CFGs) into Google's **AI Edge Model Explorer**. It provides an interactive, hierarchical view of dynamic control flow, complete with assembly metadata and iteration counts.

---

## System Requirements

| OS | Notes |
|----|-------|
| Windows | Use WSL2 with Ubuntu 22.04 |
| Ubuntu 22.04+, Debian 12+, Fedora 36+, MAC | Native installation works |
| Other Linux distros or older glibc | Use the Docker image |

---

## Installation

### Option A — Native Installation

Only recommended if you're on Ubuntu 22.04+m MAC or a distro with a compatible `glibc`.

```bash
cd CFGgrid_me
python3 -m venv venv
source venv/bin/activate   
pip install ai-edge-model-explorer
pip install -e .
```

---

### Option B — Docker

Docker is the safest choice if you're unsure about your system's `glibc` version.

**1. Build the image**

```bash
docker build -t model-explorer .
```

**2. Start the container**

Run this from the directory containing your `.cfg` files:

```bash
docker run -it --network host \
  --volume $(pwd):/workspace \
  -w /workspace \
  model-explorer
```

| Flag | Purpose |
|------|---------|
| `--network host` | Exposes the web UI at `http://localhost:8080` on your host |
| `--volume $(pwd):/workspace` | Mounts your local files into the container |
| `-w /workspace` | Sets the working directory inside the container |
| `-it` | Runs interactively with a terminal |

**3. Set up the Python environment**

Inside the container and the project folder:

```bash
cd CFGgrid_me
python3 -m venv venv
source venv/bin/activate
pip install ai-edge-model-explorer
pip install -e .
```

> `pip install -e .` assumes the adapter code is in the current directory (`/workspace`). Adjust the path if needed.

**4. Start the server to test if the installation worked**

```bash
model-explorer --host=0.0.0.0 --extensions CFGgrid_ME
```

Then open **http://localhost:8080** in your browser.

---


## Usage

### Basic Workflow

```bash
python create_model.py -m input.cfg -c
```

This generates `generated_files/<basename>_addapted.cfg`. From there:

1. Open **http://localhost:8080** in your browser.
2. Upload the generated `.cfg` file using the upload button.
3. Click nodes to inspect details, navigate into called functions, and view edge frequencies.

---

### Command-Line Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-m <file>` | Input CFG file (from CFGgrind) | `-m test.cfg` |
| `-d <file>` | Map file (`.map`) with assembly metadata | `-d test.map` |
| `-f <name>` | Focus on a single function's CFG | `-f bubble_sort` |
| `-c` | Convert only — skip opening Model Explorer | `-c` |
| `-r` | Launch Model Explorer with an empty workspace | `-r` |

---

### Examples

Convert the full program and open Model Explorer:

```bash
python create_model.py -m test.cfg
```

Convert only, without launching the UI:

```bash
python create_model.py -m test.cfg -c
```

Extract a single function's CFG with assembly metadata:

```bash
python create_model.py -m test.cfg -d test.map -f main -c
# Output: generated_files/main_metadados.cfg
```

Launch Model Explorer with an empty workspace (for manual file uploads):

```bash
python create_model.py -r
```

---

### Output Files

All output files are written to `generated_files/`.

| File Pattern | Description |
|--------------|-------------|
| `*_addapted.cfg` | Basic CFG — no assembly metadata; smaller and faster to load |
| `*_metadados.cfg` | Enriched CFG — includes assembly instructions and iteration counts; requires a `.map` file |

> **Tip:** Use `*_metadados.cfg` whenever you're doing reverse engineering or low-level debugging. Iteration counts on edges highlight hot paths and loop frequencies. Double-click any function call node to drill into its CFG; use the browser back button to return.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `glibc` version error | Switch to the Docker installation method |
| Port `8080` already in use | Use a different port: `model-explorer --port 8081 ...` |
| Permission denied on volume mount (Linux) | Add `--user $(id -u):$(id -g)` to `docker run` |
| No graph shown in Model Explorer | Make sure you've uploaded a valid `.cfg` file — run with `-c` first to generate one |
| Assembly metadata not appearing | Provide a `.map` file with `-d` and load the `*_metadados.cfg` output |
