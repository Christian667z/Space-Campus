CONTENT = """\nBUSINESS LOGIC ERRORS - ERREURS DE LOGIQUE MÉTIER

Définition pédagogique :

Les erreurs de logique métier sont des vulnérabilités qui ne viennent pas d’un bug technique classique (comme SQL injection ou XSS), mais d’une mauvaise conception des règles de fonctionnement de l’application.

La logique métier représente les règles du “monde réel” :
- Prix des produits
- Processus de paiement
- Conditions d’accès (premium, abonnement)
- Séquences d’actions

Problème :

L’application fonctionne comme prévu, mais un attaquant utilise ces règles d’une manière inattendue pour obtenir un avantage.

Objectif de l’attaquant :
Exploiter le fonctionnement normal pour :
- Réduire un prix
- Accéder gratuitement à des services
- Générer de l’argent
- Contourner des restrictions


==================================================
PARTIE 1 : MÉTHODOLOGIE GÉNÉRALE
==================================================

Contrairement aux failles techniques, ici il faut réfléchir comme un utilisateur malin.

Approche :

- Tester les limites du système
- Modifier les valeurs envoyées
- Changer l’ordre des actions
- Observer les incohérences


==================================================
PARTIE 2 : CAS PRATIQUES
==================================================


--------------------------------------------------
Test du système de reviews (avis)
--------------------------------------------------

Explication :

Les systèmes d’avis doivent garantir :
- Authenticité (avoir acheté le produit)
- Limite de notation

Tests à faire :

- Poster un avis sans achat
- Mettre une note invalide (0, 6, -1)
- Poster plusieurs avis avec le même compte
- Usurper l’identité d’un autre utilisateur
- Tester upload de fichiers (images malveillantes)
- Tester CSRF

Exemple concret :

Un utilisateur poste 100 avis positifs → manipulation de réputation


--------------------------------------------------
Test des codes promo
--------------------------------------------------

Explication :

Les codes promo doivent être limités et contrôlés.

Tests :

- Réutiliser le même code plusieurs fois
- Utiliser un code sur plusieurs comptes en même temps (race condition)
- Injecter plusieurs codes dans une requête
- Appliquer un code à un produit non éligible

Exemple concret :

code=DISCOUNT10&code=DISCOUNT10

Résultat :
Double réduction appliquée


--------------------------------------------------
Manipulation des frais de livraison
--------------------------------------------------

Explication :

Les frais doivent être strictement contrôlés côté serveur.

Tests :

- Mettre une valeur négative
- Modifier les paramètres

Exemple concret :

delivery_fee = -10

Résultat :
Le total diminue au lieu d’augmenter


--------------------------------------------------
Arbitrage de devises
--------------------------------------------------

Explication :

Exploiter les différences de taux de conversion.

Exemple concret :

1. Payer en USD
2. Demander un remboursement en EUR

Si les taux sont mal calculés → profit


--------------------------------------------------
Exploitation des fonctionnalités premium
--------------------------------------------------

Explication :

Les accès premium doivent être vérifiés côté serveur.

Tests :

- Accéder aux pages premium sans abonnement
- Modifier des valeurs (true/false)
- Vérifier cookies et localStorage

Exemple concret :

"isPremium": false → changer en true

Résultat :
Accès gratuit aux fonctionnalités premium


--------------------------------------------------
Exploitation des remboursements
--------------------------------------------------

Explication :

Le système de remboursement peut être abusé.

Tests :

- Garder un produit après remboursement
- Demander plusieurs remboursements

Exemple concret :

1. Acheter un produit
2. Demander remboursement
3. Le produit reste accessible

Résultat :
Produit gratuit


--------------------------------------------------
Exploitation panier / wishlist
--------------------------------------------------

Explication :

Le panier doit vérifier les quantités et les droits.

Tests :

- Ajouter une quantité négative
- Ajouter plus que le stock disponible
- Modifier le panier d’un autre utilisateur

Exemple concret :

quantité = -1

Résultat :
Réduction du prix total


--------------------------------------------------
Test des commentaires (threads)
--------------------------------------------------

Explication :

Les systèmes de commentaires doivent limiter les abus.

Tests :

- Poster un nombre illimité de commentaires
- Utiliser des race conditions
- Usurper un utilisateur privilégié

Exemple concret :

Un utilisateur spam des milliers de commentaires


--------------------------------------------------
Erreur d’arrondi (Rounding Error)
--------------------------------------------------

Explication :

Les erreurs de calcul peuvent créer ou détruire de l’argent.

Exemple concret :

Transaction :

0.000000005 BTC

Résultat :

- Débit arrondi à 0
- Crédit arrondi à 1 unité

Conséquence :
Création d’argent à partir de rien

Attaque :

Automatiser cette action → gains illimités


==================================================
CONCLUSION
==================================================

Les erreurs de logique métier sont dangereuses car :

- Elles ne sont pas détectées par les outils classiques
- Elles exploitent le fonctionnement normal
- Elles peuvent causer des pertes financières importantes

Causes principales :

- Mauvaise conception des règles
- Absence de validation côté serveur
- Manque de tests sur les cas limites

Bonnes pratiques :

- Toujours valider côté serveur
- Tester les cas extrêmes (valeurs négatives, limites)
- Vérifier les séquences d’actions
- Implémenter des contrôles anti-abus

Objectif en cybersécurité :

Comprendre comment fonctionne le système en profondeur pour identifier des comportements inattendus exploitables."""