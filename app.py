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


@app.route('/api/organization', methods=['GET'])
def query_organization():
    name = request.args.get("name")
    cypher = 'MATCH (n:Organization) WHERE ANY (name IN n.`organization-name` WHERE name CONTAINS $name) RETURN n LIMIT 10'

    start = perf_counter()
    res = neo4j_query(cypher, name=name)
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


@app.route("/api/neo4j/relation")
def neo4j_relation():
    """
    按照演员和导演的关系进行查询及统计（例如经常合作的演员有哪些，经常合作的导演和演员有哪些）
    """
    director = request.args.get("director", 0)
    actor = request.args.get("actor", 0)
    support_actor = request.args.get("support_actor", 0)
    skip = request.args.get("skip", 0)

    if director and actor:
        cypher = f'match (a:Actor{{ actor:"{actor}" }})--(p:Product)--(d:Director{{ director:"{director}" }}) RETURN p'
    elif director and support_actor:
        cypher = f'match (s:SupportActor{{ support_actor:"{support_actor}" }})--(p:Product)--(d:Director{{ director:"{director}" }}) RETURN p'
    elif actor and support_actor:
        cypher = f'match (a:Actor{{ actor:"{actor}" }})--(p:Product)--(s:SupportActor{{ support_actor:"{support_actor}" }}) RETURN p'
    else:
        return {"count": 0, 'time': 0, "data": []}

    print(cypher)

    start = perf_counter()
    res = neo4j_query(cypher)
    time = 1000 * (perf_counter() - start)

    res = [dict(zip(row[0].keys(), row[0].values())) for row in res]
    return {"count": len(res), 'time': time, "data": res}


@app.route("/api/neo4j/sql")
def neo4j_any():
    cypher = request.args.get("cypher", 0)
    return neo4j_query(cypher)


@app.route("/api/neo4j/product")
def neo4j_product():
    where = []
    y = request.args.get("y", 0)
    if y:
        where.append(f"p.y='{y}'")

    m = request.args.get("m", 0)
    if m:
        where.append(f"p.m='{m}'")

    d = request.args.get("d", 0)
    if d:
        where.append(f"p.d='{d}'")

    season = request.args.get("season", 0)
    if season:
        months = season2months[season]
        where.append(f"p.m='{months[0]}' or m='{months[1]}' or m='{months[2]}'")

    asin = request.args.get("asin", 0)
    if asin:
        where.append(f"p.asin='{asin}'")

    weekday = request.args.get("weekday", 0)
    if weekday:
        where.append(f"p.weekday='{weekday}'")

    title = request.args.get("title", 0)
    if title:
        where.append(f"p.title =~ '.*{title}.*'")

    rating = request.args.get("rating", 0)
    if rating:
        where.append(f"p.rating >= '{rating}'")

    director = request.args.get("director", 0)
    if director:
        where.append(f"p.director >= '{director}'")

    actor = request.args.get("actor", 0)
    if actor:
        where.append(f"a.actor = '{actor}'")

    support_actor = request.args.get("support_actor", 0)
    if support_actor:
        where.append(f"s.support_actor = '{support_actor}'")

    genres = request.args.getlist("genre[]")
    if genres:
        stat = ' or '.join([f"g.genre = '{g}'" for g in genres])
        where.append(f"({stat})")

    # elif genre:
    #     where.append(f"g.genre = '{genre}'")

    skip = request.args.get("skip", 0)

    cypher = f"MATCH (p:Product)-[pd]-(d:Director), (p)-[pa]-(a:Actor), (p)-[ps]-(s:Support_actor), (p)-[pg]-(g:Genre) WHERE {' and '.join(where)} RETURN p skip {skip} limit 20"

    cypher_count = f"MATCH (p:Product)-[pd]-(d:Director), (p)-[pa]-(a:Actor), (p)-[ps]-(s:Support_actor), (p)-[pg]-(g:Genre) WHERE {' and '.join(where)} RETURN count(p)"

    print(cypher)

    start = perf_counter()
    res = neo4j_query(cypher)
    time = 1000 * (perf_counter() - start)

    res_count = neo4j_query(cypher_count)

    res = [dict(zip(row[0].keys(), row[0].values())) for row in res]
    return {"count": res_count[0][0], 'time': time, "data": res}


if __name__ == "__main__":
    app.run(debug=True)
