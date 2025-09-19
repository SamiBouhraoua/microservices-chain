# Microservices Chain

Projet académique démontrant une **chaîne de microservices polyglottes** (Node.js, C#, Python) orchestrée par une Gateway.

---

## Description

Le système est composé de **4 microservices** et d’un **client** :

- **Service A (Node.js / Express)**  
  Transforme le message en **MAJUSCULES**.

- **Service B (C# / .NET)**  
  Inverse le message.

- **Service C (Python / FastAPI)**  
  Ajoute la longueur du message.

- **Gateway (Python / FastAPI)**  
  Centralise la communication et ajoute l’information finale.

- **Client (Python)**  
  Envoie un message initial et affiche le résultat de la chaîne complète.

Chaque service ajoute une **trace** (`service`, `language`, `info`, `timestamp`) pour suivre le parcours du message.

---

## Organisation du projet

```text
microservices-chain/
│
├─ gateway_fastapi/        # Gateway en FastAPI (Python)
│   ├─ main.py
│   ├─ requirements.txt
│
├─ service_a_node/         # Service A en Node.js
│   ├─ server.mjs
│   ├─ package.json
│
├─ service_b_csharp/       # Service B en C#
│   ├─ Program.cs
│   ├─ service_b_csharp.csproj
│
├─ service_c_fastapi/      # Service C en FastAPI (Python)
│   ├─ service_c.py
│   ├─ requirements.txt
│
├─ client/                 # Client Python
│   ├─ client.py
│
└─ README.md               # Documentation principale
```

---

## Ordre de démarrage

Toujours démarrer de l’aval vers l’amont :

```bash
# 1. Service C (Python / FastAPI, port 9003)
cd service_c_fastapi
uvicorn service_c:app --reload --port 9003

# 2. Service B (C#, port 9002)
cd service_b_csharp
dotnet run

# 3. Service A (Node.js / Express, port 9001)
cd service_a_node
npm install
npm start

# 4. Gateway (Python / FastAPI, port 8000)
cd gateway_fastapi
uvicorn main:app --reload --port 8000

# 5. Client (Python)
cd client
pip install -r requirements.txt
python client.py
```

---

## Exemple de sortie

```bash
{
  "message": "SECIVRESORCIM RUOJNOB | len=21 | service-c",
  "trace": [
    {
      "service": "service-a",
      "language": "JavaScript",
      "info": { "uppercased": true },
      "timestamp": 1758260651679
    },
    {
      "service": "service-b",
      "language": "C#",
      "info": { "reversed": true },
      "timestamp": 1758260651
    },
    {
      "service": "service-c",
      "language": "Python",
      "info": { "appended_len": 21 },
      "timestamp": 1758260651.6862278
    },
    {
      "service": "gateway",
      "language": "Python (FastAPI)",
      "info": { "final": true },
      "timestamp": 1758260651.6922114
    }
  ]
}
```

---

## Technologies utilisées

Python : FastAPI, Uvicorn, Requests

Node.js : Express, body-parser, node-fetch

C# : .NET 8, Minimal API

Client : Python (Requests)

---

## Auteur

Sami Bouhraoua
