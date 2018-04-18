import os
import time

from flask import request
from flask import Flask, render_template
import mysql.connector
from mysql.connector import errorcode


application = Flask(__name__)
app = application


def get_db_creds():
    db = os.environ.get("DB", None) or os.environ.get("database", None)
    username = os.environ.get("USER", None) or os.environ.get("username", None)
    password = os.environ.get("PASSWORD", None) or os.environ.get("password", None)
    hostname = os.environ.get("HOST", None) or os.environ.get("dbhost", None)
    return db, username, password, hostname


def create_table():
    # Check if table exists or not. Create and populate it only if it does not exist.
    db, username, password, hostname = get_db_creds()
    table_ddl = 'CREATE TABLE message(id INT UNSIGNED NOT NULL AUTO_INCREMENT, greeting TEXT, PRIMARY KEY (id))'

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)
        import MySQLdb
        #try:
        cnx = MySQLdb.connect(unix_socket=hostname, user=username, passwd=password, db=db)
        #except Exception as exp1:
        #    print(exp1)

    cur = cnx.cursor()

    try:
        cur.execute(table_ddl)
        cnx.commit()
        populate_data()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)


def populate_data():

    db, username, password, hostname = get_db_creds()

    print("Inside populate_data")
    print("DB: %s" % db)
    print("Username: %s" % username)
    print("Password: %s" % password)
    print("Hostname: %s" % hostname)

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                       host=hostname,
                                       database=db)
    except Exception as exp:
        print(exp)
        import MySQLdb
        cnx = MySQLdb.connect(unix_socket=hostname, user=username, passwd=password, db=db)

    cur = cnx.cursor()
    cur.execute("INSERT INTO message (greeting) values ('Hello, World!')")
    cnx.commit()
    print("Returning from populate_data")


def query_data():

    db, username, password, hostname = get_db_creds()

    print("Inside query_data")
    print("DB: %s" % db)
    print("Username: %s" % username)
    print("Password: %s" % password)
    print("Hostname: %s" % hostname)

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)
        import MySQLdb
        cnx = MySQLdb.connect(unix_socket=hostname, user=username, passwd=password, db=db)

    cur = cnx.cursor()

    cur.execute("SELECT greeting FROM message")
    entries = [dict(greeting=row[0]) for row in cur.fetchall()]
    return entries

try:
    print("---------" + time.strftime('%a %H:%M:%S'))
    print("Before create_table global")
    create_table()
    print("After create_data global")
except Exception as exp:
    print("Got exception %s" % exp)
    conn = None


@app.route('/add_to_db', methods=['POST'])
def add_to_db():
    print("Received request.")
    print(request.form['message'])
    msg = request.form['message']

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)
        import MySQLdb
        cnx = MySQLdb.connect(unix_socket=hostname, user=username, passwd=password, db=db)

    cur = cnx.cursor()
    cur.execute("INSERT INTO message (greeting) values ('" + msg + "')")
    cnx.commit()
    return hello()


@app.route("/")
def hello():
    print("Inside hello")
    print("Printing available environment variables")
    print(os.environ)
    print("Before displaying index.html")
    entries = query_data()
    print("Entries: %s" % entries)
    return render_template('index.html', entries=entries)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
