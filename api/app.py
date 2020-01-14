from flask import Flask, request, jsonify, render_template
from time import sleep
import sqlite3 as sqlite
import requests
import sys
import os
import socket
app = Flask(__name__)

default_api_info = """<h1>API - Temperatures</h1>
    <p><strong>GET /nuevo/:data</strong> to add new data</p>
    <p><strong>GET /nuevo/404</strong> to close the server</p>
    <p><strong>GET /flush</strong> to clean data</p>
    <p><strong>GET /listar</strong> to get all the temperature data</p>
    <p><strong>GET /grafica</strong> to get the graph</p>
    <p><strong>GET /listajson</strong> to get the last 10 temperature data</p>
    """

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/', methods=['GET'])
def home():
    return default_api_info

@app.errorhandler(404)
def page_not_found(e):
    return default_api_info

# A route to flush data
@app.route('/flush', methods=['GET'])
def api_flush():
    conn = sqlite.connect('../data/adrisalas.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    sql = "DELETE FROM temperatures;"
    cur.execute(sql)
    conn.commit()

    for i in range(10):
        sql = "INSERT INTO temperatures ('data') VALUES (0);"
        cur.execute(sql)
        conn.commit()
        sleep(1)
    

    return """<h1>API - Temperatures</h1>
        <p>Data flushed</p>
        """

# A route to get all the temperature data
@app.route('/listar', methods=['GET'])
def api_list():
    conn = sqlite.connect('../data/adrisalas.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    all_data = cur.execute("SELECT * FROM temperatures ORDER BY timestamp DESC;").fetchall()
    
    return jsonify(all_data)

# A route to get the last 10 temperature data
@app.route("/listajson", methods=['GET'])
def api_ten():
    conn = sqlite.connect('../data/adrisalas.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    all_data = cur.execute("SELECT * FROM temperatures ORDER BY timestamp DESC LIMIT 10;").fetchall()

    return jsonify(all_data)

# A route to add new data
@app.route('/nuevo/<string:data>', methods=['GET'])
def api_new(data):
    try: 
        data = int(data)
    except ValueError:
        return """<h1>API - Temperatures</h1>
        <p>INCORRECT DATA</p>
        """
    
    if (data==404):
        shutdown_server()
        return """<h1>API - Temperatures</h1>
            <p>Server Down</p>
            """

    conn = sqlite.connect('../data/adrisalas.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    sql = "INSERT INTO temperatures ('data') VALUES ("
    sql += str(data)
    sql += ");"
    
    cur.execute(sql)
    conn.commit()

    return """<h1>API - Temperatures</h1>
    <p>Data inserted</p>
    """

# A route to show a graph
@app.route('/grafico' ,methods=['GET'])
def api_graph():

    line_labels = []
    line_values = []
    response = requests.get("http://localhost/listajson")

    for dictionary in response.json():
        line_labels.append(dictionary["timestamp"])
        line_values.append(dictionary["data"])
    
    return render_template('line_chart.html', title='API - Temperatures', max=20, labels=line_labels, values=line_values)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)