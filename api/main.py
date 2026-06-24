from fastapi import FastAPI
from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from api.schemas import (
    TerraformReviewRequest,
    TerraformReviewResponse
)

from models.analysis_state import AnalysisState
from graphs.review_graph import graph
from services.report_storage import (
    save_report
)
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Terraform AI Infrastructure Advisor",
    version="0.3.0"
)

@app.get("/")
def health():

    return {
        "status": "ok"
    }


@app.post(
    "/review",
    response_model=TerraformReviewResponse
)
def review(
    request: TerraformReviewRequest
):

    state = AnalysisState(
        terraform_code=request.terraform_code
    )

    result = graph.invoke(state)

    findings = []

    for finding in result["findings"]:

        findings.append(
            {
                "title": finding.title,
                "category": finding.category,
                "severity": finding.severity,
                "score": finding.score
            }
        )

    return TerraformReviewResponse(
        total_score=result["total_score"],
        findings=findings,
        executive_summary=result.get(
            "executive_summary",
            ""
        ),
        remediation_plan=result.get(
            "remediation_plan",
            ""
        )
    )

@app.post("/review/file")
async def review_file(
    terraform_file: UploadFile = File(...)
):

    terraform_code = (
        await terraform_file.read()
    ).decode("utf-8")

    state = AnalysisState(
        terraform_code=terraform_code
    )

    result = graph.invoke(state)

    findings = []

    for finding in result["findings"]:

        findings.append(
            {
                "title": finding.title,
                "category": finding.category,
                "severity": finding.severity,
                "score": finding.score
            }
        )

    return {
        "filename": terraform_file.filename,
        "total_score": result["total_score"],
        "findings": findings,
        "executive_summary": result.get(
            "executive_summary",
            ""
        ),
        "remediation_plan": result.get(
            "remediation_plan",
            ""
        )
    }

@app.post(
    "/review/file/report"
)
async def review_file_report(
    terraform_file: UploadFile = File(...)
):

    terraform_code = (
        await terraform_file.read()
    ).decode("utf-8")

    state = AnalysisState(
        terraform_code=terraform_code
    )

    result = graph.invoke(state)

    report_path = save_report(
        result["report_html"]
    )

    return {
        "filename": terraform_file.filename,
        "total_score": result["total_score"],
        "report_file": report_path
    }

@app.get(
    "/report",
    response_class=HTMLResponse
)
def get_report():

    with open(
        "reports/report.html",
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()