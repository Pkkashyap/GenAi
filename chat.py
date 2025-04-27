from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

result = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"user","content":"what is 2+2"}
    ]
)


print(result.choices[0].message.content)