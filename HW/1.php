import flask

app = flask.Flask(__name__)

todo_list = []
token = None

@app.route("POST/todo/create", methods = ["POST"] )
def create_todo():
    pass

@app.route("GET/todo/read", methods = ["GET"])
def get_todo():
    pass

@app.route("PUT/todo/update", methods = ["PUT"])
def update_todo():
    pass

@app.route("DELETE/todo/delete", methods = ["DELETE"])
def delete_todo():
    pass