FROM ubuntu:latest

# Set bash as default shell for RUN commands
SHELL ["/bin/bash", "-c"]

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    ca-certificates \
    curl \
    git \
    wget \
    build-essential \
    sudo \
    git-lfs \
    openssh-client \
    python3 \
    python3-pip \
    python3-venv \
    pkg-config \
    libssl-dev \
    npm \
    nodejs \
    ripgrep \
    fd-find \
    unzip \
    bat \
    zsh \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install latest Rust using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Neovim from PPA
RUN add-apt-repository ppa:neovim-ppa/unstable && \
    apt-get update && \
    apt-get install -y neovim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install LunarVim with stable version and fix treesitter issues
RUN bash <(curl -s https://raw.githubusercontent.com/lunarvim/lunarvim/master/utils/installer/install.sh) -y -- --version stable

# Fix LunarVim treesitter conflict and ensure proper installation
RUN lvim --headless +'Lazy sync' +qa 2>/dev/null || true && \
    rm -rf ~/.cache/lunarvim && \
    lvim --headless +'qall' 2>/dev/null || true

# Install exa via cargo
RUN cargo install exa

# Set default shell to zsh for root
RUN chsh -s "$(which zsh)" root

# Create directory structure
RUN mkdir -p /root/.ssh /root/.oh-my-zsh /workspace /data && \
    chmod 700 /root/.ssh

# Add GitHub to known_hosts (with timeout to avoid hanging)
RUN (ssh-keyscan -T 10 github.com 2>/dev/null || echo "# GitHub key scan completed") >> /root/.ssh/known_hosts && \
    chmod 600 /root/.ssh/known_hosts

# Configure git
RUN git config --global init.defaultBranch main && \
    git config --global pull.rebase false && \
    git config --global safe.directory '*'

# Create a proper .zshrc with better error handling
RUN cat > /root/.zshrc << 'EOF'
# Disable Oh My Zsh permission checks
ZSH_DISABLE_COMPFIX="true"

# Use a simple theme
ZSH_THEME="robbyrussell"

# Source Oh My Zsh if available
if [ -f ~/.oh-my-zsh/oh-my-zsh.sh ]; then
    source ~/.oh-my-zsh/oh-my-zsh.sh
fi

# Custom PATH
export PATH="/root/.cargo/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

# Editor - with fallback to nvim if lvim has issues
if command -v lvim &> /dev/null; then
    export EDITOR=lvim
    export VISUAL=lvim
    alias vim=lvim
    alias nvim=lvim
else
    export EDITOR=nvim
    export VISUAL=nvim
fi

# Useful aliases
alias ls='exa --icons'
alias ll='exa -alF --icons'
alias la='exa -A --icons'
alias l='exa -F --icons'

# Fix for LunarVim treesitter issues
fix-lvim() {
    echo "Fixing LunarVim..."
    lvim --headless +'Lazy sync' +qa 2>/dev/null
    rm -rf ~/.cache/lunarvim
    echo "Fix applied. Restart LunarVim."
}

# Start in workspace
cd /workspace

# Welcome message
echo "=== Model Explorer Container ==="
echo "LunarVim: type 'lvim' to start"
echo "Fix LunarVim: type 'fix-lvim' if you see treesitter errors"
echo "Type 'exit' to leave the container"
echo ""
EOF

WORKDIR /workspace

USER root

# Use interactive zsh with better signal handling
CMD ["zsh", "-i"]
