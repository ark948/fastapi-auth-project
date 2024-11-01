from fastapi import (
    APIRouter, 
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=['Pages']
)


templates = Jinja2Templates(directory='src/apps/pages/templates')


@router.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name='index.html', context={'message': "Hello"}
    )