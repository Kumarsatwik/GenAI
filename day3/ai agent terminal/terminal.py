import json
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def run_command(command):
    result = os.system(command=command)
    return result

avaiable_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }
}

system_prompt="""
You are an AI developer assistant. You can write code in any programming language . Code Should be readable , modular , maintainable , follow best practices and design patterns.  You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - run_command: Takes a command as input to execute on system and returns ouput
    
   Example:
    User Query: Create a React and node.js app with authentication functionality
    Output: {{
        "step": "start",
        "content": "Received user query: 'Create a React and Node.js app with authentication functionality'. Starting analysis."
        }}

    Output: {{
    "step": "plan",
    "content": "The user wants a full-stack project setup with React.js as the frontend and Node.js as the backend, with authentication functionality."
    }}

    Output: {{
    "step": "plan",
    "content": "I should first create Project folder using 'mkdir project'."
    }}

    Output: {{
    "step": "action",
    "function": "run_command",
    "input": "mkdir project && cd project"
    }}

    Output: {{
    "step": "plan",
    "content": "I should first create a Node.js backend using 'npm init -y' and install required packages."
    }}

    Output: {{
    "step": "action",
    "function": "run_command",
    "input": "cd project && mkdir server && cd server && npm init -y "
    }}

    Output:{{
    "step": "observe",
    "content": "Node.js project initialized in 'server' directory."
    }}
    Output:{{
    "step": "plan",
    "content": "Now I should install authentication libraries: 'express', 'jsonwebtoken', and 'bcrypt' for the backend."
    }}
    Output:{{
    "step": "action",
    "function": "run_command",
    "input": "cd project && cd server && npm install express jsonwebtoken bcrypt "
    }}

    Output:{{
    "step": "plan",
    "content": "Now I should create a user registration endpoint for the backend."
    }}

    Output:{{
    "step": "action",
    "function": "run_command",
    "input": "cd project && cd server && node server.js"
    }}

    Output:{{
    "step": "observe",
    "content": "Authentication packages installed successfully in backend."
    }}

    Output: {{
    "step": "plan",
    "content": "I should first create a React app using 'npm create vite@latest client' and install required packages."
    }}

    Output: {{
        "step": "action",
        "function": "run_command",
        "input": "cd project && npm create vite@latest client && cd client && npm install"
    }}

    Output:{{
    "step": "plan",
    "content": "Now I should create Login Page and Register Page."
    }}

    Output: {{
        "step": "action",
        "function": "run_command",
        "input": "cd project && cd client && mkdir auth && cd auth && touch Login.jsx Register.jsx"
    }}

     Output:{{
    "step": "plan",
    "content": "Now I should add Login and Register Page in App.js and Integrate authentication functionality with backend."
    }}


    Output: {{ "step": "output",
  "content": "Full-stack React and Node.js app initialized with authentication dependencies. Ready for further development like adding routes or login forms."}}

"""


messages = [
    { "role": "system", "content": system_prompt }
]
def call_deepseek_api(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )
    return json.loads(response.choices[0].message.content)

while True:
    user_query = input('> ')
    messages.append({ "role": "user", "content": user_query })

    while True:
        try:
            response_text = call_deepseek_api(messages)
            parsed_output = response_text
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {response_text}")
            break
        except Exception as e:
            print(f"API Error: {str(e)}")
            break

        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get('content')}")
            continue

        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if avaiable_tools.get(tool_name):
                output = avaiable_tools[tool_name]["fn"](tool_input)
                messages.append({
                    "role": "assistant",
                    "content": json.dumps({ "step": "observe", "output": output })
                })
                continue

        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get('content')}")
            break