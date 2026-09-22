# Architecture & Bonnes Pratiques en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

L’architecture logicielle et les bonnes pratiques représentent le niveau professionnel de Python.

À ce stade, on ne parle plus seulement de “code qui fonctionne”, mais de :
- code maintenable,
- code scalable,
- code testable,
- code sécurisé,
- code utilisé en production.

Ces concepts sont essentiels pour :
- travailler en entreprise,
- construire des applications réelles,
- collaborer en équipe,
- éviter les dettes techniques,
- faire évoluer un projet sur le long terme.

---

# 1. Qu’est-ce que l’architecture logicielle ?

---

# Définition

L’architecture logicielle est la manière dont un projet est structuré et organisé.

---

# Objectif

Créer un système :
- clair,
- modulaire,
- évolutif,
- facile à maintenir.

---

# Exemple de mauvaise architecture

```text
project/
│
├── main.py
├── everything.py
```

❌ Problèmes :
- tout est mélangé
- impossible à maintenir
- difficile à tester

---

# Exemple de bonne architecture

```text
project/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── utils/
│
├── tests/
├── config/
├── requirements.txt
└── README.md
```

---

# 2. Séparation des responsabilités (Separation of Concerns)

---

# Définition

Chaque partie du code doit avoir un rôle précis.

---

# Exemple

| Couche | Rôle |
|---|---|
| Routes | Gestion des requêtes |
| Services | Logique métier |
| Models | Structure des données |
| Utils | Fonctions utilitaires |

---

# Exemple concret

```python
# service.py
def calculate_price(price):
    return price * 1.2
```

```python
# main.py
from service import calculate_price

print(calculate_price(100))
```

---

# 3. Clean Code

---

# Définition

Le clean code est un style de code :
- lisible,
- simple,
- compréhensible par tous.

---

# Mauvais exemple

```python
def a(x,y):return x+y*2
```

---

# Bon exemple

```python
def calculate_total_price(price, tax_rate):
    return price + (price * tax_rate)
```

---

# Principes Clean Code

- noms clairs
- fonctions courtes
- une fonction = une tâche
- pas de duplication
- code lisible sans commentaire

---

# 4. SOLID Principles

---

# S — Single Responsibility Principle

Une classe = une responsabilité

```python
class ReportGenerator:
    def generate(self):
        pass
```

---

# O — Open/Closed Principle

Ouvert à l’extension, fermé à la modification

```python
class Shape:
    def area(self):
        pass
```

---

# L — Liskov Substitution Principle

Une classe enfant doit remplacer la classe parent

---

# I — Interface Segregation Principle

Ne pas forcer des méthodes inutiles

---

# D — Dependency Inversion Principle

Dépendre des abstractions, pas des implémentations

---

# 5. Design Patterns

---

# Singleton

Une seule instance

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

# Factory

Créer des objets dynamiquement

```python
class Dog:
    def speak(self):
        return "Bark"

class Cat:
    def speak(self):
        return "Meow"

def animal_factory(animal):
    if animal == "dog":
        return Dog()
    if animal == "cat":
        return Cat()
```

---

# Strategy Pattern

Changer le comportement dynamiquement

```python
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def execute(func, a, b):
    return func(a, b)
```

---

# 6. Modularisation avancée

---

# Structure pro

```text
app/
│
├── controllers/
├── services/
├── repositories/
├── models/
├── utils/
└── core/
```

---

# Exemple service layer

```python
class UserService:
    def get_user(self, user_id):
        return {"id": user_id, "name": "Chris"}
```

---

# 7. Couplage faible & Cohésion forte

---

# Définition

- Couplage faible = modules indépendants
- Cohésion forte = un module bien spécialisé

---

# Mauvais exemple

```python
class A:
    def do_everything(self):
        pass
```

---

# Bon exemple

```python
class AuthService:
    def login(self):
        pass

class PaymentService:
    def pay(self):
        pass
```

---

# 8. Dependency Injection

---

# Définition

Injecter les dépendances au lieu de les créer directement.

---

# Exemple

```python
class Database:
    def connect(self):
        return "Connected"

class Service:
    def __init__(self, db):
        self.db = db

db = Database()
service = Service(db)

print(service.db.connect())
```

---

# 9. Configuration propre

---

# Mauvais

```python
API_KEY = "123456"
```

---

# Bon

```python
import os

API_KEY = os.getenv("API_KEY")
```

---

# 10. Logging professionnel

---

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Application started")
logging.error("Error occurred")
```

---

# 11. Gestion des erreurs propre

---

```python
class AppError(Exception):
    pass

def divide(a, b):
    if b == 0:
        raise AppError("Division by zero")
    return a / b
```

---

# 12. Testing architecture

---

```python
def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5
```

---

# 13. Scalabilité

---

# Techniques

- architecture modulaire
- microservices
- caching
- async programming
- load balancing

---

# 14. Performance & optimisation

---

# Bonnes pratiques

- éviter calculs inutiles
- utiliser cache
- utiliser generators
- minimiser accès disque
- optimiser requêtes

---

# 15. Sécurité architecture

---

# Règles

- valider les inputs
- éviter exec/eval
- protéger API keys
- limiter accès base de données
- utiliser HTTPS

---

# 16. Code review

---

# Objectif

Améliorer le code grâce à :
- relecture
- feedback
- standards

---

# 17. Documentation

---

# Exemple README

```md
# Project

## Installation
pip install -r requirements.txt

## Run
python main.py
```

---

# 18. CI/CD (introduction)

---

# Définition

Automatisation du test et du déploiement.

---

# Étapes

- commit
- test
- build
- deploy

---

# 19. Anti-patterns

---

# Mauvais pratiques

- god object (classe qui fait tout)
- code dupliqué
- dépendances fortes
- absence de tests
- fichiers énormes

---

# Points Clés

- Une bonne architecture est essentielle en production.
- Clean code améliore la lisibilité.
- SOLID guide la conception.
- Dependency Injection rend le code flexible.
- Modularité = scalabilité.
- Logging + tests = stabilité.
- Sécurité doit être intégrée dès le début.

---

# Exercice

## Énoncé

Créer une mini architecture :
1. service utilisateur,
2. injection de dépendance,
3. fonction principale propre.

---

# Correction

```python
class UserService:
    def get_user(self):
        return {"name": "Chris"}


class App:
    def __init__(self, service):
        self.service = service

    def run(self):
        user = self.service.get_user()
        print(user)


service = UserService()
app = App(service)

app.run()
```