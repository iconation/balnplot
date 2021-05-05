import sqlite3
import time
import ciso8601
import sys

def get_table(c, table_name) -> list:
    c.execute(f"SELECT * FROM {table_name}");
    return c.fetchall()

def get_all_data(c) -> dict:
    tables = [
      "balnBnusdPrice",
      "sicxBnusdPrice",
    ]
    result = {}
    for table in tables:
        result[table] = get_table(c, table)
    return result

conn = sqlite3.connect('./baln.db')
c = conn.cursor()
data = get_all_data(conn.cursor())

if len(data['sicxBnusdPrice']) != len(data['balnBnusdPrice']):
    print("Error, invalid tables")
    sys.exit(0)

length = len(data['sicxBnusdPrice'])

balnsicxprices = []
for i in range(length):
    balnbnusd = data['balnBnusdPrice'][i]
    sicxbnusd = data['sicxBnusdPrice'][i]
    if abs(int(sicxbnusd[0]) - int(balnbnusd[0])) > 2:
        print(f"Error, unsync at {i} : {sicxbnusd[0]}, {balnbnusd[0]}")
        sys.exit(0)
    
    balnsicxprices.append(float(balnbnusd[1] / sicxbnusd[1]))

# Export to new
for i in range(length):
    balnbnusd = data['balnBnusdPrice'][i]
    entry = [balnbnusd[0], balnsicxprices[i]]
    values = ','.join(map(str, entry))
    c.execute(f"INSERT INTO balnSicxPrice VALUES ({values})")

conn.commit()
conn.close()
