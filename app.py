from time import perf_counter
import json
from json import JSONEncoder
from datetime import datetime

from flask.helpers import make_response
from neo4j import GraphDatabase
from neo4j.time import DateTime
from flask import Flask, request, jsonify
from flask_cors import CORS

driver = GraphDatabase.driver("neo4j://7c00h.xyz:7687", auth=("neo4j", "root"))
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


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, DateTime):
            return o.iso_format()
        return super(CustomJSONEncoder, self).default(o)


def timed_query(cypher, **param):
    start = perf_counter()
    res = neo4j_query(cypher, **param)
    time = 1000 * (perf_counter() - start)

    res = [dict(zip(row[0].keys(), row[0].values())) for row in res]
    data = json.dumps(
        {"count": len(res), 'time': time, "data": res},
        ensure_ascii=False,
        separators=(',', ':'),
        cls=CustomJSONEncoder
    )
    resp = make_response(data)
    resp.headers['content-type'] = 'application/json; charset=utf-8'
    return resp


def extract_array(x):
    if isinstance(x, list):
        return x[0]
    return x


@app.route('/api/query', methods=['GET'])
def api_query():
    cypher = request.args.get("cypher")
    return timed_query(cypher)


@app.route('/api/organization', methods=['GET'])
def query_organization():
    name = request.args.get("name")
    cypher = 'MATCH (n:Organization) WHERE ANY (name IN n.`organization-name` WHERE name CONTAINS $name) RETURN n LIMIT 25'
    return timed_query(cypher, name=name)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
