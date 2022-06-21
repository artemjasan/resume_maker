# from sqlalchemy import select, delete, insert
# from sqlalchemy.orm.exc import NoResultFound
# from passlib.context import CryptContext
#
# from fastapi import HTTPException, status
# from app.database.database import AsyncSession
# from app.models.user import User
# from app.schemas.user import UserCreate, UserDB
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# async def get_user_by_email(session: AsyncSession, email: str):
#     query = select(User).where(User.email == email)
#     return await session.execute(query)
#
#
# async def get_users(session: AsyncSession) -> list[UserDB]:
#     users = await session.execute(select(User).order_by(User.id))
#     return users.scalars().all()
#
#
# async def create_user(session: AsyncSession, user: UserCreate):
#     new_user = User(
#         username=user.username,
#         email=user.email,
#         hashed_password=pwd_context.encrypt(user.password)
#     )
#     session.add(new_user)
#     return new_user
#     # query = insert(User).values(
#     #     username=user.username,
#     #     email=user.email,
#     #     hashed_password=pwd_context.encrypt(user.password)
#     # )
#     # last_record_id = await session.execute(query)
#     # return last_record_id
#
#
# async def delete_user(session: AsyncSession, current_user: UserDB, user_id: int):
#     try:
#         query = select(User).where(User.id == user_id)
#         db_user = await session.execute(query)
#     except NoResultFound:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
#
#     if db_user.id == current_user.id:
#         query = delete(User).where(User.id == user_id).execution_options(synchronize_session="fetch")
#         deleted_user_id = await session.execute(query)
#         if not deleted_user_id:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete")
