import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

# If you only set OPENAI_API_KEY but it's an OpenRouter key (sk-or-*), treat it as OpenRouter.
use_openrouter = bool(openrouter_key) or (bool(openai_key) and openai_key.startswith("sk-or-"))

if use_openrouter:
    api_key = openrouter_key or openai_key
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    llm = ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0,
        default_headers={
            "HTTP-Referer": os.getenv("OPENROUTER_REFERER", "https://localhost"),
            "X-Title": os.getenv("OPENROUTER_APP_NAME", "lab4_agent"),
        },
    )
else:
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=model, temperature=0)

try:
    response = llm.invoke("What is the capital of France?")
    print(response.content)
except Exception as e:
    print(f"Lỗi kết nối: {e}")