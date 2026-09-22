from __future__ import annotations

import json
import logging
import os
import threading
from pathlib import Path
from typing import Optional

import sip
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QCheckBox, QFrame, QSizePolicy,
    QGraphicsOpacityEffect, QMessageBox, QStackedWidget
)

# Imports applicatifs
try:
    from core.auth_manager import AuthManager
    from database.db_manager import DBManager, init_database
    from ui.themes.theme_manager import Theme, THEMES, DEFAULT_THEME
except ImportError:
    # Fallback pour le mode preview autonome si les modules ne sont pas présents
    AuthManager = None
    DBManager = None

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes de Branding & Configuration
# ---------------------------------------------------------------------------
APP_NAME = "Asta Académie"
VERSION = "2.0.0"
UNIVERSITE = "UNASMOH"
OPTION = "Sciences Informatiques"
DEV_NAME = "Space | Asta Dev"
DEV_REAL = "Lucky Luke"
PROMO = "2024-2028"
WHATSAPP = "+509 3567-2037"

# ---------------------------------------------------------------------------
# Palette de Couleurs "Cyber Space"
# ---------------------------------------------------------------------------
CLR_BG_DARK = "#080f1d"
CLR_BG_MED = "#0f172a"
CLR_ACCENT = "#10b981"
CLR_ACCENT2 = "#059669"
CLR_INPUT_BG = "#1e293b"
CLR_INPUT_BD = "#334155"
CLR_INPUT_BD_FOCUS = "#10b981"
CLR_BTN_PRI_H = "#334155"
CLR_TEXT = "#f1f5f9"
CLR_SUBTEXT = "#94a3b8"
CLR_TITLE = "#ffffff"
CLR_DIVIDER = "#1e293b"
CLR_ERR = "#ef4444"
CLR_SUCCESS = "#10b981"
CLR_WARNING = "#f59e0b"

BENEFITS = [
    "🚀  Cours complets L1 → L4 (Informatique)",
    "🛡️  Hacking Éthique & CTF (SecDev)",
    "🧠  Space AI & Compagnon d'étude local",
]

WINDOW_W = 920
WINDOW_H = 540


# ===========================================================================
# Composants du Design System (Réutilisables)
# ===========================================================================

def _make_divider(vertical: bool = False) -> QFrame:
    """Génère une ligne de séparation fine et élégante."""
    d = QFrame()
    d.setFrameShape(QFrame.VLine if vertical else QFrame.HLine)
    d.setStyleSheet(f"background: {CLR_DIVIDER}; border: none; max-{'width' if vertical else 'height'}: 1px;")
    return d


class _BaseLineEdit(QLineEdit):
    """Champ de saisie standardisé notifiant ses changements de focus via des signaux."""
    focus_changed = Signal(bool)

    def focusInEvent(self, event) -> None:
        super().focusInEvent(event)
        self.focus_changed.emit(True)

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)
        self.focus_changed.emit(False)


class _InputField(QWidget):
    """Composant champ de saisie complet avec étiquette et bordure dynamique."""

    def __init__(
        self,
        label_text: str,
        password: bool = False,
        right_btn: Optional[QPushButton] = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._password = password

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._lbl = QLabel(label_text)
        self._lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self._lbl.setStyleSheet(f"color: {CLR_SUBTEXT};")
        layout.addWidget(self._lbl)

        self._wrap = QFrame()
        self._wrap.setFixedHeight(40)
        self._wrap.setStyleSheet(self._get_border_style(focused=False))
        
        wrap_layout = QHBoxLayout(self._wrap)
        wrap_layout.setContentsMargins(12, 0, 8, 0)
        wrap_layout.setSpacing(6)

        self.input = _BaseLineEdit()
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
        wrap_layout.addWidget(self.input, 1)

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
            wrap_layout.addWidget(right_btn)

        layout.addWidget(self._wrap)
        self.input.focus_changed.connect(self._on_focus_changed)

    def _get_border_style(self, focused: bool, has_error: bool = False) -> str:
        if has_error:
            color = CLR_ERR
        else:
            color = CLR_INPUT_BD_FOCUS if focused else CLR_INPUT_BD
        return f"QFrame {{ background: {CLR_BG_DARK}; border: 1px solid {color}; border-radius: 6px; }}"

    def _on_focus_changed(self, focused: bool) -> None:
        self._wrap.setStyleSheet(self._get_border_style(focused))

    def set_error(self, has_error: bool) -> None:
        self._wrap.setStyleSheet(self._get_border_style(focused=False, has_error=has_error))

    def text(self) -> str:
        return self.input.text()

    def clear(self) -> None:
        self.input.clear()


class _PrimaryButton(QPushButton):
    """Bouton principal outline (Style Émeraude Cyber)."""

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
    """Bouton secondaire discret pour les actions d'assistance."""

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


class _ActionGradientButton(QPushButton):
    """Bouton d'action massif avec dégradé premium call-to-action."""

    def __init__(self, text: str, parent=None) -> None:
        super().__init__(text, parent)
        self.setFixedHeight(42)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {CLR_ACCENT}, stop:1 {CLR_ACCENT2});
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {CLR_ACCENT2}, stop:1 #047857);
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
# Panneaux Graphiques
# ===========================================================================

class _LeftPanel(QWidget):
    """Panneau informatif gauche (branding et features)."""
    register_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setStyleSheet(f"background: {CLR_BG_DARK};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 32, 24)
        layout.setSpacing(0)

        logo_lbl = QLabel("🎓")
        logo_lbl.setFont(QFont("Segoe UI Emoji", 36))
        layout.addWidget(logo_lbl)
        layout.addSpacing(16)

        title = QLabel("REJOINS ASTA\nACADÉMIE")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet(f"color: {CLR_TITLE};")
        layout.addWidget(title)
        layout.addSpacing(4)

        sub = QLabel(f"{UNIVERSITE} — {OPTION}")
        sub.setFont(QFont("Segoe UI", 9))
        sub.setStyleSheet(f"color: {CLR_SUBTEXT};")
        layout.addWidget(sub)
        layout.addSpacing(20)

        for benefit in BENEFITS:
            row = QHBoxLayout()
            row.setSpacing(8)
            txt = QLabel(benefit)
            txt.setFont(QFont("Segoe UI", 10))
            txt.setStyleSheet(f"color: {CLR_TEXT};")
            txt.setWordWrap(True)
            row.addWidget(txt)
            layout.addLayout(row)
            layout.addSpacing(12)

        layout.addSpacing(8)

        self._register_btn = _PrimaryButton("  CRÉER UN COMPTE")
        self._register_btn.clicked.connect(self.register_clicked)
        layout.addWidget(self._register_btn)
        layout.addStretch()

        footer = QLabel(f"Dev : {DEV_NAME}   ·   Promo {PROMO}   ·   🇭🇹 Haïti")
        footer.setFont(QFont("Segoe UI", 8))
        footer.setStyleSheet(f"color: {CLR_SUBTEXT};")
        footer.setGraphicsEffect(QGraphicsOpacityEffect(self))
        footer.graphicsEffect().setOpacity(0.45)
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

    def set_register_mode(self, registering: bool) -> None:
        self._register_btn.setText("  ← DÉJÀ UN COMPTE ?" if registering else "  CRÉER UN COMPTE")


class _LoginForm(QWidget):
    """Sous-panneau contenant exclusivement le formulaire de connexion."""
    submitted = Signal(str, str, bool)
    forgot_clicked = Signal()
    license_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        title = QLabel("CONNECTE-TOI\nÀ TON COMPTE")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet(f"color: {CLR_TITLE};")
        layout.addWidget(title)
        layout.addSpacing(24)

        self.nom_field = _InputField("Nom d'utilisateur")
        layout.addWidget(self.nom_field)
        layout.addSpacing(16)

        eye_btn = QPushButton("👁")
        eye_btn.setCheckable(True)
        self.pass_field = _InputField("Mot de passe", password=True, right_btn=eye_btn)
        eye_btn.toggled.connect(lambda on: self.pass_field.input.setEchoMode(
            QLineEdit.Normal if on else QLineEdit.Password
        ))
        layout.addWidget(self.pass_field)
        layout.addSpacing(12)

        opt_row = QHBoxLayout()
        self.remember_chk = QCheckBox("Se souvenir de moi")
        self.remember_chk.setStyleSheet(f"""
            QCheckBox {{ color: {CLR_SUBTEXT}; font-size: 11px; font-family: "Segoe UI"; spacing: 8px; }}
            QCheckBox::indicator {{ width: 14px; height: 14px; border: 1px solid {CLR_INPUT_BD}; border-radius: 3px; }}
            QCheckBox::indicator:checked {{ background: {CLR_ACCENT}; border-color: {CLR_ACCENT}; }}
        """)
        opt_row.addWidget(self.remember_chk)
        opt_row.addStretch()

        forgot_btn = QPushButton("Mot de passe oublié ?")
        forgot_btn.setCursor(Qt.PointingHandCursor)
        forgot_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: none; color: {CLR_SUBTEXT}; font-size: 11px; text-decoration: underline; font-family: "Segoe UI"; }}
            QPushButton:hover {{ color: {CLR_TEXT}; }}
        """)
        forgot_btn.clicked.connect(self.forgot_clicked)
        opt_row.addWidget(forgot_btn)
        layout.addLayout(opt_row)
        layout.addSpacing(20)

        self.action_btn = _ActionGradientButton("CONNEXION")
        self.action_btn.clicked.connect(self._on_submit)
        self.pass_field.input.returnPressed.connect(self._on_submit)
        layout.addWidget(self.action_btn)
        layout.addSpacing(16)

        or_row = QHBoxLayout()
        or_row.addWidget(_make_divider())
        or_lbl = QLabel("  ou  ")
        or_lbl.setFont(QFont("Segoe UI", 10))
        or_lbl.setStyleSheet(f"color: {CLR_SUBTEXT};")
        or_row.addWidget(or_lbl)
        or_row.addWidget(_make_divider())
        layout.addLayout(or_row)
        layout.addSpacing(12)

        wa_btn = _SecondaryButton("📱  Contacter le Support WhatsApp")
        wa_btn.clicked.connect(self.forgot_clicked)
        layout.addWidget(wa_btn)
        layout.addSpacing(8)

        lic_btn = _SecondaryButton("🆔  J'ai une clé de licence")
        lic_btn.clicked.connect(self.license_clicked)
        layout.addWidget(lic_btn)
        layout.addStretch()

        self.msg_lbl = QLabel("")
        self.msg_lbl.setAlignment(Qt.AlignCenter)
        self.msg_lbl.setWordWrap(True)
        layout.addWidget(self.msg_lbl)

    def _on_submit(self) -> None:
        nom = self.nom_field.text().strip()
        pwd = self.pass_field.text().strip()
        
        self.nom_field.set_error(not nom)
        self.pass_field.set_error(not pwd)

        if not nom or not pwd:
            self.show_message("⚠ Veuillez remplir tous les champs.", "warning")
            return
            
        self.submitted.emit(nom, pwd, self.remember_chk.isChecked())

    def show_message(self, msg: str, level: str = "danger") -> None:
        colors = {"danger": CLR_ERR, "warning": CLR_WARNING, "success": CLR_SUCCESS}
        self.msg_lbl.setText(msg)
        self.msg_lbl.setStyleSheet(f"color: {colors.get(level, CLR_ERR)}; font-size: 11px;")


class _RegisterForm(QWidget):
    """Sous-panneau contenant exclusivement le formulaire d'inscription."""
    submitted = Signal(str, str, str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        title = QLabel("CRÉER\nUN COMPTE")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet(f"color: {CLR_TITLE};")
        layout.addWidget(title)
        layout.addSpacing(24)

        self.nom_field = _InputField("Nom d'utilisateur")
        layout.addWidget(self.nom_field)
        layout.addSpacing(16)

        eye1 = QPushButton("👁")
        eye1.setCheckable(True)
        self.pass_field = _InputField("Mot de passe", password=True, right_btn=eye1)
        eye1.toggled.connect(lambda on: self.pass_field.input.setEchoMode(
            QLineEdit.Normal if on else QLineEdit.Password
        ))
        layout.addWidget(self.pass_field)
        layout.addSpacing(16)

        eye2 = QPushButton("👁")
        eye2.setCheckable(True)
        self.confirm_field = _InputField("Confirmer le mot de passe", password=True, right_btn=eye2)
        eye2.toggled.connect(lambda on: self.confirm_field.input.setEchoMode(
            QLineEdit.Normal if on else QLineEdit.Password
        ))
        layout.addWidget(self.confirm_field)
        layout.addSpacing(24)

        self.action_btn = _ActionGradientButton("S'INSCRIRE")
        self.action_btn.clicked.connect(self._on_submit)
        self.confirm_field.input.returnPressed.connect(self._on_submit)
        layout.addWidget(self.action_btn)
        layout.addStretch()

        self.msg_lbl = QLabel("")
        self.msg_lbl.setAlignment(Qt.AlignCenter)
        self.msg_lbl.setWordWrap(True)
        layout.addWidget(self.msg_lbl)

    def _on_submit(self) -> None:
        nom = self.nom_field.text().strip()
        pwd = self.pass_field.text().strip()
        pwd2 = self.confirm_field.text().strip()

        self.nom_field.set_error(not nom)
        self.pass_field.set_error(not pwd)
        self.confirm_field.set_error(not pwd2)

        if not nom or not pwd or not pwd2:
            self.show_message("⚠ Tous les champs sont obligatoires.", "warning")
            return

        if pwd != pwd2:
            self.confirm_field.set_error(True)
            self.show_message("❌ Les mots de passe ne correspondent pas.", "danger")
            return

        self.submitted.emit(nom, pwd, pwd2)

    def show_message(self, msg: str, level: str = "danger") -> None:
        colors = {"danger": CLR_ERR, "warning": CLR_WARNING, "success": CLR_SUCCESS}
        self.msg_lbl.setText(msg)
        self.msg_lbl.setStyleSheet(f"color: {colors.get(level, CLR_ERR)}; font-size: 11px;")


class _RightPanel(QStackedWidget):
    """Conteneur d'architecture propre basé sur une pile indexée pour isoler les vues."""
    login_submitted = Signal(str, str, bool)
    register_submitted = Signal(str, str, str)
    forgot_clicked = Signal()
    license_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setStyleSheet(f"background: {CLR_BG_MED};")

        self.login_form = _LoginForm()
        self.register_form = _RegisterForm()

        self.addWidget(self.login_form)
        self.addWidget(self.register_form)

        # Re-routage des signaux
        self.login_form.submitted.connect(self.login_submitted.emit)
        self.login_form.forgot_clicked.connect(self.forgot_clicked.emit)
        self.login_form.license_clicked.connect(self.license_clicked.emit)
        self.register_form.submitted.connect(self.register_submitted.emit)

    def switch_to_register(self) -> None:
        self.setCurrentWidget(self.register_form)

    def switch_to_login(self) -> None:
        self.setCurrentWidget(self.login_form)

    def set_loading(self, loading: bool, mode: str) -> None:
        form = self.login_form if mode == "login" else self.register_form
        form.action_btn.setEnabled(not loading)
        if loading:
            form.action_btn.setText("⏳ Opération en cours...")
        else:
            form.action_btn.setText("CONNEXION" if mode == "login" else "S'INSCRIRE")

    def show_message(self, msg: str, mode: str, level: str = "danger") -> None:
        form = self.login_form if mode == "login" else self.register_form
        form.show_message(msg, level)
        self.set_loading(False, mode)


# ===========================================================================
# Fenêtre Principale
# ===========================================================================

class LoginPage(QWidget):
    """Fenêtre maîtresse de gestion de l'authentification Asta Académie."""
    login_success = Signal(dict, int)

    def __init__(self, theme: Optional[Theme] = None, parent=None) -> None:
        super().__init__(parent)
        self.theme = theme
        self._mode = "login"

        self.setWindowTitle(f"{APP_NAME} — Connexion")
        self.setFixedSize(WINDOW_W, WINDOW_H)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setStyleSheet(f"background: {CLR_BG_DARK};")

        self._center_window()
        self._build_ui()
        self._animate_entrance()

    def _center_window(self) -> None:
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - WINDOW_W) // 2, (screen.height() - WINDOW_H) // 2)

    def _build_ui(self) -> None:
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self._left = _LeftPanel()
        self._left.setFixedWidth(int(WINDOW_W * 0.40))
        self._left.register_clicked.connect(self._toggle_mode)
        root_layout.addWidget(self._left)

        root_layout.addWidget(_make_divider(vertical=True))

        self._right = _RightPanel()
        self._right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._right.login_submitted.connect(self._do_login)
        self._right.register_submitted.connect(self._do_register)
        self._right.forgot_clicked.connect(self._forgot_password)
        self._right.license_clicked.connect(self._show_license_info)
        root_layout.addWidget(self._right)

    def _animate_entrance(self) -> None:
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        self._entrance_anim = QPropertyAnimation(effect, b"opacity", self)
        self._entrance_anim.setDuration(450)
        self._entrance_anim.setStartValue(0.0)
        self._entrance_anim.setEndValue(1.0)
        self._entrance_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._entrance_anim.start()

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
        self._right.set_loading(True, "login")

        def _worker() -> None:
            if AuthManager is None:
                # Simulation asynchrone si exécuté hors package
                QTimer.singleShot(1500, lambda: self._right.show_message("❌ Mode autonome : AuthManager introuvable.", "login"))
                return
            try:
                success, msg = AuthManager.login(nom, pwd, "Asta_Desktop_App")
                if success:
                    init_database(str(self._get_db_file()))
                    user = DBManager.get_user_by_name(nom)
                    user_id = user["id"] if user else 1
                    profile = self._load_profile()
                    profile["nom"] = nom
                    if remember:
                        profile["remember"] = True
                    self._save_profile(profile)
                    QTimer.singleShot(0, lambda: self.login_success.emit(profile, user_id))
                else:
                    QTimer.singleShot(0, lambda: self._right.show_message(f"❌ {msg}", "login"))
            except Exception as e:
                logger.error("Erreur critique de connexion : %s", e)
                QTimer.singleShot(0, lambda: self._right.show_message(f"❌ Erreur serveur : {e}", "login"))

        threading.Thread(target=_worker, daemon=True).start()

    def _do_register(self, nom: str, pwd: str, _pwd2: str) -> None:
        logger.info("Tentative d'inscription pour '%s'.", nom)
        self._right.set_loading(True, "register")

        def _worker() -> None:
            if AuthManager is None:
                QTimer.singleShot(1500, lambda: self._right.show_message("❌ Mode autonome : AuthManager introuvable.", "register"))
                return
            try:
                success, msg = AuthManager.register(nom, pwd)
                if success:
                    ok, msg2 = AuthManager.login(nom, pwd, "Asta_Desktop_App")
                    if ok:
                        init_database(str(self._get_db_file()))
                        user = DBManager.get_user_by_name(nom)
                        user_id = user["id"] if user else 1
                        profile = self._load_profile()
                        profile["nom"] = nom
                        self._save_profile(profile)
                        QTimer.singleShot(0, lambda: self.login_success.emit(profile, user_id))
                    else:
                        QTimer.singleShot(0, lambda: self._right.show_message(f"❌ {msg2}", "register"))
                else:
                    QTimer.singleShot(0, lambda: self._right.show_message(f"❌ {msg}", "register"))
            except Exception as e:
                logger.error("Erreur critique d'inscription : %s", e)
                QTimer.singleShot(0, lambda: self._right.show_message(f"❌ Erreur serveur : {e}", "register"))

        threading.Thread(target=_worker, daemon=True).start()

    def _forgot_password(self) -> None:
        QMessageBox.information(
            self, "Mot de passe oublié ?",
            f"Contactez l'administration d'Asta Académie :\n\n"
            f"📱 WhatsApp : {WHATSAPP}\n"
            f"👤 {DEV_REAL} (Space)\n\n"
            "Un administrateur réinitialisera vos identifiants à distance."
        )

    def _show_license_info(self) -> None:
        QMessageBox.information(
            self, "Activation de Licence",
            f"Pour générer ou valider votre clé d'accès, contactez :\n\n"
            f"📱 WhatsApp : {WHATSAPP}\n"
            f"👤 {DEV_REAL}\n\n"
            "Veuillez préparer votre identifiant machine unique (HWID)."
        )

    # ── Gestionnaires de fichiers utilitaires ─────────────────────────────────
    
    @staticmethod
    def _get_db_file() -> Path:
        d = Path(__file__).parent.parent / "data"
        d.mkdir(exist_ok=True)
        return d / "asta_database.db"

    @staticmethod
    def _get_profile_file() -> Path:
        d = Path(os.getenv("APPDATA", str(Path.home()))) / "AstaAcademie"
        d.mkdir(parents=True, exist_ok=True)
        return d / "profile.json"

    def _load_profile(self) -> dict:
        p = self._get_profile_file()
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error("Échec de chargement du profil JSON : %s", e)
        return {}

    def _save_profile(self, data: dict) -> None:
        try:
            self._get_profile_file().write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error("Échec de sauvegarde du profil JSON : %s", e)


# Execution de test autonome
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10)) # Taille par défaut harmonisée pour Windows

    win = LoginPage()
    win.login_success.connect(lambda prof, uid: print(f"Succès ! Profil: {prof} | ID: {uid}"))
    win.show()
    sys.exit(app.exec())