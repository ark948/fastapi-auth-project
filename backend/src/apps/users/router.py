# local imports
from src.apps.users.forms import RegistrationForm

# fastapi imports
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import (
    APIRouter, status, HTTPException, Request
)


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


templates = Jinja2Templates(directory='templates')
TemplateResponse = templates.TemplateResponse


@router.get('/', status_code=status.HTTP_200_OK)
def index():
    return {"message": "You reached users index page"}



@router.get('/register', response_class=HTMLResponse)
def register(request: Request):
    form = RegistrationForm()
    print(form)
    return TemplateResponse(
        request=request, name='users/register.html', context={'request': request,'form': form,}
        )


@router.post('/process-register')
def register_post(request: Request):
    return None


