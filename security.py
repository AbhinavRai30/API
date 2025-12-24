FORBIDDEN_PREFIXES = ("pg_", "sql_", "information_schema")

def validate_table_name(table: str):
    if not table.isidentifier():
        raise ValueError("Invalid table name")
    for p in FORBIDDEN_PREFIXES:
        if table.startswith(p):
            raise ValueError("Access denied")
