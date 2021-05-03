import sqlite3

conn = sqlite3.connect('./baln.db')
c = conn.cursor()

# Create table
c.execute("CREATE TABLE balnBnusdApy (time text, apy real)")
c.execute("CREATE TABLE sicxBnusdApy (time text, apy real)")
c.execute("CREATE TABLE sicxIcxApy (time text, apy real)")
c.execute("CREATE TABLE loansApy (time text, apy real)")
c.execute("CREATE TABLE totalBalnSupply (time text, supply real)")
c.execute("CREATE TABLE stakedBalnSupply (time text, supply real)")
c.execute("CREATE TABLE balnBnusdPrice (time text, bnusd real)")
c.execute("CREATE TABLE sicxBnusdPrice (time text, bnusd real)")
c.execute("CREATE TABLE sicxIcxPool (time text, icx real)")
c.execute("CREATE TABLE sicxBnusdPool (time text, sicx real, bnusd real)")
c.execute("CREATE TABLE balnBnusdPool (time text, baln real, bnusd real)")
conn.commit()
conn.close()
