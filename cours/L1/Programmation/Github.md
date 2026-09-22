# 🐙 Git & GitHub — Collaboration et Versionning

> "Si ça n'est pas sur Git, ça n'existe pas."

## 1. Introduction
**Git** est un système de contrôle de version distribué (créé par Linus Torvalds en 2005). Il permet de suivre les modifications de votre code.
**GitHub** (ou GitLab / Bitbucket) est une plateforme cloud qui héberge des dépôts Git et ajoute des outils de collaboration.

## 2. Concepts Fondamentaux

- **Repository (Dépôt) :** Votre projet, contenant tous les fichiers et l'historique.
- **Commit :** Une "photographie" (snapshot) de vos fichiers à un instant T.
- **Branch (Branche) :** Une ligne de développement parallèle (ex: `main`, `dev`, `feature-login`).
- **Merge :** Fusionner les changements d'une branche dans une autre.
- **Pull Request (PR) :** Demander à fusionner vos modifications sur GitHub pour qu'elles soient revues.

## 3. Workflow de Base (Commandes Git)

```bash
# 1. Initialiser un dépôt local
git init

# 2. Cloner un dépôt existant depuis GitHub
git clone https://github.com/user/projet.git

# 3. Voir l'état des fichiers (modifiés, ajoutés...)
git status

# 4. Ajouter des fichiers à l'index (Staging)
git add fichier.py     # Un fichier spécifique
git add .              # Tous les fichiers modifiés

# 5. Créer un commit (sauvegarder l'état)
git commit -m "Ajout de la fonction de login"

# 6. Envoyer les commits vers GitHub
git push origin main

# 7. Récupérer les nouveautés depuis GitHub
git pull origin main
```

## 4. Gestion des Branches

Ne travaillez **JAMAIS** directement sur la branche `main` en équipe!

```bash
# Créer et basculer sur une nouvelle branche
git checkout -b feature-nouvelle-page

# (Faire des modifications, git add, git commit...)

# Revenir sur main
git checkout main

# Fusionner la nouvelle branche dans main
git merge feature-nouvelle-page

# Supprimer la branche (une fois fusionnée)
git branch -d feature-nouvelle-page
```

## 5. Résoudre un Conflit
Un conflit survient quand deux personnes modifient la même ligne du même fichier.
Git insère des marqueurs dans le fichier :

```text
<<<<<<< HEAD
Ma version modifiée
=======
La version modifiée par mon collègue
>>>>>>> origin/main
```

Il faut éditer le fichier manuellement, choisir la bonne version, effacer les marqueurs, puis faire `git add` et `git commit`.
