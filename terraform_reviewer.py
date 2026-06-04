from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def review_terraform(terraform_code: str):

    with open("prompt.md", "r") as f:
        prompt = f.read().format(terraform_code=terraform_code)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    raw = response.output_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)