from fastapi import FastAPI, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import base64

from db import SessionLocal
from crud import insert_row, update_row, delete_row, get_pk

app = FastAPI(title="GreenCycles Dynamic CRUD API")

# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# ---------------- Helper (Binary-safe serializer) ----------------
def serialize_row_from_mapping(mapping):
    record = {}
    for col, val in mapping.items():
        if isinstance(val, (bytes, bytearray, memoryview)):
            record[col] = base64.b64encode(bytes(val)).decode("utf-8")
        else:
            record[col] = val
    return record

# ---------------- LIST TABLES ----------------
@app.get("/tables")
def list_tables(db: Session = Depends(get_db)):
    q = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_type = 'BASE TABLE'
    ORDER BY table_name
    """
    return [r[0] for r in db.execute(text(q))]

# ---------------- GET ALL ROWS ----------------
@app.get("/table/{table}")
def get_rows(table: str, db: Session = Depends(get_db)):
    result = db.execute(text(f"SELECT * FROM {table} LIMIT 100"))
    rows = result.fetchall()

    return [serialize_row_from_mapping(row._mapping) for row in rows]

# ---------------- GET ROW BY ID ----------------
@app.get("/table/{table}/{id}")
def get_row_by_id(
    table: str,
    id: int,
    db: Session = Depends(get_db),
):
    pk = get_pk(db, table)
    if not pk:
        raise HTTPException(status_code=400, detail="Table has no primary key")

    sql = f"SELECT * FROM {table} WHERE {pk} = :id"
    row = db.execute(text(sql), {"id": id}).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Row not found")

    return serialize_row_from_mapping(row._mapping)

# ---------------- INSERT ----------------
@app.post("/table/{table}")
def insert(
    table: str,
    data: dict = Body(...),
    db: Session = Depends(get_db),
):
    return insert_row(db, table, data)

# ---------------- UPDATE ----------------
@app.put("/table/{table}/{id}")
def update(
    table: str,
    id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
):
    pk = get_pk(db, table)
    if not pk:
        raise HTTPException(status_code=400, detail="Table has no primary key")

    return update_row(db, table, pk, id, data)

# ---------------- DELETE ----------------
@app.delete("/table/{table}/{id}")
def delete(
    table: str,
    id: int,
    db: Session = Depends(get_db),
):
    pk = get_pk(db, table)
    if not pk:
        raise HTTPException(status_code=400, detail="Table has no primary key")

    delete_row(db, table, pk, id)
    return {"status": "deleted"}
