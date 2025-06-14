import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )

    if verbose:
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)

    if response.function_calls:
        function_call_result = call_function(response.function_calls[0])
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
        print(f"-> {function_call_result.parts[0].function_response.response}")  # type: ignore
    else:
        print("Response:", response.text)


if __name__ == "__main__":
    main()
