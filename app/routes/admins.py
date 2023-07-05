from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admins")

template = Jinja2Templates(directory="templates")


@router.get("/")
async def admin_page(req: Request):
    return template.TemplateResponse('admin.html', {
        'request': req
    })
