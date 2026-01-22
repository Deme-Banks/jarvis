"""
Compliance Checker - GDPR, HIPAA, PCI-DSS compliance
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime


class ComplianceChecker:
    """Compliance checking for various standards"""
    
    def check_gdpr_compliance(self, data_handling: Dict) -> Dict:
        """Check GDPR compliance"""
        findings = []
        
        # Check data encryption
        if not data_handling.get("encryption", False):
            findings.append({
                "issue": "Data not encrypted",
                "severity": "High",
                "requirement": "GDPR Article 32"
            })
        
        # Check data retention
        if data_handling.get("retention_days", 0) > 365:
            findings.append({
                "issue": "Data retention exceeds 1 year",
                "severity": "Medium",
                "requirement": "GDPR Article 5"
            })
        
        # Check consent management
        if not data_handling.get("consent_obtained", False):
            findings.append({
                "issue": "Consent not obtained",
                "severity": "High",
                "requirement": "GDPR Article 6"
            })
        
        return {
            "standard": "GDPR",
            "findings": findings,
            "compliant": len(findings) == 0
        }
    
    def check_hipaa_compliance(self, security_measures: Dict) -> Dict:
        """Check HIPAA compliance"""
        findings = []
        
        # Check access controls
        if not security_measures.get("access_controls", False):
            findings.append({
                "issue": "Access controls not implemented",
                "severity": "High",
                "requirement": "HIPAA §164.312(a)(1)"
            })
        
        # Check audit logs
        if not security_measures.get("audit_logs", False):
            findings.append({
                "issue": "Audit logs not maintained",
                "severity": "High",
                "requirement": "HIPAA §164.312(b)"
            })
        
        # Check encryption
        if not security_measures.get("encryption", False):
            findings.append({
                "issue": "PHI not encrypted",
                "severity": "High",
                "requirement": "HIPAA §164.312(a)(2)(iv)"
            })
        
        return {
            "standard": "HIPAA",
            "findings": findings,
            "compliant": len(findings) == 0
        }
    
    def check_pci_dss_compliance(self, payment_data: Dict) -> Dict:
        """Check PCI-DSS compliance"""
        findings = []
        
        # Check card data storage
        if payment_data.get("store_card_data", False):
            findings.append({
                "issue": "Card data should not be stored",
                "severity": "Critical",
                "requirement": "PCI-DSS Requirement 3.2"
            })
        
        # Check encryption
        if not payment_data.get("encryption", False):
            findings.append({
                "issue": "Card data not encrypted",
                "severity": "Critical",
                "requirement": "PCI-DSS Requirement 3.4"
            })
        
        # Check network segmentation
        if not payment_data.get("network_segmentation", False):
            findings.append({
                "issue": "Network not segmented",
                "severity": "High",
                "requirement": "PCI-DSS Requirement 1.2"
            })
        
        return {
            "standard": "PCI-DSS",
            "findings": findings,
            "compliant": len(findings) == 0
        }
    
    def generate_compliance_report(self, checks: List[Dict]) -> str:
        """Generate compliance report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "checks": checks,
            "summary": {
                "total_checks": len(checks),
                "compliant": sum(1 for c in checks if c.get("compliant", False)),
                "non_compliant": sum(1 for c in checks if not c.get("compliant", False))
            }
        }
        
        filename = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join("reports", filename)
        os.makedirs("reports", exist_ok=True)
        
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        
        return filepath
