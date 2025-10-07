import os
import sys
import json
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from utils.tools import available_functions
from system.prompt import SYSTEM_PROMPT
from utils.caller import call_function
from utils.ui import (
    print_user_message,
    print_model_response,
    print_function_call,
    print_tool_response,
    print_error,
    print_info,
)


from google.genai.errors import ClientError, ServerError, APIError

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


def make_function_message(call_res: types.Content) -> types.Content | None:
    """Extract a function response and wrap it into a user message."""
    parts = call_res.parts or []
    if parts and parts[0].function_response and parts[0].function_response.response:
        return types.Content(
            role="user",
            parts=[types.Part(text=json.dumps(parts[0].function_response.response))],
        )
    return None


def main() -> None:
    if len(sys.argv) < 2:
        print_error(
            'a message is required for the agent to work (e.g. uv run "your message")'
        )
        sys.exit(1)

    content_message = sys.argv[1]
    messages: List[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=content_message)])
    ]

    is_verbose_mode = "--verbose" in sys.argv

    print_user_message(content_message)

    iteration = 0
    while iteration < 20:
        iteration += 1

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT, tools=[available_functions]
                ),
            )

        except (ServerError, APIError) as e:
            if e.code == 429:
                print_error(e.message)
            else:
                print_error(f"Server Error: {e.message}")
            sys.exit(1)

        if not response.candidates and not response.function_calls:
            print_info("Agent is done !")
            break

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

                    if candidate.content.parts:
                        for part in candidate.content.parts:
                            if part.text:
                                print_model_response(part.text)

        if response.function_calls:
            for call in response.function_calls:
                print_function_call(call.name, call.args)
                func_resp = call_function(call, verbose=is_verbose_mode)

                if resp := make_function_message(func_resp):
                    print_tool_response(resp.parts[0].text)
                    messages.append(resp)
                else:
                    print_error(f"Warning: {call.name} returned invalid response")
            continue

    if is_verbose_mode:
        meta = response.usage_metadata
        if meta:
            print_info(
                f"user_prompt: {content_message}\n"
                f"tokens_used: {meta.prompt_token_count}\n"
                f"candidate_token_count: {meta.candidates_token_count}\n"
            )
        else:
            print_info("No usage metadata found!")


if __name__ == "__main__":
    main()
