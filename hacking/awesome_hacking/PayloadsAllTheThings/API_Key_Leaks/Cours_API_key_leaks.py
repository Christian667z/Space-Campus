CONTENT = """\nAPI KEY ET TOKEN LEAKS - FUITES DE CLÉS API ET DE JETONS

Définition pédagogique :

Les API keys et les tokens sont des éléments d’authentification utilisés pour permettre à une application ou un utilisateur d’accéder à un service.

API Key :
Identifiant unique utilisé pour autoriser des requêtes vers une API.

Token :
Jeton de sécurité (souvent temporaire) qui donne accès à des ressources protégées.

Problème :
Si ces éléments sont exposés (leak), un attaquant peut les utiliser pour accéder aux services, voler des données ou exécuter des actions à la place de la victime.


==================================================
PARTIE 1 : OUTILS POUR DÉTECTER LES FUITES
==================================================

Explication :

Plusieurs outils permettent de scanner du code, des dépôts ou des images pour détecter des secrets exposés.

Exemples concrets :

Scanner un dépôt GitHub avec trufflehog :

docker run --rm -it -v "$PWD:/pwd" trufflesecurity/trufflehog:latest github --repo https://github.com/exemple/repo

Scanner une organisation complète :

docker run --rm -it -v "$PWD:/pwd" trufflesecurity/trufflehog:latest github --org=nom_organisation

Scanner une image Docker :

docker run --rm -it -v "$PWD:/pwd" trufflesecurity/trufflehog:latest docker --image nom_image

Tester des tokens avec nuclei :

nuclei -t token-spray/ -var token=token_list.txt


==================================================
PARTIE 2 : MÉTHODOLOGIE
==================================================


--------------------------------------------------
Comprendre API Key et Token
--------------------------------------------------

API Key :

Utilisée pour identifier une application.

Exemple :
Une API météo qui demande une clé pour accéder aux données.

Token :

Utilisé pour authentifier un utilisateur.

Exemple :
Un token OAuth permettant d’accéder à un compte Google.


--------------------------------------------------
Causes communes des fuites
--------------------------------------------------

1. Clé codée en dur dans le code

Explication :

Les développeurs mettent directement la clé dans le code.

Exemple :

api_key = "1234567890abcdef"

Problème :
Si le code est partagé ou publié, la clé est exposée


2. Dépôts publics (GitHub)

Explication :

Les clés sont accidentellement publiées dans des repos publics.

Exemple concret :

Un développeur push un fichier contenant :

AWS_SECRET=abcd1234

Tout le monde peut le voir


3. Images Docker

Explication :

Les clés peuvent être incluses dans des images Docker.

Exemple :

Une image contient un fichier config avec des credentials


4. Logs et debug

Explication :

Les systèmes enregistrent des informations sensibles dans les logs.

Exemple :

print("Token:", token)

Ces logs peuvent être accessibles


5. Fichiers de configuration

Explication :

Les fichiers comme .env ou config.json contiennent souvent des secrets.

Exemples :

.env
config.json
settings.py
.aws/credentials

Si ces fichiers sont exposés → fuite directe


--------------------------------------------------
Validation d’une API Key
--------------------------------------------------

Explication :

Une fois une clé trouvée, il faut vérifier si elle est valide.

Méthode :

1. Identifier le service (AWS, Telegram, etc.)
2. Tester la clé avec une requête

Exemple concret :

Tester un token Telegram :

curl https://api.telegram.org/bot<TOKEN>/getMe

Si la réponse est valide → la clé fonctionne


--------------------------------------------------
Identification via patterns (regex)
--------------------------------------------------

Explication :

Certaines clés ont des formats reconnaissables.

Exemple :

Clé AWS :

AKIA + 16 caractères

Regex :

AKIA[0-9A-Z]{16}

Utilité :
Permet d’automatiser la détection dans du code


==================================================
PARTIE 3 : RÉDUCTION DE LA SURFACE D’ATTAQUE
==================================================

Explication :

L’objectif est d’empêcher les fuites avant qu’elles ne se produisent.


--------------------------------------------------
Utilisation de hooks pre-commit
--------------------------------------------------

Explication :

Avant d’envoyer du code sur GitHub, un scan automatique est effectué.

Exemple :

.pre-commit-config.yaml

- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v3.2.0
  hooks:
    - id: detect-aws-credentials
    - id: detect-private-key

Résultat :
Empêche de commit des clés sensibles


--------------------------------------------------
Bonnes pratiques de sécurité
--------------------------------------------------

- Ne jamais stocker les clés dans le code
- Utiliser des variables d’environnement
- Restreindre les permissions des clés
- Mettre une expiration sur les tokens
- Surveiller les logs
- Révoquer immédiatement les clés compromises


==================================================
CONCLUSION
==================================================

Les fuites d’API keys et de tokens sont dangereuses car elles permettent :

- Accès non autorisé aux services
- Vol de données
- Utilisation abusive (ex: coût cloud élevé)

Sources principales des fuites :

- Mauvaises pratiques de développement
- Manque de contrôle avant publication
- Mauvaise gestion des secrets

Objectif en cybersécurité :

Toujours protéger les secrets comme des mots de passe critiques et vérifier leur exposition en permanence."""