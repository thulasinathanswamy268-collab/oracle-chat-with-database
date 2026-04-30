import mysql.connector
from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE


def get_connection():
    """Create and return an Oracle DB connection."""
    dsn = oracledb.makedsn(ORACLE_HOST, ORACLE_PORT, service_name=ORACLE_SERVICE)
    conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn)
    return conn


def get_schema_info():
    """Fetch all table names and their columns from Oracle DB."""
    conn = get_connection()
    cursor = conn.cursor()

    schema_text = ""

    # Get all tables in the current user schema
    cursor.execute("SELECT TABLE_NAME FROM USER_TABLES ORDER BY TABLE_NAME")
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        cursor.execute(
            "SELECT COLUMN_NAME, DATA_TYPE FROM USER_TAB_COLUMNS WHERE TABLE_NAME = ? ORDER BY COLUMN_ID",
            (table,)
        )
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
