from openai import OpenAI
from dotenv import load_dotenv
from typing import List
from models.finding import Finding

load_dotenv()

client = OpenAI()


def run_compliance_llm(
    findings: List[Finding]
) -> str:

    findings_text = "\n".join(
        [
            (
                f"Title: {f.title}\n"
                f"Category: {f.category}\n"
                f"Severity: {f.severity}\n"
            )
            for f in findings
        ]
    )

    with open(
        "prompts/compliance_agent_prompt.md",
        "r"
    ) as f:
        prompt = f.read().format(
            findings_text=findings_text
        )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text