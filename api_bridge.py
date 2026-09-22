"""
Asta Académie — API Bridge étendu
Sert de pont HTTP entre le C# WPF et le backend Python.
Endpoints : SpaceAI, Oracle, Raccourcis, Quiz, Cours, Notes, Profil
"""
import asyncio
import json
import os
import random
from aiohttp import web

# ── Chargement des modules Python ──────────────────────────────────────────

try:
    from core.ai_engine import AiEngine
    from core.config import PROFILE_FILE
    profile_data = {}
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data: profile_data = data
    ai_engine = AiEngine(profile=profile_data)
    print("[API Bridge] Space AI chargé.")
except Exception as e:
    print(f"[API Bridge] Space AI indisponible : {e}")
    ai_engine = None

try:
    from utils.oracle_hub import get_daily_tip, get_random_fact, get_random_quote, TECH_TIMELINE, HAITI_TECH_HISTORY
    from utils.shortcuts_data import (
        EXCEL_SHORTCUTS, EXCEL_FORMULAS, PROF_TRAPS,
        LINUX_COMMANDS, OSI_LAYERS, NETWORK_PROTOCOLS)
    print("[API Bridge] Oracle + Raccourcis chargés.")
except Exception as e:
    print(f"[API Bridge] Oracle/Raccourcis partiels : {e}")
    get_daily_tip   = lambda: "L'intelligence n'est pas de tout savoir, mais de savoir où chercher."
    get_random_fact = lambda: "Le premier bug informatique était un vrai papillon de nuit."
    get_random_quote = lambda: {"citation": "Talk is cheap. Show me the code.", "auteur": "Linus Torvalds", "role": "Créateur de Linux"}
    TECH_TIMELINE = []; HAITI_TECH_HISTORY = []
    EXCEL_SHORTCUTS = []; EXCEL_FORMULAS = []; PROF_TRAPS = []
    LINUX_COMMANDS = []; OSI_LAYERS = []; NETWORK_PROTOCOLS = []

try:
    from core.logic_tools import QUIZ_QUESTIONS
    print("[API Bridge] Quiz chargé.")
except Exception as e:
    print(f"[API Bridge] Quiz indisponible : {e}")
    QUIZ_QUESTIONS = {"Général": [
        {"question": "Qu'est-ce qu'une adresse IP ?", "options": ["Un identifiant réseau", "Un fichier système", "Un algorithme", "Un protocole"], "correct": 0, "explication": "L'adresse IP identifie un appareil sur un réseau.", "matiere": "Réseau", "niveau": "L1"}
    ]}

try:
    from lessons.cours_data import PROGRAMME_COMPLET
    print("[API Bridge] Cours chargés.")
except Exception as e:
    print(f"[API Bridge] Cours indisponibles : {e}")
    PROGRAMME_COMPLET = {}

try:
    from core.config import DB_FILE, NOTES_FILE, PROFILE_FILE, DATA_DIR
    print("[API Bridge] Config chargée.")
except Exception as e:
    print(f"[API Bridge] Config : {e}")
    DB_FILE = "data/asta_database.db"
    NOTES_FILE = "data/notes.json"
    DATA_DIR = "data"

# ══════════════════════════════════════════════════════════════════════════
#  HANDLERS
# ══════════════════════════════════════════════════════════════════════════

async def handle_ping(request):
    return web.json_response({"status": "online", "version": "2.0"})

# ── Space AI ──────────────────────────────────────────────────────────────

async def handle_chat(request):
    try:
        data = await request.json()
        msg = data.get("message", "")
        if not msg:
            return web.json_response({"error": "Message vide"}, status=400)
        if ai_engine:
            try:
                if asyncio.iscoroutinefunction(ai_engine.process):
                    resp = await ai_engine.process(msg)
                else:
                    resp = ai_engine.process(msg)
            except Exception as e:
                resp = f"Erreur Space AI : {e}"
        else:
            resp = "Le moteur Space AI n'a pas pu être chargé."
        return web.json_response({"response": resp})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

# ── Oracle ────────────────────────────────────────────────────────────────

async def handle_oracle_tip(request):
    return web.json_response({"tip": get_daily_tip()})

async def handle_oracle_fact(request):
    return web.json_response({"fact": get_random_fact()})

async def handle_oracle_quote(request):
    q = get_random_quote()
    return web.json_response(q if isinstance(q, dict) else {"citation": str(q), "auteur": "", "role": ""})

async def handle_oracle_timeline(request):
    return web.json_response({"timeline": TECH_TIMELINE, "haiti": HAITI_TECH_HISTORY})

# ── Raccourcis ────────────────────────────────────────────────────────────

async def handle_shortcuts_excel(request):
    return web.json_response({"shortcuts": EXCEL_SHORTCUTS, "formulas": EXCEL_FORMULAS})

async def handle_shortcuts_traps(request):
    return web.json_response({"traps": PROF_TRAPS})

async def handle_shortcuts_linux(request):
    return web.json_response({"commands": LINUX_COMMANDS})

async def handle_shortcuts_osi(request):
    return web.json_response({"layers": OSI_LAYERS})

async def handle_shortcuts_protocols(request):
    return web.json_response({"protocols": NETWORK_PROTOCOLS})

# ── Quiz ──────────────────────────────────────────────────────────────────

async def handle_quiz_questions(request):
    matiere = request.rel_url.query.get("matiere", "")
    if matiere and matiere in QUIZ_QUESTIONS:
        qs = QUIZ_QUESTIONS[matiere]
    else:
        qs = [q for lst in QUIZ_QUESTIONS.values() for q in lst]
    sample = random.sample(qs, min(10, len(qs)))
    matieres = sorted(QUIZ_QUESTIONS.keys())
    return web.json_response({"questions": sample, "matieres": matieres})

# ── Cours ─────────────────────────────────────────────────────────────────

async def handle_courses(request):
    result = []
    for niveau, data in PROGRAMME_COMPLET.items():
        for matiere, details in data.get("cours", {}).items():
            result.append({
                "niveau": niveau,
                "matiere": matiere,
                "chapitres": details if isinstance(details, list) else []
            })
    return web.json_response({"cours": result})

# ── Notes ─────────────────────────────────────────────────────────────────

async def handle_notes_get(request):
    try:
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                notes = json.load(f)
            if isinstance(notes, dict):
                flat = [{"id": k, **v} for k, v in notes.items()]
            else:
                flat = notes
            return web.json_response({"notes": flat})
    except Exception:
        # Ignoring errors here is intentional; fallback values are provided above
        pass
    return web.json_response({"notes": []})

async def handle_notes_save(request):
    try:
        data = await request.json()
        notes = {}
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                notes = json.load(f)
        note_id = data.get("id", str(random.randint(10000, 99999)))
        notes[note_id] = {
            "titre": data.get("titre", "Sans titre"),
            "contenu": data.get("contenu", ""),
            "date": data.get("date", ""),
            "categorie": data.get("categorie", "Général")
        }
        os.makedirs(DATA_DIR if isinstance(DATA_DIR, str) else str(DATA_DIR), exist_ok=True)
        path = NOTES_FILE if isinstance(NOTES_FILE, str) else str(NOTES_FILE)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
        return web.json_response({"status": "ok", "id": note_id})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def handle_notes_delete(request):
    try:
        data = await request.json()
        note_id = str(data.get("id", ""))
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                notes = json.load(f)
            notes.pop(note_id, None)
            with open(NOTES_FILE if isinstance(NOTES_FILE, str) else str(NOTES_FILE), "w", encoding="utf-8") as f:
                json.dump(notes, f, ensure_ascii=False, indent=2)
        return web.json_response({"status": "ok"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

# ── Profil ────────────────────────────────────────────────────────────────

async def handle_profile(request):
    try:
        path = PROFILE_FILE if isinstance(PROFILE_FILE, str) else str(PROFILE_FILE)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data:
                first = next(iter(data.values()))
                return web.json_response(first)
    except Exception as e:
        pass
    return web.json_response({"nom": "Étudiant", "niveau": "L2", "points": 0, "streak": 0})

# ══════════════════════════════════════════════════════════════════════════
#  ROUTING
# ══════════════════════════════════════════════════════════════════════════

app = web.Application()
app.router.add_get( '/api/ping',                  handle_ping)
app.router.add_post('/api/spaceai/chat',           handle_chat)
app.router.add_get( '/api/oracle/tip',             handle_oracle_tip)
app.router.add_get( '/api/oracle/fact',            handle_oracle_fact)
app.router.add_get( '/api/oracle/quote',           handle_oracle_quote)
app.router.add_get( '/api/oracle/timeline',        handle_oracle_timeline)
app.router.add_get( '/api/shortcuts/excel',        handle_shortcuts_excel)
app.router.add_get( '/api/shortcuts/traps',        handle_shortcuts_traps)
app.router.add_get( '/api/shortcuts/linux',        handle_shortcuts_linux)
app.router.add_get( '/api/shortcuts/osi',          handle_shortcuts_osi)
app.router.add_get( '/api/shortcuts/protocols',    handle_shortcuts_protocols)
app.router.add_get( '/api/quiz/questions',         handle_quiz_questions)
app.router.add_get( '/api/courses',                handle_courses)
app.router.add_get( '/api/notes',                  handle_notes_get)
app.router.add_post('/api/notes/save',             handle_notes_save)
app.router.add_post('/api/notes/delete',           handle_notes_delete)
app.router.add_get( '/api/profile',                handle_profile)

if __name__ == '__main__':
    print("=" * 52)
    print("  ASTA ACADÉMIE — PYTHON API BRIDGE v2.0")
    print("  Serveur sur http://localhost:5005")
    print("  Endpoints : SpaceAI, Oracle, Raccourcis,")
    print("              Quiz, Cours, Notes, Profil")
    print("=" * 52)
    web.run_app(app, host='127.0.0.1', port=5005)
