# mo-zhi

FastAPI + Loguru + SQLAlchemy(Async) + MySQL on Python 3.12

## Quickstart

1. Create and fill `.env` from `.env.example`.
2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Run dev server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints

- GET `/` basic info
- GET `/health` health check
- GET `/db/check` DB connectivity check (SELECT 1)

## Config

- Environment via `.env` using pydantic-settings
- Logging via Loguru, configured in `app/core/logging.py`
- DB via SQLAlchemy async engine `mysql+asyncmy`

## mysql

```commandline
# 推荐使用这个改进版本
docker run -d \
  --name mysql8 \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=writing_platform \
  -v mysql_data:/var/lib/mysql \
  --restart unless-stopped \
  mysql:8.0
```