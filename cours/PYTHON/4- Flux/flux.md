# Le Contrôle du Flux en Python

**Difficulté :** Easy 

---

# Introduction

Le contrôle du flux (Flow Control) est l’un des concepts les plus importants en programmation.

Il permet à un programme de :
- prendre des décisions,
- répéter des actions,
- exécuter certaines parties du code,
- ignorer certaines instructions,
- contrôler l’ordre d’exécution.

Sans contrôle du flux, un programme exécuterait simplement les lignes de code de haut en bas sans intelligence.

Le contrôle du flux transforme un simple script en véritable programme capable :
- d’interagir,
- de réfléchir,
- de réagir,
- d’automatiser des comportements.

---

# Qu’est-ce que le Contrôle du Flux ?

Le contrôle du flux désigne les mécanismes permettant de contrôler :
- l’ordre d’exécution du code,
- les décisions,
- les répétitions,
- les interruptions,
- les conditions.

---

# Les Principaux Types de Contrôle du Flux

Python possède plusieurs mécanismes fondamentaux :

| Type | Rôle |
|---|---|
| Conditions | Prendre des décisions |
| Boucles | Répéter du code |
| Instructions de saut | Modifier le comportement des boucles |
| Gestion des erreurs | Contrôler les erreurs |
| Fonctions | Organiser l’exécution |
| Exceptions | Intercepter des problèmes |

---

# Les Conditions

## Définition

Les conditions permettent au programme de prendre des décisions.

Le programme peut :
- exécuter un bloc,
- ignorer un bloc,
- choisir entre plusieurs possibilités.

---

# La Structure `if`

## Syntaxe

```python
if condition:
    instruction
```

---

# Exemple

```python
age = 18

if age >= 18:
    print("Majeur")
```

---

# Fonctionnement

Le programme :
1. vérifie la condition,
2. si elle est vraie (`True`),
3. le bloc est exécuté.

---

# Exemple Visuel

```python
temperature = 35

if temperature > 30:
    print("Il fait chaud")
```

---

# Utilisation des Conditions

Les conditions sont utilisées dans :
- les systèmes de connexion,
- les jeux,
- les formulaires,
- les systèmes de sécurité,
- les applications bancaires,
- les intelligences artificielles.

---

# L’Instruction `else`

## Définition

`else` permet d’exécuter un bloc lorsque la condition est fausse.

---

# Syntaxe

```python
if condition:
    instruction
else:
    instruction
```

---

# Exemple

```python
age = 15

if age >= 18:
    print("Majeur")
else:
    print("Mineur")
```

---

# Fonctionnement

Si :
- la condition est vraie → bloc `if`
- la condition est fausse → bloc `else`

---

# L’Instruction `elif`

## Définition

`elif` signifie :
```text
else if
```

Il permet de tester plusieurs conditions.

---

# Exemple

```python
note = 16

if note >= 18:
    print("Excellent")
elif note >= 10:
    print("Admis")
else:
    print("Échec")
```

---

# Fonctionnement

Python vérifie les conditions dans l’ordre :
1. `if`
2. `elif`
3. `else`

Le premier bloc vrai est exécuté.

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

# Exemples

```python
print(10 > 5)
print(10 == 10)
print(5 != 3)
```

---

# Les Opérateurs Logiques

## `and`

Les deux conditions doivent être vraies.

```python
age = 20

if age >= 18 and age <= 30:
    print("Jeune adulte")
```

---

## `or`

Une seule condition doit être vraie.

```python
if age < 18 or age > 60:
    print("Tarif spécial")
```

---

## `not`

Inverse une condition.

```python
connecte = False

if not connecte:
    print("Connexion requise")
```

---

# Les Conditions Imbriquées

## Définition

Une condition peut être placée à l’intérieur d’une autre.

---

# Exemple

```python
age = 20
argent = True

if age >= 18:
    if argent:
        print("Accès autorisé")
```

---

# L’Indentation

## Définition

Python utilise l’indentation pour définir les blocs.

---

# Exemple Correct

```python
if True:
    print("Bonjour")
```

---

# Exemple Incorrect

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

Les boucles permettent de répéter du code automatiquement.

---

# Pourquoi utiliser des boucles ?

Sans boucle :

```python
print("Bonjour")
print("Bonjour")
print("Bonjour")
```

Avec boucle :

```python
for i in range(3):
    print("Bonjour")
```

---

# La Boucle `while`

## Définition

La boucle `while` répète du code tant qu’une condition est vraie.

---

# Syntaxe

```python
while condition:
    instruction
```

---

# Exemple

```python
i = 0

while i < 5:
    print(i)
    i += 1
```

---

# Fonctionnement

La boucle :
1. vérifie la condition,
2. exécute le bloc,
3. recommence jusqu’à ce que la condition devienne fausse.

---

# Danger : Boucle Infinie

```python
while True:
    print("Infini")
```

Cette boucle ne s’arrête jamais.

---

# La Boucle `for`

## Définition

La boucle `for` parcourt une séquence.

---

# Exemple avec `range()`

```python
for i in range(5):
    print(i)
```

Résultat :

```text
0
1
2
3
4
```

---

# Fonction `range()`

## Définition

`range()` génère une suite de nombres.

---

# Exemples

```python
range(5)
```

Produit :

```text
0 1 2 3 4
```

---

# Début et fin

```python
range(1, 6)
```

Résultat :

```text
1 2 3 4 5
```

---

# Pas personnalisé

```python
range(0, 10, 2)
```

Résultat :

```text
0 2 4 6 8
```

---

# Parcourir une Liste

```python
noms = ["Chris", "Jean", "Marie"]

for nom in noms:
    print(nom)
```

---

# Les Instructions de Contrôle des Boucles

---

# `break`

## Définition

`break` arrête immédiatement une boucle.

---

# Exemple

```python
for i in range(10):
    if i == 5:
        break

    print(i)
```

---

# `continue`

## Définition

`continue` saute une itération.

---

# Exemple

```python
for i in range(5):
    if i == 2:
        continue

    print(i)
```

---

# `pass`

## Définition

`pass` ne fait rien.

Il sert de placeholder.

---

# Exemple

```python
if True:
    pass
```

---

# Boucles Imbriquées

## Définition

Une boucle peut contenir une autre boucle.

---

# Exemple

```python
for i in range(3):
    for j in range(2):
        print(i, j)
```

---

# Utilisations Réelles des Boucles

Les boucles sont utilisées dans :
- les jeux,
- les IA,
- les systèmes de login,
- les menus,
- les serveurs,
- les bots,
- les scripts d’automatisation.

---

# Les Exceptions et le Contrôle du Flux

Les erreurs peuvent modifier le flux du programme.

---

# Exemple Sans Gestion

```python
print(10 / 0)
```

Erreur :

```text
ZeroDivisionError
```

---

# `try` et `except`

## Définition

Permet de gérer les erreurs sans arrêter le programme.

---

# Exemple

```python
try:
    print(10 / 0)

except:
    print("Erreur détectée")
```

---

# `finally`

## Définition

`finally` s’exécute toujours.

---

# Exemple

```python
try:
    print("Test")

finally:
    print("Fin")
```

---

# Les Fonctions et le Flux

Les fonctions permettent :
- d’organiser,
- de contrôler,
- de réutiliser du code.

---

# Exemple

```python
def saluer():
    print("Bonjour")

saluer()
```

---

# L’Instruction `return`

## Définition

`return` renvoie une valeur et termine la fonction.

---

# Exemple

```python
def addition(a, b):
    return a + b
```

---

# Flux d’Exécution d’un Programme

Python exécute généralement :
1. ligne par ligne,
2. de haut en bas,
3. sauf si le contrôle du flux modifie cet ordre.

---

# Exemple Global

```python
age = 20

if age >= 18:
    for i in range(3):
        print("Accès autorisé")
```

---

# Cas Réels d’Utilisation

---

# Système de Connexion

```python
mot_de_passe = "python123"

saisie = input("Mot de passe : ")

if saisie == mot_de_passe:
    print("Connexion réussie")
else:
    print("Accès refusé")
```

---

# Vérification d’Âge

```python
age = int(input("Age : "))

if age >= 18:
    print("Accès autorisé")
else:
    print("Interdit")
```

---

# Menu Répétitif

```python
while True:
    print("1. Jouer")
    print("2. Quitter")

    choix = input("Choix : ")

    if choix == "2":
        break
```

---

# Bonnes Pratiques

- Bien indenter le code
- Éviter les boucles infinies
- Utiliser des noms clairs
- Simplifier les conditions
- Éviter trop d’imbrications

---

# Erreurs Fréquentes

- Oublier les `:`
- Mauvaise indentation
- Confondre `=` et `==`
- Boucle infinie involontaire
- Conditions mal écrites

---

# Points Clés

- Le contrôle du flux contrôle l’exécution du programme.
- Les conditions prennent des décisions.
- Les boucles répètent du code.
- `if`, `elif`, `else` gèrent les choix.
- `for` parcourt des séquences.
- `while` répète tant qu’une condition est vraie.
- `break` arrête une boucle.
- `continue` saute une itération.
- `pass` ne fait rien.
- `try` et `except` gèrent les erreurs.
- L’indentation est obligatoire en Python.

---

# Exercice

## Énoncé

Créer un programme qui :
1. demande un mot de passe,
2. vérifie s’il est correct,
3. affiche un message,
4. redemande le mot de passe jusqu’à ce qu’il soit correct.

---

# Correction

```python
mot_de_passe = "python123"

while True:

    saisie = input("Mot de passe : ")

    if saisie == mot_de_passe:
        print("Connexion réussie")
        break

    else:
        print("Mot de passe incorrect")
```