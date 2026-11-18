"""
Autonomous AI Cartoon Studio - Asset License Manager & Compliance Guard (V2.0)
Validates asset licenses for commercial YouTube monetization rights and flags non-commercial risks.
"""

PERMITTED_COMMERCIAL_LICENSES = {
    "CC0": {"commercial": True, "attribution": False},
    "MIT": {"commercial": True, "attribution": True},
    "Apache-2.0": {"commercial": True, "attribution": True},
    "BSD-2-Clause": {"commercial": True, "attribution": True},
    "BSD-3-Clause": {"commercial": True, "attribution": True},
    "GPLv3": {"commercial": True, "attribution": True},
    "Public Domain": {"commercial": True, "attribution": False},
    "Commercial-Purchased": {"commercial": True, "attribution": False},
    "Proprietary-Studio": {"commercial": True, "attribution": False}
}

RESTRICTED_NON_COMMERCIAL_LICENSES = [
    "CC-BY-NC", "CC-BY-NC-SA", "CC-BY-NC-ND", "Academic-Research-Only",
    "Non-Commercial", "SMPL-Research", "DeepMotion-Research"
]

class AssetLicenseManager:
    @staticmethod
    def audit_license(license_name: str) -> dict:
        norm = license_name.strip().upper()
        
        # Check forbidden non-commercial tags
        for forbidden in RESTRICTED_NON_COMMERCIAL_LICENSES:
            if forbidden.upper() in norm:
                return {
                    "is_permitted": False,
                    "reason": f"License '{license_name}' contains non-commercial restrictions, prohibited for commercial YouTube channel monetization.",
                    "license_type": license_name,
                    "attribution_required": False
                }
                
        for permitted, spec in PERMITTED_COMMERCIAL_LICENSES.items():
            if permitted.upper() in norm:
                return {
                    "is_permitted": True,
                    "license_type": permitted,
                    "attribution_required": spec["attribution"],
                    "commercial_safe": True
                }
                
        # Default fallback: Treat unknown licenses as requiring human review
        return {
            "is_permitted": False,
            "reason": f"Unknown license '{license_name}'. Requires manual commercial authorization before ingestion.",
            "license_type": "UNKNOWN",
            "attribution_required": True
        }

if __name__ == "__main__":
    alm = AssetLicenseManager()
    print("CC0 Audit:", alm.audit_license("CC0"))
    print("CC-BY-NC Audit:", alm.audit_license("CC-BY-NC 4.0"))
