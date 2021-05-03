from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

HOURS = 24 * 7

def get_table(c, table_name) -> list:
  c.execute(f"SELECT * FROM {table_name} WHERE time >= Datetime('now', '-{HOURS} hours');");
  return c.fetchall()

def get_all_data(c) -> str:
  return jsonify({
    "totalBalnSupply": get_table(c, "totalBalnSupply"),
    "stakedBalnSupply": get_table(c, "stakedBalnSupply"),
    "balnBnusdPrice": get_table(c, "balnBnusdPrice"),
    "sicxBnusdPrice": get_table(c, "sicxBnusdPrice"),
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
  c = conn.cursor()
  data = get_all_data(c)
  conn.close()
  return data  

@app.route('/')
def index():
  return render_template('index.jinja')
