from fastapi import Request
from fastapi.responses import RedirectResponse


def admin_required(request: Request):

    if not request.session.get("admin"):

        return RedirectResponse(
            "/admin/login",
            status_code=303
        )

    return True