export interface ChatPattern {
  regex: string;
  priority: number;
  responses: string[];
}

export const CHAT_PATTERNS: ChatPattern[] = [
  {
    "regex": "(methode|technique|conseil|comment|astuce).{0,30}(etude|etudier|apprendre|memoriser|productivite|revise|revision)",
    "priority": 2,
    "responses": [
      "📚 **Conseils de Productivité pour Étudiant en Informatique** :\n\n⏱️ Méthode Pomodoro\n- 25 min de travail intense → 5 min de pause → 4 cycles → pause 20 min\n- Utilisez le widget Pomodoro en haut à droite d'Asta Académie !\n\n💡 Technique Feynman\n- Expliquez le concept à voix haute comme à un enfant de 10 ans\n- Identifiez ce que vous ne savez pas vraiment → relisez → recommencez\n\n🧠 Rappel Actif (Active Recall)\n- Ne relisez pas passivement. Fermez le cours et testez-vous !\n- Utilisez le module Quiz d'Asta Académie après chaque leçon.\n\n🔁 Répétition Espacée\n- Révisez une leçon J+1, J+3, J+7, J+14 après l'avoir apprise.\n- Ce schéma ancre l'information dans la mémoire à long terme."
    ]
  },
  {
    "regex": "(fatigue|fatiguee|epuise|epuisee|stresse|stressee|stress|motive|motiver|motivation|marre|decourage|rate|pleure|abandonne|difficile|dur|complique)",
    "priority": 2,
    "responses": [
      "🔥 **Message de Soutien de Space AI** :\n\nLes études en Sciences Informatiques à l'UNASMOH sont exigeantes, mais chaque ligne de code, de devoir, de projet vous rapproche de votre diplôme. Ne vous décourager pas.🎓\n\n• Faites une vraie pause : 15 min loin des écrans, c'est du temps gagné.\n• Divisez pour régner : Découpez le problème en sous-problèmes — comme en algorithmique !\n• Le droit à l'erreur : Un bug résolu = une compétence acquise. C'est mathématique. il y a un truc de Space aime dire, Si tes codes on des erreurs mais que le script marche correctement ne touche plus a rien.\n\n« Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte. »\n— Winston Churchill",
      "💪 Space AI et le Staff de Asta Academie vous soutient !\n\nTout ingénieur a eu des moments de doute. Ce qui les distingue, c'est qu'ils ont continué malgré tout.\n\n• Souvenez-vous du pourquoi vous avez commencé.\n• Chaque cours maîtrisé est une brique de votre avenir.\n• Tapez 'stats' pour voir votre progression — vous avancez plus vite que vous ne le croyez !\n\n« La persévérance est ce qui fait la différence entre l'échec et la réussite. »"
    ]
  },
  {
    "regex": "(comment|aide|fonctionne|tuto|tutoriel|features|fonctionnalites|utiliser|modules?).{0,25}(application|asta|academie|plateforme)",
    "priority": 2,
    "responses": [
      "🔧 Guide d'Utilisation d'Asta Académie :\n\n| Module | Description |\n| :--- | :--- |\n| 🏠 Accueil | Progression XP, badges débloqués, streak de connexion 🔥 |\n| 📚 Cours | Leçons complètes L1 → L4, filtrées par matière |\n| 🛡️ DevSecurity | Cybersécurité éthique et outils de simulation |\n| 📝 Mes Notes | Rédigez et sauvegardez vos notes par leçon |\n| 📊 Moyennes | Calculez votre moyenne générale à partir de vos notes d'examens |\n| 🔧 Outils | SpaceCode : éditeur Python intégré, sans quitter l'app |\n| 🤖 Asta AI | Moi ! Quiz interactifs, questions de cours, navigation vocale |\n\n💡 Tapez le nom d'un module pour y accéder directement (ex: 'va sur les notes')Si vous avez des idées, des bugs, ou si vous voulez soutenir le projet veuillez nous contacter sur : whatsaap +509 35 67 2037 ou par : mail astaxacademie509@gmail.com"
    ]
  },
  {
    "regex": "\\b(pomodoro|25 min|technique de temps|minuteur)\\b",
    "priority": 1,
    "responses": [
      "⏱️ La Technique Pomodoro :\n\nInventée par Francesco Cirillo à la fin des années 1980, elle maximise la concentration.\n\nCycle standard :\n1. 🎯 Choisissez une seule tâche\n2. ⏰ Travaillez 25 minutes sans interruption\n3. ☕ Pause courte de 5 minutes\n4. Répétez × 4, puis pause longue de 20-30 minutes\n\n🚀 Le widget Pomodoro d'Asta Académie est disponible en haut à droite — utilisez-le !"
    ]
  },
  {
    "regex": "\\b(feynman|richard feynman)\\b",
    "priority": 1,
    "responses": [
      "💡 La Technique Feynman :\n\nMise au point par le prix Nobel de physique Richard Feynman, c'est la méthode la plus efficace pour vraiment comprendre.\n\nLes 4 étapes :\n1. ✍️ Écrivez le concept à apprendre sur une feuille\n2. 🗣️ Expliquez-le comme à un enfant de 10 ans (sans jargon)\n3. 🔍 Identifiez les lacunes : là où vous bloquez = ce que vous ne maîtrisez pas\n4. 📖 Retournez au cours, clarifiez, recommencez\n\nSi vous ne pouvez pas l'expliquer simplement, c'est que vous ne le comprenez pas encore vraiment."
    ]
  },
  {
    "regex": "\\b(moore|loi de moore|transistors?)\\b",
    "priority": 1,
    "responses": [
      "⚙️ La Loi de Moore :\n\nÉnoncée par Gordon Moore (co-fondateur d'Intel) en 1965 :\n\n> Le nombre de transistors sur un microprocesseur double environ tous les deux ans, à coût constant.\n\nImpact : Cette observation empirique a guidé l'industrie tech pendant 50+ ans.\n\nSituation actuelle : La loi ralentit face aux limites physiques atomiques (effet tunnel quantique). Les puces modernes comme l'Apple M-series ou les GPU NVIDIA atteignent 3-5 nm de finesse de gravure.\n\nLa suite : Informatique quantique, puces 3D, neuromorphique... 🚀"
    ]
  },
  {
    "regex": "\\b(turing|alan turing|machine de turing|test de turing)\\b",
    "priority": 1,
    "responses": [
      "🧠 Alan Turing (1912-1954) :\n\nMathématicien britannique, père fondateur de l'informatique et de l'IA.\n\nContributions majeures :\n• Machine de Turing : Modèle théorique universel de tout ordinateur\n  (ruban infini + tête L/E + table d'états)\n• Thèse de Church-Turing** : Tout algorithme peut être simulé par une Machine de Turing\n• Test de Turing : Un ordinateur est 'intelligent' si un humain ne peut pas distinguer ses réponses de celles d'un autre humain\n• Enigma : A décrypté le code nazi pendant la WWII, sauvant des millions de vies\n\nTuring est la raison pour laquelle vous avez un ordinateur aujourd'hui. 🙏"
    ]
  },
  {
    "regex": "\\b(von neumann|architecture (de )?von neumann|architecture ordinateur)\\b",
    "priority": 1,
    "responses": [
      "🖥️ Architecture de Von Neumann (1945) :\n\n99% des ordinateurs actuels reposent sur cette structure fondamentale.\n\n4 composants principaux :\n1. CPU (Processeur) : UC (contrôle) + UAL (calcul)\n2. RAM (Mémoire centrale) : stocke données ET instructions ensemble\n   (innovation révolutionnaire : le programme stocké !)\n3. Entrées/Sorties : clavier, écran, réseau...\n4. Bus : lignes de données, d'adresses et de contrôle\n\nCycle d'instruction : Fetch → Decode → Execute → Write Back\n\n⚠️ Goulot de Von Neumann : La vitesse CPU dépasse celle de la RAM → caches L1/L2/L3 pour compenser !"
    ]
  },
  {
    "regex": "\\b(de morgan|morgan|loi logique|algebre boole|boole|logique booleenne)\\b",
    "priority": 1,
    "responses": [
      "📐 Les Lois de De Morgan (logique booléenne) :\n\nCes deux lois permettent de simplifier les expressions logiques complexes :\n\nLoi 1 : `NOT (A AND B)  ≡  (NOT A) OR (NOT B)`\n```python\nnot (a and b) == (not a) or (not b)  # True\n```\n\nLoi 2 : `NOT (A OR B)  ≡  (NOT A) AND (NOT B)`\n```python\nnot (a or b) == (not a) and (not b)  # True\n```\n\nUsage pratique : Simplifier des `if` imbriqués en code et concevoir des circuits logiques.\n\n💡 Astuce examen : transformez toujours un NOT sur une parenthèse avec De Morgan !*"
    ]
  },
  {
    "regex": "\\b(pile|heap|stack|tas|memoire (pile|heap|stack|tas))\\b",
    "priority": 1,
    "responses": [
      "🧠 **Stack (Pile) vs Heap (Tas)** — Gestion de la mémoire :\n\n| Critère | Stack 🥞 | Heap 📦 |\n| :--- | :--- | :--- |\n| Vitesse | Ultra-rapide | Plus lente |\n| Gestion | Automatique (LIFO) | Manuelle / GC |\n| Contenu | Var. locales, primitifs | Objets, tableaux dynamiques |\n| Taille | Limitée et fixe | Grande, flexible |\n| Risque | Stack Overflow | Memory Leak |\n\n```python\n# Stack : variable locale\ndef foo():\n    x = 42  # sur la stack\n\n# Heap : objet dynamique\nobj = MyClass()  # sur le heap\n```\n\n⚠️ *Piège classique : récursion infinie → Stack Overflow !*"
    ]
  },
  {
    "regex": "\\b(algorithme|algo|complexite|big.?o|o\\(n\\)|o\\(log|notation asymptotique)\\b",
    "priority": 2,
    "responses": [
      "📊 Complexité Algorithmique — Notation Big O :\n\nLa notation Big O décrit le comportement d'un algorithme quand n → ∞.\n\n| Notation | Nom | Exemple |\n| :--- | :--- | :--- |\n| O(1) | Constant | Accès tableau par index |\n| O(log n) | Logarithmique | Recherche binaire |\n| O(n) | Linéaire | Parcours de liste |\n| O(n log n) | Quasi-linéaire | Tri rapide (moyen), Merge sort |\n| O(n²) | Quadratique | Tri à bulles, Tri sélection |\n| O(2ⁿ) | Exponentiel | Problèmes NP (voyageur de commerce) |\n\n⚠️ **Règle d'or :** On ne garde que le terme dominant.\n`3n² + 100n + 5 → O(n²)`\n\n💡 Notez-Bien : Big O mesure le PIRE cas, pas le cas moyen !"
    ]
  },
  {
    "regex": "\\b(tri|trier|sorting|bubble sort|merge sort|quick sort|tri bulles|tri fusion|tri rapide|tri insertion|tri selection)\\b",
    "priority": 1,
    "responses": [
      "🔀 Algorithmes de Tri — Comparaison :\n\n| Algorithme | Meilleur | Moyen | Pire | Stable? |\n| :--- | :---: | :---: | :---: | :---: |\n| Tri à Bulles | O(n) | O(n²) | O(n²) | ✅ |\n| Tri Sélection | O(n²) | O(n²) | O(n²) | ❌ |\n| Tri Insertion | O(n) | O(n²) | O(n²) | ✅ |\n| Tri Fusion | O(n log n) | O(n log n) | O(n log n) | ✅ |\n| Tri Rapide | O(n log n) | O(n log n) | O(n²) | ❌ |\n\nTri Fusion en Python (exemple) :\n```python\ndef merge_sort(lst):\n    if len(lst) <= 1: return lst\n    mid = len(lst) // 2\n    left = merge_sort(lst[:mid])\n    right = merge_sort(lst[mid:])\n    return merge(left, right)\n```\n\n💡 Python utilise Timsort (fusion de Merge sort + Insertion sort) — O(n log n) garanti."
    ]
  },
  {
    "regex": "\\b(recursion|recursivite|recursif|recursive|fonction recursive|appel recursif|factorielle|fibonacci)\\b",
    "priority": 1,
    "responses": [
      "♻️ La Récursivité :\n\nUne fonction est récursive si elle s'appelle elle-même.\n\nStructure obligatoire :\n1. Cas de base\\: condition d'arrêt (sans ça → Stack Overflow !)\n2. Cas récursif : appel de la fonction avec un problème plus petit\n\n```python\n# Factorielle récursive\ndef factorielle(n):\n    if n <= 1:        # ← cas de base\n        return 1\n    return n * factorielle(n - 1)  # ← cas récursif\n\n# Fibonacci\ndef fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)  # ⚠️ Exponentiel sans mémoïsation !\n```\n\n⚠️ Piège : `fib(n)` naïf est O(2ⁿ). Utilisez la mémoïsation :\n```python\nfrom functools import lru_cache\n@lru_cache(maxsize=None)\ndef fib(n): ...\n```"
    ]
  },
  {
    "regex": "\\b(structure de donnees?|liste chainee?|linked.?list|arbre|tree|graphe|graph|hash.?table|dictionnaire|file d.attente|queue|deque)\\b",
    "priority": 1,
    "responses": [
      "🗂️ Structures de Données Fondamentales :\n\n| Structure | Accès | Insertion | Suppression | Usage |\n| :--- | :---: | :---: | :---: | :--- |\n| Tableau | O(1) | O(n) | O(n) | Accès rapide par index |\n| Liste chaînée | O(n) | O(1) | O(1) | Insertions/supp. fréquentes |\n| Pile (Stack) | O(1) | O(1) | O(1) | Appels de fonctions, Undo |\n| File (Queue) | O(1) | O(1) | O(1) | BFS, files d'attente |\n| Table de hachage | O(1)* | O(1)* | O(1)* | Recherche rapide |\n| Arbre BST | O(log n)* | O(log n)* | O(log n)* | Données ordonnées |\n| Graphe | — | O(1) | O(V+E) | Réseaux, navigation |\n\n*= cas moyen\n\n💡 En Python : `list` = tableau dynamique, `dict` = table de hachage, `deque` (collections) = file double-extrémité O(1)."
    ]
  },
  {
    "regex": "\\b(poo|oop|objet|classe|heritage|polymorphisme|encapsulation|abstraction|interface|methode|attribut|constructeur|__init__)\\b",
    "priority": 2,
    "responses": [
      "🧩 Programmation Orientée Objet (POO) :\n\nLes 4 piliers :\n\n1. Encapsulation 🔒 : Cacher les détails internes, exposer une interface claire\n   ```python\n   class Compte:\n       def __init__(self):\n           self.__solde = 0  # privé\n       def deposer(self, m): self.__solde += m\n   ```\n\n2. Héritage 👨‍👩‍👧 : Une classe fils hérite des attributs/méthodes de la classe parent\n   ```python\n   class Animal:\n       def parler(self): pass\n   class Chien(Animal):\n       def parler(self): return 'Woof!'\n   ```\n\n3. Polymorphisme 🎭 : Même méthode, comportements différents selon la classe\n\n4. Abstraction 🎨 : N'exposer que l'essentiel, masquer la complexité\n\n💡 Principe SOLID → lisez-le après avoir maîtrisé la POO !"
    ]
  },
  {
    "regex": "\\b(python|py|script python|langage python)\\b",
    "priority": 1,
    "responses": [
      "🐍 Python — Points Essentiels :\n\nPourquoi Python ?\n- Syntaxe lisible, courbe d'apprentissage douce\n- Écosystème immense (IA, Data Science, Web, Scripts...)\n- Langage #1 mondial selon l'index TIOBE 2024\n\nConcepts à maîtriser :\n```python\n# List comprehension (pythonique)\ncarre = [x**2 for x in range(10)]\n\n# Décorateur\n@staticmethod\ndef ma_func(): ...\n\n# Générateur (mémoire optimisée)\ndef pairs():\n    for i in range(100):\n        if i % 2 == 0: yield i\n```\n\n🔧 Testez vos scripts dans SpaceCode (onglet Outils) sans quitter l'app !"
    ]
  },
  {
    "regex": "\\b(decorateur|decorator|@staticmethod|@classmethod|@property|@lru_cache|functools)\\b",
    "priority": 1,
    "responses": [
      "🎨 **Décorateurs Python** :\n\nUn décorateur est une fonction qui **modifie le comportement** d'une autre fonction.\n\n```python\n# Décorateur simple\ndef logger(func):\n    def wrapper(*args, **kwargs):\n        print(f'Appel de {func.__name__}')\n        return func(*args, **kwargs)\n    return wrapper\n\n@logger\ndef addition(a, b): return a + b\n```\n\n**Décorateurs intégrés :**\n- `@staticmethod` : méthode sans accès à `self`\n- `@classmethod` : méthode avec accès à la classe (`cls`)\n- `@property` : getter/setter élégant\n- `@lru_cache` : mémoïsation automatique\n\n💡 *Les décorateurs sont partout en frameworks (Flask `@app.route`, Django, FastAPI...)*"
    ]
  },
  {
    "regex": "\\b(generateur|generator|yield|iterateur|iterator|comprehension|list comp)\\b",
    "priority": 1,
    "responses": [
      "⚡ **Générateurs & Itérateurs Python** :\n\nUn **générateur** produit les valeurs une par une (lazy evaluation) — économise la RAM pour les grandes séquences.\n\n```python\n# Générateur : yield au lieu de return\ndef fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\ngen = fibonacci()\nprint(next(gen))  # 0\nprint(next(gen))  # 1\n```\n\n**Comparaison mémoire :**\n```python\n# ❌ Charge tout en RAM : [0,1,4,9,...] pour 1M éléments\nliste = [x**2 for x in range(1_000_000)]\n\n# ✅ Génère à la demande : O(1) RAM\ngen = (x**2 for x in range(1_000_000))\n```\n\n💡 *Règle : si vous parcourez une seule fois → utilisez un générateur.*"
    ]
  },
  {
    "regex": "\\b(osi|modele osi|couche (physique|liaison|reseau|transport|session|presentation|application)|7 couches)\\b",
    "priority": 3,
    "responses": [
      "🌐 **Modèle OSI — 7 Couches** :\n\n| # | Couche | Rôle | Protocoles |\n| :---: | :--- | :--- | :--- |\n| 7 | Application | Interface utilisateur | HTTP, FTP, SMTP, DNS |\n| 6 | Présentation | Encodage, chiffrement | SSL/TLS, JPEG, ASCII |\n| 5 | Session | Gestion de sessions | NetBIOS, RPC |\n| 4 | Transport | Segmentation, fiabilité | TCP, UDP |\n| 3 | Réseau | Routage, adressage IP | IP, ICMP, ARP |\n| 2 | Liaison | Trame, adresse MAC | Ethernet, WiFi |\n| 1 | Physique | Signal physique | Câbles, fibres, radio |\n\n**Mnémotechnique (bas→haut) :** *Please Do Not Throw Sausage Pizza Away*\n\n⚠️ *Piège exam : TCP/IP a 4 couches, pas 7 comme OSI.*"
    ]
  },
  {
    "regex": "\\b(tcp|udp|tcp.?ip|protocole de transport)\\b",
    "priority": 1,
    "responses": [
      "📡 **TCP vs UDP** :\n\n| Critère | TCP 🔒 | UDP ⚡ |\n| :--- | :--- | :--- |\n| Connexion | Orienté connexion (handshake 3 voies) | Sans connexion |\n| Fiabilité | Garanti (accusés de réception) | Non garanti |\n| Ordre | Garantit l'ordre des paquets | Ordre non garanti |\n| Vitesse | Plus lent | Très rapide |\n| Usage | Web, email, FTP | Streaming, gaming, DNS, VoIP |\n\n**Handshake TCP (3 voies) :**\n```\nClient → SYN  → Serveur\nClient ← SYN-ACK ← Serveur\nClient → ACK  → Serveur  ✅ Connexion établie\n```\n\n💡 *Règle : si perdre un paquet est inacceptable → TCP. Si la vitesse prime → UDP.*"
    ]
  },
  {
    "regex": "\\b(http|https|rest|api rest|requete http|get|post|put|delete|patch|endpoint|status.?code|200|404|500)\\b",
    "priority": 1,
    "responses": [
      "🌍 **HTTP & API REST** :\n\n**Méthodes HTTP :**\n| Méthode | Action | Idempotent? |\n| :--- | :--- | :---: |\n| GET | Lire | ✅ |\n| POST | Créer | ❌ |\n| PUT | Remplacer entier | ✅ |\n| PATCH | Modifier partiel | ❌ |\n| DELETE | Supprimer | ✅ |\n\n**Codes de statut importants :**\n- `200 OK` — succès\n- `201 Created` — ressource créée\n- `400 Bad Request` — erreur client\n- `401 Unauthorized` — non authentifié\n- `403 Forbidden` — non autorisé\n- `404 Not Found` — ressource inexistante\n- `500 Internal Server Error` — erreur serveur\n\n💡 *Testez vos APIs avec Postman, Insomnia ou `curl` en terminal.*"
    ]
  },
  {
    "regex": "\\b(dns|domain name|nom de domaine|resolution dns|serveur dns)\\b",
    "priority": 1,
    "responses": [
      "🔍 **DNS — Domain Name System** :\n\nLe DNS est le **'annuaire téléphonique d'Internet'** : il traduit un nom de domaine lisible en adresse IP.\n\n**Résolution DNS (simplifié) :**\n```\nVous tapez : www.google.com\n   1. Navigateur vérifie son cache DNS local\n   2. Demande au résolveur DNS du FAI\n   3. Résolveur interroge le serveur racine (.)\n   4. Puis le serveur TLD (.com)\n   5. Puis le serveur autoritaire de google.com\n   → Retourne : 142.250.74.68\n```\n\n**Types d'enregistrements courants :**\n- `A` → nom → IPv4\n- `AAAA` → nom → IPv6\n- `CNAME` → alias → autre nom\n- `MX` → serveur de mail\n\n⚠️ *DNS utilise UDP port 53 (pas TCP — rapidité prioritaire).*"
    ]
  },
  {
    "regex": "\\b(sql|base de donnees?|bdd|sgbd|mysql|postgresql|sqlite|requete sql|jointure|join|select|where|group by)\\b",
    "priority": 2,
    "responses": [
      "🗄️ **SQL & Bases de Données Relationnelles** :\n\n**Requête SELECT complète :**\n```sql\nSELECT colonne, COUNT(*) AS total\nFROM table\nWHERE condition\nGROUP BY colonne\nHAVING COUNT(*) > 5\nORDER BY total DESC\nLIMIT 10;\n```\n\n**Types de JOIN :**\n| JOIN | Résultat |\n| :--- | :--- |\n| INNER JOIN | Lignes qui matchent dans les 2 tables |\n| LEFT JOIN | Tout de gauche + matching droite |\n| RIGHT JOIN | Tout de droite + matching gauche |\n| FULL OUTER JOIN | Tout des 2 tables |\n\n**Propriétés ACID (transactions) :**\n- **A**tomicité : tout ou rien\n- **C**ohérence : état valide avant/après\n- **I**solation : transactions indépendantes\n- **D**urabilité : résultat permanent\n\n💡 *Pratiquez avec SQLite — il est intégré à Python (`import sqlite3`) !*"
    ]
  },
  {
    "regex": "\\b(normalisation|normal form|1nf|2nf|3nf|bcnf|dependance fonctionnelle)\\b",
    "priority": 1,
    "responses": [
      "📋 **Normalisation des Bases de Données** :\n\nProcessus d'organisation des tables pour éliminer la redondance.\n\n| Forme | Règle |\n| :--- | :--- |\n| **1NF** | Pas de valeurs multiples dans une cellule, clé primaire définie |\n| **2NF** | 1NF + tout attribut non-clé dépend de la CLÉ ENTIÈRE |\n| **3NF** | 2NF + pas de dépendance transitive (A→B→C non-clé interdit) |\n| **BCNF** | 3NF renforcée : tout déterminant est une super-clé |\n\n**Exemple de problème :**\n```\n❌ Table: (StudentID, CourseID, StudentName, InstructorName)\n   StudentName dépend de StudentID seulement → violation 2NF\n\n✅ Séparer en: Students(StudentID, StudentName)\n              Courses(CourseID, InstructorName)\n```\n\n⚠️ Piège : la sur-normalisation peut tuer les performances (trop de JOINs)."
    ]
  },
  {
    "regex": "\\b(processus|process|thread|fil d.execution|concurrence|parallelisme|mutex|semaphore|deadlock|interblocage)\\b",
    "priority": 2,
    "responses": [
      "⚙️ **Processus vs Thread — Systèmes d'Exploitation** :\n\n| Critère | Processus | Thread |\n| :--- | :--- | :--- |\n| Mémoire | Espace mémoire isolé | Partage la mémoire du processus |\n| Création | Lente (fork) | Rapide |\n| Communication | IPC complexe | Variables partagées directes |\n| Crash | Isolé (n'affecte pas les autres) | Peut crasher tout le processus |\n\n**Problème du Deadlock (interblocage) :**\n```\nThread A détient Ressource 1, attend Ressource 2\nThread B détient Ressource 2, attend Ressource 1\n→ Blocage infini !\n```\n\n**Conditions de Coffman (toutes 4 requises pour deadlock) :**\n1. Exclusion mutuelle\n2. Détention et attente\n3. Pas de préemption\n4. Attente circulaire\n\n💡 *Python GIL : un seul thread Python actif à la fois → utilisez `multiprocessing` pour le CPU.*"
    ]
  },
  {
    "regex": "\\b(ordonnancement|scheduler|scheduling|round.?robin|fifo|sjf|priorite|preemptif)\\b",
    "priority": 1,
    "responses": [
      "🗓️ **Ordonnancement des Processus** :\n\nL'ordonnanceur (scheduler) du SE décide quel processus utilise le CPU.\n\n| Algorithme | Description | Avantage | Inconvénient |\n| :--- | :--- | :--- | :--- |\n| FCFS/FIFO | Premier arrivé, premier servi | Simple | Effet convoi |\n| SJF | Plus court d'abord | Optimal (temps moyen) | Famine possible |\n| Round Robin | Quantum de temps tournant | Équitable | Overhead de contexte |\n| Priorité | Par niveau de priorité | Flexible | Famine des basses priorités |\n\n**Quantum de temps (Round Robin) :**\n- Trop petit → trop de changements de contexte\n- Trop grand → se comporte comme FCFS\n\n⚠️ *Piège exam : SJF optimal en théorie, inapplicable en pratique (on ne connaît pas la durée future).*"
    ]
  },
  {
    "regex": "\\b(securite|cybersecurite|hacking|pentest|xss|sql.?injection|csrf|chiffrement|cryptographie|hash|sha|md5|aes)\\b",
    "priority": 2,
    "responses": [
      "🛡️ **Cybersécurité — Fondamentaux** :\n\n**Vulnérabilités OWASP Top 10 (les plus critiques) :**\n1. **Injection SQL** : `' OR 1=1 --` dans un champ → accès BD non autorisé\n2. **XSS** (Cross-Site Scripting) : injection de JS dans une page\n3. **CSRF** : forcer un utilisateur authentifié à effectuer une action\n4. **IDOR** : accéder aux ressources d'autres utilisateurs par ID\n5. **Mauvaise configuration** : ports ouverts, credentials par défaut\n\n**Chiffrement :**\n| Type | Exemple | Usage |\n| :--- | :--- | :--- |\n| Symétrique | AES-256 | Chiffrement de données |\n| Asymétrique | RSA, ECC | Échange de clés, signatures |\n| Hash (unidirectionnel) | SHA-256, bcrypt | Mots de passe |\n\n⚠️ **Rappel légal & éthique :** N'utilisez ces connaissances que sur des systèmes dont vous avez l'autorisation explicite. 🔒\n\n*Accédez au module **DevSecurity** d'Asta Académie pour aller plus loin !*"
    ]
  },
  {
    "regex": "\\b(git|github|gitlab|commit|branch|merge|rebase|pull.?request|version.?control|depot|repository)\\b",
    "priority": 1,
    "responses": [
      "🔀 **Git — Commandes Essentielles** :\n\n```bash\n# Initialiser / Cloner\ngit init              # nouveau dépôt\ngit clone <url>       # cloner un dépôt\n\n# Cycle de travail quotidien\ngit status            # état des fichiers\ngit add .             # indexer tous les changements\ngit commit -m 'msg'   # créer un commit\ngit push origin main  # envoyer vers GitHub\ngit pull              # récupérer les changements\n\n# Branches\ngit branch feature-x      # créer une branche\ngit checkout feature-x    # basculer dessus\ngit merge feature-x       # fusionner dans main\ngit branch -d feature-x   # supprimer la branche\n```\n\n**Flux Git recommandé (GitFlow) :**\n`main` (prod) ← `develop` ← `feature/xxx`\n\n💡 *Règle d'or : commitez souvent, avec des messages descriptifs !*\n`feat: ajouter quiz multi-tentatives` ← Bon commit 👍"
    ]
  },
  {
    "regex": "\\b(dijkstra|plus court chemin|shortest.?path|bellman.?ford|algorithme de graphe|bfs|dfs|breadth|depth)\\b",
    "priority": 1,
    "responses": [
      "🗺️ **Algorithmes de Graphe** :\n\n**BFS (Breadth-First Search — Largeur d'abord) :**\n- Explore niveau par niveau\n- Trouve le plus court chemin en nombre d'arêtes\n- Complexité : O(V + E)\n\n**DFS (Depth-First Search — Profondeur d'abord) :**\n- Explore le plus loin possible avant de revenir\n- Utilisé pour : cycles, chemins, topological sort\n- Complexité : O(V + E)\n\n**Dijkstra (plus court chemin pondéré) :**\n- Fonctionne avec des arêtes à **poids positifs**\n- Complexité : O((V + E) log V) avec tas min\n- Usage : GPS, routage réseau\n\n**Bellman-Ford :**\n- Supporte les **poids négatifs**\n- Détecte les cycles négatifs\n- Complexité : O(V × E)\n\n⚠️ *Dijkstra échoue avec des arêtes négatives → utilisez Bellman-Ford.*"
    ]
  },
  {
    "regex": "\\b(binaire|hexadecimal|hexa|octal|base 2|base 16|bit|octet|byte|conversion numerique)\\b",
    "priority": 1,
    "responses": [
      "🔢 **Systèmes de Numération** :\n\n| Base | Nom | Chiffres | Préfixe Python |\n| :---: | :--- | :--- | :--- |\n| 2 | Binaire | 0,1 | `0b` |\n| 8 | Octal | 0-7 | `0o` |\n| 10 | Décimal | 0-9 | *(aucun)* |\n| 16 | Hexadécimal | 0-9, A-F | `0x` |\n\n**Conversions rapides en Python :**\n```python\nbin(42)    # '0b101010'  → décimal vers binaire\nhex(255)   # '0xff'      → décimal vers hexa\nint('ff', 16)  # 255    → hexa vers décimal\nint('101', 2)  # 5     → binaire vers décimal\n```\n\n**Mémo : 1 octet = 8 bits**\n- `0xFF` = `11111111₂` = `255₁₀`\n- Plage d'un octet signé : -128 à 127\n- Plage d'un octet non signé : 0 à 255\n\n💡 *L'hexadécimal est omniprésent : couleurs CSS `#FF5733`, adresses mémoire, IPv6...*"
    ]
  },
  {
    "regex": "\\b(design.?pattern|patron de conception|singleton|factory|observer|mvc|mvvm|mvc pattern|strategy|decorator pattern)\\b",
    "priority": 1,
    "responses": [
      "🏗️ **Design Patterns (Patrons de Conception)** :\n\nSolutions réutilisables à des problèmes courants en conception logicielle.\n\n**Catégories (GoF - Gang of Four) :**\n\n**Créationnels :**\n- **Singleton** : Une seule instance de la classe\n  ```python\n  class Config:\n      _instance = None\n      def __new__(cls):\n          if not cls._instance:\n              cls._instance = super().__new__(cls)\n          return cls._instance\n  ```\n- **Factory** : Déléguer la création d'objets\n\n**Structurels :**\n- **Facade** : Interface simple sur un système complexe (comme cet AiEngine !)\n- **Decorator** : Ajouter des responsabilités dynamiquement\n\n**Comportementaux :**\n- **Observer** : Notifier des abonnés quand un état change\n- **Strategy** : Interchanger des algorithmes à l'exécution\n\n💡 *MVC (Modèle-Vue-Contrôleur) est le pattern de base de Django, Flask, Rails...*"
    ]
  },
  {
    "regex": "\\b(machine learning|apprentissage machine|ia|intelligence artificielle|deep learning|reseau de neurones|neural network|regression|classification|clustering)\\b",
    "priority": 1,
    "responses": [
      "🤖 **Machine Learning — Introduction** :\n\nLe ML permet aux machines d'**apprendre à partir de données** sans être explicitement programmées.\n\n**3 types d'apprentissage :**\n1. **Supervisé** : données étiquetées → apprendre à prédire\n   - Régression (valeur continue), Classification (catégorie)\n   - Algos : Régression linéaire, SVM, Forêt aléatoire\n\n2. **Non supervisé** : données sans étiquettes → trouver des structures\n   - Clustering (K-means), Réduction de dimension (PCA)\n\n3. **Par renforcement** : agent + récompenses → optimiser une stratégie\n   - Usage : jeux (AlphaGo), robots, trading\n\n**Stack ML Python :**\n- `scikit-learn` : ML classique\n- `TensorFlow` / `PyTorch` : Deep Learning\n- `pandas` + `numpy` : manipulation de données\n- `matplotlib` / `seaborn` : visualisation\n\n💡 *L'IA qui vous répond est construite sur ces mêmes fondements !*"
    ]
  },
  {
    "regex": "\\b(cloud|aws|azure|gcp|google cloud|iaas|paas|saas|serverless|docker|container|kubernetes)\\b",
    "priority": 1,
    "responses": [
      "☁️ **Cloud Computing** :\n\n**Modèles de service :**\n| Modèle | Vous gérez | Fournisseur gère | Exemple |\n| :--- | :--- | :--- | :--- |\n| IaaS | OS, applis | Hardware, réseau | AWS EC2, Azure VM |\n| PaaS | Applis, données | OS, runtime | Heroku, Google App Engine |\n| SaaS | Rien | Tout | Gmail, Office 365 |\n\n**Docker — Conteneurisation :**\n```dockerfile\n# Exemple de Dockerfile Python\nFROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ['python', 'main.py']\n```\n\n**Avantages du cloud :**\n- Scalabilité à la demande\n- Paiement à l'usage\n- Haute disponibilité\n- Pas de matériel à gérer\n\n💡 *Les 3 grands : AWS (leader), Azure (Microsoft), GCP (Google).*"
    ]
  },
  {
    "regex": "\\b(carriere|metier|emploi|job|salaire|developpeur|ingenieur|devops|data.?scientist|fullstack|frontend|backend|recruteur)\\b",
    "priority": 1,
    "responses": [
      "💼 **Carrières en Informatique — Guide Étudiant UNASMOH** :\n\n**Profils très demandés en 2024-2025 :**\n| Métier | Salaire moyen (monde) | Stack typique |\n| :--- | :--- | :--- |\n| Dev Full Stack | 70-120k$/an | React, Node.js, Python |\n| Data Scientist | 80-140k$/an | Python, SQL, ML, Power BI |\n| DevOps / SRE | 90-150k$/an | Docker, K8s, CI/CD, Linux |\n| Cybersécurité | 85-160k$/an | Pentest, SIEM, réseau |\n| Dev Mobile | 70-120k$/an | Flutter, React Native, Swift |\n\n**Votre roadmap depuis l'UNASMOH :**\n1. ✅ Maîtriser les fondamentaux (algorithmes, BDD, réseaux)\n2. 📂 Construire un **portfolio GitHub** avec 3-5 projets concrets\n3. 🏅 Certifications : Google, AWS, Microsoft (accessibles gratuitement en ligne)\n4. 🤝 Réseautage : LinkedIn, hackathons, meetups tech\n5. 💼 Stage dès la L2 — l'expérience terrain est irremplaçable\n\n💡 *Asta Académie vous prépare aux bases. Le reste, c'est vous qui le construisez !*"
    ]
  },
  {
    "regex": "\\b(examen|exam|controle|partiel|epreuve|revision|reviser|note d.examen|ds|bac)\\b",
    "priority": 1,
    "responses": [
      "📝 **Stratégie de Préparation aux Examens** :\n\n**La semaine avant :**\n- 📋 Listez **tous les chapitres** et notez ceux maîtrisés vs à revoir\n- 🎯 Priorité aux chapitres les **plus représentés** dans les anciens sujets\n- 🧠 **Active Recall** : testez-vous avec les quiz d'Asta Académie !\n\n**La veille de l'examen :**\n- ✅ Revoyez uniquement les **points clés** (pas de nouvelle matière)\n- 😴 Dormez **au moins 7-8h** — le sommeil consolide la mémoire\n- 🚫 Évitez la caféine excessive (anxiété) et les réseaux sociaux\n\n**Pendant l'examen :**\n- 📖 Lisez **tout le sujet** avant de commencer\n- ⏱️ Allouez du temps par question selon les points\n- 💡 Si vous bloquez : passez et revenez plus tard\n- ✍️ Rédigez même partiellement — des points partiels valent mieux que rien\n\n*Vous avez travaillé dur. Faites confiance à votre préparation ! 💪*"
    ]
  },
  {
    "regex": "\\b(ada lovelace|grace hopper|dennis ritchie|linus torvalds|richard stallman|ken thompson|donald knuth|edsger dijkstra|tim berners.?lee|john mccarthy)\\b",
    "priority": 1,
    "responses": [
      "📜 **Grandes Figures de l'Informatique** :\n\n| Nom | Contribution majeure |\n| :--- | :--- |\n| **Ada Lovelace** | 1er algorithme pour machine (1843), pionnière de la programmation |\n| **Alan Turing** | Machine de Turing, déchiffrage Enigma, test de Turing |\n| **Grace Hopper** | 1er compilateur (1952), COBOL, concept de 'bug' |\n| **Dennis Ritchie** | Créateur du langage C et co-créateur d'Unix |\n| **Linus Torvalds** | Créateur du noyau Linux (1991) |\n| **Tim Berners-Lee** | Inventeur du World Wide Web (1989) |\n| **Donald Knuth** | *The Art of Computer Programming*, TeX, analyse d'algorithmes |\n| **Edsger Dijkstra** | Algorithme de plus court chemin, sémaphores, Goto harmful |\n| **John McCarthy** | Terme 'Intelligence Artificielle', LISP |\n\n*Ces géants ont posé les fondations sur lesquelles vous construisez votre avenir !* 🙌"
    ]
  },
  {
    "regex": "\\b(cours disponibles?|liste des cours|quels cours|matieres? disponibles?|que peux.?tu enseigner|qu.est.ce que tu connais)\\b",
    "priority": 1,
    "responses": [
      "📚 **Matières disponibles dans la base de connaissances d'Asta** :\n\n🔷 **Informatique Fondamentale**\n- Architecture des ordinateurs (Von Neumann, CPU, RAM, bus)\n- Algorithmique et structures de données\n- Systèmes d'exploitation (processus, mémoire, scheduling)\n\n🔷 **Programmation**\n- Python, C, Java — notions et bonnes pratiques\n- POO (Classes, héritage, polymorphisme)\n- HTML/CSS pour le Web\n\n🔷 **Réseaux & Sécurité**\n- Modèle OSI, TCP/IP, DNS, HTTP\n- Cybersécurité éthique (via module DevSecurity)\n\n🔷 **Bases de Données**\n- SQL, jointures, normalisation, ACID\n\n💡 *Posez une question précise sur l'un de ces sujets et je vous répondrai en détail !*\n*Tapez aussi **'quiz'** pour être testé sur la dernière leçon consultée.*"
    ]
  },
  {
    "regex": "\\b(merci|bravo|super|excellent|bien|parfait|genial|incroyable|top|chapeau|thanks|thank you)\\b",
    "priority": 1,
    "responses": [
      "😊 Avec plaisir ! C'est pour ça que je suis là.\n\n*N'hésitez pas à me poser d'autres questions de cours ou à lancer un **quiz** pour gagner des points !*",
      "🙏 Merci à vous ! Votre curiosité est le moteur de votre réussite.\n\n*Continuez à explorer — tapez le nom d'un sujet ou **'cours'** pour les matières disponibles.*",
      "✨ C'est un plaisir d'apprendre ensemble ! Tapez **'stats'** pour voir votre progression. 📊"
    ]
  },
  {
    "regex": "\\b(nul|idiot|stupide|imbecile|bete|mauvais|horrible|useless|worthless)\\b",
    "priority": 5,
    "responses": [
      "😊 Je comprends votre frustration ! Je fais de mon mieux pour vous aider.\n\nSi ma réponse n'était pas celle attendue, reformulez votre question avec des mots-clés plus précis (ex: 'algorithme de tri', 'protocole TCP', 'héritage Python').\n\n*Je suis là pour vous aider à réussir !* 💪"
    ]
  },
  {
    "regex": "\\b(au revoir|bye|goodbye|a bientot|ciao|bonne soiree|bonne nuit|bonne journee)\\b",
    "priority": 1,
    "responses": [
      "👋 À bientôt ! Continuez à réviser — chaque leçon vous rapproche de votre diplôme ! 🎓\n\n*Pensez à utiliser le quiz et à suivre votre streak de connexion dans Asta Académie !*",
      "🌟 Bonne continuation ! N'oubliez pas votre session d'étude de demain.\n\n*Votre progression est sauvegardée. À bientôt !*"
    ]
  },
  {
    "regex": "\\b(asta|createur|space.?dev|lucky.?luke|unasmoh|promotion 2024|qui t.a cree|qui es.?tu|c.est quoi asta)\\b",
    "priority": 1,
    "responses": [
      "🚀 **À propos d'Asta Académie & Space AI** :\n\nJe suis **Asta AI**, le moteur d'intelligence artificielle d'**Asta Académie**.\n\n- **Développeur :** Space Dev *(Lucky Luke)*, Ingénieur en Informatique, Promotion 2024-2028\n- **Université :** UNASMOH — Université Américaine des Sciences Modernes d'Haïti\n- **Mission :** Aider les étudiants de la promotion 2024-2028 à exceller en informatique\n\n**Ce que je peux faire pour vous :**\n- 📚 Répondre à vos questions de cours\n- 🧩 Lancer des quiz interactifs (et vous récompenser en points !)\n- 🔢 Faire des calculs\n- 🧭 Naviguer dans l'application\n- 💪 Vous motiver quand c'est difficile\n\n*Ensemble, vers l'excellence !* 🎓"
    ]
  },
  {
    "regex": "\\b(html|css|javascript|js|dom|balise|tag html|flexbox|grid|responsive|bootstrap)\\b",
    "priority": 1,
    "responses": [
      "🌐 **Développement Web Front-End** :\n\nLa sainte trinité du Web :\n| Technologie | Rôle | Analogie |\n| :--- | :--- | :--- |\n| HTML | Structure / Squelette | L'ossature d'une maison |\n| CSS | Style / Apparence | La peinture et décoration |\n| JavaScript | Comportement / Interaction | L'électricité et les automatismes |\n\nHTML5 — Structure de base :\n```html\n<!DOCTYPE html>\n<html lang='fr'>\n<head>\n  <meta charset='UTF-8'>\n  <title>Ma Page</title>\n  <link rel='stylesheet' href='style.css'>\n</head>\n<body>\n  <h1>Bonjour UNASMOH !</h1>\n  <script src='app.js'></script>\n</body>\n</html>\n```\n\nCSS Flexbox (essentiel) :\n```css\n.container {\n  display: flex;\n  justify-content: center; /* axe horizontal */\n  align-items: center;    /* axe vertical */\n  gap: 16px;\n}\n```\n\n💡 Testez votre HTML/CSS dans SpaceCode (onglet Outils) !"
    ]
  },
  {
    "regex": "\\b(pointeur|pointer|adresse memoire|reference|malloc|free|null pointer|segfault|segmentation)\\b",
    "priority": 1,
    "responses": [
      "🎯 Les Pointeurs (C / C++) :\n\nUn pointeur est une variable qui stocke une adresse mémoire.\n\n```c\nint x = 42;\nint *p = &x;  // p pointe vers l'adresse de x\n\nprintf('%d', x);   // 42  → valeur\nprintf('%p', p);   // 0x7ffd... → adresse\nprintf('%d', *p);  // 42  → déréférencement\n\n*p = 100;  // modifie x via le pointeur\nprintf('%d', x);  // 100\n```\n\n**Allocation dynamique :**\n```c\nint *arr = malloc(10 * sizeof(int));  // allouer\nif (arr == NULL) { / gestion erreur / }\narr[0] = 1;\nfree(arr);  // OBLIGATOIRE → sinon memory leak !\narr = NULL; // bonne pratique : nullifier après free\n```\n\n⚠️ **Erreurs classiques :**\n- **Déréférencer NULL** → Segmentation fault (crash)\n- **Use after free** → comportement indéfini (UB)\n- **Memory leak** → oublier `free()` sur un `malloc()`\n\n💡 *En Python, vous n'avez pas à gérer les pointeurs — le GC s'en charge !"
    ]
  },
  {
    "regex": "\\b(projet Asta | projet AstaAcademie | Team Asta Academie | Jephtalie | Tekno | Tecno | Samuel | Samenda)\\b",
    "priority": 1,
    "responses": [
      "C'est quoi le projet Asta Academie ? \n\nAsta Academie c'est une idée de Lucky Luke (Space ou SpaceZyy) crée avec comme langage de programation (PYTHON) \npour aider les etudiants en informatique.\n\nStaff de Asta Academie :\n\nL'etudiante Jephthalie, son rôle :\n conseillère en stratégie & Expérience\n\n Mission principale :\n\n évaluer les fonctionnalités existantes pour identifier les points de friction ou les manques.\n\nElle propose des nouveaux contenus ou modules à intégrer pour enrichir l'expérience des étudiants.\n\nElle assure que l'interface et les services répondent aux besoins réels des utilisateurs.\n\n L'etudiant Space (Créateur du projet), son rôle: \n il veille que l'application répondent aux demande des utilisateurs. \n il a coder le projet en langage Python et a mis des tecnologies comme un chat bot intelligent (moi Asta AI),\nil a ajouter des technologie de dll,\nil a mis une terminal intégré dans l'application et bien plus encore\nSpace aime relever des défis et il veut créer une application ou l'etudiant peut vibe coder, apprendre l'informatique et des langages de programmation.\nSpace est ouvert à toutes les idée pour m'ameliorer et ameliorer Asta Academie.\n"
    ]
  },
  {
    "regex": "\\b(qu'est ce que python|c'est quoi python|python c'est|présente python|définition python|python définition | definition python | python definition | kisa python an ye | presente python | python)\\b",
    "priority": 2,
    "responses": [
      "Difficulté : facile\n\n---\n\n# Qu'est-ce que Python ?\n\nPython est un langage de programmation interprété, de haut niveau, moderne et polyvalent créé par Guido van Rossum et publié officiellement en 1991.\n\nLe nom 'Python' provient de l'émission humoristique britannique *Monty Python's Flying Circus* et non du serpent.\n\nPython a été conçu avec un objectif principal :\n\n> rendre la programmation plus simple, plus lisible et plus productive.\n\nAujourd'hui, Python est considéré comme l'un des langages les plus populaires au monde grâce à :\n- sa simplicité,\n- sa puissance,\n- sa lisibilité,\n- sa flexibilité,\n- son immense communauté.\n\nPython est utilisé aussi bien par :\n- les débutants,\n- les étudiants,\n- les développeurs professionnels,\n- les chercheurs,\n- les ingénieurs,\n- les experts en cybersécurité,\n- les entreprises technologiques.\n\nDes entreprises comme :\n- Google,\n- Netflix,\n- Instagram,\n- Spotify,\n- NASA,\n- YouTube,\n- OpenAI,\nutilisent Python dans leurs infrastructures.\n\n---\n\n# Points clés\n\n- Langage interprété (pas de compilation)\n- Créé en 1991 par Guido van Rossum\n- Nom inspiré des Monty Python\n- Très populaire dans les grandes entreprises tech\n\n---\n\n# Exercice\n\n## Énoncé\n\nQui a créé Python et en quelle année ?\n\n<details>\n<summary>Voir la Correction</summary>\n\n✅ Python a été créé par **Guido van Rossum** et publié officiellement en **1991**.\n\n</details>"
    ]
  },
  {
    "regex": "\\b(histoire python|création python|guido van rossum|évolution python|python 1|python 2|python 3|van rossum | histoire de python | donnne l'histoire de python | explique l'histoire de python | ban histwa python)\\b",
    "priority": 2,
    "responses": [
      "# INTRODUCTION PYTHON — HISTOIRE DE PYTHON\nDifficulté : ★★★★★★★★☆☆\n\n---\n\n# Histoire de Python\n\n## Création du langage\n\nPython a été créé à la fin des années 1980 par Guido van Rossum au CWI (Centre for Mathematics and Computer Science) aux Pays-Bas.\n\nGuido voulait créer un langage :\n- simple,\n- clair,\n- lisible,\n- puissant,\n- facile à apprendre,\n- mais capable de gérer de gros projets.\n\n---\n\n# Évolution de Python\n\n## Python 1.0\nPremière version officielle publiée en 1991.\n\n## Python 2.x\nVersion extrêmement populaire pendant de nombreuses années.\n\n## Python 3.x\nVersion moderne actuelle.\nElle améliore :\n- les performances,\n- la cohérence,\n- la sécurité,\n- la gestion Unicode.\n\nPython 2 est aujourd'hui abandonné.\n\n---\n\n# Points clés\n\n- Création : fin des années 1980 au CWI (Pays-Bas)\n- Python 1.0 : 1991\n- Python 2.x : très populaire mais abandonné\n- Python 3.x : version actuelle à utiliser\n- Guido van Rossum est le 'Benevolent Dictator for Life' (BDFL) honoraire\n\n---\n\n# Exercice\n\n## Énoncé\n\nQuelle version de Python est recommandée aujourd'hui et laquelle est abandonnée ?\n\n<details>\n<summary>Voir la Correction</summary>\n\n✅ Python 3.x est la version recommandée. Python 2.x est abandonné.\n\n</details>"
    ]
  },
  {
    "regex": "\\b(philosophie python|zen of python|zen python|principe python|python philosophie | phylosophie de python | principe de python)\\b",
    "priority": 2,
    "responses": [
      "# INTRODUCTION PYTHON — PHILOSOPHIE (ZEN OF PYTHON)\n\nDifficulté : ★★★★★★★☆☆☆\n\n---\n\n# Philosophie de Python\n\nPython suit une philosophie appelée :\n\n## 'The Zen of Python'\n\nQuelques principes célèbres :\n\n- Beautiful is better than ugly.\n- Simple is better than complex.\n- Readability counts.\n- Explicit is better than implicit.\n\nEn français :\n- Le beau est meilleur que le laid.\n- Le simple est meilleur que le complexe.\n- La lisibilité est importante.\n- L'explicite est préférable à l'implicite.\n\nCette philosophie explique pourquoi le code Python est souvent très propre et facile à comprendre.\n\n---\n\n# Autres principes du Zen of Python\n\n- Complex is better than complicated.\n- Flat is better than nested.\n- Sparse is better than dense.\n- Errors should never pass silently.\n- In the face of ambiguity, refuse the temptation to guess.\n- There should be one — and preferably only one — obvious way to do it.\n\n---\n\n# Points clés\n\n- La lisibilité est primordiale en Python\n- Le code doit être simple et explicite\n- Le Zen of Python contient 19 aphorismes\n- Tapez `import this` dans un terminal Python pour voir le Zen complet\n\n---\n\n# Exercice\n\n## Énoncé\n\nQuelle commande Python permet d'afficher le Zen of Python ?\n\n<details>\n<summary>Voir la Correction</summary>\n\n✅ `import this`\n\n```python\nimport this\n# Affiche tous les principes du Zen of Python\n```\n\n</details>"
    ]
  },
  {
    "regex": "\\b(histoire complete python|histoire python detail|évolution python|python 0.9|python 1.0|python 2.0|python 3.0|chronologie python)\\b",
    "priority": 2,
    "responses": [
      "# INTRODUCTION PYTHON — HISTOIRE COMPLÈTE DE PYTHON\n\nDifficulté : ★★★★★★★☆☆☆\n\n---\n\n# Introduction\n\nPython est aujourd'hui l'un des langages de programmation les plus populaires au monde. Utilisé dans :\n- l'intelligence artificielle,\n- le développement web,\n- la cybersécurité,\n- la data science,\n- l'automatisation,\n- les infrastructures cloud,\n- les applications desktop.\n\nPython a parcouru un immense chemin depuis sa création à la fin des années 1980.\n\n---\n\n# Les Origines de Python\n\n## La fin des années 1980\n\nÀ la fin des années 1980, le développement logiciel devenait de plus en plus complexe.\n\nLes langages populaires de l'époque comme :\n- C,\n- C++,\n- Pascal,\n- Perl,\n\nétaient puissants, mais souvent difficiles à lire et à maintenir.\n\n---\n\n# Le Créateur : Guido van Rossum\n\nPython a été créé par Guido van Rossum, un développeur néerlandais travaillant au :\n- CWI (Centrum Wiskunde & Informatica),\n- le Centre de Mathématiques et d'Informatique des Pays-Bas.\n\nGuido travaillait sur un projet appelé :\n- ABC Programming Language.\n\nABC était un langage conçu pour être simple et éducatif, mais il possédait plusieurs limitations.\n\n---\n\n# La Naissance de Python\n\n## 1989 : Début du projet\n\nPendant les vacances de Noël 1989, Guido van Rossum commence à travailler sur un nouveau langage de programmation.\n\nSes objectifs :\n- syntaxe claire,\n- lisibilité maximale,\n- simplicité,\n- productivité élevée,\n- développement rapide.\n\n---\n\n# Pourquoi le nom 'Python' ?\n\nContrairement à ce que beaucoup pensent, le nom Python ne vient pas du serpent.\n\nLe nom vient de l'émission humoristique britannique :\n\n```text\nMonty Python's Flying Circus\n```\n\nGuido van Rossum était fan de cette émission et voulait un nom :\n- court,\n- unique,\n- mystérieux,\n- facile à retenir.\n\n---\n\n# Première Version de Python\n\n## Python 0.9.0 — 1991\n\nLa première version publique de Python sort en février 1991.\n\nElle contenait déjà :\n- les fonctions,\n- les exceptions,\n- les classes,\n- les modules,\n- les listes,\n- les dictionnaires.\n\n---\n\n# Python 1.0\n\n## Sortie officielle : 1994\n\nPython 1.0 introduit :\n- la programmation fonctionnelle,\n- lambda,\n- map(),\n- filter(),\n- reduce().\n\n---\n\n# Python Software Foundation\n\n## Création en 2001\n\nLa Python Software Foundation (PSF) est créée pour :\n- protéger Python,\n- financer le développement,\n- soutenir la communauté,\n- organiser les évolutions du langage.\n\n---\n\n# Python 2.0\n\n## Sortie : 2000\n\nPython 2.0 apporte :\n- le garbage collector,\n- les list comprehensions,\n- de meilleures performances,\n- une meilleure gestion mémoire.\n\n---\n\n# Python 3.0 : La Grande Révolution\n\n## Sortie : 2008\n\nPython 3 est une refonte majeure du langage.\n\nObjectif :\n- corriger les erreurs historiques,\n- moderniser Python,\n- rendre le langage plus cohérent.\n\n---\n\n# Changements importants de Python 3\n\n## print devient une fonction\n\nAvant :\n```python\nprint 'Bonjour'\n```\n\nAprès :\n```python\nprint('Bonjour')\n```\n\n## Meilleure gestion Unicode\n\nPython 3 améliore énormément :\n- les caractères spéciaux,\n- les langues internationales,\n- l'encodage.\n\n---\n\n# Fin de Python 2\n\n## 1er janvier 2020\n\nLe support officiel de Python 2 prend fin.\n\nAujourd'hui :\n- Python 2 est obsolète,\n- Python 3 est la norme mondiale.\n\n---\n\n# Chronologie Rapide\n\n| Année | Événement |\n| :--- | :--- |\n| 1989 | Début du projet Python |\n| 1991 | Python 0.9.0 |\n| 1994 | Python 1.0 |\n| 2000 | Python 2.0 |\n| 2001 | Création de la PSF |\n| 2008 | Python 3.0 |\n| 2020 | Fin officielle de Python 2 |\n\n---\n\n# Points Clés\n\n- Python a été créé par Guido van Rossum\n- Début du projet en 1989\n- Première version publique en 1991\n- Inspiré du langage ABC\n- Le nom vient de Monty Python\n- Python privilégie la lisibilité\n- Python est open source\n- Python 3 est la version moderne\n- Python domine aujourd'hui l'IA et la data science\n\n---\n\n# Exercice\n\n## Énoncé\n\nQui a créé Python et en quelle année la première version publique est-elle sortie ?\n\n<details>\n<summary>Voir la Correction</summary>\n\n✅ Python a été créé par Guido van Rossum.\n\n✅ La première version publique est sortie en 1991.\n\n</details>"
    ]
  }
];
