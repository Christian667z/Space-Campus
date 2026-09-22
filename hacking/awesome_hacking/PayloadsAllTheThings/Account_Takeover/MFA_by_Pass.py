CONTENT = """\nMFA BYPASSES - CONTOURNEMENT DE L’AUTHENTIFICATION MULTI-FACTEURS

Définition pédagogique :

L’authentification multi-facteurs (MFA ou 2FA) est une méthode de sécurité qui demande plusieurs preuves d’identité avant d’autoriser l’accès à un compte.

Les 3 types de facteurs :
- Ce que tu connais : mot de passe
- Ce que tu possèdes : téléphone, token
- Ce que tu es : empreinte, reconnaissance faciale

Objectif :
Même si le mot de passe est compromis, l’attaquant ne peut pas accéder au compte sans le second facteur.

Cependant, si la mise en place est mal faite, il est possible de contourner cette protection.


==================================================
PARTIE 1 : TECHNIQUES DE CONTOURNEMENT DU 2FA
==================================================


--------------------------------------------------
Manipulation de réponse (Response Manipulation)
--------------------------------------------------

Explication :

Le serveur renvoie une réponse JSON indiquant si le code 2FA est valide ou non.

Exemple :

Réponse normale :
{
  "success": false
}

Si l’application côté client (frontend) ne vérifie que cette réponse, un attaquant peut la modifier.

Exemple concret :

Dans Burp Suite, modifier la réponse en :
{
  "success": true
}

Résultat :
Accès accordé sans vérifier réellement le code


--------------------------------------------------
Manipulation du code de statut HTTP
--------------------------------------------------

Explication :

Le serveur renvoie un code HTTP indiquant une erreur (ex: 401, 403).

Si l’application accepte un code 200 OK, cela peut contourner la sécurité.

Exemple concret :

Réponse originale :
HTTP 401 Unauthorized

Attaquant modifie en :
HTTP 200 OK

Résultat :
Le système peut accepter la requête


--------------------------------------------------
Fuite du code 2FA dans la réponse
--------------------------------------------------

Explication :

Parfois, le serveur renvoie le code OTP dans sa réponse (erreur de développement).

Exemple concret :

Réponse JSON :
{
  "otp": "839201"
}

L’attaquant récupère directement le code


--------------------------------------------------
Analyse des fichiers JavaScript
--------------------------------------------------

Explication :

Certains fichiers JS contiennent des informations sensibles sur la logique du 2FA.

Exemple concret :

Un fichier JS peut contenir :
- Le format du code
- La longueur
- Une logique de validation

Cela aide à construire une attaque


--------------------------------------------------
Réutilisation du code 2FA
--------------------------------------------------

Explication :

Un code OTP doit être utilisé une seule fois.

Si le système accepte plusieurs utilisations, c’est une faille.

Exemple concret :

Code OTP : 123456

Si ce code fonctionne plusieurs fois → vulnérabilité


--------------------------------------------------
Absence de protection contre le brute force
--------------------------------------------------

Explication :

Si aucune limite de tentative n’est mise en place, l’attaquant peut tester tous les codes possibles.

Exemple concret :

Code OTP à 6 chiffres :
000000 → 999999

Avec un script automatisé, l’attaquant peut trouver le bon code


--------------------------------------------------
Absence de vérification d’intégrité du code 2FA
--------------------------------------------------

Explication :

Le code OTP doit être lié à un utilisateur spécifique.

Si ce n’est pas le cas, un code valide peut fonctionner pour plusieurs comptes.

Exemple concret :

Un attaquant génère un OTP sur son compte et l’utilise pour accéder au compte d’une victime


--------------------------------------------------
CSRF sur la désactivation du 2FA
--------------------------------------------------

Explication :

Si la désactivation du 2FA n’est pas protégée contre les attaques CSRF, un attaquant peut forcer un utilisateur à désactiver son 2FA.

Exemple concret :

Une page malveillante contient un formulaire automatique qui envoie :

POST /disable-2fa

Résultat :
Le 2FA est désactivé sans que la victime le sache


--------------------------------------------------
Réinitialisation du mot de passe désactive le 2FA
--------------------------------------------------

Explication :

Certains systèmes désactivent le 2FA après un changement de mot de passe.

Exemple concret :

1. Attaquant réinitialise le mot de passe
2. Le 2FA est automatiquement désactivé
3. Accès complet au compte


--------------------------------------------------
Abus des codes de secours (Backup Codes)
--------------------------------------------------

Explication :

Les backup codes permettent d’accéder au compte si l’utilisateur perd son téléphone.

Failles possibles :

- Codes réutilisables
- Pas d’expiration
- Validation faible

Exemple concret :

Un attaquant teste plusieurs backup codes jusqu’à trouver un valide


--------------------------------------------------
Clickjacking sur la désactivation du 2FA
--------------------------------------------------

Explication :

Le clickjacking consiste à piéger un utilisateur en superposant une interface invisible.

Exemple concret :

Une page malveillante affiche un bouton "Play", mais en réalité l’utilisateur clique sur "Désactiver 2FA"


--------------------------------------------------
Sessions actives non invalidées après activation du 2FA
--------------------------------------------------

Explication :

Quand un utilisateur active le 2FA, toutes les sessions existantes devraient être invalidées.

Sinon, un attaquant ayant déjà une session peut rester connecté.

Exemple concret :

1. Attaquant vole un cookie de session
2. L’utilisateur active le 2FA
3. La session de l’attaquant reste valide


--------------------------------------------------
Contournement via navigation forcée (Force Browsing)
--------------------------------------------------

Explication :

L’application redirige vers une page protégée après login.

Si les contrôles sont faibles, on peut accéder directement à la page sans valider le 2FA.

Exemple concret :

URL normale :
/2fa/verify

Attaquant remplace par :
/my-account

Résultat :
Accès direct sans vérification


--------------------------------------------------
Bypass avec null ou 000000
--------------------------------------------------

Explication :

Certains systèmes acceptent des valeurs par défaut.

Exemple concret :

Entrer :
000000

ou

null

Résultat :
Authentification acceptée si validation incorrecte


--------------------------------------------------
Bypass avec tableau (array injection)
--------------------------------------------------

Explication :

Au lieu d’envoyer un seul code, l’attaquant en envoie plusieurs dans un tableau.

Exemple concret :

{
  "otp": [
    "1234",
    "1111",
    "1337",
    "2222"
  ]
}

Si le serveur valide un des codes sans vérifier correctement, l’accès est accordé


==================================================
CONCLUSION
==================================================

Les failles de 2FA proviennent souvent de :

- Mauvaise validation côté serveur
- Logique uniquement côté client
- Absence de protections (CSRF, brute force)
- Mauvaise gestion des sessions

Bonnes pratiques :

- Vérification stricte côté serveur
- Limitation des tentatives (rate limiting)
- OTP à usage unique et expirables
- Liaison OTP ↔ utilisateur
- Protection CSRF
- Invalidation des sessions après changement critique

Objectif en cybersécurité :

Ne jamais supposer qu’une sécurité est fiable. Toujours tester sa robustesse face à des manipulations."""