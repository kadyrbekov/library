from sqlalchemy import create_engine, Column, Integer, VARCHAR, Sequence
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:admin@localhost:5432/rarity_db")
Base = declarative_base()

class book(Base):
    __tablename__ = 'Book'
    # Sequence('some_id_seq'),
    id_num = Column('id_num', Integer, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    author = Column(VARCHAR(255), nullable=False)
    image = Column(VARCHAR(255))


Base.metadata.create_all(engine)




