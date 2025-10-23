from pathlib import Path
import os
from dotenv import load_dotenv  # .envから環境変数を読み込む

# プロジェクトのルートパスを取得
BASE_DIR = Path(__file__).resolve().parent.parent

# .envファイルを読み込む
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 環境変数から機密情報を取得（GitHubに直書きしない）
SECRET_KEY = os.getenv("SECRET_KEY")  # セキュリティキー
DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # デバッグモード
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")  # ホスト設定

# アプリケーション設定
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "calendar_app_main",  # 作成したメインアプリ
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "calendar_app.urls"

# テンプレート設定
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # templates/ はアプリ内を自動探索
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "calendar_app.wsgi.application"

# MySQL データベース設定
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # MySQLを使用
        "NAME": os.getenv("DB_NAME"),          # DB名
        "USER": os.getenv("DB_USER"),          # ユーザー名
        "PASSWORD": os.getenv("DB_PASSWORD"),  # パスワード
        "HOST": os.getenv("DB_HOST", "localhost"),  # ホスト名
        "PORT": os.getenv("DB_PORT", "3306"),       # ポート番号（MySQLは3306）
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# 言語・タイムゾーン設定
LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

# 静的ファイル設定
STATIC_URL = "static/"

# デフォルト主キーの型
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
