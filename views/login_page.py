"""
Asta Académie — LoginPage v2.0 (PySide6)
=========================================
Fenêtre de connexion/inscription en split-layout premium, avec système de design unifié.
"""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Optional

from PySide6.QtCore import (
    Qt, Signal, QPropertyAnimation, QEasingCurve, QTimer, QRect,
)
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QCheckBox, QFrame, QSizePolicy,
    QGraphicsOpacityEffect, QMessageBox,
)
import re

from ui.themes.theme_manager import Theme, get_stylesheet

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes de Branding & Infos
# ---------------------------------------------------------------------------
APP_NAME   = "Asta Académie"
VERSION    = "2.0.0"
UNIVERSITE = "UNASMOH"
OPTION     = "Sciences Informatiques"
DEV_NAME   = "Space | Asta Dev"
DEV_REAL   = "Lucky Luke"
PROMO      = "2024-2028"
WHATSAPP   = "+509 3567-2037"
SUPPORT_PHONE = "+509 46 96 6290"
SUPPORT_EMAIL = "astasoft1804@gmail.com"

# ---------------------------------------------------------------------------
# Palette de Couleurs "Cyber Space" Contraste-Intelligent
# ---------------------------------------------------------------------------
CLR_BG_DARK   = "#080f1d"   # fond gauche (Deep space navy Slate)
CLR_BG_MED    = "#0f172a"   # fond droit (Modern space Charcoal)
CLR_ACCENT    = "#10b981"   # vert émeraude premium
CLR_ACCENT2   = "#059669"   # vert émeraude hover
CLR_INPUT_BG  = "#1e293b"   # fond des inputs
CLR_INPUT_BD  = "#334155"   # bordure inputs subtile
CLR_INPUT_BD_FOCUS = "#10b981"  # bordure focus (cyber émeraude glow)
CLR_BTN_PRI   = "#1e293b"   # bouton secondaire (fond)
CLR_BTN_PRI_H = "#334155"   # hover bouton secondaire
CLR_TEXT      = "#f1f5f9"   # texte principal clair
CLR_SUBTEXT   = "#94a3b8"   # texte secondaire gris
CLR_TITLE     = "#ffffff"   # titres principaux
CLR_DIVIDER   = "#1e293b"   # séparateur vertical
CLR_ERR       = "#ef4444"   # rouge erreur
CLR_SUCCESS   = "#10b981"   # vert succès
CLR_WARNING   = "#f59e0b"   # orange avertissement

def _show_custom_dialog(parent: QWidget, title: str, text: str) -> None:
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStyleSheet(f"""
        QMessageBox {{
            background-color: {CLR_BG_MED};
        }}
        QLabel {{
            color: {CLR_TEXT};
            font-family: "Segoe UI";
            font-size: 13px;
        }}
        QPushButton {{
            background-color: {CLR_BTN_PRI};
            color: {CLR_TEXT};
            border: 1px solid {CLR_INPUT_BD};
            border-radius: 4px;
            padding: 6px 16px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {CLR_BTN_PRI_H};
            border-color: {CLR_ACCENT};
        }}
    """)
    msg.exec()


def apply_theme(theme: Theme) -> None:
    """Applique les couleurs du Theme aux constantes CLR_* locales.
    Cette fonction met à jour les variables globales utilisées par le composant
    pour garder une compatibilité avec le code existant qui se base sur CLR_*
    """
    global CLR_BG_DARK, CLR_BG_MED, CLR_ACCENT, CLR_ACCENT2, CLR_INPUT_BG
    global CLR_INPUT_BD, CLR_INPUT_BD_FOCUS, CLR_BTN_PRI, CLR_BTN_PRI_H
    global CLR_TEXT, CLR_SUBTEXT, CLR_TITLE, CLR_DIVIDER, CLR_ERR, CLR_SUCCESS, CLR_WARNING

    CLR_BG_DARK = theme.bg_alt
    CLR_BG_MED = theme.bg
    CLR_ACCENT = theme.accent
    CLR_ACCENT2 = theme.accent2
    CLR_INPUT_BG = theme.card
    CLR_INPUT_BD = theme.border
    CLR_INPUT_BD_FOCUS = theme.accent
    CLR_BTN_PRI = theme.card
    CLR_BTN_PRI_H = theme.card_hover
    CLR_TEXT = theme.text
    CLR_SUBTEXT = theme.text_secondary
    CLR_TITLE = theme.text
    CLR_DIVIDER = theme.border
    CLR_ERR = theme.danger
    CLR_SUCCESS = theme.success
    CLR_WARNING = theme.warning

# 3 Avantages impactants avec émojis
BENEFITS = [
    "Cours complets L1 → L4 (Informatique)",
    "Hacking Éthique & CTF (SecDev)",
    "Space AI & Compagnon d'étude local",
]

WINDOW_W = 920
WINDOW_H = 540


# ===========================================================================
# Composants réutilisables (Design System)
# ===========================================================================

def _make_divider(vertical: bool = False) -> QFrame:
    d = QFrame()
    d.setFrameShape(QFrame.VLine if vertical else QFrame.HLine)
    d.setStyleSheet(f"background:{CLR_DIVIDER}; border:none; max-{'width' if vertical else 'height'}:1px;")
    return d


class _InputField(QWidget):
    """Champ de saisie avec étiquette supérieure et focus glow vert."""

    def __init__(
        self,
        label_text: str,
        password: bool = False,
        right_btn: Optional[QPushButton] = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._password = password
        self._focused  = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Label supérieur
        self._lbl = QLabel(label_text)
        self._lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self._lbl.setStyleSheet(f"color:{CLR_SUBTEXT};")
        layout.addWidget(self._lbl)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        # Conteneur unifié
        self._wrap = QFrame()
        self._wrap.setFixedHeight(40)
        self._wrap.setStyleSheet(self._border_style(focused=False))
        row.addWidget(self._wrap)

        wrap_l = QHBoxLayout(self._wrap)
        wrap_l.setContentsMargins(12, 0, 8, 0)
        wrap_l.setSpacing(6)

        # Input text
        self.input = QLineEdit()
        self.input.setPlaceholderText("") # Pas de duplication de label
        self.input.setEchoMode(QLineEdit.Password if password else QLineEdit.Normal)
        self.input.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                border: none;
                color: {CLR_TEXT};
                font-size: 13px;
                font-family: "Segoe UI";
                padding: 0px;
            }}
        """)
        self.input.setFixedHeight(30)
        wrap_l.addWidget(self.input, 1)

        # Bouton optionnel (œil pour le mot de passe)
        if right_btn:
            right_btn.setFixedSize(28, 28)
            right_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    color: #94a3b8;
                    font-size: 14px;
                    padding: 0px;
                }
                QPushButton:hover { color: #ffffff; }
            """)
            # Tooltip accessible pour basculer l'affichage du mot de passe
            try:
                right_btn.setToolTip("Afficher / masquer le mot de passe")
            except Exception:
                pass
            wrap_l.addWidget(right_btn)

        layout.addLayout(row)

        # Événements focus
        self.input.focusInEvent  = lambda e: (self._on_focus(True),  QLineEdit.focusInEvent(self.input, e))
        self.input.focusOutEvent = lambda e: (self._on_focus(False), QLineEdit.focusOutEvent(self.input, e))

    def _border_style(self, focused: bool) -> str:
        color = CLR_INPUT_BD_FOCUS if focused else CLR_INPUT_BD
        return f"""
            QFrame {{
                background: {CLR_INPUT_BG};
                border: 1px solid {color};
                border-radius: 6px;
            }}
        """

    def _on_focus(self, focused: bool) -> None:
        self._wrap.setStyleSheet(self._border_style(focused))

    def set_error(self, has_error: bool) -> None:
        color = CLR_ERR if has_error else CLR_INPUT_BD
        self._wrap.setStyleSheet(f"""
            QFrame {{
                background: {CLR_INPUT_BG};
                border: 1px solid {color};
                border-radius: 6px;
            }}
        """)

    def text(self) -> str:
        return self.input.text()

    def clear(self) -> None:
        self.input.clear()


class _PrimaryButton(QPushButton):
    """Bouton principal épuré (panneau gauche) - Outline Vert Émeraude."""

    def __init__(self, text: str, parent=None) -> None:
        super().__init__(text, parent)
        self.setFixedHeight(38)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {CLR_ACCENT};
                border: 1.5px solid {CLR_ACCENT};
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
                font-family: "Segoe UI";
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: {CLR_ACCENT};
                color: {CLR_BG_DARK};
            }}
            QPushButton:pressed {{
                background: {CLR_ACCENT2};
            }}
        """)


class _SecondaryButton(QPushButton):
    """Bouton secondaire (panneau droit) - Support / Clé de licence."""

    def __init__(self, text: str, parent=None) -> None:
        super().__init__(text, parent)
        self.setFixedHeight(38)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {CLR_INPUT_BG};
                color: {CLR_TEXT};
                border: 1px solid {CLR_INPUT_BD};
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
                font-family: "Segoe UI";
            }}
            QPushButton:hover {{
                background: {CLR_BTN_PRI_H};
                border-color: {CLR_ACCENT}55;
            }}
            QPushButton:pressed {{
                background: #1e293b;
            }}
        """)


class _ConnexionButton(QPushButton):
    """Bouton CONNEXION premium avec dégradé vert émeraude, profondeur et hover lueur."""

    def __init__(self, parent=None) -> None:
        super().__init__("CONNEXION", parent)
        self.setFixedHeight(42)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {CLR_ACCENT}, stop:1 {CLR_ACCENT2});
                color: #080f1d;
                border: none;
                border-radius: 6px;
                border-bottom: 2.5px solid #047857;
                font-size: 12px;
                font-weight: bold;
                font-family: "Segoe UI";
                letter-spacing: 1.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {CLR_ACCENT2}, stop:1 #047857);
                border-bottom: 2.5px solid #065f46;
            }}
            QPushButton:pressed {{
                background: #047857;
                border-bottom: 1px solid #047857;
            }}
            QPushButton:disabled {{
                background: #1e293b;
                color: #475569;
                border-bottom: none;
            }}
        """)


# ===========================================================================
# Panneau gauche
# ===========================================================================

class _LeftPanel(QWidget):
    register_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("left_panel")
        self.setStyleSheet(f"background:{CLR_BG_DARK};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 36, 28, 20)
        layout.setSpacing(6)

        # Logo (use PNG/SVG icon if present, fallback to generated SVG)
        self._logo_lbl = QLabel()
        try:
            from core.config import asset_file
            icon_path = asset_file("asta_academie_mark.svg")
            if icon_path.exists():
                pm = QPixmap(str(icon_path)).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self._logo_lbl.setPixmap(pm)
            else:
                from utils.svg_manager import SVGManager
                self._logo_lbl.setPixmap(SVGManager.get_icon("shield", color=CLR_ACCENT, size=64).pixmap(64, 64))
        except Exception:
            from utils.svg_manager import SVGManager
            self._logo_lbl.setPixmap(SVGManager.get_icon("shield", color=CLR_ACCENT, size=64).pixmap(64, 64))
        self._logo_lbl.setAlignment(Qt.AlignLeft)
        layout.addWidget(self._logo_lbl)

        layout.addSpacing(16)

        # Titre principal épuré
        title = QLabel("REJOINS ASTA\nACADÉMIE")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet(f"color:{CLR_TITLE}; letter-spacing:1px; line-height:110%;")
        title.setWordWrap(True)
        layout.addWidget(title)

        layout.addSpacing(4)

        # Sous-titre
        sub = QLabel(f"{UNIVERSITE} — {OPTION}")
        sub.setFont(QFont("Segoe UI", 9))
        sub.setStyleSheet(f"color:{CLR_SUBTEXT};")
        sub.setAlignment(Qt.AlignLeft)
        layout.addWidget(sub)

        layout.addSpacing(20)

        # Bénéfices (list avec puces visuelles)
        for benefit in BENEFITS:
            item_wrap = QWidget()
            item_l = QHBoxLayout(item_wrap)
            item_l.setContentsMargins(0, 0, 0, 0)
            item_l.setSpacing(10)

            dot = QLabel()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"background:{CLR_ACCENT}; border-radius:5px;")
            item_l.addWidget(dot, 0, Qt.AlignTop)

            lbl = QLabel(benefit)
            lbl.setFont(QFont("Segoe UI", 10))
            lbl.setStyleSheet(f"color:{CLR_SUBTEXT};")
            lbl.setWordWrap(True)
            item_l.addWidget(lbl, 1)

            layout.addWidget(item_wrap)
            layout.addSpacing(12)

        layout.addSpacing(8)

        # Bouton CRÉER UN COMPTE
        self._register_btn = _PrimaryButton("  CRÉER UN COMPTE")
        self._register_btn.clicked.connect(self.register_clicked)
        layout.addWidget(self._register_btn)

        layout.addStretch()

        # Footer développeur centré et à faible opacité
        footer_wrap = QWidget()
        footer_wrap.setStyleSheet("background: transparent;")
        footer_l = QHBoxLayout(footer_wrap)
        footer_l.setContentsMargins(0, 0, 0, 0)
        footer_l.setAlignment(Qt.AlignCenter)

        footer = QLabel(f"Dev : {DEV_NAME}   ·   Promo {PROMO}   ·   🇭🇹 Haïti")
        footer.setFont(QFont("Segoe UI", 8))
        footer.setStyleSheet(f"color: {CLR_SUBTEXT}; opacity: 0.45;")
        footer_l.addWidget(footer)
        layout.addWidget(footer_wrap)

    def set_register_mode(self, registering: bool) -> None:
        self._register_btn.setText(
            "  ← DÉJÀ UN COMPTE ?" if registering else "  CRÉER UN COMPTE"
        )


# ===========================================================================
# Panneau droit
# ===========================================================================

class _RightPanel(QWidget):
    """Panneau de formulaire de connexion/inscription épuré."""

    login_submitted    = Signal(str, str, bool)   # nom, mdp, remember
    register_submitted = Signal(str, str, str)    # nom, mdp, mdp_confirm
    forgot_clicked     = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("right_panel")
        self.setStyleSheet(f"background:{CLR_BG_MED};")
        self._mode = "login"   # "login" | "register"
        self._build_login()

    # ── Construction ──────────────────────────────────────────────────────────

    def _build_login(self) -> None:
        self._clear()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(8)

        # Titre
        self._title_lbl = QLabel("CONNECTE-TOI\nÀ TON COMPTE")
        self._title_lbl.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self._title_lbl.setStyleSheet(f"color:{CLR_TITLE};")
        self._title_lbl.setWordWrap(True)
        layout.addWidget(self._title_lbl)

        layout.addSpacing(24)

        # Email
        self._nom_field = _InputField("Email")
        layout.addWidget(self._nom_field)
        
        layout.addSpacing(16)

        # Mot de passe + œil
        eye_btn = QPushButton("👁")
        eye_btn.setCheckable(True)
        self._pass_field = _InputField("Mot de passe", password=True, right_btn=eye_btn)
        eye_btn.toggled.connect(lambda on: self._pass_field.input.setEchoMode(
            QLineEdit.Normal if on else QLineEdit.Password
        ))
        self._pass_field.input.returnPressed.connect(self._on_login_submit)
        layout.addWidget(self._pass_field)

        layout.addSpacing(12)

        # Se souvenir + mot de passe oublié
        opt_row = QHBoxLayout()
        self._remember_chk = QCheckBox("Se souvenir de moi")
        self._remember_chk.setStyleSheet(f"""
            QCheckBox {{
                color: {CLR_SUBTEXT};
                font-size: 11px;
                font-family: "Segoe UI";
                spacing: 8px;
            }}
            QCheckBox::indicator {{ width:14px; height:14px;
                border:1px solid {CLR_INPUT_BD}; border-radius:3px; }}
            QCheckBox::indicator:checked {{
                background:{CLR_ACCENT}; border-color:{CLR_ACCENT}; }}
        """)
        opt_row.addWidget(self._remember_chk)
        opt_row.addStretch()

        forgot_btn = QPushButton("Mot de passe oublié ?")
        forgot_btn.setCursor(Qt.PointingHandCursor)
        forgot_btn.setStyleSheet(f"""
            QPushButton {{
                background:transparent; border:none;
                color:{CLR_SUBTEXT}; font-size:11px;
                text-decoration:underline; font-family:"Segoe UI";
            }}
            QPushButton:hover {{ color:{CLR_TEXT}; }}
        """)
        forgot_btn.clicked.connect(self.forgot_clicked)
        opt_row.addWidget(forgot_btn)
        layout.addLayout(opt_row)

        layout.addSpacing(20)

        # Bouton CONNEXION
        self._action_btn = _ConnexionButton()
        self._action_btn.clicked.connect(self._on_login_submit)
        layout.addWidget(self._action_btn)

        layout.addSpacing(16)

        # Séparateur "ou"
        or_row = QHBoxLayout()
        or_row.addWidget(_make_divider())
        or_lbl = QLabel("  ou  ")
        or_lbl.setFont(QFont("Segoe UI", 10))
        or_lbl.setStyleSheet(f"color:{CLR_SUBTEXT};")
        or_row.addWidget(or_lbl)
        or_row.addWidget(_make_divider())
        layout.addLayout(or_row)

        layout.addSpacing(12)

        # Boutons support WhatsApp + activation licence
        from utils.svg_manager import SVGManager
        wa_btn = _SecondaryButton("  Contacter le Support WhatsApp")
        wa_btn.setIcon(SVGManager.get_icon("smartphone", color=CLR_TEXT, size=16))
        wa_btn.clicked.connect(lambda: self._contact_support('whatsapp'))
        layout.addWidget(wa_btn)

        layout.addSpacing(8)

        lic_btn = _SecondaryButton("  J'ai une clé de licence")
        lic_btn.setIcon(SVGManager.get_icon("shield", color=CLR_TEXT, size=16))
        lic_btn.setToolTip("Activer votre licence depuis la fenêtre principale")
        lic_btn.clicked.connect(lambda: self._contact_support('license'))
        layout.addWidget(lic_btn)

        layout.addStretch()

        # Message feedback
        self._msg_lbl = QLabel("")
        self._msg_lbl.setWordWrap(True)
        self._msg_lbl.setAlignment(Qt.AlignCenter)
        self._msg_lbl.setStyleSheet(f"color:{CLR_ERR}; font-size:11px;")
        layout.addWidget(self._msg_lbl)

    def _build_register(self) -> None:
        self._clear()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        title = QLabel("CRÉER\nUN COMPTE")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet(f"color:{CLR_TITLE};")
        title.setWordWrap(True)
        layout.addWidget(title)

        layout.addSpacing(24)

        self._nom_field = _InputField("Email")
        layout.addWidget(self._nom_field)
        
        layout.addSpacing(16)

        eye1 = QPushButton("👁")
        eye1.setCheckable(True)
        self._pass_field = _InputField("Mot de passe", password=True, right_btn=eye1)
        eye1.toggled.connect(lambda on: self._pass_field.input.setEchoMode(
            QLineEdit.Normal if on else QLineEdit.Password
        ))
        layout.addWidget(self._pass_field)
        
        layout.addSpacing(16)

        eye2 = QPushButton("👁")
        eye2.setCheckable(True)
        self._confirm_field = _InputField("Confirmer le mot de passe", password=True, right_btn=eye2)
        eye2.toggled.connect(lambda on: self._confirm_field.input.setEchoMode(
            QLineEdit.Normal if on else QLineEdit.Password
        ))
        self._confirm_field.input.returnPressed.connect(self._on_register_submit)
        layout.addWidget(self._confirm_field)

        layout.addSpacing(24)

        self._action_btn = _PrimaryButton("  S'INSCRIRE")
        self._action_btn.setFixedHeight(42)
        self._action_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {CLR_ACCENT}, stop:1 {CLR_ACCENT2});
                color: #080f1d;
                border: none;
                border-radius: 6px;
                border-bottom: 2.5px solid #047857;
                font-size: 12px;
                font-weight: bold;
                font-family: "Segoe UI";
                letter-spacing: 1.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {CLR_ACCENT2}, stop:1 #047857);
                border-bottom: 2.5px solid #065f46;
            }}
            QPushButton:pressed {{
                background: #047857;
                border-bottom: 1px solid #047857;
            }}
            QPushButton:disabled {{
                background: #1e293b;
                color: #475569;
                border-bottom: none;
            }}
        """)
        self._action_btn.clicked.connect(self._on_register_submit)
        layout.addWidget(self._action_btn)

        layout.addStretch()

        self._msg_lbl = QLabel("")
        self._msg_lbl.setWordWrap(True)
        self._msg_lbl.setAlignment(Qt.AlignCenter)
        self._msg_lbl.setStyleSheet(f"color:{CLR_ERR}; font-size:11px;")
        layout.addWidget(self._msg_lbl)

    def _clear(self) -> None:
        old = self.layout()
        if old is not None:
            def delete_items(layout):
                if layout is not None:
                    while layout.count():
                        item = layout.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()
                        else:
                            delete_items(item.layout())
            delete_items(old)
            # Astuce PySide6: affecter l'ancien layout à un widget temporaire pour le détacher
            QWidget().setLayout(old)

    # ── Basculement mode ──────────────────────────────────────────────────────

    def switch_to_register(self) -> None:
        self._mode = "register"
        self._build_register()

    def switch_to_login(self) -> None:
        self._mode = "login"
        self._build_login()

    # ── Soumission ────────────────────────────────────────────────────────────

    def _on_login_submit(self) -> None:
        nom = self._nom_field.text().strip()
        pwd = self._pass_field.text().strip()
        ok  = True
        if not nom:
            self._nom_field.set_error(True)
            ok = False
        else:
            # simple email format validation
            if not re.match(r"[^@]+@[^@]+\.[^@]+", nom):
                self._nom_field.set_error(True)
                self._show_msg("⚠ Veuillez entrer un email valide.", "warning")
                return
        if not pwd:
            self._pass_field.set_error(True)
            ok = False
        if not ok:
            self._show_msg("⚠ Veuillez remplir tous les champs.", "warning")
            return
        self._nom_field.set_error(False)
        self._pass_field.set_error(False)
        remember = self._remember_chk.isChecked()
        self._set_loading(True)
        self.login_submitted.emit(nom, pwd, remember)

    def _on_register_submit(self) -> None:
        nom  = self._nom_field.text().strip()
        pwd  = self._pass_field.text().strip()
        pwd2 = self._confirm_field.text().strip()
        ok   = True
        if not nom:
            self._nom_field.set_error(True)
            ok = False
        else:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", nom):
                self._nom_field.set_error(True)
                self._show_msg("⚠ Veuillez entrer un email valide.", "warning")
                return
        if not pwd:
            self._pass_field.set_error(True)
            ok = False
        if not pwd2:
            self._confirm_field.set_error(True)
            ok = False
        if not ok:
            self._show_msg("⚠ Tous les champs sont obligatoires.", "warning")
            return
        if pwd != pwd2:
            self._confirm_field.set_error(True)
            self._show_msg("❌ Les mots de passe ne correspondent pas.", "danger")
            return
        self._nom_field.set_error(False)
        self._pass_field.set_error(False)
        self._confirm_field.set_error(False)
        self._set_loading(True)
        self.register_submitted.emit(nom, pwd, pwd2)

    def _on_license_btn(self) -> None:
        _show_custom_dialog(
            self, "Clé de Licence",
            f"Pour activer votre licence, contactez :\n\n"
            f" WhatsApp : {WHATSAPP}\n"
            f" {DEV_REAL} (Space)\n\n"
            "Envoyez votre HWID pour recevoir votre clé d'activation."
        )

    def _contact_support(self, mode: str) -> None:
        if mode == 'whatsapp':
            _show_custom_dialog(
                self, "Support WhatsApp",
                f"Contact Support:\n\nWhatsApp: {WHATSAPP}\nTel: {SUPPORT_PHONE}\nEmail: {SUPPORT_EMAIL}\n\nEnvoyez votre demande avec votre nom d'utilisateur."
            )
        elif mode == 'license':
            _show_custom_dialog(
                self, "Activation de licence",
                f"Pour activer votre licence, contactez:\n\nWhatsApp: {WHATSAPP}\nTel: {SUPPORT_PHONE}\nEmail: {SUPPORT_EMAIL}\n\nEnvoyez votre HWID et votre nom d'utilisateur."
            )

    # ── Helpers UI ────────────────────────────────────────────────────────────

    def _set_loading(self, loading: bool) -> None:
        self._action_btn.setEnabled(not loading)
        if loading:
            self._action_btn.setText("⏳  Connexion en cours…" if self._mode == "login" else "⏳  Création en cours…")
        else:
            self._action_btn.setText("CONNEXION" if self._mode == "login" else "  S'INSCRIRE")

    def reset_loading(self) -> None:
        self._set_loading(False)

    def _show_msg(self, msg: str, level: str = "danger") -> None:
        colors = {"danger": CLR_ERR, "warning": CLR_WARNING, "success": CLR_SUCCESS}
        self._msg_lbl.setText(msg)
        self._msg_lbl.setStyleSheet(f"color:{colors.get(level, CLR_ERR)}; font-size:11px;")

    def show_message(self, msg: str, level: str = "danger") -> None:
        self._show_msg(msg, level)
        self.reset_loading()


# ===========================================================================
# Fenêtre principale LoginPage
# ===========================================================================

class LoginPage(QWidget):
    """
    Fenêtre de connexion split-layout premium navy/vert.
    """

    login_success = Signal(dict, int)

    def __init__(self, theme: Theme, parent=None) -> None:
        super().__init__(parent)
        self.theme = theme
        self._mode = "login"
        
        apply_theme(self.theme)

        # Ensure local database exists before any auth operation
        try:
            from database.db_manager import init_database
            init_database(_db_file())
        except Exception:
            logger.debug("Impossible d'initialiser la DB au démarrage du LoginPage (sera tenté plus tard).")

        self.setWindowTitle(f"{APP_NAME} — Connexion")
        self.setFixedSize(WINDOW_W, WINDOW_H)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setStyleSheet(f"background:{CLR_BG_DARK};")

        self._center_window()
        self._build()
        self._animate_entrance()

    def _center_window(self) -> None:
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width()  - WINDOW_W) // 2,
            (screen.height() - WINDOW_H) // 2,
        )

    def _build(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Panneau gauche (40%)
        self._left = _LeftPanel()
        self._left.setFixedWidth(int(WINDOW_W * 0.40))
        self._left.register_clicked.connect(self._toggle_mode)
        root.addWidget(self._left)

        # Séparateur vertical
        root.addWidget(_make_divider(vertical=True))

        # Panneau droit (60%)
        self._right = _RightPanel()
        self._right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._right.login_submitted.connect(self._do_login)
        self._right.register_submitted.connect(self._do_register)
        self._right.forgot_clicked.connect(self._forgot_password)
        root.addWidget(self._right)

    def _animate_entrance(self) -> None:
        """Fade-in de la fenêtre entière."""
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(450)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        self._entrance_anim = anim

    def _toggle_mode(self) -> None:
        if self._mode == "login":
            self._mode = "register"
            self._left.set_register_mode(True)
            self._right.switch_to_register()
        else:
            self._mode = "login"
            self._left.set_register_mode(False)
            self._right.switch_to_login()

    def _do_login(self, nom: str, pwd: str, remember: bool) -> None:
        logger.info("Tentative de connexion pour '%s'.", nom)

        def _worker() -> None:
            try:
                from core.auth_manager import AuthManager
                success, msg = AuthManager.login(nom, pwd, "Asta_Desktop_App")
                if success:
                    from database.db_manager import DBManager, init_database
                    init_database(_db_file())
                    user    = DBManager.get_user_by_name(nom)
                    user_id = user["id"] if user else 1
                    profile = _load_profile()
                    profile["nom"] = nom
                    if remember:
                        profile["remember"] = True
                    _save_profile(profile)
                    logger.info("Connexion réussie pour '%s' (ID %d).", nom, user_id)
                    QTimer.singleShot(0, self, lambda: self.login_success.emit(profile, user_id))
                else:
                    logger.warning("Connexion échouée pour '%s' : %s", nom, msg)
                    QTimer.singleShot(
                        0, self, lambda m=msg: self._right.show_message(f"❌ {m}", "danger")
                    )
            except Exception as e:
                logger.error("Erreur lors de la connexion : %s", e)
                QTimer.singleShot(
                    0, self, lambda err=e: self._right.show_message(f"❌ Erreur serveur : {err}", "danger")
                )

        threading.Thread(target=_worker, daemon=True).start()

    def _do_register(self, nom: str, pwd: str, _pwd2: str) -> None:
        logger.info("Inscription de '%s'.", nom)

        def _worker() -> None:
            try:
                from core.auth_manager import AuthManager
                success, msg = AuthManager.register(nom, pwd)
                if success:
                    ok, msg2 = AuthManager.login(nom, pwd, "Asta_Desktop_App")
                    if ok:
                        from database.db_manager import DBManager, init_database
                        init_database(_db_file())
                        user    = DBManager.get_user_by_name(nom)
                        user_id = user["id"] if user else 1
                        profile = _load_profile()
                        profile["nom"] = nom
                        _save_profile(profile)
                        logger.info("Inscription réussie pour '%s' (ID %d).", nom, user_id)
                        QTimer.singleShot(0, self, lambda: self.login_success.emit(profile, user_id))
                    else:
                        QTimer.singleShot(
                            0, self, lambda m=msg2: self._right.show_message(f"❌ {m}", "danger")
                        )
                else:
                    QTimer.singleShot(
                        0, self, lambda m=msg: self._right.show_message(f"❌ {m}", "danger")
                    )
            except Exception as e:
                logger.error("Erreur lors de l'inscription : %s", e)
                QTimer.singleShot(
                    0, self, lambda err=e: self._right.show_message(f"❌ Erreur : {err}", "danger")
                )

        threading.Thread(target=_worker, daemon=True).start()

    def _forgot_password(self) -> None:
        _show_custom_dialog(
            self, "Mot de passe oublié ?",
            f"Contactez le support Asta Académie :\n\n"
            f" WhatsApp : {WHATSAPP}\n"
            f" {DEV_REAL} (Space)\n\n"
            "L'administrateur peut réinitialiser votre compte."
        )


# ---------------------------------------------------------------------------
# Helpers de stockage
# ---------------------------------------------------------------------------
def _db_file() -> Path:
    d = Path(__file__).parent.parent / "data"
    d.mkdir(exist_ok=True)
    return d / "asta_database.db"


def _profile_file() -> Path:
    import os
    d = Path(os.getenv("APPDATA", str(Path.home()))) / "AstaAcademie"
    d.mkdir(parents=True, exist_ok=True)
    return d / "profile.enc"


def _load_profile() -> dict:
    p = _profile_file()
    try:
        from security.crypto_manager import load_encrypted_json
        if p.exists():
            return load_encrypted_json(p, {})
    except Exception:
        try:
            if p.exists():
                import json
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_profile(data: dict) -> None:
    try:
        from security.crypto_manager import save_encrypted_json
        p = _profile_file()
        ok = save_encrypted_json(p, data)
        if not ok:
            # fallback to plaintext
            import json
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        try:
            import json
            p = _profile_file()
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            logger.error("_save_profile : %s", e)


# Standalone Preview
if __name__ == "__main__":
    import sys
    from ui.themes.theme_manager import THEMES, DEFAULT_THEME

    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 13))
    theme = THEMES[DEFAULT_THEME]

    win = LoginPage(theme)

    def on_login(profile, uid):
        print(f"Connecté : {profile} / ID={uid}")
        win.close()

    win.login_success.connect(on_login)
    win.show()
    sys.exit(app.exec())
