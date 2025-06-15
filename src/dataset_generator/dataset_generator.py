# First, ensure you have the correct package installed:
# pip install -U langchain-openai

from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables from .env file (if it exists)
load_dotenv()
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
temperature = float(os.getenv("TEMPERATURE", 0.7))

# Initialize AzureChatOpenAI model with corrected parameters
model = AzureChatOpenAI(
    api_version=azure_openai_api_version,
    azure_endpoint=azure_openai_endpoint,
    api_key=azure_openai_api_key,
    azure_deployment=azure_openai_deployment_name,
    temperature=temperature
)

# Question Generator Function
def dataset_generator(chunk, num_questions=5, additional_instruction=""):
    prompt_template = PromptTemplate.from_template(
        """
You are an expert question generator.

Your task is to create diverse and relevant questions based solely on the provided CHUNK_TEXT.

RULES:
- Generate exactly {num_questions} questions.
- Each question must be fully answerable using only the CHUNK_TEXT.
- Do not include any external knowledge or subjective interpretation.
- Vary question types: factual, definitional, and simple inference.
- Keep questions clear, concise, and grammatically correct.
- Avoid ambiguity.

{additional_instruction_section}

OUTPUT FORMAT:
Return a JSON array of objects with only a "question" key, like this:
[
  {{ "question": "Your first question?" }},
]

CHUNK_TEXT:
{chunk}
        """
    )

    # If user provides additional instruction, format it properly
    additional_instruction_section = (
        f"ADDITIONAL INSTRUCTION:\n{additional_instruction}" if additional_instruction else ""
    )

    formatted_prompt = prompt_template.format(
        chunk=chunk,
        num_questions=num_questions,
        additional_instruction_section=additional_instruction_section
    )

    response = model.invoke(formatted_prompt)
    print(f"Generated Questions: {response.content}")
    return response.content
