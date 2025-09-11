import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


# user messages [the context]


def main() -> None:
    if len(sys.argv) < 2:
        print(
            'Error:a message is required for the agent to work (e.g. uv run "your message")',
            file=sys.stderr,
        )
        sys.exit(1)

    content_message = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=content_message)])]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )
    print("response:", response.text)
    print("tokens_used:", response.usage_metadata.prompt_token_count)
    print("candidate_token_count:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
