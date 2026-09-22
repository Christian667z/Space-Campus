# Concepts Avancés en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

Les concepts avancés en Python permettent de passer d’un niveau débutant/intermédiaire à un niveau professionnel.

Ils sont essentiels pour :
- développer des applications complexes,
- travailler en entreprise,
- créer des systèmes performants,
- comprendre les frameworks modernes,
- maîtriser l’architecture logicielle.

---

# 1. Programmation Orientée Objet (POO)

---

# Définition

La POO est un paradigme de programmation basé sur des **objets** et des **classes**.

Un objet contient :
- des données (attributs),
- des comportements (méthodes).

---

# Classe et Objet

## Exemple

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("Hello", self.name)

user1 = User("Chris", 20)
user1.greet()
```

---

# Concepts importants

- Classe = modèle
- Objet = instance
- self = référence à l’objet

---

# 2. Encapsulation

---

# Définition

L’encapsulation consiste à protéger les données internes d’une classe.

---

# Exemple

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
print(account.get_balance())
```

---

# 3. Héritage

---

# Définition

L’héritage permet à une classe de reprendre les propriétés d’une autre.

---

# Exemple

```python
class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def bark(self):
        print("Bark")

dog = Dog()
dog.speak()
dog.bark()
```

---

# 4. Polymorphisme

---

# Définition

Le polymorphisme permet d’utiliser une même méthode de différentes façons.

---

# Exemple

```python
class Cat:
    def speak(self):
        print("Meow")

class Dog:
    def speak(self):
        print("Bark")

animals = [Cat(), Dog()]

for animal in animals:
    animal.speak()
```

---

# 5. Fonctions avancées

---

# Lambda (fonctions anonymes)

```python
square = lambda x: x * x

print(square(5))
```

---

# Map

```python
numbers = [1, 2, 3]

result = list(map(lambda x: x * 2, numbers))

print(result)
```

---

# Filter

```python
numbers = [1, 2, 3, 4, 5]

result = list(filter(lambda x: x % 2 == 0, numbers))

print(result)
```

---

# Reduce

```python
from functools import reduce

numbers = [1, 2, 3, 4]

result = reduce(lambda x, y: x + y, numbers)

print(result)
```

---

# 6. Compréhensions (Comprehensions)

---

# List Comprehension

```python
numbers = [x for x in range(10)]

print(numbers)
```

---

# Condition dans comprehension

```python
even_numbers = [x for x in range(10) if x % 2 == 0]

print(even_numbers)
```

---

# Dictionary Comprehension

```python
squares = {x: x * x for x in range(5)}

print(squares)
```

---

# 7. Gestion des Exceptions Avancée

---

# Plusieurs exceptions

```python
try:
    x = 10 / 0

except ZeroDivisionError:
    print("Cannot divide by zero")

except Exception as e:
    print("Error:", e)
```

---

# finally

```python
try:
    print("Running")

finally:
    print("Always executed")
```

---

# 8. Modules et Packages avancés

---

# Package structure

```text
project/
│
├── main.py
├── utils/
│   ├── __init__.py
│   ├── math_tools.py
│   └── string_tools.py
```

---

# Import package

```python
from utils import math_tools
```

---

# 9. Gestion de fichiers avancée

---

# Lecture fichier

```python
with open("file.txt", "r") as file:
    content = file.read()

print(content)
```

---

# Écriture fichier

```python
with open("file.txt", "w") as file:
    file.write("Hello World")
```

---

# Ajout (append)

```python
with open("file.txt", "a") as file:
    file.write("\nNew line")
```

---

# 10. Gestion mémoire et performance

---

# Générateurs

```python
def generate_numbers():
    for i in range(5):
        yield i

for num in generate_numbers():
    print(num)
```

---

# Pourquoi utiliser yield ?

- économie de mémoire
- génération à la demande
- performance améliorée

---

# 11. Decorators

---

# Définition

Un decorator modifie le comportement d’une fonction.

---

# Exemple

```python
def decorator(func):
    def wrapper():
        print("Before function")
        func()
        print("After function")
    return wrapper

@decorator
def say_hello():
    print("Hello")

say_hello()
```

---

# 12. Context Managers

---

# Définition

Permet de gérer automatiquement les ressources.

---

# Exemple

```python
with open("file.txt", "r") as file:
    content = file.read()
```

---

# 13. Async Programming

---

# Définition

Permet d’exécuter plusieurs tâches en parallèle.

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

# 14. Threads et Concurrence

---

# Exemple simple

```python
import threading

def task():
    print("Running task")

thread = threading.Thread(target=task)
thread.start()
```

---

# 15. Gestion avancée des erreurs

---

```python
class CustomError(Exception):
    pass

raise CustomError("Something went wrong")
```

---

# 16. Concepts de performance

- éviter les boucles inutiles
- utiliser list comprehension
- utiliser generators
- éviter les copies inutiles
- utiliser les modules optimisés

---

# 17. Bonnes pratiques avancées

- écrire du code modulaire
- utiliser des classes propres
- éviter le code dupliqué
- respecter PEP8
- écrire des fonctions courtes
- commenter intelligemment

---

# 18. Erreurs fréquentes avancées

- mauvaise utilisation des decorators
- mauvaise gestion des threads
- confusion async/await
- abus des global variables
- mauvaise structure de projet

---

# Points Clés

- La POO structure les programmes.
- L’héritage réutilise le code.
- Le polymorphisme rend le code flexible.
- Les lambda simplifient les fonctions.
- Les comprehensions rendent le code plus rapide.
- Les generators optimisent la mémoire.
- Les decorators modifient les fonctions.
- Async améliore les performances.
- Les context managers gèrent les ressources.

---

# Exercice

## Énoncé

Créer :
1. une classe `Product`,
2. une méthode pour afficher le produit,
3. une liste de produits,
4. afficher tous les produits avec une boucle.

---

# Correction

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def display(self):
        print(self.name, "-", self.price)

products = [
    Product("Laptop", 1000),
    Product("Phone", 500)
]

for product in products:
    product.display()
```