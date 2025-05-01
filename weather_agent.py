import json

from dotenv import load_dotenv
from openai import OpenAI
import requests
import os

load_dotenv()
client = OpenAI()

def get_weather(city):
    print(city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return "No weather found"



def run_command(command):
    print(command)
    result  = os.system(command=command)
    return result

available_tools = {
    "get_weather": {
        "fn":get_weather,
        "description":"takes the city name as input and gives the current weather for the city"
    },

    "run_command": {
        "fn":run_command,
        "description":"takes the windows command as input to execute on system and returns output"
    }
}

system_prompt = """
You are an smart and helpful AI agent who is specialized in resolving user query.
You work on  start,analyze,action,observe and output modes.
For the given user query, please perform the modes.
Based on analyze mode select the available tools and based on tool selection you perform the action.
Wait for observation and based on the observation from the tool call resolve user query
You can take user input and convert those into python command and execute by call tools

Rules:
 - 
 - Follow the strict  JSON output as per output schema
 - Always perform  one step at a time
 - Carefully analyse the user query


Output JSON Format:
{{
    "step":"string",
    "content":"string",
    "function":"the name of the function or tool",
    "input":"the input parameter for the function or tool"
}}

Available tools:
 - get_weather : Take city name as input and returns the current weather 
 - run_command : takes the windows command as input to execute on system and returns output


Example:
user query :  What is the weather of Varanasi?
Output: {{"step":"start", "content":"User is asking about the weather of Varanasi"}}
Output: {{"step":"analyze", "content":"Let me analyze the tools available for for given user query"}}
Output: {{"step":"action", "function":"get_weather","input":"Varanasi"}}
Output: {{"step":"observe", "content":"34 degree cel"}}
Output: {{"step":"output", "content":"The weather of the Varanasi is 34 degree cel"}}

user query :  What is the weather of Varanasi,Mumbai, ?
Output: {{"step":"start", "content":"User is asking about the weather for multiple location Varanasi, Mumbai, bangalore"}}
Output: {{"step":"analyze", "content":"Let me analyze the tools available for for given user query"}}
Output: {{"step":"action", "function":"get_weather","input":"Varanasi"}}
Output: {{"step":"observe", "content":"Varanasi 34 degree cel"}}
Output: {{"step":"action", "function":"get_weather","input":"Mumbai"}}
Output: {{"step":"observe", "content":"Mumbai 34 degree cel"}}
Output: {{"step":"action", "function":"get_weather","input":"bangalore"}}
Output: {{"step":"observe", "content":"bangalore 34 degree cel"}}
Output: {{"step":"output", "content":"The weather of the Varanasi is 34 degree cel , weather of the bangalore is 34 degree cel,weather of the Mumbai is 34 degree cel"}}
"""

message = [ {"role":"system","content":system_prompt}]

while True:
    user_query = input(">")
    message.append(
        {"role":"user","content":user_query},
    )
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=message
        )
        res = json.loads(response.choices[0].message.content)
        message.append({"role": "assistant", "content": json.dumps(res)})

        if(res.get("step")=="output"):
            print("🧠▶️",res.get("content"))
            break
        elif(res.get("step")=="action"):
            tool_name = res.get("function")
            tool_input = res.get("input")
            if available_tools.get(tool_name,False)!=False:
                output = available_tools[tool_name].get("fn")(tool_input)
                message.append({"role":"assistant","content":json.dumps({"step":"observe", "content":output})})
                continue
        else:
            print("🤖🤖", res.get("content"))
