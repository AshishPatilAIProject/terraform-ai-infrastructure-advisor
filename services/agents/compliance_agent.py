from typing import List

from models.finding import Finding

from services.compliance_mapping import (
    COMPLIANCE_MAP
)


def get_compliance_severity(
    controls: set
) -> str:

    if len(controls) >= 5:
        return "HIGH"

    if len(controls) >= 3:
        return "MEDIUM"

    return "LOW"


def run_compliance_agent(
    findings: List[Finding]
) -> List[Finding]:

    cis_controls = set()
    soc2_controls = set()
    pci_controls = set()

    for finding in findings:

        mapping = COMPLIANCE_MAP.get(
            finding.category
        )

        if not mapping:
            continue

        cis_controls.update(
            mapping.get("cis", [])
        )

        soc2_controls.update(
            mapping.get("soc2", [])
        )

        pci_controls.update(
            mapping.get("pci", [])
        )

    compliance_findings = []

    if cis_controls:

        compliance_findings.append(
            Finding(
                title="CIS Compliance Impact",
                category="cis_compliance",
                severity=get_compliance_severity(
                    cis_controls
                ),
                source="compliance-agent",
                recommendation=(
                    "Affected CIS Controls: "
                    + ", ".join(
                        sorted(cis_controls)
                    )
                    + ". Review related infrastructure findings and remediate violations."
                )
            )
        )

    if soc2_controls:

        compliance_findings.append(
            Finding(
                title="SOC2 Compliance Impact",
                category="soc2_compliance",
                severity=get_compliance_severity(
                    soc2_controls
                ),
                source="compliance-agent",
                recommendation=(
                    "Affected SOC2 Controls: "
                    + ", ".join(
                        sorted(soc2_controls)
                    )
                    + ". Review related infrastructure findings and remediate violations."
                )
            )
        )

    if pci_controls:

        compliance_findings.append(
            Finding(
                title="PCI Compliance Impact",
                category="pci_compliance",
                severity=get_compliance_severity(
                    pci_controls
                ),
                source="compliance-agent",
                recommendation=(
                    "Affected PCI Controls: "
                    + ", ".join(
                        sorted(pci_controls)
                    )
                    + ". Review related infrastructure findings and remediate violations."
                )
            )
        )

    return compliance_findings