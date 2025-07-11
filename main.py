from fastapi import FastAPI
from pydantic import BaseModel
from dialog_engine import run_dialog

app = FastAPI()

class UserInput(BaseModel):
    text: str
    session_id: str

@app.post("/chat")
def chat(input: UserInput):
    return {"response": run_dialog(input.text, input.session_id)}
