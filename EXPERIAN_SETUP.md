# 🏦 Experian Security Login Automation Setup

Complete guide for setting up automated daily Experian credit monitoring login.

## 🚀 Quick Start

### 1. Deploy the System
```bash
# One-command deployment
./deploy.sh deploy

# Wait for services to start (about 2 minutes)
# Check status: docker-compose ps
```

### 2. Add Experian Configuration
```bash
# Access the containerized environment
docker-compose exec selenium-automation python3 config_manager.py add
```

**Interactive Setup:**
```
=== Add New Site for Security Login Automation ===

Site name (e.g., 'gmail', 'github'): experian
Login URL: https://experian.com/login
Username/Email: your_experian_email@example.com
Password: [your secure password - hidden]
Does this site use 2FA/TOTP? (y/n): n

✓ Site 'experian' added successfully!
  URL: https://experian.com/login
  Username: your_experian_email@example.com
  2FA: Disabled

Would you like to test the login now? (y/n): y
```

### 3. Test Your Setup
```bash
# Test the login
docker-compose exec selenium-automation python3 config_manager.py test --site experian

# View the results
docker-compose exec selenium-automation ls -la screenshots/
```

## 🏦 Experian-Specific Features

### Smart Login Detection
The Experian template includes:

- **Multiple username selectors**: `#username`, `input[name='username']`, `input[type='email']`, `#email`
- **Flexible password detection**: `#password`, `input[name='password']`, `input[type='password']`
- **Dynamic submit buttons**: `button[type='submit']`, `#submit`, `.btn-primary`
- **Extended wait times**: 8 seconds (handles slow JavaScript loading)

### Success & Failure Detection
```yaml
Success Indicators:
  - experian.com/consumer/cac/dashboard
  - experian.com/membercenter
  - dashboard
  - credit-report
  - member center

Failure Indicators:
  - invalid username or password
  - incorrect login
  - authentication failed
  - login failed
  - error
```

### Security Questions Handling
- Screenshots capture any additional prompts
- System logs all interactions for review
- Manual intervention alerts for complex verification

## ⚙️ Advanced Configuration

### Schedule Options
```bash
# Update login schedule
docker-compose exec selenium-automation python3 config_manager.py schedule

# Common schedules for credit monitoring:
# Daily at 9 AM: "0 9 * * *"
# Every 12 hours: "0 */12 * * *"
# Weekly (Monday 9 AM): "0 9 * * 1"
# Monthly (1st at 9 AM): "0 9 1 * *"
```

### Environment Variables
Add to your `.env` file:
```env
# Experian-specific settings
EXPERIAN_WAIT_TIME=10
EXPERIAN_RETRY_ATTEMPTS=5
EXPERIAN_SESSION_TIMEOUT=7200
ENABLE_EXPERIAN_SCREENSHOTS=true
```

## 📊 Monitoring Your Experian Automation

### Grafana Dashboard
1. Go to http://localhost:3000
2. Login: admin/admin123
3. View Experian metrics:
   - Login success rate
   - Response times
   - Failed login alerts
   - Session duration

### Key Metrics
```
security_login_attempts_total{site="experian"}
security_login_duration_seconds{site="experian"}
security_active_sessions{site="experian"}
```

### Log Analysis
```bash
# View live Experian logs
docker-compose logs -f selenium-automation | grep -i experian

# Check screenshots
docker-compose exec selenium-automation ls -la screenshots/experian_*

# View structured logs
docker-compose exec selenium-automation cat logs/automation_structured_*.json | jq 'select(.site == "experian")'
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Login Fails - Invalid Credentials
```bash
# Check screenshot
docker-compose exec selenium-automation ls -la screenshots/experian_*

# Update credentials
docker-compose exec selenium-automation python3 config_manager.py add
# Enter same site name to update existing configuration
```

#### 2. Page Takes Too Long to Load
```bash
# Increase wait time in automation config
# Edit configs/automation_config.yml:
browser:
  timeout: 45  # Increase from 30
  implicit_wait: 15  # Increase from 10
```

#### 3. Security Questions Prompt
```bash
# Check screenshot for manual intervention needed
docker-compose exec selenium-automation ls -la screenshots/experian_*

# The system will capture the prompt - respond manually if needed
```

#### 4. CAPTCHA Detected
```bash
# System automatically attempts OCR solving
# Check logs for CAPTCHA detection:
docker-compose logs selenium-automation | grep -i captcha
```

### Debug Mode
```bash
# Run test with visible browser (debug mode)
docker-compose exec selenium-automation python3 config_manager.py test --site experian --debug

# Enable VNC access for remote viewing
# Add to .env: ENABLE_VNC=true
# Access via VNC viewer: localhost:5900
```

## 🔐 Security & Compliance

### Credit Monitoring Compliance
- **Regular Login**: Prevents account dormancy
- **Audit Trail**: Complete log of all access attempts
- **Screenshot Evidence**: Visual proof of successful logins
- **Compliance Reporting**: Prometheus metrics for reporting

### Data Protection
- **Encrypted Storage**: Credentials encrypted with Fernet
- **No Plaintext**: Passwords never stored in plaintext
- **Secure Transmission**: All communications over HTTPS
- **Container Isolation**: Runs in isolated Docker environment

### Best Practices
1. **Regular Testing**: Test monthly to ensure functionality
2. **Credential Rotation**: Update passwords quarterly
3. **Monitor Alerts**: Set up Grafana alerts for failures
4. **Backup Configuration**: Export config monthly
5. **Review Screenshots**: Check login evidence weekly

## 🔄 Operational Commands

### Daily Operations
```bash
# Check automation status
docker-compose ps

# View recent logs
docker-compose logs --tail=50 selenium-automation

# Manual test run
docker-compose exec selenium-automation python3 config_manager.py test --site experian
```

### Weekly Maintenance
```bash
# Backup configuration
docker-compose exec selenium-automation python3 config_manager.py export

# Clean old screenshots (keep 30 days)
docker-compose exec selenium-automation find screenshots/ -name "experian_*" -mtime +30 -delete

# Update system
./deploy.sh update
```

### Emergency Procedures
```bash
# If automation fails repeatedly:
1. Check Experian website status
2. Verify credentials manually
3. Update login URL if changed
4. Restart automation service

# Restart service
docker-compose restart selenium-automation

# Full system restart
docker-compose down && docker-compose up -d
```

## 📈 Expected Results

### Normal Operation
- **Login Success Rate**: >95%
- **Average Duration**: 8-15 seconds
- **Daily Schedule**: Automatic at 9:00 AM
- **Screenshots**: Saved for each attempt
- **Logs**: Detailed activity logging

### Alerts Configuration
```yaml
# Grafana Alert Rules
- Alert: Experian Login Failed
  Condition: failure rate > 10% in 5 minutes
  Action: Send notification

- Alert: Experian Service Down
  Condition: No login attempts in 2 hours during business hours
  Action: Immediate alert
```

## 🎯 Success Criteria

Your Experian automation is working correctly when:

✅ **Daily logins complete successfully**
✅ **Screenshots show dashboard/member center**
✅ **Grafana shows >95% success rate**
✅ **No authentication errors in logs**
✅ **Session maintained for required duration**
✅ **Compliance audit trail generated**

## 🆘 Support

### Common Solutions
- **Slow performance**: Increase browser timeout
- **Element not found**: Check for Experian UI changes
- **Security questions**: Manual intervention may be needed
- **Rate limiting**: Adjust schedule frequency

### Getting Help
1. Check logs: `docker-compose logs selenium-automation`
2. Review screenshots: `docker-compose exec selenium-automation ls screenshots/`
3. Test manually: `python3 config_manager.py test --site experian`
4. Check Experian website changes manually

---

**Your Experian credit monitoring automation is now enterprise-ready! 🏦🔐** 