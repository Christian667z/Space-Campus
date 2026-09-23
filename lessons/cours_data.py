"""
╔══════════════════════════════════════════════════════════════╗
║         ASTA ACADÉMIE — COURS UNASMOH L1→L4 DATABASE        ║
║         Développé par Space | Asta Dev — Promo 2024-2028     ║
╚══════════════════════════════════════════════════════════════╝
"""

COURS_L1 = {
    "Intro à l'Informatique": {
        "pole": "Développement & Système",
        "session": "1",
        "lecons": [
            {
                "titre": "Qu'est-ce que l'Informatique ?",
                "niveau_difficulte": 3,
                "theorie": """
L'INFORMATIQUE — DÉFINITION RIGOUREUSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

L'informatique est la SCIENCE du traitement automatique de l'INFORMATION
par des systèmes numériques programmables.

Trois composantes fondamentales :
  1. DONNÉES : L'information brute (nombres, textes, images)
  2. TRAITEMENT : Les opérations appliquées aux données
  3. RÉSULTATS : L'information traitée et présentée

L'ordinateur = machine universelle de Turing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Un ordinateur peut résoudre TOUT problème calculable, pourvu qu'on lui
fournisse l'algorithme approprié. C'est le théorème fondamental de
l'informatique théorique (Alan Turing, 1936).

Les 4 fonctions essentielles d'un ordinateur :
  ▶ ENTRÉE    : Saisie clavier, souris, capteurs
  ▶ TRAITEMENT: CPU exécute les instructions
  ▶ STOCKAGE  : RAM (temporaire), Disque dur (permanent)
  ▶ SORTIE    : Écran, imprimante, haut-parleurs

ERREUR CLASSIQUE À ÉVITER :
⚠️  "L'informatique = apprendre à utiliser Word/Excel"
✅  "L'informatique = science de la résolution de problèmes par algorithmes"
""",
                "points_cles": [
                    "Informatique ≠ bureautique — c'est une science",
                    "Tout ordinateur est basé sur le modèle de Von Neumann",
                    "4 fonctions : Entrée, Traitement, Stockage, Sortie",
                    "Un bit = l'unité d'information la plus petite (0 ou 1)",
                    "8 bits = 1 octet (byte)"
                ],
                "exercice": "Décris en 3 étapes (Entrée/Traitement/Sortie) ce qui se passe quand tu tapes un mot dans un traitement de texte et que tu cliques sur 'Imprimer'.",
                "correction": "ENTRÉE: Frappe clavier → codes ASCII. TRAITEMENT: CPU interprète les codes, formate le document. SORTIE: Données envoyées à l'imprimante via le pilote d'impression.",
                "piege_prof": "Différence entre donnée et information : Une donnée brute (42°C) devient information quand contextualisée (fièvre = 42°C = danger)."
            },
            {
                "titre": "Histoire de l'Informatique — Des Origines à Aujourd'hui",
                "niveau_difficulte": 2,
                "theorie": """
CHRONOLOGIE ESSENTIELLE 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GÉNÉRATION 1 (1940-1955) — Tubes à vide
  • ENIAC (1945) : Premier calculateur électronique, 27 tonnes
  • Langage : Code machine (0 et 1 directement)
  • Problème : Surchauffe, pannes fréquentes, gigantesque

GÉNÉRATION 2 (1955-1965) — Transistors
  • Remplacement des tubes à vide par des transistors
  • 1000x plus petits, moins chauds
  • Apparition des langages assembleur et FORTRAN

GÉNÉRATION 3 (1965-1975) — Circuits Intégrés (CI)
  • Intel 4004 (1971) : Premier microprocesseur
  • Plusieurs transistors sur une seule puce
  • Apparition des systèmes d'exploitation (OS)

GÉNÉRATION 4 (1975-aujourd'hui) — Microprocesseurs
  • Apple I (1976), IBM PC (1981)
  • Ordinateur personnel pour tout le monde
  • Internet, Web, Smartphones

GÉNÉRATION 5 (en cours) — IA & Quantique
  • Intelligence Artificielle, Machine Learning
  • Informatique quantique (qubits)
""",
                "points_cles": [
                    "4 générations d'ordinateurs selon la technologie utilisée",
                    "Tubes à vide → Transistors → CI → Microprocesseurs → IA",
                    "Loi de Moore : nombre de transistors double tous les 2 ans",
                    "Ada Lovelace = première programmeuse (1843)",
                    "Alan Turing = père de l'informatique (1936)"
                ],
                "exercice": "Cite les 4 générations d'ordinateurs avec leur technologie principale et une caractéristique.",
                "correction": "G1: Tubes à vide (ENIAC, 27 tonnes). G2: Transistors (plus petits, moins chauds). G3: Circuits intégrés (microprocesseur Intel 4004). G4: Microprocesseurs (PC, smartphones).",
                "piege_prof": "Le prof peut demander: 'Qui a inventé l'ordinateur ?' — Réponse nuancée : Babbage (mécanique), Turing (théorique), Von Neumann (architecture moderne), Mauchly/Eckert (ENIAC électronique)."
            },
        ]
    },

    "Architecture des Ordinateurs": {
        "pole": "Développement & Système",
        "session": "1",
        "lecons": [
            {
                "titre": "Architecture de Von Neumann — Le Modèle Universel",
                "niveau_difficulte": 7,
                "theorie": """
ARCHITECTURE DE VON NEUMANN (1945)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Principe révolutionnaire : PROGRAMME STOCKÉ EN MÉMOIRE
Avant Von Neumann, le programme était câblé physiquement.
Von Neumann propose de stocker données ET instructions dans la MÊME mémoire.

COMPOSANTS PRINCIPAUX :
┌─────────────────────────────────────────────────────┐
│                    MÉMOIRE CENTRALE                  │
│              (Instructions + Données)                │
└────────────────────┬────────────────────────────────┘
                     │ Bus de données / adresses
┌────────────────────▼────────────────────────────────┐
│                        CPU                          │
│  ┌─────────────────┐     ┌────────────────────────┐ │
│  │    UAL (ALU)    │     │  UC (Unité de Contrôle)│ │
│  │ Calculs & Logique│    │ Séquence les instructions│ │
│  └─────────────────┘     └────────────────────────┘ │
│  ┌─────────────────────────────────────────────────┐ │
│  │   Registres (PC, IR, ACC, MAR, MDR...)          │ │
│  └─────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              PÉRIPHÉRIQUES E/S                      │
│         Clavier, Écran, Disque, Réseau              │
└─────────────────────────────────────────────────────┘

REGISTRES CLÉS DU CPU :
  • PC (Program Counter) : Adresse de la prochaine instruction
  • IR (Instruction Register) : Instruction en cours d'exécution
  • ACC (Accumulateur) : Résultat des calculs
  • MAR (Memory Address Register) : Adresse mémoire à lire/écrire
  • MDR (Memory Data Register) : Donnée lue/écrite en mémoire

CYCLE FETCH-DECODE-EXECUTE :
  1. FETCH   : PC → MAR, lire mémoire → MDR → IR, PC++
  2. DECODE  : UC décode l'instruction dans IR
  3. EXECUTE : UAL exécute l'opération

BOTTLENECK DE VON NEUMANN :
⚠️  CPU et mémoire partagent le MÊME bus → goulot d'étranglement
✅  Solution moderne : Cache L1/L2/L3 pour réduire les accès mémoire
""",
                "points_cles": [
                    "Programme stocké en mémoire = innovation de Von Neumann",
                    "CPU = UAL + UC + Registres",
                    "UAL effectue les calculs, UC contrôle la séquence",
                    "PC pointe toujours vers la prochaine instruction",
                    "Cycle: Fetch → Decode → Execute (répété infiniment)"
                ],
                "exercice": "Décris le cycle Fetch-Decode-Execute pour l'instruction: ADD 5, 3 (Addition de 5 et 3)",
                "correction": "FETCH: PC donne l'adresse, on lit l'instruction ADD 5,3 en mémoire → IR. PC s'incrémente. DECODE: UC reconnait l'opcode ADD, identifie les opérandes 5 et 3. EXECUTE: UAL additionne 5+3=8, résultat stocké dans ACC.",
                "piege_prof": "Le Von Neumann Bottleneck : Le prof peut demander pourquoi les ordinateurs modernes ont un cache. Réponse : pour compenser le goulot d'étranglement du bus unique données/instructions."
            },
            {
                "titre": "Hiérarchie Mémoire — Du Plus Rapide au Plus Lent",
                "niveau_difficulte": 6,
                "theorie": """
PYRAMIDE DE LA MÉMOIRE
━━━━━━━━━━━━━━━━━━━━━

Plus on monte = Plus RAPIDE, Plus CHER, Plus PETIT
Plus on descend = Plus LENT, Moins cher, Plus GRAND

        ┌─────────────────┐
        │   REGISTRES     │  ← Nanoseconde, quelques KB
        │  (dans le CPU)  │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │   CACHE L1/L2   │  ← 1-10 ns, 64KB - 4MB
        │   (dans le CPU) │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │      RAM        │  ← 50-100 ns, 4GB - 64GB
        │  (barrette DDR) │  VOLATILE
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │   SSD / HDD     │  ← ms, 256GB - 4TB
        │  (stockage)     │  NON-VOLATILE
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │   CLOUD / BANDE │  ← secondes/minutes, Petaoctets
        └─────────────────┘

DIFFÉRENCE CRITIQUE : Volatile vs Non-Volatile
  VOLATILE (RAM, Cache) : Perd le contenu à l'extinction
  NON-VOLATILE (ROM, SSD, HDD) : Garde le contenu

TYPES DE RAM :
  • DRAM (Dynamic RAM) : Doit être rafraîchie, moins chère, RAM principale
  • SRAM (Static RAM) : Pas de rafraîchissement, ultra-rapide, coûteuse → Cache
  • DDR4/DDR5 : DRAM moderne, double taux de transfert

TYPES DE ROM :
  • ROM : Lecture seule, fixe depuis la fabrication
  • PROM : Programmable une fois
  • EPROM : Effaçable par UV
  • EEPROM : Effaçable électriquement (clé USB, SSD)
""",
                "points_cles": [
                    "Plus rapide = plus petit, plus cher, plus près du CPU",
                    "RAM = volatile (perd à extinction), HDD = non-volatile",
                    "Cache L1 > L2 > L3 en vitesse, L3 > L2 > L1 en taille",
                    "SRAM (cache) vs DRAM (RAM principale)",
                    "ROM contient le BIOS/firmware"
                ],
                "exercice": "Classe ces mémoires du plus rapide au plus lent: HDD, Cache L1, RAM DDR4, Registres CPU, SSD",
                "correction": "1. Registres CPU (picosecondes) 2. Cache L1 (~1 ns) 3. RAM DDR4 (~50 ns) 4. SSD (~0.1 ms) 5. HDD (~10 ms)",
                "piege_prof": "Attention: Le prof peut dire que le BIOS est stocké dans une ROM. C'est exact — mais les BIOS modernes (UEFI) utilisent de la FLASH (type d'EEPROM), pas une ROM stricte."
            },
        ]
    },

    "Algèbre de Boole": {
        "pole": "Mathématiques & Logique",
        "session": "1",
        "lecons": [
            {
                "titre": "Fondements de l'Algèbre de Boole — Le Langage des Ordinateurs",
                "niveau_difficulte": 7,
                "theorie": """
ALGÈBRE DE BOOLE — POURQUOI C'EST CRUCIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Inventée par George Boole (1854). Appliquée aux circuits par Claude Shannon (1937).
TOUT ordinateur fonctionne avec 2 états: 0 (faux) et 1 (vrai).
L'algèbre de Boole est le FONDEMENT mathématique des circuits logiques.

LES 3 OPÉRATEURS DE BASE :
━━━━━━━━━━━━━━━━━━━━━━━━━

1. NOT (¬, !) — Négation
   ┌───┬──────┐
   │ A │ ¬A   │
   ├───┼──────┤
   │ 0 │  1   │
   │ 1 │  0   │
   └───┴──────┘

2. AND (·, &&) — Conjonction (VRAI seulement si LES DEUX sont vrais)
   ┌───┬───┬───────┐
   │ A │ B │ A · B │
   ├───┼───┼───────┤
   │ 0 │ 0 │   0   │
   │ 0 │ 1 │   0   │
   │ 1 │ 0 │   0   │
   │ 1 │ 1 │   1   │
   └───┴───┴───────┘

3. OR (+, ||) — Disjonction (VRAI si AU MOINS UN est vrai)
   ┌───┬───┬───────┐
   │ A │ B │ A + B │
   ├───┼───┼───────┤
   │ 0 │ 0 │   0   │
   │ 0 │ 1 │   1   │
   │ 1 │ 0 │   1   │
   │ 1 │ 1 │   1   │
   └───┴───┴───────┘

PRIORITÉ DES OPÉRATEURS (TRÈS IMPORTANT) :
  NOT (¬) > AND (·) > OR (+)
  Comme en maths: parenthèses > × > +
  Exemple: A + B·C = A + (B·C)   ← Le AND est prioritaire!

PORTES LOGIQUES DÉRIVÉES :
  NAND : ¬(A·B) — Universelle (peut tout construire)
  NOR  : ¬(A+B) — Universelle aussi
  XOR  : A⊕B = A·¬B + ¬A·B (différent, l'un ou l'autre mais pas les deux)
  XNOR : ¬(A⊕B) (identique, les deux pareils)

LOIS FONDAMENTALES :
  • Identité    : A·1 = A    |  A+0 = A
  • Annulation  : A·0 = 0    |  A+1 = 1
  • Idempotence : A·A = A    |  A+A = A
  • Complément  : A·¬A = 0  |  A+¬A = 1
  • De Morgan 1 : ¬(A·B) = ¬A+¬B
  • De Morgan 2 : ¬(A+B) = ¬A·¬B
""",
                "points_cles": [
                    "AND = 1 seulement si les DEUX entrées sont 1",
                    "OR = 1 si AU MOINS UNE entrée est 1",
                    "NOT = inverse la valeur",
                    "Priorité: NOT > AND > OR",
                    "Lois de De Morgan: convertir AND↔OR avec NOT",
                    "NAND et NOR sont des portes universelles"
                ],
                "exercice": "Construis la table de vérité pour: F = A·B + ¬A·C (3 variables, 8 lignes)",
                "correction": "A=0,B=0,C=0: F=0. A=0,B=0,C=1: F=1. A=0,B=1,C=0: F=0. A=0,B=1,C=1: F=1. A=1,B=0,C=0: F=0. A=1,B=0,C=1: F=0. A=1,B=1,C=0: F=1. A=1,B=1,C=1: F=1.",
                "piege_prof": "XOR vs OR : Le prof adore cette confusion ! OR = vrai si A ou B ou les deux. XOR = vrai seulement si A ou B mais PAS les deux. En pratique: 1+1=1 (OR) mais 1⊕1=0 (XOR)."
            },
        ]
    },

    "Programmation Fondamentale": {
        "pole": "Développement & Système",
        "session": "2",
        "lecons": [
            {
                "titre": "Algorithmique — Penser Avant de Coder",
                "niveau_difficulte": 6,
                "theorie": """
QU'EST-CE QU'UN ALGORITHME ?
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Un algorithme est une SUITE FINIE et NON-AMBIGUË d'instructions
permettant de résoudre un problème ou d'accomplir une tâche.

Propriétés d'un bon algorithme :
  1. FINITUDE : S'arrête toujours (pas de boucle infinie)
  2. PRÉCISION : Chaque étape est non-ambiguë
  3. ENTRÉES : 0 ou plusieurs données en entrée
  4. SORTIES : Au moins un résultat
  5. EFFECTIVITÉ : Chaque opération est réalisable

STRUCTURES DE CONTRÔLE :
━━━━━━━━━━━━━━━━━━━━━━━

1. SÉQUENCE — Instructions exécutées l'une après l'autre
   DÉBUT
     Instruction 1
     Instruction 2
     Instruction 3
   FIN

2. CONDITION — Branchement selon une condition
   SI (condition) ALORS
     Instructions si VRAI
   SINON
     Instructions si FAUX
   FIN SI

3. BOUCLE TANT QUE — Répétition conditionnelle
   TANT QUE (condition) FAIRE
     Instructions
   FIN TANT QUE

4. BOUCLE POUR — Répétition avec compteur
   POUR i DE 1 À n FAIRE
     Instructions
   FIN POUR

EXEMPLE — Algorithme de la moyenne :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALGORITHME CalculerMoyenne
VARIABLES:
  notes : tableau de réels
  n : entier (nombre de notes)
  somme, moyenne : réels

DÉBUT
  somme ← 0
  POUR i DE 0 À n-1 FAIRE
    somme ← somme + notes[i]
  FIN POUR
  
  SI n > 0 ALORS
    moyenne ← somme / n
    AFFICHER "Moyenne: " + moyenne
  SINON
    AFFICHER "Aucune note!"
  FIN SI
FIN
""",
                "points_cles": [
                    "Algorithme = suite finie d'instructions non-ambiguës",
                    "3 structures: Séquence, Condition, Boucle",
                    "Pseudocode = langage intermédiaire entre français et code",
                    "Toujours penser l'algorithme AVANT d'écrire le code",
                    "Test de l'algorithme sur des cas simples avant implémentation"
                ],
                "exercice": "Écris un algorithme en pseudocode qui demande 5 nombres à l'utilisateur et affiche le plus grand.",
                "correction": "VARIABLES: max, n, i: entiers. DÉBUT. max ← 0. POUR i DE 1 À 5: LIRE n. SI n > max ALORS max ← n FIN SI. FIN POUR. AFFICHER 'Maximum: ' + max. FIN",
                "piege_prof": "Attention aux indices de tableaux: en C ils commencent à 0, pas 1. Un tableau de 5 éléments a des indices 0,1,2,3,4. L'élément à l'indice 5 N'EXISTE PAS et provoque un segfault."
            },
        ]
    },

    "Logique Mathématique": {
        "pole": "Mathématiques & Logique",
        "session": "1",
        "lecons": [
            {
                "titre": "Propositions, Connecteurs et Raisonnement Logique",
                "niveau_difficulte": 7,
                "theorie": """
LOGIQUE MATHÉMATIQUE — BASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Une PROPOSITION est un énoncé qui est soit VRAI soit FAUX (pas les deux).
Exemples: "2 + 2 = 4" (vrai), "Python est un langage compilé" (faux)
Non-exemples: "Ferme la porte!" (ordre), "x > 5" (dépend de x)

CONNECTEURS LOGIQUES :
  ¬P       : Négation (NON P)
  P ∧ Q    : Conjonction (P ET Q)
  P ∨ Q    : Disjonction (P OU Q)
  P → Q    : Implication (SI P ALORS Q)
  P ↔ Q    : Équivalence (P SI ET SEULEMENT SI Q)

IMPLICATION P → Q (PIÈGE CLASSIQUE !)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌───┬───┬───────┐
  │ P │ Q │ P → Q │
  ├───┼───┼───────┤
  │ V │ V │   V   │  ← Normal
  │ V │ F │   F   │  ← Promesse non tenue
  │ F │ V │   V   │  ← Surprenant! (faux → vrai = vrai)
  │ F │ F │   V   │  ← Surprenant! (faux → faux = vrai)
  └───┴───┴───────┘

RÈGLE D'OR : P → Q est FAUX seulement quand P est VRAI et Q est FAUX
Analogie: "SI tu travailles ALORS tu réussiras"
  - Si tu travailles et réussis → V (logique)
  - Si tu travailles et échoues → F (promesse non tenue)
  - Si tu ne travailles pas et réussis → V (pas de contradiction)
  - Si tu ne travailles pas et échoues → V (promesse pas violée)

FORMES ÉQUIVALENTES À P → Q :
  Contraposée : ¬Q → ¬P  (équivalente, même valeur de vérité)
  Réciproque  : Q → P    (PAS équivalente!)
  Inverse     : ¬P → ¬Q  (PAS équivalente!)

TAUTOLOGIE vs CONTRADICTION :
  Tautologie    : Toujours vraie   → P ∨ ¬P
  Contradiction : Toujours fausse  → P ∧ ¬P
  Contingence   : Parfois vrai/faux → P ∧ Q
""",
                "points_cles": [
                    "Proposition = énoncé vrai ou faux (pas les deux)",
                    "P→Q est FAUX seulement si P=Vrai et Q=Faux",
                    "Contraposée (¬Q→¬P) = équivalente à P→Q",
                    "Réciproque (Q→P) ≠ P→Q (erreur classique!)",
                    "Tautologie = toujours vraie (P∨¬P)"
                ],
                "exercice": "Donne la contraposée et la réciproque de: 'Si tu codes, tu comprends l'informatique'",
                "correction": "Original: P→Q (coder → comprendre). Contraposée: ¬Q→¬P = 'Si tu ne comprends pas l'informatique, tu ne codes pas' (ÉQUIVALENTE). Réciproque: Q→P = 'Si tu comprends l'informatique, tu codes' (PAS équivalente).",
                "piege_prof": "La contraposée EST logiquement équivalente à l'implication originale. La réciproque NE L'EST PAS. Beaucoup d'étudiants confondent les deux!"
            },
        ]
    },
}

COURS_L2 = {
    "Système d'Exploitation I": {
        "pole": "Développement & Système",
        "session": "1",
        "lecons": [
            {
                "titre": "Rôle et Structure d'un Système d'Exploitation",
                "niveau_difficulte": 8,
                "theorie": """
SYSTÈME D'EXPLOITATION — DÉFINITION PRÉCISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Un OS est un ensemble de programmes qui :
  1. GÈRE les ressources matérielles (CPU, RAM, disque, réseau)
  2. FOURNIT une interface entre les applications et le matériel
  3. PROTÈGE les processus les uns des autres

L'OS est l'INTERMÉDIAIRE entre le matériel et les logiciels.

ARCHITECTURE EN COUCHES :
━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─────────────────────────────────────┐
  │         Applications utilisateur    │ ← Word, Chrome, jeux
  ├─────────────────────────────────────┤
  │          Interface Utilisateur      │ ← GUI (Windows) / CLI (Linux)
  ├─────────────────────────────────────┤
  │            Appels Système           │ ← API entre user et kernel
  ├─────────────────────────────────────┤
  │         NOYAU (KERNEL)              │ ← Cœur de l'OS
  │  Gestionnaire:                      │
  │  • Processus    • Mémoire           │
  │  • Fichiers     • Périphériques     │
  ├─────────────────────────────────────┤
  │              MATÉRIEL               │ ← CPU, RAM, Disque
  └─────────────────────────────────────┘

MODE KERNEL vs MODE UTILISATEUR :
  Mode Kernel : Accès TOTAL au matériel (OS, drivers)
  Mode User   : Accès RESTREINT (applications normales)
  La séparation protège le système contre les apps malveillantes

GESTION DES PROCESSUS :
━━━━━━━━━━━━━━━━━━━━━━

États d'un processus :
  NOUVEAU → PRÊT → EXÉCUTION → BLOQUÉ → TERMINÉ
  
  • PRÊT    : En mémoire, attend le CPU
  • EXÉCUTION : Le CPU l'exécute en ce moment
  • BLOQUÉ  : Attend un événement (E/S, signal)

Ordonnancement (Scheduling) :
  FCFS (First Come First Served) : Simple, injuste pour les longs
  SJF  (Shortest Job First)       : Optimal en moyenne, starvation possible
  Round Robin                      : Équitable, chaque processus a un quantum
  Priorité                         : Processus critique d'abord
""",
                "points_cles": [
                    "OS = intermédiaire matériel/logiciels + gestionnaire ressources",
                    "Kernel = noyau, cœur de l'OS avec accès total",
                    "Mode Kernel vs Mode User = sécurité fondamentale",
                    "4 états processus: Prêt, Exécution, Bloqué, Terminé",
                    "Round Robin = algorithme d'ordonnancement équitable"
                ],
                "exercice": "Explique ce qui se passe au niveau de l'OS quand tu double-cliques sur un fichier .exe",
                "correction": "1. Shell détecte le double-clic. 2. Appel système fork() crée un nouveau processus. 3. exec() charge le programme en mémoire. 4. OS alloue de la RAM et du CPU. 5. Processus passe à l'état PRÊT puis EXÉCUTION.",
                "piege_prof": "Processus vs Thread : Le prof ADORE cette question. Processus = programme en exécution avec son propre espace mémoire ISOLÉ. Thread = unité d'exécution DANS un processus, partageant la mémoire. Plusieurs threads dans un processus = risque de race condition."
            },
        ]
    },

    "Outils de Développement Web": {
        "pole": "Développement & Système",
        "session": "1",
        "lecons": [
            {
                "titre": "HTML5 — Structure du Web Moderne",
                "niveau_difficulte": 5,
                "theorie": """
HTML5 — HYPERTEXT MARKUP LANGUAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HTML n'est PAS un langage de programmation — c'est un langage de BALISAGE.
Il structure le CONTENU, pas le comportement.

STRUCTURE D'UNE PAGE HTML5 :
━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!DOCTYPE html>          ← Déclare HTML5 (obligatoire)
<html lang="fr">         ← Racine du document
  <head>                 ← Métadonnées (non affichées)
    <meta charset="UTF-8">          ← Encodage des caractères
    <meta name="viewport" ...>      ← Responsive design
    <title>Titre</title>            ← Titre onglet navigateur
    <link rel="stylesheet" href=""> ← CSS externe
  </head>
  <body>                 ← Contenu visible
    ...
  </body>
</html>

BALISES SÉMANTIQUES HTML5 (IMPORTANT !) :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Avant HTML5 : tout était des <div>
Avec HTML5 : balises avec SENS
  <header>   : En-tête de la page ou section
  <nav>      : Menu de navigation
  <main>     : Contenu principal (une seule fois)
  <article>  : Contenu autonome (blog post, news)
  <section>  : Regroupement thématique
  <aside>    : Contenu secondaire (sidebar)
  <footer>   : Pied de page

POURQUOI SÉMANTIQUE ? 
  1. SEO : Google comprend mieux la structure
  2. Accessibilité : Lecteurs d'écran pour malvoyants
  3. Maintenabilité : Code plus lisible

ATTRIBUTS ESSENTIELS :
  id       : Identifiant UNIQUE dans la page
  class    : Groupe d'éléments pour CSS/JS
  href     : Lien vers URL (<a>)
  src      : Source d'une ressource (<img>, <script>)
  alt      : Texte alternatif pour images (accessibilité)
  style    : CSS inline (à éviter)
  data-*   : Attributs personnalisés HTML5
""",
                "points_cles": [
                    "HTML = langage de BALISAGE, pas de programmation",
                    "<!DOCTYPE html> obligatoire en HTML5",
                    "head = métadonnées, body = contenu visible",
                    "Balises sémantiques: header, nav, main, article, section, footer",
                    "id = unique, class = réutilisable"
                ],
                "exercice": "Crée la structure HTML5 d'un blog avec: en-tête, navigation, 2 articles, sidebar et pied de page.",
                "correction": "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Mon Blog</title></head><body><header><h1>Mon Blog</h1></header><nav><a href='#'>Accueil</a></nav><main><article>Article 1</article><article>Article 2</article></main><aside>Sidebar</aside><footer>© 2025</footer></body></html>",
                "piege_prof": "Différence <b> vs <strong> et <i> vs <em>: <b> et <i> sont purement visuels (gras, italique). <strong> indique une importance sémantique, <em> une emphase. Pour les lecteurs d'écran et le SEO, <strong> et <em> ont du sens, pas <b> et <i>."
            },
            {
                "titre": "CSS3 — Mise en Forme et Layout",
                "niveau_difficulte": 6,
                "theorie": """
CSS3 — CASCADE STYLE SHEETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━

CSS contrôle l'APPARENCE visuelle du HTML.
Séparation des rôles : HTML (structure) + CSS (présentation)

SÉLECTEURS CSS — HIÉRARCHIE DE SPÉCIFICITÉ :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Inline style   (1000pts) : style="color:red"      ← Priorité MAX
  #id            (100pts)  : #monId { color: red; }
  .classe        (10pts)   : .maClasse { color: red;}
  balise         (1pt)     : p { color: red; }       ← Priorité MIN

RÈGLE : En cas de conflit, la SPÉCIFICITÉ la plus haute gagne.
Si égalité, la règle déclarée EN DERNIER gagne (cascade).

BOX MODEL — TOUT ÉLÉMENT EST UNE BOÎTE :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌────────────────────────────────┐
  │           MARGIN               │ ← Espace ENTRE éléments
  │  ┌──────────────────────────┐  │
  │  │         BORDER           │  │ ← Bordure visible
  │  │  ┌────────────────────┐  │  │
  │  │  │     PADDING        │  │  │ ← Espace intérieur
  │  │  │  ┌──────────────┐  │  │  │
  │  │  │  │   CONTENT    │  │  │  │ ← Le contenu réel
  │  │  │  └──────────────┘  │  │  │
  │  │  └────────────────────┘  │  │
  │  └──────────────────────────┘  │
  └────────────────────────────────┘

box-sizing: border-box ← TOUJOURS utiliser!
  Sans: width=content seulement (confus)
  Avec: width=content+padding+border (intuitif)

FLEXBOX — LAYOUT 1D :
━━━━━━━━━━━━━━━━━━━━

.container {
  display: flex;
  justify-content: center;    /* Axe principal */
  align-items: center;        /* Axe secondaire */
  gap: 20px;
  flex-wrap: wrap;
}

GRID — LAYOUT 2D :
━━━━━━━━━━━━━━━━━

.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
""",
                "points_cles": [
                    "Spécificité: Inline(1000) > #id(100) > .classe(10) > balise(1)",
                    "Box model: Content + Padding + Border + Margin",
                    "box-sizing: border-box à toujours utiliser",
                    "Flexbox = 1D (ligne ou colonne), Grid = 2D",
                    "justify-content = axe principal, align-items = axe croisé"
                ],
                "exercice": "Écris le CSS pour centrer un div de 300x200px horizontalement et verticalement dans la page.",
                "correction": "body { display: flex; justify-content: center; align-items: center; min-height: 100vh; } .box { width: 300px; height: 200px; }",
                "piege_prof": "margin: auto vs text-align: center: margin: 0 auto centre un BLOC horizontalement. text-align: center centre le CONTENU texte inline. Pour centrer verticalement, il faut Flexbox ou Grid — il n'y a pas de vertical-align simple pour les blocs!"
            },
        ]
    },

    "Structure de Données": {
        "pole": "Développement & Système",
        "session": "2",
        "lecons": [
            {
                "titre": "Listes Chaînées — La Structure Fondamentale",
                "niveau_difficulte": 9,
                "theorie": """
LISTE CHAÎNÉE — DÉFINITION
━━━━━━━━━━━━━━━━━━━━━━━━━━

Une liste chaînée est une structure où chaque NŒUD contient :
  1. La DONNÉE (valeur stockée)
  2. Un POINTEUR vers le nœud suivant (ou NULL si dernier)

Avantage sur tableau : Taille DYNAMIQUE, insertion/suppression O(1)
Désavantage : Accès séquentiel O(n), mémoire supplémentaire pour pointeurs

REPRÉSENTATION :
  HEAD → [5|→] → [12|→] → [8|→] → [3|NULL]
         Nœud1    Nœud2    Nœud3   Dernier nœud

IMPLÉMENTATION EN C :
━━━━━━━━━━━━━━━━━━━━

typedef struct Noeud {
    int donnee;
    struct Noeud* suivant;
} Noeud;

// Créer un nœud
Noeud* creerNoeud(int val) {
    Noeud* n = (Noeud*)malloc(sizeof(Noeud));
    n->donnee = val;
    n->suivant = NULL;
    return n;
}

// Insérer en tête (O(1))
Noeud* insererTete(Noeud* head, int val) {
    Noeud* n = creerNoeud(val);
    n->suivant = head;
    return n; // Nouveau head
}

// Parcourir la liste (O(n))
void afficher(Noeud* head) {
    Noeud* courant = head;
    while (courant != NULL) {
        printf("%d → ", courant->donnee);
        courant = courant->suivant;
    }
    printf("NULL\\n");
}

// Libérer la mémoire (OBLIGATOIRE en C!)
void liberer(Noeud* head) {
    Noeud* temp;
    while (head != NULL) {
        temp = head;
        head = head->suivant;
        free(temp);
    }
}

COMPLEXITÉ :
  Insertion en tête : O(1)
  Insertion en queue : O(n) sans pointeur de queue
  Recherche        : O(n)
  Suppression tête : O(1)
  Accès par index  : O(n)
""",
                "points_cles": [
                    "Nœud = donnée + pointeur vers suivant",
                    "HEAD pointe vers le premier nœud",
                    "Dernier nœud a son pointeur à NULL",
                    "Toujours libérer la mémoire avec free() en C",
                    "Insertion tête O(1), accès index O(n)"
                ],
                "exercice": "Écris une fonction C qui calcule la longueur d'une liste chaînée.",
                "correction": "int longueur(Noeud* head) { int count = 0; Noeud* courant = head; while (courant != NULL) { count++; courant = courant->suivant; } return count; }",
                "piege_prof": "Memory leak en C: Si tu malloc() sans free() → fuite mémoire. Le programme consomme de plus en plus de RAM. En C, contrairement à Java/Python, il N'Y A PAS de garbage collector — tu dois gérer la mémoire manuellement."
            },
        ]
    },
}

COURS_L3 = {
    "MySQL I": {
        "pole": "Base de Données",
        "session": "1",
        "lecons": [
            {
                "titre": "Modélisation Relationnelle — Théorie et Pratique",
                "niveau_difficulte": 8,
                "theorie": """
BASES DE DONNÉES RELATIONNELLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Inventées par Edgar F. Codd (IBM, 1970) sur la théorie des ensembles.
Principe : données organisées en TABLES avec des RELATIONS entre elles.

TERMINOLOGIE PRÉCISE :
  Relation = Table
  Tuple    = Ligne / Enregistrement
  Attribut = Colonne / Champ
  Domaine  = Ensemble de valeurs possibles d'un attribut

CLÉS :
━━━━━

CLÉ PRIMAIRE (PRIMARY KEY) :
  • Identifie UNIQUEMENT chaque tuple
  • UNIQUE : Pas deux lignes avec la même valeur
  • NON NULL : Obligatoirement renseignée
  • SIMPLE : un attribut | COMPOSITE : plusieurs attributs

CLÉ ÉTRANGÈRE (FOREIGN KEY) :
  • Référence la clé primaire d'une AUTRE table
  • Assure l'INTÉGRITÉ RÉFÉRENTIELLE
  • Valeur doit exister dans la table référencée ou être NULL

FORMES NORMALES (NORMALISATION) :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1NF : Chaque cellule contient UNE SEULE valeur atomique
2NF : 1NF + Tout attribut dépend de TOUTE la clé primaire
3NF : 2NF + Pas de dépendance transitive (A→B→C interdit)

OPÉRATIONS RELATIONNELLES :
  σ (Sélection)    : Filtrer des lignes → WHERE
  π (Projection)   : Sélectionner des colonnes → SELECT col
  ⋈ (Jointure)     : Combiner deux tables → JOIN
  ∪ (Union)        : Réunir deux tables → UNION
  − (Différence)   : Lignes dans A mais pas B → EXCEPT

SQL COMPLET :
━━━━━━━━━━━━

DDL (Data Definition Language) :
  CREATE TABLE, ALTER TABLE, DROP TABLE

DML (Data Manipulation Language) :
  SELECT, INSERT, UPDATE, DELETE

DCL (Data Control Language) :
  GRANT, REVOKE (permissions)

TCL (Transaction Control Language) :
  BEGIN, COMMIT, ROLLBACK, SAVEPOINT
""",
                "points_cles": [
                    "Clé primaire = unique + non null + identifie une ligne",
                    "Clé étrangère = référence clé primaire autre table",
                    "Intégrité référentielle = cohérence des relations",
                    "3 formes normales pour éliminer la redondance",
                    "SQL divisé en DDL, DML, DCL, TCL"
                ],
                "exercice": "Conçois un schéma relationnel pour une école: étudiants, cours, et inscriptions.",
                "correction": "ETUDIANT(id_etudiant PK, nom, prenom, date_naissance). COURS(id_cours PK, titre, credits, id_prof FK). INSCRIPTION(id_etudiant FK, id_cours FK, note, date) PK=composite(id_etudiant, id_cours).",
                "piege_prof": "DELETE vs TRUNCATE vs DROP: DELETE supprime des lignes avec WHERE (rollback possible). TRUNCATE vide TOUTE la table ultra-rapidement (difficile à annuler). DROP supprime la TABLE ENTIÈRE structure+données. Pas la même chose!"
            },
        ]
    },

    "Réseaux I": {
        "pole": "Réseaux & Infrastructure",
        "session": "1",
        "lecons": [
            {
                "titre": "Modèle OSI et TCP/IP — La Tour de Babel Résolue",
                "niveau_difficulte": 9,
                "theorie": """
MODÈLE OSI — 7 COUCHES
━━━━━━━━━━━━━━━━━━━━━━

OSI = Open Systems Interconnection (ISO, 1984)
Objectif : Permettre à des équipements différents de communiquer.
Mnémotechnique (de bas en haut): 
"Please Do Not Throw Sausage Pizza Away"
(Physical, Data link, Network, Transport, Session, Presentation, Application)

┌────┬─────────────────┬──────────────────────────┬─────────────────┐
│ N° │     Couche      │          Rôle            │    Exemples     │
├────┼─────────────────┼──────────────────────────┼─────────────────┤
│  7 │ Application     │ Interface utilisateur    │ HTTP, FTP, DNS  │
│  6 │ Présentation    │ Format, chiffrement      │ SSL, TLS, JPEG  │
│  5 │ Session         │ Gestion sessions         │ NetBIOS, RPC    │
│  4 │ Transport       │ Fiabilité, ports         │ TCP, UDP        │
│  3 │ Réseau          │ Routage, adressage IP    │ IP, ICMP, ARP   │
│  2 │ Liaison         │ MAC, frames, switch      │ Ethernet, WiFi  │
│  1 │ Physique        │ Bits, câbles, signaux    │ RJ45, Fibre     │
└────┴─────────────────┴──────────────────────────┴─────────────────┘

MODÈLE TCP/IP — 4 COUCHES (PRATIQUE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────┬──────────────────┬──────────────────┐
│    TCP/IP        │   Correspond à   │     OSI          │
├──────────────────┼──────────────────┼──────────────────┤
│ Application      │ ←──────────────→ │ App+Prés+Session │
│ Transport        │ ←──────────────→ │ Transport        │
│ Internet         │ ←──────────────→ │ Réseau           │
│ Accès Réseau     │ ←──────────────→ │ Liaison+Physique │
└──────────────────┴──────────────────┴──────────────────┘

ENCAPSULATION DES DONNÉES :
  Application : DONNÉES
  Transport   : SEGMENT (TCP) / DATAGRAMME (UDP)
  Réseau      : PAQUET (avec IP source/destination)
  Liaison     : FRAME/TRAME (avec MAC source/destination)
  Physique    : BITS (0 et 1 sur le câble)

À chaque couche, on AJOUTE un EN-TÊTE (header) → ENCAPSULATION
À la réception, on RETIRE les en-têtes → DÉSENCAPSULATION

TCP vs UDP :
━━━━━━━━━━━

TCP (Transmission Control Protocol) :
  + Orienté connexion (handshake 3 voies: SYN, SYN-ACK, ACK)
  + Fiable (accusés de réception, retransmission)
  + Contrôle de flux et congestion
  + Ordre garanti
  - Plus lent
  Usage: HTTP, Email, FTP, SSH

UDP (User Datagram Protocol) :
  + Ultra-rapide (pas de connexion)
  + Faible latence
  - Non fiable (pas d'ACK)
  - Ordre non garanti
  Usage: DNS, Streaming, Jeux en ligne, VoIP
""",
                "points_cles": [
                    "OSI = 7 couches (théorique), TCP/IP = 4 couches (pratique)",
                    "Mnémotechnique OSI: Please Do Not Throw Sausage Pizza Away",
                    "Encapsulation = ajout d'en-têtes couche par couche",
                    "TCP = fiable + lent, UDP = rapide + non fiable",
                    "Handshake TCP = SYN → SYN-ACK → ACK"
                ],
                "exercice": "Sur quelle(s) couche(s) OSI opère un switch ? Un routeur ? Un hub ?",
                "correction": "HUB: Couche 1 (Physique) — répète les signaux sans intelligence. SWITCH: Couche 2 (Liaison) — achemine selon les adresses MAC. ROUTEUR: Couche 3 (Réseau) — route selon les adresses IP.",
                "piege_prof": "Switch vs Routeur vs Hub: Trois équipements DIFFÉRENTS! Hub=répéteur bête (L1), Switch=commutateur intelligent (L2, MAC), Routeur=routeur IP (L3). Un switch ne peut PAS connecter deux réseaux différents — il faut un routeur pour ça."
            },
        ]
    },
}

COURS_L4 = {
    "Python": {
        "pole": "Développement Avancé",
        "session": "1",
        "lecons": [
            {
                "titre": "Python Avancé — POO, Décorateurs et Générateurs",
                "niveau_difficulte": 9,
                "theorie": """
PYTHON — FONCTIONNALITÉS AVANCÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPRÉHENSIONS DE LISTES (List Comprehensions) :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Méthode classique
carres = []
for i in range(10):
    if i % 2 == 0:
        carres.append(i**2)

# Comprehension (élégant et rapide)
carres = [i**2 for i in range(10) if i % 2 == 0]

# Dict comprehension
scores = {etudiant: note for etudiant, note in zip(noms, notes)}

DÉCORATEURS :
━━━━━━━━━━━━

Un décorateur est une fonction qui ENVELOPPE une autre fonction.
Syntaxe sucre : @decorateur

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Appel de {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Fin de {func.__name__}")
        return result
    return wrapper

@logger  # Équivaut à: calculer = logger(calculer)
def calculer(a, b):
    return a + b

GÉNÉRATEURS :
━━━━━━━━━━━━

Un générateur produit des valeurs UNE À UNE (lazy evaluation).
Économise la mémoire pour de grandes séquences.

def fibonacci():
    a, b = 0, 1
    while True:
        yield a        # yield = pause + retourne valeur
        a, b = b, a + b

gen = fibonacci()
for _ in range(10):
    print(next(gen))   # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

GESTION DES EXCEPTIONS :
━━━━━━━━━━━━━━━━━━━━━━━

try:
    resultat = 10 / 0
except ZeroDivisionError as e:
    print(f"Erreur: {e}")
except (TypeError, ValueError) as e:
    print(f"Type/Valeur: {e}")
else:
    print("Succès!")    # Exécuté si pas d'exception
finally:
    print("Toujours")   # Exécuté dans tous les cas

# Lever une exception personnalisée
class ErreurUNASMOH(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

raise ErreurUNASMOH("Note invalide", 400)
""",
                "points_cles": [
                    "List comprehension = [expr for x in iter if cond]",
                    "Décorateur = fonction qui enveloppe une fonction",
                    "Generator + yield = lazy evaluation (économie mémoire)",
                    "try/except/else/finally pour la gestion d'erreurs",
                    "Exceptions personnalisées héritent de Exception"
                ],
                "exercice": "Écris un décorateur qui mesure le temps d'exécution d'une fonction.",
                "correction": "import time\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f'{func.__name__}: {time.time()-start:.4f}s')\n        return result\n    return wrapper",
                "piege_prof": "yield vs return: return termine la fonction et retourne une valeur. yield SUSPEND la fonction (l'état est conservé) et retourne une valeur — la prochaine fois qu'on appelle next(), l'exécution REPREND là où elle s'était arrêtée."
            },
        ]
    },

    "Linux I": {
        "pole": "Système & Administration",
        "session": "1",
        "lecons": [
            {
                "titre": "Administration Linux — Permissions, Processus, Shell Scripting",
                "niveau_difficulte": 9,
                "theorie": """
LINUX — SYSTÈME DE PERMISSIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Chaque fichier Linux a 3 types de permissions × 3 acteurs :

ACTEURS : Propriétaire (u) | Groupe (g) | Autres (o)
DROITS  : Lecture (r=4) | Écriture (w=2) | Exécution (x=1)

Affichage: ls -la
  -rwxr-xr-- 1 lucky users 1024 Jan 15 main.py
  │└──┘└──┘└──┘
  │ u   g   o
  Type fichier (-=fichier, d=dossier, l=lien)

CHMOD — MODIFIER LES PERMISSIONS :
Notation octale :
  chmod 755 fichier.py
  7 = rwx (4+2+1) → Propriétaire : lecture+écriture+exécution
  5 = r-x (4+0+1) → Groupe : lecture+exécution
  5 = r-x (4+0+1) → Autres : lecture+exécution

Notation symbolique :
  chmod u+x fichier.py    → Ajouter exécution au propriétaire
  chmod go-w fichier.py   → Retirer écriture au groupe et autres
  chmod a+r fichier.py    → Ajouter lecture à tous

SHELL SCRIPTING :
━━━━━━━━━━━━━━━━

#!/bin/bash
# Shebang : indique l'interpréteur

# Variables
NOM="Lucky Luke"
ANNEE=2025
echo "Bonjour $NOM, nous sommes en $ANNEE"

# Conditions
if [ $ANNEE -gt 2024 ]; then
    echo "Nouveau!"
elif [ $ANNEE -eq 2024 ]; then
    echo "Cette année"
else
    echo "Passé"
fi

# Boucles
for i in 1 2 3 4 5; do
    echo "Étape $i"
done

# Boucle while
compteur=0
while [ $compteur -lt 5 ]; do
    echo "Compteur: $compteur"
    ((compteur++))
done

# Fonctions
saluer() {
    echo "Salut, $1!"  # $1 = premier argument
}
saluer "UNASMOH"

# Vérifier l'existence d'un fichier
if [ -f "fichier.txt" ]; then
    echo "Fichier existe"
fi
""",
                "points_cles": [
                    "Permissions: rwx pour user, group, others",
                    "chmod 755 = rwxr-xr-x (octal)",
                    "Shebang #!/bin/bash en première ligne",
                    "Variables: NOM='val', utilisation: $NOM",
                    "[ ] pour les conditions dans if/while"
                ],
                "exercice": "Écris un script bash qui liste tous les fichiers .py dans le répertoire courant et affiche leur taille.",
                "correction": "#!/bin/bash\nfor fichier in *.py; do\n  if [ -f \"$fichier\" ]; then\n    taille=$(wc -c < \"$fichier\")\n    echo \"$fichier : $taille octets\"\n  fi\ndone",
                "piege_prof": "chmod 777 = DANGER! Donner rwx à TOUT LE MONDE est une faille de sécurité majeure. Sur un serveur, ça permet à n'importe qui de modifier/exécuter le fichier. La bonne pratique: 755 pour les scripts, 644 pour les fichiers de données."
            },
        ]
    },
}


COURS_L4 = {
    "Gestion de Projet Informatique": {
        "pole": "Management & Ingénierie",
        "session": "1",
        "lecons": [
            {
                "titre": "Méthodes Agiles & Scrum",
                "theorie": "La méthode Agile privilégie les individus et les interactions sur les processus. Scrum est un cadre de travail Agile basé sur des itérations appelées 'Sprints' (1 à 4 semaines). Les rôles principaux sont le Product Owner (vision du produit), le Scrum Master (facilitateur) et l'Équipe de Développement.",
                "points_cles": [
                    "Sprints : Itérations courtes et régulières.",
                    "Product Backlog : Liste de toutes les fonctionnalités attendues.",
                    "Daily Standup : Réunion quotidienne de 15 minutes."
                ],
                "exercice": "Comment s'appelle la liste priorisée des tâches à réaliser dans Scrum ?",
                "correction": "Le Product Backlog.",
                "piege_prof": "Ne pas confondre le Product Backlog (tout le projet) et le Sprint Backlog (tâches du sprint en cours)."
            }
        ]
    },
    "Intelligence Artificielle": {
        "pole": "Data Science & IA",
        "session": "1",
        "lecons": [
            {
                "titre": "Machine Learning : Apprentissage Supervisé",
                "theorie": "L'apprentissage supervisé consiste à entraîner un modèle sur des données étiquetées (ex: images de chats reconnues comme 'chat'). Le modèle apprend une fonction de mapping des entrées vers les sorties pour faire des prédictions sur de nouvelles données.",
                "points_cles": [
                    "Classification : Prédire une catégorie (ex: Spam ou Non Spam).",
                    "Régression : Prédire une valeur continue (ex: Prix d'une maison).",
                    "Overfitting (Surapprentissage) : Le modèle apprend par cœur au lieu de généraliser."
                ],
                "exercice": "Quel type d'apprentissage supervisé utiliseriez-vous pour prédire la température de demain ?",
                "correction": "Une régression, car on cherche à prédire une valeur numérique continue.",
                "piege_prof": "Penser que le Machine Learning est magique. Un mauvais jeu de données d'entraînement donnera toujours un mauvais modèle (Garbage In, Garbage Out)."
            }
        ]
    },
    "Big Data & Analytics": {
        "pole": "Data Science & IA",
        "session": "2",
        "lecons": [
            {
                "titre": "Les 5 'V' du Big Data",
                "theorie": "Le Big Data se caractérise traditionnellement par 5 dimensions (les 5 V) : Volume (quantité massive), Vélocité (vitesse de génération), Variété (données structurées, non structurées), Véracité (fiabilité des données), et Valeur (utilité extraite).",
                "points_cles": [
                    "Hadoop & Spark : Outils phares pour le traitement de gros volumes.",
                    "Données non structurées : Vidéos, tweets, logs, qui ne rentrent pas dans un tableau SQL classique."
                ],
                "exercice": "Quel 'V' fait référence à la rapidité avec laquelle les données sont générées ?",
                "correction": "La Vélocité.",
                "piege_prof": "Confondre une base de données relationnelle classique (SQL) et un écosystème Big Data (NoSQL / Hadoop) qui scale horizontalement."
            }
        ]
    }
}

PROGRAMME_COMPLET = {
    "L1 (Licence 1)": {"description": "Fondamentaux et algorithmique", "cours": COURS_L1},
    "L2 (Licence 2)": {"description": "Systèmes et programmation avancée", "cours": COURS_L2},
    "L3 (Licence 3)": {"description": "Bases de données et réseaux", "cours": COURS_L3},
    "L4 (Licence 4)": {"description": "Ingénierie logicielle et spécialisation", "cours": COURS_L4},
}

def get_cours_by_niveau(niveau: str) -> dict:
    """Retourne les cours d'un niveau donné."""
    mapping = {"L1": COURS_L1, "L2": COURS_L2, "L3": COURS_L3, "L4": COURS_L4}
    return mapping.get(niveau, {})

def get_all_matieres() -> list:
    """Retourne toutes les matières de L1 à L4."""
    all_matieres = []
    for niveau, cours in [("L1", COURS_L1), ("L2", COURS_L2), ("L3", COURS_L3), ("L4", COURS_L4)]:
        for matiere in cours.keys():
            all_matieres.append({"niveau": niveau, "matiere": matiere})
    return all_matieres