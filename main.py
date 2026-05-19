import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    client = genai.Client(api_key=api_key)

    # Using argparse to create an object that receive any user text (str type)
    # we telling the argument parser to expect a single positional argument
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")        # Name the argument as user_prompt - type string
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    # Using types from google.genai - to create a list of user_prompt -- this list is expand in the future (long conversation)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    content_generated(client, messages, args.verbose)

def content_generated(client, messages, verbose):

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
    )

    # This is to guard whenever the Object-usage_metadata from Gemini is empty or None type
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response: ")
    print(response.text)


if __name__ == "__main__":
    main()
