from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import (
    APIRouter, Request,
)


router = APIRouter(
    tags=['Pages']
)


templates = Jinja2Templates(directory='templates')
TemplateResponse = templates.TemplateResponse


@router.get('/', response_class=HTMLResponse)
def index(request: Request):
    return TemplateResponse(
        request=request, name='pages/index.html', context={'message': "Hello"}
    )