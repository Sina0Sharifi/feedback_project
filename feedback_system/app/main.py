from fastapi import FastAPI, Request , Form
from fastapi.responses import RedirectResponse
from auth import admin_required
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, Base ,SessionLocal
import models
from models import Feedback
from starlette.middleware.sessions import SessionMiddleware
import random
from typing import Optional
from sqlalchemy import func
from fastapi.responses import Response
Base.metadata.create_all(bind=engine)

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
    request: Request,
    email: str = Form(...),
    title: str = Form(...),
    body: str = Form(...)
):
    if not request.session.get("verified"):

        return {
            "success": False,
            "message": "verification required"
        }
    db = SessionLocal()

    feedback = Feedback(
        email=email,
        title=title,
        body=body
    )

    db.add(feedback)

    db.commit()
    request.session["verified"] = False

    db.refresh(feedback)

    db.close()
    
    return RedirectResponse(
        url="/?success=1",
        status_code=303
    )

    
@app.get("/generate-code")
def generate_code(request: Request):

    request.session["verified"] = False

    code = random.randint(1000, 9999)

    request.session["verification_code"] = str(code)

    return {
        "generated_code": code,
        "saved_in_session": request.session["verification_code"]
    }

@app.post("/verify-code")
def verify_code(
    request: Request,
    code: str = Form(...)
):
    saved_code = request.session.get("verification_code")

    if saved_code == code:
        request.session["verified"] = True

        requested_email = request.session.get("requested_email")
        if requested_email:
            request.session["allowed_email"] = requested_email
            request.session.pop("requested_email", None)

        request.session.pop("verification_code", None)

        return {"success": True}

    return {"success": False}

    
    
@app.get("/feedbacks/{email}")
def user_feedbacks(
    request: Request,
    email: str
):

    if not request.session.get("verified"):
        return RedirectResponse(
            "/",
            status_code=303
        )

    allowed_email = request.session.get(
        "allowed_email"
    )

    if allowed_email != email:
        return RedirectResponse(
            "/",
            status_code=303
        )

    db = SessionLocal()

    feedbacks = db.query(
        Feedback
    ).filter(
        Feedback.email == email
    ).all()

    db.close()

    response = templates.TemplateResponse(
        request=request,
        name="user_feedbacks.html",
        context={
            "feedbacks": feedbacks,
            "email": email
        }
    )

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0"
    )

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response


@app.get("/user/logout")
def user_logout(
    request: Request
):

    request.session.clear()

    response = RedirectResponse(
        "/",
        status_code=303
    )

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0"
    )

    return response

@app.get("/admin/login")
def admin_login_page(
    request: Request,
    error: str = None
):
    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={
            "error": error
        }
    )


@app.post("/admin/login")
def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    if (
        username == "admin"
        and
        password == "1234"
    ):

        request.session["admin"] = True

        return RedirectResponse(
            "/admin/feedbacks",
            status_code=303
        )

    return RedirectResponse(
        "/admin/login?error=1",
        status_code=303
    )


@app.get("/admin/feedbacks")
def admin_feedbacks(
    request: Request
):

    check = admin_required(
        request
    )

    if check is not True:
        return check

    db = SessionLocal()

    emails = (
        db.query(
            Feedback.email,
            func.count(
                Feedback.id
            ).label(
                "count"
            )
        )
        .group_by(
            Feedback.email
        )
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="admin_emails.html",
        context={
            "emails": emails
        }
    )


@app.get("/admin/feedbacks/{email}")
def admin_email_feedbacks(
    request: Request,
    email: str
):

    check = admin_required(
        request
    )

    if check is not True:
        return check

    db = SessionLocal()

    feedbacks = (
        db.query(
            Feedback
        )
        .filter(
            Feedback.email == email
        )
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="admin_email_feedbacks.html",
        context={
            "feedbacks": feedbacks,
            "email": email
        }
    )

@app.get("/admin/logout")
def admin_logout(
    request: Request
):

    request.session.clear()

    return RedirectResponse(
        "/admin/login",
        status_code=303
    )
@app.get("/admin/feedback/{feedback_id}")
def admin_feedback_detail(
    request: Request,
    feedback_id: int,
    success: str = None
):

    check = admin_required(
        request
    )

    if check is not True:

        return check

    db = SessionLocal()

    feedback = db.query(
        Feedback
    ).filter(
        Feedback.id == feedback_id
    ).first()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="admin_feedback_detail.html",
        context={
            "feedback": feedback,
            "success": success
        }
    )
@app.post("/admin/feedback/{feedback_id}")
def update_feedback(
    request: Request,
    feedback_id: int,
    status: str = Form(...),
    reply: Optional[str] = Form("")
):

    check = admin_required(
        request
    )

    if check is not True:

        return check

    db = SessionLocal()

    feedback = db.query(
        Feedback
    ).filter(
        Feedback.id == feedback_id
    ).first()

    feedback.status = status
    feedback.reply = reply

    db.commit()

    db.close()

    return RedirectResponse(
        f"/admin/feedback/{feedback_id}?success=1",
        status_code=303
    )

@app.post("/prepare-feedbacks")
def prepare_feedbacks(
    request: Request,
    email: str = Form(...)
):

    request.session[
        "requested_email"
    ] = email

    return {
        "success": True
    }
@app.post("/clear-feedback-target")
def clear_feedback_target(request: Request):
    request.session.pop("requested_email", None)
    request.session.pop("allowed_email", None)
    return {"success": True}