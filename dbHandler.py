import sqlite3

print("Initializing Database...")
db_name = 'Database/main-db.db'
conn = sqlite3.connect(db_name, check_same_thread=False)

crsr = conn.cursor()


def db_conn():

  print("Connected to the database")

  sql_command = """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id VARCHAR(200),
            acc_user VARCHAR(300),
            acc_pass VARCHAR(300),
            role VARCHAR(300),
            LAST_EDIT VARCHAR(100));"""

  crsr.execute(sql_command)
  print("All tables are ready")


def insertCommand(sql_command):
  crsr.execute(sql_command)
  conn.commit()
  return crsr.fetchall()