import sqlite3
import time
import ciso8601

def get_table(c, table_name) -> list:
    now = int(time.time())
    c.execute(f"SELECT * FROM {table_name}");
    return c.fetchall()

def get_all_data(c) -> dict:
    tables = [
      "totalBalnSupply",
      "stakedBalnSupply",
      "balnBnusdPrice",
      "sicxBnusdPrice",
      "sicxIcxPool",
      "sicxBnusdPool",
      "balnBnusdPool",
      "balnBnusdApy",
      "sicxBnusdApy",
      "sicxIcxApy",
      "loansApy"
    ]
    result = {}
    for table in tables:
        result[table] = get_table(c, table)
    return result

conn = sqlite3.connect('./baln_old.db')
data = get_all_data(conn.cursor())

for name, table in data.items():
    newtable = []
    for entry in table:
        new_entry = list(entry)
        new_entry[0] = int(time.mktime(ciso8601.parse_datetime(new_entry[0]).timetuple()))
        newtable.append(tuple(new_entry))
    data[name] = newtable
conn.close()

# Export to new
conn = sqlite3.connect('./baln.db')
c = conn.cursor()

for name, table in data.items():
    for entry in table:
        values = ','.join(map(str, entry))
        query = f"INSERT INTO {name} VALUES ({values})"
        c.execute(query)

conn.commit()
conn.close()
