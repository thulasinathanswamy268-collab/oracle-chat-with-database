import mysql.connector
from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE


def get_connection():
    """Create and return a MySQL connection."""
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=int(MYSQL_PORT),
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    return conn


def get_schema_info():
    """Fetch all table names and their columns from MySQL."""
    conn = get_connection()
    cursor = conn.cursor()

    schema_text = ""

    # Get all tables in the current database
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        cursor.execute(
            "SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s ORDER BY ORDINAL_POSITION",
            (MYSQL_DATABASE, table)
        )
        columns = cursor.fetchall()
        col_defs = ", ".join([f"{col[0]} ({col[1]})" for col in columns])
        schema_text += f"Table: {table}\n  Columns: {col_defs}\n\n"

    cursor.close()
    conn.close()
    return schema_text, tables


def clean_sql(sql: str) -> str:
    """Remove semicolons and markdown from SQL."""
    sql = sql.replace("```sql", "").replace("```", "")
    sql = sql.split(";")[0]
    sql = sql.strip()
    return sql


def run_query(sql: str):
    """Execute a SQL query and return results as list of dicts."""
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
