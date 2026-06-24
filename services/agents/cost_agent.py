from typing import List, Dict, Any

from models.finding import Finding


OVERSIZED_INSTANCE_TYPES = {
    "m5.2xlarge",
    "m5.4xlarge",
    "m5.8xlarge",
    "c5.4xlarge",
    "c5.9xlarge",
    "r5.4xlarge",
    "r5.8xlarge"
}


def run_cost_agent(
    terraform_code: str,
    parsed_terraform: Dict[str, Any]
) -> List[Finding]:

    findings: List[Finding] = []

    findings.extend(
        check_s3_lifecycle_policy(terraform_code)
    )

    findings.extend(
        check_s3_intelligent_tiering(
            parsed_terraform
        )
    )

    findings.extend(
        check_oversized_ec2(
            terraform_code,
            parsed_terraform
        )
    )

    return findings


def check_s3_lifecycle_policy(
    terraform_code: str
) -> List[Finding]:

    has_s3_bucket = (
        'resource "aws_s3_bucket"' in terraform_code
    )

    has_lifecycle = (
        'resource "aws_s3_bucket_lifecycle_configuration"'
        in terraform_code
    )

    if has_s3_bucket and not has_lifecycle:

        return [
            Finding(
                title="S3 Lifecycle Policy Missing",
                category="cost_lifecycle",
                severity="LOW",
                source="cost-agent",
                recommendation=(
                    "Configure S3 lifecycle policies "
                    "to transition infrequently accessed "
                    "objects to lower-cost storage classes."
                )
            )
        ]

    return []


def check_s3_intelligent_tiering(
    parsed_terraform: Dict[str, Any]
) -> List[Finding]:

    has_s3_bucket = any(
        resource["type"] == "aws_s3_bucket"
        for resource in parsed_terraform.get(
            "resources",
            []
        )
    )

    if has_s3_bucket:

        return [
            Finding(
                title="S3 Intelligent Tiering Not Configured",
                category="cost_storage",
                severity="LOW",
                source="cost-agent",
                recommendation=(
                    "Consider enabling S3 Intelligent "
                    "Tiering to automatically optimize "
                    "storage costs."
                )
            )
        ]

    return []


def check_oversized_ec2(
    terraform_code: str,
    parsed_terraform: Dict[str, Any]
) -> List[Finding]:

    has_ec2 = any(
        resource["type"] == "aws_instance"
        for resource in parsed_terraform.get(
            "resources",
            []
        )
    )

    if not has_ec2:
        return []

    for instance_type in OVERSIZED_INSTANCE_TYPES:

        if (
            f'instance_type = "{instance_type}"'
            in terraform_code
        ):

            return [
                Finding(
                    title="Potentially Oversized EC2 Instance",
                    category="cost_ec2",
                    severity="MEDIUM",
                    source="cost-agent",
                    recommendation=(
                        f"Detected EC2 instance type "
                        f"'{instance_type}'. Review CPU "
                        f"and memory utilization and "
                        f"consider rightsizing."
                    )
                )
            ]

    return []