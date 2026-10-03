# Justo būdu
# DBeaver atlikta.


# Miko būdu
from sqlalchemy import Integer, String, Float, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Studentas(Base):
    __tablename__ = "studentas"

    id = Column(Integer, primary_key=True)
    vardas = Column(String, nullable=False)
    kursas = Column(Integer)
    vidurkis = Column(Float)


