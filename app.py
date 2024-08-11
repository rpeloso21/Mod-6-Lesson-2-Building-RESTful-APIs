from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Int(required = True)
    name = fields.String(required = True)
    age = fields.Int(required = True)

class SessionSchema(ma.Schema):
    session_id = fields.Int(required = True)
    member_id = fields.Int(required = True)
    session_date = fields.Date(required = True)
    session_time = fields.String(required = True)
    activity = fields.String(required = True)


    # class Meta:
    #     fields = ("name", "age")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

session_schema = SessionSchema()
sessions_schema = SessionSchema(many = True)


def get_db_connection():
    db_name = "e_commerce_db"
    user = "root"
    password = "Tsrost007!"
    host = "localhost"

    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )
        
        print("Connected to MySQL database successfully")
        return conn

    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    return "Mod 6 Lesson 2 Assignment Home Page"


@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Databbase connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)

        query = "select * from members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "internal server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Databbase connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)

        query = "select * from members where id = %s"

        cursor.execute(query, (id,))

        member = cursor.fetchone()

        return member_schema.jsonify(member)


    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "internal server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members', methods=['POST'])

def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Databbase connection failed"}), 500
        cursor = conn.cursor()

        new_member = (member_data['id'], member_data['name'], member_data['age'])

        query = "insert into members (id, name, age) values (%s, %s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message": "New member added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")

        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members/<int:id>', methods=['PUT'])

def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Databbase connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data['name'], member_data['age'], id)

        query = 'update members set name = %s, age = %s where id = %s'

        cursor.execute(query, updated_member)
        conn.commit()


        return jsonify({"message": "Updated member successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members/<int:id>', methods=['DELETE'])

def delete_member(id):
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Databbase connection failed"}), 500
        cursor = conn.cursor()

        member_to_remove = (id,)

        cursor.execute("select * from members where id = %s", member_to_remove)
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "Member not found"}), 404

        query = "delete from members where id = %s"
        cursor.execute(query, member_to_remove)
        conn.commit()

        return jsonify({"message": "Member deleted successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# Task 3

#--------------------------------------------------------------------------------------------
@app.route('/sessions', methods=['GET'])
def get_all_sessions():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Databbase connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)

        query = "select * from workoutsessions"

        cursor.execute(query)

        members = cursor.fetchall()

        return sessions_schema.jsonify(members)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "internal server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/sessions/<int:member_id>', methods=['GET'])
def get_sessions(member_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Databbase connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)

        query = "select * from workoutsessions where member_id = %s"

        cursor.execute(query, (member_id,))

        sessions = cursor.fetchall()

        return sessions_schema.jsonify(sessions)


    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "internal server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/sessions', methods=['POST'])

def add_session():
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Databbase connection failed"}), 500
        cursor = conn.cursor()

        new_session = (session_data['session_id'], session_data['member_id'], session_data['session_date'], session_data['session_time'], session_data['activity'])

        query = "insert into workoutsessions (session_id, member_id, session_date, session_time, activity) values (%s, %s, %s, %s, %s)"

        cursor.execute(query, new_session)
        conn.commit()

        return jsonify({"message": "New session added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")

        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/sessions/<int:session_id>', methods=['PUT'])

def update_session(session_id):
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Databbase connection failed"}), 500
        cursor = conn.cursor()

        updated_session = (session_data['session_id'], session_data['member_id'], session_data['session_date'], session_data['session_time'], session_data['activity'], session_id)

        query = 'update workoutsessions set session_id = %s, member_id = %s, session_date = %s, session_time = %s, activity = %s where session_id = %s'

        cursor.execute(query, updated_session)
        conn.commit()


        return jsonify({"message": "Updated session successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    app.run(debug = True)


