import logging
from sqlalchemy import Column, Integer, String, DateTime, func, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.config import Settings

log = logging.getLogger(__name__)
Base = declarative_base()


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(25), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())


class DatabaseManager:
    def __init__(self, config: Settings):

        self.engine = create_async_engine(config.db_url, future=True, echo=True)
        self.SessionLocal = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def add_application(self, application: Application):

        async with self.SessionLocal() as session:
            session.add(application)
            try:
                await session.commit()
                log.debug(f"Successfully added application: {application}")
            except Exception as e:
                await session.rollback()
                log.error(f"Failed to add application: {e}")
                raise

    async def get_applications(self, user_name: str = None, offset: int = 0, limit: int = 10):
        async with self.SessionLocal() as db:
            query = select(Application)
            if user_name:
                query = query.filter_by(user_name=user_name)
            query = query.offset(offset).limit(limit)
            results = await db.execute(query)
            return results.scalars().all()


db_manager = DatabaseManager(Settings())