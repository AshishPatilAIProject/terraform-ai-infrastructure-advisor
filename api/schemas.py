from pydantic import BaseModel
from typing import List

class TerraformReviewRequest(BaseModel):
    terraform_code: str

class TerraformReviewResponse(BaseModel):
    total_score: int
    findings: List[dict]
    executive_summary: str
    remediation_plan: str