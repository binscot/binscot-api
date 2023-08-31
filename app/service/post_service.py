from app.crud import post_crud
from app.dto.response_dto import BaseResponseDTO, PostResponseDTO, BaseResponseListDTO


def read_post(db, post_id):
    response_data = PostResponseDTO(**post_crud.get_post(db, post_id=post_id).__dict__)
    if response_data is None:
        return BaseResponseDTO(
            status_code=400,
            data=None,
            detail='Post not found'
        )
    return BaseResponseDTO(
        status_code=200,
        data=response_data.__dict__,
        detail='success'
    )


def create_post(db, post, current_user):
    try:
        response_data = PostResponseDTO(**post_crud.create_post(db, post, current_user).__dict__)
        return BaseResponseDTO(
            status_code=200,
            data=response_data.__dict__,
            detail='success'
        )
    except Exception as e:
        return BaseResponseDTO(
            status_code=500,
            data=None,
            detail=str(e)
        )


def get_post_list(db):
    try:
        post_list = post_crud.get_posts(db)
        response_data = [
            PostResponseDTO(
                id=post.id,
                title=post.title,
                content=post.content,
                image=post.image,
                owner_id=post.owner_id,
                owner_name=post.owner_name
            )
            for post in post_list
        ]
    except Exception as e:
        return BaseResponseDTO(
            status_code=500,
            data=None,
            detail=str(e)
        )
    return BaseResponseListDTO(
        status_code=200,
        data=response_data,
        detail="Post list fetched successfully."
    )
