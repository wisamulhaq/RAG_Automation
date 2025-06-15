from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import re

# Load environment variables from .env file (if it exists)
load_dotenv()
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
temperature = float(os.getenv("TEMPERATURE", 0.3))

# Initialize AzureChatOpenAI model with corrected parameters
model = AzureChatOpenAI(
    api_version=azure_openai_api_version,
    azure_endpoint=azure_openai_endpoint,
    api_key=azure_openai_api_key,
    azure_deployment=azure_openai_deployment_name,
    temperature=temperature
)

def evaluate_response(
    question,
    response,
    chunk,
    criteria="relevance, factual accuracy, completeness",
    detail_level="brief"
):
    prompt_template = PromptTemplate.from_template(
        """
QUESTION:
{question}

CHUNK_TEXT:
{chunk}

RESPONSE:
{response}

TASK:
You are an expert evaluator.

Evaluate whether the RESPONSE accurately, completely, and relevantly answers the QUESTION using only the CHUNK_TEXT as reference.

CRITERIA: {criteria}
- Do not use any external knowledge.
- Be objective, and provide a {detail_level} explanation.

FORMAT:
Return a JSON object like:
{{ 
  "verdict": "accurate" | "inaccurate" | "partially accurate",
  "explanation": "Your explanation here"
}}
        """
    )

    formatted_prompt = prompt_template.format(
        question=question,
        response=response,
        chunk=chunk,
        criteria=criteria,
        detail_level=detail_level
    )

    evaluation = model.invoke(formatted_prompt)
    cleaned = re.sub(r"^```json\s*|\s*```$", "", evaluation.content.strip())
    return cleaned
