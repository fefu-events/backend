from fastapi import Request, Depends, HTTPException

from fastapi_azure_auth.user import User as UserAzure

from backend.models.user import User
from backend.routers.authentication import azure_scheme
from backend.resources import strings


# def get_user_info_from_schema(user: UserAzure):
#     user_process = {
#         "email": user.claims["preferred_username"],
#         "name": user.claims["name"]
#     }
#     return UserBase(**user_process)
#
#
# def get_user_azure(user_azure: UserAzure = Depends(azure_scheme)):
#     return get_user_info_from_schema(user_azure)
#
#
# def user_exist(
#     request: Request,
#     user_azure: UserAzure = Depends(get_user_azure),
# ):
#     with Session(engine) as session:
#         user: User | None = session.exec(
#             select(User).where(User.email == user_azure.email)
#         ).first()
#         if not user:
#             raise HTTPException(
#                 status_code=400,
#                 detail=strings.USER_DOES_NOT_EXIST_ERROR
#             )
#         request.state.current_user = user
