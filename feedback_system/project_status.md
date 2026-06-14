# Feedback System - Current Project Status

## Project Goal

ساخت یک سیستم مدیریت بازخورد (Feedback System) با FastAPI + SQLAlchemy + SQLite + Jinja2 + Bootstrap 5

---

## Technologies

Backend:

* FastAPI
* SQLAlchemy ORM
* SQLite

Frontend:

* Jinja2 Templates
* Bootstrap 5
* Vanilla JavaScript (later)

Authentication:

* Session Middleware

---

## Current Folder Structure

feedback_system/

app/

database.py

models.py

main.py

templates/

index.html

feedback.db

venv/

---

## Database

SQLite Database:

feedback.db

Table:

feedbacks

Columns:

* id (Integer, Primary Key)
* email (String)
* title (String)
* body (Text)
* status (String)
* reply (Text, Nullable)

Default Status:

"دریافتی"

---

## Completed Features

### 1. Database Layer

Created:

database.py

Contains:

* SQLAlchemy Engine
* SessionLocal
* Base

---

### 2. ORM Layer

Created:

models.py

Contains:

Feedback model

Mapped to:

feedbacks table

---

### 3. FastAPI Setup

Created:

main.py

Contains:

* FastAPI app
* Database initialization
* Jinja2 configuration

---

### 4. Home Page

Route:

GET /

Returns:

templates/index.html

---

### 5. UI

Created:

templates/index.html

Contains:

Section 1:

* Email
* Title
* Body
* Submit Feedback

Section 2:

* Email
* View Feedbacks

Design:

* Bootstrap 5
* Responsive
* White + Orange (#E66C00)

---

### 6. Feedback Creation

Route:

POST /feedback/create

Functionality:

* Receives email
* Receives title
* Receives body
* Saves feedback to SQLite

---

### 7. Success Redirect

Implemented:

PRG Pattern

Flow:

POST
↓
Redirect
↓
GET

After save:

Redirect to:

/?success=1

Shows Bootstrap Success Alert

---

### 8. Session Setup (Started)

Added:

SessionMiddleware

Imports:

from starlette.middleware.sessions import SessionMiddleware

Purpose:

Preparing for verification code system.

---

## Current Stage

Currently implementing:

Server-side 4-digit verification code system.

Goal:

User
↓
Generate Code
↓
Store In Session
↓
Verify Code
↓
Allow Save Feedback

---

## Not Implemented Yet

### Verification System

* /generate-code
* /verify-code
* Modal
* Code input UI

---

### User Feedback Viewer

Page:

user_feedbacks.html

Features:

* Search by email
* View all feedbacks
* View status
* View admin reply

---

### Admin Authentication

Pages:

admin_login.html

Features:

* admin login
* session validation
* logout

---

### Admin Dashboard

Page:

admin_feedbacks.html

Features:

* list all feedbacks
* show title
* show sender email

---

### Feedback Detail Page

Page:

admin_feedback_detail.html

Features:

* view full feedback
* change status
* write reply
* save reply

---

## Important Notes

Developer preference:

* Explain architecture before coding.
* Implement one small step at a time.
* Do not generate large blocks of code unless requested.
* Explain where every file should be created.
* Explain purpose of every new code block.
