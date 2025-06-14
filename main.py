import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_CALLS
from function_schema import available_functions
from functions.call_function import call_function
from prompts import SYSTEM_PROMPT


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("Please provide your prompt as an additional argument")
        print('\nUsage: python main.py "your prompt here" [--verbose] ')
        sys.exit(1)

    input_prompt = " ".join(args)
    if verbose:
        print("User prompt: ", input_prompt)

    messages = [types.Content(role="user", parts=[types.Part(text=input_prompt)])]

    for i in range(MAX_CALLS):
        response = generate_content(client, messages, verbose)

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)  # type: ignore

        try:
            if response.function_calls:
                function_call_result = call_function(response.function_calls[0])
                messages.append(function_call_result)
                if i < MAX_CALLS - 1:
                    continue
        except Exception as e:
            print(f"Error generating content: {e}")

        print("Final Response:", response.text)
        break


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )

    if verbose:
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)

    return response


if __name__ == "__main__":
    main()
