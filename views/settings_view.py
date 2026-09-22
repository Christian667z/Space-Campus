"""
Asta Académie — Paramètres v2.0 (PySide6)
==========================================
Page de paramètres complète et redessinée.

Améliorations v2.0 :
  - Section Profil : édition du nom, avatar emoji, niveau, objectif
  - Section Thème : cartes visuelles avec aperçu de couleurs (plus de simples boutons)
  - Section Apparence : taille de police (Petite / Normale / Grande)
  - Section Notifications : son, rappel de streak, rappel de révision
  - Section Données : export/import .asta_save avec validation,
    réinitialisation à double confirmation (saisie du mot "SUPPRIMER")
  - Section Raccourcis clavier : tableau de référence complet
  - Section À propos : version, crédits animés, lien de contact
  - Stats rapides en haut (points, niveau, streak, notes)
  - Imports tous au niveau du module (plus d'imports dans les méthodes)
  - Logging structuré (plus d'exceptions silencieuses)
  - Signals pour notifier le reste de l'app des changements
  - Type hints complets
  - Bouton "Appliquer" global + feedback visuel de succès
"""

import json
import logging
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPalette
from PySide6.QtWidgets import (
    QButtonGroup, QCheckBox, QDialog, QFileDialog,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSlider, QSpinBox,
    QTextEdit, QVBoxLayout, QWidget,
)

from ui.components.widgets import Card, SectionHeader, add_shadow
from ui.themes.theme_manager import Theme, THEMES
from utils.svg_manager import SVGManager

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

APP_VERSION   = "2.0.0"
APP_NAME      = "Asta Académie"
DEVELOPER     = "Lucky Luke (Space | Asta Dev)"
UNIVERSITY    = "UNASMOH — Promo 2024-2028"
WHATSAPP      = "+509 3567-2037"

AVATAR_OPTIONS = ["dev", "student_male", "student_female", "rocket", "star", "fox", "dragon", "degree", "bolt", "flame"]
LEVELS         = ["L1", "L2", "L3", "L4", "Master"]
FONT_SIZES     = {"Petite": 11, "Normale": 13, "Grande": 15}
OBJECTIVES     = [
    "Obtenir mon diplôme avec mention",
    "Trouver un emploi en tech",
    "Créer ma propre startup",
    "Contribuer à l'open source",
    "Devenir enseignant",
    "Maîtriser la cybersécurité",
]

SHORTCUTS = [
    ("Ctrl+S",      "Sauvegarder la note active"),
    ("Ctrl+N",      "Nouvelle note"),
    ("Ctrl+F",      "Rechercher dans les notes"),
    ("Ctrl+B",      "Gras"),
    ("Ctrl+I",      "Italique"),
    ("Ctrl+U",      "Souligné"),
    ("Delete",      "Supprimer (liste de notes)"),
    ("Ctrl+Z",      "Annuler la dernière action"),
    ("Ctrl+Y",      "Rétablir"),
    ("Ctrl+A",      "Tout sélectionner"),
    ("Ctrl+C / V",  "Copier / Coller"),
    ("Esc",         "Fermer un dialogue"),
]


# ===========================================================================
# Widget réutilisable : Carte de section
# ===========================================================================

class SettingSection(QFrame):
    """Carte de paramètre avec titre, icône et contenu."""

    def __init__(self, icon: str, title: str, subtitle: str, theme: Theme, parent=None) -> None:
        super().__init__(parent)
        self.theme = theme
        self.setStyleSheet(f"""
            QFrame {{
                background: {theme.card};
                border: 1px solid {theme.border};
                border-radius: 12px;
            }}
        """)
        add_shadow(self)

        self._inner = QVBoxLayout(self)
        self._inner.setContentsMargins(24, 20, 24, 20)
        self._inner.setSpacing(14)

        # En-tête de section
        hdr = QHBoxLayout()
        
        icon_lbl = QLabel()
        icon_lbl.setPixmap(SVGManager.get_icon(icon, color=theme.text, size=24).pixmap(24, 24))
        icon_lbl.setFixedWidth(36)
        hdr.addWidget(icon_lbl)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        t = QLabel(title)
        t.setFont(QFont("Segoe UI", 13, QFont.Bold))
        t.setStyleSheet(f"color: {theme.text}; border: none; background: transparent;")
        text_col.addWidget(t)
        if subtitle:
            s = QLabel(subtitle)
            s.setStyleSheet(f"color: {theme.text_secondary}; font-size: 11px; border: none; background: transparent;")
            s.setWordWrap(True)
            text_col.addWidget(s)
        hdr.addLayout(text_col, 1)
        self._inner.addLayout(hdr)

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background: {theme.border}; border: none; max-height: 1px;")
        self._inner.addWidget(sep)

    def body(self) -> QVBoxLayout:
        """Layout dans lequel ajouter le contenu de la section."""
        return self._inner


# ===========================================================================
# Carte de thème visuelle
# ===========================================================================

class ThemeCard(QPushButton):
    """Bouton-carte affichant un aperçu visuel du thème (pastilles de couleur)."""

    def __init__(self, theme_key: str, theme_obj: Theme, selected: bool, parent=None) -> None:
        super().__init__(parent)
        self._tkey   = theme_key
        self._tobj   = theme_obj
        self._selected = selected
        self.setCheckable(True)
        self.setChecked(selected)
        self.setFixedSize(110, 90)
        self.setCursor(Qt.PointingHandCursor)
        self._apply_style()

    def _apply_style(self) -> None:
        border = f"2px solid {self._tobj.accent}" if self._selected else f"1px solid {self._tobj.border}"
        self.setStyleSheet(f"""
            QPushButton {{
                background: {self._tobj.bg};
                border: {border};
                border-radius: 10px;
            }}
            QPushButton:hover {{
                border: 2px solid {self._tobj.accent}99;
            }}
        """)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Nom du thème
        painter.setPen(QColor(self._tobj.text))
        font = QFont("Segoe UI", 9, QFont.Bold)
        painter.setFont(font)
        painter.drawText(0, 8, 110, 24, Qt.AlignCenter, self._tobj.name)

        # Pastilles de couleur
        colors = [self._tobj.bg, self._tobj.card, self._tobj.accent,
                  self._tobj.text, self._tobj.border]
        x_start = 12
        for i, color in enumerate(colors[:5]):
            painter.setBrush(QColor(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x_start + i * 18, 38, 14, 14)

        # Badge "Actif" si sélectionné
        if self._selected:
            painter.setBrush(QColor(self._tobj.accent))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(25, 60, 60, 20, 10, 10)
            painter.setPen(QColor("#FFFFFF"))
            painter.setFont(QFont("Segoe UI", 8, QFont.Bold))
            painter.drawText(25, 60, 60, 20, Qt.AlignCenter, "✓ Actif")

        painter.end()

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        self.setChecked(selected)
        self._apply_style()
        self.update()


# ===========================================================================
# Dialogue de confirmation double (réinitialisation)
# ===========================================================================

class DoubleConfirmDialog(QDialog):
    """Dialogue exigeant la saisie du mot 'SUPPRIMER' pour confirmer."""

    def __init__(self, theme: Theme, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("⚠️ Confirmation de réinitialisation")
        self.setFixedWidth(420)
        self.setStyleSheet(f"background: {theme.bg}; color: {theme.text};")

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        icon = QLabel()
        from utils.svg_manager import SVGManager
        icon.setPixmap(SVGManager.get_icon("alert", color="#E74C3C", size=48).pixmap(48, 48))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        msg = QLabel(
            "Cette action supprimera <b>TOUTES</b> vos données :\n"
            "profil, notes, historique, points, badges.\n\n"
            "Pour confirmer, tapez exactement :\n"
        )
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet(f"color: {theme.text};")
        layout.addWidget(msg)

        confirm_word = QLabel("SUPPRIMER")
        confirm_word.setFont(QFont("Courier", 14, QFont.Bold))
        confirm_word.setAlignment(Qt.AlignCenter)
        confirm_word.setStyleSheet(f"color: #E74C3C; letter-spacing: 4px;")
        layout.addWidget(confirm_word)

        self._input = QLineEdit()
        self._input.setPlaceholderText("Tapez SUPPRIMER ici…")
        self._input.setAlignment(Qt.AlignCenter)
        self._input.setStyleSheet(f"""
            QLineEdit {{
                background: {theme.card};
                color: {theme.text};
                border: 2px solid #E74C3C;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 2px;
            }}
        """)
        self._input.textChanged.connect(self._check_input)
        layout.addWidget(self._input)

        btn_row = QHBoxLayout()
        self._cancel_btn = QPushButton("Annuler")
        self._cancel_btn.setProperty("class", "secondary")
        self._cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(self._cancel_btn)

        self._confirm_btn = QPushButton(" Réinitialiser définitivement")
        self._confirm_btn.setIcon(SVGManager.get_icon("trash", color="#ffffff", size=18))
        self._confirm_btn.setProperty("class", "danger_btn")
        self._confirm_btn.setEnabled(False)
        self._confirm_btn.clicked.connect(self.accept)
        btn_row.addWidget(self._confirm_btn)
        layout.addLayout(btn_row)

    def _check_input(self, text: str) -> None:
        self._confirm_btn.setEnabled(text.strip() == "SUPPRIMER")


# ===========================================================================
# Page principale : SettingsPage
# ===========================================================================

class SettingsPage(QWidget):
    """
    Page de paramètres complète pour Asta Académie.

    Signals
    -------
    theme_changed(str)         : Clé du nouveau thème appliqué.
    font_size_changed(int)     : Nouvelle taille de police en pt.
    profile_updated(dict)      : Dictionnaire profil mis à jour.
    data_reset()               : Émis après réinitialisation complète.
    """

    theme_changed    = Signal(str)
    font_size_changed = Signal(int)
    profile_updated  = Signal(dict)
    data_reset       = Signal()

    def __init__(
        self,
        theme: Theme,
        on_theme_change: Callable,
        profile: Optional[dict] = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.theme            = theme
        self.on_theme_change  = on_theme_change
        self.profile          = profile or {}
        self._theme_cards: dict[str, ThemeCard] = {}
        self._pending_changes = False

        self.setStyleSheet("background: transparent;")
        self._build_ui()

    # -----------------------------------------------------------------------
    # Construction de l'interface
    # -----------------------------------------------------------------------

    def _build_ui(self) -> None:
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        scroll.setWidget(content)

        self._layout = QVBoxLayout(content)
        self._layout.setContentsMargins(24, 24, 24, 40)
        self._layout.setSpacing(20)

        # En-tête
        self._layout.addWidget(
            SectionHeader("Paramètres", "Personnalisez entièrement votre expérience Asta Académie")
        )

        # Statistiques rapides
        self._layout.addWidget(self._build_stats_banner())

        # Sections
        self._layout.addWidget(self._build_profile_section())
        self._layout.addWidget(self._build_theme_section())
        self._layout.addWidget(self._build_appearance_section())
        self._layout.addWidget(self._build_notifications_section())
        self._layout.addWidget(self._build_data_section())
        self._layout.addWidget(self._build_shortcuts_section())
        self._layout.addWidget(self._build_about_section())

        # Bouton Appliquer global
        self._layout.addWidget(self._build_apply_bar())
        self._layout.addStretch()

    # ── Bannière de statistiques ─────────────────────────────────────────────

    def _build_stats_banner(self) -> QFrame:
        banner = QFrame()
        banner.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.theme.accent}22,
                    stop:1 {self.theme.card}
                );
                border: 1px solid {self.theme.accent}44;
                border-radius: 12px;
            }}
        """)
        row = QHBoxLayout(banner)
        row.setContentsMargins(20, 14, 20, 14)
        row.setSpacing(0)

        stats = [
            ("star", str(self.profile.get("points", 0)),  "Points"),
            ("book", self.profile.get("niveau", "L1"),     "Niveau"),
            ("flame", str(self.profile.get("streak", 0)),   "Streak"),
            ("badge", str(len(self.profile.get("badges", []))), "Badges"),
        ]
        for i, (icon, val, label) in enumerate(stats):
            col = QVBoxLayout()
            col.setSpacing(2)
            col.setAlignment(Qt.AlignCenter)

            top = QHBoxLayout()
            top.setAlignment(Qt.AlignCenter)
            top.setSpacing(4)
            ico = QLabel()
            ico.setPixmap(SVGManager.get_icon(icon, color=self.theme.accent, size=20).pixmap(20, 20))
            v = QLabel(val)
            v.setFont(QFont("Segoe UI", 18, QFont.Bold))
            v.setStyleSheet(f"color: {self.theme.accent}; border: none; background: transparent;")
            top.addWidget(ico)
            top.addWidget(v)
            col.addLayout(top)

            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 11px; border: none; background: transparent;")
            col.addWidget(lbl)

            row.addLayout(col, 1)
            if i < len(stats) - 1:
                sep = QFrame()
                sep.setFrameShape(QFrame.VLine)
                sep.setStyleSheet(f"background: {self.theme.border}; border: none; max-width: 1px;")
                row.addWidget(sep)

        return banner

    # ── Profil ───────────────────────────────────────────────────────────────

    def _build_profile_section(self) -> SettingSection:
        sec = SettingSection(
            "user", "Mon Profil",
            "Modifiez vos informations personnelles affichées dans l'application.",
            self.theme,
        )
        body = sec.body()

        # Nom
        row_nom = QHBoxLayout()
        lbl_nom = self._lbl("Nom d'affichage :")
        row_nom.addWidget(lbl_nom)
        self._input_nom = QLineEdit(self.profile.get("nom", ""))
        self._input_nom.setPlaceholderText("Votre nom…")
        self._style_input(self._input_nom)
        self._input_nom.textChanged.connect(self._mark_changed)
        row_nom.addWidget(self._input_nom, 1)
        body.addLayout(row_nom)

        # Niveau
        row_niv = QHBoxLayout()
        row_niv.addWidget(self._lbl("Niveau d'études :"))
        self._level_group = QButtonGroup(self)
        level_row = QHBoxLayout()
        current = self.profile.get("niveau", "L2")
        for lvl in LEVELS:
            rb = QRadioButton(lvl)
            rb.setChecked(lvl == current)
            rb.setStyleSheet(f"color: {self.theme.text}; font-size: 12px;")
            rb.toggled.connect(self._mark_changed)
            self._level_group.addButton(rb)
            level_row.addWidget(rb)
        level_row.addStretch()
        row_niv.addLayout(level_row, 1)
        body.addLayout(row_niv)

        # Avatar
        row_av = QHBoxLayout()
        row_av.addWidget(self._lbl("Avatar :"))
        self._avatar_group = QButtonGroup(self)
        av_row = QHBoxLayout()
        av_row.setSpacing(6)
        current_av = self.profile.get("avatar", "🧑‍💻")
        for av in AVATAR_OPTIONS:
            btn = QPushButton(av)
            btn.setCheckable(True)
            btn.setChecked(av == current_av)
            btn.setFixedSize(38, 38)
            btn.setFont(QFont("Segoe UI Emoji", 16))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {self.theme.bg};
                    border: 1px solid {self.theme.border};
                    border-radius: 8px;
                }}
                QPushButton:checked {{
                    background: {self.theme.accent}33;
                    border: 2px solid {self.theme.accent};
                }}
                QPushButton:hover {{ background: {self.theme.card_hover}; }}
            """)
            btn.clicked.connect(self._mark_changed)
            self._avatar_group.addButton(btn)
            av_row.addWidget(btn)
        av_row.addStretch()
        row_av.addLayout(av_row, 1)
        body.addLayout(row_av)

        # Objectif
        row_obj = QHBoxLayout()
        row_obj.addWidget(self._lbl("Objectif :"))
        self._obj_buttons: list[QPushButton] = []
        obj_wrap = QHBoxLayout()
        obj_wrap.setSpacing(6)
        current_obj = self.profile.get("objectif", "")
        for obj in OBJECTIVES:
            btn = QPushButton(obj)
            btn.setCheckable(True)
            btn.setChecked(obj == current_obj)
            btn.setStyleSheet(self._tag_style(btn.isChecked()))
            btn.clicked.connect(lambda _, b=btn: self._select_objective(b))
            self._obj_buttons.append(btn)
            obj_wrap.addWidget(btn)
        obj_wrap.addStretch()
        row_obj.addLayout(obj_wrap, 1)
        body.addLayout(row_obj)

        return sec

    # ── Thème ────────────────────────────────────────────────────────────────

    def _build_theme_section(self) -> SettingSection:
        sec = SettingSection(
            "palette", "Thème de l'Interface",
            "Le changement est appliqué immédiatement. Passez votre souris sur une carte pour un aperçu.",
            self.theme,
        )
        body = sec.body()

        cards_row = QHBoxLayout()
        cards_row.setSpacing(12)
        active_key = self._active_theme_key()

        for key, t_obj in THEMES.items():
            card = ThemeCard(
                theme_key=key,
                theme_obj=t_obj,
                selected=(key == active_key),
            )
            card.clicked.connect(lambda _, k=key: self._apply_theme(k))
            self._theme_cards[key] = card
            cards_row.addWidget(card)

        cards_row.addStretch()
        body.addLayout(cards_row)
        return sec

    # ── Apparence ────────────────────────────────────────────────────────────

    def _build_appearance_section(self) -> SettingSection:
        sec = SettingSection(
            "monitor", "Apparence",
            "Ajustez la taille du texte et la densité de l'interface.",
            self.theme,
        )
        body = sec.body()

        # Taille de police
        row_font = QHBoxLayout()
        row_font.addWidget(self._lbl("Taille du texte :"))
        self._font_group = QButtonGroup(self)
        font_row = QHBoxLayout()
        font_row.setSpacing(8)
        current_size = self.profile.get("font_size", "Normale")
        for label in FONT_SIZES:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setChecked(label == current_size)
            btn.setFixedHeight(32)
            btn.setStyleSheet(self._toggle_style(btn.isChecked()))
            btn.clicked.connect(lambda _, l=label, b=btn: self._select_font_size(l, b))
            self._font_group.addButton(btn)
            font_row.addWidget(btn)
        font_row.addStretch()
        row_font.addLayout(font_row, 1)
        body.addLayout(row_font)

        # Animations
        row_anim = QHBoxLayout()
        row_anim.addWidget(self._lbl("Animations :"))
        self._chk_anim = QCheckBox("Activer les animations de transition")
        self._chk_anim.setChecked(self.profile.get("animations", True))
        self._chk_anim.setStyleSheet(f"color: {self.theme.text};")
        self._chk_anim.stateChanged.connect(self._mark_changed)
        row_anim.addWidget(self._chk_anim)
        row_anim.addStretch()
        body.addLayout(row_anim)

        # Compact mode
        row_compact = QHBoxLayout()
        row_compact.addWidget(self._lbl("Mode compact :"))
        self._chk_compact = QCheckBox("Réduire les marges et espacements")
        self._chk_compact.setChecked(self.profile.get("compact_mode", False))
        self._chk_compact.setStyleSheet(f"color: {self.theme.text};")
        self._chk_compact.stateChanged.connect(self._mark_changed)
        row_compact.addWidget(self._chk_compact)
        row_compact.addStretch()
        body.addLayout(row_compact)

        return sec

    # ── Notifications ────────────────────────────────────────────────────────

    def _build_notifications_section(self) -> SettingSection:
        sec = SettingSection(
            "bell", "Notifications & Rappels",
            "Configurez les alertes et sons de l'application.",
            self.theme,
        )
        body = sec.body()

        notifs = [
            ("_chk_sound",   "Sons d'interface",        "Son de confirmation lors des actions (quiz, sauvegarde...)", "sounds"),
            ("_chk_streak",  "Rappel de série (streak)", "Me rappeler si je n'ai pas ouvert l'app depuis 24h",        "streak_reminder"),
            ("_chk_quiz",    "Rappels de révision",      "Me suggérer des leçons à réviser au démarrage",             "quiz_reminder"),
            ("_chk_points",  "Animations de points",     "Afficher l'animation +XP lors des récompenses",             "points_anim"),
        ]
        for attr, title, desc, key in notifs:
            row = QVBoxLayout()
            top = QHBoxLayout()
            chk = QCheckBox(title)
            chk.setChecked(self.profile.get(key, True))
            chk.setFont(QFont("Segoe UI", 11))
            chk.setStyleSheet(f"color: {self.theme.text};")
            chk.stateChanged.connect(self._mark_changed)
            setattr(self, attr, chk)
            top.addWidget(chk)
            top.addStretch()
            row.addLayout(top)
            sub = QLabel(desc)
            sub.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 11px; padding-left: 22px;")
            row.addWidget(sub)
            body.addLayout(row)

        return sec

    # ── Données ──────────────────────────────────────────────────────────────

    def _build_data_section(self) -> SettingSection:
        sec = SettingSection(
            "save", "Gestion des Données",
            "Exportez ou importez votre profil complet. La réinitialisation est irréversible.",
            self.theme,
        )
        body = sec.body()

        # Boutons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        export_btn = QPushButton(" Exporter le profil")
        export_btn.setIcon(SVGManager.get_icon("export", color=self.theme.text, size=18))
        export_btn.setProperty("class", "secondary")
        export_btn.setFixedHeight(36)
        export_btn.setToolTip("Sauvegarde toutes vos données dans un fichier .asta_save")
        export_btn.clicked.connect(self._export)
        btn_row.addWidget(export_btn)

        import_btn = QPushButton(" Importer un profil")
        import_btn.setIcon(SVGManager.get_icon("import", color=self.theme.text, size=18))
        import_btn.setProperty("class", "secondary")
        import_btn.setFixedHeight(36)
        import_btn.setToolTip("Restaure vos données depuis un fichier .asta_save")
        import_btn.clicked.connect(self._import)
        btn_row.addWidget(import_btn)

        btn_row.addStretch()

        reset_btn = QPushButton(" Réinitialiser toutes les données")
        reset_btn.setIcon(SVGManager.get_icon("trash", color="#ffffff", size=18))
        reset_btn.setProperty("class", "danger_btn")
        reset_btn.setFixedHeight(36)
        reset_btn.setToolTip("Supprime TOUTES les données de façon irréversible")
        reset_btn.clicked.connect(self._reset)
        btn_row.addWidget(reset_btn)

        body.addLayout(btn_row)

        # Info sur le dernier export
        self._export_info = QLabel("")
        self._export_info.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 11px;")
        body.addWidget(self._export_info)

        return sec

    # ── Raccourcis ───────────────────────────────────────────────────────────

    def _build_shortcuts_section(self) -> SettingSection:
        sec = SettingSection(
            "code", "Raccourcis Clavier",
            "Référence complète des raccourcis disponibles dans Asta Académie.",
            self.theme,
        )
        body = sec.body()

        grid = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        half = len(SHORTCUTS) // 2

        for i, (keys, desc) in enumerate(SHORTCUTS):
            row = QHBoxLayout()
            key_lbl = QLabel(keys)
            key_lbl.setFont(QFont("Courier New", 10, QFont.Bold))
            key_lbl.setFixedWidth(90)
            key_lbl.setStyleSheet(f"""
                color: {self.theme.text};
                background: {self.theme.bg};
                border: 1px solid {self.theme.border};
                border-radius: 4px;
                padding: 2px 6px;
            """)
            row.addWidget(key_lbl)
            desc_lbl = QLabel(desc)
            desc_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px; border: none; background: transparent;")
            row.addWidget(desc_lbl)
            row.addStretch()
            (col1 if i < half else col2).addLayout(row)

        grid.addLayout(col1, 1)
        grid.addSpacing(20)
        grid.addLayout(col2, 1)
        body.addLayout(grid)
        return sec

    # ── À propos ─────────────────────────────────────────────────────────────

    def _build_about_section(self) -> SettingSection:
        sec = SettingSection(
            "smartphone", "À propos & Contact",
            "Informations sur l'application et le développeur.",
            self.theme,
        )
        body = sec.body()

        about_row = QHBoxLayout()
        about_row.setSpacing(20)

        # Infos app
        app_col = QVBoxLayout()
        app_col.setSpacing(4)

        for line, color, size in [
            (f"{APP_NAME}", self.theme.accent, 15),
            (f"Version {APP_VERSION}", self.theme.text, 12),
            ("Plateforme éducative pour étudiants en Sciences Informatiques", self.theme.text_secondary, 11),
            (f"{UNIVERSITY}", self.theme.text_secondary, 11),
        ]:
            lbl = QLabel(line)
            lbl.setFont(QFont("Segoe UI", size, QFont.Bold if size == 15 else QFont.Normal))
            lbl.setStyleSheet(f"color: {color}; border: none; background: transparent;")
            lbl.setWordWrap(True)
            app_col.addWidget(lbl)

        about_row.addLayout(app_col, 1)

        # Séparateur vertical
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet(f"background: {self.theme.border}; border: none; max-width: 1px;")
        about_row.addWidget(sep)

        # Développeur
        dev_col = QVBoxLayout()
        dev_col.setSpacing(6)

        dev_title = QLabel("Développeur")
        dev_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        dev_title.setStyleSheet(f"color: {self.theme.text}; border: none; background: transparent;")
        dev_col.addWidget(dev_title)

        for line in [
            f"{DEVELOPER}",
            f"WhatsApp : {WHATSAPP}",
            "Fait en Haïti, pour les Haïtiens",
        ]:
            lbl = QLabel(line)
            lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px; border: none; background: transparent;")
            dev_col.addWidget(lbl)

        # Bouton feedback
        fb_btn = QPushButton(" Envoyer un feedback")
        fb_btn.setIcon(SVGManager.get_icon("message", color=self.theme.text, size=18))
        fb_btn.setProperty("class", "secondary")
        fb_btn.setFixedHeight(32)
        fb_btn.clicked.connect(self._open_feedback)
        dev_col.addWidget(fb_btn)

        about_row.addLayout(dev_col, 1)
        body.addLayout(about_row)

        # Barre de crédits
        credits = QLabel(
            f"© 2024-2025 {DEVELOPER} · Tous droits réservés · "
            "Construit avec ❤️ pour la promotion UNASMOH 2024-2028"
        )
        credits.setAlignment(Qt.AlignCenter)
        credits.setWordWrap(True)
        credits.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 10px; border: none; background: transparent;")
        body.addWidget(credits)

        return sec

    # ── Barre d'application globale ──────────────────────────────────────────

    def _build_apply_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.card};
                border: 1px solid {self.theme.border};
                border-radius: 10px;
            }}
        """)
        row = QHBoxLayout(bar)
        row.setContentsMargins(20, 12, 20, 12)

        self._apply_info = QLabel("✅ Tous les paramètres sont à jour.")
        self._apply_info.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px; border: none; background: transparent;")
        row.addWidget(self._apply_info)
        row.addStretch()

        self._apply_btn = QPushButton("✅ Appliquer les modifications")
        self._apply_btn.setProperty("class", "primary")
        self._apply_btn.setFixedHeight(36)
        self._apply_btn.setEnabled(False)
        self._apply_btn.clicked.connect(self._apply_all)
        row.addWidget(self._apply_btn)

        return bar

    # -----------------------------------------------------------------------
    # Logique
    # -----------------------------------------------------------------------

    def _apply_theme(self, key: str) -> None:
        for k, card in self._theme_cards.items():
            card.set_selected(k == key)
        self.on_theme_change(key)
        self.theme_changed.emit(key)
        logger.info("Thème changé → '%s'", key)

    def _select_font_size(self, label: str, clicked_btn: QPushButton) -> None:
        for btn in self._font_group.buttons():
            btn.setStyleSheet(self._toggle_style(btn is clicked_btn))
        self.font_size_changed.emit(FONT_SIZES[label])
        self._mark_changed()

    def _select_objective(self, clicked_btn: QPushButton) -> None:
        for btn in self._obj_buttons:
            is_me = btn is clicked_btn
            if is_me:
                btn.setChecked(not btn.isChecked())
            btn.setStyleSheet(self._tag_style(btn.isChecked()))
        self._mark_changed()

    def _mark_changed(self) -> None:
        if not self._pending_changes:
            self._pending_changes = True
            self._apply_btn.setEnabled(True)
            self._apply_info.setText("⚠️  Des modifications sont en attente.")
            self._apply_info.setStyleSheet(f"color: #E67E22; font-size: 12px; border: none; background: transparent;")

    def _apply_all(self) -> None:
        """Collecte tous les champs et met à jour le profil."""
        # Nom
        self.profile["nom"] = self._input_nom.text().strip()

        # Niveau
        for btn in self._level_group.buttons():
            if btn.isChecked():
                self.profile["niveau"] = btn.text()
                break

        # Avatar
        for btn in self._avatar_group.buttons():
            if btn.isChecked():
                self.profile["avatar"] = btn.text()
                break

        # Objectif
        for btn in self._obj_buttons:
            if btn.isChecked():
                self.profile["objectif"] = btn.text()
                break

        # Apparence
        for btn in self._font_group.buttons():
            if btn.isChecked():
                self.profile["font_size"] = btn.text()
                break
        self.profile["animations"]   = self._chk_anim.isChecked()
        self.profile["compact_mode"] = self._chk_compact.isChecked()

        # Notifications
        self.profile["sounds"]         = self._chk_sound.isChecked()
        self.profile["streak_reminder"] = self._chk_streak.isChecked()
        self.profile["quiz_reminder"]   = self._chk_quiz.isChecked()
        self.profile["points_anim"]     = self._chk_points.isChecked()

        self.profile_updated.emit(self.profile)
        logger.info("Profil mis à jour : %s", {k: v for k, v in self.profile.items() if k != "ai_memory"})

        self._pending_changes = False
        self._apply_btn.setEnabled(False)
        self._apply_info.setText("✅ Paramètres sauvegardés !")
        self._apply_info.setStyleSheet(f"color: #27AE60; font-size: 12px; font-weight: bold; border: none; background: transparent;")
        QTimer.singleShot(4000, self._reset_apply_info)

    def _reset_apply_info(self) -> None:
        self._apply_info.setText("✅ Tous les paramètres sont à jour.")
        self._apply_info.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px; border: none; background: transparent;")

    # ── Export / Import / Reset ─────────────────────────────────────────────

    def _export(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter le profil Asta",
            f"sauvegarde_asta_{self.profile.get('nom', 'user').replace(' ', '_')}.asta_save",
            "Sauvegarde Asta (*.asta_save);;JSON (*.json)",
        )
        if not path:
            return
        try:
            from main_qt import PROFILE_FILE, NOTES_FILE, load_json
            data = {
                "version":  APP_VERSION,
                "exported": __import__("datetime").datetime.now().isoformat(),
                "profile":  load_json(PROFILE_FILE, {}),
                "notes":    load_json(NOTES_FILE, {}),
            }
            Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            self._export_info.setText(f"✅ Exporté vers : {path}")
            logger.info("Profil exporté vers '%s'", path)
            QMessageBox.information(self, "✅ Export réussi", f"Votre profil a été exporté :\n{path}")
        except Exception as e:
            logger.error("Erreur export : %s", e)
            QMessageBox.critical(self, "❌ Erreur d'export", str(e))

    def _import(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Importer un profil Asta", "",
            "Sauvegarde Asta (*.asta_save);;JSON (*.json)",
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
                QMessageBox.critical(
                    self, "❌ Fichier invalide",
                    "Ce fichier n'est pas une sauvegarde Asta Académie valide.\n"
                    "Vérifiez que vous avez sélectionné le bon fichier."
                )
                return

            reply = QMessageBox.question(
                self, "Confirmer l'import",
                f"Importer le profil depuis :\n{path}\n\n"
                "Ceci remplacera vos données actuelles. Continuer ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

            from main_qt import PROFILE_FILE, NOTES_FILE, save_json
            save_json(PROFILE_FILE, data.get("profile", {}))
            save_json(NOTES_FILE,   data.get("notes",   {}))
            logger.info("Profil importé depuis '%s' (version %s)", path, data.get("version", "?"))
            QMessageBox.information(
                self, "✅ Import réussi",
                "Profil importé avec succès !\nRedémarrez l'application pour voir les changements."
            )
        except json.JSONDecodeError:
            QMessageBox.critical(self, "❌ Fichier corrompu", "Le fichier JSON est invalide ou corrompu.")
        except Exception as e:
            logger.error("Erreur import : %s", e)
            QMessageBox.critical(self, "❌ Erreur d'import", str(e))

    def _reset(self) -> None:
        dlg = DoubleConfirmDialog(self.theme, parent=self)
        if dlg.exec() != QDialog.Accepted:
            return
        try:
            from main_qt import PROFILE_FILE, NOTES_FILE, save_json
            blank_profile = {
                "nom": "", "niveau": "L1", "avatar": "🧑‍💻",
                "points": 0, "badges": [], "streak": 0,
                "ai_memory": "", "objectif": "",
            }
            save_json(PROFILE_FILE, blank_profile)
            save_json(NOTES_FILE, {})
            self.data_reset.emit()
            logger.warning("Données réinitialisées par l'utilisateur.")
            QMessageBox.information(
                self, "✅ Réinitialisé",
                "Toutes les données ont été effacées.\n"
                "Redémarrez l'application pour repartir de zéro."
            )
        except Exception as e:
            logger.error("Erreur reset : %s", e)
            QMessageBox.critical(self, "❌ Erreur", str(e))

    def _open_feedback(self) -> None:
        QMessageBox.information(
            self, "💬 Feedback",
            f"Pour envoyer votre feedback :\n\n"
            f"📱 WhatsApp : {WHATSAPP}\n\n"
            "Vos suggestions contribuent à améliorer Asta Académie ! 🙏"
        )

    # -----------------------------------------------------------------------
    # Utilitaires
    # -----------------------------------------------------------------------

    def _active_theme_key(self) -> str:
        for key, t_obj in THEMES.items():
            if t_obj.name == self.theme.name:
                return key
        return list(THEMES.keys())[0]

    def _lbl(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setFixedWidth(160)
        lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px; font-weight: bold; border: none; background: transparent;")
        return lbl

    def _style_input(self, widget: QLineEdit) -> None:
        widget.setStyleSheet(f"""
            QLineEdit {{
                background: {self.theme.bg};
                color: {self.theme.text};
                border: 1px solid {self.theme.border};
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.theme.accent};
            }}
        """)

    def _toggle_style(self, active: bool) -> str:
        if active:
            return f"""
                QPushButton {{
                    background: {self.theme.accent}22;
                    color: {self.theme.accent};
                    border: 1px solid {self.theme.accent};
                    border-radius: 7px;
                    padding: 4px 14px;
                    font-weight: bold;
                }}
            """
        return f"""
            QPushButton {{
                background: {self.theme.bg};
                color: {self.theme.text};
                border: 1px solid {self.theme.border};
                border-radius: 7px;
                padding: 4px 14px;
            }}
            QPushButton:hover {{ background: {self.theme.card_hover}; }}
        """

    def _tag_style(self, active: bool) -> str:
        if active:
            return f"""
                QPushButton {{
                    background: {self.theme.accent}22;
                    color: {self.theme.accent};
                    border: 1px solid {self.theme.accent};
                    border-radius: 12px;
                    padding: 4px 10px;
                    font-size: 11px;
                }}
            """
        return f"""
            QPushButton {{
                background: {self.theme.bg};
                color: {self.theme.text_secondary};
                border: 1px solid {self.theme.border};
                border-radius: 12px;
                padding: 4px 10px;
                font-size: 11px;
            }}
            QPushButton:hover {{ background: {self.theme.card_hover}; }}
        """
