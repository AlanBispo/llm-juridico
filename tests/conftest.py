import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.core.database import get_db, Base

# URL do banco de testes
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:root@db:5432/juridico"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)

TestingSessionLocal = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Cria e apaga as tabelas a CADA teste"""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    """Gera uma sessao EXCLUSIVA para o codigo do teste (ex: popular dados falsos antes da chamada HTTP)"""
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client():
    """Cliente HTTP que usa o override do banco de forma segura"""
    
    async def _override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()