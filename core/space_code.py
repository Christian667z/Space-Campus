"""
╔══════════════════════════════════════════════════════════════╗
║           ASTA ACADÉMIE — SPACE CODE EDITOR MODULE           ║
║         Développé par Space | Asta Dev — Promo 2024-2028     ║
╚══════════════════════════════════════════════════════════════╝
"""

import tempfile
import webbrowser
import os

HTML_TEMPLATES = {
    "Page HTML5 de Base": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ma Page</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            text-align: center;
            padding: 40px;
        }
        h1 { color: #4fc3f7; font-size: 2.5rem; margin-bottom: 20px; }
        p { font-size: 1.2rem; color: #b0bec5; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Asta Académie</h1>
        <p>UNASMOH — Sciences Informatiques</p>
        <p>Développé par Space | Asta Dev</p>
    </div>
</body>
</html>""",

    "Formulaire de Contact": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Formulaire de Contact</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .form-card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 40px;
            width: 400px;
        }
        h2 { color: #4fc3f7; margin-bottom: 25px; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; color: #b0bec5; margin-bottom: 8px; font-size: 0.9rem; }
        input, textarea {
            width: 100%;
            padding: 12px 15px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 10px;
            color: white;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }
        input:focus, textarea:focus { border-color: #4fc3f7; }
        textarea { resize: vertical; min-height: 100px; }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(45deg, #4fc3f7, #0288d1);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="form-card">
        <h2>📬 Contactez-nous</h2>
        <div class="form-group">
            <label>Nom complet</label>
            <input type="text" placeholder="Lucky Luke">
        </div>
        <div class="form-group">
            <label>Email</label>
            <input type="email" placeholder="etudiant@unasmoh.edu.ht">
        </div>
        <div class="form-group">
            <label>Message</label>
            <textarea placeholder="Votre message..."></textarea>
        </div>
        <button onclick="alert('Message envoyé ! ✅')">Envoyer</button>
    </div>
</body>
</html>""",

    "Tableau de Bord": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Étudiant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0d1117;
            color: #c9d1d9;
        }
        .sidebar {
            width: 200px;
            background: #161b22;
            height: 100vh;
            position: fixed;
            padding: 20px;
            border-right: 1px solid #30363d;
        }
        .sidebar h2 { color: #4fc3f7; margin-bottom: 30px; }
        .nav-item {
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 5px;
            transition: background 0.2s;
        }
        .nav-item:hover { background: #21262d; }
        .nav-item.active { background: #1f6feb; color: white; }
        .main {
            margin-left: 200px;
            padding: 30px;
        }
        .cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
        }
        .card .number { font-size: 2.5rem; font-weight: bold; color: #4fc3f7; }
        .card .label { color: #8b949e; margin-top: 5px; }
        h1 { color: white; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>🎓 UNASMOH</h2>
        <div class="nav-item active">📊 Dashboard</div>
        <div class="nav-item">📚 Cours</div>
        <div class="nav-item">📝 Notes</div>
        <div class="nav-item">⚙️ Paramètres</div>
    </div>
    <div class="main">
        <h1>Tableau de Bord Étudiant</h1>
        <p style="color:#8b949e; margin-top:5px;">Bienvenue, Lucky Luke — L2 Sciences Info</p>
        <div class="cards">
            <div class="card">
                <div class="number">14.5</div>
                <div class="label">Moyenne Générale</div>
            </div>
            <div class="card">
                <div class="number">8</div>
                <div class="label">Cours ce semestre</div>
            </div>
            <div class="card">
                <div class="number">92%</div>
                <div class="label">Taux de présence</div>
            </div>
        </div>
    </div>
</body>
</html>""",

    "Page de Login": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: radial-gradient(ellipse at center, #1a1a2e 0%, #000 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-box {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(79,195,247,0.3);
            border-radius: 20px;
            padding: 50px 40px;
            width: 380px;
            text-align: center;
            box-shadow: 0 0 40px rgba(79,195,247,0.1);
        }
        .logo { font-size: 3rem; margin-bottom: 10px; }
        h2 { color: #4fc3f7; margin-bottom: 5px; }
        .subtitle { color: #546e7a; font-size: 0.9rem; margin-bottom: 30px; }
        input {
            width: 100%;
            padding: 14px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            color: white;
            margin-bottom: 15px;
            font-size: 1rem;
            outline: none;
        }
        input:focus { border-color: #4fc3f7; }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(45deg, #1565c0, #4fc3f7);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            letter-spacing: 1px;
            transition: opacity 0.2s;
        }
        button:hover { opacity: 0.9; }
        .footer { margin-top: 20px; color: #546e7a; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo">🔐</div>
        <h2>Asta Académie</h2>
        <p class="subtitle">UNASMOH — Sciences Informatiques</p>
        <input type="text" placeholder="Identifiant étudiant">
        <input type="password" placeholder="Mot de passe">
        <button onclick="alert('Connexion réussie ! 🎉')">SE CONNECTER</button>
        <p class="footer">Développé par Space | Asta Dev © 2025</p>
    </div>
</body>
</html>""",
}


def render_html_in_browser(html_content: str) -> tuple[bool, str]:
    """
    Sauvegarde le HTML dans un fichier temporaire et l'ouvre dans le navigateur.
    Retourne (success: bool, message: str)
    """
    try:

        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, "asta_preview.html")
        
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        

        webbrowser.open(f"file:///{temp_file.replace(os.sep, '/')}")
        return True, f"✅ Rendu dans le navigateur ! Fichier: {temp_file}"
    except Exception as e:
        return False, f"❌ Erreur: {str(e)}"

def validate_html(html: str) -> list:
    """Validation basique du HTML."""
    warnings = []
    if "<!DOCTYPE html>" not in html and "<!doctype html>" not in html.lower():
        warnings.append("⚠️ Manque la déclaration <!DOCTYPE html>")
    if "<html" not in html:
        warnings.append("⚠️ Manque la balise <html>")
    if "<head>" not in html:
        warnings.append("⚠️ Manque la balise <head>")
    if "<body>" not in html:
        warnings.append("⚠️ Manque la balise <body>")
    if "<meta charset" not in html:
        warnings.append("ℹ️ Conseil: Ajouter <meta charset='UTF-8'> pour les accents")
    if "<title>" not in html:
        warnings.append("ℹ️ Conseil: Ajouter un <title> pour l'onglet du navigateur")
    
    for tag in ["div", "p", "span", "section", "article", "header", "footer"]:
        opens = html.count(f"<{tag}")
        closes = html.count(f"</{tag}>")
        if opens != closes:
            warnings.append(f"⚠️ Balise <{tag}> ouverte {opens}x mais fermée {closes}x")
    
    if not warnings:
        warnings.append("✅ HTML valide — Aucun problème détecté")
    
    return warnings


CSS_REFERENCE = {
    "Flexbox": {
        "description": "Système de mise en page flexible",
        "proprietes": [
            "display: flex;",
            "justify-content: center | flex-start | flex-end | space-between | space-around;",
            "align-items: center | flex-start | flex-end | stretch;",
            "flex-direction: row | column | row-reverse | column-reverse;",
            "flex-wrap: wrap | nowrap;",
            "gap: 20px;",
            "flex: 1; /* L'élément prend tout l'espace disponible */",
        ]
    },
    "Grid": {
        "description": "Grille CSS bidimensionnelle",
        "proprietes": [
            "display: grid;",
            "grid-template-columns: repeat(3, 1fr);",
            "grid-template-rows: auto;",
            "gap: 20px;",
            "grid-column: span 2; /* Occupe 2 colonnes */",
            "place-items: center; /* center dans les deux axes */",
        ]
    },
    "Animations": {
        "description": "Animations et transitions CSS",
        "proprietes": [
            "transition: all 0.3s ease;",
            "animation: monAnim 2s infinite;",
            "@keyframes monAnim { from { opacity: 0; } to { opacity: 1; } }",
            "transform: translateX(10px) rotate(45deg) scale(1.2);",
        ]
    },
    "Variables CSS": {
        "description": "Variables personnalisées CSS",
        "proprietes": [
            ":root { --couleur-principale: #4fc3f7; }",
            "color: var(--couleur-principale);",
            "--espacement: 20px;",
            "margin: var(--espacement);",
        ]
    },
}