from flask import Flask , redirect , render_template ,request ,flash , session , url_for , jsonify
from flask_mysqldb import MySQL
from wtforms import Form , StringField , TextAreaField, PasswordField , validators
from flask_cors import CORS


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "pakistan1999$"
app.config['MYSQL_DB'] = "todoapp"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Init database
mysql = MySQL(app)
CORS(app)

@app.route('/api/tasks' , methods = ['GET'])
def get_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM list")
    result = cur.fetchall()
    return jsonify(result)

@app.route('/api/new_task' , methods = ['POST'])
def add_task():
    cur = mysql.connection.cursor()
    title = request.get_json()['title']
    des = request.get_json()['des']
    cur.execute("INSERT INTO `todoapp`.`list` (`subject`, `details`) VALUES ('" +str(title)+"', '" +str(des)+ "')")
    mysql.connection.commit()
    result = [{'title' : title },{'description' : des}]
    return jsonify(result)
    
@app.route('/api/task/<id>' , methods = ['PUT'])
def update_task(id):
    cur = mysql.connection.cursor()
    title = request.get_json()['title']
    des = request.get_json()['des']
    cur.execute("UPDATE `todoapp`.`list` SET `subject` = '" +str(title)+ "', `details` = '" +str(des)+ "' WHERE (`id` = '" + id +"' )")
    mysql.connection.commit()
    result = [{'title' : title},{'description' : des}]
    return jsonify( result)

@app.route('/api/remove/<id>' , methods=['DELETE'])
def delete(id):
    cur = mysql.connection.cursor()
    response = cur.execute("DELETE FROM list WHERE id = '"+id+"'")
    mysql.connection.commit()
    if response > 0 :
        result = {'message' : 'successful'}
    else:
        result = {'message' : 'unsuccessful'}
    return jsonify({'result' : result})

if __name__ == "__main__":
    app.run(debug=True , port=50)