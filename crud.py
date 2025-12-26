from sqlalchemy import text
from fastapi import HTTPException


# -------------------------------
# Safety: validate table name
# -------------------------------
def validate_table_name(table: str):
    if not table.isidentifier():
        raise HTTPException(status_code=400, detail="Invalid table name")


# -------------------------------
# Detect primary key
# -------------------------------
def get_pk(db, table: str):
    validate_table_name(table)

    sql = (
        "SELECT a.attname "
        "FROM pg_index i "
        "JOIN pg_attribute a "
        "  ON a.attrelid = i.indrelid "
        " AND a.attnum = ANY(i.indkey) "
        f"WHERE i.indrelid = '{table}'::regclass "
        "  AND i.indisprimary"
    )

    row = db.execute(text(sql)).fetchone()
    return row[0] if row else None


# -------------------------------
# Columns safe for INSERT
# -------------------------------
def get_insertable_columns(db, table: str):
    sql = (
        "SELECT column_name "
        "FROM information_schema.columns "
        "WHERE table_schema = 'public' "
        "  AND table_name = :table "
        "  AND is_identity = 'NO' "
    )
    rows = db.execute(text(sql), {"table": table}).fetchall()
    return [r[0] for r in rows]


# -------------------------------
# INSERT ROW
# -------------------------------
def insert_row(db, table: str, data: dict):
    validate_table_name(table)

    cols = get_insertable_columns(db, table)
    payload = {k: v for k, v in data.items() if k in cols}

    if not payload:
        raise HTTPException(
            status_code=400, detail=f"No valid insertable columns for table '{table}'"
        )

    keys = ", ".join(payload.keys())
    values = ", ".join(f":{k}" for k in payload)

    sql = f"INSERT INTO {table} ({keys}) VALUES ({values}) RETURNING *"
    row = db.execute(text(sql), payload).fetchone()
    return dict(row._mapping)


# -------------------------------
# UPDATE ROW
# -------------------------------
def update_row(db, table: str, pk: str, pk_value: int, data: dict):
    validate_table_name(table)

    if not data:
        raise HTTPException(status_code=400, detail="No data to update")

    sets = ", ".join(f"{k}=:{k}" for k in data.keys())
    data["pk"] = pk_value

    sql = f"UPDATE {table} SET {sets} WHERE {pk} = :pk RETURNING *"
    row = db.execute(text(sql), data).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Row not found")

    return dict(row._mapping)


# -------------------------------
# DELETE ROW
# -------------------------------
def delete_row(db, table: str, pk: str, pk_value: int):
    validate_table_name(table)

    sql = f"DELETE FROM {table} WHERE {pk} = :pk"
    result = db.execute(text(sql), {"pk": pk_value})

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Row not found")
