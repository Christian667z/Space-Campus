# Sécurité & Déploiement en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

La sécurité et le déploiement sont les dernières étapes d’un projet Python professionnel.

Elles garantissent que :
- l’application est protégée contre les attaques,
- les données sont sécurisées,
- le système est stable en production,
- le projet est accessible aux utilisateurs,
- les mises à jour sont fiables.

Ces concepts sont essentiels pour :
- les applications web,
- les APIs,
- les systèmes cloud,
- les SaaS,
- les applications d’entreprise.

---

# 1. Sécurité en Python

---

# 1.1 Validation des entrées (Input Validation)

---

# Problème

Les utilisateurs peuvent envoyer des données malveillantes.

---

# Mauvais exemple

```python
user_input = input("Enter age: ")
print(eval(user_input))  # ❌ DANGEREUX
```

---

# Bon exemple

```python
user_input = input("Enter age: ")

if user_input.isdigit():
    age = int(user_input)
    print(age)
else:
    print("Invalid input")
```

---

# 1.2 Injection de code (SQL / Command Injection)

---

# Mauvais exemple

```python
query = "SELECT * FROM users WHERE name = '" + name + "'"
```

❌ Risque : SQL Injection

---

# Bon exemple (paramétré)

```python
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

---

# 1.3 Protection des mots de passe

---

# Mauvais

```python
password = "123456"
```

---

# Bon (hash sécurisé)

```python
import hashlib

password = "secret"
hashed = hashlib.sha256(password.encode()).hexdigest()

print(hashed)
```

---

# 1.4 Utilisation de secrets (au lieu de random)

---

```python
import secrets

token = secrets.token_hex(16)

print(token)
```

---

# 1.5 Variables sensibles (ENV)

---

```python
import os

API_KEY = os.getenv("API_KEY")
```

---

# 1.6 Cryptographie moderne (bcrypt recommandé)

---

```python
import bcrypt

password = b"secret"

hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print(hashed)
```

---

# 2. Sécurité Web (API / Backend)

---

# 2.1 Protection CORS

```python
from flask_cors import CORS

CORS(app)
```

---

# 2.2 Limitation des requêtes (Rate Limiting)

```python
from flask_limiter import Limiter

limiter = Limiter(app)
```

---

# 2.3 Authentification JWT

```python
import jwt

token = jwt.encode({"user": "Chris"}, "secret", algorithm="HS256")

print(token)
```

---

# 3. Sécurité des fichiers

---

# Mauvais

```python
open("/etc/passwd")
```

---

# Bon

```python
with open("data.txt", "r") as file:
    print(file.read())
```

---

# 4. Gestion des permissions

---

```python
import os

if os.access("file.txt", os.R_OK):
    print("Readable file")
```

---

# 5. Sécurité des dépendances

---

# Bonnes pratiques

- utiliser requirements.txt
- éviter packages inconnus
- scanner vulnérabilités

```bash
pip install safety
safety check
```

---

# 6. Logging sécurité

---

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.warning("Unauthorized access attempt")
```

---

# 7. Déploiement en Python

---

# 7.1 Qu’est-ce que le déploiement ?

Le déploiement consiste à rendre une application accessible en ligne.

---

# 7.2 Modes de déploiement

| Type | Description |
|---|---|
| Local | Machine personnelle |
| VPS | Serveur privé |
| Cloud | AWS, Azure, GCP |
| Container | Docker |

---

# 8. Déploiement avec Flask

---

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Deployed App"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

# 9. Déploiement avec Gunicorn

---

```bash
gunicorn app:app
```

---

# 10. Docker (standard professionnel)

---

# Dockerfile

```dockerfile
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
```

---

# Build & Run

```bash
docker build -t myapp .
docker run -p 5000:5000 myapp
```

---

# 11. CI/CD (Automation déploiement)

---

# Pipeline

1. push code
2. run tests
3. build app
4. deploy

---

# Exemple GitHub Actions

```yaml
name: Python CI

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python -m unittest
```

---

# 12. Serveurs de production

---

# Outils

- Nginx
- Gunicorn
- Uvicorn (FastAPI)

---

# Exemple FastAPI production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

# 13. Monitoring

---

# Objectif

Surveiller l’application en production.

---

# Outils

- Prometheus
- Grafana
- Sentry

---

# Exemple logging avancé

```python
import logging

logging.error("Server crash detected")
```

---

# 14. Backup & Recovery

---

# Exemple simple

```python
import shutil

shutil.copy("db.sqlite", "backup/db_backup.sqlite")
```

---

# 15. Scaling (mise à l’échelle)

---

# Techniques

- load balancing
- horizontal scaling
- caching
- microservices

---

# 16. Sécurité en production

---

# Règles importantes

- HTTPS obligatoire
- variables d’environnement
- firewall actif
- logs surveillés
- accès restreint
- pas de secrets dans le code

---

# 17. Erreurs fréquentes

- exposer API keys
- utiliser eval()
- mauvais stockage passwords
- absence de HTTPS
- dépendances non mises à jour

---

# Points Clés

- La sécurité est obligatoire en production.
- Toujours valider les entrées utilisateur.
- Jamais de secrets dans le code.
- Utiliser hash pour mots de passe.
- Docker est standard moderne.
- CI/CD automatise les déploiements.
- Monitoring évite les pannes silencieuses.
- Scaling permet de supporter plus d’utilisateurs.

---

# Exercice

## Énoncé

Créer :
1. une API Flask simple,
2. sécuriser une entrée utilisateur,
3. afficher un message protégé.

---

# Correction

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/hello")
def hello():
    name = request.args.get("name")

    if not name:
        return "Missing name"

    if not name.isalpha():
        return "Invalid input"

    return f"Hello {name}"

if __name__ == "__main__":
    app.run()
```