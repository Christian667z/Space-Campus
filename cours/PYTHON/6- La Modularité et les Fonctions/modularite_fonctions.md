# La Modularité et les Fonctions en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

La modularité et les fonctions sont des concepts fondamentaux en programmation Python.

Ils permettent de :
- organiser le code,
- éviter les répétitions,
- améliorer la lisibilité,
- faciliter la maintenance,
- réutiliser des blocs de code,
- structurer des projets professionnels.

Sans fonctions et modularité, un programme devient :
- long,
- difficile à comprendre,
- impossible à maintenir.

---

# 1. Les Fonctions

---

# Définition

Une fonction est un bloc de code réutilisable qui exécute une tâche précise.

---

# Pourquoi utiliser des fonctions ?

Les fonctions servent à :
- éviter de répéter le même code,
- structurer un programme,
- simplifier la lecture,
- rendre le code plus propre,
- faciliter le débogage.

---

# Syntaxe d’une fonction

```python
def nom_de_la_fonction():
    instruction
```

---

# Exemple simple

```python
def saluer():
    print("Bonjour !")

saluer()
```

---

# 2. Fonction avec paramètres

---

# Définition

Les paramètres permettent de donner des informations à une fonction.

---

# Exemple

```python
def saluer(nom):
    print("Bonjour", nom)

saluer("Chris")
saluer("Jean")
```

---

# Plusieurs paramètres

```python
def addition(a, b):
    print(a + b)

addition(5, 3)
```

---

# 3. Fonction avec valeur de retour

---

# Définition

`return` permet de renvoyer une valeur.

---

# Exemple

```python
def addition(a, b):
    return a + b

resultat = addition(5, 3)
print(resultat)
```

---

# Pourquoi utiliser return ?

- stocker un résultat,
- réutiliser une valeur,
- faire des calculs complexes.

---

# 4. Types de fonctions

---

# Fonction sans paramètre

```python
def bonjour():
    print("Salut")
```

---

# Fonction avec paramètres

```python
def saluer(nom):
    print(nom)
```

---

# Fonction avec retour

```python
def carre(x):
    return x * x
```

---

# Fonction complète

```python
def calcul(a, b):
    return (a + b) * 2
```

---

# 5. Portée des variables (Scope)

---

# Définition

La portée détermine où une variable est accessible.

---

# Variable locale

```python
def test():
    x = 10
    print(x)
```

---

# Variable globale

```python
x = 20

def test():
    print(x)

test()
```

---

# Différence importante

| Type | Accès |
|---|---|
| Locale | Seulement dans la fonction |
| Globale | Partout dans le programme |

---

# 6. Modularité

---

# Définition

La modularité consiste à diviser un programme en plusieurs parties appelées modules.

---

# Pourquoi la modularité ?

- organiser le code,
- faciliter la maintenance,
- réutiliser du code,
- travailler en équipe,
- éviter les fichiers énormes.

---

# 7. Les modules Python

---

# Définition

Un module est un fichier Python contenant du code réutilisable.

---

# Exemple

```python
# fichier: math_utils.py

def addition(a, b):
    return a + b
```

---

# Utilisation d’un module

```python
import math_utils

print(math_utils.addition(5, 3))
```

---

# 8. Importation de modules

---

# Import simple

```python
import math
```

---

# Import spécifique

```python
from math import sqrt
```

---

# Import avec alias

```python
import math as m

print(m.sqrt(16))
```

---

# 9. Modules intégrés (built-in)

Python contient déjà des modules :

| Module | Utilité |
|---|---|
| math | Calculs mathématiques |
| random | Nombres aléatoires |
| datetime | Dates et heures |
| os | Système d’exploitation |
| sys | Paramètres système |

---

# Exemple avec math

```python
import math

print(math.sqrt(25))
```

---

# Exemple avec random

```python
import random

print(random.randint(1, 10))
```

---

# 10. Organisation d’un projet (modularité réelle)

---

# Exemple structure

```text
projet/
│
├── main.py
├── utils.py
├── database.py
└── config.py
```

---

# Exemple utils.py

```python
def saluer(nom):
    return "Bonjour " + nom
```

---

# main.py

```python
import utils

print(utils.saluer("Chris"))
```

---

# 11. Avantages de la modularité

- code plus propre
- facile à comprendre
- facile à tester
- réutilisable
- travail en équipe facilité

---

# 12. Erreurs fréquentes

- oublier les parenthèses lors de l’appel
- oublier return
- mauvaise indentation
- nom de module incorrect
- confusion entre import et from

---

# 13. Bonnes pratiques

- une fonction = une tâche
- noms clairs et descriptifs
- éviter les fonctions trop longues
- séparer le code en fichiers
- utiliser des modules

---

# 14. Exemple complet

```python
# module: operations.py

def addition(a, b):
    return a + b

def multiplication(a, b):
    return a * b
```

---

```python
# main.py

import operations

print(operations.addition(2, 3))
print(operations.multiplication(2, 3))
```

---

# Points Clés

- Une fonction est un bloc de code réutilisable.
- `def` sert à créer une fonction.
- `return` renvoie une valeur.
- Les paramètres permettent de personnaliser les fonctions.
- Les modules permettent d’organiser le code.
- `import` sert à utiliser un module.
- La modularité rend les projets professionnels.

---

# Exercice

## Énoncé

Créer :
1. une fonction qui multiplie deux nombres,
2. une fonction qui affiche un message personnalisé,
3. utiliser les deux fonctions dans un programme.

---

# Correction

```python
def multiplier(a, b):
    return a * b

def saluer(nom):
    print("Bonjour", nom)

print(multiplier(3, 4))
saluer("Chris")
```