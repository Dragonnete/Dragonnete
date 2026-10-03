from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from uzduotis import Studentas
from typing import Optional

import os
from dotenv import load_dotenv

from pydantic import BaseModel, ConfigDict

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()



@app.get("/")
def zinute():
    return {"zinute": "veikia"}

class StudentasCreate(BaseModel):
    vardas: str
    kursas: int
    vidurkis: float

class StudentasRead(StudentasCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class StudentasUpdate(BaseModel):
    vardas: Optional[str] = None
    kursas: Optional[int] = None
    vidurkis: Optional[float] = None
    
@app.post("/studentai", response_model=StudentasRead)
def studentas_create(studentas: StudentasCreate, db: Session = Depends(get_db)):
    new_create = Studentas(
        vardas = studentas.vardas,
        kursas = studentas.kursas,
        vidurkis = studentas.vidurkis
    )

    db.add(new_create)
    db.commit()
    db.refresh(new_create)

    return new_create

@app.get("/studentai/{studentas_id}", response_model=StudentasRead)
def studentas_read_id(studentas_id: int, db: Session = Depends(get_db)):
    rastas = db.get(Studentas, studentas_id)

    if rastas is None:
        raise HTTPException(status_code=404, detail="Studento ID nerastas duombazėje.")
    return rastas

@app.get("/studentai", response_model=list[StudentasRead])
def visa_lentele(db: Session = Depends(get_db)):

    duomenys = db.query(Studentas).all()
    
    return duomenys

@app.put("/studentai/{studento_id}", response_model=StudentasRead)
def keiciami_duomenys(studento_id: int, duomenys: StudentasUpdate, db: Session = Depends(get_db)):
    rastas = db.get(Studentas, studento_id)

    if rastas is None:
        raise HTTPException(status_code=404, detail="Studento ID nerastas duombazėje.")

    if duomenys.vardas is not None:
        rastas.vardas = duomenys.vardas

    if duomenys.kursas is not None:
        rastas.kursas = duomenys.kursas

    if duomenys.vidurkis is not None:
        rastas.vidurkis = duomenys.vidurkis

    db.commit()
    db.refresh(rastas)

    return rastas

@app.delete("/studentai/{studento_id}")
def trinti_id(studento_id: int, db: Session = Depends(get_db)):
    rastas = db.get(Studentas, studento_id)

    if rastas is None:
        raise HTTPException(status_code=404, detail="Studentas nerastas duombazėje.")
    db.delete(rastas)

    db.commit()

    return {"ištrintas_studentas": studento_id}