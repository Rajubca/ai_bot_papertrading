# # app/db/session.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.config import settings

# engine = create_engine(settings.DB_URL, pool_pre_ping=True)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# MySQL does NOT need check_same_thread
engine = create_engine(
    settings.DB_URL,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

SessionLocal = sessionmaker(bind=engine)