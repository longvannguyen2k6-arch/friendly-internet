"""Central configuration. Values come from environment variables, or from a
local `.env` file next to this module (see `.env.example`), so secrets such as
the DB password and Flask secret key stay out of the source code.
"""
import os
from pathlib import Path


def _load_env_file(path):
    """Minimal .env reader (KEY=VALUE lines); real env vars take precedence."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file(Path(__file__).resolve().parent / ".env")

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "webprogramming")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "longdepzaii").lower()
DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

# E-mail (used to send password-reset codes). Leave SMTP_HOST empty in
# development: the code is then printed in the server console instead.
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "") or SMTP_USER
SMTP_SSL = os.getenv("SMTP_SSL", "0") == "1"   # implicit TLS (port 465)
SMTP_TLS = os.getenv("SMTP_TLS", "1") == "1"   # STARTTLS (port 587)

RESET_CODE_MINUTES = 15
RESET_MAX_ATTEMPTS = 5
RESET_RESEND_SECONDS = 60
