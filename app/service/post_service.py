from fastapi import HTTPException

from app.crud import post_crud


def read_post(db, post_id):
    db_post = post_crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
