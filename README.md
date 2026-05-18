# Edge Model Graph Visualization

Edge Model Graph Visualization is an adapter that brings [CFGgrind](https://github.com/rimsa/CFGgrind) control-flow graphs (CFGs) into Google's **AI Edge Model Explorer**. It provides an interactive, hierarchical view of dynamic control flow, complete with assembly metadata and iteration counts.

<img width="1918" height="966" alt="funcionamento" src="https://github.com/user-attachments/assets/3b4b3cb5-feae-484f-b317-b8626a8a19e4" />


---

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation](#installation)
  - [Option A — Native Installation](#option-a--native-installation)
  - [Option B — Docker](#option-b--docker)
- [Usage](#usage)
  - [Basic Workflow](#basic-workflow)
  - [Command-Line Reference](#command-line-reference)
  - [Examples](#examples)
  - [Output Files](#output-files)
- [Troubleshooting](#troubleshooting)

---

## System Requirements

| OS                                         | Notes                                                                               |
| ------------------------------------------ | ----------------------------------------------------------------------------------- |
| Windows                                    | Use [WSL2](https://learn.microsoft.com/pt-br/windows/wsl/install) with Ubuntu 22.04 |
| Ubuntu 22.04+, Debian 12+, Fedora 36+, MAC | Native installation works                                                           |
| Other Linux distros or older glibc         | Use the Docker image                                                                |

Please ensure that you have:

Python version > **3.9**

glibc version > **2.17**

PIP version > **0.1.21**

---

## Installation

### Option A — Native Installation

Only recommended if you're on Ubuntu 22.04+, MAC or a distro with a compatible `glibc`.

```bash
cd CFGgrid_ME
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

| Flag                         | Purpose                                                    |
| ---------------------------- | ---------------------------------------------------------- |
| `--network host`             | Exposes the web UI at `http://localhost:8080` on your host |
| `--volume $(pwd):/workspace` | Mounts your local files into the container                 |
| `-w /workspace`              | Sets the working directory inside the container            |
| `-it`                        | Runs interactively with a terminal                         |

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

---

## Usage

**Start the server to test if the installation worked**

**If you are on the docker, please use --host=0.0.0.0 to create a tunneling**

```bash
model-explorer --extensions CFGgrid_ME
```

Then open **<http://localhost:8080>** in your browser.

---

### Basic Workflow

```bash
python create_model.py -m input.cfg -c
```

This generates `generated_files/<basename>_adapted.cfg`. From there:

1. Open **<http://localhost:8080>** in your browser.
2. Upload the generated `.cfg` file using the upload button.
3. Click nodes to inspect details, navigate into called functions, and view edge frequencies.

---

### Command-Line Reference

| Option      | Description                                   | Example          |
| ----------- | --------------------------------------------- | ---------------- |
| `-g <file>` | Input CFG file (from CFGgrind)                | `-g test.cfg`    |
| `-m <file>` | Map file (`.map`) with assembly metadata      | `-m test.map`    |
| `-f <name>` | Focus on a single function's CFG              | `-f bubble_sort` |
| `-c`        | Convert only — skip opening Model Explorer    | `-c`             |
| `-r`        | Launch Model Explorer with an empty workspace | `-r`             |

---

### Examples

Convert the full program and open Model Explorer:

```bash
python create_model.py -g  <file>.cfg
```

Convert only, without launching the UI:

```bash
python create_model.py -g <file>.cfg -c
```

Extract a single function's CFG with assembly metadata:

```bash
python create_model.py -g <file>.cfg -m <file>.map -f main -c
# Output: generated_files/main_metadata.cfg
```

Launch Model Explorer with an empty workspace (for manual file uploads):

```bash
python create_model.py -r
```

---

### Output Files

All output files are written to `generated_files/`.

| File Pattern     | Description                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------ |
| `*_adapted.cfg`  | Basic CFG — no assembly metadata; smaller and faster to load                               |
| `*_metadata.cfg` | Enriched CFG — includes assembly instructions and iteration counts; requires a `.map` file |

---

## Troubleshooting

| Problem                                   | Solution                                                                            |
| ----------------------------------------- | ----------------------------------------------------------------------------------- |
| `glibc` version error                     | Switch to the Docker installation method                                            |
| Port `8080` already in use                | Use a different port: `model-explorer --port 8081 ...`                              |
| Permission denied on volume mount (Linux) | Add `--user $(id -u):$(id -g)` to `docker run`                                      |
| No graph shown in Model Explorer          | Make sure you've uploaded a valid `.cfg` file — run with `-c` first to generate one |
| Assembly metadata not appearing           | Provide a `.map` file with `-d` and load the `*_metadados.cfg` output               |
