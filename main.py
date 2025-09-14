import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from utils.tools import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


# user messages [the context]


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


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
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )

    if len(response.function_calls) > 0:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    print("response:", response.text)

    if "--verbose" in sys.argv:
        print("----- info ---------")
        print("user_prompt:", content_message)
        print("tokens_used:", response.usage_metadata.prompt_token_count)
        print("candidate_token_count:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
