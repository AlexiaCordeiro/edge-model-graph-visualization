# Docker Development Environment Setup Guide

## Quick Start

```bash
# 1. Clone the repository
git clone git@github.com:AlexiaCordeiro/TCC.git
cd TCC

# 2. Set up environment
cp .env.example .env
# Edit .env with your GitHub credentials

# 3. Start development environment
./docker/scripts/run.sh
```

## Prerequisites

- Docker installed
- Docker Compose installed
- GitHub account with personal access token

## Detailed Setup

### 1. Clone the Repository
```bash
git clone git@github.com:AlexiaCordeiro/TCC.git
cd TCC
```

### 2. Configure Environment Variables
```bash
# Copy the environment template
cp .env.example .env

# Edit the file with your credentials
lvim .env  # or your preferred editor
```

**Required .env values:**
```bash
GITHUB_TOKEN=your_actual_github_token_here
GITHUB_USER=your_github_username_here
```

### 3. Get GitHub Personal Access Token
1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token" (classic)
3. Select these scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read organization data)
   - ✅ `read:user` (Read user profile data)
   - ✅ `user:email` (Read user email addresses)
4. Copy the token and paste it in your `.env` file

### 4. Start the Development Environment
```bash
# Make scripts executable (if needed)
chmod +x docker/scripts/run.sh

# Start the container
./docker/scripts/run.sh
```

## Project Structure
```
TCC/
├── docker/                 # Docker configuration
│   ├── Dockerfile         # Container definition
│   ├── docker-compose.yaml # Service configuration
│   └── scripts/
│       └── run.sh         # Startup script
├── data/                  # Data files
└── .env                   # Environment variables (create this)
```

## What's Included
The Docker environment comes pre-configured with:
- **LunarVim** - Modern Neovim-based IDE
- **Python 3.11** with data science packages
- **Jupyter Lab** for notebooks
- **Git** with SSH configuration
- **Rust** and Cargo
- **Development tools**: exa, ripgrep, fd-find, bat

## Daily Usage

### Start Development Session
```bash
./docker/scripts/run.sh
```

### Access Running Container
```bash
# In a new terminal
docker exec -it tcc-dev zsh
```

### Stop the Environment
```bash
# Press Ctrl+C in the terminal running the container
# Or in a new terminal:
docker-compose down
```

## Troubleshooting

### Common Issues

**Permission denied errors:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

**Docker not found:**
```bash
# Install Docker and Docker Compose
sudo apt update
sudo apt install docker.io docker-compose
```

**GitHub authentication failed:**
- Verify your GitHub token has correct scopes
- Check that `.env` file contains correct values
- Ensure token hasn't expired

### Reset Environment
```bash
# Complete reset
docker-compose down
docker system prune -f
./docker/scripts/run.sh
```

### Check Container Status
```bash
docker ps
docker-compose logs
```

## Development Workflow

1. **Start environment**: `./docker/scripts/run.sh`
2. **Code**: Use LunarVim (`lvim`) or your preferred editor
3. **Run experiments**: Use Jupyter notebooks or Python scripts
4. **Version control**: Commit changes with git
5. **Stop**: `Ctrl+C` or `docker-compose down`

## Features
- ✅ Isolated development environment
- ✅ Pre-configured development tools
- ✅ GitHub integration
- ✅ Data science stack ready
- ✅ Persistent workspace data

## Support
If you encounter issues:
1. Check the troubleshooting section above
2. Verify Docker and Docker Compose are installed
3. Ensure GitHub token has correct permissions
4. Check container logs: `docker-compose logs`

---

**Happy coding!** 🚀
