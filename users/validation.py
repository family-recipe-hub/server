import re
import dns.resolver
from typing import Tuple
from django.core.exceptions import ValidationError

class EmailValidator:
    def __init__(self):
        self.common_typos = {
            'gmil.com': 'gmail.com',
            'gmail.co': 'gmail.com',
            'yahooo.com': 'yahoo.com',
            'yaho.com': 'yahoo.com',
            'hotmal.com': 'hotmail.com',
            'hotmil.com': 'hotmail.com',
            'outloo.com': 'outlook.com',
            'outlok.com': 'outlook.com'
        }
        
        self.valid_tlds = [
            'com', 'org', 'net', 'edu', 'gov', 'mil', 
            'int', 'info', 'io', 'co', 'biz'
        ]
        
        self.blacklisted_domains = [
            'spam.com', 
            'fake.com',
            'temporary.com',
            'disposable.com'
        ]

    def domain_exists(self, domain: str) -> bool:
        """Check if a domain has an MX (Mail Exchange) record."""
        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, 
                dns.resolver.Timeout, dns.exception.DNSException):
            return False

    def check_common_typos(self, email: str) -> Tuple[bool, str, str]:
        """Check for common email domain typos."""
        domain = email.split('@')[1]
        if domain in self.common_typos:
            suggested_domain = self.common_typos[domain]
            suggested_email = f"{email.split('@')[0]}@{suggested_domain}"
            return True, suggested_email, f"Did you mean {suggested_email}?"
        return False, email, ""

    def validate_email(self, value: str) -> str:
        """
        Validate email format, domain, and existence of mail server.
        Returns cleaned email or raises ValidationError.
        """
        # Basic format check
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValidationError("Invalid email format. Please enter a valid email address.")

        # Split email into parts
        try:
            local_part, domain = value.split('@')
        except ValueError:
            raise ValidationError("Invalid email format: missing @ symbol.")

        # Check domain parts
        domain_parts = domain.split('.')
        if len(domain_parts) < 2:
            raise ValidationError("Invalid email domain structure.")

        # Check TLD
        tld = domain_parts[-1].lower()
        if tld not in self.valid_tlds:
            raise ValidationError(f"Invalid email domain extension: .{tld}")

        # Check blacklisted domains
        if domain.lower() in self.blacklisted_domains:
            raise ValidationError("This email domain is not allowed.")

        # Check for common typos
        has_typo, suggested_email, message = self.check_common_typos(value)
        if has_typo:
            raise ValidationError(message)

        # Verify domain exists (MX Record)
        if not self.domain_exists(domain):
            raise ValidationError("This email domain does not exist or cannot receive emails.")

        return value
    
