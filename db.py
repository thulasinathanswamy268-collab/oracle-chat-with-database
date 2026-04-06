import oracledb
from config import ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN

def get_connection():
    """Create and return an Oracle DB connection."""
    conn = oracledb.connect(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN
    )
    return conn


def get_schema_info():
    """Fetch all table names and their columns from Oracle DB."""
    conn = get_connection()
    cursor = conn.cursor()

    schema_text = ""

    # Get all user tables
    cursor.execute("""
        SELECT table_name 
        FROM user_tables 
        ORDER BY table_name
    """)
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        cursor.execute(f"""
            SELECT column_name, data_type, nullable
            FROM user_tab_columns
            WHERE table_name = '{table}'
            ORDER BY column_id
        """)
        columns = cursor.fetchall()
        col_defs = ", ".join([f"{col[0]} ({col[1]})" for col in columns])
        schema_text += f"Table: {table}\n  Columns: {col_defs}\n\n"

    cursor.close()
    conn.close()
    return schema_text, tables


def clean_sql(sql: str) -> str:
    """Remove semicolons and markdown from SQL."""
    # Remove markdown code block markers
    sql = sql.replace("```sql", "").replace("```", "")
    # Take only first statement (before any semicolon)
    sql = sql.split(";")[0]
    # Strip whitespace
    sql = sql.strip()
    return sql


def run_query(sql: str):
    """Execute a SQL query and return results as list of dicts."""
    # ✅ Clean SQL before executing
    sql = clean_sql(sql)

    if not sql:
        return [{"error": "Empty SQL query"}]

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchmany(100)
            result = [dict(zip(columns, row)) for row in rows]
        else:
            conn.commit()
            result = [{"status": "Query executed successfully", "rows_affected": cursor.rowcount}]
    except Exception as e:
        result = [{"error": str(e)}]
    finally:
        cursor.close()
        conn.close()
    return result
