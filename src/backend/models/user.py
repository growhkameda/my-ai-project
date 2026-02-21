# src/backend/models/user.py
# @spec-id: DZM-001, DZM-002, DZM-003, DZM-004
# ユーザー登録：ユーザー名・メールアドレス・パスワードを保持。パスワードはハッシュ化（DZM-021）
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from src.backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # @spec-id: DZM-001
    username = Column(String(255), unique=True, nullable=False, index=True)
    # @spec-id: DZM-002
    email = Column(String(255), unique=True, nullable=False, index=True)
    # @spec-id: DZM-003, DZM-021（平文保存禁止のためハッシュのみ保存）
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
