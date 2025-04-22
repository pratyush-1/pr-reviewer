from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

model = Ollama(model=os.getenv("MODEL_NAME"))

prompt = PromptTemplate.from_template(
    "Review ONLY the actual changed code in this diff. "
    "Provide concise feedback. If changes are simple and correct, just say: "
    "'LGTM, ready to merge'. Focus on:\n"
    "1. Actual bugs/errors in the changed lines\n"
    "2. Security issues\n"
    "3. Major style violations ONLY if they affect readability\n\n"
    "Diff:\n{code_diff}\n\n"
    "Review summary:"
)

def review_code(code_diff: str) -> str:
    formatted = prompt.format(code_diff=code_diff)
    return model.invoke(formatted)

if __name__ == "__main__":
    sample_diff = """
    - def add(a, b):
    -     return a + b
    + def add_numbers(a, b):
    +     return a + b
    """
    print(review_code(sample_diff))
