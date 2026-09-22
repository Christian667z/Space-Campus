# Développement Professionnel & Outils en Python

**Difficulté :** ★★★★★★★★★★

---

# Introduction

Le développement professionnel en Python ne consiste pas seulement à écrire du code.

Il consiste à :
- organiser des projets réels,
- utiliser des outils modernes,
- travailler en équipe,
- gérer des versions de code,
- tester et sécuriser les applications,
- déployer des projets,
- suivre des standards professionnels.

Ce niveau est utilisé dans :
- les entreprises,
- les startups,
- les projets open-source,
- les grandes applications web,
- les systèmes d’IA,
- les plateformes cloud.

---

# 1. Structure Professionnelle d’un Projet Python

---

# Exemple de structure standard

```text
project/
│
├── src/
│   ├── main.py
│   ├── app.py
│   ├── utils.py
│   └── services/
│       └── auth.py
│
├── tests/
│   └── test_app.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Pourquoi cette structure ?

Elle permet :
- organisation claire,
- travail en équipe,
- maintenance facile,
- évolutivité,
- séparation logique du code.

---

# 2. Environnements Virtuels (Virtual Environment)

---

# Définition

Un environnement virtuel permet d’isoler les dépendances d’un projet.

---

# Création

```bash
python -m venv venv
```

---

# Activation

## Windows

```bash
venv\Scripts\activate
```

## Mac/Linux

```bash
source venv/bin/activate
```

---

# Pourquoi utiliser un environnement virtuel ?

- éviter les conflits de bibliothèques,
- isoler chaque projet,
- reproduire facilement un projet,
- travailler comme en entreprise.

---

# 3. Gestion des dépendances (pip)

---

# Installer un package

```bash
pip install requests
```

---

# Sauvegarder les dépendances

```bash
pip freeze > requirements.txt
```

---

# Installer depuis requirements.txt

```bash
pip install -r requirements.txt
```

---

# 4. Git & GitHub (Version Control)

---

# Définition

Git permet de suivre les modifications du code.

GitHub permet de stocker et partager le code en ligne.

---

# Commandes Git de base

## Initialiser un projet

```bash
git init
```

---

## Ajouter des fichiers

```bash
git add .
```

---

## Commit

```bash
git commit -m "Initial commit"
```

---

## Envoyer vers GitHub

```bash
git push origin main
```

---

## Cloner un projet

```bash
git clone https://github.com/user/repo.git
```

---

# Pourquoi Git est important ?

- travail en équipe,
- historique du code,
- retour en arrière possible,
- collaboration mondiale.

---

# 5. Qualité du Code (PEP8)

---

# Définition

PEP8 est le guide officiel de style Python.

---

# Bonnes pratiques PEP8

- noms en snake_case

```python
user_name = "Chris"
```

- classes en CamelCase

```python
class UserAccount:
    pass
```

- indentation 4 espaces

---

# Mauvais exemple

```python
def MyFunction():
 print("Hello")
```

---

# Bon exemple

```python
def my_function():
    print("Hello")
```

---

# 6. Logging (journalisation)

---

# Définition

Le logging permet de suivre ce que fait un programme.

---

# Exemple

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Application started")
logging.warning("Low memory")
logging.error("An error occurred")
```

---

# Pourquoi utiliser logging ?

- remplacer print(),
- suivre les erreurs,
- analyser les comportements,
- production professionnelle.

---

# 7. Tests Unitaires

---

# Définition

Les tests permettent de vérifier que le code fonctionne correctement.

---

# Exemple avec unittest

```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

unittest.main()
```

---

# Pourquoi tester ?

- éviter les bugs,
- sécuriser le code,
- garantir la qualité,
- faciliter les mises à jour.

---

# 8. Debugging (Débogage)

---

# Techniques

- print debugging
- debugger IDE (VS Code, PyCharm)
- logging
- breakpoints

---

# Exemple breakpoint

```python
x = 10
y = 20

breakpoint()

print(x + y)
```

---

# 9. Packaging Python

---

# Définition

Créer un package permet de distribuer un projet Python.

---

# Exemple structure

```text
mypackage/
│
├── __init__.py
├── core.py
└── utils.py
```

---

# Installation locale

```bash
pip install .
```

---

# 10. API & Requests

---

# Exemple avec requests

```python
import requests

response = requests.get("https://api.github.com")

print(response.status_code)
print(response.json())
```

---

# 11. Web Development (Flask Example)

---

# Exemple simple

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

app.run()
```

---

# 12. Sécurité de base

---

# Bonnes pratiques

- ne jamais hardcoder les mots de passe,
- utiliser variables d’environnement,
- valider les entrées utilisateur,
- éviter injection de code.

---

# Exemple sécurisé

```python
import os

password = os.getenv("PASSWORD")
```

---

# 13. Variables d’environnement

---

# Définition

Permet de stocker des données sensibles.

---

# Exemple

```python
import os

api_key = os.getenv("API_KEY")
```

---

# 14. Performance et optimisation

---

# Bonnes pratiques

- éviter boucles inutiles,
- utiliser list comprehension,
- utiliser generators,
- éviter duplication,
- utiliser bibliothèques optimisées.

---

# Exemple optimisé

```python
numbers = [x * 2 for x in range(1000)]
```

---

# 15. Déploiement

---

# Définition

Le déploiement consiste à mettre une application en ligne.

---

# Outils

- Docker
- AWS
- Heroku
- VPS
- Render

---

# Exemple Docker (simple)

```dockerfile
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
```

---

# 16. Collaboration en équipe

---

# Outils utilisés

- GitHub
- GitLab
- Jira
- Trello
- Slack

---

# 17. Bonnes pratiques professionnelles

- écrire du code propre
- commenter intelligemment
- utiliser Git correctement
- tester le code
- structurer les projets
- documenter les fonctions

---

# 18. Erreurs fréquentes en pro

- mauvais usage Git
- absence de tests
- code non structuré
- dépendances non gérées
- pas de virtual environment

---

# Points Clés

- Un projet Python professionnel est structuré.
- Git est obligatoire en équipe.
- Les environnements virtuels isolent les projets.
- PEP8 définit les bonnes pratiques.
- Logging remplace print().
- Les tests garantissent la qualité.
- Les APIs permettent la communication.
- Le déploiement rend le projet accessible.
- La sécurité est essentielle.

---

# Exercice

## Énoncé

Créer un mini projet structuré :
1. une fonction dans un module,
2. un fichier principal,
3. utilisation de logging,
4. affichage d’un message propre.

---

# Correction

```python
# utils.py
def greet(name):
    return "Hello " + name
```

```python
# main.py
import logging
import utils

logging.basicConfig(level=logging.INFO)

message = utils.greet("Chris")
logging.info(message)
```