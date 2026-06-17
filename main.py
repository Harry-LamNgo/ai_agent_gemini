import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERS


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    client = genai.Client(api_key=api_key)

    # Using argparse to create an object that receive any user text (str type)
    # we telling the argument parser to expect a single positional argument
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to AI model")        # Name the argument as user_prompt - type string
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()
    
    # Using types from google.genai - to create a list of user_prompt -- this list is expand in the future (long conversation)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    
    # Create a loop (loops for Agent to find the result - depend on how many tokens you have with AI account - in this case I used 20 loops only)
    for _ in range(MAX_ITERS):
        # Call the model, handle the response
        final_result = content_generated(client, messages, args.verbose)
        if final_result:
            print("Final Response: ")
            print(final_result.text)
            return
    print(f"The AI agent has reached the maximum iterartion ({MAX_ITERS}) - Cannot find the final Answer")
    sys.exit(1)
        



def content_generated(client: genai.Client, messages: list[types.Content], verbose: bool) -> str | None:

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    # This is to guard whenever the Object-usage_metadata from Gemini is empty or None type
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Check if the response from AI has .candidates property
    # - if yes, iterate through candidates and append the candidate.content to message for Agent to keep track the conversation
    if response.candidates:
        for response_candidate in response.candidates:
            if response_candidate.content:
                messages.append(response_candidate.content)

    # Check if function_calls of response is None
    # - if there is no function_calls - then return
    if not response.function_calls:
        return response

    function_responses: list[types.Part] = []
    if response.function_calls:
        for function_call in response.function_calls:
            # call_function - AI run the function need to run
            result = call_function(function_call, verbose)

            # If any information in .parts of the result object is empty or None -> Raise Error because no information to response
            if (not result.parts 
                or not result.parts[0].function_response 
                or not result.parts[0].function_response.response):
                raise RuntimeError(f"Empty function response for {function_call.name}")

            if verbose:
                print(f"-> {result.parts[0].function_response.response}")

            function_responses.append(result.parts[0])
        
        # Each time function_call runs, add the content of answer to message for Agent to keep track
        messages.append(types.Content(role="user", parts=function_responses))
    

if __name__ == "__main__":
    main()
