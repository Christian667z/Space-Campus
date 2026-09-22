# 🐍 Programmation Python — Les Bases

> "Python est exécutable pseudo-code. Python est l'élégance pure."

## 1. Introduction
Python est un langage interprété, orienté objet, à typage dynamique. Il est très utilisé pour le web (Django/Flask), les scripts systèmes, et l'IA (Machine Learning).

## 2. Syntaxe de Base

### Variables et Types
Contrairement au C ou Java, on ne déclare pas le type d'une variable.

```python
nom = "Asta"        # String
age = 22            # Integer
taille = 1.75       # Float
est_etudiant = True # Boolean
```

### Conditions
L'indentation (4 espaces) remplace les accolades `{}`.

```python
if age >= 18:
    print("Majeur")
elif age == 17:
    print("Bientôt majeur")
else:
    print("Mineur")
```

### Boucles
```python
# Boucle For (itération sur une séquence)
for i in range(5):
    print(i) # 0, 1, 2, 3, 4

# Boucle While
compteur = 0
while compteur < 5:
    print(compteur)
    compteur += 1
```

## 3. Structures de Données

```python
# Liste (Tableau dynamique)
fruits = ["Pomme", "Banane", "Cerise"]
fruits.append("Orange")

# Dictionnaire (Clé-Valeur)
etudiant = {
    "nom": "Asta",
    "niveau": "L2",
    "notes": [18, 15, 19]
}
print(etudiant["nom"]) # Affiche "Asta"
```

## 4. Fonctions

```python
def calculer_moyenne(notes):
    if not notes:
        return 0
    return sum(notes) / len(notes)

ma_moyenne = calculer_moyenne([15, 18, 14])
print(f"Moyenne : {ma_moyenne}")
```
