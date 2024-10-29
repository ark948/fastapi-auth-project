from fastapi import (
    APIRouter, 
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()


templates = Jinja2Templates(directory='templates')


@router.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name='pages/index.html', context={'message': "HELLO"}
    )



# test this route to check if pytest works
@router.get('/test')
def test_route(request: Request):
    return 'hello world'