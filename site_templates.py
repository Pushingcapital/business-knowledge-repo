#!/usr/bin/env python3
"""
Site Templates for Common Login Pages
Pre-configured selectors and settings for popular sites
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SiteTemplate:
    """Template for site-specific login configuration"""
    name: str
    display_name: str
    url_pattern: str
    username_selectors: List[str]
    password_selectors: List[str]
    submit_selectors: List[str]
    totp_selectors: List[str]
    success_indicators: List[str]
    failure_indicators: List[str]
    wait_time: int = 5
    requires_2fa: bool = False
    notes: str = ""

# Pre-configured templates for common sites
SITE_TEMPLATES = {
    "gmail": SiteTemplate(
        name="gmail",
        display_name="Gmail / Google Account",
        url_pattern="accounts.google.com",
        username_selectors=[
            "input[type='email']",
            "#identifierId",
            "input[name='identifier']"
        ],
        password_selectors=[
            "input[type='password']",
            "input[name='password']",
            "#password"
        ],
        submit_selectors=[
            "#identifierNext",
            "#passwordNext",
            "button[type='submit']"
        ],
        totp_selectors=[
            "input[name='totpPin']",
            "#totpPin",
            "input[aria-label*='code']"
        ],
        success_indicators=[
            "myaccount.google.com",
            "gmail.com/mail",
            "accounts.google.com/ManageAccount"
        ],
        failure_indicators=[
            "wrong password",
            "incorrect",
            "try again",
            "account disabled"
        ],
        requires_2fa=True,
        notes="Google requires clicking 'Next' between username and password"
    ),
    
    "github": SiteTemplate(
        name="github",
        display_name="GitHub",
        url_pattern="github.com/login",
        username_selectors=[
            "#login_field",
            "input[name='login']"
        ],
        password_selectors=[
            "#password",
            "input[name='password']"
        ],
        submit_selectors=[
            "input[type='submit']",
            "button[type='submit']"
        ],
        totp_selectors=[
            "input[name='otp']",
            "#app_totp"
        ],
        success_indicators=[
            "github.com/dashboard",
            "github.com/settings",
            "logged-in"
        ],
        failure_indicators=[
            "incorrect username or password",
            "authentication failed"
        ],
        requires_2fa=True,
        notes="GitHub may require additional verification for new devices"
    ),
    
    "linkedin": SiteTemplate(
        name="linkedin",
        display_name="LinkedIn",
        url_pattern="linkedin.com/login",
        username_selectors=[
            "#username",
            "input[name='session_key']"
        ],
        password_selectors=[
            "#password",
            "input[name='session_password']"
        ],
        submit_selectors=[
            "button[type='submit']",
            ".btn__primary--large"
        ],
        totp_selectors=[
            "input[name='pin']",
            "#input__phone_verification_pin"
        ],
        success_indicators=[
            "linkedin.com/feed",
            "linkedin.com/in/",
            "linkedin.com/mynetwork"
        ],
        failure_indicators=[
            "please check your email and password",
            "sign in failed"
        ],
        requires_2fa=False,
        notes="LinkedIn may show CAPTCHA for automated logins"
    ),
    
    "microsoft": SiteTemplate(
        name="microsoft",
        display_name="Microsoft Account",
        url_pattern="login.microsoftonline.com",
        username_selectors=[
            "input[type='email']",
            "input[name='loginfmt']",
            "#i0116"
        ],
        password_selectors=[
            "input[type='password']",
            "input[name='passwd']",
            "#i0118"
        ],
        submit_selectors=[
            "#idSIButton9",
            "input[type='submit']",
            "button[type='submit']"
        ],
        totp_selectors=[
            "input[name='otc']",
            "#idTxtBx_SAOTCC_OTC"
        ],
        success_indicators=[
            "portal.office.com",
            "outlook.office.com",
            "myaccount.microsoft.com"
        ],
        failure_indicators=[
            "sign-in name or password",
            "account doesn't exist",
            "incorrect password"
        ],
        requires_2fa=True,
        notes="Microsoft uses multi-step authentication flow"
    ),
    
    "amazon": SiteTemplate(
        name="amazon",
        display_name="Amazon",
        url_pattern="amazon.com/ap/signin",
        username_selectors=[
            "#ap_email",
            "input[name='email']"
        ],
        password_selectors=[
            "#ap_password",
            "input[name='password']"
        ],
        submit_selectors=[
            "#signInSubmit",
            "input[type='submit']"
        ],
        totp_selectors=[
            "input[name='otpCode']",
            "#auth-mfa-otpcode"
        ],
        success_indicators=[
            "amazon.com/gp/homepage",
            "your account",
            "prime"
        ],
        failure_indicators=[
            "password is incorrect",
            "cannot find an account",
            "enter a valid email"
        ],
        requires_2fa=False,
        notes="Amazon may require additional verification steps"
    ),
    
    "facebook": SiteTemplate(
        name="facebook",
        display_name="Facebook",
        url_pattern="facebook.com/login",
        username_selectors=[
            "#email",
            "input[name='email']"
        ],
        password_selectors=[
            "#pass",
            "input[name='pass']"
        ],
        submit_selectors=[
            "button[type='submit']",
            "#loginbutton"
        ],
        totp_selectors=[
            "input[name='approvals_code']",
            "#checkpointSubmitButton"
        ],
        success_indicators=[
            "facebook.com/home",
            "facebook.com/profile",
            "data-testid"
        ],
        failure_indicators=[
            "password that you've entered is incorrect",
            "email or phone number you entered"
        ],
        requires_2fa=False,
        notes="Facebook frequently changes selectors and may require additional verification"
    ),
    
    "apple": SiteTemplate(
        name="apple",
        display_name="Apple ID",
        url_pattern="appleid.apple.com/sign-in",
        username_selectors=[
            "#account_name_text_field",
            "input[type='email']"
        ],
        password_selectors=[
            "#password_text_field",
            "input[type='password']"
        ],
        submit_selectors=[
            "#sign-in",
            "button[type='submit']"
        ],
        totp_selectors=[
            "input[maxlength='6']",
            ".form-textbox-character"
        ],
        success_indicators=[
            "appleid.apple.com/account",
            "icloud.com"
        ],
        failure_indicators=[
            "apple id or password",
            "incorrect"
        ],
        requires_2fa=True,
        notes="Apple ID requires 2FA and may send codes to trusted devices"
    ),
    
    "dropbox": SiteTemplate(
        name="dropbox",
        display_name="Dropbox",
        url_pattern="dropbox.com/login",
        username_selectors=[
            "input[name='login_email']",
            ".login-form input[type='email']"
        ],
        password_selectors=[
            "input[name='login_password']",
            ".login-form input[type='password']"
        ],
        submit_selectors=[
            "button[type='submit']",
            ".login-button"
        ],
        totp_selectors=[
            "input[name='sms_code']",
            "input[name='totp_token']"
        ],
        success_indicators=[
            "dropbox.com/home",
            "dropbox.com/files"
        ],
        failure_indicators=[
            "incorrect email or password",
            "login failed"
        ],
        requires_2fa=False,
        notes="Dropbox may require phone verification"
    ),
    
    "slack": SiteTemplate(
        name="slack",
        display_name="Slack",
        url_pattern="slack.com/signin",
        username_selectors=[
            "#email",
            "input[type='email']"
        ],
        password_selectors=[
            "#password",
            "input[type='password']"
        ],
        submit_selectors=[
            "#signin_btn",
            "button[type='submit']"
        ],
        totp_selectors=[
            "input[name='code']",
            ".c-input_text"
        ],
        success_indicators=[
            "app.slack.com",
            "workspace"
        ],
        failure_indicators=[
            "email and password don't match",
            "workspace not found"
        ],
        requires_2fa=False,
        notes="Slack workspace URL varies by organization"
    ),
    
    "discord": SiteTemplate(
        name="discord",
        display_name="Discord",
        url_pattern="discord.com/login",
        username_selectors=[
            "input[name='email']",
            "input[type='email']"
        ],
        password_selectors=[
            "input[name='password']",
            "input[type='password']"
        ],
        submit_selectors=[
            "button[type='submit']",
            ".marginBottom8-AtZOdT"
        ],
        totp_selectors=[
            "input[maxlength='8']",
            ".inputDefault-_djjkz"
        ],
        success_indicators=[
            "discord.com/channels",
            "discord.com/app"
        ],
        failure_indicators=[
            "login or password is invalid",
            "account disabled"
        ],
        requires_2fa=False,
        notes="Discord has 6-digit backup codes in addition to TOTP"
    ),
    
    "experian": SiteTemplate(
        name="experian",
        display_name="Experian Credit Monitoring",
        url_pattern="experian.com/login",
        username_selectors=[
            "#username",
            "input[name='username']",
            "input[type='email']",
            "#email"
        ],
        password_selectors=[
            "#password",
            "input[name='password']",
            "input[type='password']"
        ],
        submit_selectors=[
            "button[type='submit']",
            "#submit",
            ".btn-primary",
            "input[type='submit']"
        ],
        totp_selectors=[
            "input[name='verificationCode']",
            "input[name='code']",
            "#verificationCode",
            ".verification-code-input"
        ],
        success_indicators=[
            "experian.com/consumer/cac/dashboard",
            "experian.com/membercenter",
            "dashboard",
            "credit-report",
            "member center"
        ],
        failure_indicators=[
            "invalid username or password",
            "incorrect login",
            "authentication failed",
            "login failed",
            "error"
        ],
        requires_2fa=False,
        wait_time=8,
        notes="Experian may require additional security questions or phone verification. Login URL may vary (experian.com/login or members.experian.com). Site sometimes uses heavy JavaScript loading."
    )
}

def get_template(site_name: str) -> Optional[SiteTemplate]:
    """Get template for a specific site"""
    return SITE_TEMPLATES.get(site_name.lower())

def list_available_templates() -> List[str]:
    """Get list of available site templates"""
    return [template.display_name for template in SITE_TEMPLATES.values()]

def search_templates(query: str) -> List[SiteTemplate]:
    """Search templates by name or URL pattern"""
    query = query.lower()
    results = []
    
    for template in SITE_TEMPLATES.values():
        if (query in template.name.lower() or 
            query in template.display_name.lower() or 
            query in template.url_pattern.lower()):
            results.append(template)
    
    return results

def get_template_by_url(url: str) -> Optional[SiteTemplate]:
    """Find template that matches a given URL"""
    url = url.lower()
    
    for template in SITE_TEMPLATES.values():
        if template.url_pattern in url:
            return template
    
    return None

def print_template_info(template: SiteTemplate):
    """Print detailed information about a template"""
    print(f"\n📋 Template: {template.display_name}")
    print(f"   Name: {template.name}")
    print(f"   URL Pattern: {template.url_pattern}")
    print(f"   2FA Required: {'Yes' if template.requires_2fa else 'No'}")
    if template.notes:
        print(f"   Notes: {template.notes}")
    print(f"   Username Selectors: {', '.join(template.username_selectors[:2])}...")
    print(f"   Password Selectors: {', '.join(template.password_selectors[:2])}...")

if __name__ == "__main__":
    print("🏠 Available Site Templates:")
    print("=" * 50)
    
    for template in SITE_TEMPLATES.values():
        print_template_info(template)
    
    print(f"\n📊 Total Templates: {len(SITE_TEMPLATES)}")
    print("\nUse these templates to quickly configure common sites!")
    print("Example: python3 config_manager.py add --template gmail") 