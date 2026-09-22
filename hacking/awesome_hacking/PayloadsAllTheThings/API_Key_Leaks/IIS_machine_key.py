CONTENT = """\nIIS MACHINE KEYS - CLÉS MACHINE DANS IIS (ASP.NET)

Définition pédagogique :

Les machine keys sont des clés cryptographiques utilisées par ASP.NET (IIS) pour sécuriser plusieurs éléments importants :

- Les cookies d’authentification
- Le ViewState (état de la page)
- Les sessions utilisateur

Elles servent à :
- Vérifier l’intégrité des données (éviter les modifications)
- Chiffrer et déchiffrer des informations sensibles

Problème :
Si un attaquant récupère ces clés, il peut manipuler des données sécurisées, voire exécuter du code à distance (RCE).


==================================================
PARTIE 1 : VIEWSTATE
==================================================

Explication :

Le ViewState est un mécanisme qui permet à une page web ASP.NET de conserver des données entre deux requêtes (postback).

Il est stocké dans un champ caché HTML :

<input type="hidden" name="__VIEWSTATE" value="..." />

Formats possibles :

1. Base64 simple
   - Pas sécurisé
   - Pas de vérification d’intégrité

2. Base64 + MAC
   - Ajoute une signature pour vérifier l’intégrité

3. Base64 chiffré
   - Données chiffrées

Indice important :

Un ViewState non chiffré commence souvent par :
/wEP

Exemple concret :

Un attaquant inspecte le code HTML et récupère le __VIEWSTATE pour l’analyser


==================================================
PARTIE 2 : MACHINE KEY
==================================================

Explication :

La machineKey définit les clés et algorithmes utilisés pour sécuriser les données.

Structure :

<machineKey validationKey="..." decryptionKey="..." validation="SHA1" decryption="AES" />

Détails :

validationKey :
Clé utilisée pour signer les données (éviter la modification)

decryptionKey :
Clé utilisée pour chiffrer/déchiffrer

validation :
Algorithme de signature (SHA1, HMACSHA256, etc.)

decryption :
Algorithme de chiffrement (AES, DES, etc.)

Exemple concret :

Si un attaquant possède ces clés, il peut :
- Modifier un cookie
- Générer un faux ViewState valide


--------------------------------------------------
Emplacements des machine keys
--------------------------------------------------

Fichiers :

C:\Windows\Microsoft.NET\Framework\v4.0.30319\config\machine.config

C:\Windows\Microsoft.NET\Framework64\v4.0.30319\config\machine.config

Registre (si auto-généré) :

HKEY_CURRENT_USER\Software\Microsoft\ASP.NET\...


==================================================
PARTIE 3 : IDENTIFICATION DES MACHINE KEYS
==================================================

Explication :

Les développeurs utilisent parfois des clés connues ou faibles.

Un attaquant peut tester une liste de clés connues.

Exemple concret :

Utiliser un outil pour tester plusieurs clés :

viewstalker --viewstate /wEP... --machinekeys liste.txt

Résultat :
Si une clé correspond → vulnérabilité


==================================================
PARTIE 4 : DÉCODAGE DU VIEWSTATE
==================================================

Explication :

Décoder le ViewState permet de comprendre :

- S’il est chiffré
- S’il est signé
- Les données qu’il contient

Exemple concret :

viewgen --decode "VIEWSTATE"

Résultat :
Affiche les données internes


==================================================
PARTIE 5 : GÉNÉRATION DE VIEWSTATE MALVEILLANT (RCE)
==================================================

Explication :

Si un attaquant peut générer un ViewState valide, il peut injecter du code malveillant.

Conditions nécessaires :

- Avoir __VIEWSTATE
- Avoir __VIEWSTATEGENERATOR
- Connaître la machineKey (dans certains cas)


--------------------------------------------------
Cas 1 : MAC désactivé
--------------------------------------------------

Explication :

Aucune protection d’intégrité → attaque facile

Exemple concret :

Générer un ViewState avec une commande :

ysoserial.exe -g TypeConfuseDelegate -c "commande"


--------------------------------------------------
Cas 2 : MAC activé, chiffrement désactivé
--------------------------------------------------

Explication :

Le ViewState est signé mais pas chiffré

Attaque :

1. Trouver la validationKey
2. Générer un ViewState signé

Exemple :

ysoserial.exe -p ViewState -g TypeConfuseDelegate -c "commande" --validationkey=KEY


--------------------------------------------------
Cas 3 : MAC activé et chiffrement activé
--------------------------------------------------

Explication :

Le cas le plus sécurisé, mais toujours exploitable si les clés sont connues

Particularités :

- Avant .NET 4.5 → certaines failles permettent de contourner le chiffrement
- Après .NET 4.5 → sécurité renforcée mais dépend toujours des clés

Exemple concret :

ysoserial.exe avec paramètres de chiffrement et signature


==================================================
PARTIE 6 : MODIFICATION DES COOKIES
==================================================

Explication :

Les cookies d’authentification ASP.NET sont protégés avec la machineKey.

Si un attaquant possède la clé :

- Il peut déchiffrer un cookie
- Modifier les données (ex: rôle admin)
- Rechiffrer et réutiliser

Exemple concret :

1. Déchiffrer un cookie
2. Modifier :
   role=user → role=admin
3. Rechiffrer et envoyer


==================================================
CONCLUSION
==================================================

Les machine keys sont critiques pour la sécurité ASP.NET.

Risques principaux :

- Exécution de code à distance (RCE)
- Vol de session
- Escalade de privilèges

Causes des vulnérabilités :

- Clés faibles ou connues
- Mauvaise configuration
- ViewState non sécurisé

Bonnes pratiques :

- Utiliser des clés longues et aléatoires
- Activer MAC et chiffrement
- Ne jamais exposer les clés
- Mettre à jour .NET (>= 4.5)
- Désactiver ViewState si inutile

Objectif en cybersécurité :

Toujours vérifier comment les données sont protégées et si les mécanismes cryptographiques sont correctement implémentés."""