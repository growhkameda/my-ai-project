# src/backend/schemas/user.py
# @spec-id: DZM-001, DZM-002, DZM-003, DZM-004
# ユーザー登録リクエスト・レスポンスおよびバリデーションエラー用スキーマ
import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# RFC 5322 簡易メール形式チェック用（厳密には email-validator 推奨）
EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


# @spec-id: DZM-001
class RegisterRequest(BaseModel):
    """ユーザー名・メールアドレス・パスワードを送信しアカウントを登録する（DZM-004）"""

    username: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1)

    # @spec-id: DZM-001 - 必須・バリデーション
    @field_validator("username")
    @classmethod
    def username_required_and_valid(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("ユーザー名は必須です")
        return v.strip()

    # @spec-id: DZM-002 - 必須・形式チェック（RFC準拠等）
    @field_validator("email")
    @classmethod
    def email_required_and_format(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("メールアドレスは必須です")
        v = v.strip()
        if not EMAIL_PATTERN.match(v):
            raise ValueError("有効なメールアドレス形式で入力してください")
        return v

    # @spec-id: DZM-003 - 必須・バリデーション
    @field_validator("password")
    @classmethod
    def password_required(cls, v: str) -> str:
        if not v:
            raise ValueError("パスワードは必須です")
        return v


# @spec-id: DZM-004 - 登録成功時レスポンス
class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str


# @spec-id: DZM-004 - バリデーションエラー時はエラーメッセージを表示
class ValidationErrorResponse(BaseModel):
    detail: str
    errors: Optional[list[dict]] = None
