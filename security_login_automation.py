#!/usr/bin/env python3
"""
Advanced Security Login Automation System
Cutting-edge Selenium automation with stealth, security, and monitoring features
"""

import asyncio
import json
import os
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import base64
from dataclasses import dataclass
from contextlib import asynccontextmanager

# Core automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Advanced features
import undetected_chromedriver as uc
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from fake_useragent import UserAgent
import pyotp
import qrcode

# Computer vision
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Security and encryption
from cryptography.fernet import Fernet
import keyring

# Monitoring and logging
from loguru import logger
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import sentry_sdk

# Configuration
import yaml
from dotenv import load_dotenv

# Database and storage
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

# Scheduling
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import schedule

load_dotenv()

# Metrics
login_attempts = Counter('security_login_attempts_total', 'Total login attempts', ['site', 'status'])
login_duration = Histogram('security_login_duration_seconds', 'Login duration', ['site'])
active_sessions = Gauge('security_active_sessions', 'Active login sessions', ['site'])

@dataclass
class LoginCredentials:
    """Secure credential storage"""
    username: str
    password: str
    totp_secret: Optional[str] = None
    backup_codes: Optional[List[str]] = None
    site_url: str = ""
    site_name: str = ""

@dataclass
class BrowserConfig:
    """Browser configuration settings"""
    browser_type: str = "chrome"
    headless: bool = False
    stealth_mode: bool = True
    user_data_dir: Optional[str] = None
    proxy: Optional[str] = None
    user_agent: Optional[str] = None

class SecurityLoginAutomation:
    """Advanced security login automation system"""
    
    def __init__(self, config_path: str = "configs/automation_config.yml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.setup_logging()
        self.setup_database()
        self.setup_redis()
        self.setup_monitoring()
        self.encryption_key = self.get_or_create_encryption_key()
        self.ua = UserAgent()
        self.scheduler = AsyncIOScheduler()
        
    def load_config(self) -> Dict:
        """Load configuration from YAML file"""
        config_file = Path(self.config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Create default config
            default_config = {
                'browser': {
                    'type': 'chrome',
                    'headless': False,
                    'stealth': True,
                    'timeout': 30,
                    'implicit_wait': 10
                },
                'security': {
                    'max_attempts': 3,
                    'retry_delay': 60,
                    'session_timeout': 3600,
                    'enable_2fa': True
                },
                'monitoring': {
                    'enable_screenshots': True,
                    'enable_metrics': True,
                    'log_level': 'INFO'
                },
                'sites': []
            }
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
    
    def setup_logging(self):
        """Configure advanced logging"""
        log_level = self.config.get('monitoring', {}).get('log_level', 'INFO')
        logger.remove()
        
        # Console logging
        logger.add(
            lambda msg: print(msg, end=""),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level
        )
        
        # File logging
        logger.add(
            "logs/automation_{time:YYYY-MM-DD}.log",
            rotation="1 day",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            level=log_level
        )
        
        # JSON logging for structured analysis
        logger.add(
            "logs/automation_structured_{time:YYYY-MM-DD}.json",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            serialize=True,
            rotation="1 day",
            retention="30 days"
        )
    
    def setup_database(self):
        """Setup SQLAlchemy database"""
        Base = declarative_base()
        
        class LoginSession(Base):
            __tablename__ = 'login_sessions'
            
            id = Column(Integer, primary_key=True)
            site_name = Column(String(100), nullable=False)
            username = Column(String(100), nullable=False)
            login_time = Column(DateTime, default=datetime.utcnow)
            success = Column(Boolean, nullable=False)
            session_duration = Column(Integer)  # seconds
            error_message = Column(Text)
            screenshot_path = Column(String(500))
            
        self.engine = create_engine('sqlite:///logs/login_sessions.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()
        self.LoginSession = LoginSession
    
    def setup_redis(self):
        """Setup Redis connection for session management"""
        try:
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=0,
                decode_responses=True
            )
            self.redis_client.ping()
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            self.redis_client = None
    
    def setup_monitoring(self):
        """Setup Prometheus metrics server"""
        if self.config.get('monitoring', {}).get('enable_metrics', True):
            try:
                start_http_server(8080)
                logger.info("Prometheus metrics server started on port 8080")
            except Exception as e:
                logger.warning(f"Failed to start metrics server: {e}")
    
    def get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for credentials"""
        key_file = Path("configs/.encryption_key")
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            os.makedirs(key_file.parent, exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
            os.chmod(key_file, 0o600)  # Restrict permissions
            return key
    
    def encrypt_credentials(self, credentials: LoginCredentials) -> str:
        """Encrypt credentials for secure storage"""
        f = Fernet(self.encryption_key)
        data = {
            'username': credentials.username,
            'password': credentials.password,
            'totp_secret': credentials.totp_secret,
            'backup_codes': credentials.backup_codes,
            'site_url': credentials.site_url,
            'site_name': credentials.site_name
        }
        encrypted_data = f.encrypt(json.dumps(data).encode())
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_credentials(self, encrypted_data: str) -> LoginCredentials:
        """Decrypt credentials from secure storage"""
        f = Fernet(self.encryption_key)
        decoded_data = base64.b64decode(encrypted_data.encode())
        decrypted_data = f.decrypt(decoded_data)
        data = json.loads(decrypted_data.decode())
        return LoginCredentials(**data)
    
    def create_stealth_browser(self, config: BrowserConfig) -> webdriver.Chrome:
        """Create a stealth browser with anti-detection features"""
        if config.browser_type.lower() == "chrome":
            options = uc.ChromeOptions()
            
            # Stealth arguments
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Performance optimizations
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            
            # Privacy and security
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-ipc-flooding-protection")
            
            if config.headless:
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
            
            if config.user_data_dir:
                options.add_argument(f"--user-data-dir={config.user_data_dir}")
            
            if config.proxy:
                options.add_argument(f"--proxy-server={config.proxy}")
            
            if config.user_agent:
                options.add_argument(f"--user-agent={config.user_agent}")
            else:
                options.add_argument(f"--user-agent={self.ua.random}")
            
            # Create undetected Chrome driver
            driver = uc.Chrome(options=options, version_main=None)
            
            if config.stealth_mode:
                stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                )
            
            return driver
        
        elif config.browser_type.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            
            if config.headless:
                options.add_argument("--headless")
            
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference('useAutomationExtension', False)
            options.set_preference("general.useragent.override", config.user_agent or self.ua.random)
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
            return driver
        
        else:
            raise ValueError(f"Unsupported browser type: {config.browser_type}")
    
    def human_like_typing(self, element, text: str, typing_speed: float = 0.1):
        """Simulate human-like typing with random delays"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(typing_speed * 0.5, typing_speed * 1.5))
    
    def random_mouse_movement(self, driver):
        """Add random mouse movements for human-like behavior"""
        action = ActionChains(driver)
        
        # Random movements
        for _ in range(random.randint(2, 5)):
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            action.move_by_offset(x_offset, y_offset)
            action.pause(random.uniform(0.1, 0.5))
        
        action.perform()
    
    def take_screenshot(self, driver, name: str) -> str:
        """Take and save screenshot"""
        if not self.config.get('monitoring', {}).get('enable_screenshots', True):
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/{name}_{timestamp}.png"
        os.makedirs("screenshots", exist_ok=True)
        
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    def solve_captcha_with_ocr(self, driver, captcha_element) -> Optional[str]:
        """Attempt to solve simple text CAPTCHAs using OCR"""
        try:
            # Take screenshot of captcha element
            location = captcha_element.location
            size = captcha_element.size
            
            driver.save_screenshot("temp_captcha.png")
            
            # Crop captcha area
            image = Image.open("temp_captcha.png")
            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']
            
            captcha_image = image.crop((left, top, right, bottom))
            captcha_image.save("captcha_cropped.png")
            
            # Process with OpenCV for better OCR
            cv_image = cv2.imread("captcha_cropped.png")
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply image processing techniques
            kernel = np.ones((1, 1), np.uint8)
            processed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
            processed = cv2.medianBlur(processed, 3)
            
            # OCR
            text = pytesseract.image_to_string(processed, config='--psm 7')
            text = ''.join(filter(str.isalnum, text))
            
            # Cleanup
            os.remove("temp_captcha.png")
            os.remove("captcha_cropped.png")
            
            if text and len(text) > 2:
                logger.info(f"CAPTCHA text detected: {text}")
                return text
            
        except Exception as e:
            logger.error(f"CAPTCHA OCR failed: {e}")
        
        return None
    
    def generate_totp(self, secret: str) -> str:
        """Generate TOTP code for 2FA"""
        totp = pyotp.TOTP(secret)
        return totp.now()
    
    async def perform_login(self, credentials: LoginCredentials, config: BrowserConfig) -> bool:
        """Perform secure login with advanced features"""
        driver = None
        start_time = time.time()
        screenshot_path = ""
        
        try:
            logger.info(f"Starting login process for {credentials.site_name}")
            login_attempts.labels(site=credentials.site_name, status='started').inc()
            
            # Create browser
            driver = self.create_stealth_browser(config)
            driver.implicitly_wait(self.config.get('browser', {}).get('implicit_wait', 10))
            
            # Navigate to login page
            logger.info(f"Navigating to {credentials.site_url}")
            driver.get(credentials.site_url)
            
            # Random delay to appear human
            await asyncio.sleep(random.uniform(2, 5))
            
            # Take initial screenshot
            screenshot_path = self.take_screenshot(driver, f"{credentials.site_name}_initial")
            
            # Find login elements (this is site-specific and would need customization)
            try:
                # Common username field selectors
                username_selectors = [
                    "input[name='username']",
                    "input[name='email']",
                    "input[type='email']",
                    "input[id*='username']",
                    "input[id*='email']",
                    "#username",
                    "#email",
                    ".username",
                    ".email"
                ]
                
                username_field = None
                for selector in username_selectors:
                    try:
                        username_field = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        break
                    except TimeoutException:
                        continue
                
                if not username_field:
                    raise NoSuchElementException("Username field not found")
                
                # Human-like interaction
                self.random_mouse_movement(driver)
                ActionChains(driver).move_to_element(username_field).click().perform()
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
                # Type username
                self.human_like_typing(username_field, credentials.username)
                
                # Find password field
                password_selectors = [
                    "input[name='password']",
                    "input[type='password']",
                    "input[id*='password']",
                    "#password",
                    ".password"
                ]
                
                password_field = None
                for selector in password_selectors:
                    try:
                        password_field = driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except NoSuchElementException:
                        continue
                
                if not password_field:
                    raise NoSuchElementException("Password field not found")
                
                # Type password
                ActionChains(driver).move_to_element(password_field).click().perform()
                await asyncio.sleep(random.uniform(0.5, 1.5))
                self.human_like_typing(password_field, credentials.password)
                
                # Handle CAPTCHA if present
                try:
                    captcha_element = driver.find_element(By.CSS_SELECTOR, "img[src*='captcha'], .captcha img")
                    captcha_text = self.solve_captcha_with_ocr(driver, captcha_element)
                    if captcha_text:
                        captcha_input = driver.find_element(By.CSS_SELECTOR, "input[name*='captcha'], input[id*='captcha']")
                        self.human_like_typing(captcha_input, captcha_text)
                except NoSuchElementException:
                    pass  # No CAPTCHA present
                
                # Submit form
                submit_selectors = [
                    "button[type='submit']",
                    "input[type='submit']",
                    "button[name='login']",
                    ".login-button",
                    "#login-button"
                ]
                
                submit_button = None
                for selector in submit_selectors:
                    try:
                        submit_button = driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except NoSuchElementException:
                        continue
                
                if submit_button:
                    ActionChains(driver).move_to_element(submit_button).click().perform()
                else:
                    # Try pressing Enter on password field
                    password_field.send_keys(Keys.RETURN)
                
                # Wait for page to load
                await asyncio.sleep(random.uniform(3, 7))
                
                # Handle 2FA if required
                if credentials.totp_secret:
                    try:
                        totp_selectors = [
                            "input[name*='code']",
                            "input[name*='token']",
                            "input[name*='2fa']",
                            "input[name*='otp']",
                            "#verification-code",
                            ".verification-code"
                        ]
                        
                        totp_field = None
                        for selector in totp_selectors:
                            try:
                                totp_field = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                )
                                break
                            except TimeoutException:
                                continue
                        
                        if totp_field:
                            totp_code = self.generate_totp(credentials.totp_secret)
                            logger.info("2FA required, entering TOTP code")
                            self.human_like_typing(totp_field, totp_code)
                            
                            # Find and click 2FA submit button
                            totp_submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
                            ActionChains(driver).move_to_element(totp_submit).click().perform()
                            
                            await asyncio.sleep(random.uniform(3, 7))
                        
                    except TimeoutException:
                        logger.info("No 2FA prompt detected")
                
                # Take final screenshot
                screenshot_path = self.take_screenshot(driver, f"{credentials.site_name}_final")
                
                # Check if login was successful (this would need site-specific logic)
                current_url = driver.current_url
                page_source = driver.page_source.lower()
                
                # Common success indicators
                success_indicators = [
                    "dashboard",
                    "welcome",
                    "profile",
                    "logout",
                    "account"
                ]
                
                # Common failure indicators
                failure_indicators = [
                    "error",
                    "invalid",
                    "incorrect",
                    "failed",
                    "try again"
                ]
                
                success = any(indicator in current_url.lower() or indicator in page_source 
                            for indicator in success_indicators)
                
                failed = any(indicator in page_source for indicator in failure_indicators)
                
                if failed:
                    success = False
                
                # Store session info
                if self.redis_client:
                    session_data = {
                        'site_name': credentials.site_name,
                        'username': credentials.username,
                        'login_time': datetime.utcnow().isoformat(),
                        'success': success,
                        'url': current_url
                    }
                    self.redis_client.setex(
                        f"session:{credentials.site_name}:{credentials.username}",
                        self.config.get('security', {}).get('session_timeout', 3600),
                        json.dumps(session_data)
                    )
                
                # Record in database
                session_duration = int(time.time() - start_time)
                db_session = self.LoginSession(
                    site_name=credentials.site_name,
                    username=credentials.username,
                    success=success,
                    session_duration=session_duration,
                    screenshot_path=screenshot_path
                )
                self.db_session.add(db_session)
                self.db_session.commit()
                
                # Update metrics
                status = 'success' if success else 'failed'
                login_attempts.labels(site=credentials.site_name, status=status).inc()
                login_duration.labels(site=credentials.site_name).observe(session_duration)
                
                if success:
                    active_sessions.labels(site=credentials.site_name).inc()
                    logger.success(f"Login successful for {credentials.site_name}")
                else:
                    logger.error(f"Login failed for {credentials.site_name}")
                
                return success
                
            except Exception as e:
                logger.error(f"Login error for {credentials.site_name}: {e}")
                
                # Record failed attempt
                session_duration = int(time.time() - start_time)
                db_session = self.LoginSession(
                    site_name=credentials.site_name,
                    username=credentials.username,
                    success=False,
                    session_duration=session_duration,
                    error_message=str(e),
                    screenshot_path=screenshot_path
                )
                self.db_session.add(db_session)
                self.db_session.commit()
                
                login_attempts.labels(site=credentials.site_name, status='error').inc()
                return False
                
        except Exception as e:
            logger.error(f"Critical error during login: {e}")
            return False
            
        finally:
            if driver:
                try:
                    # Keep session alive for configured time if successful
                    if 'success' in locals() and success:
                        logger.info(f"Keeping session alive for {credentials.site_name}")
                        await asyncio.sleep(random.uniform(30, 120))  # Stay logged in briefly
                    
                    driver.quit()
                except Exception as e:
                    logger.error(f"Error closing browser: {e}")
    
    def add_site_credentials(self, credentials: LoginCredentials):
        """Add encrypted credentials for a site"""
        encrypted_creds = self.encrypt_credentials(credentials)
        
        # Store in keyring for secure access
        keyring.set_password("security_automation", credentials.site_name, encrypted_creds)
        
        # Update config
        site_config = {
            'name': credentials.site_name,
            'url': credentials.site_url,
            'enabled': True,
            'schedule': '0 9 * * *'  # Daily at 9 AM
        }
        
        if 'sites' not in self.config:
            self.config['sites'] = []
        
        # Update or add site
        existing = next((s for s in self.config['sites'] if s['name'] == credentials.site_name), None)
        if existing:
            existing.update(site_config)
        else:
            self.config['sites'].append(site_config)
        
        # Save config
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
        
        logger.info(f"Credentials stored for {credentials.site_name}")
    
    def get_site_credentials(self, site_name: str) -> Optional[LoginCredentials]:
        """Retrieve and decrypt credentials for a site"""
        try:
            encrypted_creds = keyring.get_password("security_automation", site_name)
            if encrypted_creds:
                return self.decrypt_credentials(encrypted_creds)
        except Exception as e:
            logger.error(f"Failed to retrieve credentials for {site_name}: {e}")
        return None
    
    async def run_daily_logins(self):
        """Run scheduled daily logins for all configured sites"""
        logger.info("Starting daily security login routine")
        
        for site_config in self.config.get('sites', []):
            if not site_config.get('enabled', True):
                continue
            
            site_name = site_config['name']
            credentials = self.get_site_credentials(site_name)
            
            if not credentials:
                logger.warning(f"No credentials found for {site_name}")
                continue
            
            browser_config = BrowserConfig(
                browser_type=self.config.get('browser', {}).get('type', 'chrome'),
                headless=self.config.get('browser', {}).get('headless', False),
                stealth_mode=self.config.get('browser', {}).get('stealth', True)
            )
            
            max_attempts = self.config.get('security', {}).get('max_attempts', 3)
            retry_delay = self.config.get('security', {}).get('retry_delay', 60)
            
            for attempt in range(max_attempts):
                try:
                    success = await self.perform_login(credentials, browser_config)
                    if success:
                        break
                    elif attempt < max_attempts - 1:
                        logger.warning(f"Login attempt {attempt + 1} failed for {site_name}, retrying in {retry_delay} seconds")
                        await asyncio.sleep(retry_delay)
                except Exception as e:
                    logger.error(f"Login attempt {attempt + 1} error for {site_name}: {e}")
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(retry_delay)
            
            # Random delay between sites
            await asyncio.sleep(random.uniform(60, 180))
    
    def start_scheduler(self):
        """Start the automated scheduling system"""
        # Schedule daily logins
        self.scheduler.add_job(
            self.run_daily_logins,
            'cron',
            hour=9,
            minute=0,
            id='daily_security_logins'
        )
        
        # Add health check job
        self.scheduler.add_job(
            self.health_check,
            'interval',
            minutes=30,
            id='health_check'
        )
        
        self.scheduler.start()
        logger.info("Scheduler started - daily logins will run at 9:00 AM")
    
    async def health_check(self):
        """Perform system health check"""
        logger.info("Performing health check")
        
        # Check database connection
        try:
            self.db_session.execute("SELECT 1")
            logger.info("Database connection OK")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
        
        # Check Redis connection
        if self.redis_client:
            try:
                self.redis_client.ping()
                logger.info("Redis connection OK")
            except Exception as e:
                logger.error(f"Redis connection failed: {e}")
        
        # Report metrics
        logger.info("Health check completed")

async def main():
    """Main application entry point"""
    automation = SecurityLoginAutomation()
    
    # Example: Add a site's credentials
    # credentials = LoginCredentials(
    #     username="your_username",
    #     password="your_password",
    #     totp_secret="your_2fa_secret",  # Optional
    #     site_url="https://example.com/login",
    #     site_name="example_site"
    # )
    # automation.add_site_credentials(credentials)
    
    # Start the scheduler
    automation.start_scheduler()
    
    logger.info("Security Login Automation System started")
    logger.info("Monitoring dashboard available at: http://localhost:3000 (Grafana)")
    logger.info("Metrics endpoint available at: http://localhost:8080/metrics")
    
    try:
        # Keep the application running
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        automation.scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 