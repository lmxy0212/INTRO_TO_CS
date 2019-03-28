from flask import Flask
import pymysql.cursors
import pymysql
app = Flask(__name__)


@app.route("/")
def lol():
    conn = pymysql.connect(host='chalbroker.cs1122.engineering.nyu.edu',
                                 user='student',
                                 password='student',
                                 db='cs1122')
    cur = conn.cursor()
    cur.execute("SELECT*FROM students WHERE net_id = 'ml5719'")
    row = cur.fetchall()
    row = str(row)
    cur.close()
    conn.close()
    return row


if __name__ == "__main__":
    app.run(debug = True)
