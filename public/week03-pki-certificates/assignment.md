# Week 3 Assignment: Enterprise Certificate Authority System

**Due**: End of Week 3 (see Canvas for exact deadline)  
**Points**: 25 points  
**Estimated Time**: 6 hours  
**Submission**: Submit Pull Request URL to Canvas

## 🎯 Assignment Overview

Build a focused Certificate Authority (CA) system that demonstrates certificate validation and basic PKI operations. This assignment emphasizes core PKI concepts while providing infrastructure code to reduce complexity.

## 📋 Requirements

### Core Functionality (15 points)

**Focus Area: Certificate Validation Engine**

#### 1. Certificate Validation System (15 points)
- **Certificate chain verification** up to root CA
- **Expiration date checking** 
- **Digital signature validation**
- **Certificate format parsing** and field extraction
- **Basic revocation checking**

*Note: CA infrastructure and CSR processing code provided as starter templates*

### Command-Line Interface (5 points)

Implement validation-focused CLI commands:

```bash
# Validate certificate (primary focus)
python ca_system.py validate --cert-file client.crt

# Check certificate details
python ca_system.py info --cert-file client.crt

# Verify certificate chain
python ca_system.py verify-chain --cert-file client.crt --ca-file ca.crt
```

### Security Features (5 points)

- **Certificate parsing security** with input validation
- **Proper error handling** for malformed certificates
- **Secure validation algorithms** following standards

## 🔧 Technical Specifications

### Required Libraries
```python
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
import datetime
import os
import sys
import argparse
import json
```

### File Structure
```
ca_system.py              # Main implementation
ca_database.json          # Certificate tracking database
ca_private_key.pem        # CA private key (secure permissions)
ca_certificate.pem        # CA public certificate
crl.pem                   # Certificate Revocation List
README.txt                # Usage instructions and design notes
```

### Certificate Database Format
Design a JSON-based database to track issued certificates:
```json
{
  "serial_numbers": ["1234567890", "1234567891"],
  "issued_certificates": [
    {
      "serial_number": "1234567890",
      "subject": "CN=client.example.com,O=Example Corp",
      "issued_date": "2024-01-15T10:30:00",
      "expiry_date": "2025-01-15T10:30:00",
      "status": "active",
      "revocation_date": null,
      "revocation_reason": null
    }
  ]
}
```

## 📝 Detailed Requirements

### 1. CA Initialization
```python
def init_ca(ca_name, key_size=2048, validity_years=10):
    """
    Initialize Certificate Authority
    
    Args:
        ca_name (str): Name for the CA certificate
        key_size (int): RSA key size (default 2048)
        validity_years (int): CA certificate validity period
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Generate RSA private key
    # Create self-signed root certificate
    # Set proper certificate extensions
    # Save private key and certificate securely
```

### 2. CSR Generation and Processing
```python
def create_csr(common_name, organization, email, key_size=2048):
    """
    Generate Certificate Signing Request
    
    Args:
        common_name (str): Subject common name
        organization (str): Organization name
        email (str): Contact email
        key_size (int): RSA key size
        
    Returns:
        tuple: (private_key, csr) objects
    """
    # Generate private key for client
    # Create CSR with proper subject information
    # Add relevant extensions
    # Return both private key and CSR

def sign_csr(csr_file, ca_cert, ca_private_key, validity_days=365):
    """
    Sign CSR and issue certificate
    
    Args:
        csr_file (str): Path to CSR file
        ca_cert: CA certificate object
        ca_private_key: CA private key object
        validity_days (int): Certificate validity period
        
    Returns:
        x509.Certificate: Issued certificate
    """
    # Load and validate CSR
    # Generate unique serial number
    # Create certificate with proper extensions
    # Sign with CA private key
    # Update certificate database
```

### 3. Certificate Validation
```python
def validate_certificate(cert_file, ca_cert):
    """
    Validate certificate against CA
    
    Args:
        cert_file (str): Path to certificate file
        ca_cert: CA certificate object
        
    Returns:
        dict: Validation results with details
    """
    # Load certificate from file
    # Verify signature against CA
    # Check expiration dates
    # Verify certificate chain
    # Check revocation status
    # Return comprehensive validation report
```

## 💻 Example Usage

```bash
$ python ca_system.py init --ca-name "CSCI347 Training CA"
🔐 Generating CA private key (2048 bits)...
📜 Creating root certificate...
✅ Certificate Authority initialized successfully!
   CA Certificate: ca_certificate.pem
   Private Key: ca_private_key.pem (keep secure!)

$ python ca_system.py create-csr --name "student.lab.local" --email "student@university.edu"
🔑 Generating client private key...
📝 Creating certificate signing request...
✅ CSR created successfully!
   Private Key: student.lab.local_private.pem
   CSR File: student.lab.local.csr

$ python ca_system.py sign-csr --csr-file student.lab.local.csr --days 180
📋 Processing certificate signing request...
🔍 Validating CSR contents...
🏷️  Assigning serial number: 1847293856
✅ Certificate issued successfully!
   Certificate: student.lab.local.crt
   Valid until: 2024-07-13 15:42:33

$ python ca_system.py validate --cert-file student.lab.local.crt
🔍 Validating certificate...
✅ Certificate Validation Results:
   Serial Number: 1847293856
   Subject: CN=student.lab.local,O=University Lab,emailAddress=student@university.edu
   Issuer: CN=CSCI347 Training CA
   Valid From: 2024-01-15 15:42:33
   Valid Until: 2024-07-13 15:42:33
   Status: VALID ✅
   Signature: VERIFIED ✅
   Chain: TRUSTED ✅
   Revocation: NOT REVOKED ✅

$ python ca_system.py list-certs
📋 Issued Certificates:
┌─────────────┬──────────────────────┬─────────────┬─────────────────────┬──────────┐
│ Serial      │ Subject              │ Status      │ Expiry Date         │ Days Left│
├─────────────┼──────────────────────┼─────────────┼─────────────────────┼──────────┤
│ 1847293856  │ student.lab.local    │ Active      │ 2024-07-13 15:42:33 │ 179      │
│ 1847293857  │ server.lab.local     │ Active      │ 2024-12-31 09:15:22 │ 351      │
│ 1847293858  │ client.example.com   │ Revoked     │ 2025-01-15 10:30:00 │ -        │
└─────────────┴──────────────────────┴─────────────┴─────────────────────┴──────────┘

$ python ca_system.py revoke --cert-file client.example.com.crt --reason "keyCompromise"
⚠️  Revoking certificate...
🔍 Certificate Serial: 1847293858
📅 Revocation Date: 2024-01-16 14:25:10
🚨 Reason: Key Compromise
✅ Certificate revoked successfully!
   Updated CRL: crl.pem
```

## 📊 Grading Rubric (25 Points Total)

### Component Breakdown

| Component | Weight | Points |
|-----------|---------|---------|
| **Certificate Validation** | 60% | 15 points |
| **CLI Interface** | 20% | 5 points |
| **Security Practices** | 20% | 5 points |

### 5-Point Scale Criteria

**Certificate Validation (15 points)**
- **Excellent (15)**: Comprehensive validation, chain verification, proper parsing, all security checks
- **Proficient (12)**: Good validation logic, most security checks implemented
- **Developing (9)**: Basic validation, some security checks missing
- **Needs Improvement (6)**: Limited validation, security gaps
- **Inadequate (3)**: Poor validation, major security vulnerabilities
- **No Submission (0)**: Missing or no attempt

**CLI Interface (5 points)**
- **Excellent (5)**: All validation commands work perfectly, clear output
- **Proficient (4)**: Most commands work well, good usability
- **Developing (3)**: Basic commands functional, adequate interface
- **Needs Improvement (2)**: Some commands work, poor usability
- **Inadequate (1)**: Major interface problems, commands fail
- **No Submission (0)**: Missing or no attempt

**Security Practices (5 points)**
- **Excellent (5)**: Secure validation algorithms, proper error handling, input validation
- **Proficient (4)**: Good security practices, minor vulnerabilities
- **Developing (3)**: Basic security considerations
- **Needs Improvement (2)**: Limited security practices
- **Inadequate (1)**: Poor or no security considerations
- **No Submission (0)**: Missing or no attempt

### Grade Scale
- **23-25 points (A)**: Professional-quality CA system
- **20-22 points (B)**: Good implementation, minor issues
- **18-19 points (C)**: Satisfactory, meets basic requirements
- **15-17 points (D)**: Below expectations, significant issues
- **Below 15 points (F)**: Unsatisfactory, major problems

## 🚀 Optional Challenge

**Advanced Certificate Analysis**: Implement certificate extension parsing and analysis for Key Usage, Extended Key Usage, and Subject Alternative Name fields. Document findings about certificate security policies.

## 📋 Submission Checklist

Before submitting, verify:

- [ ] **Certificate validation performs all security checks**
- [ ] **Certificate chain verification works correctly**
- [ ] **CLI validation commands work without errors**
- [ ] **Certificate parsing handles various formats**
- [ ] **Error handling for invalid certificates**
- [ ] **Code handles edge cases gracefully**
- [ ] **README.txt explains validation methodology**

### Testing Your CA System
```bash
# Complete workflow test
python ca_system.py init --ca-name "Test CA"
python ca_system.py create-csr --name "test.example.com" --email "test@example.com"
python ca_system.py sign-csr --csr-file test.example.com.csr --days 30
python ca_system.py validate --cert-file test.example.com.crt
python ca_system.py list-certs
python ca_system.py revoke --cert-file test.example.com.crt --reason "cessationOfOperation"

# Error handling tests
python ca_system.py validate --cert-file nonexistent.crt
python ca_system.py sign-csr --csr-file invalid.csr
```

## 📚 Resources and References

### Documentation
- **Cryptography library X.509**: https://cryptography.io/en/latest/x509/
- **RFC 5280 - X.509 Certificate Profile**: https://tools.ietf.org/html/rfc5280
- **RFC 3280 - Certificate Path Validation**: https://tools.ietf.org/html/rfc3280

### Security Guidelines
- **NIST SP 800-57 - Key Management**: https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final
- **CA/Browser Forum Requirements**: https://cabforum.org/baseline-requirements/

### Example Implementation Structure
```python
import argparse
import json
import os
import sys
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class CertificateAuthority:
    def __init__(self, ca_dir="./ca_data"):
        self.ca_dir = Path(ca_dir)
        self.ca_dir.mkdir(exist_ok=True)
        self.db_file = self.ca_dir / "ca_database.json"
        self.ca_cert_file = self.ca_dir / "ca_certificate.pem"
        self.ca_key_file = self.ca_dir / "ca_private_key.pem"
        
    def init_ca(self, ca_name, key_size=2048, validity_years=10):
        """Initialize Certificate Authority"""
        pass
    
    def load_ca_credentials(self):
        """Load CA certificate and private key"""
        pass
    
    def create_csr(self, common_name, organization, email, key_size=2048):
        """Generate Certificate Signing Request"""
        pass
    
    def sign_csr(self, csr_file, validity_days=365):
        """Sign CSR and issue certificate"""
        pass
    
    def validate_certificate(self, cert_file):
        """Validate certificate against CA"""
        pass
    
    def revoke_certificate(self, cert_file, reason):
        """Revoke certificate and update CRL"""
        pass
    
    def list_certificates(self):
        """List all issued certificates"""
        pass
    
    def _load_database(self):
        """Load certificate database"""
        pass
    
    def _save_database(self, data):
        """Save certificate database"""
        pass
    
    def _generate_serial_number(self):
        """Generate unique serial number"""
        pass

def main():
    parser = argparse.ArgumentParser(description="Certificate Authority System")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add subcommands for each CA operation
    init_parser = subparsers.add_parser('init', help='Initialize CA')
    csr_parser = subparsers.add_parser('create-csr', help='Create CSR')
    sign_parser = subparsers.add_parser('sign-csr', help='Sign CSR')
    # ... add other subparsers
    
    args = parser.parse_args()
    ca = CertificateAuthority()
    
    # Handle different commands
    if args.command == 'init':
        ca.init_ca(args.ca_name)
    # ... handle other commands

if __name__ == "__main__":
    main()
```

## ❓ Frequently Asked Questions

**Q: How should I store the CA private key securely?**  
A: Set restrictive file permissions (600) and consider the key as highly sensitive. In production, it would be stored in an HSM.

**Q: What certificate extensions should I include?**  
A: Include Key Usage, Extended Key Usage, Subject Alternative Name, and Authority Key Identifier extensions as appropriate.

**Q: How do I handle certificate serial number collisions?**  
A: Use cryptographically random serial numbers and track all issued serials in your database to prevent duplicates.

**Q: Should certificates be visible in plain text when listed?**  
A: Yes, displaying certificate details helps with administration, but be mindful of sensitive information.

**Q: How complex should the revocation system be?**  
A: Implement basic CRL generation. OCSP is bonus material due to complexity.

## 🔍 Self-Assessment Questions

Before submitting, ask yourself:

1. **Would I trust this CA system in a production environment?**
2. **Does it properly validate all certificate fields and signatures?**
3. **Are private keys adequately protected?**
4. **Does the revocation system work correctly?**
5. **Have I tested all error conditions and edge cases?**

---

**Need Help?**
- Review the PKI tutorial materials
- Check Canvas discussions for common implementation issues
- Attend office hours for debugging assistance
- Use the certificate validation tools to verify your work

**Good luck!** This assignment will give you practical experience with real-world PKI systems used in enterprise security.