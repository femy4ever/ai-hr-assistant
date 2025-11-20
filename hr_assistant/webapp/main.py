from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from pathlib import Path

from hr_assistant.demo import initialise

load_dotenv()

templates = Path(__file__).parent.joinpath("templates")

app = FastAPI()
templates = Jinja2Templates(directory=str(templates.absolute()))
assistant = initialise()

@app.get("/", response_class=HTMLResponse)
async def get_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process", response_class=HTMLResponse)
async def process_text(request: Request, user_text: str = Form(...)):
    # Your server-side logic
    reply = assistant.ask(user_text)
    return templates.TemplateResponse("response.html", {"request": request, "reply": reply})