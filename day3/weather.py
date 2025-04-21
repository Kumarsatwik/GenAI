import json
import requests
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI


DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def query_db(sql):
    pass

def run_command(command):
    result = os.system(command=command)
    return result

def get_weather(city: str):
    print("🔨 Tool Called: get_weather", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

def add(x, y):
    print("🔨 Tool Called: add", x, y)
    return x + y

avaiable_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }
}

system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "start | plan | action | observe | output",
        "content": "Description of reasoning or result",
        "function": "Function name (only required if step is 'action')",
        "input": "Input parameters for the function (only if step is 'action')"
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns ouput
    
    Example:
    User Query: Create a React and node.js app with authentication functionality
    Output: {{ "step": "plan", "content": "The User wants to create React.js app as frontend and node.js app as a backend and integrate authentication and authorization functionality" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
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
            print('response.result', parsed_output)
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