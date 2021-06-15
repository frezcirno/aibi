from time import perf_counter
import json
from json import JSONEncoder
from datetime import datetime

from flask.helpers import make_response
from neo4j import GraphDatabase
from neo4j.time import DateTime
from flask import Flask, request, jsonify
from flask_cors import CORS

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "root"))
session = driver.session()

app = Flask(__name__)
CORS(app)


def neo4j_query(cypher, **param):
    def query(tx):
        res = []
        for result in tx.run(cypher, **param):
            res.append(result.values())
        return res

    return session.read_transaction(query)


def convert_time(dt: DateTime):
    pdt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                   int(dt.second), int(dt.second * 1000000 % 1000000))
    return pdt


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, DateTime):
            return super(CustomJSONEncoder, self).encode(convert_time(o).isoformat())
        return super(CustomJSONEncoder, self).default(o)


def extract_array(x):
    if isinstance(x, list):
        return x[0]
    return x


@app.route('/api/query', methods=['GET'])
def api_query():
    cypher = request.args.get("cypher")

    start = perf_counter()
    res = neo4j_query(cypher)
    time = 1000 * (perf_counter() - start)

    res = [dict(zip(row[0].keys(), [extract_array(val) for val in row[0].values()])) for row in res]
    data = json.dumps(
        {"count": len(res), 'time': time, "data": res},
        ensure_ascii=False,
        separators=(',', ':'),
        cls=CustomJSONEncoder
    )
    resp = make_response(data)
    resp.headers['content-type'] = 'application/json; charset=utf-8'
    return resp


@app.route('/api/organization', methods=['GET'])
def query_organization():
    name = request.args.get("name")
    cypher = 'MATCH (n:Organization) WHERE ANY (name IN n.`organization-name` WHERE name CONTAINS $name) RETURN n LIMIT 25'

    start = perf_counter()
    res = neo4j_query(cypher, name=name)
    time = 1000 * (perf_counter() - start)

    res = [dict(zip(row[0].keys(), [extract_array(val) for val in row[0].values()])) for row in res]
    data = json.dumps(
        {"count": len(res), 'time': time, "data": res},
        ensure_ascii=False,
        separators=(',', ':'),
        cls=CustomJSONEncoder
    )
    resp = make_response(data)
    resp.headers['content-type'] = 'application/json; charset=utf-8'
    return resp


if __name__ == "__main__":
    app.run(port=8080, debug=True)
