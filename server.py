from flask import Flask, render_template, jsonify
import sqlite3
import time

app = Flask(__name__)

SECONDS = 3600 * 24 * 7

def get_table(c, table_name) -> list:
  now = int(time.time())
  c.execute(f"SELECT * FROM {table_name} WHERE time >= {now - SECONDS}");
  return c.fetchall()

def get_all_data(c) -> str:
  return jsonify({
    "totalBalnSupply": get_table(c, "totalBalnSupply"),
    "stakedBalnSupply": get_table(c, "stakedBalnSupply"),
    "balnBnusdPrice": get_table(c, "balnBnusdPrice"),
    "sicxBnusdPrice": get_table(c, "sicxBnusdPrice"),
    "balnSicxPrice": get_table(c, "balnSicxPrice"),
    "sicxIcxPool": get_table(c, "sicxIcxPool"),
    "sicxBnusdPool": get_table(c, "sicxBnusdPool"),
    "balnBnusdPool": get_table(c, "balnBnusdPool"),
    "balnBnusdApy": get_table(c, "balnBnusdApy"),
    "sicxBnusdApy": get_table(c, "sicxBnusdApy"),
    "sicxIcxApy": get_table(c, "sicxIcxApy"),
    "loansApy": get_table(c, "loansApy"),
  })

@app.route('/readall')
def readall():
  conn = sqlite3.connect('./baln.db')
  data = get_all_data(conn.cursor())
  conn.close()
  return data  

@app.route('/')
def index():
  return render_template('index.jinja')
