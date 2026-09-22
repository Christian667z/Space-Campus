"""
Space AI Engine - Synonym Map Module
Standardise le vocabulaire de l'étudiant pour correspondre aux mots-clés du cours.
"""
import unicodedata

SYNONYM_MAP = {
    "bdd": "base_donnees",
    "base": "base_donnees",
    "bases": "base_donnees",
    "database": "base_donnees",
    "databases": "base_donnees",
    "sql": "mysql",
    "mysql": "mysql",
    "relationnel": "relationnel",
    "relationnelle": "relationnel",
    "html": "html5",
    "html5": "html5",
    "css": "css3",
    "css3": "css3",
    "style": "css3",
    "flex": "flexbox",
    "flexbox": "flexbox",
    "grid": "grid",
    "boole": "boole",
    "boolean": "boole",
    "booleen": "boole",
    "booleenne": "boole",
    "morgan": "morgan",
    "demorgan": "morgan",
    "porte": "porte",
    "portes": "porte",
    "gate": "porte",
    "gates": "porte",
    "algo": "algorithme",
    "algos": "algorithme",
    "algorithme": "algorithme",
    "algorithmes": "algorithme",
    "algorithmique": "algorithme",
    "prog": "programmation",
    "programmation": "programmation",
    "code": "programmation",
    "coder": "programmation",
    "dev": "programmation",
    "developpement": "programmation",
    "ordinateur": "architecture",
    "ordinateurs": "architecture",
    "architecture": "architecture",
    "pc": "architecture",
    "machine": "architecture",
    "von": "neumann",
    "neumann": "neumann",
    "os": "systeme",
    "systeme": "systeme",
    "noyau": "kernel",
    "kernel": "kernel",
    "process": "processus",
    "processus": "processus",
    "thread": "thread",
    "threads": "thread",
    "liste": "liste_chainee",
    "listes": "liste_chainee",
    "chainee": "liste_chainee",
    "chainees": "liste_chainee",
    "noeud": "noeud",
    "noeuds": "noeud",
    "node": "noeud",
    "nodes": "noeud",
    "pointer": "pointeur",
    "pointers": "pointeur",
    "pointeur": "pointeur",
    "pointeurs": "pointeur",
    "memory": "memoire",
    "memoire": "memoire",
    "ram": "ram",
    "rom": "rom",
    "cache": "cache",
    "registre": "registre",
    "registres": "registre",
}

def remove_accents(text: str) -> str:
    """Retire les accents d'une chaîne de caractères."""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calcule la distance de Levenshtein entre deux mots."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
        
    return previous_row[-1]

def find_best_synonym_match(token: str) -> str | None:
    """Trouve la clé de synonyme la plus proche en utilisant la distance de Levenshtein."""
    best_key = None
    min_dist = 99
    
    # Seuil maximal de modifications (1 pour les mots courts, 2 pour les mots plus longs)
    max_dist = 1 if len(token) < 5 else 2
    
    for key in SYNONYM_MAP.keys():
        if abs(len(token) - len(key)) > max_dist:
            continue
        dist = levenshtein_distance(token, key)
        if dist < min_dist:
            min_dist = dist
            best_key = key
            
    if min_dist <= max_dist:
        return best_key
    return None

def standardize_tokens(tokens: list) -> list:
    """Remplace les tokens par leur équivalent standardisé avec correction orthographique Levenshtein."""
    standardized = []
    for token in tokens:
        clean_token = remove_accents(token.lower().strip())
        if clean_token in SYNONYM_MAP:
            standardized.append(SYNONYM_MAP[clean_token])
        else:
            corrected = find_best_synonym_match(clean_token)
            if corrected:
                standardized.append(SYNONYM_MAP[corrected])
            else:
                standardized.append(clean_token)
    return standardized

