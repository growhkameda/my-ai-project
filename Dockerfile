# ベースイメージ（Python 3.11）
FROM python:3.11-slim

# 作業ディレクトリ設定
WORKDIR /app

# 依存関係のインストール（FastAPI, DB, パスワードハッシュ用）
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY ./src /app/src

# 起動コマンド
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]