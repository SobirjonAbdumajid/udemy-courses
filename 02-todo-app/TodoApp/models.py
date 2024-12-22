from database import Base
from sqlalchemy import Column, String, Integer, Boolean

class Todos(Base):
    __tablename__ = 'todos'  # Bu jadvalning nomini belgilaydi. Ma'lumotlar bazasida ushbu sinf todos nomli jadval sifatida saqlanadi.

    id = Column(Integer, primary_key=True, index=True)  # with index searching may work faster
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
