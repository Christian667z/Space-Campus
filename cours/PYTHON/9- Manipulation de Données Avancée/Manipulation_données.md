# Manipulation de Données Avancée en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

La manipulation de données avancée est une compétence essentielle en Python moderne.

Elle est utilisée dans :
- la data science,
- l’intelligence artificielle,
- les APIs,
- les bases de données,
- les systèmes financiers,
- les applications web,
- l’automatisation avancée.

L’objectif est de savoir :
- transformer des données,
- nettoyer des données,
- filtrer des données,
- analyser des données,
- structurer des données complexes.

---

# 1. Structures de données avancées

---

# Rappel rapide

Python utilise principalement :
- list
- dict
- set
- tuple

Mais en avancé, on combine tout cela.

---

# Exemple complexe

```python
users = [
    {
        "id": 1,
        "name": "Chris",
        "skills": ["Python", "AI", "Cybersecurity"]
    },
    {
        "id": 2,
        "name": "John",
        "skills": ["JavaScript", "React"]
    }
]
```

---

# 2. Accès aux données complexes

---

# Exemple

```python
print(users[0]["name"])
print(users[0]["skills"][1])
```

---

# 3. Filtrage de données

---

# Exemple : trouver les utilisateurs Python

```python
python_users = []

for user in users:
    if "Python" in user["skills"]:
        python_users.append(user)

print(python_users)
```

---

# 4. List Comprehension avancée

---

# Exemple

```python
python_users = [user for user in users if "Python" in user["skills"]]
```

---

# 5. Transformation de données

---

# Exemple : extraire les noms

```python
names = [user["name"] for user in users]
print(names)
```

---

# 6. Dictionary Comprehension avancé

---

# Exemple : mapping id → name

```python
user_map = {user["id"]: user["name"] for user in users}
print(user_map)
```

---

# 7. Tri de données

---

# Exemple : trier par nom

```python
sorted_users = sorted(users, key=lambda x: x["name"])
print(sorted_users)
```

---

# Exemple : tri par nombre de skills

```python
sorted_users = sorted(users, key=lambda x: len(x["skills"]), reverse=True)
```

---

# 8. Lambda avancé

---

# Exemple

```python
get_name = lambda user: user["name"]

print(get_name(users[0]))
```

---

# 9. Map, Filter, Reduce (niveau avancé)

---

# Map

```python
names = list(map(lambda u: u["name"], users))
```

---

# Filter

```python
python_users = list(filter(lambda u: "Python" in u["skills"], users))
```

---

# Reduce

```python
from functools import reduce

total_skills = reduce(lambda acc, u: acc + len(u["skills"]), users, 0)
print(total_skills)
```

---

# 10. Nettoyage de données

---

# Exemple

```python
data = ["  Chris ", "John ", "  Marie"]

cleaned = [name.strip().lower() for name in data]
print(cleaned)
```

---

# 11. Suppression des doublons

---

# Exemple

```python
numbers = [1, 2, 2, 3, 4, 4, 5]

unique = list(set(numbers))
print(unique)
```

---

# 12. Fusion de structures

---

# Exemple

```python
a = {"name": "Chris"}
b = {"age": 20}

merged = {**a, **b}
print(merged)
```

---

# 13. Manipulation de JSON

---

# Exemple

```python
import json

data = '{"name": "Chris", "age": 20}'

parsed = json.loads(data)
print(parsed["name"])
```

---

# Conversion Python → JSON

```python
obj = {"name": "Chris"}

json_data = json.dumps(obj)
print(json_data)
```

---

# 14. Lecture de données complexes

---

# Exemple fichier JSON

```python
with open("data.json", "r") as file:
    data = json.load(file)

print(data)
```

---

# 15. Agrégation de données

---

# Exemple : somme des âges

```python
users = [
    {"name": "Chris", "age": 20},
    {"name": "John", "age": 25}
]

total_age = sum(user["age"] for user in users)
print(total_age)
```

---

# 16. Groupement de données

---

# Exemple : group by skills

```python
from collections import defaultdict

groups = defaultdict(list)

for user in users:
    for skill in user["skills"]:
        groups[skill].append(user["name"])

print(groups)
```

---

# 17. Manipulation de fichiers (avancé)

---

# Écriture structurée

```python
data = ["Chris", "John", "Marie"]

with open("users.txt", "w") as file:
    for name in data:
        file.write(name + "\n")
```

---

# Lecture avancée

```python
with open("users.txt", "r") as file:
    lines = [line.strip() for line in file]

print(lines)
```

---

# 18. Générateurs de données

---

# Exemple

```python
def generate_users():
    for i in range(5):
        yield {"id": i, "name": f"User{i}"}

for user in generate_users():
    print(user)
```

---

# 19. Data pipelines simples

---

# Exemple complet

```python
data = ["  Chris ", "JOHN", "marie  "]

result = [
    name.strip().lower()
    for name in data
    if len(name.strip()) > 3
]

print(result)
```

---

# 20. Performance en manipulation de données

---

# Bonnes pratiques

- utiliser list comprehension
- éviter les boucles inutiles
- utiliser set pour unicité
- utiliser generators pour gros volumes
- éviter les copies inutiles

---

# 21. Erreurs fréquentes

- oublier strip() lors du nettoyage
- confondre list et set
- modifier une liste pendant une boucle
- mauvais accès aux clés dict
- erreurs JSON mal formaté

---

# 22. Applications réelles

La manipulation avancée de données est utilisée dans :

- IA et machine learning
- analyse de données (Data Science)
- systèmes bancaires
- APIs REST
- moteurs de recherche
- réseaux sociaux
- cybersécurité
- dashboards

---

# Points Clés

- Les données complexes sont souvent imbriquées.
- List comprehension = traitement rapide.
- Dict comprehension = structuration efficace.
- JSON est essentiel pour les APIs.
- set permet de supprimer les doublons.
- reduce permet les agrégations.
- generators optimisent la mémoire.
- defaultdict facilite le groupement.

---

# Exercice

## Énoncé

Créer un programme qui :
1. filtre les utilisateurs qui connaissent Python,
2. extrait leurs noms,
3. affiche le résultat.

---

# Correction

```python
users = [
    {"name": "Chris", "skills": ["Python", "AI"]},
    {"name": "John", "skills": ["JavaScript"]},
    {"name": "Marie", "skills": ["Python"]}
]

python_users = [
    user["name"]
    for user in users
    if "Python" in user["skills"]
]

print(python_users)
```