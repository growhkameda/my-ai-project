# src/backend/services/user_service.py
# @spec-id: DZM-001, DZM-002, DZM-003, DZM-004
# ユーザー登録のビジネスロジック：重複チェック・パスワードハッシュ化
from sqlalchemy.orm import Session

from src.backend.models.user import User
from src.backend.schemas.user import RegisterRequest, RegisterResponse


def hash_password(password: str) -> str:
    # @spec-id: DZM-021 パスワードのハッシュ化
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    except Exception:
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()


# @spec-id: DZM-001 - 重複したユーザー名の登録を防止する
def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username.strip()).first()


# @spec-id: DZM-002 - 重複したメールアドレスの登録を防止する
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.strip().lower()).first()


# @spec-id: DZM-004 - ユーザー名・メールアドレス・パスワードを送信し、アカウントを登録する
def register_user(db: Session, body: RegisterRequest) -> RegisterResponse:
    # DZM-001: 重複したユーザー名の登録を防止
    if get_user_by_username(db, body.username):
        raise ValueError("このユーザー名は既に登録されています")

    # DZM-002: 重複したメールアドレスの登録を防止
    if get_user_by_email(db, body.email):
        raise ValueError("このメールアドレスは既に登録されています")

    user = User(
        username=body.username.strip(),
        email=body.email.strip().lower(),
        password_hash=hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return RegisterResponse(id=user.id, username=user.username, email=user.email)
