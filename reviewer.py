import json
from openai import OpenAI
from dotenv import load_dotenv
from terraform_reviewer import review_terraform


with open("sample2.tf", "r") as f:
    terraform_code = f.read()

review = review_terraform(terraform_code)

for finding in review["findings"]:
    print(finding["title"])
  




