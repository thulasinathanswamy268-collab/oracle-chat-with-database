import oracledb

conn = oracledb.connect(
    user="hr",
    password="hr",
    dsn="localhost:1521/XE"
)

print("✅ Connected to Oracle DB!")
