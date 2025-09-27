#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_debug() { echo -e "${BLUE}[DEBUG]${NC} $1"; }

# Function to check requirements
check_requirements() {
    local missing=0
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        missing=1
    fi
    
    # Check Docker Compose
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker-compose"
    elif docker compose version &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker compose"
    else
        print_error "Docker Compose is not installed"
        missing=1
    fi
    
    # Check Docker daemon
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker daemon is not running"
        missing=1
    fi
    
    return $missing
}

# Function to setup environment
setup_environment() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating template..."
        cat > .env << 'EOF'
# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_USER=your_github_username_here

# How to get GitHub Token:
# 1. Go to https://github.com/settings/tokens
# 2. Click 'Generate new token' (classic)
# 3. Select scopes: repo, read:org, read:user, user:email
# 4. Copy the token and paste it below
EOF
        print_status "Please edit .env file with your actual values"
        return 1
    fi
    
    # Load .env file
    set -a
    source .env
    set +a
    
    # Validate environment variables
    if [ -z "$GITHUB_TOKEN" ] || [ "$GITHUB_TOKEN" = "your_github_token_here" ]; then
        print_error "GITHUB_TOKEN is not set in .env file"
        return 1
    fi
    
    if [ -z "$GITHUB_USER" ] || [ "$GITHUB_USER" = "your_github_username_here" ]; then
        print_error "GITHUB_USER is not set in .env file"
        return 1
    fi
    
    print_status "Environment loaded: GITHUB_USER=$GITHUB_USER"
    return 0
}

# Function to build and run
build_and_run() {
    local cmd=$1
    
    print_status "Creating workspace directory..."
    mkdir -p workspace
    
    print_status "Building Docker image (this may take several minutes)..."
    if [ "$cmd" = "docker compose" ]; then
        $cmd build --progress=plain
    else
        $cmd build
    fi
    
    if [ $? -eq 0 ]; then
        print_status "Build successful! Starting container..."
        $cmd up
    else
        print_error "Build failed!"
        return 1
    fi
}

# Main execution
main() {
    echo "=========================================="
    echo "    Model Explorer Development Environment"
    echo "=========================================="
    
    # Check requirements
    print_debug "Checking system requirements..."
    if ! check_requirements; then
        print_error "System requirements not met. Please install Docker and Docker Compose."
        exit 1
    fi
    
    print_status "Docker Compose command: $DOCKER_COMPOSE_CMD"
    
    # Setup environment
    print_debug "Setting up environment..."
    if ! setup_environment; then
        exit 1
    fi
    
    # Build and run
    print_debug "Starting build process..."
    build_and_run "$DOCKER_COMPOSE_CMD"
}

# Run main function
main "$@"
