# src/adbs/database/db_session.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.niver65 import settings

# Configuração do banco de dados
DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print(f'Url DB: {DATABASE_URL}')

def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()



## Modo Assincrono

# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from src.adbs import settings
#
# # Configuração do banco de dados para assíncrono
# DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
#
# engine = create_async_engine(DATABASE_URL, echo=True)
#
# # Note o uso de class_=AsyncSession para suportar sessões assíncronas
# AsyncSessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
# )
#
# async def get_db_session():
#     async with AsyncSessionLocal() as session:
#         yield session
