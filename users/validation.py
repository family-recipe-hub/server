import re
import dns.resolver
from django.core.exceptions import ValidationError

def domain_exists(domain):
    """Check if a domain has an MX (Mail Exchange) record, meaning it can receive emails."""
    try:
        dns.resolver.resolve(domain, 'MX')  # Query MX record
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout, dns.exception.DNSException):
        return False  # Domain does not exist or has no mail server

def validate_email(value):
    """Validate email format, domain, and existence of mail server."""
    blacklisted_domains = ['spam.com', 'fake.com']
    valid_tlds = ['com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'info', 'io', 'co', 'biz']

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        raise ValidationError("Invalid email format.")
    
    email_domain = value.split('@')[-1]  
    domain_parts = email_domain.split('.')

    if len(domain_parts) < 2:
        raise ValidationError("Invalid email domain.")

    tld = domain_parts[-1]
    if tld not in valid_tlds:
        raise ValidationError("Invalid email domain extension.")
    
    if email_domain in blacklisted_domains:
        raise ValidationError("This email domain is not allowed.")
    
    # **Ensure the domain actually exists (MX Record)**
    if not domain_exists(email_domain):
        raise ValidationError("This email domain does not exist or cannot receive emails.")
    
    return value
