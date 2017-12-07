import sqlite3

db_name = "match.db"
db_conn = None
db_cur = None

def connect():
    global db_conn
    global db_cur
    db_conn = sqlite3.connect(db_name)
    db_cur = db_conn.cursor()

def commit():
    db_conn.commit()

def close():
    global db_conn
    global db_cur
    db_conn.close()
    db_cur = None
    db_conn = None

def execute(sql, binds = None):
    db_cur.execute(sql, binds)
    return db_cur.lastrowid

def excecute_all(sqls):
    for sql in sqls:
        db_cur.execute(sql)

def fetch(sql, binds = None):
    if binds is None:
        db_cur.execute(sql)
    else:
        db_cur.execute(sql, binds)
    return db_cur.fetchall()

if __name__ == "__main__":
    None
