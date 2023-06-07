import sqlite3
import os

print("#4 python")

# Connect to the first database
db1 = sqlite3.connect('db_new.sqlite3')

# Connect to the second database
db2 = sqlite3.connect('db/db.sqlite3') 

# Retrieve the new values from the first database
new_houses = db1.execute('SELECT * FROM houses').fetchall()

# Replace the old values in the second database
db2.execute('DELETE FROM houses')
db2.executemany('INSERT INTO houses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,?)', new_houses)


# Commit the changes to the second database
db2.commit()


# Close the database connections
db1.close()
db2.close()

os.remove("db_new.sqlite3")
os.remove("houses.sqlite3")

print ('DONE')