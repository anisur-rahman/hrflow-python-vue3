from contextlib import asynccontextmanager
from datetime import date
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import create_engine, ForeignKey, String, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hrflow.db")
kwargs = {"connect_args": {"check_same_thread": False}} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, **kwargs)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    hire_date: Mapped[date]
    status: Mapped[str] = mapped_column(String(20), default="active")
    department: Mapped[Department] = relationship()


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class DepartmentOut(DepartmentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    department_id: int
    hire_date: date


class EmployeeOut(EmployeeCreate):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)


class EmployeePage(BaseModel):
    items: list[EmployeeOut]
    total: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="HRFlow API", version="0.1.0", lifespan=lifespan)


def get_db():
    with SessionLocal() as db:
        yield db


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/departments", response_model=DepartmentOut, status_code=201)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    if db.scalar(select(Department).where(Department.name == payload.name)):
        raise HTTPException(409, "Department already exists")
    obj = Department(name=payload.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/v1/departments", response_model=list[DepartmentOut])
def list_departments(db: Session = Depends(get_db)):
    return db.scalars(select(Department).order_by(Department.name)).all()


@app.post("/api/v1/employees", response_model=EmployeeOut, status_code=201)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    if db.get(Department, payload.department_id) is None:
        raise HTTPException(404, "Department not found")
    if db.scalar(select(Employee).where(Employee.email == str(payload.email))):
        raise HTTPException(409, "Email already exists")
    obj = Employee(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/api/v1/employees", response_model=EmployeePage)
def list_employees(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    items = db.scalars(
        select(Employee).order_by(Employee.id).offset(offset).limit(limit)
    ).all()
    total = db.scalar(select(func.count()).select_from(Employee)) or 0
    return {"items": items, "total": total}


@app.get("/api/v1/employees/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    obj = db.get(Employee, employee_id)
    if obj is None:
        raise HTTPException(404, "Employee not found")
    return obj


@app.get("/api/v1/reports/headcount")
def headcount(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Department.name, func.count(Employee.id))
        .outerjoin(Employee)
        .group_by(Department.id)
        .order_by(Department.name)
    ).all()
    return {"by_department": [{"department": name, "count": count} for name, count in rows]}
