"""
Space AI Engine - Intent Parser Module
Analyse l'entrée utilisateur pour extraire son intention.
"""
import re
from core.synonym_map import standardize_tokens, remove_accents

STOP_WORDS = {
    "le", "la", "les", "un", "une", "des", "du", "de", "d", "l", "s", "se", "ce", "cet", "cette", "ces", 
    "et", "ou", "mais", "donc", "or", "ni", "car", "que", "qui", "quoi", "dont", "ou", "a", "à", "en", "dans",
    "par", "pour", "avec", "sans", "sous", "sur", "vers", "chez", "je", "tu", "il", "elle", "nous",
    "vous", "ils", "elles", "mon", "ton", "son", "ma", "ta", "sa", "mes", "tes", "ses", "notre", "votre",
    "leur", "nos", "vos", "leurs", "est", "sont", "ont", "aussi", "plus", "moins", "fait", "faire", "veux",
    "peux", "doit", "savoir", "connaître", "connaitre", "pose", "poser", "question", "questions"
}

GREETING_WORDS = {"bonjour", "salut", "bonsoir", "hello", "coucou", "hey", "salutation", "salutations", "yo"}
TIME_WORDS = {"heure", "temps", "date", "horloge", "moment"}
NAVIGATE_WORDS = {"navigue", "aller", "va", "ouvre", "affiche", "montre", "dirige", "redirige", "onglet"}

def tokenize(text: str) -> list[str]:
    """Sépare le texte en mots nettoyés, sans ponctuation et en minuscules."""
    text = remove_accents(text.lower())
    # Remplace les caractères de ponctuation par des espaces
    text = re.sub(r"[^\w\+\-\*\/\(\)\^\%\=\.]", " ", text)
    tokens = text.split()
    return tokens

def parse_intent(text: str) -> tuple[str, list[str]]:
    """Classifie l'intention de l'utilisateur et retourne les tokens nettoyés."""
    tokens = tokenize(text)
    
    # 1. Nettoyage des stop words
    filtered_tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]
    
    # 2. Standardisation via le synonym_map
    standardized_tokens = standardize_tokens(filtered_tokens)
    
    text_lower = remove_accents(text.lower())
    
    # 3. Détection de l'intention NAVIGATE
    if any(w in standardized_tokens for w in NAVIGATE_WORDS) or "onglet" in text_lower or "va sur" in text_lower:
        return "NAVIGATE", standardized_tokens
        
    # 4. Détection de l'intention GREETING
    if any(w in tokens for w in GREETING_WORDS):
        return "GREETING", standardized_tokens
        
    # 5. Détection de l'intention TIME
    if any(w in standardized_tokens for w in TIME_WORDS):
        return "TIME", standardized_tokens
        
    # 6. Détection de l'intention MATHS
    # Si le texte contient "calcule", "combien font", "somme", ou ressemble à une formule
    # regex pour repérer si le texte contient principalement des chiffres et opérateurs arithmétiques
    math_pattern = r"[\d\+\-\*\/\(\)\s\.\^\%]+"
    # On nettoie les espaces
    cleaned_expr = text_lower.replace("calcule", "").replace("=", "").strip()
    # Si après nettoyage il reste principalement une expression mathématique
    if re.fullmatch(math_pattern, cleaned_expr) and any(op in cleaned_expr for op in ["+", "-", "*", "/", "^", "%"]) and any(c.isdigit() for c in cleaned_expr):
        return "MATHS", [cleaned_expr]
    elif "calcule" in text_lower or "combien font" in text_lower:
        # Extraire l'expression après "calcule" ou "combien font"
        expr_match = re.search(r"(?:calcule|combien font|combien fait)\s*(.*)", text_lower)
        if expr_match:
            potential_expr = expr_match.group(1).replace("=", "").strip()
            if potential_expr:
                return "MATHS", [potential_expr]
        
    # 7. Intention par défaut : COURS
    return "COURS", standardized_tokens
