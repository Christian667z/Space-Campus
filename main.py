"""
╔══════════════════════════════════════════════════════════════════════╗
║                    ASTA ACADÉMIE v2.0.0                              ║
║          Application Étudiante — Sciences Informatiques              ║
║          UNASMOH — Université Américaine des Sciences Modernes       ║
║          Développé par Space | Asta Dev — Promo 2024-2028            ║
╚══════════════════════════════════════════════════════════════════════╝

Améliorations v2.0 par rapport à v1.x :
  - LicenseWindow : auto-format clé, bouton 👁, compteur tentatives (max 5)
  - Suppression du time.sleep(2) bloquant → health-check non-bloquant
  - Bug streak corrigé (crash 1er du mois via replace(day=day-1))
  - Badges streak multi-niveaux : 3j 🌱, 7j 🔥, 14j 💎, 30j 👑
  - Sidebar : streak, points et niveau affichés sous le nom
  - Navigation clavier : Ctrl+1…Ctrl+9 pour les sections
  - Topbar : Ctrl+K pour ouvrir la recherche globale
  - Pomodoro : cycles work → courte pause → longue pause (4 cycles),
    compteur de sessions, durées configurables, couleurs différenciées
  - _do_search : fix du bug de closure lambda, badges de catégorie
  - Barre de statut : streak 🔥 affiché en direct
  - _show_section : exceptions loggées (plus de traceback.print_exc seul)
  - _on_close : fermeture propre sans os._exit(0)
  - global_exception_handler : bare except → except Exception
  - Logging structuré partout
  - Type hints complets
"""

import json
import os
import subprocess
import sys
import threading
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Optional

import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog

from security.security_auth import (
    load_hacking_license, verify_hacking_key, save_hacking_license,
    check_license_on_startup, verify_license, save_license,
    generate_hwid, log_usage,
)
from core.logic_tools import (
    convert_all, process_terminal_command, calculate_subnet,
    BOOL_LAWS, BIG_O_TABLE, ASCII_TABLE, CODE_TEMPLATES,
    QUIZ_QUESTIONS, get_quiz_question,
)
from utils.shortcuts_data import (
    EXCEL_SHORTCUTS, EXCEL_FORMULAS, PROF_TRAPS,
    LINUX_COMMANDS, NETWORK_PROTOCOLS, OSI_LAYERS,
)
from utils.oracle_hub import (
    get_random_fact, get_random_quote, get_daily_tip,
    TECH_TIMELINE, HAITI_TECH_HISTORY, CAREER_ADVICE,
)
from core.space_code import HTML_TEMPLATES, validate_html, CSS_REFERENCE
from lessons.cours_data import PROGRAMME_COMPLET
from utils.updates_asta import verify_update_file, apply_update, CURRENT_VERSION
from utils.logger import AstaLogger
from core.config import (
    APP_NAME, VERSION, UNIVERSITE, OPTION, PROMO,
    DEV_NAME, DEV_REAL, WHATSAPP, FULL_UNI,
    COLORS, DATA_DIR, PROFILE_FILE, NOTES_FILE, DB_FILE,
    SESSION_FILE, BASE_DIR,
    get_translation, load_json, save_json,
)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

MAX_LICENSE_ATTEMPTS   = 5
POMO_WORK_DEFAULT      = 25 * 60      # 25 minutes
POMO_SHORT_BREAK       = 5  * 60      # 5 minutes
POMO_LONG_BREAK        = 15 * 60      # 15 minutes
POMO_SESSIONS_BEFORE_LONG = 4         # toutes les 4 séances → longue pause

STREAK_BADGES = [
    (3,  "Assidu 3j 🌱"),
    (7,  "Assidu 7j 🔥"),
    (14, "Assidu 14j 💎"),
    (30, "Assidu 30j 👑"),
]

SPLASH_TIPS = [
    "Chargement des modules…",
    "Vérification de la base de données…",
    "Initialisation des cours L1→L4…",
    "Chargement de l'Oracle et des outils…",
    "Préparation du module CTF…",
    "Configuration de l'interface…",
    "Bienvenue sur Asta Académie ! 🚀",
]

NAV_SECTIONS = [
    ("dashboard", "🏠 Accueil"),
    ("oracle",    "🔮 L'Oracle"),
    ("tools",     "🔧 Outils"),
    ("courses",   "📚 Cours"),
    ("shortcuts", "⚡ Raccourcis"),
    ("spacecode", "💻 SpaceCode"),
    ("hacking",   "🛡️ DevSecurity"),
    ("quiz",      "🧠 Quiz"),
    ("notes",     "📝 Mes Notes"),
    ("grades",    "📊 Moyennes"),
    ("guide",     "📖 Guide"),
    ("profile",   "👤 Profil"),
    ("career",    "🎯 Carrière"),
    ("about",     "ℹ️ À Propos"),
    ("legal",     "⚖️ Légal"),
    ("settings",  "⚙️ Paramètres"),
]

# Raccourcis Ctrl+1…Ctrl+9 pour les 9 premières sections
NAV_SHORTCUTS = {f"<Control-Key-{i+1}>": NAV_SECTIONS[i][0] for i in range(min(9, len(NAV_SECTIONS)))}


# ===========================================================================
# Fenêtre de licence
# ===========================================================================

class LicenseWindow(ctk.CTk):
    """Fenêtre d'activation de la licence avec auto-format et compteur de tentatives."""

    def __init__(self, hwid: str) -> None:
        super().__init__()
        self.hwid             = hwid
        self.result           = False
        self._attempt_count   = 0
        self._key_visible     = False

        self.title(f"{APP_NAME} — Activation")
        self.geometry("620x560")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._set_icon()
        self._build()

    def _set_icon(self) -> None:
        try:
            base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent
            ico = base / "assets" / "Space_logo.ico"
            if ico.exists():
                self.iconbitmap(str(ico))
        except Exception:
            pass

    def _on_close(self) -> None:
        self.result = False
        self.destroy()

    def _build(self) -> None:
        # En-tête
        ctk.CTkLabel(self, text="🔐", font=("Segoe UI Emoji", 48)).pack(pady=(28, 4))
        ctk.CTkLabel(self, text=APP_NAME,
                     font=("Segoe UI", 22, "bold"), text_color="#4fc3f7").pack()
        ctk.CTkLabel(self, text=f"{UNIVERSITE} — {OPTION}",
                     font=("Segoe UI", 11), text_color="#8b949e").pack(pady=(0, 16))

        # HWID
        hwid_f = ctk.CTkFrame(self, fg_color="#1c2128", corner_radius=12)
        hwid_f.pack(padx=40, fill="x", pady=4)
        ctk.CTkLabel(hwid_f, text="Votre HWID (ID Machine) :",
                     font=("Segoe UI", 10), text_color="#8b949e").pack(pady=(10, 2))
        ctk.CTkLabel(hwid_f, text=self.hwid,
                     font=("Courier New", 13, "bold"), text_color="#4fc3f7").pack(pady=(0, 4))
        ctk.CTkButton(hwid_f, text="📋 Copier le HWID",
                      command=self._copy_hwid,
                      fg_color="#21262d", hover_color="#30363d",
                      height=28, font=("Segoe UI", 10)).pack(pady=(0, 10))

        # Contact
        info_f = ctk.CTkFrame(self, fg_color="#1a2f1a", corner_radius=10,
                               border_color="#3fb950", border_width=1)
        info_f.pack(padx=40, fill="x", pady=8)
        ctk.CTkLabel(info_f,
                     text=(f"📱 Contactez {DEV_REAL} sur WhatsApp : {WHATSAPP}\n"
                           "Envoyez votre HWID pour recevoir votre clé d'activation."),
                     font=("Segoe UI", 10), text_color="#3fb950",
                     justify="center").pack(pady=10)

        # Saisie de la clé
        ctk.CTkLabel(self, text="Entrez votre clé d'activation :",
                     font=("Segoe UI", 11), text_color="#e6edf3").pack(pady=(10, 3))

        key_row = ctk.CTkFrame(self, fg_color="transparent")
        key_row.pack()
        self.key_entry = ctk.CTkEntry(key_row,
                                       placeholder_text="XXXXX-XXXXX-XXXXX-XXXXX",
                                       font=("Courier New", 13),
                                       height=42, width=310,
                                       show="•")
        self.key_entry.pack(side="left", padx=(0, 6))
        self.key_entry.bind("<KeyRelease>", self._auto_format_key)
        self.key_entry.bind("<Return>", lambda _: self._verify())

        self._eye_btn = ctk.CTkButton(key_row, text="👁", width=42, height=42,
                                       fg_color="#21262d", hover_color="#30363d",
                                       command=self._toggle_visibility,
                                       font=("Segoe UI Emoji", 14))
        self._eye_btn.pack(side="left")

        # Feedback tentatives
        self._feedback_lbl = ctk.CTkLabel(self, text="",
                                            font=("Segoe UI", 10), text_color="#ef4444")
        self._feedback_lbl.pack(pady=(4, 0))

        # Bouton activer
        self._activate_btn = ctk.CTkButton(self, text="✅  Activer la Licence",
                                            command=self._verify,
                                            fg_color="#1565c0", hover_color="#1976d2",
                                            height=42, font=("Segoe UI", 12, "bold"))
        self._activate_btn.pack(pady=12)

        ctk.CTkLabel(self, text=f"Développé par {DEV_NAME} © {PROMO}",
                     font=("Segoe UI", 9), text_color="#30363d").pack(pady=(0, 10))

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _copy_hwid(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(self.hwid)
        messagebox.showinfo("Copié", "HWID copié dans le presse-papier !")

    def _toggle_visibility(self) -> None:
        self._key_visible = not self._key_visible
        self.key_entry.configure(show="" if self._key_visible else "•")
        self._eye_btn.configure(text="🙈" if self._key_visible else "👁")

    def _auto_format_key(self, _event=None) -> None:
        """Auto-formate la clé en XXXXX-XXXXX-XXXXX-XXXXX pendant la saisie."""
        raw = self.key_entry.get().replace("-", "").upper()
        parts = [raw[i:i+5] for i in range(0, min(len(raw), 20), 5)]
        formatted = "-".join(parts)
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, formatted)

    def _verify(self) -> None:
        if not self._activate_btn.cget("state") == "normal":
            return
        key = self.key_entry.get().strip()
        if not key:
            messagebox.showwarning("Attention", "Veuillez entrer une clé de licence.")
            return

        if verify_license(self.hwid, key):
            save_license(self.hwid, key)
            self.result = True
            AstaLogger.info("Licence activée avec succès.")
            messagebox.showinfo("✅ Activé !", f"Bienvenue dans {APP_NAME} !\nLicence activée avec succès.")
            self.destroy()
        else:
            self._attempt_count += 1
            remaining = MAX_LICENSE_ATTEMPTS - self._attempt_count
            AstaLogger.warning("Tentative d'activation échouée #%d.", self._attempt_count)

            if remaining <= 0:
                self._activate_btn.configure(state="disabled")
                self._feedback_lbl.configure(
                    text="🔒 Trop de tentatives. Relancez l'application."
                )
                messagebox.showerror(
                    "⛔ Bloqué",
                    "Nombre maximum de tentatives atteint.\n"
                    f"Contactez {DEV_REAL} : {WHATSAPP}"
                )
            else:
                self._feedback_lbl.configure(
                    text=f"❌ Clé invalide — {remaining} tentative(s) restante(s)."
                )
                messagebox.showerror(
                    "❌ Clé invalide",
                    f"Cette clé ne correspond pas à votre machine.\n"
                    f"Contactez {DEV_REAL} : {WHATSAPP}\n\n"
                    f"Tentatives restantes : {remaining}"
                )


# ===========================================================================
# Import des Mixins de vues
# ===========================================================================

from views.dashboard_view  import DashboardMixin
from views.oracle_view     import OracleMixin
from views.tools_view      import ToolsMixin
from views.courses_view    import CoursesMixin
from views.shortcuts_view  import ShortcutsMixin
from views.spacecode_view  import SpacecodeMixin
from views.hacking_view    import HackingMixin
from views.quiz_view       import QuizMixin
from views.notes_view      import NotesMixin
from views.grades_view     import GradesMixin
from views.profile_view    import ProfileMixin
from views.career_view     import CareerMixin
from views.about_view      import AboutMixin
from views.settings_view   import SettingsMixin
from views.guide_view      import GuideMixin
from views.legal_view      import LegalMixin


# ===========================================================================
# Application principale
# ===========================================================================

class AstaAcademie(
    ctk.CTk,
    DashboardMixin, OracleMixin, ToolsMixin, CoursesMixin, ShortcutsMixin,
    SpacecodeMixin, HackingMixin, QuizMixin, NotesMixin, GradesMixin,
    ProfileMixin, CareerMixin, AboutMixin, SettingsMixin, GuideMixin, LegalMixin,
):
    def __init__(self) -> None:
        super().__init__()
        AstaLogger.setup()
        AstaLogger.info("Démarrage de %s v%s", APP_NAME, VERSION)

        # ── Profil & langue ──────────────────────────────────────────────────
        self.lang       = "fr"
        self.theme_name = "noir_vert"
        self.C          = COLORS["noir_vert"]
        self.profile    = load_json(
            PROFILE_FILE,
            {"nom": "", "niveau": "L2", "points": 0, "badges": [], "streak": 0},
        )
        # Restaurer le thème sauvegardé
        saved_theme = self.profile.get("theme", "noir_vert")
        if saved_theme in COLORS:
            self.theme_name = saved_theme
            self.C          = COLORS[saved_theme]

        # ── Zoom ─────────────────────────────────────────────────────────────
        self._zoom_levels = [0.8, 0.9, 1.0, 1.1, 1.25, 1.4, 1.6]
        self._zoom_idx    = max(
            0, min(self.profile.get("zoom_idx", 2), len(self._zoom_levels) - 1)
        )

        # ── Pomodoro ─────────────────────────────────────────────────────────
        self.pomodoro_running    = False
        self.pomodoro_time       = POMO_WORK_DEFAULT
        self.pomodoro_mode       = "work"     # "work" | "short_break" | "long_break"
        self._pomo_session_count = 0          # combien de sessions "work" terminées
        self._pomo_work_min      = 25         # configurable
        self._pomo_short_min     = 5
        self._pomo_long_min      = 15

        # ── État de l'app ────────────────────────────────────────────────────
        self.current_quiz_q    = None
        self.selected_note_key = None
        self.grade_entries     = {}
        self.grade_gen_lbl     = None
        self.tab_frames: dict  = {}
        self.current_tab: Optional[str] = None

        # ── Backend Go ──────────────────────────────────────────────────────
        self.backend_process: Optional[subprocess.Popen] = None
        self._start_backend()

        # ── Base de données SQLite ──────────────────────────────────────────
        self._init_database()

        # ── Construction de l'interface ─────────────────────────────────────
        self._setup_window()
        self._build_ui()
        self._show_section("dashboard")
        self._show_splash()
        self._update_streak()
        log_usage("startup")

    # -----------------------------------------------------------------------
    # Initialisation backend & DB
    # -----------------------------------------------------------------------

    def _start_backend(self) -> None:
        """Lance le serveur Go en arrière-plan (non-bloquant)."""
        try:
            backend_dir = BASE_DIR / "backend"
            if getattr(sys, "frozen", False):
                exe = Path(sys._MEIPASS) / "backend" / "asta_backend.exe"
                cmd = [str(exe)]
            else:
                cmd = ["go", "run", "main.go"]

            flags = {}
            if os.name == "nt":
                flags["creationflags"] = subprocess.CREATE_NO_WINDOW

            self.backend_process = subprocess.Popen(
                cmd, cwd=str(backend_dir),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                **flags,
            )
            AstaLogger.info("Backend Go démarré (PID %d).", self.backend_process.pid)
        except FileNotFoundError:
            AstaLogger.warning("Backend Go introuvable — mode hors ligne.")
        except Exception as e:
            AstaLogger.error("Impossible de démarrer le backend : %s", e)

    def _wait_backend_ready(self, timeout: float = 5.0) -> bool:
        """Attend que le backend réponde sur /health (non-bloquant via thread)."""
        import urllib.request
        import time

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                urllib.request.urlopen("http://localhost:8080/health", timeout=0.5)
                return True
            except Exception:
                time.sleep(0.2)
        AstaLogger.warning("Backend non disponible après %.1fs.", timeout)
        return False

    def _init_database(self) -> None:
        """Initialise SQLite et charge l'utilisateur (avec health-check non-bloquant)."""
        # Attente backend en thread séparé pour ne pas bloquer l'UI
        threading.Thread(target=self._wait_backend_ready, daemon=True).start()

        try:
            from database.db_manager import init_database, get_or_create_user, get_quiz_stats, check_user_active
            init_database(DB_FILE)
            nom = self.profile.get("nom", "Étudiant")
            self.user_id = get_or_create_user(DB_FILE, nom)

            if not check_user_active(DB_FILE, self.user_id):
                messagebox.showerror(
                    "Accès Refusé",
                    "Votre compte a été bloqué par l'Administrateur.\nVeuillez le contacter."
                )
                AstaLogger.security(
                    "Tentative de connexion bloquée pour %s (ID %d).", nom, self.user_id
                )
                sys.exit(0)

            hwid = self.profile.get("hwid", "UNKNOWN")
            AstaLogger.set_user_context(self.user_id, nom, hwid)
            AstaLogger.info("Session démarrée pour %s (ID %d).", nom, self.user_id)

            self.quiz_score, self.quiz_total = get_quiz_stats(DB_FILE, self.user_id)
        except SystemExit:
            raise
        except Exception as e:
            AstaLogger.error("Erreur d'initialisation de la base de données : %s", e)
            self.user_id    = 0
            self.quiz_score = 0
            self.quiz_total = 0

    # -----------------------------------------------------------------------
    # Fenêtre principale
    # -----------------------------------------------------------------------

    def _setup_window(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        sc = self._zoom_levels[self._zoom_idx]
        ctk.set_widget_scaling(sc)
        ctk.set_window_scaling(sc)

        self.title(f"{APP_NAME} v{VERSION} — {UNIVERSITE}")
        self.geometry("1200x680")
        self.minsize(900, 600)
        self.configure(fg_color=self.C["bg"])
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._set_window_icon()

    def _set_window_icon(self) -> None:
        try:
            base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent
            ico  = base / "assets" / "Space_logo.ico"
            if ico.exists():
                self.iconbitmap(str(ico))
                return
            png = base / "assets" / "Space_logo_256.png"
            if png.exists():
                img = Image.open(str(png)).resize((64, 64), Image.LANCZOS)
                self._icon_img = ImageTk.PhotoImage(img)
                self.iconphoto(True, self._icon_img)
        except Exception as e:
            AstaLogger.warning("Icône de fenêtre non chargée : %s", e)

    # -----------------------------------------------------------------------
    # Construction de l'UI
    # -----------------------------------------------------------------------

    def _build_ui(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_topbar()
        self._build_sidebar()
        self._build_main_area()
        self._build_statusbar()
        self._setup_global_shortcuts()

    def _setup_global_shortcuts(self) -> None:
        """Raccourcis clavier globaux."""
        # Ctrl+K : ouvrir la recherche globale
        self.bind("<Control-k>", lambda _: self._focus_search())
        self.bind("<Control-f>", lambda _: self._focus_search())
        # Zoom
        self.bind("<Control-equal>", lambda _: self._zoom_in())
        self.bind("<Control-plus>",  lambda _: self._zoom_in())
        self.bind("<Control-minus>", lambda _: self._zoom_out())
        self.bind("<Control-0>",     lambda _: self._zoom_reset())
        # Navigation Ctrl+1…Ctrl+9
        for shortcut, section_key in NAV_SHORTCUTS.items():
            self.bind(shortcut, lambda _, k=section_key: self._show_section(k))

    # ── Topbar ───────────────────────────────────────────────────────────────

    def _build_topbar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=self.C["sidebar"], height=50, corner_radius=0)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        bar.grid_columnconfigure(2, weight=1)

        # Logo + nom
        ctk.CTkLabel(bar, text=f"  🎓 {APP_NAME}",
                     font=("Segoe UI", 14, "bold"),
                     text_color=self.C["accent"]).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(bar, text=f"v{VERSION}",
                     font=("Segoe UI", 9),
                     text_color=self.C["subtext"]).grid(row=0, column=1)

        # Recherche globale (Ctrl+K)
        self.search_var = ctk.StringVar()
        self._search_entry = ctk.CTkEntry(
            bar, textvariable=self.search_var,
            placeholder_text="🔍 Rechercher… (Ctrl+K)",
            width=260, height=32,
            fg_color=self.C["card"],
            border_color=self.C["border"],
        )
        self._search_entry.grid(row=0, column=2, padx=(20, 4))
        self._search_entry.bind("<Return>", self._do_search)
        ctk.CTkButton(
            bar, text="🔍", command=self._do_search,
            width=36, height=32,
            fg_color=self.C["accent"], hover_color=self.C["accent2"],
        ).grid(row=0, column=3, padx=(0, 10))

        # Pomodoro
        self._build_topbar_pomo(bar)

        # Zoom
        zoom_f = ctk.CTkFrame(bar, fg_color="transparent")
        zoom_f.grid(row=0, column=7, padx=(0, 8))
        ctk.CTkButton(zoom_f, text="−", width=26, height=26,
                      command=self._zoom_out,
                      fg_color=self.C["card"], hover_color=self.C["hover"],
                      text_color=self.C["text"], font=("Segoe UI", 13, "bold")
                      ).pack(side="left")
        self._zoom_lbl = ctk.CTkLabel(zoom_f, text=self._zoom_pct(),
                                       font=("Segoe UI", 9),
                                       text_color=self.C["subtext"], width=38)
        self._zoom_lbl.pack(side="left")
        ctk.CTkButton(zoom_f, text="+", width=26, height=26,
                      command=self._zoom_in,
                      fg_color=self.C["card"], hover_color=self.C["hover"],
                      text_color=self.C["text"], font=("Segoe UI", 13, "bold")
                      ).pack(side="left")

        # Indicateur réseau
        self.network_indicator = ctk.CTkLabel(
            bar, text="🟢 Connecté",
            font=("Segoe UI", 11, "bold"), text_color="#10b981",
        )
        self.network_indicator.grid(row=0, column=8, padx=15)

        try:
            from utils.event_bus import EventBus, AppEvents
            EventBus.subscribe(AppEvents.NETWORK_ONLINE,  lambda _: self.network_indicator.configure(text="🟢 Connecté",  text_color="#10b981"))
            EventBus.subscribe(AppEvents.NETWORK_OFFLINE, lambda _: self.network_indicator.configure(text="🔴 Hors ligne", text_color="#ef4444"))
            EventBus.subscribe(AppEvents.SYNC_START,      lambda _: self.network_indicator.configure(text="🟠 Synchro",   text_color="#f59e0b"))
        except Exception as e:
            AstaLogger.warning("EventBus non disponible : %s", e)

    def _build_topbar_pomo(self, bar: ctk.CTkFrame) -> None:
        """Widget Pomodoro dans la topbar."""
        pomo_f = ctk.CTkFrame(bar, fg_color="transparent")
        pomo_f.grid(row=0, column=4, padx=8)

        self.pomo_label = ctk.CTkLabel(
            pomo_f, text="⏱️ 25:00",
            font=("Segoe UI", 11, "bold"), text_color=self.C["accent"],
        )
        self.pomo_label.pack(side="left", padx=(0, 4))

        # Sessions compteur
        self._pomo_session_lbl = ctk.CTkLabel(
            pomo_f, text="🍅×0",
            font=("Segoe UI", 9), text_color=self.C["subtext"],
        )
        self._pomo_session_lbl.pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            pomo_f, text="▶", command=self._pomo_toggle,
            width=28, height=28, fg_color=self.C["accent2"],
        ).pack(side="left")
        ctk.CTkButton(
            pomo_f, text="↺", command=self._pomo_reset,
            width=28, height=28,
            fg_color=self.C["card"], hover_color=self.C["hover"],
        ).pack(side="left", padx=(2, 0))

    # ── Sidebar ──────────────────────────────────────────────────────────────

    def _build_sidebar(self) -> None:
        self.sidebar = ctk.CTkScrollableFrame(
            self, fg_color=self.C["sidebar"], width=200, corner_radius=0
        )
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        # Logo
        logo_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_f.pack(fill="x", pady=(14, 4), padx=10)
        try:
            png = BASE_DIR / "assets" / "Space_logo_256.png"
            if png.exists():
                img = ctk.CTkImage(Image.open(str(png)), size=(64, 64))
                ctk.CTkLabel(logo_f, image=img, text="").pack(pady=(0, 4))
            else:
                ctk.CTkLabel(logo_f, text="🎓", font=("Segoe UI", 44)).pack(pady=(0, 4))
        except Exception:
            ctk.CTkLabel(logo_f, text="🎓", font=("Segoe UI", 44)).pack(pady=(0, 4))

        # Nom de l'utilisateur
        nom = self.profile.get("nom", "Étudiant")
        ctk.CTkLabel(logo_f, text=nom,
                     font=("Segoe UI", 11, "bold"),
                     text_color=self.C["accent"]).pack()
        ctk.CTkLabel(logo_f, text=OPTION,
                     font=("Segoe UI", 8),
                     text_color=self.C["subtext"]).pack()

        # Miniature des stats : streak + points + niveau
        stats_f = ctk.CTkFrame(logo_f, fg_color=self.C.get("card", "#161b22"), corner_radius=8)
        stats_f.pack(fill="x", pady=(6, 0))
        streak = self.profile.get("streak", 0)
        points = self.profile.get("points", 0)
        niveau = self.profile.get("niveau", "L2")
        row_f = ctk.CTkFrame(stats_f, fg_color="transparent")
        row_f.pack(pady=6)
        for icon, val in [("🔥", str(streak)), ("⭐", str(points)), ("📚", niveau)]:
            col = ctk.CTkFrame(row_f, fg_color="transparent")
            col.pack(side="left", padx=8)
            ctk.CTkLabel(col, text=icon, font=("Segoe UI Emoji", 14)).pack()
            ctk.CTkLabel(col, text=val,
                         font=("Segoe UI", 10, "bold"),
                         text_color=self.C["accent"]).pack()

        # Séparateur
        ctk.CTkLabel(self.sidebar, text="─" * 23,
                     text_color=self.C["border"]).pack(pady=(6, 0))

        # Boutons de navigation
        self.nav_buttons: dict = {}
        for key, label in NAV_SECTIONS:
            btn = ctk.CTkButton(
                self.sidebar, text=label,
                command=lambda k=key: self._show_section(k),
                anchor="w", height=36, corner_radius=8,
                fg_color="transparent",
                hover_color=self.C["hover"],
                text_color=self.C["text"],
                font=("Segoe UI", 11),
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.nav_buttons[key] = btn

        # Pied de sidebar
        ctk.CTkLabel(self.sidebar, text="─" * 23,
                     text_color=self.C["border"]).pack(pady=(8, 0))
        ctk.CTkLabel(self.sidebar,
                     text=f"Dev: {DEV_NAME}\nPromo {PROMO}",
                     font=("Segoe UI", 8),
                     text_color=self.C["subtext"],
                     justify="center").pack(pady=4)

    # ── Zone principale ──────────────────────────────────────────────────────

    def _build_main_area(self) -> None:
        self.main_area = ctk.CTkFrame(self, fg_color=self.C["bg"], corner_radius=0)
        self.main_area.grid(row=1, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

    # ── Barre de statut ──────────────────────────────────────────────────────

    def _build_statusbar(self) -> None:
        self.statusbar = ctk.CTkFrame(self, fg_color=self.C["sidebar"],
                                       height=28, corner_radius=0)
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.statusbar.grid_columnconfigure(4, weight=1)

        self.status_time = ctk.CTkLabel(self.statusbar, text="",
                                         font=("Segoe UI", 9), text_color=self.C["subtext"])
        self.status_time.grid(row=0, column=0, padx=10)

        self.status_niveau = ctk.CTkLabel(
            self.statusbar,
            text=f"Niveau : {self.profile.get('niveau', 'L2')}",
            font=("Segoe UI", 9), text_color=self.C["accent"],
        )
        self.status_niveau.grid(row=0, column=1, padx=10)

        self.status_points = ctk.CTkLabel(
            self.statusbar,
            text=f"⭐ {self.profile.get('points', 0)} pts",
            font=("Segoe UI", 9), text_color=self.C.get("warning", "#f59e0b"),
        )
        self.status_points.grid(row=0, column=2, padx=10)

        self.status_streak = ctk.CTkLabel(
            self.statusbar,
            text=f"🔥 Streak : {self.profile.get('streak', 0)}j",
            font=("Segoe UI", 9), text_color=self.C.get("warning", "#f59e0b"),
        )
        self.status_streak.grid(row=0, column=3, padx=10)

        ctk.CTkLabel(
            self.statusbar,
            text=f"{APP_NAME} — {UNIVERSITE} | {DEV_NAME}",
            font=("Segoe UI", 9), text_color=self.C["subtext"],
        ).grid(row=0, column=5, padx=10)

        self._update_clock()

    def _refresh_statusbar(self) -> None:
        """Met à jour les métriques dynamiques de la barre de statut."""
        try:
            self.status_niveau.configure(text=f"Niveau : {self.profile.get('niveau', 'L2')}")
            self.status_points.configure(text=f"⭐ {self.profile.get('points', 0)} pts")
            self.status_streak.configure(text=f"🔥 Streak : {self.profile.get('streak', 0)}j")
        except Exception as e:
            AstaLogger.warning("_refresh_statusbar : %s", e)

    # -----------------------------------------------------------------------
    # Navigation entre sections
    # -----------------------------------------------------------------------

    def _show_section(self, key: str) -> None:
        # Mise en évidence du bouton actif
        for k, btn in self.nav_buttons.items():
            btn.configure(
                fg_color=self.C["accent"] if k == key else "transparent",
                text_color="#ffffff"       if k == key else self.C["text"],
            )

        # Masquer l'onglet courant
        if self.current_tab and self.current_tab in self.tab_frames:
            self.tab_frames[self.current_tab].grid_remove()

        dispatch = {
            "dashboard": self._build_dashboard,
            "oracle":    self._build_oracle,
            "tools":     self._build_tools,
            "courses":   self._build_courses,
            "shortcuts": self._build_shortcuts,
            "hacking":   self._build_hacking,
            "spacecode": self._build_spacecode,
            "quiz":      self._build_quiz,
            "notes":     self._build_notes,
            "grades":    self._build_grades,
            "guide":     self._build_guide,
            "profile":   self._build_profile,
            "career":    self._build_career,
            "about":     self._build_about,
            "legal":     self._build_legal,
            "settings":  self._build_settings,
        }

        # Construire l'onglet s'il n'existe pas encore (cache)
        if key not in self.tab_frames and key in dispatch:
            tab_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
            tab_frame.grid(row=0, column=0, sticky="nsew")
            tab_frame.grid_columnconfigure(0, weight=1)
            tab_frame.grid_rowconfigure(0, weight=1)

            old_main = self.main_area
            self.main_area = tab_frame
            try:
                dispatch[key]()
            except Exception as e:
                AstaLogger.error("Erreur lors de la construction de la section '%s' : %s\n%s",
                                 key, e, traceback.format_exc())
            finally:
                self.main_area = old_main
            self.tab_frames[key] = tab_frame

        # Afficher depuis le cache
        if key in self.tab_frames:
            self.tab_frames[key].grid(row=0, column=0, sticky="nsew")
            self.current_tab = key
            if hasattr(self, "_on_tab_show"):
                self._on_tab_show(key)

        AstaLogger.info("Section affichée : '%s'", key)

    # -----------------------------------------------------------------------
    # Helpers de construction de l'UI
    # -----------------------------------------------------------------------

    def _focus_search(self) -> None:
        """Donne le focus à la barre de recherche globale."""
        self._search_entry.focus_set()
        self._search_entry.select_range(0, "end")

    def L(self, key: str) -> str:
        return get_translation(self.lang).get(key, key)

    def _scrollable_frame(self) -> ctk.CTkScrollableFrame:
        f = ctk.CTkScrollableFrame(self.main_area, fg_color=self.C["bg"])
        f.grid(row=0, column=0, sticky="nsew")
        f.grid_columnconfigure(0, weight=1)
        return f

    def _section_header(self, parent, title: str, subtitle: str = "") -> None:
        ctk.CTkLabel(parent, text=title,
                     font=("Segoe UI", 18, "bold"),
                     text_color=self.C["accent"]).pack(anchor="w", padx=20, pady=(15, 2))
        if subtitle:
            ctk.CTkLabel(parent, text=subtitle,
                         font=("Segoe UI", 10),
                         text_color=self.C["subtext"]).pack(anchor="w", padx=22, pady=(0, 10))

    def _card(self, parent, bg=None) -> ctk.CTkFrame:
        f = ctk.CTkFrame(
            parent,
            fg_color=bg or self.C["card"],
            corner_radius=14,
            border_color=self.C["border"],
            border_width=1,
        )
        f.pack(fill="x", padx=20, pady=8)
        return f

    # -----------------------------------------------------------------------
    # Section SpaceCode (maintenance)
    # -----------------------------------------------------------------------

    def _build_spacecode(self) -> None:
        frame = self._scrollable_frame()
        self._section_header(frame, "🚀 SpaceCode Studio", "IDE Asta Académie (En maintenance)")
        card = self._card(frame)
        ctk.CTkLabel(card, text="⚙️", font=("Segoe UI", 72)).pack(pady=(28, 8))
        ctk.CTkLabel(card, text="MODULE EN MAINTENANCE",
                     font=("Segoe UI", 22, "bold"), text_color=self.C["accent"]).pack()
        ctk.CTkLabel(
            card,
            text=(
                "L'éditeur SpaceCode Studio est en cours de réécriture pour la V2.\n"
                "Nouveau moteur de coloration syntaxique + exécution asynchrone.\n\n"
                "Merci de votre patience !"
            ),
            font=("Segoe UI", 12), text_color=self.C["subtext"], justify="center",
        ).pack(pady=(4, 28))

    # -----------------------------------------------------------------------
    # Splash screen
    # -----------------------------------------------------------------------

    def _show_splash(self) -> None:
        splash = ctk.CTkToplevel(self)
        splash.title("")
        splash.geometry("480x300")
        splash.resizable(False, False)
        splash.configure(fg_color="#0d1117")
        splash.grab_set()
        splash.overrideredirect(True)

        splash.update_idletasks()
        x = (splash.winfo_screenwidth()  - 480) // 2
        y = (splash.winfo_screenheight() - 300) // 2
        splash.geometry(f"480x300+{x}+{y}")

        # Logo
        try:
            png = BASE_DIR / "assets" / "Space_logo_256.png"
            if png.exists():
                logo = ctk.CTkImage(Image.open(str(png)), size=(110, 110))
                ctk.CTkLabel(splash, image=logo, text="").pack(pady=(18, 4))
            else:
                ctk.CTkLabel(splash, text="🎓", font=("Segoe UI", 52)).pack(pady=(24, 4))
        except Exception:
            ctk.CTkLabel(splash, text="🎓", font=("Segoe UI", 52)).pack(pady=(24, 4))

        ctk.CTkLabel(splash, text=APP_NAME,
                     font=("Segoe UI", 22, "bold"), text_color="#4fc3f7").pack()
        ctk.CTkLabel(splash, text=f"{UNIVERSITE} — {OPTION}",
                     font=("Segoe UI", 10), text_color="#8b949e").pack()

        bar = ctk.CTkProgressBar(splash, width=380, progress_color="#4fc3f7")
        bar.set(0)
        bar.pack(pady=14)

        tip_lbl = ctk.CTkLabel(splash, text=SPLASH_TIPS[0],
                                font=("Segoe UI", 9), text_color="#8b949e")
        tip_lbl.pack()

        step = 100 // max(len(SPLASH_TIPS), 1)

        def animate(i: int = 0) -> None:
            if i <= 100:
                bar.set(i / 100)
                tip_idx = min(i // step, len(SPLASH_TIPS) - 1)
                tip_lbl.configure(text=SPLASH_TIPS[tip_idx])
                splash.after(16, animate, i + 2)
            else:
                splash.destroy()

        animate()

    # -----------------------------------------------------------------------
    # Streak quotidien
    # -----------------------------------------------------------------------

    def _update_streak(self) -> None:
        """Met à jour le streak et attribue les badges multi-niveaux."""
        try:
            today     = datetime.now().date()
            yesterday = today - timedelta(days=1)    # ✅ corrigé (plus de crash 1er du mois)

            today_str     = today.strftime("%Y-%m-%d")
            yesterday_str = yesterday.strftime("%Y-%m-%d")
            last_date     = self.profile.get("last_launch_date", "")
            streak        = self.profile.get("streak", 0)

            if last_date == today_str:
                return  # déjà lancé aujourd'hui

            streak = (streak + 1) if last_date == yesterday_str else 1

            self.profile["streak"]             = streak
            self.profile["last_launch_date"]   = today_str

            # Badges multi-niveaux
            badges = self.profile.setdefault("badges", [])
            for threshold, badge_name in STREAK_BADGES:
                if streak >= threshold and badge_name not in badges:
                    badges.append(badge_name)
                    AstaLogger.info("Badge débloqué : %s", badge_name)

            save_json(PROFILE_FILE, self.profile)
            self._refresh_statusbar()
        except Exception as e:
            AstaLogger.error("_update_streak : %s", e)

    # -----------------------------------------------------------------------
    # Fermeture propre
    # -----------------------------------------------------------------------

    def _on_close(self) -> None:
        """Fermeture propre : sauvegarde, arrêt du backend, destruction de la fenêtre."""
        self.pomodoro_running = False

        # Sauvegarde automatique
        try:
            save_json(PROFILE_FILE, self.profile)
        except Exception as e:
            AstaLogger.error("Sauvegarde du profil échouée : %s", e)

        try:
            save_json(NOTES_FILE, getattr(self, "notes_data", {}))
        except Exception as e:
            AstaLogger.error("Sauvegarde des notes échouée : %s", e)

        # Arrêt du backend Go
        if self.backend_process and self.backend_process.poll() is None:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=3)
                AstaLogger.info("Backend Go terminé proprement.")
            except Exception as e:
                AstaLogger.warning("Arrêt du backend : %s", e)
                try:
                    self.backend_process.kill()
                except Exception:
                    pass

        AstaLogger.info("Fermeture de %s.", APP_NAME)

        try:
            self.destroy()
        except Exception:
            pass
        # Pas d'os._exit(0) — on laisse Python terminer normalement

    # -----------------------------------------------------------------------
    # Pomodoro
    # -----------------------------------------------------------------------

    def _pomo_toggle(self) -> None:
        self.pomodoro_running = not self.pomodoro_running
        if self.pomodoro_running:
            self._pomo_tick()

    def _pomo_reset(self) -> None:
        self.pomodoro_running    = False
        self.pomodoro_time       = self._pomo_work_min * 60
        self.pomodoro_mode       = "work"
        self._pomo_session_count = 0
        self.pomo_label.configure(
            text=f"⏱️ {self._pomo_work_min:02d}:00",
            text_color=self.C["accent"],
        )
        self._pomo_session_lbl.configure(text="🍅×0")

    def _pomo_tick(self) -> None:
        if not self.pomodoro_running:
            return
        try:
            if not self.winfo_exists() or not self.pomo_label.winfo_exists():
                return
        except Exception:
            return

        if self.pomodoro_time > 0:
            self.pomodoro_time -= 1
            m, s = divmod(self.pomodoro_time, 60)

            # Couleur par mode
            colors = {
                "work":        self.C.get("success", "#10b981"),
                "short_break": self.C.get("warning", "#f59e0b"),
                "long_break":  self.C.get("accent",  "#4fc3f7"),
            }
            self.pomo_label.configure(
                text=f"⏱️ {m:02d}:{s:02d}",
                text_color=colors.get(self.pomodoro_mode, self.C["accent"]),
            )
            self.after(1000, self._pomo_tick)
        else:
            self._pomo_next_phase()

    def _pomo_next_phase(self) -> None:
        """Gère les transitions work → courte pause → (longue pause toutes les N sessions)."""
        if self.pomodoro_mode == "work":
            self._pomo_session_count += 1
            self._pomo_session_lbl.configure(text=f"🍅×{self._pomo_session_count}")

            if self._pomo_session_count % POMO_SESSIONS_BEFORE_LONG == 0:
                self.pomodoro_mode  = "long_break"
                self.pomodoro_time  = self._pomo_long_min * 60
                msg = f"🌿 Grande pause ! {self._pomo_long_min} minutes de repos bien mérité."
            else:
                self.pomodoro_mode  = "short_break"
                self.pomodoro_time  = self._pomo_short_min * 60
                msg = f"☕ Courte pause ! {self._pomo_short_min} minutes."

            messagebox.showinfo("⏱️ Pomodoro", msg)

        else:
            # Fin de la pause → reprise du travail
            self.pomodoro_mode  = "work"
            self.pomodoro_time  = self._pomo_work_min * 60
            messagebox.showinfo("⏱️ Pomodoro", f"💪 C'est reparti ! {self._pomo_work_min} minutes de travail.")

        self._pomo_tick()

    # -----------------------------------------------------------------------
    # Recherche globale (bug de closure corrigé)
    # -----------------------------------------------------------------------

    def _do_search(self, _event=None) -> None:
        query = self.search_var.get().strip().lower()
        if not query:
            return

        AstaLogger.info("Recherche globale : '%s'", query)
        results: list[dict] = []

        # Raccourcis Excel
        for s in EXCEL_SHORTCUTS:
            if query in s["key"].lower() or query in s["action"].lower():
                results.append({
                    "category": "⚡ Raccourcis",
                    "text":     f"[Excel] {s['key']} → {s['action']}",
                    "section":  "shortcuts",
                })

        # Commandes Linux
        for c in LINUX_COMMANDS:
            if query in c["cmd"].lower() or query in c["description"].lower():
                results.append({
                    "category": "🔧 Outils",
                    "text":     f"[Linux] {c['cmd']} → {c['description']}",
                    "section":  "tools",
                })

        # Pièges profs
        for t in PROF_TRAPS:
            if query in t["piege"].lower() or query in t["matiere"].lower():
                results.append({
                    "category": "🔮 Oracle",
                    "text":     f"[Piège] [{t['matiere']}] {t['piege']}",
                    "section":  "oracle",
                })

        # Cours
        for niveau, ndata in PROGRAMME_COMPLET.items():
            for matiere in ndata.get("cours", {}):
                if query in matiere.lower():
                    results.append({
                        "category": "📚 Cours",
                        "text":     f"[Cours] {niveau} → {matiere}",
                        "section":  "courses",
                    })

        # Notes SQLite — ✅ closure fixée avec argument par défaut
        if hasattr(self, "user_id"):
            try:
                from database.db_manager import get_notes
                for n in get_notes(DB_FILE, self.user_id):
                    if query in n["titre"].lower() or query in n["contenu"].lower():
                        results.append({
                            "category": "📝 Notes",
                            "text":     f"[Note] {n['titre']}",
                            "section":  "notes",
                            "note_id":  n["id"],
                        })
            except Exception as e:
                AstaLogger.warning("Recherche dans les notes : %s", e)

        # Missions CTF
        for m in getattr(self, "ctf_missions", []):
            if query in m.get("title", "").lower() or query in m.get("desc", "").lower():
                results.append({
                    "category": "🛡️ Hacking",
                    "text":     f"[Mission CTF] {m['title']}",
                    "section":  "hacking",
                })

        AstaLogger.info("Résultats trouvés : %d", len(results))
        self._show_search_results(query, results)

    def _show_search_results(self, query: str, results: list[dict]) -> None:
        win = ctk.CTkToplevel(self)
        win.title(f"Résultats pour : {query}")
        win.geometry("680x520")
        win.configure(fg_color=self.C["bg"])
        win.grab_set()

        win.update_idletasks()
        x = (win.winfo_screenwidth()  - 680) // 2
        y = (win.winfo_screenheight() - 520) // 2
        win.geometry(f"680x520+{x}+{y}")

        ctk.CTkLabel(
            win,
            text=f"🔍 Résultats pour « {query} » — {len(results)} trouvé(s)",
            font=("Segoe UI", 15, "bold"), text_color=self.C["accent"],
        ).pack(pady=14)

        scr = ctk.CTkScrollableFrame(win, fg_color=self.C["bg"])
        scr.pack(fill="both", expand=True, padx=14, pady=4)

        if results:
            current_cat = None
            for r in results:
                cat = r.get("category", "")
                if cat != current_cat:
                    current_cat = cat
                    ctk.CTkLabel(scr, text=cat,
                                 font=("Segoe UI", 10, "bold"),
                                 text_color=self.C["subtext"]).pack(anchor="w", padx=8, pady=(8, 2))

                # ✅ closure fixée : on capture section et note_id dans les defaults
                def make_action(section: str, note_id: Optional[int] = None):
                    def action():
                        win.destroy()
                        self._show_section(section)
                        if note_id is not None and hasattr(self, "_note_load"):
                            self.after(100, lambda: self._note_load(note_id))
                    return action

                btn = ctk.CTkButton(
                    scr, text=r["text"],
                    font=("Segoe UI", 11),
                    fg_color=self.C["card"], hover_color=self.C["hover"],
                    text_color=self.C["text"], anchor="w",
                    command=make_action(r["section"], r.get("note_id")),
                )
                btn.pack(fill="x", padx=8, pady=3)
        else:
            ctk.CTkLabel(scr,
                         text="🔍 Aucun résultat trouvé dans l'application.",
                         text_color=self.C["subtext"],
                         font=("Segoe UI", 12)).pack(pady=40)

        ctk.CTkButton(win, text="✖ Fermer", command=win.destroy,
                      fg_color=self.C.get("danger", "#ef4444"),
                      hover_color="#ff0000").pack(pady=12)

    # -----------------------------------------------------------------------
    # Thème & langue
    # -----------------------------------------------------------------------

    def _change_theme(self, val: str) -> None:
        mapping = {
            "⬜ Blanc & Noir":  "noir_blanc_1",
            "⬛ Noir & Blanc":  "noir_blanc_2",
            "🟢 Noir & Vert":   "noir_vert",
            "🔴 Rouge & Noir":  "rouge_noir",
            "🔵 Bleu Nuit":     "bleu_nuit",
            "🟣 Violet Cyber":  "violet_cyber",
            "🟠 Orange Feu":    "orange_feu",
            "🌸 Rose Néon":     "rose_neon",
            "🌊 Océan":         "ocean",
        }
        key = mapping.get(val, "noir_vert")
        if key not in COLORS:
            AstaLogger.warning("Thème inconnu : '%s'", key)
            return

        self.theme_name = key
        self.C          = COLORS[key]
        self.profile["theme"] = key
        save_json(PROFILE_FILE, self.profile)

        try:
            self.sidebar.configure(fg_color=self.C["sidebar"])
            self.main_area.configure(fg_color=self.C["bg"])
            self.configure(fg_color=self.C["bg"])
            if hasattr(self, "statusbar"):
                self.statusbar.configure(fg_color=self.C["sidebar"])
            for w in self.grid_slaves(row=0, column=0):
                if isinstance(w, ctk.CTkFrame):
                    w.configure(fg_color=self.C["sidebar"])
        except Exception as e:
            AstaLogger.warning("Mise à jour partielle du thème : %s", e)

        AstaLogger.info("Thème changé → '%s'", key)
        self._show_section("settings")

    def _toggle_lang(self, choice: Optional[str] = None) -> None:
        if choice:
            self.lang = "kr" if "Krey" in choice else ("en" if "Eng" in choice else "fr")
        else:
            self.lang = "kr" if self.lang == "fr" else "fr"

        try:
            for key, btn in self.nav_buttons.items():
                btn.configure(text=self.L(key))
        except Exception as e:
            AstaLogger.warning("_toggle_lang : %s", e)

        # Reconstruire toutes les vues pour appliquer la traduction
        for f in list(self.tab_frames.values()):
            f.destroy()
        self.tab_frames.clear()
        self._show_section(self.current_tab or "dashboard")

    # -----------------------------------------------------------------------
    # Zoom
    # -----------------------------------------------------------------------

    def _zoom_pct(self) -> str:
        return f"{int(self._zoom_levels[self._zoom_idx] * 100)}%"

    def _apply_zoom(self) -> None:
        sc = self._zoom_levels[self._zoom_idx]
        ctk.set_widget_scaling(sc)
        ctk.set_window_scaling(sc)
        try:
            self._zoom_lbl.configure(text=self._zoom_pct())
        except Exception:
            pass
        try:
            self._settings_zoom_lbl.configure(text=f"Zoom : {self._zoom_pct()}")
        except Exception:
            pass
        self.profile["zoom_idx"] = self._zoom_idx
        save_json(PROFILE_FILE, self.profile)

    def _zoom_in(self) -> None:
        if self._zoom_idx < len(self._zoom_levels) - 1:
            self._zoom_idx += 1
            self._apply_zoom()

    def _zoom_out(self) -> None:
        if self._zoom_idx > 0:
            self._zoom_idx -= 1
            self._apply_zoom()

    def _zoom_reset(self) -> None:
        self._zoom_idx = 2   # 100%
        self._apply_zoom()

    # -----------------------------------------------------------------------
    # Horloge
    # -----------------------------------------------------------------------

    def _update_clock(self) -> None:
        try:
            if not self.winfo_exists():
                return
            self.status_time.configure(text=datetime.now().strftime("%d/%m/%Y  %H:%M:%S"))
            self.after(1000, self._update_clock)
        except Exception:
            pass

    # -----------------------------------------------------------------------
    # Easter eggs
    # -----------------------------------------------------------------------

    def _check_easter_egg(self, _event=None) -> None:
        code = self.egg_entry.get().strip().lower()
        secrets = {
            "luckyluke": (
                f"🎉 FÉLICITATIONS !\n\n"
                f"Tu as trouvé l'Easter Egg secret !\n\n"
                f"« {APP_NAME} » a été entièrement conçu et développé par\n"
                f"{DEV_REAL} aka {DEV_NAME}\n"
                f"Promotion {PROMO} — {UNIVERSITE}\n\n"
                f"🇭🇹 Fait en Haïti, pour les Haïtiens 🇭🇹\n\n"
                f"Le premier outil éducatif de son genre en Haïti 🚀"
            ),
            "astaadev": "🔥 Mode Développeur Activé ! Salut, Space !",
            "unasmoh":  f"🏛️ Vive {FULL_UNI} !\nL'excellence académique au service de la nation haïtienne 🇭🇹",
            "haiti":    "🇭🇹 Liberté · Égalité · Fraternité — Dessalines vit ! 🇭🇹",
        }
        if code in secrets:
            AstaLogger.info("Easter egg découvert : '%s'", code)
            messagebox.showinfo("🥚 Easter Egg !", secrets[code])
        else:
            messagebox.showwarning("🥚 Easter Egg", "Code incorrect. Continue de chercher… 🔍")

    # -----------------------------------------------------------------------
    # Gestion des mises à jour
    # -----------------------------------------------------------------------

    def _load_update(self) -> None:
        path = filedialog.askopenfilename(
            filetypes=[("Asta Update", "*.astaupdate"), ("Tous fichiers", "*.*")]
        )
        if not path:
            return
        is_valid, message, update_data = verify_update_file(path)
        if is_valid:
            app_dir = os.path.dirname(
                sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)
            )
            success, msg = apply_update(update_data, app_dir)
            if success:
                messagebox.showinfo("✅ Mise à Jour", msg + "\nRedémarrez l'application.")
            else:
                messagebox.showerror("❌ Erreur", msg)
        else:
            messagebox.showerror("❌ Erreur", message)

    # -----------------------------------------------------------------------
    # Export / Import / Reset du profil
    # -----------------------------------------------------------------------

    def _export_profile(self) -> None:
        nom = self.profile.get("nom", "user").replace(" ", "_")
        path = filedialog.asksaveasfilename(
            defaultextension=".asta_save",
            filetypes=[("Sauvegarde Asta Académie", "*.asta_save")],
            initialfile=f"sauvegarde_{nom}.asta_save",
        )
        if not path:
            return
        try:
            data = {
                "version":  VERSION,
                "exported": datetime.now().isoformat(),
                "profile":  self.profile,
                "notes":    getattr(self, "notes_data", {}),
            }
            Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            AstaLogger.info("Profil exporté vers '%s'.", path)
            messagebox.showinfo("✅ Exporté", f"Profil exporté vers :\n{path}")
        except Exception as e:
            AstaLogger.error("Export du profil : %s", e)
            messagebox.showerror("❌ Erreur", str(e))

    def _import_profile(self) -> None:
        path = filedialog.askopenfilename(
            filetypes=[("Sauvegarde Asta", "*.asta_save"), ("JSON", "*.json"), ("Tous", "*.*")]
        )
        if not path:
            return
        try:
            raw = Path(path).read_bytes()
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                text = raw.decode("latin-1")

            data = json.loads(text)
            if "profile" not in data and "notes" not in data:
                messagebox.showerror("❌ Erreur", "Ce fichier n'est pas un profil Asta Académie valide.")
                return

            imported_nom = data.get("profile", {}).get("nom", "?")
            from tkinter import messagebox as mb
            if not mb.askyesno("Confirmer l'import",
                               f"Importer le profil de « {imported_nom} » ?\n"
                               "Vos données actuelles seront remplacées."):
                return

            self.profile = data.get("profile", self.profile)
            self.notes_data = data.get("notes", getattr(self, "notes_data", {}))

            # Ensure required keys
            for k, default in [("nom", ""), ("niveau", "L2"), ("points", 0), ("badges", []), ("streak", 0)]:
                self.profile.setdefault(k, default)

            save_json(PROFILE_FILE, self.profile)
            save_json(NOTES_FILE, self.notes_data)
            self._refresh_statusbar()

            AstaLogger.info("Profil importé depuis '%s' (version %s).", path, data.get("version", "?"))
            messagebox.showinfo("✅ Importé",
                                f"Profil de {self.profile.get('nom', '?')} importé avec succès !")
        except json.JSONDecodeError:
            messagebox.showerror("❌ Erreur", "Fichier JSON corrompu ou invalide.")
        except Exception as e:
            AstaLogger.error("Import du profil : %s", e)
            messagebox.showerror("❌ Erreur", f"Impossible d'importer : {e}")

    def _reset_all(self) -> None:
        from tkinter import simpledialog
        confirm = simpledialog.askstring(
            "⚠️ Réinitialisation",
            "Pour confirmer, tapez exactement SUPPRIMER :",
        )
        if confirm != "SUPPRIMER":
            messagebox.showinfo("Annulé", "Réinitialisation annulée.")
            return

        self.profile    = {"nom": "", "niveau": "L2", "points": 0, "badges": [], "streak": 0}
        self.notes_data = {}
        save_json(PROFILE_FILE, self.profile)
        save_json(NOTES_FILE, {})
        self._refresh_statusbar()
        AstaLogger.warning("Réinitialisation complète des données utilisateur.")
        messagebox.showinfo("✅ Réinitialisé", "Toutes les données ont été effacées.")

    # -----------------------------------------------------------------------
    # Navigation directe vers une note
    # -----------------------------------------------------------------------

    def _nav_to_note(self, note_id: int) -> None:
        self._show_section("notes")
        if hasattr(self, "_note_load"):
            self.after(100, lambda: self._note_load(note_id))


# ===========================================================================
# Gestionnaire d'exceptions globales
# ===========================================================================

def global_exception_handler(exc_type, exc_value, exc_traceback) -> None:
    err_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    log_file = DATA_DIR / "crash_log.txt"
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] CRASH FATAL\n{err_msg}\n{'─' * 60}\n")
        AstaLogger.critical("Crash fatal : %s", err_msg[:200])
        messagebox.showerror(
            "Erreur Fatale",
            f"Une erreur inattendue s'est produite.\n"
            f"Rapport enregistré dans :\n{log_file}\n\n"
            f"Erreur : {exc_value}",
        )
    except Exception:
        pass  # Dernier recours : on ne peut rien faire de plus
    sys.exit(1)


sys.excepthook = global_exception_handler


# ==========================================
# MEMOIRE PERSISTANTE
# ==========================================
MEMOIRE_FILE = "SpaceAI_memoire.json"

def charger_memoire():
    if os.path.exists(MEMOIRE_FILE):
        try:
            with open(MEMOIRE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def sauvegarder_memoire(memoire):
    try:
        with open(MEMOIRE_FILE, "w", encoding="utf-8") as f:
            json.dump(memoire, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erreur sauvegarde memoire : {e}")

def ajouter_memoire(cle, valeur):
    memoire      = charger_memoire()
    memoire[cle] = {"valeur": valeur, "timestamp": time.strftime("%d/%m/%Y %H:%M")}
    sauvegarder_memoire(memoire)

def supprimer_memoire(cle):
    memoire = charger_memoire()
    if cle in memoire:
        del memoire[cle]
        sauvegarder_memoire(memoire)
        return True
    return False

def construire_contexte_memoire():
    memoire = charger_memoire()
    if not memoire:
        return ""
    lignes = ["MEMOIRE PERSISTANTE :"]
    for cle, data in memoire.items():
        lignes.append(f"  - {cle} : {data['valeur']} (note le {data['timestamp']})")
    return "\n".join(lignes)

# ==========================================
# HISTORIQUE CONVERSATIONS PERSISTANT
# ==========================================
HISTORIQUE_CONV_FILE = "SpaceAI_conversations.json"
MAX_ECHANGES_FICHIER = 200   # max échanges stockés sur disque
MAX_ECHANGES_CHARGE  = 30    # échanges rechargés au démarrage (contexte IA)

def _sauvegarder_echange_conv(user_text: str, model_text: str):
    """Ajoute un échange user/model au fichier JSON persistant."""
    try:
        echanges = []
        if os.path.exists(HISTORIQUE_CONV_FILE):
            with open(HISTORIQUE_CONV_FILE, "r", encoding="utf-8") as f:
                echanges = json.load(f)
        echanges.append({
            "date":  time.strftime("%d/%m/%Y"),
            "heure": time.strftime("%H:%M"),
            "user":  user_text[:2000],
            "model": model_text[:3000],
        })
        if len(echanges) > MAX_ECHANGES_FICHIER:
            echanges = echanges[-MAX_ECHANGES_FICHIER:]
        with open(HISTORIQUE_CONV_FILE, "w", encoding="utf-8") as f:
            json.dump(echanges, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[CONV] Erreur sauvegarde historique: {e}")

def _charger_historique_recent():
    """Charge les derniers échanges et retourne une liste types.Content."""
    if not os.path.exists(HISTORIQUE_CONV_FILE):
        return []
    try:
        with open(HISTORIQUE_CONV_FILE, "r", encoding="utf-8") as f:
            echanges = json.load(f)
        recents = echanges[-MAX_ECHANGES_CHARGE:]
        hist = []
        for e in recents:
            date_str = f"[{e.get('date','?')} {e.get('heure','?')}] "
            hist.append(types.Content(role="user",  parts=[types.Part(text=date_str + e["user"])]))
            hist.append(types.Content(role="model", parts=[types.Part(text=e["model"])]))
        print(f"[CONV] {len(recents)} echanges passes rechargees en memoire.")
        return hist
    except Exception as e:
        print(f"[CONV] Erreur chargement historique: {e}")
        return []

# ==========================================
# MODE BOULOT
# ==========================================

def _boulot_trouver_exe(noms_exe: list, chemins_hints: list = None) -> str:
    """Trouve un exécutable sur n'importe quel Windows.
    Ordre : registre App Paths → PATH système → chemins connus."""
    # 1. Registre Windows (le plus fiable — tous les apps installées y sont)
    try:
        import winreg
        for exe in noms_exe:
            for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                try:
                    key = winreg.OpenKey(
                        hive,
                        f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\{exe}"
                    )
                    path, _ = winreg.QueryValueEx(key, "")
                    winreg.CloseKey(key)
                    p = os.path.expandvars(path.strip('"'))
                    if os.path.exists(p):
                        return p
                except Exception:
                    pass
    except ImportError:
        pass

    # 2. PATH système
    for exe in noms_exe:
        found = shutil.which(exe)
        if found:
            return found

    # 3. Chemins connus communs
    if chemins_hints:
        for hint in chemins_hints:
            p = os.path.expandvars(hint)
            if os.path.exists(p):
                return p

    return ""


def _boulot_lancer(label: str, noms_exe: list,
                   chemins_hints: list = None, env_key: str = None) -> bool:
    """Lance une application — détection universelle, sans popup d'erreur Windows."""
    # Override via .env (priorité absolue)
    if env_key:
        env_val = os.path.expandvars(os.getenv(env_key, ""))
        if env_val and os.path.exists(env_val):
            try:
                subprocess.Popen([env_val])
                return True
            except Exception:
                pass

    # Détection automatique (registre → PATH → hints)
    exe_path = _boulot_trouver_exe(noms_exe, chemins_hints)
    if exe_path:
        try:
            subprocess.Popen([exe_path])
            return True
        except Exception:
            pass

    # Pas trouvé — on log silencieusement, aucune popup Windows
    print(f"[BOULOT] {label} introuvable sur ce PC (registre, PATH et hints épuisés)")
    return False


def _fermer_app(noms_process: list) -> bool:
    """Termine tous les processus correspondant aux noms donnés (insensible à la casse)."""
    if psutil is None:
        return False
    tues = 0
    noms_lower = [n.lower() for n in noms_process]
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in noms_lower:
                proc.terminate()
                tues += 1
        except Exception:
            pass
    return tues > 0


# Catalogue d'applications ouvrables / fermables par commande vocale
_APPS_CATALOGUE = {
    # ── Navigateurs ──────────────────────────────────────────
    "chrome": {
        "label": "Google Chrome", "noms": ["chrome.exe"],
        "hints": [
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
            r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe",
            r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe",
        ],
    },
    "firefox": {
        "label": "Firefox", "noms": ["firefox.exe"],
        "hints": [r"%PROGRAMFILES%\Mozilla Firefox\firefox.exe", r"%PROGRAMFILES(X86)%\Mozilla Firefox\firefox.exe"],
    },
    "edge": {
        "label": "Microsoft Edge", "noms": ["msedge.exe"],
        "hints": [
            r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe",
            r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe",
        ],
    },
    "opera": {
        "label": "Opera", "noms": ["opera.exe"],
        "hints": [
            r"%LOCALAPPDATA%\Programs\Opera\opera.exe",
            r"%LOCALAPPDATA%\Programs\Opera GX\opera.exe",
            r"%APPDATA%\Opera Software\Opera Stable\opera.exe",
            r"%APPDATA%\Opera Software\Opera GX Stable\opera.exe",
        ],
    },
    "brave": {
        "label": "Brave", "noms": ["brave.exe"],
        "hints": [
            r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"%PROGRAMFILES%\BraveSoftware\Brave-Browser\Application\brave.exe",
        ],
    },
    # ── Jeux / Launchers ─────────────────────────────────────
    "steam": {
        "label": "Steam", "noms": ["steam.exe"],
        "hints": [r"%PROGRAMFILES(X86)%\Steam\steam.exe", r"%PROGRAMFILES%\Steam\steam.exe"],
    },
    "epic": {
        "label": "Epic Games", "noms": ["EpicGamesLauncher.exe"],
        "hints": [
            r"%PROGRAMFILES(X86)%\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
            r"%PROGRAMFILES%\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
        ],
    },
    "origin": {
        "label": "Origin", "noms": ["Origin.exe"],
        "hints": [r"%PROGRAMFILES(X86)%\Origin\Origin.exe", r"%PROGRAMFILES%\Origin\Origin.exe"],
    },
    "ea": {
        "label": "EA App", "noms": ["EADesktop.exe", "EA.exe"],
        "hints": [
            r"%PROGRAMFILES%\Electronic Arts\EA Desktop\EA Desktop.exe",
            r"%PROGRAMFILES(X86)%\Electronic Arts\EA Desktop\EA Desktop.exe",
        ],
    },
    "ubisoft": {
        "label": "Ubisoft Connect", "noms": ["UbisoftConnect.exe", "upc.exe"],
        "hints": [
            r"%PROGRAMFILES(X86)%\Ubisoft\Ubisoft Game Launcher\UbisoftConnect.exe",
            r"%PROGRAMFILES%\Ubisoft\Ubisoft Game Launcher\UbisoftConnect.exe",
        ],
    },
    "gog": {
        "label": "GOG Galaxy", "noms": ["GalaxyClient.exe"],
        "hints": [
            r"%PROGRAMFILES(X86)%\GOG Galaxy\GalaxyClient.exe",
            r"%PROGRAMFILES%\GOG Galaxy\GalaxyClient.exe",
        ],
    },
    "minecraft": {
        "label": "Minecraft", "noms": ["Minecraft.exe", "MinecraftLauncher.exe"],
        "hints": [
            r"%PROGRAMFILES(X86)%\Minecraft Launcher\MinecraftLauncher.exe",
            r"%LOCALAPPDATA%\Packages\Microsoft.4297127D64EC6_8wekyb3d8bbwe\Minecraft.exe",
        ],
    },
    # ── Communication ────────────────────────────────────────
    "discord": {
        "label": "Discord", "noms": ["Discord.exe", "Update.exe"],
        "hints": [
            r"%LOCALAPPDATA%\Discord\Update.exe",
            r"%LOCALAPPDATA%\Discord\app-*\Discord.exe",
            r"%APPDATA%\Discord\Update.exe",
        ],
    },
    "teams": {
        "label": "Microsoft Teams", "noms": ["ms-teams.exe", "Teams.exe"],
        "hints": [
            r"%LOCALAPPDATA%\Microsoft\WindowsApps\ms-teams.exe",
            r"%LOCALAPPDATA%\Microsoft\Teams\current\Teams.exe",
            r"%PROGRAMFILES%\Microsoft\Teams\current\Teams.exe",
        ],
    },
    "whatsapp": {
        "label": "WhatsApp", "noms": ["WhatsApp.exe"],
        "hints": [
            r"%LOCALAPPDATA%\WhatsApp\WhatsApp.exe",
            r"%LOCALAPPDATA%\Programs\WhatsApp\WhatsApp.exe",
        ],
    },
    "telegram": {
        "label": "Telegram", "noms": ["Telegram.exe"],
        "hints": [
            r"%APPDATA%\Telegram Desktop\Telegram.exe",
            r"%LOCALAPPDATA%\Telegram Desktop\Telegram.exe",
        ],
    },
    "zoom": {
        "label": "Zoom", "noms": ["Zoom.exe"],
        "hints": [
            r"%APPDATA%\Zoom\bin\Zoom.exe",
            r"%PROGRAMFILES%\Zoom\bin\Zoom.exe",
            r"%PROGRAMFILES(X86)%\Zoom\bin\Zoom.exe",
        ],
    },
    "skype": {
        "label": "Skype", "noms": ["Skype.exe"],
        "hints": [
            r"%LOCALAPPDATA%\Microsoft\WindowsApps\Skype.exe",
            r"%PROGRAMFILES(X86)%\Microsoft\Skype for Desktop\Skype.exe",
        ],
    },
    # ── Bureautique / Office ─────────────────────────────────
    "word": {
        "label": "Microsoft Word", "noms": ["WINWORD.EXE", "winword.exe"],
        "hints": [
            r"%PROGRAMFILES%\Microsoft Office\root\Office16\WINWORD.EXE",
            r"%PROGRAMFILES(X86)%\Microsoft Office\root\Office16\WINWORD.EXE",
            r"%PROGRAMFILES%\Microsoft Office\Office16\WINWORD.EXE",
        ],
    },
    "excel": {
        "label": "Microsoft Excel", "noms": ["EXCEL.EXE", "excel.exe"],
        "hints": [
            r"%PROGRAMFILES%\Microsoft Office\root\Office16\EXCEL.EXE",
            r"%PROGRAMFILES(X86)%\Microsoft Office\root\Office16\EXCEL.EXE",
            r"%PROGRAMFILES%\Microsoft Office\Office16\EXCEL.EXE",
        ],
    },
    "powerpoint": {
        "label": "Microsoft PowerPoint", "noms": ["POWERPNT.EXE", "powerpnt.exe"],
        "hints": [
            r"%PROGRAMFILES%\Microsoft Office\root\Office16\POWERPNT.EXE",
            r"%PROGRAMFILES(X86)%\Microsoft Office\root\Office16\POWERPNT.EXE",
        ],
    },
    "outlook": {
        "label": "Outlook", "noms": ["OUTLOOK.EXE", "outlook.exe", "olk.exe"],
        "hints": [
            r"%PROGRAMFILES%\Microsoft Office\root\Office16\OUTLOOK.EXE",
            r"%PROGRAMFILES(X86)%\Microsoft Office\root\Office16\OUTLOOK.EXE",
            r"%LOCALAPPDATA%\Microsoft\WindowsApps\olk.exe",
        ],
    },
    "onenote": {
        "label": "OneNote", "noms": ["ONENOTE.EXE", "onenote.exe"],
        "hints": [
            r"%PROGRAMFILES%\Microsoft Office\root\Office16\ONENOTE.EXE",
            r"%PROGRAMFILES(X86)%\Microsoft Office\root\Office16\ONENOTE.EXE",
        ],
    },
    # ── Créatif / Design ─────────────────────────────────────
    "photoshop": {
        "label": "Photoshop", "noms": ["Photoshop.exe"],
        "hints": [
            r"%PROGRAMFILES%\Adobe\Adobe Photoshop 2024\Photoshop.exe",
            r"%PROGRAMFILES%\Adobe\Adobe Photoshop 2025\Photoshop.exe",
            r"%PROGRAMFILES%\Adobe\Adobe Photoshop CC 2023\Photoshop.exe",
            r"%PROGRAMFILES%\Adobe\Adobe Photoshop 2023\Photoshop.exe",
        ],
    },
    "premiere": {
        "label": "Premiere Pro", "noms": ["Adobe Premiere Pro.exe"],
        "hints": [
            r"%PROGRAMFILES%\Adobe\Adobe Premiere Pro 2024\Adobe Premiere Pro.exe",
            r"%PROGRAMFILES%\Adobe\Adobe Premiere Pro 2025\Adobe Premiere Pro.exe",
            r"%PROGRAMFILES%\Adobe\Adobe Premiere Pro CC 2023\Adobe Premiere Pro.exe",
        ],
    },
    "after effects": {
        "label": "After Effects", "noms": ["AfterFX.exe"],
        "hints": [
            r"%PROGRAMFILES%\Adobe\Adobe After Effects 2024\Support Files\AfterFX.exe",
            r"%PROGRAMFILES%\Adobe\Adobe After Effects 2025\Support Files\AfterFX.exe",
            r"%PROGRAMFILES%\Adobe\Adobe After Effects 2023\Support Files\AfterFX.exe",
        ],
    },
    "illustrator": {
        "label": "Illustrator", "noms": ["Illustrator.exe"],
        "hints": [
            r"%PROGRAMFILES%\Adobe\Adobe Illustrator 2024\Support Files\Contents\Windows\Illustrator.exe",
            r"%PROGRAMFILES%\Adobe\Adobe Illustrator 2025\Support Files\Contents\Windows\Illustrator.exe",
        ],
    },
    "capcut": {
        "label": "CapCut", "noms": ["CapCut.exe"],
        "hints": [
            r"%LOCALAPPDATA%\CapCut\Apps\CapCut.exe",
            r"%PROGRAMFILES%\CapCut\CapCut.exe",
        ],
    },
    "obs": {
        "label": "OBS Studio", "noms": ["obs64.exe", "obs32.exe"],
        "hints": [
            r"%PROGRAMFILES%\obs-studio\bin\64bit\obs64.exe",
            r"%PROGRAMFILES(X86)%\obs-studio\bin\64bit\obs64.exe",
        ],
    },
    "blender": {
        "label": "Blender", "noms": ["blender.exe"],
        "hints": [
            r"%PROGRAMFILES%\Blender Foundation\Blender 4.0\blender.exe",
            r"%PROGRAMFILES%\Blender Foundation\Blender 3.6\blender.exe",
            r"%PROGRAMFILES%\Blender Foundation\Blender\blender.exe",
        ],
    },
    "gimp": {
        "label": "GIMP", "noms": ["gimp-2.10.exe", "gimp.exe"],
        "hints": [
            r"%PROGRAMFILES%\GIMP 2\bin\gimp-2.10.exe",
            r"%PROGRAMFILES(X86)%\GIMP 2\bin\gimp-2.10.exe",
        ],
    },
    # ── Développement ────────────────────────────────────────
    "vscode": {
        "label": "Visual Studio Code", "noms": ["Code.exe"],
        "hints": [
            r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",
            r"%PROGRAMFILES%\Microsoft VS Code\Code.exe",
        ],
    },
    "claude": {
        "label": "Claude", "noms": ["claude.exe", "Claude.exe"],
        "hints": [
            r"%LOCALAPPDATA%\AnthropicClaude\claude.exe",
            r"%PROGRAMFILES%\AnthropicClaude\claude.exe",
            r"%APPDATA%\AnthropicClaude\claude.exe",
        ],
    },
    "terminal": {
        "label": "Terminal", "noms": ["wt.exe", "WindowsTerminal.exe"],
        "hints": [
            r"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe",
        ],
    },
    # ── Multimédia ───────────────────────────────────────────
    "vlc": {
        "label": "VLC", "noms": ["vlc.exe"],
        "hints": [
            r"%PROGRAMFILES%\VideoLAN\VLC\vlc.exe",
            r"%PROGRAMFILES(X86)%\VideoLAN\VLC\vlc.exe",
        ],
    },
    "spotify": {
        "label": "Spotify", "noms": ["Spotify.exe"],
        "hints": [
            r"%APPDATA%\Spotify\Spotify.exe",
            r"%LOCALAPPDATA%\Microsoft\WindowsApps\Spotify.exe",
        ],
    },
    # ── Utilitaires ──────────────────────────────────────────
    "filezilla": {
        "label": "FileZilla", "noms": ["filezilla.exe"],
        "hints": [
            r"%PROGRAMFILES%\FileZilla FTP Client\filezilla.exe",
            r"%PROGRAMFILES(X86)%\FileZilla FTP Client\filezilla.exe",
        ],
    },
    "winrar": {
        "label": "WinRAR", "noms": ["WinRAR.exe"],
        "hints": [
            r"%PROGRAMFILES%\WinRAR\WinRAR.exe",
            r"%PROGRAMFILES(X86)%\WinRAR\WinRAR.exe",
        ],
    },
    "7zip": {
        "label": "7-Zip", "noms": ["7zFM.exe"],
        "hints": [
            r"%PROGRAMFILES%\7-Zip\7zFM.exe",
            r"%PROGRAMFILES(X86)%\7-Zip\7zFM.exe",
        ],
    },
    "antigravity": {
        "label": "Antigravity", "noms": ["Antigravity.exe", "antigravity.exe"],
        "hints": [
            r"%LOCALAPPDATA%\Antigravity\Antigravity.exe",
            r"%PROGRAMFILES%\Antigravity\Antigravity.exe",
            r"%PROGRAMFILES(X86)%\Antigravity\Antigravity.exe",
            r"%APPDATA%\Antigravity\Antigravity.exe",
            r"%LOCALAPPDATA%\Programs\Antigravity\Antigravity.exe",
        ],
    },
}
# Alias — plusieurs façons de nommer la même app
_APPS_CATALOGUE["ea app"]          = _APPS_CATALOGUE["ea"]
_APPS_CATALOGUE["microsoft edge"]  = _APPS_CATALOGUE["edge"]
_APPS_CATALOGUE["opera gx"]        = _APPS_CATALOGUE["opera"]
_APPS_CATALOGUE["google chrome"]   = _APPS_CATALOGUE["chrome"]
_APPS_CATALOGUE["epic games"]      = _APPS_CATALOGUE["epic"]
_APPS_CATALOGUE["epic game"]       = _APPS_CATALOGUE["epic"]
_APPS_CATALOGUE["ubisoft connect"] = _APPS_CATALOGUE["ubisoft"]
_APPS_CATALOGUE["uplay"]          = _APPS_CATALOGUE["ubisoft"]
_APPS_CATALOGUE["gog galaxy"]     = _APPS_CATALOGUE["gog"]
_APPS_CATALOGUE["visual studio code"] = _APPS_CATALOGUE["vscode"]
_APPS_CATALOGUE["vs code"]        = _APPS_CATALOGUE["vscode"]
_APPS_CATALOGUE["code"]           = _APPS_CATALOGUE["vscode"]
_APPS_CATALOGUE["premiere pro"]   = _APPS_CATALOGUE["premiere"]
_APPS_CATALOGUE["adobe premiere"] = _APPS_CATALOGUE["premiere"]
_APPS_CATALOGUE["adobe photoshop"]= _APPS_CATALOGUE["photoshop"]
_APPS_CATALOGUE["adobe after effects"] = _APPS_CATALOGUE["after effects"]
_APPS_CATALOGUE["adobe illustrator"] = _APPS_CATALOGUE["illustrator"]
_APPS_CATALOGUE["microsoft word"] = _APPS_CATALOGUE["word"]
_APPS_CATALOGUE["microsoft excel"]= _APPS_CATALOGUE["excel"]
_APPS_CATALOGUE["microsoft powerpoint"] = _APPS_CATALOGUE["powerpoint"]
_APPS_CATALOGUE["powerpoint"]     = _APPS_CATALOGUE["powerpoint"]
_APPS_CATALOGUE["ppt"]            = _APPS_CATALOGUE["powerpoint"]
_APPS_CATALOGUE["microsoft outlook"] = _APPS_CATALOGUE["outlook"]
_APPS_CATALOGUE["microsoft teams"]= _APPS_CATALOGUE["teams"]
_APPS_CATALOGUE["obs studio"]     = _APPS_CATALOGUE["obs"]
_APPS_CATALOGUE["sept zip"]       = _APPS_CATALOGUE["7zip"]
_APPS_CATALOGUE["7 zip"]          = _APPS_CATALOGUE["7zip"]


async def mode_boulot():
    """Lance Spotify, ouvre Documents, Téléchargements, Chrome et Antigravity
    en disposition quadrants sur l'écran."""
    try:
        import win32gui, win32con, win32api
    except ImportError:
        return "pywin32 manquant — installez-le pour la disposition des fenêtres."

    await parler("Bien, je prépare votre espace de travail.")

    # ── 1. Spotify en fond (PRIORITE — lancé en premier) ────
    spotify_lancer_playlist(SPOTIFY_MUSIQUE_URI)
    time.sleep(0.5)

    # ── 2. Ouverture des dossiers ────────────────────────────
    # Documents (ira en haut à gauche)
    chemin_documents = resoudre_chemin("documents")
    subprocess.Popen(["explorer", chemin_documents])
    time.sleep(0.3)

    # Téléchargements (ira en haut à droite)
    chemin_telechargements = resoudre_chemin("downloads")
    subprocess.Popen(["explorer", chemin_telechargements])
    time.sleep(0.3)

    # ── 3. Chrome (ira en bas à gauche) ──────────────────────
    _boulot_lancer(
        "Chrome", ["chrome.exe"],
        chemins_hints=[
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
            r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe",
            r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe",
        ],
        env_key="CHROME_PATH"
    )
    time.sleep(0.3)

    # ── 4. Antigravity (ira en bas à droite) ─────────────────
    _boulot_lancer(
        "Antigravity", ["Antigravity.exe", "antigravity.exe"],
        chemins_hints=[
            r"%LOCALAPPDATA%\Antigravity\Antigravity.exe",
            r"%PROGRAMFILES%\Antigravity\Antigravity.exe",
            r"%PROGRAMFILES(X86)%\Antigravity\Antigravity.exe",
            r"%APPDATA%\Antigravity\Antigravity.exe",
            r"%LOCALAPPDATA%\Programs\Antigravity\Antigravity.exe",
        ],
        env_key="ANTIGRAVITY_PATH"
    )
    time.sleep(0.3)

    await parler("Applications lancées, j'arrange votre espace dans quelques secondes.")
    time.sleep(7)

    # ── 5. Disposition en 4 quadrants ────────────────────────
    screen_w = win32api.GetSystemMetrics(0)
    screen_h = win32api.GetSystemMetrics(1)
    work_h   = screen_h - 48
    hw = screen_w // 2
    hh = work_h  // 2

    #  ┌──────────────────┬──────────────────┐
    #  │   Documents      │  Téléchargements │
    #  │   (haut gauche)  │  (haut droite)   │
    #  ├──────────────────┼──────────────────┤
    #  │   Chrome         │  Antigravity     │
    #  │   (bas gauche)   │  (bas droite)    │
    #  └──────────────────┴──────────────────┘
    disposition = [
        {"titres": ["Documents"],                           "pos": (0,  0,  hw, hh)},
        {"titres": ["Téléchargements", "Telechargements",
                    "Downloads"],                           "pos": (hw, 0,  hw, hh)},
        {"titres": ["Chrome", "Google Chrome"],             "pos": (0,  hh, hw, hh)},
        {"titres": ["Antigravity"],                         "pos": (hw, hh, hw, hh)},
    ]

    def _trouver_hwnd(titres):
        found = [None]
        def cb(hwnd, _):
            if found[0]:
                return
            if win32gui.IsWindowVisible(hwnd):
                t = win32gui.GetWindowText(hwnd)
                if any(mot.lower() in t.lower() for mot in titres):
                    found[0] = hwnd
        win32gui.EnumWindows(cb, None)
        return found[0]

    ok = 0
    for item in disposition:
        hwnd = _trouver_hwnd(item["titres"])
        if hwnd:
            x, y, w, h = item["pos"]
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetWindowPos(
                hwnd, win32con.HWND_TOP, x, y, w, h,
                win32con.SWP_SHOWWINDOW
            )
            time.sleep(0.2)
            ok += 1

    if ok == 4:
        return "Votre espace de travail est prêt, Asta. Bonne journée !"
    return f"Espace prêt — {ok}/4 fenêtres positionnées. Musique lancée en fond."        

# ===========================================================================
# Point d'entrée
# ===========================================================================

def main() -> None:
    from core.config      import SESSION_FILE
    from core.auth_manager import AuthManager
    from views.auth_view  import AuthWindow
    from utils.cache_manager import CacheManager
    from core.health_manager import HealthManager
    from utils.status_manager import StatusManager

    # Vérification de la licence matérielle
    _, hwid = check_license_on_startup()

    # Init du cache disque
    CacheManager.initialize(DATA_DIR / "cache")

    # Restauration de session (refresh token)
    AuthManager.initialize(SESSION_FILE)

    # Surveillance du backend
    HealthManager.start()

    if not StatusManager.is_authenticated():
        auth_win = AuthWindow()
        auth_win.mainloop()
        if not auth_win.success:
            sys.exit(0)

    # Lancement de l'application
    app = AstaAcademie()
    app.mainloop()
    sys.exit(0)


if __name__ == "__main__":
    main()
