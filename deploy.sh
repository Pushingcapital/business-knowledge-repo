#!/bin/bash

# Security Login Automation Deployment Script
# Cutting-edge Selenium automation with Docker deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root. This is not recommended for security reasons."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running. Please start Docker service."
        exit 1
    fi
    
    # Check Python 3.12+
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        log_info "Python version: $PYTHON_VERSION"
    fi
    
    log_success "System requirements check passed"
}

# Setup directories
setup_directories() {
    log_info "Setting up directory structure..."
    
    mkdir -p logs
    mkdir -p screenshots
    mkdir -p downloads
    mkdir -p configs
    mkdir -p monitoring
    
    # Set proper permissions
    chmod 755 logs screenshots downloads configs monitoring
    
    log_success "Directory structure created"
}

# Install local Python dependencies (optional for local development)
install_python_deps() {
    if [[ "$1" == "--local" ]]; then
        log_info "Installing Python dependencies locally..."
        
        if command -v python3 &> /dev/null; then
            python3 -m pip install --user -r requirements.txt
            log_success "Python dependencies installed locally"
        else
            log_warning "Python3 not found, skipping local installation"
        fi
    fi
}

# Build Docker images
build_images() {
    log_info "Building Docker images..."
    
    docker-compose build --no-cache
    
    log_success "Docker images built successfully"
}

# Deploy services
deploy_services() {
    log_info "Deploying services..."
    
    # Stop any existing services
    docker-compose down
    
    # Start services
    docker-compose up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to start..."
    sleep 10
    
    # Check service health
    check_services_health
    
    log_success "Services deployed successfully"
}

# Check service health
check_services_health() {
    log_info "Checking service health..."
    
    # Check Redis
    if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
        log_success "Redis is healthy"
    else
        log_warning "Redis health check failed"
    fi
    
    # Check Prometheus
    if curl -s http://localhost:9090/-/healthy | grep -q "Prometheus is Healthy"; then
        log_success "Prometheus is healthy"
    else
        log_warning "Prometheus health check failed"
    fi
    
    # Check if automation service is running
    if docker-compose ps selenium-automation | grep -q "Up"; then
        log_success "Automation service is running"
    else
        log_warning "Automation service health check failed"
    fi
}

# Setup initial configuration
setup_initial_config() {
    log_info "Setting up initial configuration..."
    
    # Create environment file if it doesn't exist
    if [[ ! -f .env ]]; then
        cat > .env << EOF
# Security Login Automation Environment Variables

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Timezone
TZ=America/New_York

# Monitoring
ENABLE_METRICS=true
ENABLE_SCREENSHOTS=true

# Security
MAX_LOGIN_ATTEMPTS=3
SESSION_TIMEOUT=3600

# Browser Configuration
DEFAULT_BROWSER=chrome
HEADLESS_MODE=false
STEALTH_MODE=true

# Logging
LOG_LEVEL=INFO
EOF
        log_success "Environment configuration created"
    fi
    
    # Create default automation config
    python3 -c "
from security_login_automation import SecurityLoginAutomation
automation = SecurityLoginAutomation()
print('Default configuration initialized')
" 2>/dev/null || log_warning "Could not initialize default config"
}

# Show deployment information
show_deployment_info() {
    log_success "Deployment completed successfully!"
    echo
    echo "🚀 Security Login Automation System is now running!"
    echo
    echo "📊 Monitoring Dashboards:"
    echo "   • Grafana:    http://localhost:3000 (admin/admin123)"
    echo "   • Prometheus: http://localhost:9090"
    echo "   • Metrics:    http://localhost:8080/metrics"
    echo
    echo "🔧 Management Commands:"
    echo "   • Add site:     python3 config_manager.py add"
    echo "   • List sites:   python3 config_manager.py list"
    echo "   • Test login:   python3 config_manager.py test"
    echo
    echo "📁 Important Directories:"
    echo "   • Logs:         ./logs/"
    echo "   • Screenshots:  ./screenshots/"
    echo "   • Config:       ./configs/"
    echo
    echo "🐳 Docker Commands:"
    echo "   • View logs:    docker-compose logs -f"
    echo "   • Stop:         docker-compose down"
    echo "   • Restart:      docker-compose restart"
    echo
    echo "📚 Next Steps:"
    echo "   1. Add your first site: python3 config_manager.py add"
    echo "   2. Test the login: python3 config_manager.py test"
    echo "   3. Monitor via Grafana dashboard"
    echo
}

# Cleanup function
cleanup() {
    log_info "Cleaning up deployment artifacts..."
    
    # Stop services
    docker-compose down
    
    # Remove volumes (optional)
    read -p "Remove all data volumes? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v
        log_info "Data volumes removed"
    fi
    
    # Remove images (optional)
    read -p "Remove Docker images? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down --rmi all
        log_info "Docker images removed"
    fi
    
    log_success "Cleanup completed"
}

# Update deployment
update_deployment() {
    log_info "Updating deployment..."
    
    # Pull latest changes (if in git repo)
    if [[ -d .git ]]; then
        git pull
    fi
    
    # Rebuild and redeploy
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    
    log_success "Deployment updated"
}

# Main deployment function
main() {
    echo "🔐 Security Login Automation Deployment"
    echo "========================================"
    echo
    
    case "${1:-deploy}" in
        "deploy")
            check_root
            check_requirements
            setup_directories
            install_python_deps "$2"
            setup_initial_config
            build_images
            deploy_services
            show_deployment_info
            ;;
        "cleanup")
            cleanup
            ;;
        "update")
            update_deployment
            ;;
        "health")
            check_services_health
            ;;
        "logs")
            docker-compose logs -f
            ;;
        "stop")
            docker-compose down
            log_success "Services stopped"
            ;;
        "start")
            docker-compose up -d
            log_success "Services started"
            ;;
        "restart")
            docker-compose restart
            log_success "Services restarted"
            ;;
        *)
            echo "Usage: $0 {deploy|cleanup|update|health|logs|stop|start|restart}"
            echo
            echo "Commands:"
            echo "  deploy   - Full deployment (default)"
            echo "  cleanup  - Remove all services and data"
            echo "  update   - Update and redeploy"
            echo "  health   - Check service health"
            echo "  logs     - View service logs"
            echo "  stop     - Stop all services"
            echo "  start    - Start all services"
            echo "  restart  - Restart all services"
            echo
            echo "Options for deploy:"
            echo "  --local  - Also install Python deps locally"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 