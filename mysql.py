import sqlite3

try:
    #Connecting to SQLite database
    stealthConn = sqlite3.connect('stealth.db')

    cursor = stealthConn.cursor()
    print('DB Init')

    query = 'select sqlite_version()'
    cursor.execute(query)
    result = cursor.fetchall()
    print('SQLite Version is {}'.format(result))
    cursor.close()

except sqlite3.Error as error:
    print('Error occured - ', error)

finally:
    if stealthConn:
        stealthConn.close()
        print('SQLite connection closed')