# Les Structures de Données en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

Les structures de données sont des outils fondamentaux en programmation.

Elles permettent de :
- organiser les données,
- stocker des informations,
- manipuler des collections,
- accéder rapidement aux données,
- optimiser les performances des programmes.

Sans structures de données, il serait impossible de créer :
- des applications modernes,
- des jeux,
- des réseaux sociaux,
- des systèmes d’IA,
- des bases de données.

---

# Qu’est-ce qu’une Structure de Données ?

Une structure de données est une manière d’organiser et de stocker des données pour pouvoir les utiliser efficacement.

---

# Les Principales Structures de Données en Python

Python possède 4 structures de données fondamentales :

| Structure | Description |
|---|---|
| Liste | Collection ordonnée et modifiable |
| Tuple | Collection ordonnée et non modifiable |
| Dictionnaire | Collection clé/valeur |
| Ensemble (Set) | Collection non ordonnée sans doublons |

---

# 1. Les Listes (list)

---

# Définition

Une liste est une structure de données :
- ordonnée,
- modifiable,
- dynamique,
- pouvant contenir plusieurs types de données.

---

# Création d’une liste

```python
nombres = [1, 2, 3, 4, 5]
```

```python
noms = ["Chris", "Jean", "Marie"]
```

---

# Accès aux éléments

Les listes utilisent des index (commencent à 0).

```python
noms = ["Chris", "Jean", "Marie"]

print(noms[0])  # Chris
print(noms[1])  # Jean
```

---

# Index négatifs

```python
noms = ["Chris", "Jean", "Marie"]

print(noms[-1])  # Marie
```

---

# Modifier une liste

```python
noms = ["Chris", "Jean"]

noms[1] = "Paul"
print(noms)
```

---

# Ajouter des éléments

## append()

Ajoute à la fin :

```python
noms.append("Marie")
```

---

## insert()

Ajoute à une position :

```python
noms.insert(1, "Paul")
```

---

# Supprimer des éléments

## remove()

```python
noms.remove("Chris")
```

## pop()

```python
noms.pop()
```

## del

```python
del noms[0]
```

---

# Taille d’une liste

```python
print(len(noms))
```

---

# Parcourir une liste

```python
for nom in noms:
    print(nom)
```

---

# Liste avec différents types

```python
data = ["Chris", 20, True, 3.14]
```

---

# 2. Les Tuples (tuple)

---

# Définition

Un tuple est :
- ordonné,
- non modifiable (immutable),
- plus rapide qu’une liste.

---

# Création

```python
coordonnees = (10, 20)
```

---

# Accès

```python
print(coordonnees[0])
```

---

# Tuple à un élément

```python
t = (10,)
```

⚠️ la virgule est obligatoire

---

# Pourquoi utiliser un tuple ?

- données constantes,
- sécurité,
- performance,
- données fixes (ex: coordonnées GPS).

---

# 3. Les Dictionnaires (dict)

---

# Définition

Un dictionnaire stocke des données sous forme :
```text
clé → valeur
```

---

# Création

```python
utilisateur = {
    "nom": "Chris",
    "age": 20,
    "ville": "Port-au-Prince"
}
```

---

# Accès aux valeurs

```python
print(utilisateur["nom"])
```

---

# Ajouter une clé

```python
utilisateur["email"] = "test@gmail.com"
```

---

# Modifier une valeur

```python
utilisateur["age"] = 21
```

---

# Supprimer une clé

```python
del utilisateur["ville"]
```

---

# Méthodes importantes

## keys()

```python
print(utilisateur.keys())
```

---

## values()

```python
print(utilisateur.values())
```

---

## items()

```python
for cle, valeur in utilisateur.items():
    print(cle, valeur)
```

---

# Dictionnaire imbriqué

```python
etudiant = {
    "nom": "Chris",
    "notes": {
        "math": 15,
        "info": 18
    }
}
```

---

# Accès imbriqué

```python
print(etudiant["notes"]["math"])
```

---

# 4. Les Ensembles (set)

---

# Définition

Un set est :
- non ordonné,
- sans doublons,
- modifiable.

---

# Création

```python
nombres = {1, 2, 3, 4}
```

---

# Suppression des doublons automatique

```python
nombres = {1, 1, 2, 2, 3}
print(nombres)
```

Résultat :

```text
{1, 2, 3}
```

---

# Ajouter un élément

```python
nombres.add(5)
```

---

# Supprimer un élément

```python
nombres.remove(2)
```

---

# Opérations sur les sets

## Union

```python
a | b
```

## Intersection

```python
a & b
```

## Différence

```python
a - b
```

---

# Exemple complet

```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)
print(a & b)
print(a - b)
```

---

# 5. Comparaison des Structures

| Structure | Ordonnée | Modifiable | Doublons | Usage |
|---|---|---|---|---|
| Liste | Oui | Oui | Oui | Données générales |
| Tuple | Oui | Non | Oui | Données fixes |
| Dictionnaire | Oui (Python 3.7+) | Oui | Clés uniques | Données associatives |
| Set | Non | Oui | Non | Valeurs uniques |

---

# 6. Quand utiliser chaque structure ?

---

# Liste

Utiliser quand :
- ordre important,
- données modifiables,
- stockage simple.

Ex :
- utilisateurs,
- produits,
- scores.

---

# Tuple

Utiliser quand :
- données fixes,
- sécurité importante.

Ex :
- coordonnées GPS,
- constantes.

---

# Dictionnaire

Utiliser quand :
- relation clé/valeur,
- données structurées.

Ex :
- utilisateurs,
- profils,
- configurations.

---

# Set

Utiliser quand :
- éviter doublons,
- opérations mathématiques.

Ex :
- tags,
- identifiants uniques.

---

# 7. Conversion entre structures

---

```python
list()
tuple()
set()
dict()
```

---

# Exemple

```python
liste = [1, 2, 3]
print(set(liste))
```

---

# 8. Erreurs fréquentes

- Confondre liste et tuple
- Utiliser une clé inexistante dans un dictionnaire
- Oublier que les sets n’ont pas d’index
- Modifier un tuple (erreur)
- Oublier les crochets ou accolades

---

# 9. Applications réelles

Les structures de données sont utilisées dans :

- réseaux sociaux (listes d’utilisateurs),
- moteurs de recherche,
- bases de données,
- IA,
- jeux vidéo,
- systèmes bancaires,
- applications mobiles.

---

# 10. Exemple complet pratique

```python
utilisateurs = [
    {"nom": "Chris", "age": 20},
    {"nom": "Jean", "age": 25}
]

for u in utilisateurs:
    print(u["nom"], u["age"])
```

---

# Points Clés

- Les structures de données organisent les informations.
- Liste = flexible et ordonnée.
- Tuple = fixe et sécurisé.
- Dictionnaire = clé/valeur.
- Set = valeurs uniques.
- Chaque structure a un usage spécifique.
- Bien choisir une structure améliore les performances.

---

# Exercice

## Énoncé

Créer :
1. une liste de 3 noms,
2. ajouter un nouveau nom,
3. afficher chaque nom avec une boucle.

---

# Correction

```python
noms = ["Chris", "Jean", "Marie"]

noms.append("Paul")

for nom in noms:
    print(nom)
```