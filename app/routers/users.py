from fastapi import APIRouter, Depends
from app.deps.auth import require_token
from app.errors import AppError
from app.schemas.user import UserOut
from app.responses import success_response

router = APIRouter()

# In-memory data store
_fake_db: list[dict] = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin", "created_at": "2024-01-01T00:00:00"},
    {"id": 2, "name": "Bob",   "email": "bob@example.com",   "role": "user",  "created_at": "2024-01-02T00:00:00"},
]

@router.get("/users")
def list_users():
    return success_response(
        data=_fake_db,
        meta={
            "page": 1,
            "page_size": 20,
            "total_items": len(_fake_db)
        }
    )

@router.get("/users/me")
def get_current_user(auth=Depends(require_token)):
    return success_response(
        data={
            "user_id": auth["user_id"],
            "token": auth["token"][:10] + "..."
        }
    )

@router.get("/users/{user_id}")
def get_user(user_id: int):
    user = next((u for u in _fake_db if u["id"] == user_id), None)
    if not user:
        raise AppError(
            status_code=404,
            code="USER_NOT_FOUND",
            message=f"User dengan ID {user_id} tidak ditemukan",
            detail=[]
        )
    return success_response(data=user)