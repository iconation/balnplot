#!/usr/bin/env python3

import sqlite3
import requests
import json

def filter_str(input) -> str:
    return input.replace("BALN", "").replace("bnUSD", "").replace("sICX", "").replace("ICX", "").replace(",", "")

def get_baln_data() -> dict:
    data = json.loads(requests.get("https://onz7so.deta.dev/api/v1/info").text)
    return {
        "totalBalnSupply": float(filter_str(data['totalBalnSupply'])),
        "stakedBalnSupply": float(filter_str(data['stakedBalnSupply'])),
        "balnBnusdPrice": float(filter_str(data['balnBnusdPrice'])),
        "sicxBnusdPrice": float(filter_str(data['sicxBnusdPrice'])),
        "sicxIcxPool": float(filter_str(data['sicxIcxPool'])),
        "sicxBnusdPool": list(map(lambda x: float(x), filter_str(data['sicxBnusdPool']).split('/'))),
        "balnBnusdPool": list(map(lambda x: float(x), filter_str(data['balnBnusdPool']).split('/')))
    }

# Get ping
data = get_baln_data()
print(data)

# get db data
conn = sqlite3.connect('./baln.db')
c = conn.cursor()

c.execute("INSERT INTO totalBalnSupply VALUES (datetime('now', 'localtime'), %f)" % data['totalBalnSupply'])
c.execute("INSERT INTO stakedBalnSupply VALUES (datetime('now', 'localtime'), %f)" % data['stakedBalnSupply'])
c.execute("INSERT INTO balnBnusdPrice VALUES (datetime('now', 'localtime'), %f)" % data['balnBnusdPrice'])
c.execute("INSERT INTO sicxBnusdPrice VALUES (datetime('now', 'localtime'), %f)" % data['sicxBnusdPrice'])
c.execute("INSERT INTO sicxIcxPool VALUES (datetime('now', 'localtime'), %f)" % data['sicxIcxPool'])
c.execute("INSERT INTO sicxBnusdPool VALUES (datetime('now', 'localtime'), %f, %f)" % (data['sicxBnusdPool'][0], data['sicxBnusdPool'][1]))
c.execute("INSERT INTO balnBnusdPool VALUES (datetime('now', 'localtime'), %f, %f)" % (data['balnBnusdPool'][0], data['balnBnusdPool'][1]))

conn.commit()
conn.close()
