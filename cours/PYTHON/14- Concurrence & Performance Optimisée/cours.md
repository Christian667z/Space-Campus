# Concurrence & Performance Optimisée en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

La concurrence et l’optimisation des performances sont des concepts essentiels en Python avancé.

Ils permettent de :
- exécuter plusieurs tâches en même temps,
- améliorer la vitesse des programmes,
- gérer des systèmes lourds,
- optimiser les ressources CPU et mémoire,
- construire des applications scalables.

Ces concepts sont utilisés dans :
- les serveurs web,
- les APIs,
- les systèmes cloud,
- l’intelligence artificielle,
- le traitement de données,
- les applications temps réel.

---

# 1. Concurrence vs Parallélisme

---

# Définition

| Concept | Description |
|---|---|
| Concurrence | Gérer plusieurs tâches en alternance |
| Parallélisme | Exécuter plusieurs tâches en même temps |

---

# Exemple simple

- Concurrence = multitâche logique
- Parallélisme = multitâche réel (CPU multiple)

---

# 2. Threading (Multithreading)

---

# Définition

Le threading permet d’exécuter plusieurs threads dans un même processus.

---

# Exemple basique

```python
import threading
import time

def task():
    print("Task started")
    time.sleep(2)
    print("Task finished")

thread1 = threading.Thread(target=task)
thread2 = threading.Thread(target=task)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
```

---

# Avantages

- utile pour tâches I/O (réseau, fichiers)
- améliore réactivité
- exécution simultanée logique

---

# Limite importante

👉 GIL (Global Interpreter Lock) limite les performances CPU.

---

# 3. Multiprocessing

---

# Définition

Le multiprocessing exécute plusieurs processus indépendants.

---

# Exemple

```python
from multiprocessing import Process

def task():
    print("Processing task")

process1 = Process(target=task)
process2 = Process(target=task)

process1.start()
process2.start()

process1.join()
process2.join()
```

---

# Avantages

- utilise plusieurs cœurs CPU
- idéal pour calculs lourds
- contourne le GIL

---

# Comparaison Thread vs Process

| Thread | Process |
|---|---|
| léger | lourd |
| partage mémoire | mémoire séparée |
| bon pour I/O | bon pour CPU |

---

# 4. Asyncio (Programmation Asynchrone)

---

# Définition

Asyncio permet d’exécuter du code non bloquant.

---

# Exemple simple

```python
import asyncio

async def task():
    print("Start")
    await asyncio.sleep(1)
    print("End")

asyncio.run(task())
```

---

# Plusieurs tâches

```python
import asyncio

async def task(name):
    print(name, "start")
    await asyncio.sleep(1)
    print(name, "end")

async def main():
    await asyncio.gather(
        task("A"),
        task("B"),
        task("C")
    )

asyncio.run(main())
```

---

# Avantages

- très rapide pour I/O
- scalable
- utilisé dans FastAPI

---

# 5. Event Loop

---

# Définition

L’event loop gère les tâches async.

---

# Fonctionnement

1. reçoit les tâches
2. les exécute
3. gère les pauses (await)
4. optimise l’ordre d’exécution

---

# 6. GIL (Global Interpreter Lock)

---

# Définition

Le GIL empêche plusieurs threads Python d’exécuter du code Python en même temps.

---

# Impact

- limite le multithreading CPU
- n’impacte pas I/O async

---

# Solution

- multiprocessing
- asyncio
- extensions C (NumPy)

---

# 7. Performance Optimization

---

# 7.1 List Comprehension vs Loop

## Mauvais

```python
result = []

for i in range(1000):
    result.append(i * 2)
```

## Bon

```python
result = [i * 2 for i in range(1000)]
```

---

# 7.2 Générateurs (Memory Efficient)

```python
def generate():
    for i in range(1000000):
        yield i

for value in generate():
    pass
```

---

# 7.3 Built-ins optimisés

```python
numbers = [1, 2, 3, 4]

print(sum(numbers))
print(max(numbers))
```

---

# 8. Caching (Optimisation mémoire)

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

# Avantages

- réduit calculs répétitifs
- améliore performance exponentiellement

---

# 9. Profiling (Analyse performance)

---

# Exemple

```python
import cProfile

def test():
    total = 0
    for i in range(100000):
        total += i
    return total

cProfile.run('test()')
```

---

# Utilité

- identifier lenteurs
- optimiser bottlenecks

---

# 10. Memory Management

---

# Garbage Collection

```python
import gc

gc.collect()
```

---

# Références

```python
a = [1, 2, 3]
b = a
```

---

# 11. Optimisation des boucles

---

# Mauvais

```python
for i in range(len(list)):
    print(list[i])
```

---

# Bon

```python
for item in list:
    print(item)
```

---

# 12. String Optimization

---

# Mauvais

```python
s = ""
for i in range(1000):
    s += str(i)
```

---

# Bon

```python
s = "".join(str(i) for i in range(1000))
```

---

# 13. I/O Optimization

---

# Lecture efficace

```python
with open("file.txt", "r") as file:
    for line in file:
        print(line.strip())
```

---

# 14. Parallelism avancé

---

# Pool de processus

```python
from multiprocessing import Pool

def square(x):
    return x * x

with Pool(4) as p:
    print(p.map(square, [1, 2, 3, 4]))
```

---

# 15. Lazy Evaluation

---

# Définition

Calcul uniquement quand nécessaire.

---

# Exemple

```python
numbers = (x * x for x in range(10))
```

---

# 16. Optimisation réseau

---

# Exemple async HTTP

```python
import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

---

# 17. Erreurs fréquentes

- confusion threading vs multiprocessing
- abus async sans besoin
- memory leaks (références circulaires)
- concaténation de strings en boucle
- pas de profiling

---

# 18. Bonnes pratiques

- utiliser asyncio pour I/O
- multiprocessing pour CPU
- profiling avant optimisation
- privilégier built-ins
- éviter boucles lourdes
- utiliser generators

---

# Points Clés

- Threading = multitâche léger
- Multiprocessing = CPU parallèle
- Asyncio = I/O non bloquant
- GIL limite le multithreading CPU
- Caching améliore fortement performance
- Profiling est essentiel avant optimisation
- Generators économisent mémoire
- Built-ins sont optimisés en C

---

# Exercice

## Énoncé

Créer :
1. une fonction async,
2. exécuter plusieurs tâches en parallèle,
3. afficher le résultat.

---

# Correction

```python
import asyncio

async def task(name):
    print(name, "start")
    await asyncio.sleep(1)
    print(name, "end")

async def main():
    await asyncio.gather(
        task("Task 1"),
        task("Task 2"),
        task("Task 3")
    )

asyncio.run(main())
```