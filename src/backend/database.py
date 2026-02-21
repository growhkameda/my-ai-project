# src/backend/database.py
# DB接続（ユーザー登録 DZM-001〜004 で利用）
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = os.getenv("DB_URL", "postgresql://user:password@localhost:5432/mydb")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """テーブル作成（起動時呼び出し用）。呼び出し元で models を import した後に実行すること。"""
    Base.metadata.create_all(bind=engine)
