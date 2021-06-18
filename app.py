from time import perf_counter
import json
from json import JSONEncoder
from datetime import datetime

from flask.helpers import make_response
from neo4j import GraphDatabase
from neo4j.time import DateTime
from neo4j.graph import Path, Node, Relationship
from flask import Flask, request, jsonify
from flask_cors import CORS

driver = GraphDatabase.driver("neo4j://7c00h.xyz:7687", auth=("neo4j", "root"))
# session = driver.session()

app = Flask(__name__)
CORS(app)


def query(tx, cypher, **param):
    res = []
    for result in tx.run(cypher, **param):
        res.append(result.values())
    return res


def neo4j_query(cypher, **param):
    with driver.session() as session:
        return session.read_transaction(query, cypher, **param)


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, DateTime):
            return o.iso_format()
        return super(CustomJSONEncoder, self).default(o)


class ProcessError(RuntimeError):
    pass


def preprocess(x):
    if isinstance(x, Node):
        return {"id": x.id, 'labels': list(x.labels), 'properties': x._properties}
    elif isinstance(x, Relationship):
        return {'id': x.id,
                'type': x.type,
                'start_node': preprocess(x.start_node),
                'end_node': preprocess(x.end_node),
                'nodes': [preprocess(n) for n in x.nodes]}
    elif isinstance(x, Path):
        return {'start_node': preprocess(x.start_node),
                'end_node': preprocess(x.end_node),
                'nodes': [preprocess(n) for n in x.nodes],
                'relationships': [preprocess(r) for r in x.relationships]}
    else:
        raise ProcessError()


def timed_query(cypher, **param):
    start = perf_counter()
    res = neo4j_query(cypher, **param)
    time = 1000 * (perf_counter() - start)

    res = [preprocess(row[0]) for row in res]
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


if __name__ == "__main__":
    app.run(port=8080, debug=True)
