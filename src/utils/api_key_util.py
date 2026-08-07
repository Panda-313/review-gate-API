import getpass
import os


def ensure_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        api_key = getpass.getpass("Enter your OpenAI API key: ")
        if not api_key:
            raise ValueError("OpenAI API key is required")

    os.environ["OPENAI_API_KEY"] = api_key
    return api_key