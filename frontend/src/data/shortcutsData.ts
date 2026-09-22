export const EXCEL_SHORTCUTS = [
  {
    "key": "F4",
    "action": "Fixer une cellule (référence absolue $A$1)",
    "niveau": "Essentiel"
  },
  {
    "key": "Alt + =",
    "action": "Somme automatique instantanée",
    "niveau": "Essentiel"
  },
  {
    "key": "Ctrl + ;",
    "action": "Insérer la date du jour",
    "niveau": "Essentiel"
  },
  {
    "key": "Ctrl + Shift + :",
    "action": "Insérer l'heure actuelle",
    "niveau": "Essentiel"
  },
  {
    "key": "Ctrl + T",
    "action": "Créer un tableau structuré",
    "niveau": "Intermédiaire"
  },
  {
    "key": "Ctrl + Shift + L",
    "action": "Activer/désactiver les filtres",
    "niveau": "Intermédiaire"
  },
  {
    "key": "Alt + H + O + I",
    "action": "Ajuster la largeur des colonnes automatiquement",
    "niveau": "Intermédiaire"
  },
  {
    "key": "Ctrl + Page Up/Down",
    "action": "Naviguer entre les feuilles",
    "niveau": "Basique"
  },
  {
    "key": "Ctrl + Flèches",
    "action": "Aller à la dernière cellule remplie",
    "niveau": "Basique"
  },
  {
    "key": "Ctrl + Shift + +",
    "action": "Insérer une ligne/colonne",
    "niveau": "Basique"
  },
  {
    "key": "Alt + Enter",
    "action": "Saut de ligne dans une cellule",
    "niveau": "Basique"
  },
  {
    "key": "Ctrl + 1",
    "action": "Ouvrir Format de cellule",
    "niveau": "Intermédiaire"
  },
  {
    "key": "F2",
    "action": "Modifier la cellule active",
    "niveau": "Basique"
  },
  {
    "key": "Ctrl + Z / Y",
    "action": "Annuler / Rétablir",
    "niveau": "Basique"
  },
  {
    "key": "Ctrl + F",
    "action": "Rechercher dans la feuille",
    "niveau": "Basique"
  },
  {
    "key": "Ctrl + H",
    "action": "Remplacer un contenu",
    "niveau": "Basique"
  },
  {
    "key": "F11",
    "action": "Créer un graphique instantanément",
    "niveau": "Avancé"
  },
  {
    "key": "Ctrl + Shift + $",
    "action": "Format monétaire",
    "niveau": "Intermédiaire"
  },
  {
    "key": "Ctrl + Shift + %",
    "action": "Format pourcentage",
    "niveau": "Intermédiaire"
  },
  {
    "key": "Alt + F1",
    "action": "Insérer graphique dans la feuille",
    "niveau": "Avancé"
  }
];

export const EXCEL_FORMULAS = [
  {
    "formule": "=SOMME(A1:A10)",
    "description": "Additionner une plage de cellules"
  },
  {
    "formule": "=MOYENNE(A1:A10)",
    "description": "Calculer la moyenne d'une plage"
  },
  {
    "formule": "=SI(A1>10, \"Oui\", \"Non\")",
    "description": "Condition simple SI/THEN/ELSE"
  },
  {
    "formule": "=RECHERCHEV(A1, B:C, 2, 0)",
    "description": "Chercher une valeur dans un tableau"
  },
  {
    "formule": "=NB.SI(A1:A10, \">5\")",
    "description": "Compter les cellules selon critère"
  },
  {
    "formule": "=CONCATENER(A1, \" \", B1)",
    "description": "Fusionner du texte"
  },
  {
    "formule": "=AUJOURD'HUI()",
    "description": "Afficher la date du jour"
  },
  {
    "formule": "=MAX(A1:A10)",
    "description": "Trouver la valeur maximale"
  },
  {
    "formule": "=MIN(A1:A10)",
    "description": "Trouver la valeur minimale"
  },
  {
    "formule": "=ARRONDI(A1, 2)",
    "description": "Arrondir à 2 décimales"
  },
  {
    "formule": "=NBVAL(A1:A10)",
    "description": "Compter les cellules non vides"
  },
  {
    "formule": "=GAUCHE(A1, 3)",
    "description": "Extraire les 3 premiers caractères"
  },
  {
    "formule": "=DROITE(A1, 3)",
    "description": "Extraire les 3 derniers caractères"
  },
  {
    "formule": "=MAJUSCULE(A1)",
    "description": "Convertir en majuscules"
  },
  {
    "formule": "=MINUSCULE(A1)",
    "description": "Convertir en minuscules"
  },
  {
    "formule": "=SOMME.SI(A1:A10,\">5\")",
    "description": "Additionner selon condition"
  },
  {
    "formule": "=SOMME.SI.ENS(A1:A10,B1:B10,\">5\")",
    "description": "Somme avec plusieurs conditions"
  },
  {
    "formule": "=NB.SI.ENS(A1:A10,\">5\",B1:B10,\"<10\")",
    "description": "Compter avec plusieurs critères"
  },
  {
    "formule": "=INDEX(A1:A10,5)",
    "description": "Retourner une valeur par position"
  },
  {
    "formule": "=EQUIV(A1,B1:B10,0)",
    "description": "Trouver la position d'une valeur"
  },
  {
    "formule": "=INDEX(A1:A10,EQUIV(A1,B1:B10,0))",
    "description": "Recherche avancée (remplace RECHERCHEV)"
  },
  {
    "formule": "=RECHERCHEX(A1,A1:A10,B1:B10)",
    "description": "Recherche moderne et flexible"
  },
  {
    "formule": "=SIERREUR(A1/B1,\"Erreur\")",
    "description": "Gérer les erreurs"
  },
  {
    "formule": "=ESTVIDE(A1)",
    "description": "Vérifier si cellule vide"
  },
  {
    "formule": "=ESTNUM(A1)",
    "description": "Tester si valeur numérique"
  },
  {
    "formule": "=ESTTEXTE(A1)",
    "description": "Tester si texte"
  },
  {
    "formule": "=NBCAR(A1)",
    "description": "Compter le nombre de caractères"
  },
  {
    "formule": "=STXT(A1,2,3)",
    "description": "Extraire du texte au milieu"
  },
  {
    "formule": "=SUPPRESPACE(A1)",
    "description": "Supprimer espaces inutiles"
  },
  {
    "formule": "=REMPLACER(A1,1,3,\"XYZ\")",
    "description": "Remplacer une partie du texte"
  },
  {
    "formule": "=SUBSTITUE(A1,\"a\",\"b\")",
    "description": "Remplacer texte spécifique"
  },
  {
    "formule": "=TROUVE(\"a\",A1)",
    "description": "Trouver position d'un texte"
  },
  {
    "formule": "=CHERCHE(\"a\",A1)",
    "description": "Recherche insensible à la casse"
  },
  {
    "formule": "=CONCAT(A1,B1)",
    "description": "Concaténer texte moderne"
  },
  {
    "formule": "=JOINDRE.TEXTE(\",\",VRAI,A1:A10)",
    "description": "Joindre avec séparateur"
  },
  {
    "formule": "=MAINTENANT()",
    "description": "Date + heure actuelle"
  },
  {
    "formule": "=ANNEE(A1)",
    "description": "Extraire l'année"
  },
  {
    "formule": "=MOIS(A1)",
    "description": "Extraire le mois"
  },
  {
    "formule": "=JOUR(A1)",
    "description": "Extraire le jour"
  },
  {
    "formule": "=HEURE(A1)",
    "description": "Extraire l'heure"
  },
  {
    "formule": "=MINUTE(A1)",
    "description": "Extraire les minutes"
  },
  {
    "formule": "=SECONDE(A1)",
    "description": "Extraire les secondes"
  },
  {
    "formule": "=NB.JOURS(A1,B1)",
    "description": "Différence en jours"
  },
  {
    "formule": "=FIN.MOIS(A1,1)",
    "description": "Dernier jour du mois"
  },
  {
    "formule": "=ALEA()",
    "description": "Nombre aléatoire entre 0 et 1"
  },
  {
    "formule": "=ALEA.ENTRE.BORNES(1,100)",
    "description": "Nombre aléatoire entier"
  },
  {
    "formule": "=PUISSANCE(A1,2)",
    "description": "Calcul puissance"
  },
  {
    "formule": "=RACINE(A1)",
    "description": "Racine carrée"
  },
  {
    "formule": "=ABS(A1)",
    "description": "Valeur absolue"
  },
  {
    "formule": "=ENT(A1)",
    "description": "Partie entière"
  },
  {
    "formule": "=MOD(A1,2)",
    "description": "Reste de division"
  },
  {
    "formule": "=PRODUIT(A1:A10)",
    "description": "Multiplier une plage"
  },
  {
    "formule": "=SOMMEPROD(A1:A10,B1:B10)",
    "description": "Produit + somme"
  },
  {
    "formule": "=TRANSPOSE(A1:B2)",
    "description": "Inverser lignes/colonnes"
  },
  {
    "formule": "=FILTRE(A1:A10,A1:A10>5)",
    "description": "Filtrer dynamiquement"
  },
  {
    "formule": "=TRIER(A1:A10)",
    "description": "Trier automatiquement"
  },
  {
    "formule": "=UNIQUE(A1:A10)",
    "description": "Extraire valeurs uniques"
  },
  {
    "formule": "=DECALER(A1,1,1)",
    "description": "Décaler une référence"
  },
  {
    "formule": "=INDIRECT(\"A1\")",
    "description": "Référence dynamique"
  },
  {
    "formule": "=CELLULE(\"adresse\",A1)",
    "description": "Infos sur cellule"
  },
  {
    "formule": "=INFO(\"osversion\")",
    "description": "Infos système Excel"
  },
  {
    "formule": "=NA()",
    "description": "Retourne erreur #N/A"
  },
  {
    "formule": "=TYPE(A1)",
    "description": "Type de donnée"
  },
  {
    "formule": "=PMT(0.05/12,60,10000)",
    "description": "Calculer un paiement de prêt"
  },
  {
    "formule": "=VA(0.05,10,-1000)",
    "description": "Valeur actuelle d'un investissement"
  },
  {
    "formule": "=VC(0.05,10,-1000)",
    "description": "Valeur future"
  },
  {
    "formule": "=TAUX(10,-1000,10000)",
    "description": "Calculer un taux d'intérêt"
  },
  {
    "formule": "=NBPER(0.05,-100,1000)",
    "description": "Nombre de périodes"
  },
  {
    "formule": "=MEDIANE(A1:A10)",
    "description": "Valeur médiane"
  },
  {
    "formule": "=ECARTYPE(A1:A10)",
    "description": "Écart-type"
  },
  {
    "formule": "=VAR(A1:A10)",
    "description": "Variance"
  },
  {
    "formule": "=QUARTILE(A1:A10,1)",
    "description": "Quartile"
  },
  {
    "formule": "=RANG(A1,A1:A10)",
    "description": "Classement d'une valeur"
  },
  {
    "formule": "=GRANDE.VALEUR(A1:A10,1)",
    "description": "Plus grande valeur"
  },
  {
    "formule": "=PETITE.VALEUR(A1:A10,1)",
    "description": "Plus petite valeur"
  },
  {
    "formule": "=FREQUENCE(A1:A10,B1:B5)",
    "description": "Distribution de fréquence"
  },
  {
    "formule": "=ET(A1>0,B1<10)",
    "description": "Condition logique ET"
  },
  {
    "formule": "=OU(A1>0,B1<10)",
    "description": "Condition logique OU"
  },
  {
    "formule": "=NON(A1>0)",
    "description": "Inverser une condition"
  },
  {
    "formule": "=SI.CONDITIONS(A1>10,\"A\",A1>5,\"B\")",
    "description": "Conditions multiples"
  },
  {
    "formule": "=CHOISIR(2,\"A\",\"B\",\"C\")",
    "description": "Choisir valeur par index"
  },
  {
    "formule": "=COLONNE(A1)",
    "description": "Numéro de colonne"
  },
  {
    "formule": "=LIGNE(A1)",
    "description": "Numéro de ligne"
  },
  {
    "formule": "=COLONNES(A1:C1)",
    "description": "Nombre de colonnes"
  },
  {
    "formule": "=LIGNES(A1:A10)",
    "description": "Nombre de lignes"
  },
  {
    "formule": "=ADRESSE(1,1)",
    "description": "Créer une adresse de cellule"
  },
  {
    "formule": "=DECALER(A1,2,2)",
    "description": "Référence décalée"
  },
  {
    "formule": "=LIEN_HYPERTEXTE(\"https://exemple.com\",\"Lien\")",
    "description": "Créer un lien cliquable"
  },
  {
    "formule": "=GAUCHEB(A1,3)",
    "description": "Texte multi-octets gauche"
  },
  {
    "formule": "=DROITEB(A1,3)",
    "description": "Texte multi-octets droite"
  },
  {
    "formule": "=NBCAR(A1)",
    "description": "Nombre de caractères (rappel utile)"
  },
  {
    "formule": "=ESTERREUR(A1)",
    "description": "Tester erreur"
  },
  {
    "formule": "=ESTNA(A1)",
    "description": "Tester #N/A"
  },
  {
    "formule": "=TRIERPAR(A1:A10,B1:B10)",
    "description": "Tri basé sur autre colonne"
  },
  {
    "formule": "=SEQUENCE(10)",
    "description": "Créer une séquence automatique"
  },
  {
    "formule": "=ALEA.ENTRE.BORNES(1,100)",
    "description": "Aléatoire entier"
  },
  {
    "formule": "=SOMMEPROD((A1:A10>5)*(B1:B10))",
    "description": "Somme conditionnelle avancée"
  },
  {
    "formule": "=NB(A1:A10)",
    "description": "Compter cellules numériques"
  },
  {
    "formule": "=CNUM(\"123\")",
    "description": "Convertir texte en nombre"
  },
  {
    "formule": "=TEXTE(A1,\"0.00\")",
    "description": "Formater nombre en texte"
  },
  {
    "formule": "=JOURSEM(A1)",
    "description": "Jour de la semaine"
  },
  {
    "formule": "=NO.SEMAINE(A1)",
    "description": "Numéro de semaine"
  },
  {
    "formule": "=TEMPS(12,30,0)",
    "description": "Créer une heure"
  },
  {
    "formule": "=DATE(2025,1,1)",
    "description": "Créer une date"
  },
  {
    "formule": "=REPT(\"*\",5)",
    "description": "Répéter un texte"
  },
  {
    "formule": "=EXACT(A1,B1)",
    "description": "Comparer texte exact"
  },
  {
    "formule": "=FORMULETEXTE(A1)",
    "description": "Afficher formule d'une cellule"
  }
];

export const PROF_TRAPS = [
  {
    "matiere": "Architecture",
    "piege": "BIOS vs Système d'Exploitation",
    "question_type": "Quelle est la différence entre le BIOS et l'OS ?",
    "erreur_classique": "Confondre le BIOS avec l'OS ou dire que le BIOS est un logiciel ordinaire",
    "bonne_reponse": "Le BIOS (Basic Input/Output System) est un firmware stocké sur une puce ROM de la carte mère. Il s'exécute AVANT l'OS, initialise le matériel (POST) et lance le bootloader. L'OS (Windows, Linux) est un logiciel chargé APRÈS le BIOS depuis le disque dur.",
    "niveau": "L1",
    "danger": "🔴 Très fréquent en examen"
  },
  {
    "matiere": "Architecture",
    "piege": "RAM vs ROM",
    "question_type": "Décris la différence entre RAM et ROM",
    "erreur_classique": "Dire que la RAM garde les données quand on éteint l'ordinateur",
    "bonne_reponse": "RAM (Random Access Memory) = mémoire VOLATILE, perd son contenu à l'extinction. ROM (Read Only Memory) = mémoire NON-VOLATILE, garde son contenu. La RAM est rapide et temporaire (programmes en cours). La ROM contient le firmware permanent (BIOS).",
    "niveau": "L1",
    "danger": "🔴 Très fréquent en examen"
  },
  {
    "matiere": "Logique/Architecture",
    "piege": "Formatage Haut-Niveau vs Bas-Niveau",
    "question_type": "Qu'est-ce que le formatage bas niveau ?",
    "erreur_classique": "Dire que formater = simplement effacer les fichiers",
    "bonne_reponse": "Le formatage BAS NIVEAU divise physiquement le disque en secteurs et pistes — fait par le fabricant. Le formatage HAUT NIVEAU crée le système de fichiers (FAT32, NTFS, ext4). Formater depuis Windows = formatage haut niveau, PAS bas niveau.",
    "niveau": "L1",
    "danger": "🟠 Fréquent"
  },
  {
    "matiere": "Programmation C",
    "piege": "Passage par valeur vs par pointeur",
    "question_type": "Pourquoi cette fonction ne modifie pas la variable originale ?",
    "erreur_classique": "Oublier que C passe les arguments par VALEUR par défaut (copie)",
    "bonne_reponse": "En C, les fonctions reçoivent une COPIE des arguments (passage par valeur). Pour modifier la variable originale, il faut passer son ADRESSE avec & et utiliser un pointeur *. Ex: void modifier(int *x) { *x = 10; }",
    "niveau": "L1/L2",
    "danger": "🔴 Très fréquent en examen"
  },
  {
    "matiere": "Algèbre de Boole",
    "piege": "Priorité des opérateurs logiques",
    "question_type": "Évalue: A + B.C sans parenthèses",
    "erreur_classique": "Évaluer de gauche à droite comme en arithmétique",
    "bonne_reponse": "En Algèbre de Boole: NOT (¬) > AND (.) > OR (+). Donc A + B.C = A + (B AND C). Le AND est prioritaire sur le OR, comme la multiplication sur l'addition en maths classiques.",
    "niveau": "L1",
    "danger": "🔴 Classique en intra"
  },
  {
    "matiere": "Système d'Exploitation",
    "piege": "Processus vs Thread",
    "question_type": "Quelle est la différence entre un processus et un thread ?",
    "erreur_classique": "Dire qu'un thread est la même chose qu'un processus",
    "bonne_reponse": "Un PROCESSUS est un programme en exécution avec son propre espace mémoire isolé. Un THREAD est une unité d'exécution DANS un processus, partageant la mémoire du processus. Un processus peut contenir plusieurs threads. Les threads sont plus légers à créer.",
    "niveau": "L2",
    "danger": "🔴 Incontournable en SE"
  },
  {
    "matiere": "Système d'Exploitation",
    "piege": "Deadlock (Interblocage)",
    "question_type": "Donne les 4 conditions nécessaires à un deadlock",
    "erreur_classique": "Ne citer que 2-3 conditions ou les confondre",
    "bonne_reponse": "Les 4 conditions de Coffman: 1) EXCLUSION MUTUELLE (ressource non partageable) 2) DÉTENTION ET ATTENTE (processus tient une ressource et attend une autre) 3) NON-PRÉEMPTION (ressource ne peut être retirée de force) 4) ATTENTE CIRCULAIRE (cycle d'attente entre processus).",
    "niveau": "L2",
    "danger": "🟠 Fréquent en final"
  },
  {
    "matiere": "POO / C++",
    "piege": "Héritage vs Composition",
    "question_type": "Quand utiliser l'héritage et quand utiliser la composition ?",
    "erreur_classique": "Toujours utiliser l'héritage par défaut",
    "bonne_reponse": "HÉRITAGE (is-a): Quand B EST UN type de A. Ex: Chien est un Animal. COMPOSITION (has-a): Quand B POSSÈDE un A. Ex: Voiture a un Moteur. Règle d'or: Préférer la composition à l'héritage pour éviter le couplage fort.",
    "niveau": "L2",
    "danger": "🟠 Classique en Concepts Objet"
  },
  {
    "matiere": "Réseaux",
    "piege": "Modèle OSI vs TCP/IP",
    "question_type": "Combien de couches a le modèle OSI ? Et TCP/IP ?",
    "erreur_classique": "Confondre les couches des deux modèles",
    "bonne_reponse": "OSI = 7 couches: Physique, Liaison, Réseau, Transport, Session, Présentation, Application. TCP/IP = 4 couches: Accès Réseau (= couches 1+2 OSI), Internet (= couche 3), Transport (= couche 4), Application (= couches 5+6+7). Mnémonique OSI: 'Please Do Not Throw Sausage Pizza Away'",
    "niveau": "L3",
    "danger": "🔴 Toujours dans l'examen réseaux"
  },
  {
    "matiere": "Base de Données",
    "piege": "Clé Primaire vs Clé Étrangère",
    "question_type": "Définis et distingue clé primaire et clé étrangère",
    "erreur_classique": "Dire qu'une clé étrangère identifie uniquement une ligne",
    "bonne_reponse": "CLÉ PRIMAIRE: Identifie UNIQUEMENT chaque enregistrement dans SA table. Doit être unique et non nulle. CLÉ ÉTRANGÈRE: Référence la clé primaire d'UNE AUTRE table. Crée un lien (relation) entre deux tables. Garantit l'intégrité référentielle.",
    "niveau": "L3",
    "danger": "🔴 Fondamental en BD"
  },
  {
    "matiere": "SQL",
    "piege": "DELETE vs TRUNCATE vs DROP",
    "question_type": "Quelle est la différence entre DELETE, TRUNCATE et DROP ?",
    "erreur_classique": "Dire que les trois font la même chose",
    "bonne_reponse": "DELETE: Supprime des lignes avec condition WHERE, peut être annulé (ROLLBACK), lent. TRUNCATE: Supprime TOUTES les lignes, plus rapide que DELETE, ne peut pas être annulé facilement. DROP: Supprime la TABLE ENTIÈRE (structure + données), irréversible.",
    "niveau": "L3",
    "danger": "🟠 Classique en MySQL/Oracle"
  },
  {
    "matiere": "Structures de Données",
    "piege": "Stack vs Queue",
    "question_type": "Donne le principe de fonctionnement d'un Stack et d'une Queue",
    "erreur_classique": "Inverser LIFO et FIFO",
    "bonne_reponse": "STACK (Pile) = LIFO (Last In First Out): Le dernier élément ajouté est le premier sorti. Comme une pile d'assiettes. Opérations: PUSH (ajouter) et POP (retirer). QUEUE (File) = FIFO (First In First Out): Le premier entré est le premier sorti. Comme une file d'attente. Opérations: ENQUEUE et DEQUEUE.",
    "niveau": "L2",
    "danger": "🔴 Incontournable en Structures de Données"
  },
  {
    "matiere": "Réseaux",
    "piege": "TCP vs UDP",
    "question_type": "Quand utiliser TCP et quand utiliser UDP ?",
    "erreur_classique": "Dire que TCP est toujours meilleur",
    "bonne_reponse": "TCP: Orienté connexion, fiable, contrôle d'erreurs, ordre garanti. Utilisé pour: HTTP, FTP, Email. Plus LENT. UDP: Sans connexion, non fiable, pas de contrôle. Utilisé pour: streaming, jeux en ligne, DNS. Plus RAPIDE. TCP = livraison recommandée. UDP = courrier normal.",
    "niveau": "L3",
    "danger": "🟠 Fréquent en Réseaux"
  },
  {
    "matiere": "Programmation",
    "piege": "Compilation vs Interprétation",
    "question_type": "Quelle est la différence entre un langage compilé et interprété ?",
    "erreur_classique": "Dire que Python est compilé ou que Java est purement interprété",
    "bonne_reponse": "COMPILÉ (C, C++): Code source traduit EN ENTIER en code machine AVANT l'exécution. Rapide à l'exécution. INTERPRÉTÉ (Python): Traduit et exécuté LIGNE PAR LIGNE à l'exécution. Plus lent. Java: MIXTE — compilé en bytecode puis interprété par la JVM.",
    "niveau": "L1/L2",
    "danger": "🟠 Classique en intro programmation"
  },
  {
    "matiere": "Architecture",
    "piege": "Von Neumann Bottleneck",
    "question_type": "Qu'est-ce que le goulot d'étranglement de Von Neumann ?",
    "erreur_classique": "Ne pas connaître ce concept pourtant fondamental",
    "bonne_reponse": "Dans l'architecture de Von Neumann, le CPU et la mémoire partagent un SEUL bus pour les données ET les instructions. Le CPU attend souvent la mémoire (plus lente). Ce bottleneck limite les performances. Solution moderne: mémoire cache (L1, L2, L3) pour rapprocher les données du CPU.",
    "niveau": "L1",
    "danger": "🟡 Avancé mais impressionne le prof"
  }
];

export const LINUX_COMMANDS = [
  {
    "cmd": "ls -la",
    "description": "Lister tous les fichiers avec détails"
  },
  {
    "cmd": "cd /chemin",
    "description": "Changer de répertoire"
  },
  {
    "cmd": "pwd",
    "description": "Afficher le répertoire courant"
  },
  {
    "cmd": "mkdir nom",
    "description": "Créer un répertoire"
  },
  {
    "cmd": "rm -rf nom",
    "description": "Supprimer dossier et contenu (DANGEREUX)"
  },
  {
    "cmd": "cp source dest",
    "description": "Copier un fichier"
  },
  {
    "cmd": "mv source dest",
    "description": "Déplacer ou renommer"
  },
  {
    "cmd": "cat fichier",
    "description": "Afficher le contenu d'un fichier"
  },
  {
    "cmd": "grep 'motif' fichier",
    "description": "Chercher un motif dans un fichier"
  },
  {
    "cmd": "chmod 755 fichier",
    "description": "Modifier les permissions"
  },
  {
    "cmd": "chown user:group fichier",
    "description": "Changer le propriétaire"
  },
  {
    "cmd": "ps aux",
    "description": "Lister tous les processus"
  },
  {
    "cmd": "kill -9 PID",
    "description": "Forcer l'arrêt d'un processus"
  },
  {
    "cmd": "top / htop",
    "description": "Moniteur de ressources système"
  },
  {
    "cmd": "df -h",
    "description": "Espace disque utilisé"
  },
  {
    "cmd": "free -h",
    "description": "Mémoire RAM disponible"
  },
  {
    "cmd": "ifconfig / ip a",
    "description": "Voir les interfaces réseau"
  },
  {
    "cmd": "ping hôte",
    "description": "Tester la connectivité réseau"
  },
  {
    "cmd": "ssh user@ip",
    "description": "Connexion SSH distante"
  },
  {
    "cmd": "sudo commande",
    "description": "Exécuter en tant que root"
  },
  {
    "cmd": "apt install paquet",
    "description": "Installer un paquet (Debian/Ubuntu)"
  },
  {
    "cmd": "nano / vim fichier",
    "description": "Éditeur de texte en terminal"
  },
  {
    "cmd": "tar -czvf archive.tar.gz dossier",
    "description": "Compresser un dossier"
  },
  {
    "cmd": "find / -name 'fichier'",
    "description": "Chercher un fichier"
  },
  {
    "cmd": "history",
    "description": "Historique des commandes"
  },
  {
    "cmd": "man commande",
    "description": "Afficher le manuel d'une commande"
  },
  {
    "cmd": "alias nom='commande'",
    "description": "Créer un raccourci de commande"
  },
  {
    "cmd": "whoami",
    "description": "Afficher l'utilisateur courant"
  },
  {
    "cmd": "id",
    "description": "Afficher UID, GID et groupes utilisateur"
  },
  {
    "cmd": "uname -a",
    "description": "Infos système (kernel, OS)"
  },
  {
    "cmd": "uptime",
    "description": "Temps de fonctionnement du système"
  },
  {
    "cmd": "which commande",
    "description": "Localiser un exécutable"
  },
  {
    "cmd": "locate fichier",
    "description": "Recherche rapide de fichiers indexés"
  },
  {
    "cmd": "updatedb",
    "description": "Mettre à jour la base de locate"
  },
  {
    "cmd": "echo texte",
    "description": "Afficher du texte ou variable"
  },
  {
    "cmd": "export VAR=valeur",
    "description": "Créer une variable d'environnement"
  },
  {
    "cmd": "env",
    "description": "Afficher les variables d'environnement"
  },
  {
    "cmd": "clear",
    "description": "Nettoyer le terminal"
  },
  {
    "cmd": "reboot",
    "description": "Redémarrer le système"
  },
  {
    "cmd": "shutdown now",
    "description": "Éteindre immédiatement le système"
  },
  {
    "cmd": "crontab -e",
    "description": "Planifier des tâches automatiques"
  },
  {
    "cmd": "wget url",
    "description": "Télécharger un fichier depuis Internet"
  },
  {
    "cmd": "curl url",
    "description": "Requêtes HTTP/API depuis terminal"
  },
  {
    "cmd": "scp fichier user@ip:/path",
    "description": "Copie sécurisée via SSH"
  },
  {
    "cmd": "rsync -av source dest",
    "description": "Synchronisation de fichiers"
  },
  {
    "cmd": "netstat -tulnp",
    "description": "Ports et connexions réseau"
  },
  {
    "cmd": "ss -tulnp",
    "description": "Version moderne de netstat"
  },
  {
    "cmd": "iptables -L",
    "description": "Afficher les règles firewall"
  },
  {
    "cmd": "ufw status",
    "description": "Firewall simplifié (Ubuntu)"
  },
  {
    "cmd": "dmesg",
    "description": "Logs du kernel système"
  },
  {
    "cmd": "journalctl -xe",
    "description": "Logs système systemd"
  },
  {
    "cmd": "mount",
    "description": "Afficher les disques montés"
  },
  {
    "cmd": "umount /point",
    "description": "Démonter un disque"
  },
  {
    "cmd": "lsblk",
    "description": "Lister les disques et partitions"
  },
  {
    "cmd": "fdisk -l",
    "description": "Infos disque avancées"
  },
  {
    "cmd": "useradd nom",
    "description": "Créer un utilisateur"
  },
  {
    "cmd": "passwd user",
    "description": "Changer mot de passe utilisateur"
  },
  {
    "cmd": "usermod -aG groupe user",
    "description": "Ajouter utilisateur à un groupe"
  },
  {
    "cmd": "groupadd nom",
    "description": "Créer un groupe"
  },
  {
    "cmd": "service nom start",
    "description": "Démarrer un service"
  },
  {
    "cmd": "systemctl status service",
    "description": "État d'un service systemd"
  },
  {
    "cmd": "systemctl restart service",
    "description": "Redémarrer un service"
  },
  {
    "cmd": "git clone url",
    "description": "Cloner un dépôt Git"
  },
  {
    "cmd": "git status",
    "description": "Voir l'état du repo Git"
  },
  {
    "cmd": "git add .",
    "description": "Ajouter tous les fichiers"
  },
  {
    "cmd": "git push",
    "description": "Envoyer vers dépôt distant"
  },
  {
    "cmd": "git pull",
    "description": "Récupérer les modifications"
  }
];

export const OSI_LAYERS = [
  {
    "numero": 7,
    "nom": "Application",
    "role": "Interface avec l'utilisateur",
    "exemples": "HTTP, FTP, DNS, SMTP"
  },
  {
    "numero": 6,
    "nom": "Présentation",
    "role": "Formatage, chiffrement, compression",
    "exemples": "SSL, TLS, JPEG, ASCII"
  },
  {
    "numero": 5,
    "nom": "Session",
    "role": "Gestion des sessions de communication",
    "exemples": "NetBIOS, RPC"
  },
  {
    "numero": 4,
    "nom": "Transport",
    "role": "Fiabilité, contrôle de flux",
    "exemples": "TCP, UDP"
  },
  {
    "numero": 3,
    "nom": "Réseau",
    "role": "Routage et adressage logique",
    "exemples": "IP, ICMP, ARP"
  },
  {
    "numero": 2,
    "nom": "Liaison",
    "role": "Adressage physique (MAC)",
    "exemples": "Ethernet, WiFi, PPP"
  },
  {
    "numero": 1,
    "nom": "Physique",
    "role": "Transmission des bits",
    "exemples": "Câbles, Hubs, Signaux"
  }
];

export const NETWORK_PROTOCOLS = [
  {
    "port": "20/21",
    "protocole": "FTP",
    "description": "Transfert de fichiers",
    "type": "TCP"
  },
  {
    "port": "22",
    "protocole": "SSH",
    "description": "Connexion sécurisée distante",
    "type": "TCP"
  },
  {
    "port": "23",
    "protocole": "Telnet",
    "description": "Connexion distante non sécurisée",
    "type": "TCP"
  },
  {
    "port": "25",
    "protocole": "SMTP",
    "description": "Envoi d'emails",
    "type": "TCP"
  },
  {
    "port": "53",
    "protocole": "DNS",
    "description": "Résolution de noms de domaine",
    "type": "TCP/UDP"
  },
  {
    "port": "67/68",
    "protocole": "DHCP",
    "description": "Attribution d'adresses IP",
    "type": "UDP"
  },
  {
    "port": "80",
    "protocole": "HTTP",
    "description": "Web non sécurisé",
    "type": "TCP"
  },
  {
    "port": "110",
    "protocole": "POP3",
    "description": "Réception d'emails",
    "type": "TCP"
  },
  {
    "port": "143",
    "protocole": "IMAP",
    "description": "Gestion d'emails sur serveur",
    "type": "TCP"
  },
  {
    "port": "443",
    "protocole": "HTTPS",
    "description": "Web sécurisé (SSL/TLS)",
    "type": "TCP"
  },
  {
    "port": "3306",
    "protocole": "MySQL",
    "description": "Base de données MySQL",
    "type": "TCP"
  },
  {
    "port": "3389",
    "protocole": "RDP",
    "description": "Bureau à distance Windows",
    "type": "TCP"
  },
  {
    "port": "8080",
    "protocole": "HTTP-Alt",
    "description": "Serveur web alternatif",
    "type": "TCP"
  }
];
