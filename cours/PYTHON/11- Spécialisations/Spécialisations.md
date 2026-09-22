# Spécialisations en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

Les spécialisations en Python représentent les domaines professionnels où Python est utilisé de manière avancée et ciblée.

À ce niveau, Python n’est plus seulement un langage d’apprentissage, mais un outil de production utilisé dans :
- les entreprises technologiques,
- les systèmes industriels,
- la recherche,
- la finance,
- la cybersécurité,
- l’intelligence artificielle.

Chaque spécialisation utilise Python avec des bibliothèques, architectures et méthodes différentes.

---

# 1. Développement Web (Backend)

---

# Définition

Le développement web backend consiste à créer la logique serveur d’une application web.

---

# Frameworks principaux

- Django
- Flask
- FastAPI

---

# Exemple Flask

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

if __name__ == "__main__":
    app.run()
```

---

# Exemple FastAPI

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
```

---

# Utilisations

- API REST
- applications web
- systèmes SaaS
- microservices

---

# 2. Data Science

---

# Définition

La data science consiste à analyser et exploiter des données.

---

# Bibliothèques principales

- NumPy
- Pandas
- Matplotlib
- Seaborn

---

# Exemple Pandas

```python
import pandas as pd

data = {
    "name": ["Chris", "John"],
    "age": [20, 25]
}

df = pd.DataFrame(data)

print(df)
```

---

# Utilisations

- analyse de données
- visualisation
- statistiques
- business intelligence

---

# 3. Intelligence Artificielle (AI / ML)

---

# Définition

L’IA consiste à créer des systèmes capables d’apprendre et de prendre des décisions.

---

# Bibliothèques

- TensorFlow
- PyTorch
- Scikit-learn

---

# Exemple simple ML

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()

X = [[1], [2], [3]]
y = [2, 4, 6]

model.fit(X, y)

print(model.predict([[4]]))
```

---

# Utilisations

- reconnaissance d’image
- prédiction
- NLP (chatbots)
- recommandations

---

# 4. Cybersécurité

---

# Définition

Python est utilisé pour analyser, tester et sécuriser les systèmes.

---

# Bibliothèques

- socket
- scapy
- hashlib
- requests

---

# Exemple hash

```python
import hashlib

password = "secret"

hashed = hashlib.sha256(password.encode()).hexdigest()

print(hashed)
```

---

# Utilisations

- analyse réseau
- pentesting
- scripts de sécurité
- automation sécurité

---

# 5. Automatisation (Scripting)

---

# Définition

Automatiser des tâches répétitives avec Python.

---

# Exemple

```python
import os

files = os.listdir(".")

for file in files:
    print(file)
```

---

# Utilisations

- gestion fichiers
- scripts système
- bots
- automatisation bureautique

---

# 6. DevOps & Cloud

---

# Définition

Utilisation de Python pour gérer infrastructure et serveurs.

---

# Outils

- Docker
- Kubernetes
- AWS SDK (boto3)

---

# Exemple AWS (simplifié)

```python
import boto3

s3 = boto3.client("s3")

buckets = s3.list_buckets()

print(buckets)
```

---

# Utilisations

- cloud computing
- déploiement automatique
- infrastructure as code

---

# 7. Développement de Jeux Vidéo

---

# Bibliothèque principale

- Pygame

---

# Exemple simple

```python
import pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
```

---

# Utilisations

- jeux 2D
- prototypes
- simulations

---

# 8. Finance & Trading

---

# Définition

Python est utilisé pour analyser les marchés financiers.

---

# Bibliothèques

- pandas
- numpy
- yfinance

---

# Exemple

```python
import yfinance as yf

data = yf.download("AAPL", start="2024-01-01")

print(data.head())
```

---

# Utilisations

- trading algorithmique
- analyse de marché
- prédictions financières

---

# 9. Web Scraping

---

# Définition

Extraire des données depuis des sites web.

---

# Bibliothèques

- BeautifulSoup
- requests
- scrapy

---

# Exemple

```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title.text)
```

---

# Utilisations

- collecte de données
- comparaison de prix
- analyse web

---

# 10. Robotique & IoT

---

# Définition

Python contrôle des appareils physiques.

---

# Exemple conceptuel

```python
def move_robot():
    print("Robot moving forward")
```

---

# Utilisations

- Raspberry Pi
- capteurs
- automation industrielle

---

# 11. NLP (Natural Language Processing)

---

# Définition

Traitement du langage humain.

---

# Bibliothèques

- NLTK
- spaCy
- transformers

---

# Exemple simple

```python
text = "Hello world"

words = text.split()

print(words)
```

---

# Utilisations

- chatbots
- analyse de texte
- traduction automatique

---

# 12. Big Data

---

# Définition

Traitement de très grandes quantités de données.

---

# Outils

- PySpark
- Hadoop

---

# Exemple PySpark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("App").getOrCreate()

df = spark.createDataFrame([(1, "Chris")], ["id", "name"])

df.show()
```

---

# 13. Backend API avancée (architecture moderne)

---

# Exemple structure

```text
app/
├── main.py
├── routes/
├── services/
├── models/
└── database/
```

---

# 14. Architecture logicielle

---

# Concepts

- MVC (Model View Controller)
- Microservices
- Clean Architecture

---

# Exemple logique

```python
class Service:
    def process(self):
        return "Processing data"
```

---

# 15. Performance Engineering

---

# Techniques

- caching
- async programming
- multiprocessing
- optimisation mémoire

---

# Exemple cache

```python
from functools import lru_cache

@lru_cache
def compute(x):
    return x * x
```

---

# 16. Bonnes pratiques professionnelles

- choisir une spécialisation claire
- maîtriser les bibliothèques associées
- comprendre les architectures
- écrire du code testable
- utiliser Git systématiquement

---

# Points Clés

- Python est utilisé dans plusieurs industries.
- Chaque spécialisation a ses propres outils.
- Web → APIs et serveurs.
- Data Science → analyse de données.
- AI → apprentissage automatique.
- Cybersecurity → sécurité et scripts.
- Automation → gain de temps.
- DevOps → infrastructure cloud.
- Game dev → jeux vidéo.
- Scraping → extraction de données.
- NLP → langage humain.

---

# Exercice

## Énoncé

Choisir une spécialisation et :
1. écrire un petit exemple Python,
2. expliquer son utilisation.

---

# Correction (exemple AI)

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()

X = [[1], [2], [3]]
y = [2, 4, 6]

model.fit(X, y)

print(model.predict([[5]]))
```