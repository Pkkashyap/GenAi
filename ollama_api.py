from fastapi import FastAPI,Body
from ollama import Client

app = FastAPI()

client  = Client(
    host="http://localhost:11434"
)

client.pull('deepseek-r1:1.5b')

@app.post("/chat")
def chat(message:str = Body(...,description="chat message")):
    response = client.chat(model='deepseek-r1:1.5b',messages=[
        {"role":"user","content":message}
    ] ,options={'temperature': 0},)
    return response['message']['content']