CONTENT = """\nCRLF INJECTION - INJECTION CARRIAGE RETURN / LINE FEED

Définition pédagogique :

Une injection CRLF est une vulnérabilité web où un attaquant injecte des caractères spéciaux de fin de ligne dans une requête ou une réponse HTTP.

CR (Carriage Return) = retour au début de la ligne (\r)
LF (Line Feed) = passage à la ligne suivante (\n)

Dans HTTP, ces caractères servent à séparer les en-têtes.

Impact :
- manipulation de headers HTTP
- création de réponses falsifiées
- détournement de session
- XSS
- redirections forcées
- cache poisoning


==================================================
PARTIE 1 : PRINCIPE DE FONCTIONNEMENT
==================================================


--------------------------------------------------
Comment fonctionne une réponse HTTP
--------------------------------------------------

Explication :

Une réponse HTTP est structurée avec :
- headers
- ligne vide
- body (contenu)

Exemple :

HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: sessionid=abc123

<html>page</html>


--------------------------------------------------
Principe de l’injection CRLF
--------------------------------------------------

Explication :

Si un attaquant injecte \r\n dans une entrée utilisateur, il peut casser la structure HTTP.

Il peut alors :
- ajouter de nouveaux headers
- modifier la réponse
- injecter du contenu


==================================================
PARTIE 2 : TYPES D’ATTAQUES
==================================================


--------------------------------------------------
Session Fixation
--------------------------------------------------

Explication :

L’attaquant injecte un header Set-Cookie pour forcer une valeur de session.

Exemple vulnérable :

Input utilisateur :
value\r\nSet-Cookie: admin=true

Résultat :

Set-Cookie: sessionid=value
Set-Cookie: admin=true

Impact :
- élévation de privilèges
- détournement de session


--------------------------------------------------
Cross-Site Scripting via CRLF
--------------------------------------------------

Explication :

CRLF permet de modifier le body de la réponse et injecter du HTML ou JavaScript.

Impact :
- XSS
- phishing
- exécution de scripts malveillants


Exemple conceptuel :

Un paramètre URL est injecté avec des caractères CRLF.

Le serveur construit une réponse falsifiée contenant du HTML injecté comme :

<html>You have been Phished</html>


--------------------------------------------------
Désactivation de protections XSS
--------------------------------------------------

Explication :

Un attaquant peut injecter un header de sécurité falsifié.

Exemple :

X-XSS-Protection: 0

Impact :
- désactivation du filtre XSS du navigateur
- facilitation de l’exécution de scripts malveillants


--------------------------------------------------
Open Redirect
--------------------------------------------------

Explication :

L’injection CRLF permet d’ajouter un header Location.

Exemple :

Location: http://site-attaquant.com

Impact :
- redirection forcée
- phishing
- vol de crédibilité du site


==================================================
PARTIE 3 : CAS D’EXPLOITATION AVANCÉS
==================================================


--------------------------------------------------
Réécriture complète de la réponse HTTP
--------------------------------------------------

Explication :

Dans les cas critiques, l’attaquant peut injecter :
- headers
- nouveau body
- structure HTTP complète

Impact :
- page totalement falsifiée
- phishing avancé
- contrôle visuel de la réponse


--------------------------------------------------
Cache Poisoning
--------------------------------------------------

Explication :

Une réponse modifiée peut être stockée dans un cache proxy.

Impact :
- contenu malveillant servi à d’autres utilisateurs
- persistance de l’attaque


==================================================
PARTIE 4 : CONTOURNEMENT DES FILTRES
==================================================


--------------------------------------------------
Filtrage des caractères
--------------------------------------------------

Explication :

Les serveurs bloquent souvent \r et \n.

Mais certains systèmes :
- mal filtrent
- ou acceptent des encodages alternatifs


--------------------------------------------------
Encodage UTF-8
--------------------------------------------------

Explication :

Certains caractères Unicode peuvent être interprétés comme CR ou LF après décodage.

Impact :
- contournement des filtres
- injection indirecte


Exemple pédagogique :
caractères Unicode contenant des équivalents de saut de ligne


==================================================
PARTIE 5 : IMPACTS DE SÉCURITÉ
==================================================

Une vulnérabilité CRLF peut permettre :

- vol de session via cookies injectés
- XSS dans la réponse HTTP
- redirection vers sites malveillants
- manipulation de headers de sécurité
- empoisonnement de cache
- création de pages de phishing

Gravité :
moyenne à critique selon le contexte


==================================================
PARTIE 6 : BONNES PRATIQUES DE SÉCURITÉ
==================================================


--------------------------------------------------
Validation des entrées utilisateur
--------------------------------------------------

Ne jamais permettre :
- \r
- \n
dans les paramètres utilisés dans les headers


--------------------------------------------------
Encodage des données
--------------------------------------------------

Toutes les données utilisateur doivent être :
- échappées
- encodées
- filtrées avant insertion dans les headers


--------------------------------------------------
Utilisation de frameworks sécurisés
--------------------------------------------------

Les frameworks modernes gèrent automatiquement :
- séparation headers/body
- encodage sécurisé


--------------------------------------------------
Éviter la construction manuelle de headers
--------------------------------------------------

Ne jamais construire des headers HTTP avec concaténation directe de données utilisateur


==================================================
CONCLUSION
==================================================

CRLF injection est une vulnérabilité liée à une mauvaise séparation des données dans HTTP.

Elle permet de :
- modifier les réponses serveur
- injecter des headers
- détourner des sessions
- créer des attaques XSS ou phishing

C’est une faille de type “structure de protocole”, donc très dangereuse car elle casse le fonctionnement même du HTTP."""