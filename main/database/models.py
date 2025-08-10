from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey

engine = create_async_engine(url='sqlite+aiosqlite:///database.db', echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(25), nullable=True)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class Card(Base):
    __tablename__ = 'cards'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[int]
    image: Mapped[str] = mapped_column(String(256))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)