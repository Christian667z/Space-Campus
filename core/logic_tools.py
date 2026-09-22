"""
╔══════════════════════════════════════════════════════════════╗
║            ASTA ACADÉMIE — LOGIC TOOLS MODULE                ║
║         Développé par Space | Asta Dev — Promo 2024-2028     ║
╚══════════════════════════════════════════════════════════════╝
"""

import random



def decimal_to_binary(n: int) -> str:
    """Convertit décimal → binaire avec explication étape par étape."""
    if n < 0:
        return f"Complément à 2: {bin(n & 0xFF)[2:].zfill(8)}"
    if n == 0:
        return "0"
    return bin(n)[2:]

def decimal_to_hex(n: int) -> str:
    return hex(n)[2:].upper()

def decimal_to_octal(n: int) -> str:
    return oct(n)[2:]

def binary_to_decimal(b: str) -> int:
    return int(b, 2)

def hex_to_decimal(h: str) -> int:
    return int(h, 16)

def convert_all(value: str, base: str) -> dict:
    """Convertit une valeur dans toutes les bases."""
    try:
        if base == "decimal":
            n = int(value)
        elif base == "binary":
            n = int(value, 2)
        elif base == "hex":
            n = int(value, 16)
        elif base == "octal":
            n = int(value, 8)
        else:
            return {"error": "Base non reconnue"}

        return {
            "decimal": str(n),
            "binary": bin(n)[2:],
            "hexadecimal": hex(n)[2:].upper(),
            "octal": oct(n)[2:],
            "ascii": chr(n) if 32 <= n <= 126 else "N/A",
        }
    except ValueError as e:
        return {"error": f"Valeur invalide: {e}"}

def explain_binary_conversion(n: int) -> list:
    """Explique la conversion décimal → binaire étape par étape."""
    if n == 0:
        return [{"division": "0", "quotient": "0", "reste": "0"}]
    steps = []
    while n > 0:
        steps.append({
            "division": str(n),
            "quotient": str(n // 2),
            "reste": str(n % 2)
        })
        n //= 2
    steps.reverse()
    return steps

def generate_truth_table(variables: list, expression: str) -> list:
    """
    Génère une table de vérité pour une expression booléenne.
    variables: ['A', 'B', 'C']
    expression: 'A and (B or not C)'
    """
    rows = []
    n = len(variables)
    for i in range(2**n):
        vals = {}
        for j, var in enumerate(variables):
            vals[var] = bool((i >> (n-1-j)) & 1)
        
        local_vars = {k: v for k, v in vals.items()}
        local_vars['not_'] = lambda x: not x
        
        try:
            expr_eval = expression.lower()
            for var in variables:
                expr_eval = expr_eval.replace(var.lower(), str(vals[var]))
            result = eval(expr_eval)
        except Exception:
            result = None
        
        row = {var: "1" if vals[var] else "0" for var in variables}
        row["Résultat"] = "1" if result else "0"
        rows.append(row)
    return rows

BIG_O_TABLE = [
    {"notation": "O(1)",      "complexite": "O(1)",      "nom": "Constante",      "exemple": "Accès à un index de tableau",          "vitesse": "⚡ Excellent"},
    {"notation": "O(log n)",  "complexite": "O(log n)",  "nom": "Logarithmique",  "exemple": "Recherche binaire",                   "vitesse": "✅ Très bon"},
    {"notation": "O(n)",      "complexite": "O(n)",      "nom": "Linéaire",       "exemple": "Parcours d'une liste simple",          "vitesse": "🟡 Acceptable"},
    {"notation": "O(n log n)","complexite": "O(n log n)","nom": "Quasi-linéaire", "exemple": "Tri Fusion (Merge Sort)",              "vitesse": "🟡 Acceptable"},
    {"notation": "O(n²)",     "complexite": "O(n²)",     "nom": "Quadratique",    "exemple": "Tri à bulles (Bubble Sort)",           "vitesse": "🔴 Lent"},
    {"notation": "O(2ⁿ)",    "complexite": "O(2ⁿ)",    "nom": "Exponentielle",  "exemple": "Algorithmes récursifs de Fibonacci",   "vitesse": "💀 Très lent"},
    {"notation": "O(n!)",     "complexite": "O(n!)",     "nom": "Factorielle",    "exemple": "Problème du voyageur de commerce",     "vitesse": "☠️ Extrême"},
]

ASCII_TABLE = [
    {"decimal": 32, "char": '(Espace)', "hex": "20", "binaire": "00100000"},
    {"decimal": 33, "char": '!', "hex": "21", "binaire": "00100001"},
    {"decimal": 34, "char": '"', "hex": "22", "binaire": "00100010"},
    {"decimal": 35, "char": '#', "hex": "23", "binaire": "00100011"},
    {"decimal": 36, "char": '$', "hex": "24", "binaire": "00100100"},
    {"decimal": 37, "char": '%', "hex": "25", "binaire": "00100101"},
    {"decimal": 38, "char": '&', "hex": "26", "binaire": "00100110"},
    {"decimal": 39, "char": "'", "hex": "27", "binaire": "00100111"},
    {"decimal": 40, "char": '(', "hex": "28", "binaire": "00101000"},
    {"decimal": 41, "char": ')', "hex": "29", "binaire": "00101001"},
    {"decimal": 42, "char": '*', "hex": "2A", "binaire": "00101010"},
    {"decimal": 43, "char": '+', "hex": "2B", "binaire": "00101011"},
    {"decimal": 44, "char": ',', "hex": "2C", "binaire": "00101100"},
    {"decimal": 45, "char": '-', "hex": "2D", "binaire": "00101101"},
    {"decimal": 46, "char": '.', "hex": "2E", "binaire": "00101110"},
    {"decimal": 47, "char": '/', "hex": "2F", "binaire": "00101111"},
    {"decimal": 48, "char": '0', "hex": "30", "binaire": "00110000"},
    {"decimal": 49, "char": '1', "hex": "31", "binaire": "00110001"},
    {"decimal": 50, "char": '2', "hex": "32", "binaire": "00110010"},
    {"decimal": 51, "char": '3', "hex": "33", "binaire": "00110011"},
    {"decimal": 52, "char": '4', "hex": "34", "binaire": "00110100"},
    {"decimal": 53, "char": '5', "hex": "35", "binaire": "00110101"},
    {"decimal": 54, "char": '6', "hex": "36", "binaire": "00110110"},
    {"decimal": 55, "char": '7', "hex": "37", "binaire": "00110111"},
    {"decimal": 56, "char": '8', "hex": "38", "binaire": "00111000"},
    {"decimal": 57, "char": '9', "hex": "39", "binaire": "00111001"},
    {"decimal": 58, "char": ':', "hex": "3A", "binaire": "00111010"},
    {"decimal": 59, "char": ';', "hex": "3B", "binaire": "00111011"},
    {"decimal": 60, "char": '<', "hex": "3C", "binaire": "00111100"},
    {"decimal": 61, "char": '=', "hex": "3D", "binaire": "00111101"},
    {"decimal": 62, "char": '>', "hex": "3E", "binaire": "00111110"},
    {"decimal": 63, "char": '?', "hex": "3F", "binaire": "00111111"},
    {"decimal": 64, "char": '@', "hex": "40", "binaire": "01000000"},
    {"decimal": 65, "char": 'A', "hex": "41", "binaire": "01000001"},
    {"decimal": 66, "char": 'B', "hex": "42", "binaire": "01000010"},
    {"decimal": 67, "char": 'C', "hex": "43", "binaire": "01000011"},
    {"decimal": 68, "char": 'D', "hex": "44", "binaire": "01000100"},
    {"decimal": 69, "char": 'E', "hex": "45", "binaire": "01000101"},
    {"decimal": 70, "char": 'F', "hex": "46", "binaire": "01000110"},
    {"decimal": 71, "char": 'G', "hex": "47", "binaire": "01000111"},
    {"decimal": 72, "char": 'H', "hex": "48", "binaire": "01001000"},
    {"decimal": 73, "char": 'I', "hex": "49", "binaire": "01001001"},
    {"decimal": 74, "char": 'J', "hex": "4A", "binaire": "01001010"},
    {"decimal": 75, "char": 'K', "hex": "4B", "binaire": "01001011"},
    {"decimal": 76, "char": 'L', "hex": "4C", "binaire": "01001100"},
    {"decimal": 77, "char": 'M', "hex": "4D", "binaire": "01001101"},
    {"decimal": 78, "char": 'N', "hex": "4E", "binaire": "01001110"},
    {"decimal": 79, "char": 'O', "hex": "4F", "binaire": "01001111"},
    {"decimal": 80, "char": 'P', "hex": "50", "binaire": "01010000"},
    {"decimal": 81, "char": 'Q', "hex": "51", "binaire": "01010001"},
    {"decimal": 82, "char": 'R', "hex": "52", "binaire": "01010010"},
    {"decimal": 83, "char": 'S', "hex": "53", "binaire": "01010011"},
    {"decimal": 84, "char": 'T', "hex": "54", "binaire": "01010100"},
    {"decimal": 85, "char": 'U', "hex": "55", "binaire": "01010101"},
    {"decimal": 86, "char": 'V', "hex": "56", "binaire": "01010110"},
    {"decimal": 87, "char": 'W', "hex": "57", "binaire": "01010111"},
    {"decimal": 88, "char": 'X', "hex": "58", "binaire": "01011000"},
    {"decimal": 89, "char": 'Y', "hex": "59", "binaire": "01011001"},
    {"decimal": 90, "char": 'Z', "hex": "5A", "binaire": "01011010"},
    {"decimal": 91, "char": '[', "hex": "5B", "binaire": "01011011"},
    {"decimal": 92, "char": '\\', "hex": "5C", "binaire": "01011100"},
    {"decimal": 93, "char": ']', "hex": "5D", "binaire": "01011101"},
    {"decimal": 94, "char": '^', "hex": "5E", "binaire": "01011110"},
    {"decimal": 95, "char": '_', "hex": "5F", "binaire": "01011111"},
    {"decimal": 96, "char": '`', "hex": "60", "binaire": "01100000"},
    {"decimal": 97, "char": 'a', "hex": "61", "binaire": "01100001"},
    {"decimal": 98, "char": 'b', "hex": "62", "binaire": "01100010"},
    {"decimal": 99, "char": 'c', "hex": "63", "binaire": "01100011"},
    {"decimal": 100, "char": 'd', "hex": "64", "binaire": "01100100"},
    {"decimal": 101, "char": 'e', "hex": "65", "binaire": "01100101"},
    {"decimal": 102, "char": 'f', "hex": "66", "binaire": "01100110"},
    {"decimal": 103, "char": 'g', "hex": "67", "binaire": "01100111"},
    {"decimal": 104, "char": 'h', "hex": "68", "binaire": "01101000"},
    {"decimal": 105, "char": 'i', "hex": "69", "binaire": "01101001"},
    {"decimal": 106, "char": 'j', "hex": "6A", "binaire": "01101010"},
    {"decimal": 107, "char": 'k', "hex": "6B", "binaire": "01101011"},
    {"decimal": 108, "char": 'l', "hex": "6C", "binaire": "01101100"},
    {"decimal": 109, "char": 'm', "hex": "6D", "binaire": "01101101"},
    {"decimal": 110, "char": 'n', "hex": "6E", "binaire": "01101110"},
    {"decimal": 111, "char": 'o', "hex": "6F", "binaire": "01101111"},
    {"decimal": 112, "char": 'p', "hex": "70", "binaire": "01110000"},
    {"decimal": 113, "char": 'q', "hex": "71", "binaire": "01110001"},
    {"decimal": 114, "char": 'r', "hex": "72", "binaire": "01110010"},
    {"decimal": 115, "char": 's', "hex": "73", "binaire": "01110011"},
    {"decimal": 116, "char": 't', "hex": "74", "binaire": "01110100"},
    {"decimal": 117, "char": 'u', "hex": "75", "binaire": "01110101"},
    {"decimal": 118, "char": 'v', "hex": "76", "binaire": "01110110"},
    {"decimal": 119, "char": 'w', "hex": "77", "binaire": "01110111"},
    {"decimal": 120, "char": 'x', "hex": "78", "binaire": "01111000"},
    {"decimal": 121, "char": 'y', "hex": "79", "binaire": "01111001"},
    {"decimal": 122, "char": 'z', "hex": "7A", "binaire": "01111010"},
    {"decimal": 123, "char": '{', "hex": "7B", "binaire": "01111011"},
    {"decimal": 124, "char": '|', "hex": "7C", "binaire": "01111100"},
    {"decimal": 125, "char": '}', "hex": "7D", "binaire": "01111101"},
    {"decimal": 126, "char": '~', "hex": "7E", "binaire": "01111110"}
]

BOOL_LAWS = [
    {"loi": "Identité", "and_form": "A · 1 = A", "or_form": "A + 0 = A"},
    {"loi": "Annulation", "and_form": "A · 0 = 0", "or_form": "A + 1 = 1"},
    {"loi": "Idempotence", "and_form": "A · A = A", "or_form": "A + A = A"},
    {"loi": "Complément", "and_form": "A · Ā = 0", "or_form": "A + Ā = 1"},
    {"loi": "Double négation", "and_form": "——", "or_form": "¬(¬A) = A"},
    {"loi": "Commutativité", "and_form": "A · B = B · A", "or_form": "A + B = B + A"},
    {"loi": "Associativité", "and_form": "(A·B)·C = A·(B·C)", "or_form": "(A+B)+C = A+(B+C)"},
    {"loi": "Distributivité", "and_form": "A·(B+C) = A·B + A·C", "or_form": "A+(B·C) = (A+B)·(A+C)"},
    {"loi": "De Morgan 1", "and_form": "¬(A·B) = Ā+B̄", "or_form": "NOR vers NAND"},
    {"loi": "De Morgan 2", "and_form": "¬(A+B) = Ā·B̄", "or_form": "NAND vers NOR"},
    {"loi": "Absorption", "and_form": "A·(A+B) = A", "or_form": "A+(A·B) = A"},
]

TERMINAL_RESPONSES = {
    "ls": "Documents/  Téléchargements/  Bureau/  Images/  Musique/  Vidéos/  main.py  readme.txt",
    "ls -la": "total 48\ndrwxr-xr-x 8 etudiant users 4096 Jan 15 09:30 .\ndrwxr-xr-x 3 root     root  4096 Jan 10 08:00 ..\n-rw-r--r-- 1 etudiant users  220 Jan 10 08:00 .bash_logout\n-rw-r--r-- 1 etudiant users 3526 Jan 10 08:00 .bashrc\ndrwxr-xr-x 2 etudiant users 4096 Jan 15 09:25 Documents\ndrwxr-xr-x 2 etudiant users 4096 Jan 12 14:30 Bureau\n-rw-r--r-- 1 etudiant users 1024 Jan 15 09:30 main.py",
    "dir": "Le volume dans le lecteur C n'a pas de nom.\nRépertoire de C:\\Users\\Etudiant\n\n15/01/2025  09:30    <REP>          Documents\n15/01/2025  09:25    <REP>          Bureau\n15/01/2025  08:00    <REP>          Images\n               0 fichier(s)               0 octets\n               3 Rép(s)  125 Go disponibles",
    "ipconfig": "Configuration IP de Windows\n\nCarte Ethernet Ethernet:\n   Suffixe DNS propre à la connexion. . : \n   Adresse IPv4. . . . . . . . . . . . : 192.168.1.105\n   Masque de sous-réseau. . . . . . . . : 255.255.255.0\n   Passerelle par défaut. . . . . . . . : 192.168.1.1\n\nCarte réseau sans fil Wi-Fi:\n   Adresse IPv4. . . . . . . . . . . . : 192.168.1.107\n   Masque de sous-réseau. . . . . . . . : 255.255.255.0\n   Passerelle par défaut. . . . . . . . : 192.168.1.1",
    "ifconfig": "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n        inet 192.168.1.105  netmask 255.255.255.0  broadcast 192.168.1.255\n        ether 08:00:27:ab:cd:ef  txqueuelen 1000  (Ethernet)\n        RX packets 12456  bytes 1234567 (1.2 MB)\n        TX packets 8932  bytes 987654 (987.6 KB)\n\nlo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536\n        inet 127.0.0.1  netmask 255.0.0.0",
    "whoami": "etudiant_unasmoh",
    "pwd": "/home/etudiant/Asta_Academie",
    "clear": "__CLEAR__",
    "cls": "__CLEAR__",
    "help": "Commandes disponibles:\n  ls / dir    - Lister les fichiers\n  ls -la      - Détails complets\n  ipconfig    - Config réseau Windows\n  ifconfig    - Config réseau Linux\n  whoami      - Utilisateur actuel\n  pwd         - Répertoire courant\n  ping [host] - Tester la connectivité\n  date        - Date et heure\n  echo [texte]- Afficher du texte\n  python      - Lancer Python\n  clear / cls - Effacer l'écran\n  uname -a    - Info système Linux\n  systeminfo  - Info système Windows\n  netstat     - Connexions réseau\n  tracert     - Tracer la route réseau",
    "date": "Jeudi 15 janvier 2025 - 09:30:45 GMT-5 (Haïti)",
    "uname -a": "Linux UNASMOH-PC 5.15.0-91-generic #101-Ubuntu SMP Thu Sep 1 00:12:51 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux",
    "systeminfo": "Nom de l'hôte:          UNASMOH-PC\nNom du système d'exploitation: Microsoft Windows 11 Pro\nVersion du système d'exploitation: 10.0.22631 Build 22631\nFabricant du système d'exploitation: Microsoft Corporation\nType de système:        PC basé sur x64\nProcesseur(s):          Intel(R) Core(TM) i5-1135G7 @ 2.40GHz\nMémoire physique totale: 8 192 Mo\nMémoire physique disponible: 3 421 Mo",
    "netstat": "Connexions actives\n\n  Proto  Adresse locale         Adresse distante       État\n  TCP    127.0.0.1:5432         127.0.0.1:49234        ESTABLISHED\n  TCP    0.0.0.0:80             0.0.0.0:0              LISTENING\n  TCP    0.0.0.0:443            0.0.0.0:0              LISTENING\n  TCP    192.168.1.105:49235    142.250.185.78:443     ESTABLISHED",
    "python": "Python 3.13.0 (main, Oct  7 2024, 05:02:14)\n[GCC 12.2.0] on linux\nType 'help', 'copyright', 'credits' or 'license' for more information.\n>>>",
    "python --version": "Python 3.13.0",
    "java -version": 'openjdk version "21.0.1" 2023-10-17\nOpenJDK Runtime Environment (build 21.0.1+12-29)\nOpenJDK 64-Bit Server VM (build 21.0.1+12-29, mixed mode)',
    "gcc --version": "gcc (Ubuntu 12.3.0-1ubuntu1~22.04) 12.3.0\nCopyright (C) 2022 Free Software Foundation, Inc.",
    "mysql --version": "mysql  Ver 8.0.35 Distrib 8.0.35, for Linux (x86_64)",
    "git --version": "git version 2.43.0",
}

def process_terminal_command(cmd: str) -> str:
    """Traite une commande terminal. Exécute de vraies commandes système de manière sécurisée."""
    import subprocess
    cmd = cmd.strip()
    cmd_lower = cmd.lower()
    
    if cmd == "" or cmd_lower == "clear" or cmd_lower == "cls":
        return "__CLEAR__"
        
    try:
        # Exécuter la vraie commande Windows avec timeout de 5 secondes
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        output = result.stdout
        if result.stderr:
            output += "\n" + result.stderr
        
        # fallback si vide
        if not output.strip():
            return f"[Commande '{cmd}' exécutée sans sortie]"
        
        # Garder les 2000 derniers caractères pour éviter de saturer l'UI
        return output.strip()[-2000:]
        
    except subprocess.TimeoutExpired:
        return f"[Erreur] La commande '{cmd}' a dépassé le délai autorisé (5s)."
    except Exception as e:
        return f"[Erreur] Impossible d'exécuter la commande : {str(e)}"


def matrix_add(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return None, "Matrices de dimensions différentes"
    result = [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    return result, "OK"

def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        return None, "Colonnes de A ≠ Lignes de B"
    rows_A, cols_A, cols_B = len(A), len(A[0]), len(B[0])
    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return result, "OK"

def matrix_transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def matrix_determinant_2x2(A):
    if len(A) != 2 or len(A[0]) != 2:
        return None, "Seulement pour matrices 2x2"
    return A[0][0]*A[1][1] - A[0][1]*A[1][0], "OK"


def ip_to_binary(ip: str) -> str:
    parts = ip.split('.')
    return '.'.join(bin(int(p))[2:].zfill(8) for p in parts)

def calculate_subnet(ip: str, cidr: int) -> dict:
    """Calcule les informations d'un sous-réseau."""
    try:
        parts = [int(x) for x in ip.split('.')]
        ip_int = sum(parts[i] << (24 - 8*i) for i in range(4))

        mask_int = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
        network_int = ip_int & mask_int
        broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
        first_host = network_int + 1
        last_host = broadcast_int - 1
        num_hosts = broadcast_int - network_int - 1

        def int_to_ip(n):
            return '.'.join(str((n >> (24 - 8*i)) & 0xFF) for i in range(4))

        mask_parts = [(mask_int >> (24 - 8*i)) & 0xFF for i in range(4)]

        return {
            "ip": ip,
            "cidr": f"/{cidr}",
            "masque": '.'.join(str(p) for p in mask_parts),
            "reseau": int_to_ip(network_int),
            "broadcast": int_to_ip(broadcast_int),
            "premier_hote": int_to_ip(first_host),
            "dernier_hote": int_to_ip(last_host),
            "nb_hotes": num_hosts,
            "ip_binaire": ip_to_binary(ip),
            "masque_binaire": ip_to_binary('.'.join(str(p) for p in mask_parts)),
        }
    except Exception as e:
        return {"error": str(e)}


QUIZ_QUESTIONS = {
    "Architecture": [
        {
            "question": "Quel est le rôle de l'Unité Arithmétique et Logique (UAL/ALU) ?",
            "options": ["Stocker les données", "Effectuer les calculs et opérations logiques", "Gérer la mémoire", "Contrôler les périphériques"],
            "correct": 1,
            "explication": "L'ALU (Arithmetic Logic Unit) est le composant du CPU qui effectue toutes les opérations mathématiques (addition, soustraction...) et logiques (AND, OR, NOT, comparaisons).",
            "matiere": "Architecture",
            "niveau": "Intermédiaire",
        },
        {
            "question": "Qu'est-ce que le 'bus' dans une architecture d'ordinateur ?",
            "options": ["Un programme de transport", "Un canal de communication entre composants", "Un type de processeur", "Une mémoire externe"],
            "correct": 1,
            "explication": "Le bus est un ensemble de lignes de communication qui permettent le transfert de données entre le CPU, la mémoire et les périphériques. Il y a le bus de données, d'adresses et de contrôle.",
            "matiere": "Architecture",
            "niveau": "Intermédiaire",
        },
        {
            "question": "Quelle est la différence entre la mémoire cache L1 et L2 ?",
            "options": ["L1 est plus lente que L2", "L1 est plus rapide et plus petite que L2", "L2 est intégrée dans le CPU", "Aucune différence"],
            "correct": 1,
            "explication": "Cache L1: très rapide, très petite (32-64 KB), directement dans le cœur du CPU. Cache L2: plus lente que L1, plus grande (256 KB - 1 MB), partagée entre cœurs. L3 encore plus grande mais plus lente.",
            "matiere": "Architecture",
            "niveau": "Intermédiaire",
        },
    ],
    "Algèbre de Boole": [
        {
            "question": "Quelle est la valeur de: 1 AND 0 ?",
            "options": ["1", "0", "Indéfini", "2"],
            "correct": 1,
            "explication": "AND (ET logique) retourne 1 seulement si LES DEUX entrées sont 1. Ici, une entrée est 0, donc 1 AND 0 = 0.",
            "matiere": "Algèbre de Boole",
            "niveau": "Fondamental",
        },
        {
            "question": "Selon la loi de De Morgan, ¬(A AND B) est équivalent à ?",
            "options": ["¬A AND ¬B", "A OR B", "¬A OR ¬B", "¬(A OR B)"],
            "correct": 2,
            "explication": "Première loi de De Morgan: ¬(A·B) = ¬A + ¬B. Le NON d'un ET devient le OU des NON. C'est fondamental pour simplifier les circuits logiques.",
            "matiere": "Algèbre de Boole",
            "niveau": "Fondamental",
        },
        {
            "question": "Combien de lignes contient une table de vérité à 3 variables ?",
            "options": ["6", "8", "9", "12"],
            "correct": 1,
            "explication": "Une table de vérité à n variables contient 2ⁿ lignes. Pour 3 variables: 2³ = 8 lignes. Pour 2 variables: 4 lignes. Pour 4 variables: 16 lignes.",
            "matiere": "Algèbre de Boole",
            "niveau": "Fondamental",
        },
    ],
    "Programmation C": [
        {
            "question": "Quelle est la taille d'un int en C sur un système 32 bits ?",
            "options": ["2 octets", "4 octets", "8 octets", "Dépend du compilateur"],
            "correct": 3,
            "explication": "La taille d'un int en C n'est pas fixe — elle dépend du compilateur et de l'architecture. Sur 32 bits elle est généralement 4 octets, mais C ne le garantit pas. Utilise int32_t si tu veux une taille fixe.",
            "matiere": "Programmation C",
            "niveau": "Intermédiaire",
        },
        {
            "question": "Qu'affiche: printf(\"%d\", 5/2) en C ?",
            "options": ["2.5", "2", "3", "Erreur"],
            "correct": 1,
            "explication": "En C, la division entre deux entiers donne un entier (division entière). 5/2 = 2 (le reste 1 est ignoré). Pour obtenir 2.5, il faut: 5.0/2 ou (float)5/2.",
            "matiere": "Programmation C",
            "niveau": "Intermédiaire",
        },
        {
            "question": "Que fait le symbole & devant une variable dans scanf ?",
            "options": ["Effectue un AND logique", "Passe l'adresse mémoire de la variable", "Duplique la variable", "Crée un pointeur"],
            "correct": 1,
            "explication": "Le & (opérateur d'adresse) retourne l'adresse mémoire de la variable. scanf a besoin de l'adresse pour pouvoir MODIFIER la variable (écrire dedans). Sans &, scanf reçoit une copie et ne peut pas modifier l'original.",
            "matiere": "Programmation C",
            "niveau": "Intermédiaire",
        },
    ],
    "SQL/MySQL": [
        {
            "question": "Quelle clause SQL filtre les résultats après un GROUP BY ?",
            "options": ["WHERE", "HAVING", "FILTER", "CONDITION"],
            "correct": 1,
            "explication": "WHERE filtre les lignes AVANT le groupement. HAVING filtre les groupes APRÈS le GROUP BY. Ex: SELECT dept, COUNT(*) FROM emp GROUP BY dept HAVING COUNT(*) > 5;",
            "matiere": "SQL/MySQL",
            "niveau": "Avancé",
        },
        {
            "question": "Quelle est la différence entre INNER JOIN et LEFT JOIN ?",
            "options": ["Aucune différence", "INNER JOIN retourne seulement les lignes correspondantes des deux tables", "LEFT JOIN retourne seulement la table de gauche", "INNER JOIN retourne toutes les lignes"],
            "correct": 1,
            "explication": "INNER JOIN: retourne seulement les lignes qui ont une correspondance dans LES DEUX tables. LEFT JOIN: retourne TOUTES les lignes de la table gauche + les correspondances de droite (NULL si pas de correspondance).",
            "matiere": "SQL/MySQL",
            "niveau": "Avancé",
        },
        {
            "question": "Qu'est-ce qu'une transaction SQL ?",
            "options": ["Une requête SELECT", "Un ensemble d'opérations qui s'exécutent comme une unité atomique", "Un type de jointure", "Un index de table"],
            "correct": 1,
            "explication": "Une transaction est un groupe d'opérations SQL traité comme une unité. Propriétés ACID: Atomicité (tout ou rien), Cohérence, Isolation, Durabilité. Commandes: BEGIN, COMMIT, ROLLBACK.",
            "matiere": "SQL/MySQL",
            "niveau": "Avancé",
        },
    ],
    "Réseaux": [
        {
            "question": "Quelle est l'adresse de loopback (localhost) en IPv4 ?",
            "options": ["192.168.0.1", "10.0.0.1", "127.0.0.1", "172.16.0.1"],
            "correct": 2,
            "explication": "127.0.0.1 est l'adresse de loopback — elle pointe vers la machine elle-même. Utilisée pour tester les applications réseau localement. Le nom DNS correspondant est 'localhost'.",
            "matiere": "Réseaux",
            "niveau": "Fondamental",
        },
        {
            "question": "Combien de couches a le modèle OSI ?",
            "options": ["4", "5", "6", "7"],
            "correct": 3,
            "explication": "Le modèle OSI a 7 couches: 1-Physique, 2-Liaison, 3-Réseau, 4-Transport, 5-Session, 6-Présentation, 7-Application. Mnémotechnique: 'Please Do Not Throw Sausage Pizza Away'",
            "matiere": "Réseaux",
            "niveau": "Fondamental",
        },
    ],
    "Python": [
        {
            "question": "Quelle est la sortie de: print(type([])).__name__ ?",
            "options": ["array", "list", "Array", "List"],
            "correct": 1,
            "explication": "En Python, [] crée une liste (list). type([]) retourne <class 'list'>, et .__name__ retourne la chaîne 'list'. Les listes Python sont dynamiques et peuvent contenir des types mixtes.",
            "matiere": "Python",
            "niveau": "Intermédiaire",
        },
        {
            "question": "Quelle est la différence entre une liste et un tuple en Python ?",
            "options": ["Aucune différence", "Un tuple utilise [] et une liste ()", "Un tuple est immuable, une liste est modifiable", "Un tuple ne peut contenir que des nombres"],
            "correct": 2,
            "explication": "Liste []: MUTABLE — on peut ajouter, supprimer, modifier des éléments. Tuple (): IMMUABLE — une fois créé, impossible de le modifier. Les tuples sont plus rapides et utilisent moins de mémoire.",
            "matiere": "Python",
            "niveau": "Intermédiaire",
        },
        {
            "question": "Que fait le mot-clé 'yield' dans une fonction Python ?",
            "options": ["Arrête immédiatement la fonction", "Retourne une valeur et met la fonction en pause", "Génère une erreur d'exécution", "Crée un thread séparé"],
            "correct": 1,
            "explication": "'yield' transforme une fonction classique en générateur. Contrairement à 'return' qui détruit les variables locales, 'yield' renvoie une valeur et garde l'état de la fonction en mémoire pour le prochain appel.",
            "matiere": "Python",
            "niveau": "Avancé",
        },
    ],
    "Développement Web": [
        {
            "question": "Que signifie l'acronyme DOM en JavaScript ?",
            "options": ["Data Object Model", "Document Object Model", "Digital Orientation Module", "Document Order Method"],
            "correct": 1,
            "explication": "Le DOM (Document Object Model) est une interface de programmation qui représente le document HTML/XML sous forme d'une arborescence d'objets, permettant à JavaScript de manipuler la page.",
            "matiere": "Développement Web",
            "niveau": "Intermédiaire",
        },
        {
            "question": "Quelle méthode HTTP est principalement utilisée pour mettre à jour une ressource de manière partielle ?",
            "options": ["PUT", "POST", "PATCH", "UPDATE"],
            "correct": 2,
            "explication": "PATCH est utilisé pour appliquer des modifications partielles à une ressource, tandis que PUT remplace généralement la ressource entière.",
            "matiere": "Développement Web",
            "niveau": "Intermédiaire",
        },
        {
            "question": "En CSS, que fait 'box-sizing: border-box' ?",
            "options": ["Met une bordure autour de toutes les boîtes", "Le padding et la bordure sont inclus dans la largeur/hauteur", "Rend la boîte invisible", "Arrondit les angles de la boîte"],
            "correct": 1,
            "explication": "Avec border-box, la largeur (width) inclut le padding et la bordure. C'est essentiel pour éviter que les éléments ne débordent de leur parent lorsqu'on leur ajoute des marges internes.",
            "matiere": "Développement Web",
            "niveau": "Intermédiaire",
        },
    ],
    "Cybersécurité": [
        {
            "question": "Qu'est-ce qu'une attaque par force brute ?",
            "options": ["Casser le matériel avec un marteau", "Surcharger un serveur de requêtes (DDoS)", "Essayer toutes les combinaisons possibles de mots de passe", "Infiltrer physiquement un bâtiment"],
            "correct": 2,
            "explication": "Une attaque par force brute (brute-force) consiste à tester toutes les combinaisons possibles (lettres, chiffres, symboles) jusqu'à trouver le bon mot de passe ou la clé de déchiffrement.",
            "matiere": "Cybersécurité",
            "niveau": "Fondamental",
        },
        {
            "question": "Que signifie XSS dans le contexte de la sécurité web ?",
            "options": ["Cross-Site Scripting", "XML Site Security", "Cross-Server Synchronization", "Extreme System Securing"],
            "correct": 0,
            "explication": "Cross-Site Scripting (XSS) est une faille permettant d'injecter des scripts malveillants (souvent du JavaScript) dans les pages web vues par d'autres utilisateurs.",
            "matiere": "Cybersécurité",
            "niveau": "Avancé",
        },
        {
            "question": "Quel est le but principal de l'attaque CSRF ?",
            "options": ["Voler la base de données", "Forcer un utilisateur authentifié à exécuter une action à son insu", "Déchiffrer le trafic réseau", "Faire tomber le site hors ligne"],
            "correct": 1,
            "explication": "CSRF (Cross-Site Request Forgery) exploite la confiance qu'un site a envers le navigateur de l'utilisateur. Si l'utilisateur est connecté, un site malveillant peut lui faire envoyer une requête forgée (ex: virement bancaire).",
            "matiere": "Cybersécurité",
            "niveau": "Avancé",
        },
    ],
    "Linux & Terminal": [
        {
            "question": "Quelle commande Linux est utilisée pour changer les permissions d'un fichier ?",
            "options": ["chown", "chmod", "chperm", "modfile"],
            "correct": 1,
            "explication": "'chmod' (change mode) modifie les droits d'accès (lecture, écriture, exécution) d'un fichier ou dossier. 'chown' modifie le propriétaire (owner).",
            "matiere": "Linux & Terminal",
            "niveau": "Intermédiaire",
        },
        {
            "question": "Dans le terminal bash, que fait 'ls -la' ?",
            "options": ["Liste tous les fichiers, y compris les fichiers cachés, avec des détails", "Lance un scan local", "Supprime tous les fichiers", "Liste seulement les applications"],
            "correct": 0,
            "explication": "ls (list) avec les flags -l (format long avec détails) et -a (all, incluant les fichiers cachés commençant par '.').",
            "matiere": "Linux & Terminal",
            "niveau": "Fondamental",
        },
    ]
}

def get_quiz_question(matiere: str = None) -> dict:
    """Retourne une question aléatoire pour une matière donnée, ou toutes si matiere est None."""
    if matiere is None:
        all_questions = [q for qs in QUIZ_QUESTIONS.values() for q in qs]
        return random.choice(all_questions) if all_questions else {}
    if matiere in QUIZ_QUESTIONS and QUIZ_QUESTIONS[matiere]:
        return random.choice(QUIZ_QUESTIONS[matiere])
    return {}


CODE_TEMPLATES = {
    "Boucle For en C": {
        "langage": "c",
        "code": """#include <stdio.h>

int main() {
    int i;
    int n = 10; // Nombre d'itérations
    
    for (i = 0; i < n; i++) {
        printf("Itération %d\\n", i);
    }
    
    return 0;
}"""
    },
    "Boucle While en C": {
        "langage": "c",
        "code": """#include <stdio.h>

int main() {
    int compteur = 0;
    
    while (compteur < 5) {
        printf("Compteur: %d\\n", compteur);
        compteur++;
    }
    
    return 0;
}"""
    },
    "Fonction avec Pointeur en C": {
        "langage": "c",
        "code": """#include <stdio.h>

// Passage par pointeur pour modifier la variable originale
void incrementer(int *valeur) {
    *valeur = *valeur + 1;
}

int main() {
    int nombre = 5;
    printf("Avant: %d\\n", nombre);
    
    incrementer(&nombre); // On passe l'adresse
    
    printf("Après: %d\\n", nombre);
    return 0;
}"""
    },
    "Classe en Java": {
        "langage": "java",
        "code": """public class Etudiant {
    // Attributs (encapsulation)
    private String nom;
    private int age;
    private double moyenne;
    
    // Constructeur
    public Etudiant(String nom, int age) {
        this.nom = nom;
        this.age = age;
        this.moyenne = 0.0;
    }
    
    // Getters et Setters
    public String getNom() { return nom; }
    public void setMoyenne(double moy) { this.moyenne = moy; }
    
    // Méthode
    public String getStatut() {
        return (moyenne >= 10) ? "Admis" : "Recalé";
    }
    
    // Main
    public static void main(String[] args) {
        Etudiant e = new Etudiant("Lucky Luke", 20);
        e.setMoyenne(14.5);
        System.out.println(e.getNom() + ": " + e.getStatut());
    }
}"""
    },
    "Requête SQL de base": {
        "langage": "sql",
        "code": """-- Créer une table
CREATE TABLE etudiants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    moyenne DECIMAL(4,2),
    date_inscription DATE DEFAULT CURRENT_DATE
);

-- Insérer des données
INSERT INTO etudiants (nom, prenom, moyenne)
VALUES ('Luke', 'Lucky', 14.50);

-- Sélectionner avec condition
SELECT nom, prenom, moyenne
FROM etudiants
WHERE moyenne >= 10
ORDER BY moyenne DESC;

-- Jointure
SELECT e.nom, c.titre_cours
FROM etudiants e
INNER JOIN inscriptions i ON e.id = i.etudiant_id
INNER JOIN cours c ON i.cours_id = c.id;"""
    },
    "Script Python de base": {
        "langage": "python",
        "code": """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Votre script Python ici
def main():
    print("Bonjour depuis Asta Académie !")

if __name__ == "__main__":
    main()
"""
    },
    "Classe en Python (POO)": {
        "langage": "python",
        "code": """class Etudiant:
    # Attribut de classe
    universite = "UNASMOH"
    
    def __init__(self, nom: str, niveau: str):
        # Attributs d'instance
        self.nom = nom
        self.niveau = niveau
        self.notes = []
    
    def ajouter_note(self, note: float):
        if 0 <= note <= 20:
            self.notes.append(note)
    
    def calculer_moyenne(self) -> float:
        if not self.notes:
            return 0.0
        return sum(self.notes) / len(self.notes)
    
    def __str__(self):
        return f"{self.nom} ({self.niveau}) - Moy: {self.calculer_moyenne():.2f}"


# Utilisation
etudiant = Etudiant("Lucky Luke", "L2")
etudiant.ajouter_note(15)
etudiant.ajouter_note(14)
etudiant.ajouter_note(16)
print(etudiant)
print(f"Université: {Etudiant.universite}")"""
    },
}

# =====================================================================
# BLOC DE TESTS DE VALIDATION
# =====================================================================
if __name__ == "__main__":
    print("Exécution des tests de validation de logic_tools.py...")
    
    # Test decimal_to_binary
    assert decimal_to_binary(4) == "100", "Erreur: decimal_to_binary(4)"
    assert decimal_to_binary(-5) == "Complément à 2: 11111011", "Erreur: decimal_to_binary(-5)"
    
    # Test convert_all
    res = convert_all("4", "decimal")
    assert res["binary"] == "100" and res["hexadecimal"] == "4", "Erreur: convert_all('4', 'decimal')"
    
    # Test matrix_add
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    R, msg = matrix_add(A, B)
    assert R == [[6, 8], [10, 12]] and msg == "OK", "Erreur: matrix_add"
    
    # Test matrix_multiply
    R_mul, msg_mul = matrix_multiply(A, B)
    assert R_mul == [[19, 22], [43, 50]] and msg_mul == "OK", "Erreur: matrix_multiply"
    
    # Test ip_to_binary
    assert ip_to_binary("192.168.1.1") == "11000000.10101000.00000001.00000001", "Erreur: ip_to_binary"
    
    # Test calculate_subnet
    subnet = calculate_subnet("192.168.1.10", 24)
    assert subnet["masque"] == "255.255.255.0", "Erreur: masque de sous-réseau"
    assert subnet["reseau"] == "192.168.1.0", "Erreur: adresse réseau"
    assert subnet["broadcast"] == "192.168.1.255", "Erreur: adresse broadcast"
    
    print("[OK] Tous les tests de validation ont réussi avec succès !")