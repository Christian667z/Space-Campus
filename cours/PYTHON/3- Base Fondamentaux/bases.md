# Les Bases Fondamentales de Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

Avant de créer :
- des applications,
- des intelligences artificielles,
- des sites web,
- des outils de cybersécurité,
- des scripts d’automatisation,

il est indispensable de maîtriser les bases fondamentales de Python.

Ces fondations sont essentielles car presque tout en Python repose dessus.

---

# Structure d’un Programme Python

Un programme Python est composé de :
- variables,
- fonctions,
- conditions,
- boucles,
- classes,
- modules,
- commentaires,
- instructions.

Exemple simple :

```python
nom = "Chris"

print("Bonjour", nom)
```

---

# La Fonction `print()`

## Définition

La fonction `print()` permet d’afficher du texte ou des données dans la console.

---

## Exemple

```python
print("Bonjour")
```

Résultat :

```text
Bonjour
```

---

## Afficher plusieurs valeurs

```python
nom = "Chris"
age = 20

print(nom, age)
```

---

## Afficher des calculs

```python
print(10 + 5)
```

Résultat :

```text
15
```

---

# Les Commentaires

## Définition

Les commentaires servent à :
- expliquer le code,
- documenter,
- rendre le programme plus lisible.

Python ignore les commentaires pendant l’exécution.

---

# Commentaire sur une ligne

```python
# Ceci est un commentaire
```

---

# Commentaire multiligne

```python
"""
Commentaire
sur plusieurs lignes
"""
```

---

# Les Variables

## Définition

Une variable sert à stocker une donnée en mémoire.

---

# Création d’une variable

```python
nom = "Chris"
age = 20
```

---

# Règles des variables

Une variable :
- peut contenir des lettres,
- des chiffres,
- des underscores `_`.

Mais :
- elle ne peut pas commencer par un chiffre,
- elle ne peut pas contenir d’espaces.

---

# Exemples valides

```python
nom_utilisateur = "Chris"
age1 = 20
```

---

# Exemples invalides

```python
1age = 20
nom utilisateur = "Chris"
```

---

# Les Types de Données

Python possède plusieurs types fondamentaux.

---

# Les Chaînes de caractères (`str`)

## Définition

Une chaîne contient du texte.

---

## Exemple

```python
nom = "Python"
```

---

## Guillemets simples

```python
nom = 'Python'
```

---

## Concaténation

```python
prenom = "Chris"
nom = "Jean"

print(prenom + " " + nom)
```

---

# Les Entiers (`int`)

## Définition

Les entiers sont des nombres sans virgule.

---

## Exemple

```python
age = 20
```

---

# Les Nombres Décimaux (`float`)

## Définition

Les floats contiennent des nombres avec virgule.

---

## Exemple

```python
prix = 19.99
```

---

# Les Booléens (`bool`)

## Définition

Les booléens possèdent uniquement deux valeurs :
- True
- False

---

## Exemple

```python
est_connecte = True
```

---

# Vérifier le Type d’une Variable

## Fonction `type()`

```python
age = 20

print(type(age))
```

Résultat :

```text
<class 'int'>
```

---

# Conversion de Types

## `int()`

```python
age = int("20")
```

---

## `float()`

```python
prix = float("19.99")
```

---

## `str()`

```python
age = str(20)
```

---

## `bool()`

```python
valeur = bool(1)
```

---

# Les Opérateurs Mathématiques

| Opérateur | Description |
|---|---|
| `+` | Addition |
| `-` | Soustraction |
| `*` | Multiplication |
| `/` | Division |
| `//` | Division entière |
| `%` | Modulo |
| `**` | Puissance |

---

# Exemples

```python
print(10 + 5)
print(10 - 5)
print(10 * 5)
print(10 / 5)
print(10 % 3)
print(2 ** 3)
```

---

# Les Opérateurs de Comparaison

| Opérateur | Signification |
|---|---|
| `==` | Égal |
| `!=` | Différent |
| `>` | Supérieur |
| `<` | Inférieur |
| `>=` | Supérieur ou égal |
| `<=` | Inférieur ou égal |

---

# Exemple

```python
print(10 > 5)
```

Résultat :

```text
True
```

---

# Les Opérateurs Logiques

| Opérateur | Description |
|---|---|
| `and` | ET |
| `or` | OU |
| `not` | NON |

---

# Exemple

```python
print(True and False)
```

---

# Les Conditions

## Définition

Les conditions permettent de prendre des décisions.

---

# `if`

```python
age = 18

if age >= 18:
    print("Majeur")
```

---

# `else`

```python
age = 15

if age >= 18:
    print("Majeur")
else:
    print("Mineur")
```

---

# `elif`

```python
note = 15

if note >= 18:
    print("Excellent")
elif note >= 10:
    print("Admis")
else:
    print("Échec")
```

---

# L’Indentation

## Définition

Python utilise l’indentation pour définir les blocs de code.

---

# Exemple

```python
if True:
    print("Bonjour")
```

---

# Erreur fréquente

```python
if True:
print("Bonjour")
```

Erreur :

```text
IndentationError
```

---

# Les Boucles

## Définition

Les boucles permettent de répéter du code.

---

# Boucle `while`

```python
i = 0

while i < 5:
    print(i)
    i += 1
```

---

# Boucle `for`

```python
for i in range(5):
    print(i)
```

---

# La Fonction `range()`

## Définition

`range()` génère une suite de nombres.

---

# Exemple

```python
range(5)
```

Produit :

```text
0 1 2 3 4
```

---

# Les Listes

## Définition

Une liste stocke plusieurs valeurs.

---

# Création

```python
notes = [10, 15, 20]
```

---

# Accès

```python
print(notes[0])
```

---

# Ajouter un élément

```python
notes.append(18)
```

---

# Supprimer un élément

```python
notes.remove(15)
```

---

# Les Tuples

## Définition

Un tuple est une collection non modifiable.

---

# Exemple

```python
coordonnees = (10, 20)
```

---

# Les Dictionnaires

## Définition

Un dictionnaire stocke des données sous forme clé/valeur.

---

# Exemple

```python
utilisateur = {
    "nom": "Chris",
    "age": 20
}
```

---

# Accès aux valeurs

```python
print(utilisateur["nom"])
```

---

# Les Fonctions

## Définition

Une fonction est un bloc de code réutilisable.

---

# Création d’une fonction

```python
def saluer():
    print("Bonjour")
```

---

# Appel d’une fonction

```python
saluer()
```

---

# Fonction avec paramètres

```python
def saluer(nom):
    print("Bonjour", nom)

saluer("Chris")
```

---

# Valeur de retour

```python
def addition(a, b):
    return a + b

resultat = addition(5, 3)
```

---

# L’Entrée Utilisateur

## Fonction `input()`

```python
nom = input("Votre nom : ")
```

---

# Exemple complet

```python
nom = input("Nom : ")

print("Bonjour", nom)
```

---

# Gestion des Erreurs

## Exemple

```python
print(10 / 0)
```

Erreur :

```text
ZeroDivisionError
```

---

# `try` et `except`

```python
try:
    print(10 / 0)
except:
    print("Erreur détectée")
```

---

# Les Modules

## Définition

Les modules permettent de réutiliser du code.

---

# Exemple

```python
import math

print(math.sqrt(25))
```

---

# Installer des Bibliothèques

## `pip`

```bash
pip install requests
```

---

# Les Fichiers Python

Les fichiers Python utilisent l’extension :

```text
.py
```

Exemple :

```text
main.py
```

---

# Exécuter un Programme Python

## Terminal

```bash
python main.py
```

---

# Les Mots Réservés

Quelques mots réservés :

```python
if
else
for
while
class
def
return
import
True
False
None
```

---

# Bonnes Pratiques

- Utiliser des noms clairs
- Bien indenter
- Commenter le code
- Éviter les variables inutiles
- Organiser son code

---

# Erreurs Fréquentes des Débutants

- Mauvaise indentation
- Oublier les parenthèses
- Confondre `=` et `==`
- Variables non définies
- Oublier les `:` dans les conditions

---

# Points Clés

- `print()` affiche du texte.
- Une variable stocke une donnée.
- Python possède plusieurs types.
- Les conditions prennent des décisions.
- Les boucles répètent du code.
- Les fonctions rendent le code réutilisable.
- Les listes stockent plusieurs valeurs.
- Les dictionnaires utilisent des clés.
- L’indentation est obligatoire.
- `input()` récupère des données utilisateur.

---

# Exercice

## Énoncé

Créer un programme qui :
1. demande le nom de l’utilisateur,
2. demande son âge,
3. affiche un message personnalisé.

---

# Correction

```python
nom = input("Nom : ")
age = input("Age : ")

print("Bonjour", nom)
print("Vous avez", age, "ans")
```