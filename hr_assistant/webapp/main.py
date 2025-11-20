from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from hr_assistant.demo import initialise

app = FastAPI()
templates = Jinja2Templates(directory="templates")
assistant = initialise()

@app.get("/", response_class=HTMLResponse)
async def get_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process", response_class=HTMLResponse)
async def process_text(request: Request, user_text: str = Form(...)):
    # Your server-side logic
    reply = assistant.ask(user_text)
    return templates.TemplateResponse("response.html", {"request": request, "reply": reply})