from openai import OpenAI
from dotenv import load_dotenv
from models.finding import Finding
from typing import List
import os

SUMMARY_PROMPT_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "prompts",
    "generate_summary_prompt.md"
)

load_dotenv()

client = OpenAI()


def generate_executive_summary(
    findings: List[Finding],
    total_score: int
) -> str:

    findings_text = "\n".join(
        [
            (
                f"Title: {finding.title}\n"
                f"Category: {finding.category}\n"
                f"Severity: {finding.severity}\n"
                f"Score: {finding.score}\n"
            )
            for finding in findings
        ]
    )

    with open(SUMMARY_PROMPT_PATH, "r") as f:
        prompt = f.read().format(
            findings_text=findings_text,
            total_score=total_score
        )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text