# Concepts Avancés du Langage Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

Les concepts avancés du langage Python représentent le cœur profond du fonctionnement du langage lui-même.

Ils expliquent :
- comment Python exécute le code,
- comment les objets fonctionnent en mémoire,
- comment le langage est construit,
- comment optimiser et comprendre Python en profondeur.

Ces concepts sont essentiels pour :
- devenir développeur senior,
- comprendre les frameworks internes,
- optimiser les performances,
- écrire du code propre et robuste.

---

# 1. Le Modèle d’Exécution Python

---

# Définition

Python exécute le code ligne par ligne via un interpréteur.

---

# Étapes internes

1. Compilation en bytecode
2. Exécution par la Python Virtual Machine (PVM)

---

# Exemple simple

```python
x = 10
y = 20
print(x + y)
```

---

# Ce qui se passe en interne

- Python transforme le code en bytecode
- La PVM exécute ce bytecode

---

# Importance

Comprendre cela aide à :
- optimiser le code
- comprendre les performances
- éviter les erreurs de design

---

# 2. Tout est un Objet

---

# Définition

En Python, TOUT est un objet :
- nombres
- fonctions
- classes
- modules

---

# Exemple

```python
x = 10

print(type(x))
print(type(print))
```

---

# Résultat conceptuel

- int est une classe
- print est une fonction objet

---

# 3. Références et Mémoire

---

# Définition

Les variables ne contiennent pas des valeurs, mais des références.

---

# Exemple

```python
a = [1, 2, 3]
b = a

b.append(4)

print(a)
```

---

# Explication

- a et b pointent vers le même objet mémoire

---

# Vérification mémoire

```python
print(id(a))
print(id(b))
```

---

# 4. Mutabilité vs Immutabilité

---

# Mutables

Peuvent être modifiés :

```python
list, dict, set
```

---

# Exemple

```python
a = [1, 2, 3]
a.append(4)
```

---

# Immutables

Ne peuvent pas être modifiés :

```python
int, str, tuple
```

---

# Exemple

```python
x = "hello"
x = x + " world"
```

---

# 5. Garbage Collection

---

# Définition

Python libère automatiquement la mémoire inutilisée.

---

# Exemple conceptuel

```python
a = [1, 2, 3]
a = None
```

---

# Résultat

L’ancien objet devient éligible à la suppression.

---

# 6. Namespace et Scope avancé

---

# Types de scope

| Type | Description |
|---|---|
| Local | Dans une fonction |
| Enclosing | Fonction englobante |
| Global | Niveau module |
| Built-in | Python natif |

---

# Exemple LEGB

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)

    inner()

outer()
```

---

# 7. Closures (niveau profond)

---

# Exemple

```python
def outer(msg):

    def inner():
        print(msg)

    return inner

func = outer("Hello")
func()
```

---

# Pourquoi c’est important

- callbacks
- decorators
- encapsulation fonctionnelle

---

# 8. Decorators (avancé interne)

---

# Exemple

```python
def decorator(func):

    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result

    return wrapper

@decorator
def add(a, b):
    return a + b

print(add(2, 3))
```

---

# 9. Descriptors

---

# Définition

Les descriptors contrôlent l’accès aux attributs.

---

# Exemple

```python
class Descriptor:
    def __get__(self, instance, owner):
        return "Accessed"

class MyClass:
    attr = Descriptor()

obj = MyClass()

print(obj.attr)
```

---

# Utilisation

- ORM (Django)
- validation d’attributs

---

# 10. Méthodes Magiques (Dunder Internals)

---

# Exemple

```python
class User:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User({self.name})"

u = User("Chris")

print(u)
```

---

# Autres méthodes

| Méthode | Rôle |
|---|---|
| __init__ | constructeur |
| __str__ | affichage utilisateur |
| __repr__ | debug |
| __len__ | longueur |
| __call__ | rendre objet appelable |

---

# Exemple __call__

```python
class Greeter:
    def __call__(self, name):
        return "Hello " + name

g = Greeter()

print(g("Chris"))
```

---

# 11. MRO (Method Resolution Order)

---

# Définition

Détermine l’ordre d’héritage des classes.

---

# Exemple

```python
class A:
    pass

class B(A):
    pass

print(B.mro())
```

---

# 12. Multiple Inheritance

---

# Exemple

```python
class A:
    def show(self):
        print("A")

class B:
    def show(self):
        print("B")

class C(A, B):
    pass

obj = C()
obj.show()
```

---

# 13. Duck Typing

---

# Définition

Si ça ressemble à un canard, c’est un canard.

---

# Exemple

```python
class Dog:
    def speak(self):
        print("Bark")

class Robot:
    def speak(self):
        print("Beep")

def make_speak(entity):
    entity.speak()

make_speak(Dog())
make_speak(Robot())
```

---

# 14. Introspection

---

# Exemple

```python
print(dir(str))
print(type(10))
print(hasattr("hello", "upper"))
```

---

# 15. Metaclasses

---

# Définition

Une metaclass contrôle la création des classes.

---

# Exemple simple

```python
class Meta(type):
    pass

class MyClass(metaclass=Meta):
    pass
```

---

# Utilisation

- frameworks (Django ORM)
- validation automatique
- génération dynamique de classes

---

# 16. Compilation vs Interprétation

---

# Python est :

- interprété
- mais compilé en bytecode

---

# Résumé

| Étape | Rôle |
|---|---|
| Code Python | écrit par développeur |
| Bytecode | version intermédiaire |
| PVM | exécution |

---

# 17. Performance interne

---

# Optimisations Python

- caching
- interning strings
- memory pooling
- lazy evaluation

---

# Exemple string interning

```python
a = "hello"
b = "hello"

print(a is b)
```

---

# 18. Global Interpreter Lock (GIL)

---

# Définition

Le GIL limite l’exécution simultanée des threads Python.

---

# Impact

- threads limités pour CPU
- multiprocessing recommandé

---

# 19. Eval & Exec (dangereux)

---

# Exemple

```python
code = "print(10 + 5)"

exec(code)
```

---

# ⚠️ Risque

- sécurité
- injection de code

---

# 20. Functional Internals

---

# map

```python
numbers = map(lambda x: x * 2, [1, 2, 3])
print(list(numbers))
```

---

# filter

```python
numbers = filter(lambda x: x > 1, [1, 2, 3])
print(list(numbers))
```

---

# reduce

```python
from functools import reduce

result = reduce(lambda a, b: a + b, [1, 2, 3])
print(result)
```

---

# 21. Optimisation avancée

---

# Bonnes pratiques

- éviter exec/eval
- utiliser generators
- préférer built-ins
- réduire complexité O(n)
- éviter copies inutiles

---

# 22. Erreurs fréquentes

- mauvaise gestion mémoire
- abus de metaclasses
- confusion scope LEGB
- mauvaise compréhension références
- surutilisation decorators

---

# Points Clés

- Python est un langage objet profond.
- Tout est objet et référence.
- La mémoire est gérée automatiquement.
- LEGB définit le scope.
- Les decorators modifient les fonctions.
- Les metaclasses contrôlent les classes.
- Duck typing rend Python flexible.
- GIL limite le multithreading CPU.

---

# Exercice

## Énoncé

Créer :
1. une classe avec __call__,
2. un decorator,
3. une fonction décorée,
4. exécuter le tout.

---

# Correction

```python
def decorator(func):

    def wrapper(*args, **kwargs):
        print("Start")
        result = func(*args, **kwargs)
        print("End")
        return result

    return wrapper


class Greeter:
    def __call__(self, name):
        return "Hello " + name


@decorator
def greet(name):
    return "Hi " + name


g = Greeter()

print(g("Chris"))
print(greet("Chris"))
```