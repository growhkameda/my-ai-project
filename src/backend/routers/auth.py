# src/backend/routers/auth.py
# @spec-id: DZM-001, DZM-002, DZM-003, DZM-004
# ユーザー登録API：POST /api/auth/register
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.backend.database import get_db
from src.backend.schemas.user import RegisterRequest, RegisterResponse
from src.backend.services.user_service import register_user

router = APIRouter()


# @spec-id: DZM-004 - ユーザー名・メールアドレス・パスワードを送信し、アカウントを登録する
# バリデーションエラー時はエラーメッセージを表示する（400 + detail）
@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
    responses={
        400: {"description": "バリデーションエラー", "content": {"application/json": {"example": {"detail": "エラーメッセージ"}}}},
        409: {"description": "ユーザー名またはメールアドレス重複"},
        500: {"description": "サーバーエラー"},
    },
)
def register(
    body: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    ユーザー登録（DZM-001〜004）。
    ユーザー名・メールアドレス・パスワードは必須。重複登録は不可。
    """
    try:
        return register_user(db, body)
    except ValueError as e:
        # DZM-004: バリデーションエラー時はエラーメッセージを返す（重複含む）
        msg = str(e)
        if "既に登録されています" in msg:
            raise HTTPException(status_code=409, detail=msg)
        raise HTTPException(status_code=400, detail=msg)
    except Exception:
        raise HTTPException(status_code=500, detail="登録処理中にエラーが発生しました")
