# to run this use
# uvicorn hr_assistant.webapp.main:app --reload
# from the root folder
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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
    reply = assistant.ask(user_text)
    return templates.TemplateResponse(
        "response.html", {"request": request, "reply": reply}
    )
