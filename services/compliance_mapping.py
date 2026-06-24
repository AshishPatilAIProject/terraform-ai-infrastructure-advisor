# services/compliance_mapping.py

COMPLIANCE_MAP = {
    "open_ssh": {
        "cis": ["4.1"],
        "soc2": ["CC6.6"],
        "pci": ["1.2"]
    },

    "s3_encryption": {
        "cis": ["3.1"],
        "soc2": ["CC6.1"],
        "pci": ["3.5"]
    },

    "s3_versioning": {
        "cis": ["2.1"],
        "soc2": ["CC7.2"],
        "pci": ["10.5"]
    },

    "s3_public_access": {
        "cis": ["3.2"],
        "soc2": ["CC6.7"],
        "pci": ["7.1"]
    }
}