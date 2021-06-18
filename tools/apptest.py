import requests

cypher = ''

res = requests.get('http://localhost:8080/api/query', {'cypher': cypher}).json()

print(res)
