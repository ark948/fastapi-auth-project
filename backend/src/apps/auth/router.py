# local imports
from src.apps.auth.models import User
from src.apps.auth.tokens import Token, create_access_token, decode_reset_password_token, create_reset_password_token
from src.apps.auth.oauth2 import authenticate_user, get_current_user
from src.apps.auth.sqlmodels import UpdateUserSQLModel
from src.apps.auth import crud
from src.apps.auth.hash import hash_plain_password
from src.db import SessionDep
from src.apps.auth.schemas import (
    ShowUser, CreateUser, VerifyUser, ForgetPasswordRequest, SuccessMessage, SetNewPassword
)
from src.apps.auth.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# fastapi imports
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import (
    APIRouter, status, HTTPException, Depends
)

# other imports
from pydantic import EmailStr
from typing import Annotated, List
from datetime import timedelta


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.get('/test-route')
def test_route(session: SessionDep, current_user: User = Depends(get_current_user)):
    return {'message': f"Testing auth app... Current User ID: {current_user.id}"}


@router.post('/test-route')
def test_route_post(message: str, session: SessionDep, current_user: User = Depends(get_current_user)):
    return {"input": message, "message": "Your message has been received"}


@router.get('/get-all-users', response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def get_all_users(session: SessionDep):
    return crud.get_all(session)


@router.post('/create', response_model=CreateUser, status_code=status.HTTP_201_CREATED)
def create_user(request: CreateUser, session: SessionDep) -> User:
    return crud.create(request, session)


@router.get('/{id}', response_model=ShowUser, status_code=status.HTTP_200_OK)
def get_user_route(id: int, session: SessionDep) -> User:
    return crud.show(id, session)


# use patch for user edit profile (put for auth or admins)
# for this, we will use specifically use sqlmodel schema (not pydantic)
@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, request: UpdateUserSQLModel, session: SessionDep) -> dict:
    return crud.update(id, request, session)


@router.delete('/{id}')
def delete_user(id: int, session: SessionDep) -> dict:
    return crud.delete(id, session)


@router.post('/verify-user/{id}', status_code=status.HTTP_200_OK)
def verify_user_account(id: int, request: VerifyUser, session: SessionDep) -> dict:
    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with {id} was not found."
        )
    if db_user.is_active == False and db_user.vcode == request.vcode:
        db_user.is_active = True
        db_user.vcode = ""
        session.add(db_user)
        session.commit()
        session.refresh(db_user)   
        return {'message': f'Verification Successful, for {db_user.email}.'}
    elif db_user.is_active == True:
        return {"message": "User already verified."}
    else:
        return {"message": "Code is invalid."}
    

@router.post('/forgot-password')
def send_password_request(request: ForgetPasswordRequest, session: SessionDep):
    user = crud.get_user_from_email(email=request.email, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email was not found.",)
    secret_token = create_reset_password_token(email=user.email)
    forget_url_link = f"http://127.0.0.1:8000/auth/forgot-password/{secret_token}"
    email_body = { "company_name": "my stuff",
                       "link_expiry_min": 10,
                       "reset_link": forget_url_link }
    # could not find anyting similar to console email backend
    # gonna have to just print the link
    print(f"\n\n{secret_token}\n\n")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Email has been sent"})


@router.post("/reset-password", response_model=SuccessMessage)
async def reset_password(request: SetNewPassword, db: SessionDep):
    try:
        info = decode_reset_password_token(token=request.secret_token)
        if info is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid Password Reset Payload or Reset Link Expired")
        if request.new_password != request.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="New password and confirm password are not same.")

        hashed_password = hash_plain_password(request.new_password)
        user = crud.get_user_from_email(email=info, session=db)
        user.password = hashed_password
        db.add(user)
        db.commit()
        return {'success': True, 'status_code': status.HTTP_200_OK, 'message': 'Password Rest Successfull!'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Some thing unexpected happened!")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    session: SessionDep
    ) -> Token:
    user = authenticate_user(email=form_data.username, password=form_data.password, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    token = Token(access_token=access_token, token_type="bearer")
    return token