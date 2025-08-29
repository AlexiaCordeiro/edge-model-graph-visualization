# Installantions 

## DOCKER
### To build the docker
```
docker build -t <<your docker name>> .
```
### To run the docker
```
docker run -ti --rm 
    -v ~/Docker_Share:/data \
    -v ~/docker_configs/nvim:/root/.config/nvim \
    -p 8080:8080 \
    -e GITHUB_TOKEN="$GITHUB_TOKEN" \
    -e GITHUB_USER="$GITHUB_USER" \
    <<your docker name>>
```
## To run the model

```
python3 -m venv venv
source venv/bin/activate
pip install ai-edge-model-explorer
```

```
model-explorer --host=0.0.0.0 --extensions CFGgrid-ME 
```

# TO-DO

[] ADD EDGES
[] ADD METADATA
[] ADD EDGES INFO
