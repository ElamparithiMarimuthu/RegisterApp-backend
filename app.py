import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

def make_connection_to_db():
    """Establishes connection to the MySQL database."""
    mydb = mysql.connector.connect(
        host="database-3.czu28y4mu5vf.us-east-2.rds.amazonaws.com",
        user="Elam",
        password="eL1mXpMKp6Xbgh3ghwGh",
        database="Elam"
    )
    return mydb

def create_table():
    """Creates a 'users' table if it does not exist."""
    connect = make_connection_to_db()
    cursor = connect.cursor()
    sql_command = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name TEXT NOT NULL,
        passwd TEXT NOT NULL,
        age INT
    )
    """
    cursor.execute(sql_command)
    connect.commit()  
    cursor.close()  
    connect.close()  

@app.route("/register", methods=["POST"])
def register_app():
    """Registers a new user through a POST API."""
    data = request.get_json()  
    name = data.get('name')
    passwd = data.get('passwd')
    age = data.get('age')

    if not name or not passwd or age is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        connect = make_connection_to_db()
        cursor = connect.cursor()
        sql_command = """
        INSERT INTO users (name, passwd, age)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql_command, (name, passwd, age))
        connect.commit()
        user_id = cursor.lastrowid
        cursor.close()
        connect.close()
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__" :
    app.run(host="0.0.0.0" ,port=5000)

