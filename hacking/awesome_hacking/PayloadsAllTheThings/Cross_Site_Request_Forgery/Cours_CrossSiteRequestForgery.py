CONTENT = """\nCross-Site Request Forgery (CSRF)

Définition :

La Cross-Site Request Forgery (CSRF / XSRF) est une attaque qui force un utilisateur final à exécuter des actions non désirées sur une application web dans laquelle il est actuellement authentifié.

Les attaques CSRF ciblent principalement les requêtes qui modifient des données (actions d’état), et non le vol de données, car l’attaquant ne peut pas voir la réponse de la requête forgée. - OWASP


Résumé :

Outils
Méthodologie
HTML GET - nécessitant une interaction utilisateur
HTML GET - sans interaction utilisateur
HTML POST - nécessitant une interaction utilisateur
HTML POST - auto-submit sans interaction utilisateur
HTML POST multipart/form-data avec upload de fichier
JSON GET simple
JSON POST simple
JSON POST complexe
Labs
Références


Outils :

XSRFProbe : outil d’audit et d’exploitation CSRF


Méthodologie :

Quand tu es connecté à un site, tu as une session.
L’identifiant de session est stocké dans un cookie et envoyé à chaque requête.

Même si un autre site déclenche la requête, le cookie est envoyé automatiquement.
Donc le site croit que c’est l’utilisateur qui agit.

(Principe fondamental : confiance automatique des cookies)


HTML GET - nécessitant interaction utilisateur :

<a href="http://www.example.com/api/setusername?username=CSRFd">Clique ici</a>

Explication :
L’utilisateur doit cliquer pour déclencher l’action.


HTML GET - sans interaction utilisateur :

<img src="http://www.example.com/api/setusername?username=CSRFd">

Explication :
La requête se lance automatiquement au chargement de la page.


HTML POST - nécessitant interaction utilisateur :

<form action="http://www.example.com/api/setusername" enctype="text/plain" method="POST">
 <input name="username" type="hidden" value="CSRFd" />
 <input type="submit" value="Envoyer" />
</form>

Explication :
L’utilisateur doit cliquer sur le bouton.


HTML POST - auto submit sans interaction :

<form id="autosubmit" action="http://www.example.com/api/setusername" enctype="text/plain" method="POST">
 <input name="username" type="hidden" value="CSRFd" />
</form>

<script>
document.getElementById("autosubmit").submit();
</script>

Explication :
Le formulaire est envoyé automatiquement via JavaScript.


HTML POST multipart/form-data avec upload :

Script qui crée un fichier et l’envoie automatiquement via formulaire caché.

Explication :
Permet de simuler un upload de fichier sans consentement réel.


JSON GET simple :

Script JS qui envoie une requête GET API.

Explication :
Permet de récupérer des infos utilisateur (si pas protégé).


JSON POST simple :

Utilisation de XMLHttpRequest avec Content-Type modifié.

Explication :
Tentative d’envoyer du JSON malgré restrictions navigateur.


JSON POST complexe :

xhr.withCredentials = true

Explication :
Permet d’envoyer cookies + requête API authentifiée.


Labs :

Exercices PortSwigger CSRF :
- sans protection
- token non lié session
- validation referer faible
etc.


Références :

OWASP CSRF
articles de recherche sécurité web
cas réels PayPal, Facebook, Messenger


Conclusion pédagogique :

La CSRF exploite une faiblesse simple :

le navigateur envoie automatiquement les cookies.

Donc :
si une action sensible n’a pas de protection (token CSRF, vérification origine),
elle peut être exécutée à distance sans consentement utilisateur.


Reflexion importante :

CSRF n’est pas un bug complexe,
c’est un problème de confiance mal contrôlée entre navigateur et serveur.

La défense doit toujours être côté serveur, pas côté interface."""