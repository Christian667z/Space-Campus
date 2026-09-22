CONTENT = """\nCLIENT-SIDE PATH TRAVERSAL (CSPT) – EXPLICATION PÉDAGOGIQUE

Le Client-Side Path Traversal est une vulnérabilité qui apparaît dans les applications web modernes lorsque le navigateur construit des requêtes HTTP en utilisant des données contrôlées par l’utilisateur.

Contrairement aux path traversal classiques côté serveur (comme ../../etc/passwd), ici l’exploitation se produit côté navigateur (client), avant même que la requête n’arrive au serveur.

Le problème principal vient du fait que JavaScript utilise des fonctions comme fetch() pour construire des requêtes dynamiques vers des endpoints internes de l’application.

Si les paramètres utilisés dans l’URL ne sont pas correctement encodés ou validés, un attaquant peut injecter des séquences comme ../ afin de modifier la route finale appelée par l’application.

------------------------------------------------------------

FONCTIONNEMENT GÉNÉRAL

Dans une application web moderne :

- Le frontend appelle une API interne via fetch()
- L’URL est construite avec des paramètres utilisateur
- Le navigateur ajoute automatiquement cookies et tokens d’authentification
- La requête est envoyée au backend

Si un paramètre est manipulé, l’attaquant peut rediriger cette requête vers une autre route interne non prévue.

------------------------------------------------------------

EXEMPLE SIMPLE DE CSPT

Une application contient :

https://example.com/news?newsid=123

Le JavaScript fait :

fetch("/api/news/" + newsid)

Donc :

/news/123 est appelé normalement

Mais si l’attaquant injecte :

newsid=../admin/config

La requête devient :

/api/news/../admin/config

Après normalisation du chemin :

/api/admin/config

Résultat :
Le navigateur a appelé une route sensible sans intention utilisateur.

------------------------------------------------------------

CSPT VERS XSS

Le CSPT peut être transformé en XSS si la redirection atteint un fichier JavaScript ou une page interprétée.

Exemple :

https://example.com/page?file=../static/app.js?cb=alert(document.domain)

Si le paramètre est injecté dans un script exécuté, l’attaquant peut provoquer l’exécution de JavaScript.

Le point important :
Le CSPT ne déclenche pas directement XSS, mais il permet d’atteindre des fichiers ou endpoints injectables.

------------------------------------------------------------

CSPT VERS CSRF

Le CSPT devient encore plus dangereux lorsqu’il est utilisé pour contourner les protections CSRF.

Normalement :

- Le CSRF nécessite une requête forgée depuis un autre site
- Les cookies SameSite et tokens CSRF bloquent cela

Mais avec CSPT :

- La requête est initiée depuis le frontend légitime
- Le navigateur inclut automatiquement cookies et tokens
- Les protections CSRF deviennent inutiles

Donc CSPT permet :

- Modifier des données utilisateur
- Exécuter des actions sensibles
- Contourner les protections SameSite=Lax

------------------------------------------------------------

SCÉNARIO RÉEL CSPT2CSRF

Une application de chat utilise :

fetch("/api/channel/" + channelId)

L’attaquant injecte :

../../api/admin/deleteUser

Résultat :

La requête est envoyée avec session utilisateur valide
L’action admin est exécutée

------------------------------------------------------------

OUTILS UTILISÉS

Un outil important est CSPTBurpExtension.

Il permet :

- Détecter les injections dans les chemins
- Tester les ../ dans les paramètres
- Identifier les endpoints vulnérables côté client

------------------------------------------------------------

LABORATOIRES D’ENTRAÎNEMENT

CSPTPlayground permet de simuler :

- Injection dans fetch()
- Manipulation des chemins
- Redirections internes

Root-Me propose aussi des challenges pour comprendre la logique.

------------------------------------------------------------

MÉTHODOLOGIE D’EXPLOITATION

Étapes typiques :

1. Identifier une requête fetch() ou API dynamique
2. Repérer un paramètre utilisateur injecté dans l’URL
3. Tester ../ ou encodages similaires
4. Observer la normalisation du chemin
5. Vérifier si la requête atteint un endpoint sensible
6. Tester si cookies/session sont automatiquement inclus

------------------------------------------------------------

CAS AVANCÉS

Le CSPT peut aussi apparaître dans :

- Plugins JSON API
- Systèmes de notifications internes
- Applications SPA (React, Vue, Angular)
- Microservices appelés via frontend

------------------------------------------------------------

EXEMPLE DE FAILLE RÉELLE

Dans certaines applications comme Grafana ou Mattermost :

- Le frontend construit des URLs dynamiques
- Les paramètres sont concaténés sans validation
- Les attaques permettent de rediriger vers des API internes

Cela peut mener à :

- Lecture de données sensibles
- Suppression de ressources
- Modification de configuration

------------------------------------------------------------

DIFFÉRENCE AVEC PATH TRAVERSAL CLASSIQUE

Path Traversal classique :
- Exploitation côté serveur
- Accès fichiers système
- Exemple : ../../etc/passwd

CSPT :
- Exploitation côté client
- Manipulation de requêtes API
- Impact sur authentification et logique applicative

------------------------------------------------------------

CONCLUSION PÉDAGOGIQUE

Le CSPT est une vulnérabilité moderne liée aux architectures frontend-heavy.

Il est dangereux car :

- Il contourne les protections CSRF
- Il exploite la logique du frontend
- Il abuse de la confiance du navigateur
- Il peut rediriger des requêtes authentifiées

Comprendre CSPT est essentiel pour analyser les applications modernes basées sur SPA et API."""