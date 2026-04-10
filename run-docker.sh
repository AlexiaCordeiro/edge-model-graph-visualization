#!/bin/bash

# ============================================================
# CONFIGURAÇÕES – edite conforme necessário
# ============================================================

# Nome da imagem Docker
IMAGE_NAME="cfggrid-model-explorer"

# Nome do container (opcional)
CONTAINER_NAME="cfggrid-dev"

# Diretório do repositório local (use $PWD para o diretório atual)
# Exemplo: HOST_REPO_DIR="${PWD}"
HOST_REPO_DIR="${PWD}"

# Diretório de trabalho dentro do container
CONTAINER_WORKDIR="/workspace"

# (Opcional) Montar chaves SSH? Deixe vazio para não montar.
# Exemplo: HOST_SSH="${HOME}/.ssh"
HOST_SSH=""

# Usar rede do host? (necessário para acessar Model Explorer no navegador)
USE_HOST_NETWORK=true

# Remover container ao sair? (recomendado)
RM_CONTAINER=true

# ============================================================
# NÃO EDITE A PARTIR DAQUI
# ============================================================

# Constrói a imagem se não existir
if [[ -z "$(docker images -q "$IMAGE_NAME" 2>/dev/null)" ]]; then
    echo "Construindo imagem '$IMAGE_NAME'..."
    docker build -t "$IMAGE_NAME" .
fi

# Remove container antigo
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Removendo container antigo '$CONTAINER_NAME'..."
    docker rm -f "$CONTAINER_NAME" 2>/dev/null
fi

# Monta volumes
VOLUMES="--volume \"$HOST_REPO_DIR:$CONTAINER_WORKDIR\""
if [[ -n "$HOST_SSH" ]]; then
    VOLUMES="$VOLUMES --volume \"$HOST_SSH:/root/.ssh:ro\""
fi

# Rede
NETWORK_ARG=""
if [[ "$USE_HOST_NETWORK" == "true" ]]; then
    NETWORK_ARG="--network host"
fi

# Remoção
RM_ARG=""
if [[ "$RM_CONTAINER" == "true" ]]; then
    RM_ARG="--rm"
fi

# Comando final
CMD="docker run -it $RM_ARG $NETWORK_ARG --name \"$CONTAINER_NAME\" $VOLUMES -w \"$CONTAINER_WORKDIR\" \"$IMAGE_NAME\" bash"
echo "Executando: $CMD"
eval "$CMD"
