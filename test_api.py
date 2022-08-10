import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/test/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_data = cur.execute('SELECT * FROM mock_data;').fetchall()

    return jsonify(all_data)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/test', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    first_name = query_parameters.get('first_name')
    last_name = query_parameters.get('last_name')
    email = query_parameters.get('email')
    birth_date = query_parameters.get('birth_date')

    query = "SELECT * FROM mock_data WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if first_name:
        query += ' first_name=? AND'
        to_filter.append(first_name)
    if last_name:
        query += ' last_name=? AND'
        to_filter.append(last_name)
    if email:
        query += ' email=? AND'
        to_filter.append(email)
    if birth_date:
        query += ' birth_date=? AND'
        to_filter.append(birth_date)
    if not (id or first_name or last_name or email or birth_date):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
