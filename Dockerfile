FROM ubuntu:latest

# Install latest Neovim from official PPA
RUN apt update && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:neovim-ppa/unstable && \
    apt update && \
    apt install -y neovim zsh curl git wget build-essential sudo git-lfs && \
    rm -rf /var/lib/apt/lists/*

RUN chsh -s $(which zsh)
RUN mkdir -p /root/.config/nvim
RUN mkdir -p /root/.ssh
RUN git config --global init.defaultBranch main && \
    git config --global pull.rebase false && \
    git config --global safe.directory /root/.config/nvim

WORKDIR /workspace

CMD ["zsh"]
