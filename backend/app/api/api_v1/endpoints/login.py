from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, crud, models
from app.api import dependencies
from app.database.database import get_session
from app.core.config import settings
from app.core import security

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
        session: AsyncSession = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect mail or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.UserCreateResponse)
def test_token(current_user: models.User = Depends(dependencies.get_current_user)):
    """
    Test access token
    """
    return current_user
