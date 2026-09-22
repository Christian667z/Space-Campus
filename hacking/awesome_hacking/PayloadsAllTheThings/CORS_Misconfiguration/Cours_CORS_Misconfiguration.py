CONTENT = """\nCORS MISCONFIGURATION - MAUVAISE CONFIGURATION DU PARTAGE DE RESSOURCES INTER-ORIGINES

Définition pédagogique :

CORS (Cross-Origin Resource Sharing) est un mécanisme de sécurité du navigateur qui contrôle quelles origines peuvent accéder à des ressources d’une API.

Une mauvaise configuration CORS signifie que le serveur autorise des origines non fiables à accéder à des données sensibles.

Impact :
- vol de données utilisateur
- accès aux API authentifiées
- exfiltration de cookies ou tokens
- prise de contrôle de compte dans certains cas


==================================================
PARTIE 1 : FONCTIONNEMENT DE BASE DE CORS
==================================================


--------------------------------------------------
Principe de CORS
--------------------------------------------------

Explication :

Lorsqu’un site web fait une requête vers un autre domaine, le navigateur vérifie les règles CORS.

Le serveur peut répondre avec des headers comme :

- Access-Control-Allow-Origin
- Access-Control-Allow-Credentials

Exemple :

Access-Control-Allow-Origin: https://site-legitime.com
Access-Control-Allow-Credentials: true

Résultat :
Le navigateur autorise ou bloque l’accès aux données.


--------------------------------------------------
Pourquoi c’est important
--------------------------------------------------

Explication :

Sans CORS, un site malveillant pourrait lire les réponses d’autres sites avec la session de l’utilisateur.

CORS sert donc de barrière entre les sites web.


==================================================
PARTIE 2 : TYPES DE MAUVAISES CONFIGURATIONS
==================================================


--------------------------------------------------
Origin Reflection (réflexion de l’origine)
--------------------------------------------------

Explication :

Le serveur accepte n’importe quelle origine et la renvoie directement dans la réponse.

Cela revient à dire :
"Je fais confiance à tout le monde".

Exemple :

Requête :
Origin: https://evil.com

Réponse :
Access-Control-Allow-Origin: https://evil.com
Access-Control-Allow-Credentials: true

Impact :
Le site attaquant peut lire les données de la victime connectée.


Exemple concret :

Un script JavaScript sur le site attaquant envoie une requête vers l’API victime.

Il récupère la réponse contenant des données sensibles et les envoie à l’attaquant.


--------------------------------------------------
Null Origin
--------------------------------------------------

Explication :

Certains serveurs acceptent l’origine "null".

Cela arrive souvent avec :
- iframe sandbox
- fichiers locaux
- data URI

Exemple :

Origin: null
Access-Control-Allow-Origin: null

Impact :
Un attaquant peut forcer le navigateur à utiliser une origine "null" et contourner la sécurité.


Exemple concret :

Utilisation d’un iframe sandbox pour exécuter un script qui envoie une requête authentifiée vers l’API.


--------------------------------------------------
Wildcard (*)
--------------------------------------------------

Explication :

Le serveur répond avec :

Access-Control-Allow-Origin: *

Cela signifie :
"tout le monde peut accéder à cette ressource"

Limite importante :
Avec "*", les cookies ne sont pas envoyés si credentials sont activés.

Impact :
- fuite de données publiques
- accès non protégé aux API internes mal sécurisées


Exemple concret :

Un script JavaScript appelle une API interne et récupère des données sans authentification.


--------------------------------------------------
CORS avec credentials activés
--------------------------------------------------

Explication :

Access-Control-Allow-Credentials: true permet d’envoyer cookies et sessions.

Si combiné avec une mauvaise validation des origines :
→ attaque critique

Impact :
- vol de session utilisateur
- accès compte utilisateur complet


==================================================
PARTIE 3 : SCÉNARIOS D’EXPLOITATION
==================================================


--------------------------------------------------
Exploitation via JavaScript
--------------------------------------------------

Explication :

Un site attaquant exécute un script qui :
1. envoie une requête vers l’API victime
2. récupère la réponse
3. exfiltre les données vers un serveur externe

Exemple logique :

- XMLHttpRequest avec withCredentials = true
- récupération de données sensibles
- envoi vers serveur attaquant


--------------------------------------------------
Exploitation via iframe / sandbox
--------------------------------------------------

Explication :

Un iframe sandbox peut forcer l’origine "null".

Cela permet de contourner certaines restrictions CORS mal configurées.

Impact :
accès à des endpoints protégés si CORS est faible


--------------------------------------------------
XSS sur origine de confiance
--------------------------------------------------

Explication :

Si une origine est autorisée par CORS et qu’elle contient une faille XSS :
→ l’attaquant peut exploiter CORS indirectement

Impact :
- contournement complet de la whitelist CORS
- exfiltration de données utilisateur


==================================================
PARTIE 4 : ERREURS FRÉQUENTES DES DÉVELOPPEURS
==================================================


--------------------------------------------------
Mauvaise validation des origines
--------------------------------------------------

Explication :

Les développeurs utilisent parfois des regex incorrectes.

Exemple :
accepter evilexample.com car il contient example.com

Impact :
attaque par domaine similaire (typosquatting)


--------------------------------------------------
Regex mal échappée
--------------------------------------------------

Explication :

Une validation comme :
^api.example.com$

peut être mal interprétée si le point n’est pas échappé.

Impact :
contournement via apiiexample.com


--------------------------------------------------
Utilisation de *
--------------------------------------------------

Explication :

Mettre "*" est simple mais dangereux si API sensible.

Impact :
exposition totale des données si pas d’authentification correcte


==================================================
PARTIE 5 : IMPACTS DE SÉCURITÉ
==================================================

Une mauvaise configuration CORS peut entraîner :

- vol de données personnelles
- accès API interne
- détournement de session
- lecture de données privées
- pivot vers réseau interne dans certains cas

Gravité :
Élevée à critique selon les endpoints exposés


==================================================
PARTIE 6 : BONNES PRATIQUES DE SÉCURITÉ
==================================================


--------------------------------------------------
Whitelist stricte
--------------------------------------------------

Autoriser uniquement des domaines précis et validés.


--------------------------------------------------
Ne jamais utiliser *
--------------------------------------------------

Surtout si credentials sont activés.


--------------------------------------------------
Validation correcte des origins
--------------------------------------------------

- éviter regex permissives
- éviter matching partiel de domaine


--------------------------------------------------
Désactiver credentials si inutile
--------------------------------------------------

Access-Control-Allow-Credentials: false


--------------------------------------------------
Séparer API publique et privée
--------------------------------------------------

- API publique sans données sensibles
- API privée avec authentification stricte


==================================================
CONCLUSION
==================================================

CORS est une protection du navigateur, pas une protection serveur.

Une mauvaise configuration transforme un mécanisme de sécurité en faille critique permettant :
- accès non autorisé
- vol de données
- exploitation via navigateur

La sécurité réelle doit toujours être assurée côté serveur, pas uniquement via CORS."""