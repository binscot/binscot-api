from app.crud import user_crud
from app.dto.response_dto import UserListResDTO
from app.schemas.user_schemas import User


def get_user_me(current_user):
    current_user.status_code = 200
    current_user.detail = 'success'
    return current_user


def get_user_list(db):
    user_list = user_crud.get_users(db)
    response_data = [
        User(
            id=user.id,
            username=user.username,
            disabled=user.disabled,
            posts=user.posts
        ) for user in user_list
    ]

    return UserListResDTO(
        status_code=200,
        user_list=response_data,
        detail='success'
    )
