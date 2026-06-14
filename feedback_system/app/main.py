from fastapi import FastAPI, Request , Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, Base ,SessionLocal
import models
from models import Feedback
from starlette.middleware.sessions import SessionMiddleware
import random

Base.metadata.create_all(bind=engine)
from fastapi.responses import RedirectResponse
app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key="my-super-secret-key"
)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(
    request: Request,
    success: str = None
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "success": success
        }
    )

@app.post("/feedback/create")
def create_feedback(
    email: str = Form(...),
    title: str = Form(...),
    body: str = Form(...)
):
    db = SessionLocal()

    feedback = Feedback(
        email=email,
        title=title,
        body=body
    )

    db.add(feedback)

    db.commit()

    db.refresh(feedback)

    db.close()

    return RedirectResponse(
        url="/?success=1",
        status_code=303
    )
@app.get("/generate-code")
def generate_code(request: Request):

    code = random.randint(1000, 9999)

    request.session["verification_code"] = str(code)

    return {
        "generated_code": code,
        "saved_in_session": request.session["verification_code"]
    }