import os
import sys
import argparse

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from config import MAX_AGENT_LOOP
from functions.call_function import available_functions, call_function


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

    for _ in range(MAX_AGENT_LOOP):
        try:
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                tools=available_functions,
            )

            if not response.usage:
                raise RuntimeError("API response appears to be malformed")

            if args.verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")

            message = response.choices[0].message
            messages.append(message)

            if not message.tool_calls:
                print("Final response:")
                print(message.content)
                return

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    if tool_call.type != "function":
                        continue
                    result_message = call_function(tool_call, args.verbose)
                    if not result_message.get("content"):
                        raise RuntimeError(
                            f"Empty function response for {tool_call.function.name}"
                        )
                    if args.verbose:
                        print(f"-> {result_message['content']}")
                    messages.append(result_message)
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_AGENT_LOOP}) reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
