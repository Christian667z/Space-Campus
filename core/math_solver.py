"""
Space AI Engine - Math Solver Module
Évalue de manière sécurisée les expressions arithmétiques pour éviter l'utilisation de eval().
"""
import ast
import operator

# Opérateurs binaires supportés
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Opérateurs unaires supportés
UNARY_OPS = {
    ast.UAdd: lambda x: x,
    ast.USub: lambda x: -x,
}

def eval_node(node):
    """Évalue récursivement un nœud de l'arbre syntaxique abstrait (AST)."""
    # Nombres
    if isinstance(node, ast.Constant):
        val = node.value
        if isinstance(val, (int, float)):
            return val
        raise ValueError("Seuls les nombres réels ou entiers sont autorisés.")
    
    # Compatibilité avec anciennes versions de Python (au cas où)
    elif isinstance(node, ast.Num):
        val = node.n
        if isinstance(val, (int, float)):
            return val
        raise ValueError("Seuls les nombres réels ou entiers sont autorisés.")
        
    # Opérations binaires (+, -, *, /, etc.)
    elif isinstance(node, ast.BinOp):
        left = eval_node(node.left)
        right = eval_node(node.right)
        op_type = type(node.op)
        
        if op_type in BIN_OPS:
            # Sécurité : Division par zéro
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                raise ZeroDivisionError("Division par zéro impossible.")
            # Sécurité : Limiter les exposants pour éviter les dépassements de mémoire (ex: 9999**9999)
            if op_type == ast.Pow:
                if right > 100 or left > 10000:
                    raise ValueError("Exposant ou base trop élevé.")
            return BIN_OPS[op_type](left, right)
            
        raise NotImplementedError(f"Opérateur non supporté : {op_type.__name__}")
        
    # Opérations unaires (-5, +3)
    elif isinstance(node, ast.UnaryOp):
        operand = eval_node(node.operand)
        op_type = type(node.op)
        
        if op_type in UNARY_OPS:
            return UNARY_OPS[op_type](operand)
            
        raise NotImplementedError(f"Opérateur non supporté : {op_type.__name__}")
        
    # Nœud racine de l'expression
    elif isinstance(node, ast.Expression):
        return eval_node(node.body)
        
    raise ValueError("Expression contenant des éléments non autorisés.")

def safe_eval(expr: str) -> float | int | str:
    """Valide et évalue une chaîne contenant une expression mathématique de manière sécurisée."""
    expr = expr.strip()
    if not expr:
        return "Expression vide."
        
    # Remplacements de commodité
    expr = expr.replace("^", "**")
    
    try:
        # Analyse et parsing sécurisé
        tree = ast.parse(expr, mode='eval')
        result = eval_node(tree)
        
        # Formater pour éviter les .0 inutiles sur les entiers
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result
    except ZeroDivisionError:
        return "Erreur : Division par zéro."
    except Exception as e:
        return f"Erreur de calcul : {str(e)}"
