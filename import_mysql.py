import oracledb
from config import ORACLE_USER, ORACLE_PASSWORD, ORACLE_HOST, ORACLE_PORT, ORACLE_SERVICE

dsn = oracledb.makedsn(ORACLE_HOST, ORACLE_PORT, service_name=ORACLE_SERVICE)
conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn)

print("✅ Connected to Oracle DB!")
