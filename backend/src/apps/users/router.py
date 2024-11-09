# local imports
from src.apps.users.forms import RegistrationForm
from src.apps.users.schemas import RegisterUser

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
def register_html(request: Request):
    form = RegistrationForm()
    print(form)
    return TemplateResponse(request=request, name='users/register.html', context={'request': request,'form': form,})


@router.post('/process-register')
def register_process_html(request: Request):
    return None


@router.get('/register', status_code=status.HTTP_201_CREATED)
def register(request: RegisterUser):
    return