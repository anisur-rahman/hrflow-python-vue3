import os
import tempfile
from pathlib import Path

_tmp = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = "sqlite:///" + str(Path(_tmp.name) / "test.db")

from fastapi.testclient import TestClient
from app.main import app


def test_employee_flow():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}

        dept = client.post("/api/v1/departments", json={"name": "IT"})
        assert dept.status_code == 201
        dept_id = dept.json()["id"]

        emp = client.post("/api/v1/employees", json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "department_id": dept_id,
            "hire_date": "2024-03-01",
        })
        assert emp.status_code == 201

        assert client.get("/api/v1/employees").json()["total"] == 1
        assert client.get("/api/v1/reports/headcount").json()["by_department"][0]["count"] == 1

        duplicate = client.post("/api/v1/employees", json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "department_id": dept_id,
            "hire_date": "2024-03-01",
        })
        assert duplicate.status_code == 409
