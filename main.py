import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions

def main():
    #load in API key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("api key could not be found")

    client = genai.Client(api_key=api_key)

    #set up parser to recognize prompts and --verbose flags
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #add prompt to list of running messages
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    
    #generate response from gemini
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )

    if(response.usage_metadata is None):
        raise RuntimeError("metadata for this prompt could not be found")

    #print metadata if verbose flag used
    if(args.verbose == True):
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    #print function calls or a response
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})\n")
    else:
        print(f"Response:\n {response.text}")

if __name__ == "__main__":
    main()