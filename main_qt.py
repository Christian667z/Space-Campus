"""
Asta Académie — Fenêtre Principale Qt v2.0 (PySide6)
=====================================================
Architecture : Sidebar + TopBar + StackedWidget + StatusBar

Améliorations v2.0 :
  - NavButton : tooltips Ctrl+N, badge count (quiz en attente, etc.)
  - Sidebar   : mini-bannière streak/points/niveau, bouton collapse,
                chargement du logo PNG, scrollArea sans barre visible
  - TopBar    : boutons zoom connectés, Ctrl+K → focus recherche
  - StatusBar : streak 🔥 affiché, méthode refresh_profile()
  - AstaAcademieWindow :
      · Badges streak multi-niveaux : 3j 🌱, 7j 🔥, 14j 💎, 30j 👑
      · Raccourcis Ctrl+1…9 pour les 9 premières sections
      · Ctrl+K / Ctrl+F → focus barre de recherche
      · Recherche globale groupée par catégorie (QListWidget avec sections)
      · Splash enrichi (7 conseils, barre colorée)
      · Page d'erreur avec bouton "Copier l'erreur"
      · closeEvent : sauvegarde + arrêt propre du backend
      · Logging structuré (plus de `except: pass` nus)
  - LicenseWindow : auto-format clé, bouton 👁, max 5 tentatives
  - launch() : flow nettoyé, guard sur fenêtre auth déjà fermée
"""

from __future__ import annotations

import logging
import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Optional, Dict, Any

from PySide6.QtCore import (
    Qt, QTimer, Signal, QObject, QSize, QPropertyAnimation, QEasingCurve,
)
from PySide6.QtGui import (
    QFont, QIcon, QPixmap, QKeySequence, QShortcut, QColor,
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QStackedWidget, QScrollArea, QSizePolicy,
    QLineEdit, QDialog, QMessageBox, QListWidget, QListWidgetItem,
    QProgressBar, QToolTip,
)

from ui.themes.theme_manager import THEMES, DEFAULT_THEME, get_stylesheet, Theme
from ui.components.widgets import (
    Card, StatCard, Badge, SectionHeader, PomodoroWidget,
    NetworkIndicator, add_shadow, AnimatedCounter,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

APP_NAME   = "Asta Académie"
VERSION    = "1.0.0"
UNIVERSITE = "UNASMOH"
FULL_UNI   = "Université Américaine des Sciences Modernes"
OPTION     = "Sciences Informatiques"
DEV_NAME   = "Space | Asta Dev"
DEV_REAL   = "Lucky Luke"
PROMO      = "2024-2028"
WHATSAPP   = "+509 3567-2037 / +509 4696-6290"

from core.config import DATA_DIR, PROFILE_FILE, NOTES_FILE, DB_FILE

DATA_DIR.mkdir(parents=True, exist_ok=True)
SESSION_FILE = DATA_DIR / "session.enc"

MAX_LICENSE_ATTEMPTS = 5

STREAK_BADGES = [
    (3,  "Assidu 3j 🌱"),
    (7,  "Assidu 7j 🔥"),
    (14, "Assidu 14j 💎"),
    (30, "Assidu 30j 👑"),
]

SPLASH_TIPS = [
    "Chargement des modules…",
    "Connexion à la base de données…",
    "Initialisation des cours L1→L4…",
    "Chargement de l'Oracle et des outils…",
    "Préparation du module CTF…",
    "Configuration de l'interface…",
    "Bienvenue sur Asta Académie ! 🚀",
]

# Sections dans l'ordre (key, icon, label, shortcut_hint)
SECTIONS = [
    ("dashboard",  "home",  "Accueil",      "Ctrl+1"),
    ("space_ai",   "assistant",  "Space AI",     "Ctrl+2"),
    ("oracle",     "insight",  "L'Oracle",     "Ctrl+3"),
    ("tools",      "tools",  "Outils",       "Ctrl+4"),
    ("courses",    "library",  "Cours",        "Ctrl+5"),
    ("shortcuts",  "flash",  "Raccourcis",   "Ctrl+6"),
    ("hacking",    "shield",  "DevSecurity",  "Ctrl+7"),
    ("quiz",       "brain",  "Quiz",         "Ctrl+8"),
    ("notes",      "notes",  "Mes Notes",    "Ctrl+9"),
    ("grades",     "stats",  "Moyennes",     ""),
    ("guide",      "guide",  "Guide",        ""),
    ("profile",    "user",  "Profil",       ""),
    ("career",     "target",  "Carrière",     ""),
    ("about",      "info",  "À Propos",    ""),
    ("settings",   "settings",  "Paramètres",  ""),
]


def load_json(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("load_json(%s) : %s", path, e)
    return default


def save_json(path: Path, data):
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error("save_json(%s) : %s", path, e)


# ===========================================================================
# NavButton
# ===========================================================================

class NavButton(QPushButton):
    """Bouton de navigation sidebar avec badge et tooltip de raccourci."""

    def __init__(self, key: str, label: str, icon_name: str, theme_obj: Theme, shortcut_hint: str = "", parent=None) -> None:
        super().__init__(label, parent)
        self.key = key
        self.icon_name = icon_name
        self.setProperty("class", "nav_btn")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)
        
        self.update_icon(theme_obj)
        self.setIconSize(QSize(18, 18))
        
        if shortcut_hint:
            self.setToolTip(f"{label}  [{shortcut_hint}]")

        # Badge (ex: nombre de quiz non répondus)
        self._badge: Optional[QLabel] = None

    def update_icon(self, theme_obj: Theme) -> None:
        from utils.svg_manager import SVGManager
        icon_color = theme_obj.accent if self.property("active") == "true" else theme_obj.text_secondary
        self.setIcon(SVGManager.get_icon(self.icon_name, color=icon_color, size=18))

    def set_active(self, active: bool, theme_obj: Theme) -> None:
        self.setProperty("active", "true" if active else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update_icon(theme_obj)

    def set_badge(self, count: int) -> None:
        """Affiche ou cache un badge numérique sur le bouton."""
        if count > 0:
            if self._badge is None:
                self._badge = QLabel(self)
                self._badge.setFixedSize(18, 18)
                self._badge.setAlignment(Qt.AlignCenter)
                self._badge.setStyleSheet(
                    "background:#ef4444; color:white; border-radius:9px; font-size:10px; font-weight:bold;"
                )
            self._badge.setText(str(min(count, 99)))
            self._badge.move(self.width() - 22, 11)
            self._badge.show()
        elif self._badge:
            self._badge.hide()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self._badge:
            self._badge.move(self.width() - 22, 11)


# ===========================================================================
# Sidebar
# ===========================================================================

class Sidebar(QWidget):
    nav_clicked    = Signal(str)
    collapse_toggled = Signal(bool)

    def __init__(self, profile: dict, theme: Theme, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.theme        = theme
        self._collapsed   = False
        self._full_width  = 220
        self._mini_width  = 56
        self.setFixedWidth(self._full_width)

        self._nav_buttons: dict[str, NavButton] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 12, 8, 12)
        layout.setSpacing(0)

        # ── Logo + Nom ──────────────────────────────────────────────────────
        self._logo_frame = self._build_logo(profile)
        layout.addWidget(self._logo_frame)

        # ── Statistiques mini ───────────────────────────────────────────────
        self._stats_frame = self._build_stats(profile)
        layout.addWidget(self._stats_frame)

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("background:#2d3f55; border:none;")
        layout.addWidget(sep)
        layout.addSpacing(6)

        # ── Boutons nav ─────────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { background:transparent; border:none; }")

        nav_w = QWidget()
        nav_w.setStyleSheet("background:transparent;")
        nav_l = QVBoxLayout(nav_w)
        nav_l.setContentsMargins(0, 0, 0, 0)
        nav_l.setSpacing(2)

        for key, icon, label, shortcut in SECTIONS:
            btn = NavButton(key, label, icon, theme, shortcut)
            btn.clicked.connect(lambda _=False, k=key: self.nav_clicked.emit(k))
            nav_l.addWidget(btn)
            self._nav_buttons[key] = btn

        nav_l.addStretch()
        scroll.setWidget(nav_w)
        layout.addWidget(scroll, 1)

        # ── Bouton collapse + footer ────────────────────────────────────────
        layout.addSpacing(8)
        self._collapse_btn = QPushButton("◀ Réduire")
        self._collapse_btn.setProperty("class", "ghost")
        self._collapse_btn.setFixedHeight(28)
        self._collapse_btn.setFont(QFont("Segoe UI", 9))
        self._collapse_btn.clicked.connect(self._toggle_collapse)
        layout.addWidget(self._collapse_btn)

        self._footer = QLabel(f"Dev: {DEV_NAME}\nPromo {PROMO}")
        self._footer.setFont(QFont("Segoe UI", 8))
        self._footer.setAlignment(Qt.AlignCenter)
        self._footer.setStyleSheet("color:#475569;")
        layout.addWidget(self._footer)

    def _build_logo(self, profile: dict) -> QWidget:
        frame = QWidget()
        lo = QVBoxLayout(frame)
        lo.setContentsMargins(8, 0, 8, 10)
        lo.setSpacing(4)
        lo.setAlignment(Qt.AlignCenter)

        # Essaie de charger le PNG du logo
        self._icon_lbl = QLabel()
        self._icon_lbl.setAlignment(Qt.AlignCenter)
        logo_loaded = False
        try:
            from core.config import asset_file
            png = asset_file("Space_logo_256.png")
            if png.exists():
                pm = QPixmap(str(png)).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self._icon_lbl.setPixmap(pm)
                logo_loaded = True
        except Exception:
            pass
        if not logo_loaded:
            self._icon_lbl.setText("🎓")
            self._icon_lbl.setFont(QFont("Segoe UI Emoji", 34))

        lo.addWidget(self._icon_lbl)

        self.user_lbl = QLabel(profile.get("nom", "Étudiant"))
        self.user_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.user_lbl.setObjectName("app_title")
        self.user_lbl.setAlignment(Qt.AlignCenter)
        lo.addWidget(self.user_lbl)

        opt = QLabel(OPTION)
        opt.setFont(QFont("Segoe UI", 8))
        opt.setObjectName("app_subtitle")
        opt.setAlignment(Qt.AlignCenter)
        lo.addWidget(opt)
        return frame

    def _build_stats(self, profile: dict) -> QWidget:
        """Mini-bannière streak / points / niveau."""
        frame = QFrame()
        frame.setObjectName("sidebar_stats")
        frame.setStyleSheet("""
            QFrame#sidebar_stats {
                background: rgba(16, 185, 129, 0.08);
                border: 1px solid rgba(16, 185, 129, 0.25);
                border-radius: 8px;
                margin: 4px 4px 8px 4px;
            }
        """)
        row = QHBoxLayout(frame)
        row.setContentsMargins(8, 6, 8, 6)
        row.setSpacing(0)

        streak = profile.get("streak", 0)
        points = profile.get("points", 0)
        niveau = profile.get("niveau", "L2")

        for icon, val in [("🔥", str(streak)), ("⭐", str(points)), ("📚", niveau)]:
            col = QVBoxLayout()
            col.setSpacing(0)
            col.setAlignment(Qt.AlignCenter)
            i = QLabel(icon)
            i.setFont(QFont("Segoe UI Emoji", 13))
            i.setAlignment(Qt.AlignCenter)
            v = QLabel(val)
            v.setFont(QFont("Segoe UI", 9, QFont.Bold))
            v.setStyleSheet("color:#10b981;")
            v.setAlignment(Qt.AlignCenter)
            col.addWidget(i)
            col.addWidget(v)
            row.addLayout(col)
            if icon != "📚":
                sep2 = QFrame()
                sep2.setFrameShape(QFrame.VLine)
                sep2.setStyleSheet("color:#2d3f55;")
                row.addWidget(sep2)

        self._stats_streak_lbl = frame.findChildren(QLabel)  # références pour refresh
        return frame

    def refresh_stats(self, profile: dict) -> None:
        """Met à jour les valeurs de streak/points/niveau dans le mini-stats."""
        # Reconstruction simple (la frame est légère)
        old = self._stats_frame
        new = self._build_stats(profile)
        self._stats_frame = new
        parent_layout = self.layout()
        idx = parent_layout.indexOf(old)
        parent_layout.takeAt(idx)
        old.deleteLater()
        parent_layout.insertWidget(idx, new)

    def set_active(self, key: str) -> None:
        for k, btn in self._nav_buttons.items():
            btn.set_active(k == key, self.theme)

    def refresh_theme(self, theme: Theme) -> None:
        self.theme = theme
        self.refresh_stats(self.profile)
        for btn in self._nav_buttons.values():
            btn.update_icon(theme)

    def update_user(self, nom: str) -> None:
        self.user_lbl.setText(nom)

    def set_badge(self, key: str, count: int) -> None:
        if key in self._nav_buttons:
            self._nav_buttons[key].set_badge(count)

    def _toggle_collapse(self) -> None:
        self._collapsed = not self._collapsed
        target_w = self._mini_width if self._collapsed else self._full_width
        self.setFixedWidth(target_w)
        self._logo_frame.setVisible(not self._collapsed)
        self._stats_frame.setVisible(not self._collapsed)
        self._footer.setVisible(not self._collapsed)
        self._collapse_btn.setText("▶" if self._collapsed else "◀ Réduire")
        for key, btn in self._nav_buttons.items():
            key_data = next((s for s in SECTIONS if s[0] == key), None)
            if key_data:
                label = key_data[2]
                btn.setText("" if self._collapsed else label)
        self.collapse_toggled.emit(self._collapsed)


# ===========================================================================
# TopBar
# ===========================================================================

class TopBar(QWidget):
    search_requested = Signal(str)
    zoom_in_clicked  = Signal()
    zoom_out_clicked = Signal()
    zoom_rst_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("topbar")
        self.setFixedHeight(54)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(10)

        # Logo + version
        app_lbl = QLabel(f"🎓  {APP_NAME}")
        app_lbl.setFont(QFont("Segoe UI", 13, QFont.Bold))
        app_lbl.setStyleSheet("color:#10b981;")
        layout.addWidget(app_lbl)

        ver_lbl = QLabel(f"v{VERSION}")
        ver_lbl.setFont(QFont("Segoe UI", 9))
        ver_lbl.setStyleSheet("color:#475569;")
        layout.addWidget(ver_lbl)

        layout.addStretch()

        # Recherche (Ctrl+K)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Rechercher…  (Ctrl+K)")
        self.search_input.setFixedWidth(270)
        self.search_input.setFixedHeight(34)
        self.search_input.returnPressed.connect(
            lambda: self.search_requested.emit(self.search_input.text()))
        layout.addWidget(self.search_input)

        srch_btn = QPushButton("🔍")
        srch_btn.setFixedSize(34, 34)
        srch_btn.setProperty("class", "primary")
        srch_btn.clicked.connect(
            lambda: self.search_requested.emit(self.search_input.text()))
        layout.addWidget(srch_btn)

        layout.addSpacing(12)

        # Pomodoro
        self.pomo = PomodoroWidget()
        layout.addWidget(self.pomo)

        layout.addSpacing(12)

        # Zoom (boutons connectés via signal)
        zoom_f = QWidget()
        zl = QHBoxLayout(zoom_f)
        zl.setContentsMargins(0, 0, 0, 0)
        zl.setSpacing(2)

        zm_btn = QPushButton("−")
        zm_btn.setFixedSize(26, 26)
        zm_btn.setProperty("class", "ghost")
        zm_btn.setToolTip("Zoom arrière (Ctrl+-)")
        zm_btn.clicked.connect(self.zoom_out_clicked)
        zl.addWidget(zm_btn)

        self.zoom_lbl = QLabel("100%")
        self.zoom_lbl.setFont(QFont("Segoe UI", 9))
        self.zoom_lbl.setStyleSheet("color:#475569;")
        self.zoom_lbl.setFixedWidth(42)
        self.zoom_lbl.setAlignment(Qt.AlignCenter)
        self.zoom_lbl.setCursor(Qt.PointingHandCursor)
        self.zoom_lbl.mousePressEvent = lambda _: self.zoom_rst_clicked.emit()
        self.zoom_lbl.setToolTip("Cliquer pour 100% (Ctrl+0)")
        zl.addWidget(self.zoom_lbl)

        zp_btn = QPushButton("+")
        zp_btn.setFixedSize(26, 26)
        zp_btn.setProperty("class", "ghost")
        zp_btn.setToolTip("Zoom avant (Ctrl+=)")
        zp_btn.clicked.connect(self.zoom_in_clicked)
        zl.addWidget(zp_btn)

        layout.addWidget(zoom_f)
        layout.addSpacing(8)

        # Indicateur réseau
        self.net_indicator = NetworkIndicator()
        layout.addWidget(self.net_indicator)

    def focus_search(self) -> None:
        self.search_input.setFocus()
        self.search_input.selectAll()


# ===========================================================================
# StatusBar
# ===========================================================================

class StatusBar(QWidget):
    def __init__(self, profile: dict, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statusbar")
        self.setFixedHeight(28)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(20)

        self.clock_lbl = QLabel()
        self.clock_lbl.setFont(QFont("Segoe UI", 9))
        self.clock_lbl.setStyleSheet("color:#475569;")
        layout.addWidget(self.clock_lbl)

        self.niveau_lbl = QLabel()
        self.niveau_lbl.setFont(QFont("Segoe UI", 9))
        self.niveau_lbl.setStyleSheet("color:#10b981;")
        layout.addWidget(self.niveau_lbl)

        self.points_lbl = QLabel()
        self.points_lbl.setFont(QFont("Segoe UI", 9))
        self.points_lbl.setStyleSheet("color:#f59e0b;")
        layout.addWidget(self.points_lbl)

        self.streak_lbl = QLabel()
        self.streak_lbl.setFont(QFont("Segoe UI", 9))
        self.streak_lbl.setStyleSheet("color:#f97316;")
        layout.addWidget(self.streak_lbl)

        layout.addStretch()

        brand = QLabel(f"{APP_NAME} — {UNIVERSITE} | {DEV_NAME}")
        brand.setFont(QFont("Segoe UI", 9))
        brand.setStyleSheet("color:#2d3f55;")
        layout.addWidget(brand)

        self.refresh_profile(profile)

        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._tick)
        self._clock_timer.start(1000)
        self._tick()

    def _tick(self) -> None:
        self.clock_lbl.setText(datetime.now().strftime("%d/%m/%Y  %H:%M:%S"))

    def refresh_profile(self, profile: dict) -> None:
        self.niveau_lbl.setText(f"Niveau : {profile.get('niveau', 'L2')}")
        self.points_lbl.setText(f"⭐ {profile.get('points', 0)} pts")
        streak = profile.get("streak", 0)
        self.streak_lbl.setText(f"🔥 {streak}j" if streak else "")


# ===========================================================================
# Fenêtre principale
# ===========================================================================

class AstaAcademieWindow(QMainWindow):
    def __init__(self, profile: dict, user_id: int) -> None:
        super().__init__()
        self.profile          = profile
        self.user_id          = user_id
        self.theme_name       = profile.get("theme", DEFAULT_THEME)
        self.theme: Theme     = THEMES.get(self.theme_name, THEMES[DEFAULT_THEME])
        self._current_section = "dashboard"
        self._page_cache: dict[str, QWidget] = {}
        self.notes_data       = load_json(NOTES_FILE, {})
        self.backend_process: Optional[subprocess.Popen] = None

        self._setup_window()
        self._apply_theme()
        self._build_ui()
        self._setup_shortcuts()

        QTimer.singleShot(80,  self._show_splash)
        QTimer.singleShot(200, lambda: self._show_section("dashboard"))
        QTimer.singleShot(350, self._update_streak)

        logger.info("AstaAcademieWindow ouverte pour %s (ID %d).", profile.get("nom"), user_id)

    # ── Setup ─────────────────────────────────────────────────────────────────

    def _setup_window(self) -> None:
        self.setWindowTitle(f"{APP_NAME} v{VERSION} — {UNIVERSITE}")
        self.setMinimumSize(1024, 660)
        self.resize(1280, 740)
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - 1280) // 2, (screen.height() - 740) // 2)
        try:
            from core.config import asset_file
            ico = asset_file("Space_logo.ico")
            if ico.exists():
                self.setWindowIcon(QIcon(str(ico)))
        except Exception:
            pass

    def _apply_theme(self) -> None:
        self.setStyleSheet(get_stylesheet(self.theme))

    # ── Build UI ──────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.topbar = TopBar()
        self.topbar.search_requested.connect(self._do_search)
        self.topbar.zoom_in_clicked.connect(self._zoom_in)
        self.topbar.zoom_out_clicked.connect(self._zoom_out)
        self.topbar.zoom_rst_clicked.connect(self._zoom_reset)
        root.addWidget(self.topbar)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self.sidebar = Sidebar(self.profile, self.theme)
        self.sidebar.nav_clicked.connect(self._show_section)
        body.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")
        body.addWidget(self.stack, 1)

        root.addLayout(body, 1)

        self.status_bar_widget = StatusBar(self.profile)
        root.addWidget(self.status_bar_widget)

    # ── Raccourcis ────────────────────────────────────────────────────────────

    def _setup_shortcuts(self) -> None:
        # Zoom
        QShortcut(QKeySequence("Ctrl+="), self).activated.connect(self._zoom_in)
        QShortcut(QKeySequence("Ctrl++"), self).activated.connect(self._zoom_in)
        QShortcut(QKeySequence("Ctrl+-"), self).activated.connect(self._zoom_out)
        QShortcut(QKeySequence("Ctrl+0"), self).activated.connect(self._zoom_reset)
        # Recherche
        QShortcut(QKeySequence("Ctrl+K"), self).activated.connect(self.topbar.focus_search)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.topbar.focus_search)
        # Navigation Ctrl+1…Ctrl+9
        for i, (key, _, _, _) in enumerate(SECTIONS[:9], start=1):
            QShortcut(QKeySequence(f"Ctrl+{i}"), self).activated.connect(
                lambda k=key: self._show_section(k)
            )

    # ── Navigation ────────────────────────────────────────────────────────────

    def _show_section(self, key: str) -> None:
        self.sidebar.set_active(key)
        self._current_section = key

        if key not in self._page_cache:
            page = self._build_page(key)
            if page:
                self._page_cache[key] = page
                self.stack.addWidget(page)

        if key in self._page_cache:
            self.stack.setCurrentWidget(self._page_cache[key])

        logger.info("Section affichée : '%s'", key)

    def _build_page(self, key: str) -> QWidget:
        from views.dashboard_view  import DashboardPage
        from views.courses_view    import CoursesPage
        from views.notes_view      import NotesPage
        from views.quiz_view       import QuizPage
        from views.profile_view    import ProfilePage
        from views.settings_view   import SettingsPage
        from views.tools_view      import ToolsPage
        from views.grades_view     import GradesPage
        from views.shortcuts_view  import ShortcutsPage
        from views.about_view      import AboutPage
        from views.space_ai_view   import SpaceAiPage
        from views.oracle_view     import OraclePage
        from views.guide_view      import GuidePage
        from views.hacking_view    import HackingPage
        from views.career_view     import CareerPage
        from views.legal_view      import LegalPage

        builders: dict[str, Callable[[], QWidget]] = {
            "dashboard": lambda: DashboardPage(self.profile, self.user_id, self.theme),
            "courses":   lambda: CoursesPage(self.theme),
            "notes":     lambda: NotesPage(self.theme, self.user_id),
            "quiz":      lambda: QuizPage(self.theme, self.user_id),
            "profile":   lambda: ProfilePage(self.profile, self.user_id, self.theme),
            "settings":  lambda: SettingsPage(self.theme, self._on_theme_change),
            "tools":     lambda: ToolsPage(self.theme),
            "grades":    lambda: GradesPage(self.user_id, self.theme),
            "shortcuts": lambda: ShortcutsPage(self.theme),
            "about":     lambda: AboutPage(self.theme),
            "space_ai":  lambda: SpaceAiPage(self.profile, self.user_id, self.theme),
            "oracle":    lambda: OraclePage(self.theme),
            "guide":     lambda: GuidePage(self.theme),
            "hacking":   lambda: HackingPage(self.profile, self.user_id, self.theme),
            "career":    lambda: CareerPage(self.theme),
            "legal":     lambda: LegalPage(self.profile, self.theme),
        }

        if key in builders:
            try:
                return builders[key]()
            except Exception as e:
                import traceback
                logger.error("Erreur construction '%s' : %s\n%s", key, e, traceback.format_exc())
                return self._error_page(key, str(e), traceback.format_exc())
        return self._placeholder_page(key)

    def _placeholder_page(self, key: str) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background:transparent;")
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        lbl = QLabel(f"⚙️  Module « {key} » en cours de développement…")
        lbl.setFont(QFont("Segoe UI", 14))
        lbl.setStyleSheet(f"color:{self.theme.text_secondary};")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        return page

    def _error_page(self, key: str, err: str, full_trace: str = "") -> QWidget:
        page = QWidget()
        page.setStyleSheet("background:transparent;")
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        lbl = QLabel(f"⚠️  Erreur dans « {key} »\n\n{err}")
        lbl.setFont(QFont("Segoe UI", 12))
        lbl.setStyleSheet(f"color:{self.theme.danger};")
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)

        copy_btn = QPushButton("📋 Copier l'erreur complète")
        copy_btn.setProperty("class", "ghost")
        copy_btn.setFixedWidth(260)
        copy_btn.clicked.connect(
            lambda: QApplication.clipboard().setText(full_trace or err)
        )
        layout.addWidget(copy_btn, alignment=Qt.AlignCenter)
        return page

    # ── Streak (multi-badges) ─────────────────────────────────────────────────

    def _update_streak(self) -> None:
        try:
            today      = datetime.now().date()
            today_str  = today.strftime("%Y-%m-%d")
            yesterday  = (today - timedelta(days=1)).strftime("%Y-%m-%d")
            last_date  = self.profile.get("last_launch_date", "")
            streak     = self.profile.get("streak", 0)

            if last_date == today_str:
                return

            streak = (streak + 1) if last_date == yesterday else 1
            self.profile["streak"]           = streak
            self.profile["last_launch_date"] = today_str

            badges = self.profile.setdefault("badges", [])
            for threshold, badge_name in STREAK_BADGES:
                if streak >= threshold and badge_name not in badges:
                    badges.append(badge_name)
                    logger.info("Badge débloqué : %s", badge_name)

            save_json(PROFILE_FILE, self.profile)
            self.status_bar_widget.refresh_profile(self.profile)
            self.sidebar.refresh_stats(self.profile)
            logger.info("Streak mis à jour : %d jours.", streak)
        except Exception as e:
            logger.error("_update_streak : %s", e)

    # ── Recherche globale groupée ─────────────────────────────────────────────

    def _do_search(self, query: str) -> None:
        query = query.strip().lower()
        if not query:
            return
        logger.info("Recherche : '%s'", query)

        grouped: dict[str, list[tuple[str, str]]] = {}

        def add(category: str, section: str, text: str) -> None:
            grouped.setdefault(category, []).append((section, text))

        try:
            from utils.shortcuts_data import EXCEL_SHORTCUTS, LINUX_COMMANDS, PROF_TRAPS
            for s in EXCEL_SHORTCUTS:
                if query in s.get("key", "").lower() or query in s.get("action", "").lower():
                    add("⚡ Raccourcis", "shortcuts", f"[Excel] {s['key']} → {s['action']}")
            for c in LINUX_COMMANDS:
                if query in c.get("cmd", "").lower() or query in c.get("description", "").lower():
                    add("🔧 Outils", "tools", f"[Linux] {c['cmd']} → {c['description']}")
            for t in PROF_TRAPS:
                if query in t.get("piege", "").lower() or query in t.get("matiere", "").lower():
                    add("🔮 Oracle", "oracle", f"[Piège] [{t['matiere']}] {t['piege']}")
        except Exception as e:
            logger.warning("Recherche shortcuts/oracle : %s", e)

        try:
            from lessons.cours_data import PROGRAMME_COMPLET
            for niveau, ndata in PROGRAMME_COMPLET.items():
                for matiere in ndata.get("cours", {}):
                    if query in matiere.lower():
                        add("📚 Cours", "courses", f"[Cours] {niveau} → {matiere}")
        except Exception as e:
            logger.warning("Recherche cours : %s", e)

        try:
            from database.db_manager import get_notes
            for n in get_notes(DB_FILE, self.user_id):
                if query in n.get("titre", "").lower() or query in n.get("contenu", "").lower():
                    add("📝 Notes", "notes", f"[Note] {n['titre']}")
        except Exception as e:
            logger.warning("Recherche notes : %s", e)

        total = sum(len(v) for v in grouped.values())
        logger.info("Résultats : %d", total)
        self._show_search_dialog(query, grouped)

    def _show_search_dialog(self, query: str, grouped: dict) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Résultats pour « {query} »")
        dialog.setMinimumSize(680, 480)
        dialog.setStyleSheet(get_stylesheet(self.theme))

        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.setSpacing(10)

        total = sum(len(v) for v in grouped.values())
        header = QLabel(f"🔍  Résultats pour « {query} » — {total} trouvé(s)")
        header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        header.setStyleSheet(f"color:{self.theme.accent};")
        dlg_layout.addWidget(header)

        list_w = QListWidget()
        list_w.setStyleSheet(f"""
            QListWidget {{
                background:{self.theme.card}; border:1px solid {self.theme.border};
                border-radius:10px; color:{self.theme.text}; font-size:12px;
            }}
            QListWidget::item {{ padding:8px 12px; border-bottom:1px solid {self.theme.border}44; }}
            QListWidget::item:selected {{ background:{self.theme.accent}33; }}
            QListWidget::item[header="true"] {{
                color:{self.theme.text_secondary}; font-size:11px; font-style:italic;
                background:{self.theme.card}; padding:4px 12px;
            }}
        """)

        if grouped:
            for category, items in grouped.items():
                # Séparateur de catégorie
                sep_item = QListWidgetItem(f"  {category}")
                sep_item.setFlags(Qt.ItemIsEnabled)
                sep_item.setForeground(QColor(self.theme.text_secondary))
                font = QFont("Segoe UI", 10, QFont.Bold)
                font.setItalic(True)
                sep_item.setFont(font)
                list_w.addItem(sep_item)

                for section_key, text in items:
                    item = QListWidgetItem(f"    {text}")
                    item.setData(Qt.UserRole, section_key)
                    list_w.addItem(item)
        else:
            list_w.addItem("🔍  Aucun résultat trouvé dans l'application.")

        def on_double_click(item):
            sec = item.data(Qt.UserRole)
            if sec:
                dialog.accept()
                self._show_section(sec)

        list_w.itemDoubleClicked.connect(on_double_click)
        dlg_layout.addWidget(list_w, 1)

        close_btn = QPushButton("✖ Fermer")
        close_btn.setProperty("class", "ghost")
        close_btn.clicked.connect(dialog.accept)
        dlg_layout.addWidget(close_btn, alignment=Qt.AlignRight)
        dialog.exec()

    # ── Thème ─────────────────────────────────────────────────────────────────

    def _on_theme_change(self, theme_name: str) -> None:
        self.theme_name = theme_name
        self.theme      = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
        self.profile["theme"] = theme_name
        save_json(PROFILE_FILE, self.profile)
        self._apply_theme()
        self.sidebar.refresh_theme(self.theme)
        for w in list(self._page_cache.values()):
            w.deleteLater()
        self._page_cache.clear()
        while self.stack.count():
            self.stack.removeWidget(self.stack.widget(0))
        QTimer.singleShot(100, lambda: self._show_section(self._current_section))
        logger.info("Thème changé → '%s'.", theme_name)

    # ── Zoom ──────────────────────────────────────────────────────────────────

    _zoom_levels = [0.8, 0.9, 1.0, 1.1, 1.25, 1.4, 1.6]
    _zoom_idx    = 2

    def _zoom_in(self) -> None:
        if self._zoom_idx < len(self._zoom_levels) - 1:
            self._zoom_idx += 1
            self._apply_zoom()

    def _zoom_out(self) -> None:
        if self._zoom_idx > 0:
            self._zoom_idx -= 1
            self._apply_zoom()

    def _zoom_reset(self) -> None:
        self._zoom_idx = 2
        self._apply_zoom()

    def _apply_zoom(self) -> None:
        pct = int(self._zoom_levels[self._zoom_idx] * 100)
        self.topbar.zoom_lbl.setText(f"{pct}%")
        app  = QApplication.instance()
        font = app.font()
        font.setPointSize(max(8, int(13 * self._zoom_levels[self._zoom_idx])))
        app.setFont(font)
        self.profile["zoom_idx"] = self._zoom_idx
        save_json(PROFILE_FILE, self.profile)

    # ── Splash ────────────────────────────────────────────────────────────────

    def _show_splash(self) -> None:
        splash = QDialog(self, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        splash.setFixedSize(460, 290)
        splash.setStyleSheet(f"""
            QDialog {{
                background:#080e1c;
                border:1px solid {self.theme.border};
                border-radius:18px;
            }}
        """)
        screen = QApplication.primaryScreen().geometry()
        splash.move((screen.width() - 460) // 2, (screen.height() - 290) // 2)

        layout = QVBoxLayout(splash)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)

        icon_lbl = QLabel("🎓")
        icon_lbl.setFont(QFont("Segoe UI Emoji", 44))
        icon_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_lbl)

        title_lbl = QLabel(APP_NAME)
        title_lbl.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_lbl.setStyleSheet(f"color:{self.theme.accent};")
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)

        uni_lbl = QLabel(f"{UNIVERSITE} — {OPTION}")
        uni_lbl.setFont(QFont("Segoe UI", 10))
        uni_lbl.setStyleSheet("color:#475569;")
        uni_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(uni_lbl)

        progress = QProgressBar()
        progress.setTextVisible(False)
        progress.setFixedHeight(5)
        progress.setRange(0, 100)
        progress.setValue(0)
        progress.setStyleSheet(f"""
            QProgressBar {{ background:#1e293b; border:none; border-radius:3px; }}
            QProgressBar::chunk {{ background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {self.theme.accent}, stop:1 #34d399); border-radius:3px; }}
        """)
        layout.addWidget(progress)

        tip_lbl = QLabel(SPLASH_TIPS[0])
        tip_lbl.setFont(QFont("Segoe UI", 9))
        tip_lbl.setStyleSheet("color:#475569;")
        tip_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(tip_lbl)

        val = [0]
        step = 100 // max(len(SPLASH_TIPS), 1)

        splash.show()

        def animate():
            if not splash.isVisible():
                return
            val[0] = min(val[0] + 2, 100)
            progress.setValue(val[0])
            idx = min(val[0] // step, len(SPLASH_TIPS) - 1)
            tip_lbl.setText(SPLASH_TIPS[idx])
            if val[0] >= 100:
                splash.accept()
            else:
                QTimer.singleShot(18, animate)

        QTimer.singleShot(60, animate)

    # ── Fermeture propre ──────────────────────────────────────────────────────

    def closeEvent(self, event) -> None:
        try:
            save_json(PROFILE_FILE, self.profile)
            save_json(NOTES_FILE, self.notes_data)
        except Exception as e:
            logger.error("Sauvegarde lors de la fermeture : %s", e)

        if self.backend_process and self.backend_process.poll() is None:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=3)
            except Exception as e:
                logger.warning("Arrêt backend : %s", e)

        logger.info("Fermeture propre de %s.", APP_NAME)
        super().closeEvent(event)


# ===========================================================================
# LicenseWindow (redesign : auto-format, 👁, max tentatives)
# ===========================================================================

class LicenseWindow(QWidget):
    license_accepted = Signal()

    def __init__(self, hwid: str, theme: Theme) -> None:
        super().__init__()
        self.hwid            = hwid
        self.theme           = theme
        self._attempts       = 0
        self._key_visible    = False
        self.setWindowTitle(f"{APP_NAME} — Activation")
        self.setFixedSize(600, 540)
        self.setStyleSheet(get_stylesheet(theme))
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 28, 40, 28)
        layout.setSpacing(14)
        layout.setAlignment(Qt.AlignCenter)

        icon_lbl = QLabel("🔐")
        icon_lbl.setFont(QFont("Segoe UI Emoji", 42))
        icon_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_lbl)

        title = QLabel(APP_NAME)
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet(f"color:{self.theme.accent};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(f"{UNIVERSITE} — {OPTION}")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color:#475569;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # HWID card
        hwid_card = Card()
        hwid_l = QVBoxLayout(hwid_card)
        hwid_l.setContentsMargins(20, 14, 20, 14)
        hwid_l.setSpacing(6)

        lbl_s = QLabel("Votre HWID (ID Machine) :")
        lbl_s.setStyleSheet(f"color:{self.theme.text_secondary}; font-size:10px;")
        lbl_s.setAlignment(Qt.AlignCenter)
        hwid_l.addWidget(lbl_s)

        hwid_lbl = QLabel(self.hwid)
        hwid_lbl.setFont(QFont("Consolas", 13, QFont.Bold))
        hwid_lbl.setStyleSheet(f"color:{self.theme.accent};")
        hwid_lbl.setAlignment(Qt.AlignCenter)
        hwid_l.addWidget(hwid_lbl)

        copy_btn = QPushButton("📋 Copier le HWID")
        copy_btn.setProperty("class", "ghost")
        copy_btn.setFixedHeight(28)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(self.hwid))
        hwid_l.addWidget(copy_btn, alignment=Qt.AlignCenter)
        layout.addWidget(hwid_card)

        # Info contact
        info_card = Card()
        info_card.setStyleSheet(
            f"background:{self.theme.success}11; border-color:{self.theme.success}44;"
        )
        info_l = QVBoxLayout(info_card)
        contact_lbl = QLabel(
            f"📱 Contactez {DEV_REAL} sur WhatsApp : {WHATSAPP}\n"
            "Envoyez votre HWID pour recevoir votre clé d'activation."
        )
        contact_lbl.setStyleSheet(f"color:{self.theme.success}; font-size:11px;")
        contact_lbl.setAlignment(Qt.AlignCenter)
        contact_lbl.setWordWrap(True)
        info_l.addWidget(contact_lbl)
        layout.addWidget(info_card)

        # Champ clé + bouton œil
        key_lbl = QLabel("Entrez votre clé d'activation :")
        key_lbl.setStyleSheet(f"color:{self.theme.text};")
        layout.addWidget(key_lbl)

        key_row = QHBoxLayout()
        key_row.setSpacing(6)
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("XXXXX-XXXXX-XXXXX-XXXXX")
        self.key_input.setFixedHeight(42)
        self.key_input.setAlignment(Qt.AlignCenter)
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.textChanged.connect(self._auto_format)
        self.key_input.returnPressed.connect(self._verify)
        key_row.addWidget(self.key_input)

        self._eye_btn = QPushButton("👁")
        self._eye_btn.setFixedSize(42, 42)
        self._eye_btn.setProperty("class", "ghost")
        self._eye_btn.clicked.connect(self._toggle_visibility)
        key_row.addWidget(self._eye_btn)
        layout.addLayout(key_row)

        # Feedback tentatives
        self._feedback_lbl = QLabel("")
        self._feedback_lbl.setStyleSheet("color:#ef4444; font-size:11px;")
        self._feedback_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._feedback_lbl)

        # Bouton activer
        self._activate_btn = QPushButton("✅  Activer la Licence")
        self._activate_btn.setFixedHeight(44)
        self._activate_btn.setProperty("class", "primary")
        self._activate_btn.clicked.connect(self._verify)
        layout.addWidget(self._activate_btn)

    def _auto_format(self, text: str) -> None:
        raw    = text.replace("-", "").upper()[:20]
        parts  = [raw[i:i+5] for i in range(0, len(raw), 5)]
        formatted = "-".join(parts)
        if formatted != text:
            self.key_input.blockSignals(True)
            self.key_input.setText(formatted)
            self.key_input.blockSignals(False)

    def _toggle_visibility(self) -> None:
        self._key_visible = not self._key_visible
        self.key_input.setEchoMode(
            QLineEdit.Normal if self._key_visible else QLineEdit.Password
        )
        self._eye_btn.setText("🙈" if self._key_visible else "👁")

    def _verify(self) -> None:
        if not self._activate_btn.isEnabled():
            return
        from security.security_auth import verify_license, save_license
        key = self.key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer votre clé.")
            return
        if verify_license(self.hwid, key):
            save_license(self.hwid, key)
            QMessageBox.information(self, "✅ Activé", "Licence activée avec succès !\nBienvenue sur Asta Académie.")
            self.license_accepted.emit()
            self.close()
        else:
            self._attempts += 1
            remaining = MAX_LICENSE_ATTEMPTS - self._attempts
            if remaining <= 0:
                self._activate_btn.setEnabled(False)
                self._feedback_lbl.setText("🔒 Trop de tentatives. Relancez l'application.")
                QMessageBox.critical(self, "⛔ Bloqué",
                    f"Nombre maximum de tentatives atteint.\nContactez {DEV_REAL} : {WHATSAPP}")
            else:
                self._feedback_lbl.setText(f"❌ Clé invalide — {remaining} tentative(s) restante(s).")
                QMessageBox.critical(self, "❌ Clé invalide",
                    f"Cette clé ne correspond pas à votre machine.\n"
                    f"Tentatives restantes : {remaining}\nContactez {DEV_REAL} : {WHATSAPP}")


# ===========================================================================
# Point d'entrée
# ===========================================================================

def launch() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("UNASMOH")
    app.setFont(QFont("Segoe UI", 13))

    theme = THEMES[DEFAULT_THEME]

    # Vérification licence
    from security.security_auth import check_license_on_startup
    is_licensed, hwid = check_license_on_startup()

    if not is_licensed:
        lic_win = LicenseWindow(hwid, theme)

        def on_license_accepted():
            lic_win.close()
            _launch_auth(app, theme)

        lic_win.license_accepted.connect(on_license_accepted)
        lic_win.show()
    else:
        _launch_auth(app, theme)

    sys.exit(app.exec())


def _launch_auth(app: QApplication, theme: Theme) -> None:
    try:
        from database.db_manager import init_database
        init_database(DB_FILE)
    except Exception as e:
        logger.error("DB init : %s", e)

    profile = load_json(PROFILE_FILE, {})

    if not profile.get("nom"):
        from views.login_page import LoginPage, apply_theme
        # Apply theme globals to the login view
        apply_theme(theme)
        login = LoginPage(theme)

        def on_login(prof: dict, uid: int) -> None:
            login.close()
            _open_main(app, theme, prof, uid)

        login.login_success.connect(on_login)
        login.show()
    else:
        from database.db_manager import DBManager
        try:
            user = DBManager.get_user_by_name(profile["nom"])
            uid  = user["id"] if user else 1
        except Exception as e:
            logger.warning("get_user_by_name : %s", e)
            uid = 1
        _open_main(app, theme, profile, uid)


def _open_main(app: QApplication, theme: Theme, profile: dict, user_id: int) -> None:
    win = AstaAcademieWindow(profile, user_id)
    win.show()


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    launch()
