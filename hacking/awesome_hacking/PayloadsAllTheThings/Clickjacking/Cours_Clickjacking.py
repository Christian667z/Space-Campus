CONTENT = """\nCLICKJACKING - DÉTOURNEMENT D’INTERFACE UTILISATEUR

Définition pédagogique :

Le clickjacking est une attaque où un utilisateur est trompé pour cliquer sur quelque chose de différent de ce qu’il voit réellement.

Principe :
L’attaquant cache ou superpose des éléments invisibles sur une page web légitime.

Objectif :
Forcer l’utilisateur à effectuer des actions sans s’en rendre compte :
- cliquer sur “supprimer compte”
- valider un paiement
- liker ou commenter
- changer des paramètres sensibles


==================================================
PARTIE 1 : TECHNIQUES DE CLICKJACKING
==================================================


--------------------------------------------------
UI Redressing (détournement d’interface)
--------------------------------------------------

Explication :

L’attaquant recouvre une interface légitime avec une couche invisible contenant des actions malveillantes.

Principe :
L’utilisateur pense cliquer sur un bouton normal, mais clique en réalité sur un élément caché.

Exemple concret :

<div style="opacity:0; position:absolute; top:0; left:0; width:100%; height:100%;">
  <a href="site-malveillant">Clique ici</a>
</div>

Résultat :
L’utilisateur clique sans voir le lien réel


--------------------------------------------------
Invisible Frames (iframes invisibles)
--------------------------------------------------

Explication :

Une page légitime charge un site malveillant dans un iframe invisible.

Exemple concret :

<iframe src="site-malveillant" style="opacity:0; width:0; height:0;"></iframe>

Résultat :
Les actions se déroulent sur le site caché

Attaque typique :
- formulaire de login caché
- action bancaire invisible


--------------------------------------------------
Button / Form Hijacking
--------------------------------------------------

Explication :

L’attaquant fait croire à un utilisateur qu’il clique sur un bouton normal, mais déclenche une action cachée.

Exemple concret :

Bouton visible :
<button>Cliquer ici</button>

Formulaire caché :
<form action="transfer-money" style="display:none;">
</form>

Résultat :
Le clic déclenche une action non voulue


--------------------------------------------------
Méthodes d’exécution
--------------------------------------------------

Explication :

L’attaquant combine :
- éléments visibles (leurre)
- éléments invisibles (attaque)

Exemple :

1. Afficher un bouton “Play video”
2. Superposer un formulaire invisible
3. L’utilisateur clique → action exécutée

Résultat :
Transfert d’argent ou modification de compte


==================================================
PARTIE 2 : TECHNIQUES DE PERSUASION ET D’OBSCURCISSEMENT
==================================================


--------------------------------------------------
onBeforeUnload (anti-détection)
--------------------------------------------------

Explication :

Cette technique empêche ou ralentit la fermeture de la page pour garder l’utilisateur piégé.

Exemple concret :

window.onbeforeunload = function() {
    return "Voulez-vous quitter ?";
}

Résultat :
L’utilisateur hésite et reste sur la page


Version avancée :

L’attaquant force des rechargements constants pour bloquer la sortie


==================================================
PARTIE 3 : CONTRE-MESURES (DÉFENSE)
==================================================


--------------------------------------------------
X-Frame-Options
--------------------------------------------------

Explication :

Empêche une page d’être chargée dans un iframe.

Exemple :

Header:
X-Frame-Options: SAMEORIGIN

Effet :
Le site ne peut pas être intégré dans un site externe


--------------------------------------------------
Content Security Policy (CSP)
--------------------------------------------------

Explication :

Contrôle les sources autorisées (scripts, frames, etc.)

Exemple :

<meta http-equiv="Content-Security-Policy" content="frame-ancestors 'self';">

Effet :
Empêche les sites externes de charger la page en iframe


--------------------------------------------------
Désactivation JavaScript
--------------------------------------------------

Explication :

Certaines protections reposent sur JavaScript.

Si JS est désactivé :
- les protections peuvent être contournées
- les frame-busting scripts ne fonctionnent plus


Exemple :

<iframe src="site" sandbox></iframe>

Effet :
Limite les capacités du contenu chargé


==================================================
PARTIE 4 : CONTRE-MESURES CÔTÉ NAVIGATEUR
==================================================


--------------------------------------------------
XSS Filter (IE / Chrome anciens)
--------------------------------------------------

Explication :

Les anciens navigateurs tentaient de bloquer les scripts malveillants.

Problème :
Ces filtres peuvent casser les protections anti-clickjacking.

Exemple :
Un script de protection est modifié ou bloqué par erreur


==================================================
PARTIE 5 : ANALYSE DU CHALLENGE
==================================================

Code analysé :

<div style="position:absolute; opacity:0;">
  <iframe src="https://legitimate-site.com/login"></iframe>
</div>

<button onclick="document.getElementsByTagName('iframe')[0].contentWindow.location='malicious-site.com';">
Click me
</button>

Explication pédagogique :

1. Un iframe invisible charge un site légitime (login)
2. Le bouton visible semble inoffensif
3. Mais le clic redirige l’iframe vers un site malveillant

Vulnérabilité :

- L’utilisateur interagit avec un bouton normal
- Mais déclenche une redirection cachée
- L’iframe est manipulé sans consentement

Impact :

- Vol de session
- Phishing
- Redirection vers site malveillant


==================================================
CONCLUSION
==================================================

Le clickjacking repose sur un principe simple mais puissant :

Tromper la perception visuelle de l’utilisateur.

Risques :

- Actions non autorisées
- Vol de données
- Modification de compte
- Fraude

Bonnes pratiques :

- X-Frame-Options activé
- CSP (frame-ancestors)
- Désactiver les actions sensibles dans iframe
- Vérification côté serveur pour actions critiques

Objectif en cybersécurité :

Ne jamais faire confiance à l’interface utilisateur seule. Toujours valider les actions côté serveur.\n"""