from dotenv import load_dotenv
from openai import OpenAI
import json
from pyexpat.errors import messages

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant which is expert in breaking down the problem into multiple step for the user query.

For the given user input, analyse the input and break it down to step by step process by which it can be solved.

Follow the steps is sequence that is "analyse" "process" "think" "output" "validation" "result"

Rules:
1: Follow the strict  JSON output as per output schema
2: Always perform  one step at a time    
3: Carefully analyse the user query

Example:
Input : 2 + 2
Output: {{step : "analyse", "content: Ok!, user is giving the mathematical problem for which I need to think or correct output"}}
Output: {{step : "think", content: "To give user the correct output, need to add this mathematical expression from left to right"}}
Output: {{step : "output", content: "2+2 is 4"}}
Output: {{step : "validation", content: "i think 4 is the correct answer after careful observation"}}
Output" {{step : "result", content: "2+2 = 4 it is the most  accurate answer"}}
"""


messages = [
    {"role":"system","content":system_prompt}
]

user_input = input("> ")
messages.append({"role":"user","content":user_input})
while True:
    result = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_res = json.loads(result.choices[0].message.content)
    messages.append({"role":"assistant", "content": json.dumps(parsed_res)})


    if parsed_res.get("step")!="result":
        print(f"🧠 : {parsed_res}")
        continue
    else:
        print(f"🤖 : {parsed_res}")
        break

