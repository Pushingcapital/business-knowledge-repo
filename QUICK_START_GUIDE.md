# 🚀 Quick Start Guide - Security Login Automation

Get your cutting-edge Selenium automation system running in under 10 minutes!

## 📋 Prerequisites

- **Docker** and **Docker Compose** installed
- **Python 3.12+** (optional for local development)
- **Linux/macOS** environment (Windows with WSL2)
- At least **4GB RAM** and **2GB disk space**

## ⚡ Option 1: Super Quick Start (Recommended)

```bash
# Run the automated setup script
python3 quick_start.py
```

This will:
- ✅ Check all dependencies
- ✅ Deploy the entire system with Docker
- ✅ Guide you through adding your first site
- ✅ Test the login immediately
- ✅ Show you all monitoring dashboards

## ⚡ Option 2: Manual Deployment

### 1. Deploy the System
```bash
# Make deployment script executable
chmod +x deploy.sh

# Deploy with full monitoring stack
./deploy.sh deploy
```

### 2. Add Your First Site
```bash
# Interactive site configuration
python3 config_manager.py add
```

### 3. Test the Login
```bash
# Test your configuration
python3 config_manager.py test --site your_site_name
```

## 🎯 Pre-Configured Site Templates

The system includes templates for popular sites:

```bash
# View available templates
python3 site_templates.py

# Quick setup for Gmail
python3 config_manager.py add --template gmail

# Quick setup for GitHub  
python3 config_manager.py add --template github
```

**Available Templates:**
- Gmail/Google Account (with 2FA)
- GitHub (with 2FA)
- Microsoft Account (with 2FA)
- LinkedIn
- Amazon
- Facebook
- Apple ID (with 2FA)
- Dropbox
- Slack
- Discord

## 📊 Access Your Dashboards

After deployment, access these URLs:

- **Grafana Dashboard**: http://localhost:3000
  - Username: `admin`
  - Password: `admin123`

- **Prometheus Metrics**: http://localhost:9090

- **Application Metrics**: http://localhost:8080/metrics

## 🔧 Essential Commands

### Site Management
```bash
# List all configured sites
python3 config_manager.py list

# Enable/disable a site
python3 config_manager.py enable-disable

# Update scheduling
python3 config_manager.py schedule

# Export configuration backup
python3 config_manager.py export
```

### Testing
```bash
# Test specific site
python3 config_manager.py test --site gmail

# Test with visible browser (debugging)
python3 config_manager.py test --site gmail --visible
```

### Docker Management
```bash
# View live logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Start services
docker-compose up -d

# Check service status
docker-compose ps
```

## 🔐 Security Best Practices

### 1. Secure Credential Storage
- Passwords are encrypted with Fernet encryption
- 2FA secrets are stored securely in keyring
- No plaintext credentials in configuration files

### 2. 2FA Setup
```bash
# Generate QR code for new 2FA setup
python3 config_manager.py qr

# Test TOTP generation
python3 -c "
import pyotp
secret = 'YOUR_SECRET_KEY'
print(f'Current TOTP: {pyotp.TOTP(secret).now()}')
"
```

### 3. Backup Your Configuration
```bash
# Export encrypted backup
python3 config_manager.py export

# This creates: automation_backup_YYYYMMDD_HHMMSS.json
```

## 🎛 Advanced Configuration

### Environment Variables
Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
# Edit with your preferred settings
```

### Browser Settings
```yaml
# configs/automation_config.yml
browser:
  type: chrome          # chrome, firefox
  headless: false       # true for background operation
  stealth: true         # anti-detection features
  timeout: 30          # page load timeout
```

### Scheduling
```yaml
sites:
  - name: gmail
    schedule: "0 9 * * *"     # Daily at 9 AM
  - name: github  
    schedule: "0 */6 * * *"   # Every 6 hours
```

## 🔍 Troubleshooting

### Browser Issues
```bash
# Check if Chrome is installed
google-chrome --version

# Test X11 forwarding (Linux)
xvfb-run -a google-chrome --headless --dump-dom https://google.com
```

### Login Failures
```bash
# Enable debug screenshots
export ENABLE_SCREENSHOTS=true

# Check screenshot folder
ls -la screenshots/

# View detailed logs
tail -f logs/automation_*.log
```

### Service Health
```bash
# Check all services
./deploy.sh health

# Individual service checks
docker-compose exec redis redis-cli ping
curl http://localhost:9090/-/healthy
```

## 📈 Monitoring & Alerts

### Grafana Setup
1. Go to http://localhost:3000
2. Login with `admin`/`admin123`
3. Import dashboard from `monitoring/` folder
4. Set up notification channels (Slack, email, etc.)

### Prometheus Metrics
- `security_login_attempts_total` - Login attempts by status
- `security_login_duration_seconds` - Login duration
- `security_active_sessions` - Active sessions

### Log Analysis
```bash
# Search for errors
grep -i error logs/automation_*.log

# View structured logs
cat logs/automation_structured_*.json | jq '.level'

# Monitor live logs
tail -f logs/automation_*.log
```

## 🔄 Daily Operations

### Morning Routine
1. Check Grafana dashboard for overnight activity
2. Review any failed login attempts
3. Update credentials if needed

### Weekly Maintenance
```bash
# Update system
./deploy.sh update

# Clean old logs (older than 30 days)
find logs/ -name "*.log" -mtime +30 -delete

# Backup configuration
python3 config_manager.py export
```

## 🚨 Emergency Procedures

### If Login Fails
1. Check service status: `docker-compose ps`
2. Review logs: `docker-compose logs selenium-automation`
3. Test manually: `python3 config_manager.py test --site SITENAME`
4. Update credentials if needed

### If System is Down
```bash
# Restart everything
docker-compose down && docker-compose up -d

# Check system resources
df -h && free -h

# Review system logs
journalctl -u docker
```

## 💡 Pro Tips

1. **Use Templates**: Start with pre-configured templates for faster setup
2. **Enable 2FA**: More secure and often required by modern sites
3. **Monitor Regularly**: Check Grafana dashboard daily
4. **Keep Backups**: Export configuration weekly
5. **Test Changes**: Always test after modifying configurations

## 🎉 You're Ready!

Your cutting-edge security login automation system is now operational. The system will:

- ✅ Automatically log into configured sites daily at 9 AM
- ✅ Handle 2FA/TOTP codes automatically
- ✅ Capture screenshots for verification
- ✅ Send alerts if login fails
- ✅ Maintain detailed logs and metrics
- ✅ Scale horizontally with Docker Swarm/Kubernetes

**Next Steps:**
1. Add your important sites
2. Set up monitoring alerts
3. Configure backup schedules
4. Enjoy automated security compliance! 🔐 