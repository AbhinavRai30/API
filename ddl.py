from sqlalchemy import text
from security import validate_table_name

def create_table(db, name, columns):
    validate_table_name(name)

    col_defs = []
    for c in columns:
        col = f"{c['name']} {c['type']}"
        if c.get("primary_key"):
            col += " PRIMARY KEY"
        col_defs.append(col)

    sql = f"CREATE TABLE public.{name} ({', '.join(col_defs)})"
    db.execute(text(sql))
