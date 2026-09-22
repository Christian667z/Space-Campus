CONTENT = """\nBRUTE FORCE ET RATE LIMIT - ATTAQUES PAR FORCE BRUTE ET LIMITATION DE TAUX

Définition pédagogique :

Le brute force est une technique d’attaque qui consiste à tester un grand nombre de combinaisons (mots de passe, tokens, codes OTP) jusqu’à trouver la bonne.

Le rate limit est un mécanisme de défense qui limite le nombre de requêtes qu’un utilisateur peut envoyer dans un certain laps de temps.

Objectif de l’attaquant :
Contourner ces protections pour tester un maximum de combinaisons sans être bloqué.


==================================================
PARTIE 1 : BRUTE FORCE
==================================================

Explication :

Le brute force repose sur l’automatisation. L’attaquant envoie des milliers voire des millions de requêtes.

Exemples de cibles :

- Formulaire de connexion (username/password)
- Code OTP (2FA)
- Tokens de reset
- Identifiants utilisateur

Exemple concret :

Tester tous les mots de passe possibles pour un utilisateur :

admin / 123456
admin / password
admin / admin123

Si aucune protection n’est en place → accès compromis


--------------------------------------------------
Burp Suite Intruder
--------------------------------------------------

Explication :

Burp Intruder permet d’automatiser des attaques sur des paramètres HTTP.

Types d’attaques :


1. Sniper

Explication :

Un seul paramètre est testé avec plusieurs valeurs.

Exemple :

username=admin
password=1234, 12345, 123456

Résultat :
Teste plusieurs mots de passe pour un seul utilisateur


2. Battering Ram

Explication :

Même valeur envoyée sur plusieurs champs.

Exemple :

username=admin, password=admin
username=test, password=test

Utilité :
Tester des identifiants identiques


3. Pitchfork

Explication :

Deux listes sont utilisées en parallèle.

Exemple :

username1 / password1
username2 / password2

Utilité :
Tester des couples déjà connus


4. Cluster Bomb

Explication :

Teste toutes les combinaisons possibles entre plusieurs listes.

Exemple :

admin / 1234
admin / 12345
user / 1234
user / 12345

C’est l’attaque la plus puissante mais aussi la plus lente


--------------------------------------------------
FFUF (Fuzz Faster U Fool)
--------------------------------------------------

Explication :

FFUF est un outil rapide pour automatiser des attaques sur des applications web.

Exemple concret :

Tester plusieurs combinaisons :

ffuf -w usernames.txt:USER -w passwords.txt:PASS \
-u https://target/login \
-X POST \
-d "username=USER&password=PASS"

Résultat :
Teste automatiquement toutes les combinaisons


==================================================
PARTIE 2 : RATE LIMIT ET CONTournement
==================================================

Explication :

Le rate limiting bloque ou ralentit les requêtes après un certain seuil.

Exemple :
5 tentatives par minute → blocage


--------------------------------------------------
HTTP Pipelining
--------------------------------------------------

Explication :

Permet d’envoyer plusieurs requêtes sans attendre les réponses.

Utilité :
Augmenter la vitesse d’attaque


--------------------------------------------------
TLS Fingerprinting (JA3)
--------------------------------------------------

Explication :

JA3 identifie un client via son empreinte TLS.

Même si tu changes ton User-Agent, ton empreinte TLS peut te trahir.

Exemple :

Burp Suite → JA3 spécifique
Tor → JA3 différent

Contournement :

- Utiliser un vrai navigateur automatisé
- Modifier l’empreinte TLS
- Utiliser curl modifié


--------------------------------------------------
Réseau IPv4 (rotation d’IP)
--------------------------------------------------

Explication :

Le rate limit est souvent basé sur l’adresse IP.

Solution :
Utiliser plusieurs proxies

Exemple concret :

Configurer proxychains :

random_chain
chain_len = 1

Liste de proxies :

socks5 127.0.0.1 1080
http proxy1.com 8080

Résultat :
Chaque requête vient d’une IP différente


--------------------------------------------------
Réseau IPv6
--------------------------------------------------

Explication :

IPv6 offre un nombre énorme d’adresses.

Exemple :

Un bloc /64 contient :
18 trillions d’adresses

Utilité :
Changer d’IP à chaque requête sans limite


==================================================
PARTIE 3 : CONTRE-MESURES (DÉFENSE)
==================================================

Pour se protéger contre le brute force :

- Rate limiting strict
- Blocage après plusieurs tentatives
- CAPTCHA
- MFA (2FA)
- Mots de passe forts
- Détection comportementale


==================================================
CONCLUSION
==================================================

Le brute force est une attaque simple mais efficace si les protections sont faibles.

Points critiques :

- Absence de limitation de requêtes
- Mots de passe faibles
- Mauvaise détection des attaques

Techniques d’attaque :

- Automatisation (Burp, FFUF)
- Rotation d’IP
- Contournement du fingerprinting

Objectif en cybersécurité :

Toujours limiter, surveiller et détecter les comportements anormaux pour empêcher les attaques automatisées."""