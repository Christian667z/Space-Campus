# Introduction Complète de PYTHON

**Difficulté :** ★★★★★★★★★★

---

# Qu'est-ce que Python ?

Python est un langage de programmation interprété, de haut niveau, moderne et polyvalent créé par Guido van Rossum et publié officiellement en 1991.

Le nom "Python" provient de l’émission humoristique britannique *Monty Python’s Flying Circus* et non du serpent.

Python a été conçu avec un objectif principal :

> rendre la programmation plus simple, plus lisible et plus productive.

Aujourd’hui, Python est considéré comme l’un des langages les plus populaires au monde grâce à :
- sa simplicité,
- sa puissance,
- sa lisibilité,
- sa flexibilité,
- son immense communauté.

Python est utilisé aussi bien par :
- les débutants,
- les étudiants,
- les développeurs professionnels,
- les chercheurs,
- les ingénieurs,
- les experts en cybersécurité,
- les entreprises technologiques.

Des entreprises comme :
- Google,
- Netflix,
- Instagram,
- Spotify,
- NASA,
- YouTube,
- OpenAI,
utilisent Python dans leurs infrastructures.

---

# Histoire de Python

## Création du langage

Python a été créé à la fin des années 1980 par Guido van Rossum au CWI (Centre for Mathematics and Computer Science) aux Pays-Bas.

Guido voulait créer un langage :
- simple,
- clair,
- lisible,
- puissant,
- facile à apprendre,
- mais capable de gérer de gros projets.

---

## Évolution de Python

### Python 1.0
Première version officielle publiée en 1991.

### Python 2.x
Version extrêmement populaire pendant de nombreuses années.

### Python 3.x
Version moderne actuelle.
Elle améliore :
- les performances,
- la cohérence,
- la sécurité,
- la gestion Unicode.

Python 2 est aujourd’hui abandonné.

---

# Philosophie de Python

Python suit une philosophie appelée :

## "The Zen of Python"

Quelques principes célèbres :

- Beautiful is better than ugly.
- Simple is better than complex.
- Readability counts.
- Explicit is better than implicit.

En français :
- Le beau est meilleur que le laid.
- Le simple est meilleur que le complexe.
- La lisibilité est importante.
- L’explicite est préférable à l’implicite.

Cette philosophie explique pourquoi le code Python est souvent très propre et facile à comprendre.

---

# Caractéristiques Principales de Python

## Langage interprété

Python est un langage interprété.

Cela signifie :
- le code est exécuté ligne par ligne,
- il n’y a pas de compilation complexe avant l’exécution,
- les tests sont rapides.

---

## Langage de haut niveau

Python masque les détails complexes de la machine.

Le développeur se concentre davantage sur :
- la logique,
- les fonctionnalités,
- les algorithmes.

---

## Syntaxe simple et lisible

Python utilise une syntaxe proche du langage humain.

Exemple :

```python
print("Hello World")
```

---

## Typage dynamique

Le type des variables est déterminé automatiquement.

Exemple :

```python
nom = "Chris"
age = 22
```

---

## Typage fort

Python empêche certains mélanges incorrects entre types.

Exemple incorrect :

```python
print("Age : " + 22)
```

Erreur :
```text
TypeError
```

---

## Langage orienté objet

Python supporte la programmation orientée objet (POO).

On peut créer :
- des classes,
- des objets,
- de l’héritage,
- du polymorphisme.

---

## Multi-paradigme

Python supporte :
- la programmation procédurale,
- la programmation orientée objet,
- la programmation fonctionnelle,
- la programmation modulaire.

---

## Open Source

Python est gratuit et open source.

Tout le monde peut :
- l’utiliser,
- le modifier,
- le distribuer.

---

## Multiplateforme

Python fonctionne sur :
- Windows,
- Linux,
- macOS,
- Raspberry Pi,
- serveurs cloud.

---

# Pourquoi apprendre Python ?

Python est :
- simple à apprendre,
- puissant,
- très demandé sur le marché,
- moderne,
- extrêmement populaire.

Il est parfait pour :
- les débutants,
- les étudiants,
- les développeurs professionnels,
- les chercheurs,
- les hackers éthiques,
- les data scientists.

---

# Domaines d'utilisation de Python

## Développement Web

Frameworks populaires :
- Django
- Flask
- FastAPI

Python permet de créer :
- des sites web,
- des APIs,
- des backends.

---

## Intelligence Artificielle

Python domine le domaine de l’IA grâce à :
- TensorFlow,
- PyTorch,
- Scikit-learn.

Applications :
- chatbots,
- reconnaissance faciale,
- vision par ordinateur,
- IA générative,
- machine learning.

---

## Data Science

Bibliothèques populaires :
- Pandas,
- NumPy,
- Matplotlib,
- Seaborn.

Python est utilisé pour :
- analyser des données,
- créer des graphiques,
- manipuler des datasets,
- faire des statistiques.

---

## Cybersécurité

Python est énormément utilisé en :
- pentest,
- automatisation,
- analyse réseau,
- forensic,
- scripts de sécurité.

Exemples :
- scanners,
- brute force tools,
- analyse de logs,
- automatisation réseau.

---

## Automatisation

Python permet d’automatiser :
- les tâches répétitives,
- les fichiers,
- les emails,
- les serveurs,
- les bots.

---

## Développement Desktop

Bibliothèques :
- Tkinter,
- PyQt,
- Kivy,
- CustomTkinter.

---

## Jeux Vidéo

Avec :
- Pygame.

---

## Réseaux et Cloud

Python est utilisé en :
- DevOps,
- administration système,
- cloud computing,
- automatisation serveur.

---

# Fonctionnement de Python

Quand un programme Python est lancé :

1. Le fichier `.py` est lu.
2. Le code source est converti en bytecode.
3. La machine virtuelle Python exécute le bytecode.

---

# Structure d’un Programme Python

Un programme Python contient souvent :

- des variables,
- des fonctions,
- des conditions,
- des boucles,
- des classes,
- des modules,
- des bibliothèques.

Exemple :

```python
nom = "Chris"

def saluer():
    print("Bonjour", nom)

saluer()
```

---

# Installation de Python

## Télécharger Python

Site officiel :

https://www.python.org

---

## Installation sous Windows

Pendant l’installation :
- cocher `Add Python to PATH`.

---

## Vérification

Commande :

```bash
python --version
```

ou :

```bash
py --version
```

---

# Premier Programme Python

```python
print("Bonjour, monde !")
```

Résultat :

```text
Bonjour, monde !
```

---

# Les fichiers Python

Les fichiers Python utilisent l’extension :

```text
.py
```

Exemple :

```text
main.py
```

---

# Les commentaires en Python

## Commentaire simple

```python
# Ceci est un commentaire
```

## Commentaire multiligne

```python
"""
Commentaire
sur plusieurs lignes
"""
```

---

# Les variables

Une variable sert à stocker une donnée.

Exemple :

```python
nom = "Chris"
age = 20
```

---

# Types de données en Python

## Chaîne de caractères

```python
nom = "Python"
```

## Entier

```python
age = 20
```

## Nombre décimal

```python
prix = 19.99
```

## Booléen

```python
est_connecte = True
```

## Liste

```python
notes = [10, 15, 20]
```

## Tuple

```python
coordonnees = (10, 20)
```

## Dictionnaire

```python
user = {
    "name": "Asta",
    "age": 22
}
```

---

# L’indentation en Python

Python utilise l’indentation pour définir les blocs de code.

Exemple :

```python
if True:
    print("Hello World")
```

Une mauvaise indentation provoque :

```text
IndentationError
```

---

# Les bibliothèques Python

Python possède énormément de bibliothèques.

Exemples :
- requests
- pandas
- numpy
- flask
- pygame
- tkinter

Installation :

```bash
pip install nom_bibliotheque
```

---

# Gestionnaire de paquets : pip

`pip` permet d’installer des bibliothèques Python.

Exemple :

```bash
pip install requests
```

---

# Avantages de Python

- Facile à apprendre
- Syntaxe claire
- Très puissant
- Grande communauté
- Énorme écosystème
- Développement rapide
- Compatible avec l’IA
- Très utilisé professionnellement
- Excellent pour les débutants

---

# Inconvénients de Python

- Plus lent que certains langages compilés
- Consomme plus de mémoire
- Moins performant pour les systèmes bas niveau
- Moins utilisé pour les jeux AAA

---

# Comparaison avec d'autres langages

| Langage | Difficulté | Rapidité | Lisibilité |
|---|---|---|---|
| Python | Facile | Moyenne | Très élevée |
| C++ | Difficile | Très rapide | Moyenne |
| Java | Moyenne | Rapide | Bonne |
| JavaScript | Moyenne | Rapide | Bonne |

---

# Cas d'utilisation réels

Python est utilisé dans :
- les banques,
- les universités,
- les systèmes cloud,
- les applications web,
- les IA modernes,
- les outils de cybersécurité,
- les scripts système.

---

# Points Clés

- Python est un langage interprété.
- Créé par Guido van Rossum.
- Publié en 1991.
- Syntaxe simple et lisible.
- Typage dynamique et fort.
- Compatible avec plusieurs paradigmes.
- Très utilisé en IA, cybersécurité et web.
- Fonctionne sur plusieurs systèmes.
- Python 3 est la version recommandée.
- `print()` affiche du texte dans la console.
- L’indentation est obligatoire.
- `pip` permet d’installer des bibliothèques.

---

# Exercice

## Énoncé

Quel est le rôle de la fonction `print()` en Python ?

<details>
<summary><b>Voir la Correction</b></summary>

✅ La fonction `print()` permet d’afficher du texte, des variables ou des résultats dans la console.

Exemple :

```python
print("Hello Python")
```

Résultat :

```text
Hello Python
```

</details>