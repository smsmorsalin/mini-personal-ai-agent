import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools import calculator, get_datetime, read_notes


# Load environment variables
load_dotenv()

# Connect to OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# -------------------------------
# Define Available Tools
# -------------------------------

TOOLS = [

    {
        "type": "function",
        "name": "calculator",
        "description": "Calculate mathematical expressions.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression."
                }
            },
            "required": ["expression"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_datetime",
        "description": "Get the current date and time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "read_notes",
        "description": "Read the contents of notes.txt.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    }

]


# -------------------------------
# Tool Execution Function
# -------------------------------

def execute_tool(name, arguments):

    if name == "calculator":
        return calculator(arguments["expression"])

    elif name == "get_datetime":
        return get_datetime()

    elif name == "read_notes":
        return read_notes()

    else:
        return "Unknown tool."


# -------------------------------
# AI Agent Function
# -------------------------------

def run_agent(user_input, previous_response_id=None):

    instructions = """
    You are a helpful personal AI assistant.

    You can use these tools:
    1. Calculator
    2. Date and Time
    3. Read Notes

    Use tools whenever they are needed.

    Never invent calculator results.
    Explain your answers clearly.
    """

    response = client.responses.create(
        model="gpt-6-astra",
        instructions=instructions,
        input=user_input,
        tools=TOOLS,
        previous_response_id=previous_response_id
    )

    # Agent execution loop
    while True:

        function_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        # If there are no more tool calls,
        # return the final AI response.
        if not function_calls:
            return response.output_text, response.id

        tool_outputs = []

        # Execute requested tools
        for call in function_calls:

            print(f"\n[Agent] Using tool: {call.name}")

            arguments = json.loads(call.arguments)

            result = execute_tool(
                call.name,
                arguments
            )

            print(f"[Tool Result] {result}")

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": str(result)
            })

        # Send tool results back to the AI
        response = client.responses.create(
            model="gpt-6-astra",
            instructions=instructions,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS
        )


# -------------------------------
# Main Application
# -------------------------------

def main():

    print("=" * 45)
    print("       MINI PERSONAL AI AGENT")
    print("=" * 45)

    print("Agent is ready!")
    print("Type 'exit' to stop.\n")

    previous_response_id = None

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Agent: Goodbye!")
            break

        if not user_input:
            continue

        try:

            answer, previous_response_id = run_agent(
                user_input,
                previous_response_id
            )

            print("\nAgent:", answer, "\n")

        except Exception as error:

            print("\nError:", error, "\n")


if __name__ == "__main__":
    main()