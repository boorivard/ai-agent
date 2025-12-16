import os
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("api key could not be found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="Prompt")
args = parser.parse_args()
    
response = client.models.generate_content(
    model='gemini-2.5-flash', contents=args.prompt
)

if(response.usage_metadata is None):
    raise RuntimeError("metadata for this prompt could not be found")

print(f"Prompt: {args.prompt}")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(f"Response:\n {response.text}")

