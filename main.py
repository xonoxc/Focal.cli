import os
import sys
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


def main():
    content_message = sys.argv[1]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=content_message
    )
    print("response:", response.text)
    print("tokens_used:", response.usage_metadata.prompt_token_count)
    print("candidate_token_count:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
