from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant which is expert in solving mathematical problem.
You should not answer any other question with is not related to mathematics

For given query help user to give the solution.

Example:
Input: 2+2
Output: 2 + 2 is 4 which is calculated by adding 2 with 2

Input: 5*10
Output: 5 * 10 is 50 which is calculated by multiplying 5 with 10. FunFact, 10 * 5 will result in same output.

Input : what is life?
Output: Incorrect input, please ask only maths related question.
"""

result = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"system","content":system_prompt},
        {"role":"user","content":"what is table 2"}
    ]
)


print(result.choices[0].message.content)