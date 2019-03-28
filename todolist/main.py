from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import pymysql.cursors

app = Flask(__name__)

# todo_list = session['todo_list']
app.secret_key = b'\xceH\x1an\xab\xee,\xcb\xbbL\xc8~S\xb2i\x0f\xd3\xc1\xc9Fz\xe0\xcdF'

connection = pymysql.connect(host='localhost',
                             user='project1',
                             password='cs1122',
                             db='Project1')

# I put instructions on how to setup the database on your machine
# There is a table in the database called TodoList with the following columns
# +------------------------------------------+
# |                 TodoList                 |
# +----------------------------+-------------+
# | id (auto-incrementing int) | todo (text) |
# +----------------------------+-------------+

@app.route("/")
def index():
    # if "todo_list" not in session:
    #     session['todo_list'] = []
    # app.logger.debug(session['todo_list'])
    todos = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT todo FROM TodoList")
        todos = cursor.fetchall()
    return render_template("index.html", todo_list=todos)


@app.route("/todo/create", methods = ["POST"] )
def create_todo():
    #print("Yello")
    #print(request.get_json())
    data = request.get_json()
    #print(request)
    text = data['content']
    # session['todo_list'].append(text)
    # session.modified = True
    sql = "INSERT INTO TodoList (todo) VALUES (%s)"
    connection.cursor().execute(sql,(data['content'],))
    connection.commit()
    #print(text)
    return jsonify(result="success")


@app.route("/todo/read", methods = ["GET"])
def get_todo():
  #     return jsonify(session['todo_list'])
    cur = connection.cursor()
    read = "SELECT todo FROM TodoList"
    cur.execute(read)
    lst = cur.fetchall()
    return jsonify(lst)





@app.route("/todo/update", methods = ["PUT"])
def update_todo():
    data = request.get_json()
    #print(data)
    #session['todo_list'][session['todo_list'].index(data["item"])] = data["new"]
    #session.modified = True
    #print(todo_list)
    print(data["new"])
    sql = "UPDATE TodoList SET todo=%s WHERE todo=%s"
    connection.cursor().execute(sql, (data["new"], data["item"]))
    connection.commit()


    return jsonify(result="success")


@app.route("/todo/delete", methods = ["DELETE"])
def delete_todo():
    ##print(request.get_json())
    ##print(len(todo_list))
    #index = 0
    #for s in session['todo_list']:
    #    if(s==request.get_json()["item"]):
    #        session['todo_list'].pop(index)
    #        session.modified = True
    #        print(len(session['todo_list']))
    #        return jsonify(result="success")
    #    index = index + 1
    #return jsonify(result="failure")
    data = request.get_json()
    delete = "DELETE FROM TodoList WHERE todo=%s";
    connection.cursor().execute(delete, data["item"])
    connection.commit()
    return jsonify(result="success")

if __name__ == "__main__":
    app.run(debug = True)