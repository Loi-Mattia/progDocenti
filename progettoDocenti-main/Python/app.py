from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash,  render_template, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pymssql
import json

import psycopg2  # pip install psycopg2
import psycopg2.extras

app = Flask(__name__)

app.secret_key = 'xyzsdfg'


def connection():
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS',
                            user='barbieri.riccardo', password='xxx123##', database='barbieri.riccardo')
    return conn


mysql = MySQL(app)
CORS(app)


@app.route('/')
def index():
    return "Ciao"


@app.route('/verifica')
def exams():
    # Create a connection
    conn = connection()
    # Create a cursor
    cur = conn.cursor(as_dict=True)
    # Execute the SQL SELECT statement
    cur.execute("SELECT * FROM progetto.verifica")
    # Fetch all rows from the SELECT statement
    list_users = cur.fetchall()
    # Render the index.html template and pass the list of students
    # return render_template('hehe.html', list_users = list_users)

    return jsonify(list_users)
    resp = jsonify(list_users)
    # return json.dumps(list_users)
    resp = json_util.dumps(list_users)
    return Response(resp, mimetype='application/json')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # return jsonify({"message": request.json['email']}), 200
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        # return jsonify({"message": email, "m2":password}), 200
        # print("ciao")
        conn = connection()
        # Create a cursor
        cursor = conn.cursor()
        # Execute a SELECT query
        cursor.execute(
            'SELECT * FROM progetto.docente WHERE email=%s AND password=%s', (email, password))
        # Fetch the data
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Logged in successfully", "email": email, "password": password}), 200
        else:
            return jsonify("Doesn't match"), 400

    return jsonify({"message": "Error"}), 400

          
@app.route('/logout')
def logout():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('name', None)
        session.pop('mail', None)
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return jsonify({"message": "You are not logged in"}), 400


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.json['nome']
        cognome = request.json['cognome']
        email = request.json['mail']
        password = request.json['password']

        conn = connection()
        # Create a cursor
        cursor = conn.cursor()
        # Execute a SELECT query
        cursor.execute('SELECT * FROM Progetto.docente WHERE mail=%s', (mail))
        # Fetch the data
        account = cursor.fetchone()
        if account:
            return jsonify({"message": "Account already exists"}), 400
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail):
            return jsonify({"message": "Invalid mail address"}), 400
        elif not name or not password or not mail:
            return jsonify({"message": "Please fill out the form"}), 400
        else:
            # Execute an INSERT query
            print("10")
            cursor.execute(
                'INSERT INTO Progetto.docente (nome, cognome, mail, password) VALUES (%s, %s, %s, %s)', (nome, cognome, mail, password))
            conn.commit()
            return jsonify({"message": "You have successfully registered"}), 201


@app.route('/verifica', methods=['POST', 'GET'])
def data1():
    conn = connection()
    # Create a cursor
    cur = conn.cursor(as_dict=True)
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        testo = body['testo']
        griglia = body['griglia']
        titolo = body['titolo']
        difficolta = body['difficolta']
        materia = body['materia']
        durata = body['durata']
  
        
        
     

        cur.execute("INSERT INTO progetto.verifica (testo,griglia,titolo,difficolta,materia, durata) VALUES (%s,%s,%s,%s,%s,%s)",
                    (testo,griglia,titolo,difficolta,materia, durata))
        conn.commit()
        return jsonify({
            'status': 'Data is posted to SQLite!',
            'testo': testo,
            'griglia': griglia,
            'titolo': titolo,
            'difficolta': difficolta,
            'materia': materia,
            'durata': durata,
      
        })

    # GET all data from database
    if request.method == 'GET':
        conn = connection()
        # Create a cursor
        cur = conn.cursor(as_dict=True)
        cur.execute("SELECT * FROM progetto.verifica")
        data = cur.fetchall()
        dataJson = []
        print(data)
        for doc in data:
            id = doc['id']
            testo = doc['testo']
            griglia = doc['griglia']
            titolo = doc['titolo']
            difficolta = doc['difficolta']
            materia = doc['materia']
          
            durata = doc['durata']
        
            dataDict = {
                'id': id,
                'testo': testo,
                'griglia': griglia,
                'titolo': titolo,
                'difficolta': difficolta,
                'materia': materia,
               
                'durata': durata,
          
             }
        dataJson.append(dataDict)
        return jsonify(dataJson)


@app.route('/verifica/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata1(id):

    # GET a specific data by id
    if request.method == 'GET':
        conn = connection()
        # Create a cursor
        cur = conn.cursor(as_dict=True)
        cur.execute("SELECT * FROM progetto.verifica WHERE id = %s", (id, ))
        ver = cur.fetchone()
        dataDict = {
            'id' : ver['id'],
            'testo' : ver['testo'],
            'griglia' : ver['griglia'],
            'titolo' : ver['titolo'],
            'difficolta' : ver['difficolta'],
            'materia' :ver['materia'],
            'durata' :ver['durata'],
      
        }
        cur.close()
        conn.close()
        return jsonify(dataDict)

    # DELETE a data
    if request.method == 'DELETE':
        conn = connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM progetto.verifica WHERE id = %s', (id,))
        ver = cur.fetchone()
        if ver:
            cur.execute('DELETE FROM progetto.verifica WHERE id = %s', (id,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'status': 'Data id: ' + str(id) + ' is deleted!'})
        else:
            return jsonify({"message": "Data not found"}), 404

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        testo = body['testo']
        griglia = body['griglia']
        titolo = body['titolo']
        difficolta = body['difficolta']
        materia = body['materia']
        durata = body['durata']
    

        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Progetto.verifica WHERE id = %s", (id,))
        ver = cur.fetchone()
        if ver:
            cur.execute("UPDATE Progetto.verifica SET testo = %s, griglia = %s, titolo = %s, difficolta = %s, materia = %s, durata = %s, WHERE id = %s",
                        (testo, griglia, titolo, difficolta, materia, durata, id))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'status': 'Data id: ' + str(id) + ' is updated!'})
        else:
            return jsonify({"message": "Data not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
