from app.crud import user_crud
from app.dto.response_dto import BaseResponseDTO, UserResDTO


def get_user_me(current_user):
    response_data = UserResDTO(
        id=current_user.id,
        username=current_user.username,
        disabled=current_user.disabled,
        posts=current_user.posts
    )
    return BaseResponseDTO(
        status_code=200,
        data=response_data,
        detail='success'
    )


def get_user_list(db):
    user_list = user_crud.get_users(db)
    response_data = [
        UserResDTO(
            id=user.id,
            username=user.username,
            disabled=user.disabled,
            posts=user.posts
        ) for user in user_list
    ]

    return BaseResponseDTO(
        status_code=200,
        data=response_data,
        detail='success'
    )
