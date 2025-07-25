FROM ubuntu:24.04

LABEL maintainer="Aléxia Cordeiro"
LABEL description="Development environment with Python and Zsh"

ENV LANG=pt_BR.UTF-8 \
    TZ=UTC \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt update && \
    apt install -y --no-install-recommends locales && \
    locale-gen pt_BR.UTF-8 && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean all

RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
        ca-certificates \
        bat \
        curl \
        htop \
        iotop \
        rsync \
        tar \
        neovim \
        black \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        python3-full \
        sudo \
        unzip \
        git \
        make \
        build-essential \
        zsh \
        fonts-powerline \
        libc6 \
        openssh-client \
        npm && \
    npm install -g neovim && \
    apt autoremove -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel pynvim

ARG USERNAME=alexia
ARG USER_UID=1001

RUN useradd --uid $USER_UID --create-home --shell /bin/zsh $USERNAME && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME && \
    chmod -R 775 /home/$USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir -p /home/$USERNAME/.cache && \
    chown $USERNAME:$USERNAME /home/$USERNAME/.cache && \
    chown -R $USERNAME:$USERNAME /opt/venv

USER $USERNAME
WORKDIR /home/$USERNAME

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k && \
    chmod -R 755 ${ZSH_CUSTOM:-$HOME/.oh-my-zsh} && \
    sed -i 's/^ZSH_THEME=.*/ZSH_THEME="powerlevel10k\/powerlevel10k"/' ~/.zshrc && \
    echo '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh' >> ~/.zshrc && \
    echo "umask 002" >> ~/.zshrc && \
    echo "umask 002" >> ~/.profile
USER root
RUN git clone https://github.com/zsh-users/zsh-syntax-highlighting.git &&  \
	echo "source $WORKDIR/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> $WORKDIR/.zshrc	

USER $USERNAME
HEALTHCHECK --interval=30s --timeout=5s \
    CMD ps aux | grep '[z]sh' || exit 1

EXPOSE 8080
CMD ["zsh"]
