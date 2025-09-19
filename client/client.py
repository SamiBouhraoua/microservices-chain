import requests, json

payload = {"message": "Bonjour microservices", "trace": []}
res = requests.post("http://127.0.0.1:8000/api/chain", json=payload)

print("Réponse finale :")
print(json.dumps(res.json(), indent=2, ensure_ascii=False))