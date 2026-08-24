import os
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OpenRouter API key not found")

    parser = argparse.ArgumentParser(description="ChatBot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    user_prompt = args.user_prompt
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": user_prompt,
        },
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )
    message = response.choices[0].message

    if not response.usage:
        raise RuntimeError("Request has failed")

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
