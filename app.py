import math
import yfinance as yf
from time import perf_counter
import json
from json import JSONEncoder
import redis
from datetime import datetime

from flask.helpers import make_response
from neo4j import GraphDatabase
from neo4j.time import DateTime
from neo4j.graph import Path, Node, Relationship
from flask import Flask, request, jsonify
from flask_cors import CORS

r = redis.Redis(host='7c00h.xyz', port=6379, password='tanzixuan', db=2)
driver = GraphDatabase.driver("neo4j://7c00h.xyz:7687", auth=("neo4j", "root"))

app = Flask(__name__)
CORS(app)


def ScoreforO(ticker: str) -> int:
    msft = yf.Ticker(ticker)
    df = msft.get_financials(proxy='http://7c00h.xyz:7890')
    if df.empty:
        return 5.0
    items = ["Income Before Tax", ""]
    weight = [0.55, 0.15, 0.05, 0.05, 0.1, 0.1]
    fin = []
    i = df.loc["Income Before Tax"]
    fin.append((i.sum()-i.min()*4)/(i.max()-i.min())*5)
    #i=df.loc["Total Revenue"]/df.loc["Total Revenue"]
    return fin[0]


@app.route('/api/oscore')
def api_oscore():
    ticker = request.args.get('ticker')
    return {'score': ScoreforO(ticker)}


def ScoreforI(tickers: list, edu: int) -> int:
    score = 0
    for i in tickers:
        score += ScoreforO(i)
    edu = edu/1.6
    score = (math.exp(score)/(math.exp(score)+1)-0.5)*8
    lscore = (math.exp(edu)/(math.exp(edu)+1)-0.5)*2
    return {'score': score+lscore}


@app.route('/api/pscore')
def api_pscore():
    tickers = request.args.getlist('tickers[]')
    edu = int(request.args.get('edu'))
    return ScoreforI(tickers, edu)


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
        labels = list(x.labels)
        if 'Resource' in labels:
            labels.remove('Resource')
        return {"id": x.id, 'labels': labels, 'properties': x._properties}
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
    if r.exists(cypher):
        print('cached!')
        data = r.get(cypher)
        resp = make_response(data)
        resp.headers['content-type'] = 'application/json; charset=utf-8'
        return resp

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
    r.setex(cypher, 10 * 60, data)  # cache for 10 mins
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
