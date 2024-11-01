# local imports

# fastapi imports
from fastapi import (
    APIRouter, status, HTTPException
)


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/', status_code=status.HTTP_200_OK)
def index():
    return {"message": "You reached users index page"}