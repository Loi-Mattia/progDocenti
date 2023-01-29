from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash,  render_template, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pymssql
import pandas as pd
from bson import json_util
import json

import psycopg2  # pip install psycopg2
import psycopg2.extras

app = Flask(__name__)

app.secret_key = 'xyzsdfg'


def connection():
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS',
                           user='franzetti.giulio', password='WWWWS7sN', database='franzetti.giulio')

    return conn


mysql = MySQL(app)
CORS(app)


@app.route('/')
def index():
    return "Ciao"


@app.route('/exams')
def exams():
    # Create a connection
    conn = connection()
    # Create a cursor
    cur = conn.cursor(as_dict=True)
    # Execute the SQL SELECT statement
    cur.execute("SELECT * FROM Progetto.verifica")
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
            'SELECT * FROM Progetto.docente WHERE email=%s AND password=%s', (email, password))
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
        session.pop('email', None)
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return jsonify({"message": "You are not logged in"}), 400


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.json['nome']
        cognome = request.json['cognome']
        email = request.json['email']
        password = request.json['password']

        conn = connection()
        # Create a cursor
        cursor = conn.cursor()
        # Execute a SELECT query
        cursor.execute('SELECT * FROM Progetto.docente WHERE email=%s', (email))
        # Fetch the data
        account = cursor.fetchone()
        if account:
            return jsonify({"message": "Account already exists"}), 400
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({"message": "Invalid email address"}), 400
        elif not name or not password or not email:
            return jsonify({"message": "Please fill out the form"}), 400
        else:
            # Execute an INSERT query
            print("10")
            cursor.execute(
                'INSERT INTO Progetto.docente (nome, cognome, email, password) VALUES (%s, %s, %s, %s)', (nome, cognome, email, password))
            conn.commit()
            return jsonify({"message": "You have successfully registered"}), 201


@app.route('/verifiche', methods=['POST', 'GET'])
def data1():
    conn = connection()
    # Create a cursor
    cur = conn.cursor(as_dict=True)
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        titolo = body['titolo']
        indirizzo = body['indirizzo']
        tipo_prova = body['tipo_prova']
        difficolta = body['difficolta']
        durata = body['durata']
        classe = body['classe']
        materia = body['materia']
        griglia = body['griglia']
        testo = body['testo']

        cur.execute("INSERT INTO Progetto.verifica (titolo,indirizzo,tipo_prova,difficolta,durata, classe,materia,griglia,testo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (titolo, indirizzo, tipo_prova, difficolta, durata, classe, materia, griglia, testo))
        conn.commit()
        return jsonify({
            'status': 'Data is posted to SQLite!',
            'titolo': titolo,
            'indirizzo': indirizzo,
            'tipo_prova': tipo_prova,
            'difficolta': difficolta,
            'durata': durata,
            'classe': classe,
            'materia': materia,
            'griglia': griglia,
            'testo': testo
        })

    # GET all data from database
    if request.method == 'GET':
        conn = connection()
        # Create a cursor
        cur = conn.cursor(as_dict=True)
        cur.execute("SELECT * FROM Progetto.verifica")
        data = cur.fetchall()
        dataJson = []
        print(data)
        for doc in data:
            id = doc['id']
            titolo = doc['titolo']
            indirizzo = doc['indirizzo']
            tipo_prova = doc['tipo_prova']
            difficolta = doc['difficolta']
            durata = doc['durata']
            classe = doc['classe']
            materia = doc['materia']
            griglia = doc['griglia']
            testo = doc['testo']
            dataDict = {
                'id': id,
                'titolo': titolo,
                'indirizzo': indirizzo,
                'tipo_prova': tipo_prova,
                'difficolta': difficolta,
                'durata': durata,
                'classe': classe,
                'materia': materia,
                'griglia': griglia,
                'testo': testo
             }
        dataJson.append(dataDict)
        return jsonify(dataJson)


@app.route('/verifiche/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata1(id):

    # GET a specific data by id
    if request.method == 'GET':
        conn = connection()
        # Create a cursor
        cur = conn.cursor(as_dict=True)
        cur.execute("SELECT * FROM Progetto.verifica WHERE id = %s", (id, ))
        ver = cur.fetchone()
        dataDict = {
            'id' : ver['id'],
            'titolo' : ver['titolo'],
            'indirizzo' : ver['indirizzo'],
            'tipo_prova' : ver['tipo_prova'],
            'difficolta' : ver['difficolta'],
            'durata' :ver['durata'],
            'classe' : ver['classe'],
            'materia' :ver['materia'],
            'griglia' :ver['griglia'],
            'testo' : ver['testo']
        }
        cur.close()
        conn.close()
        return jsonify(dataDict)

    # DELETE a data
    if request.method == 'DELETE':
        conn = connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM Progetto.verifica WHERE id = %s', (id,))
        ver = cur.fetchone()
        if ver:
            cur.execute('DELETE FROM Progetto.verifica WHERE id = %s', (id,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'status': 'Data id: ' + str(id) + ' is deleted!'})
        else:
            return jsonify({"message": "Data not found"}), 404

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        titolo = body['titolo']
        indirizzo = body['indirizzo']
        tipo_prova = body['tipo_prova']
        difficolta = body['difficolta']
        durata = body['durata']
        classe = body['classe']
        materia = body['materia']
        griglia = body['griglia']
        testo = body['testo']

        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Progetto.verifica WHERE id = %s", (id,))
        ver = cur.fetchone()
        if ver:
            cur.execute("UPDATE Progetto.verifica SET titolo = %s, indirizzo = %s, tipo_prova = %s, difficolta = %s, durata = %s, classe = %s, materia = %s, griglia = %s, testo = %s WHERE id = %s",
                        (titolo, indirizzo, tipo_prova, difficolta, durata, classe, materia, griglia, testo ,id))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'status': 'Data id: ' + str(id) + ' is updated!'})
        else:
            return jsonify({"message": "Data not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
