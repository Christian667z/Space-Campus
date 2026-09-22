# Fonctionnalités Python Avancées

**Difficulté :** ★★★★★★★★★★

---

# Introduction

Python possède de nombreuses fonctionnalités avancées qui rendent le langage :
- puissant,
- flexible,
- moderne,
- professionnel.

Ces fonctionnalités sont utilisées dans :
- les frameworks modernes,
- l’intelligence artificielle,
- les systèmes distribués,
- les APIs,
- les outils DevOps,
- les bibliothèques professionnelles.

Maîtriser ces concepts permet :
- d’écrire du code plus propre,
- plus rapide,
- plus maintenable,
- plus professionnel.

---

# 1. Iterators (Itérateurs)

---

# Définition

Un itérateur est un objet capable de parcourir des données une par une.

---

# Exemple

```python
numbers = [1, 2, 3]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

---

# Fonctionnement

- `iter()` crée un itérateur
- `next()` récupère la prochaine valeur

---

# StopIteration

Quand il n’y a plus de données :

```python
StopIteration
```

---

# Utilité des itérateurs

- économie mémoire
- traitement progressif
- gros volumes de données

---

# 2. Generators

---

# Définition

Un générateur produit des données à la demande grâce à `yield`.

---

# Exemple simple

```python
def generate_numbers():
    for i in range(5):
        yield i

for number in generate_numbers():
    print(number)
```

---

# Différence avec return

| return | yield |
|---|---|
| termine la fonction | suspend la fonction |
| une seule valeur | plusieurs valeurs progressives |

---

# Avantages des generators

- faible consommation mémoire
- traitement efficace
- idéal pour gros fichiers

---

# Generator Expression

```python
numbers = (x * 2 for x in range(5))

print(list(numbers))
```

---

# 3. Decorators

---

# Définition

Un decorator modifie le comportement d’une fonction sans modifier son code.

---

# Exemple simple

```python
def decorator(func):

    def wrapper():
        print("Before function")
        func()
        print("After function")

    return wrapper

@decorator
def hello():
    print("Hello")

hello()
```

---

# Utilisations réelles

Les decorators sont utilisés pour :
- authentification,
- logging,
- permissions,
- cache,
- timing,
- validation.

---

# Decorator avec paramètres

```python
def repeat(func):

    def wrapper():
        func()
        func()

    return wrapper

@repeat
def greet():
    print("Hello")

greet()
```

---

# 4. Closures

---

# Définition

Une closure est une fonction interne qui garde accès aux variables externes.

---

# Exemple

```python
def outer(message):

    def inner():
        print(message)

    return inner

func = outer("Hello")
func()
```

---

# Utilité

- encapsulation
- callbacks
- programmation fonctionnelle

---

# 5. Higher-Order Functions

---

# Définition

Une fonction de haut niveau :
- reçoit une fonction,
- ou retourne une fonction.

---

# Exemple

```python
def operate(func, value):
    return func(value)

def square(x):
    return x * x

print(operate(square, 5))
```

---

# 6. Lambda Functions

---

# Définition

Fonction anonyme courte.

---

# Exemple

```python
square = lambda x: x * x

print(square(5))
```

---

# Utilisation fréquente

- map
- filter
- sorting
- callbacks

---

# 7. Comprehensions avancées

---

# List Comprehension

```python
numbers = [x * 2 for x in range(10)]
```

---

# Nested comprehension

```python
matrix = [[i * j for j in range(3)] for i in range(3)]

print(matrix)
```

---

# Set Comprehension

```python
numbers = {x for x in range(5)}

print(numbers)
```

---

# Dictionary Comprehension

```python
squares = {x: x * x for x in range(5)}

print(squares)
```

---

# 8. unpacking (déballage)

---

# Liste

```python
numbers = [1, 2, 3]

a, b, c = numbers

print(a)
```

---

# Avec *

```python
numbers = [1, 2, 3, 4, 5]

a, *rest = numbers

print(rest)
```

---

# Dictionary unpacking

```python
user = {"name": "Chris"}
details = {"age": 20}

data = {**user, **details}

print(data)
```

---

# 9. args et kwargs

---

# *args

Permet plusieurs arguments positionnels.

---

# Exemple

```python
def total(*numbers):
    return sum(numbers)

print(total(1, 2, 3))
```

---

# **kwargs

Permet plusieurs arguments nommés.

---

# Exemple

```python
def show_user(**data):
    print(data)

show_user(name="Chris", age=20)
```

---

# 10. Typing (Type Hinting)

---

# Définition

Le type hinting améliore :
- la lisibilité,
- les IDE,
- la maintenance.

---

# Exemple

```python
def add(a: int, b: int) -> int:
    return a + b
```

---

# Liste typée

```python
from typing import List

numbers: List[int] = [1, 2, 3]
```

---

# 11. Dataclasses

---

# Définition

Simplifie la création de classes de données.

---

# Exemple

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

user = User("Chris", 20)

print(user)
```

---

# Avantages

- moins de code
- plus lisible
- automatique

---

# 12. Context Managers

---

# Définition

Gèrent automatiquement les ressources.

---

# Exemple

```python
with open("file.txt", "r") as file:
    content = file.read()
```

---

# Pourquoi utiliser with ?

- fermeture automatique
- sécurité
- gestion mémoire

---

# 13. Async & Await

---

# Définition

Permet la programmation asynchrone.

---

# Exemple

```python
import asyncio

async def task():
    print("Start")
    await asyncio.sleep(1)
    print("End")

asyncio.run(task())
```

---

# Utilité

- APIs
- serveurs
- réseau
- applications temps réel

---

# 14. Threading

---

# Exemple

```python
import threading

def run_task():
    print("Task running")

thread = threading.Thread(target=run_task)

thread.start()
```

---

# 15. Multiprocessing

---

# Définition

Utilise plusieurs processus CPU.

---

# Exemple

```python
from multiprocessing import Process

def task():
    print("Running")

p = Process(target=task)

p.start()
p.join()
```

---

# Différence Thread vs Process

| Thread | Process |
|---|---|
| mémoire partagée | mémoire séparée |
| plus léger | plus puissant |
| I/O | CPU intensive |

---

# 16. Metaprogramming

---

# Définition

Le programme modifie du code dynamiquement.

---

# Exemple avec getattr

```python
class User:
    name = "Chris"

user = User()

print(getattr(user, "name"))
```

---

# setattr

```python
setattr(user, "age", 20)

print(user.age)
```

---

# 17. Magic Methods (Dunder Methods)

---

# Définition

Méthodes spéciales commençant par `__`.

---

# Exemple

```python
class User:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

user = User("Chris")

print(user)
```

---

# Méthodes importantes

| Méthode | Rôle |
|---|---|
| `__init__` | constructeur |
| `__str__` | affichage |
| `__len__` | longueur |
| `__add__` | addition |
| `__getitem__` | accès index |

---

# 18. Caching

---

# Exemple avec lru_cache

```python
from functools import lru_cache

@lru_cache
def fibonacci(n):

    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(30))
```

---

# 19. Serialization

---

# JSON

```python
import json

user = {"name": "Chris"}

data = json.dumps(user)

print(data)
```

---

# Pickle

```python
import pickle

data = pickle.dumps(user)
```

---

# 20. Reflection & Introspection

---

# Exemple

```python
print(type(10))
print(dir(str))
```

---

# hasattr

```python
print(hasattr(user, "name"))
```

---

# 21. Bonnes pratiques avancées

- utiliser generators pour gros volumes
- éviter les decorators inutiles
- typer le code
- utiliser dataclass pour données simples
- éviter le code trop complexe

---

# 22. Erreurs fréquentes

- confusion async/threading
- abus de lambda
- decorators mal écrits
- mauvaise gestion mémoire
- comprehension illisible

---

# Applications Réelles

Ces fonctionnalités sont utilisées dans :
- Django
- Flask
- FastAPI
- TensorFlow
- PyTorch
- systèmes cloud
- microservices
- IA moderne

---

# Points Clés

- Les generators économisent la mémoire.
- Les decorators modifient les fonctions.
- Lambda simplifie les petites fonctions.
- Async améliore la concurrence.
- Dataclass simplifie les objets.
- Type hinting améliore la qualité du code.
- Context managers gèrent les ressources.
- Metaprogramming rend Python très flexible.

---

# Exercice

## Énoncé

Créer :
1. une dataclass `Product`,
2. un generator qui génère plusieurs produits,
3. afficher tous les produits.

---

# Correction

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: int

def generate_products():

    products = [
        Product("Laptop", 1000),
        Product("Phone", 500)
    ]

    for product in products:
        yield product

for item in generate_products():
    print(item)
```