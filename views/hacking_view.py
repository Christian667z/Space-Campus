"""
Asta Académie — Advanced Cyber Security Laboratory v2.5 (PySide6)
===================================================================
Laboratoire d'évaluation de la sécurité offensive, émulation de terminaux 
et validation de modules cryptographiques (CTF). 

Conception conforme aux exigences logicielles et industrielles d'élite.
"""

from __future__ import annotations

import getpass
import logging
import os
import socket
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

from PySide6.QtCore import Qt, QProcess, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QClipboard, QGuiApplication
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QScrollArea, QSplitter,
    QTabWidget, QTextBrowser, QTextEdit, QToolButton,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,
    QProgressBar, QSizePolicy,
)

from core.config import DB_FILE
from security.security_auth import (
    generate_hwid, load_hacking_license,
    save_hacking_license, verify_hacking_key,
)
from ui.components.widgets import Card
from ui.themes.theme_manager import Theme

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes de Configuration du Laboratoire
# ---------------------------------------------------------------------------
MAX_UNLOCK_ATTEMPTS = 5
READER_FONT_DEFAULT = 13
READER_FONT_MIN     = 9
READER_FONT_MAX     = 20

# Commandes système sous surveillance (Filtre de sécurité préventif)
DANGEROUS_COMMANDS = {
    "rm", "rmdir", "del", "format", "mkfs", "dd",
    "shutdown", "reboot", "halt", "poweroff",
    "chmod 777", "chown", ":(){:|:&};:",
    "mv /", "cp /", "wget", "curl",
}

# Indicateurs d'extensions de fichiers système
FILE_ICONS = {
    ".py": "[SRC.PY]", 
    ".md": "[DOC.MD]", 
    ".txt": "[TXT.RAW]", 
    ".sh": "[CONF.SH]", 
    ".json": "[DATA.JSON]"
}


# ---------------------------------------------------------------------------
# Banque d'Évaluations Pratiques (CTF Framework)
# ---------------------------------------------------------------------------
def _build_missions() -> List[Dict[str, Any]]:
    """Génère la matrice d'évaluations pratiques avec flags dynamiques système."""
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        local_ip = "127.0.0.1"

    try:
        username = getpass.getuser()
    except Exception:
        username = "user"

    hostname = socket.gethostname()

    return [
        # ── RECONNAISSANCE & AUDIT SYSTEME ──
        {
            "id": "ctf_01", "category": "RECONNAISSANCE & AUDIT", "difficulty": "Facile",
            "title": "Évaluation 01 : Détermination d'Adressage Logique IPv4",
            "desc": "Identifier l'adresse IPv4 locale affectée à l'interface réseau active du système hôte.",
            "flag": local_ip, "xp": 50,
            "hints": [
                "Exécuter l'utilitaire de configuration réseau de l'hôte : `ipconfig` (Windows) ou `ip a` (Linux).",
                f"Le préfixe du sous-réseau détecté commence par : {local_ip[:local_ip.rfind('.')+1]}…",
            ],
        },
        {
            "id": "ctf_02", "category": "RECONNAISSANCE & AUDIT", "difficulty": "Facile",
            "title": "Évaluation 02 : Extraction d'Identité Privilégiée",
            "desc": "Extraire le nom d'utilisateur (Username) associé au contexte d'exécution de la session courante.",
            "flag": username, "xp": 50,
            "hints": [
                "Utiliser la commande d'identification de session standard : `whoami` ou inspecter la variable globale `$USER`.",
                f"La séquence d'identification commence par le caractère : '{username[0]}…'",
            ],
        },
        {
            "id": "ctf_03", "category": "RECONNAISSANCE & AUDIT", "difficulty": "Facile",
            "title": "Évaluation 03 : Résolution de l'Identifiant Réseau",
            "desc": "Résoudre le nom d'hôte unique identifiant le nœud courant sur la topologie réseau.",
            "flag": hostname, "xp": 50,
            "hints": [
                "Invoquer la commande de résolution d'infrastructure : `hostname`.",
                f"Le segment d'identification machine débute par : '{hostname[0]}…'",
            ],
        },
        # ── CRYPTOGRAPHIE & CRYPTANALYSE ──
        {
            "id": "ctf_04", "category": "CRYPTOGRAPHIE & CRYPTANALYSE", "difficulty": "Facile",
            "title": "Évaluation 04 : Inversion d'Encodage Linéaire Base64",
            "desc": "Effectuer le décodage algorithmique du flux binaire structuré sous le format suivant : `QXN0YV9IYWNrZXI=`",
            "flag": "Asta_Hacker", "xp": 75,
            "hints": [
                "Base64 constitue un encodage de transfert et non un algorithme de chiffrement. Utiliser le package `base64` en Python.",
                "La chaîne décodée intègre un séparateur d'arborescence de type underscore.",
            ],
        },
        {
            "id": "ctf_05", "category": "CRYPTOGRAPHIE & CRYPTANALYSE", "difficulty": "Moyen",
            "title": "Évaluation 05 : Cryptanalyse Élémentaire - Substitution par Décalage (ROT13)",
            "desc": "Déchiffrer la chaîne de caractères soumise à une permutation symétrique de type César : `Nfgn_Unpxre`",
            "flag": "Asta_Hacker", "xp": 100,
            "hints": [
                "Appliquer l'algorithme de décalage circulaire uniforme (moteur d'inversion ROT13 via le module `codecs`).",
                "Le décalage appliqué correspond exactement à une translation de la moitié de l'alphabet standard.",
            ],
        },
        {
            "id": "ctf_06", "category": "CRYPTOGRAPHIE & CRYPTANALYSE", "difficulty": "Difficile",
            "title": "Évaluation 06 : Identification d'Empreinte Cryptographique (Hashing)",
            "desc": "Déterminer la fonction de hachage à sens unique à l'origine du condensat (checksum) de longueur fixe spécifié : `e3b0c44298fc1c149afb4c8996fb92427ae41e4649b934ca495991b7852b855`",
            "flag": "SHA-256", "xp": 150,
            "hints": [
                "Ce hash correspond au calcul d'intégrité d'un buffer totalement VIDE.",
                "La nomenclature attendue est exprimée en majuscules avec un tiret de séparation standard (ex: SHA-XXX).",
            ],
        },
        # ── SECURITE DES APPLICATIONS WEB ──
        {
            "id": "ctf_07", "category": "SÉCURITÉ DES APPLICATIONS WEB", "difficulty": "Moyen",
            "title": "Évaluation 07 : Analyse de Protocoles - Code d'État HTTP",
            "desc": "Identifier le code de statut standardisé renvoyé par un serveur HTTP pour notifier un défaut d'authentification client.",
            "flag": "401", "xp": 75,
            "hints": [
                "Les codes de la classe 4xx désignent des anomalies de requêtes imputables au client.",
                "Le code recherché précède immédiatement la restriction d'accès de type '403 Forbidden'.",
            ],
        },
        {
            "id": "ctf_08", "category": "SÉCURITÉ DES APPLICATIONS WEB", "difficulty": "Difficile",
            "title": "Évaluation 08 : Injection SQL de Contournement (Auth Bypass)",
            "desc": "Fournir l'expression logique d'injection SQL canonique permettant de neutraliser la clause restrictive de validation d'identité.",
            "flag": "' OR '1'='1", "xp": 150,
            "hints": [
                "L'injection exploite une tautologie logique absolue au sein de la clause restrictive WHERE.",
                "La chaîne débute par un caractère d'échappement (apostrophe) et injecte l'opérateur booléen OR.",
            ],
        },
        # ── ANALYSE FORENSIQUE & INVESTIGATION ──
        {
            "id": "ctf_09", "category": "ANALYSE FORENSIQUE & INVESTIGATION", "difficulty": "Moyen",
            "title": "Évaluation 09 : Analyse de Services - Persistance Distante SSH",
            "desc": "Désigner le port d'écoute standard attribué par l'IANA pour l'établissement de sessions de shell sécurisé.",
            "flag": "22", "xp": 75,
            "hints": [
                "Le protocole Secure Shell s'exécute par défaut sur un port de la plage privilégiée (inférieur à 100).",
                "Ce port succède immédiatement au service de transfert de fichiers FTP (port 21).",
            ],
        },
        {
            "id": "ctf_10", "category": "ANALYSE FORENSIQUE & INVESTIGATION", "difficulty": "Difficile",
            "title": "Évaluation 10 : Artefact Cryptographique d'Infrastructure",
            "desc": "Soumettre le jeton de validation cryptographique principal de l'infrastructure de cyberdéfense d'Asta Académie.",
            "flag": "ASTA_SEC_2024", "xp": 200,
            "hints": [
                "Le jeton respecte le formalisme strict de l'organisation en majuscules avec underscores.",
                "Structure attendue : ASTA_XXX_XXXX (se terminant par le millésime de la promotion).",
            ],
        },
    ]


# ===========================================================================
# Interface Principale : Module de Sécurité Transparente
# ===========================================================================
class HackingPage(QWidget):
    """Contrôleur applicatif du laboratoire de sécurité — Protection matérielle par HWID."""

    xp_earned = Signal(int, str)  # Pipeline de synchronisation de l'expérience utilisateur

    def __init__(self, profile: dict, user_id: int, theme: Theme, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.profile: dict = profile
        self.user_id: int = user_id
        self.theme: Theme = theme
        self._unlock_attempts: int = 0
        self._cmd_history: List[str] = []
        self._hist_idx: int = -1
        self._reader_font_size: int = READER_FONT_DEFAULT
        self.process: Optional[QProcess] = None

        self.current_hwid: str = generate_hwid()
        self.saved_key: Optional[str] = load_hacking_license()

        self.setStyleSheet("background: transparent;")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # En-tête Unifié
        root.addWidget(self._build_header())

        # Zone d'affichage dynamique de la pile de sécurité
        self._content_frame = QFrame()
        self._content_frame.setStyleSheet("background: transparent;")
        self._content_layout = QVBoxLayout(self._content_frame)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        root.addWidget(self._content_frame, 1)

        # Vérification d'intégrité cryptographique de la clé
        if self.saved_key and verify_hacking_key(self.current_hwid, self.saved_key):
            self._show_unlocked()
        else:
            self._show_locked()

    def _build_header(self) -> QFrame:
        """Génère l'en-tête technique d'authentification du module."""
        hdr = QFrame()
        hdr.setStyleSheet(
            f"background: {self.theme.sidebar}; "
            f"border-bottom: 2px solid {self.theme.danger};"
        )
        layout = QHBoxLayout(hdr)
        layout.setContentsMargins(20, 10, 20, 10)

        t1 = QLabel("LABORATOIRE DE SÉCURITÉ OFFENSIVE & CYBERDÉFENSE")
        t1.setFont(QFont("Consolas", 14, QFont.Bold))
        t1.setStyleSheet(f"color: {self.theme.danger};")
        layout.addWidget(t1)

        layout.addStretch()

        t2 = QLabel("MODULE INTEGRAL DE PRODUCTION · ASTA ACADÉMIE")
        t2.setFont(QFont("Consolas", 9, QFont.Bold))
        t2.setStyleSheet(f"color: {self.theme.text_secondary};")
        layout.addWidget(t2)

        return hdr

    def _clear_content(self) -> None:
        """Purge la disposition de l'interface graphique pour rechargement d'état."""
        while self._content_layout.count():
            child = self._content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # -----------------------------------------------------------------------
    # Passerelle de Contrôle d'Accès (Écran Verrouillé)
    # -----------------------------------------------------------------------
    def _show_locked(self) -> None:
        """Déploie la console de verrouillage de sécurité."""
        self._clear_content()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        w = QWidget()
        w.setStyleSheet("background: transparent;")
        scroll.setWidget(w)

        outer = QVBoxLayout(w)
        outer.setAlignment(Qt.AlignCenter)
        outer.setContentsMargins(40, 40, 40, 40)

        card = Card()
        card.setFixedWidth(640)
        card.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.card};
                border: 1px solid {self.theme.danger}44;
                border-radius: 12px;
            }}
        """)
        cl = QVBoxLayout(card)
        cl.setAlignment(Qt.AlignCenter)
        cl.setSpacing(18)
        cl.setContentsMargins(32, 28, 32, 28)

        t1 = QLabel("CONTRÔLE D'ACCÈS SYSTEME — ZONE RESTREINTE")
        t1.setFont(QFont("Consolas", 18, QFont.Bold))
        t1.setStyleSheet(f"color: {self.theme.danger};")
        t1.setAlignment(Qt.AlignCenter)
        cl.addWidget(t1)

        t2 = QLabel("VÉRIFICATION DE SÉCURITÉ EN COURS — ACCREDITATION REQUISE")
        t2.setFont(QFont("Consolas", 10))
        t2.setStyleSheet(f"color: {self.theme.text_secondary};")
        t2.setAlignment(Qt.AlignCenter)
        cl.addWidget(t2)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background: {self.theme.danger}33; border: none; max-height: 1px;")
        cl.addWidget(sep)

        # Zone d'affichage HWID
        hwid_frame = QFrame()
        hwid_frame.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.bg};
                border: 1px solid {self.theme.border};
                border-radius: 6px;
            }}
        """)
        hwid_layout = QVBoxLayout(hwid_frame)
        hwid_layout.setContentsMargins(14, 12, 14, 12)
        hwid_layout.setSpacing(8)

        hwid_title = QLabel("Signature d'Empreinte Matérielle Active (HWID) :")
        hwid_title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        hwid_title.setStyleSheet(f"color: {self.theme.text_secondary}; border: none; background: transparent;")
        hwid_layout.addWidget(hwid_title)

        hwid_row = QHBoxLayout()
        hwid_val = QLabel(self.current_hwid)
        hwid_val.setFont(QFont("Consolas", 12, QFont.Bold))
        hwid_val.setStyleSheet(f"color: {self.theme.accent}; border: none; background: transparent;")
        hwid_val.setTextInteractionFlags(Qt.TextSelectableByMouse)
        hwid_row.addWidget(hwid_val, 1)

        copy_hwid_btn = QPushButton("Copier HWID")
        copy_hwid_btn.setFixedHeight(28)
        copy_hwid_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.theme.accent}22;
                color: {self.theme.accent};
                border: 1px solid {self.theme.accent}44;
                border-radius: 4px;
                padding: 2px 12px;
                font-size: 11px;
                font-family: Consolas;
            }}
            QPushButton:hover {{ background: {self.theme.accent}44; }}
        """)
        copy_hwid_btn.clicked.connect(
            lambda: QGuiApplication.clipboard().setText(self.current_hwid)
        )
        hwid_row.addWidget(copy_hwid_btn)
        hwid_layout.addLayout(hwid_row)

        sub = QLabel("Veuillez transmettre cet identifiant d'infrastructure au support d'administration pour la génération de votre clé d'accès.")
        sub.setFont(QFont("Segoe UI", 10))
        sub.setStyleSheet(f"color: {self.theme.text_secondary}; border: none; background: transparent;")
        sub.setWordWrap(True)
        hwid_layout.addWidget(sub)

        cl.addWidget(hwid_frame)

        # Module de saisie de la clé de licence
        key_lbl = QLabel("Saisie du Jeton d'Activation Cryptographique :")
        key_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        key_lbl.setStyleSheet(f"color: {self.theme.text}; border: none; background: transparent;")
        cl.addWidget(key_lbl)

        key_row = QHBoxLayout()
        self.key_entry = QLineEdit()
        self.key_entry.setPlaceholderText("XXXXX-XXXXX-XXXXX-XXXXX")
        self.key_entry.setFont(QFont("Consolas", 14, QFont.Bold))
        self.key_entry.setAlignment(Qt.AlignCenter)
        self.key_entry.setEchoMode(QLineEdit.Password)
        self.key_entry.setStyleSheet(f"""
            QLineEdit {{
                background: {self.theme.bg};
                color: {self.theme.danger};
                border: 1px solid {self.theme.danger}44;
                border-radius: 6px;
                padding: 10px;
                letter-spacing: 2px;
            }}
            QLineEdit:focus {{ border: 1px solid {self.theme.danger}; }}
        """)
        self.key_entry.textChanged.connect(self._auto_format_key)
        self.key_entry.returnPressed.connect(self._try_unlock)
        key_row.addWidget(self.key_entry, 1)

        self._eye_btn = QPushButton("Afficher")
        self._eye_btn.setFixedSize(70, 42)
        self._eye_btn.setCheckable(True)
        self._eye_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.theme.bg};
                color: {self.theme.text_secondary};
                border: 1px solid {self.theme.border};
                border-radius: 6px;
                font-size: 11px;
            }}
            QPushButton:checked {{ background: {self.theme.accent}22; color: {self.theme.accent}; }}
        """)
        self._eye_btn.clicked.connect(
            lambda chk: (
                self.key_entry.setEchoMode(QLineEdit.Normal if chk else QLineEdit.Password),
                self._eye_btn.setText("Masquer" if chk else "Afficher")
            )
        )
        key_row.addWidget(self._eye_btn)
        cl.addLayout(key_row)

        self._attempts_lbl = QLabel("")
        self._attempts_lbl.setAlignment(Qt.AlignCenter)
        self._attempts_lbl.setStyleSheet(f"color: {self.theme.danger}; font-size: 11px; font-family: Consolas; background: transparent;")
        cl.addWidget(self._attempts_lbl)

        self._unlock_btn = QPushButton("INITIALISER L'ACCÈS AU LABORATOIRE")
        self._unlock_btn.setProperty("class", "danger_btn")
        self._unlock_btn.setFixedHeight(45)
        self._unlock_btn.setFont(QFont("Consolas", 12, QFont.Bold))
        self._unlock_btn.clicked.connect(self._try_unlock)
        cl.addWidget(self._unlock_btn)

        contact = QLabel("Support de Délivrance des Licences : Canal WhatsApp Extérieur +509 3567-2037")
        contact.setFont(QFont("Segoe UI", 10, QFont.Bold))
        contact.setStyleSheet(f"color: {self.theme.success}; border: none; background: transparent;")
        contact.setAlignment(Qt.AlignCenter)
        cl.addWidget(contact)

        outer.addWidget(card)
        self._content_layout.addWidget(scroll)

    def _auto_format_key(self, text: str) -> None:
        """Assure le formatage algorithmique synchrone de la clé d'infrastructure."""
        clean = text.replace("-", "").upper()
        parts = [clean[i:i+5] for i in range(0, min(len(clean), 20), 5)]
        formatted = "-".join(parts)
        if formatted != text:
            self.key_entry.blockSignals(True)
            self.key_entry.setText(formatted)
            self.key_entry.setCursorPosition(len(formatted))
            self.key_entry.blockSignals(False)

    def _try_unlock(self) -> None:
        """Intercepte et valide l'intégrité de la licence saisie."""
        key = self.key_entry.text().strip()
        if not key:
            return

        if verify_hacking_key(self.current_hwid, key):
            save_hacking_license(key)
            self._show_unlocked()
        else:
            self._unlock_attempts += 1
            if self._unlock_attempts >= MAX_UNLOCK_ATTEMPTS:
                self._unlock_btn.setEnabled(False)
                self.key_entry.setEnabled(False)
                self._attempts_lbl.setText("CRITICAL: SÉCURITÉ DU SYSTÈME COMPROMISE. SESSIONS BLOQUÉES.")
                logger.error("Dépassement du quota de tentatives d'authentification cryptographique.")
            else:
                self._attempts_lbl.setText(
                    f"Échec de l'authentification ({self._unlock_attempts}/{MAX_UNLOCK_ATTEMPTS}). Jeton invalide."
                )

    # -----------------------------------------------------------------------
    # Espace de Production Déverrouillé (Environnement d'Analyse)
    # -----------------------------------------------------------------------
    def _show_unlocked(self) -> None:
        """Déploie l'environnement d'ingénierie complet et asynchrone."""
        self._clear_content()

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background: transparent; }")

        # Volet Latéral : Navigation d'Infrastructure
        sidebar = self._build_sidebar()
        splitter.addWidget(sidebar)

        # Zone Centrale : Système d'onglets unifié
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::panel {{ border: none; background: transparent; }}
            QTabBar::tab {{
                background: {self.theme.sidebar};
                color: {self.theme.text_secondary};
                padding: 10px 16px;
                font-family: Consolas;
                font-size: 11px;
                border: none;
            }}
            QTabBar::tab:selected {{
                background: {self.theme.bg};
                color: {self.theme.danger};
                border-bottom: 2px solid {self.theme.danger};
            }}
        """)

        self.tabs.addTab(self._build_reader(), "LISEUSE DOCUMENTAIRE")
        self.tabs.addTab(self._build_terminal(), "CONSOLE TERMINAL")
        self.tabs.addTab(self._build_ctf(), "FRAMEWORK CTF & ÉVALUATIONS")

        splitter.addWidget(self.tabs)
        splitter.setSizes([260, 740])

        self._content_layout.addWidget(splitter)
        self._start_terminal_process()

    def _build_sidebar(self) -> QFrame:
        """Génère l'arborescence analytique des fichiers de documentation."""
        frame = QFrame()
        frame.setStyleSheet(f"background: {self.theme.sidebar}; border-right: 1px solid {self.theme.border};")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        lbl = QLabel("RÉFÉRENTIELS LOGIQUES")
        lbl.setFont(QFont("Consolas", 10, QFont.Bold))
        lbl.setStyleSheet(f"color: {self.theme.text_secondary};")
        layout.addWidget(lbl)

        self._tree_search = QLineEdit()
        self._tree_search.setPlaceholderText("Filtrer l'arborescence...")
        self._tree_search.setStyleSheet(f"""
            QLineEdit {{
                background: {self.theme.bg};
                color: {self.theme.text};
                border: 1px solid {self.theme.border};
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
                font-family: Consolas;
            }}
        """)
        self._tree_search.textChanged.connect(self._filter_tree)
        layout.addWidget(self._tree_search)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(4)
        for label, method in [("Développer All", lambda: self.tree.expandAll()), ("Réduire All", lambda: self.tree.collapseAll())]:
            btn = QPushButton(label)
            btn.setFixedHeight(22)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {self.theme.bg};
                    color: {self.theme.text_secondary};
                    border: 1px solid {self.theme.border};
                    border-radius: 4px;
                    font-size: 10px;
                    font-family: Segoe UI;
                }}
                QPushButton:hover {{ color: {self.theme.accent}; }}
            """)
            btn.clicked.connect(method)
            btn_row.addWidget(btn)
        layout.addLayout(btn_row)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet(f"""
            QTreeWidget {{
                background-color: transparent;
                color: {self.theme.text};
                border: none;
                font-family: Consolas;
                font-size: 12px;
                outline: none;
            }}
            QTreeWidget::item {{ padding: 4px 2px; border-radius: 4px; }}
            QTreeWidget::item:hover {{ background: {self.theme.card_hover}; }}
            QTreeWidget::item:selected {{ background: {self.theme.danger}22; color: {self.theme.danger}; }}
        """)
        self._build_tree()
        self.tree.itemClicked.connect(self._on_tree_clicked)
        layout.addWidget(self.tree, 1)

        self._file_count_lbl = QLabel("")
        self._file_count_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 10px; font-family: Consolas;")
        layout.addWidget(self._file_count_lbl)
        self._update_file_count()

        return frame

    def _build_tree(self) -> None:
        """Alimente l'arborescence à partir des ressources système de production."""
        base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent.parent
        hacking_dir = base / "hacking"
        
        self.tree.clear()
        if not hacking_dir.exists():
            QTreeWidgetItem(self.tree, [" [Alerte] Répertoire /hacking introuvable"])
            return

        def populate(path: Path, parent_item: QTreeWidgetItem | QTreeWidget) -> None:
            for p in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
                if p.is_dir():
                    item = QTreeWidgetItem(parent_item, [f" {p.name.upper()}"])
                    populate(p, item)
                elif p.is_file() and p.suffix in FILE_ICONS:
                    tag = FILE_ICONS.get(p.suffix, "[RAW]")
                    item = QTreeWidgetItem(parent_item, [f"{tag} {p.name}"])
                    item.setData(0, Qt.UserRole, str(p))

        populate(hacking_dir, self.tree)

    def _filter_tree(self, text: str) -> None:
        """Filtre les nœuds de l'arborescence documentaire en temps réel."""
        def filter_item(item: QTreeWidgetItem) -> bool:
            match = text.lower() in item.text(0).lower()
            any_child_visible = False
            for i in range(item.childCount()):
                if filter_item(item.child(i)):
                    any_child_visible = True
            visible = match or any_child_visible
            item.setHidden(not visible)
            if visible and text:
                item.setExpanded(True)
            return visible

        for i in range(self.tree.topLevelItemCount()):
            filter_item(self.tree.topLevelItem(i))

    def _update_file_count(self) -> None:
        """Comptabilise l'intégralité des ressources d'évaluation indexées."""
        count = 0
        def count_items(item: QTreeWidgetItem) -> None:
            nonlocal count
            if item.data(0, Qt.UserRole):
                count += 1
            for i in range(item.childCount()):
                count_items(item.child(i))
        for i in range(self.tree.topLevelItemCount()):
            count_items(self.tree.topLevelItem(i))
        self._file_count_lbl.setText(f"Registre : {count} ressource(s) disponible(s)")

    def _on_tree_clicked(self, item: QTreeWidgetItem, col: int) -> None:
        filepath = item.data(0, Qt.UserRole)
        if filepath:
            self._load_file(filepath)
            self.tabs.setCurrentIndex(0)

    # -----------------------------------------------------------------------
    # Module Liseuse Documentaire
    # -----------------------------------------------------------------------
    def _build_reader(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        toolbar = QFrame()
        toolbar.setStyleSheet(f"background: {self.theme.sidebar}; border-bottom: 1px solid {self.theme.border};")
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(12, 6, 12, 6)
        tb_layout.setSpacing(8)

        self._lbl_file = QLabel(" [Statut] En attente de sélection d'une ressource documentaire...")
        self._lbl_file.setFont(QFont("Consolas", 10))
        self._lbl_file.setStyleSheet(f"color: {self.theme.text_secondary}; border: none; background: transparent;")
        tb_layout.addWidget(self._lbl_file, 1)

        for label, delta in [("Format −", -1), ("Format +", +1)]:
            btn = QPushButton(label)
            btn.setFixedHeight(26)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {self.theme.bg}; color: {self.theme.text};
                    border: 1px solid {self.theme.border}; border-radius: 4px;
                    padding: 0 10px; font-family: Consolas; font-size: 11px;
                }}
                QPushButton:hover {{ border: 1px solid {self.theme.danger}; }}
            """)
            btn.clicked.connect(lambda _, d=delta: self._change_font_size(d))
            tb_layout.addWidget(btn)

        copy_btn = QPushButton("Copier Flux Raw")
        copy_btn.setFixedHeight(26)
        copy_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.theme.danger}22; color: {self.theme.danger};
                border: 1px solid {self.theme.danger}44; border-radius: 4px;
                padding: 0 12px; font-family: Consolas; font-size: 11px; font-weight: bold;
            }}
            QPushButton:hover {{ background: {self.theme.danger}44; }}
        """)
        copy_btn.clicked.connect(self._copy_reader_content)
        tb_layout.addWidget(copy_btn)

        layout.addWidget(toolbar)

        self._browser = QTextBrowser()
        self._browser.setOpenExternalLinks(True)
        self._browser.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {self.theme.bg};
                color: {self.theme.text};
                border: none;
                padding: 24px;
                font-family: Consolas;
                font-size: {self._reader_font_size}px;
            }}
        """)
        layout.addWidget(self._browser)
        return w

    def _change_font_size(self, delta: int) -> None:
        self._reader_font_size = max(READER_FONT_MIN, min(READER_FONT_MAX, self._reader_font_size + delta))
        self._browser.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {self.theme.bg}; color: {self.theme.text}; border: none;
                padding: 24px; font-family: Consolas; font-size: {self._reader_font_size}px;
            }}
        """)

    def _load_file(self, filepath: str) -> None:
        try:
            p = Path(filepath)
            self._lbl_file.setText(f" Flux Source : {p.name}")
            content = p.read_text(encoding="utf-8", errors="replace")
            
            import html
            escaped = html.escape(content)
            html_payload = f"""
            <html>
            <body style='background-color:{self.theme.bg}; color:{self.theme.text}; font-family:Consolas;'>
                <pre style='background:{self.theme.card}; border:1px solid {self.theme.border}; border-radius:6px; padding:16px; font-size:{self._reader_font_size}px; white-space:pre-wrap; line-height:1.5;'>{escaped}</pre>
            </body>
            </html>
            """
            self._browser.setHtml(html_payload)
        except Exception as e:
            logger.error("Défaut critique d'E/S sur la ressource documentaire : %s", e)

    def _copy_reader_content(self) -> None:
        QGuiApplication.clipboard().setText(self._browser.toPlainText())

    # -----------------------------------------------------------------------
    # Module d'Émulation Terminal
    # -----------------------------------------------------------------------
    def _build_terminal(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        tb = QFrame()
        tb.setStyleSheet("background: #0d0d0d; border-bottom: 1px solid #262626;")
        tb_l = QHBoxLayout(tb)
        tb_l.setContentsMargins(12, 6, 12, 6)
        
        lbl = QLabel("CONSOLE D'ÉMULATION DE TERMINAL UNIVERSEL")
        lbl.setFont(QFont("Consolas", 10, QFont.Bold))
        lbl.setStyleSheet("color: #00ff00; border: none; background: transparent;")
        tb_l.addWidget(lbl)
        tb_l.addStretch()

        for label, method in [("Effacer Écran", self._clear_terminal), ("Copier Sortie", self._copy_terminal_output)]:
            btn = QPushButton(label)
            btn.setFixedHeight(22)
            btn.setStyleSheet("""
                QPushButton {
                    background: #1a1a1a; color: #8c8c8c; border: 1px solid #333;
                    border-radius: 4px; padding: 0 10px; font-family: Consolas; font-size: 10px;
                }
                QPushButton:hover { color: #00ff00; border: 1px solid #00ff00; }
            """)
            btn.clicked.connect(method)
            tb_l.addWidget(btn)
        layout.addWidget(tb)

        self._term_out = QTextEdit()
        self._term_out.setReadOnly(True)
        self._term_out.setStyleSheet("""
            QTextEdit {
                background-color: #050505; color: #00ff00; border: none;
                font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; padding: 12px;
            }
        """)
        layout.addWidget(self._term_out, 1)

        input_frame = QFrame()
        input_frame.setStyleSheet("background: #0d0d0d; border-top: 1px solid #262626;")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(8, 6, 8, 6)

        prompt_lbl = QLabel(" [SHELL] $ ")
        prompt_lbl.setFont(QFont("Consolas", 11, QFont.Bold))
        prompt_lbl.setStyleSheet("color: #00ff00;")
        input_layout.addWidget(prompt_lbl)

        self._term_in = QLineEdit()
        self._term_in.setFont(QFont("Consolas", 11))
        self._term_in.setStyleSheet("background: transparent; color: #ffffff; border: none; outline: none;")
        self._term_in.returnPressed.connect(self._exec_cmd)
        input_layout.addWidget(self._term_in, 1)
        
        layout.addWidget(input_frame)
        self._print_terminal_banner()
        return w

    def _print_terminal_banner(self) -> None:
        self._term_out.append("=====================================================================")
        self._term_out.append(" SUBSYSTÈME D'ÉMULATION DE SHELL SÉCURISÉ — ASTA ACADÉMIE CORE v2.5")
        self._term_out.append(f" ENVIRONNEMENT ACTIF : HÔTE LIAISON LOGIQUE EN COURS")
        self._term_out.append("=====================================================================")

    def _start_terminal_process(self) -> None:
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self._read_output)
        shell = "cmd.exe" if os.name == "nt" else "/bin/sh"
        self.process.start(shell)
        if not self.process.waitForStarted(2000):
            logger.error("Défaut critique d'initialisation du processus d'émulation système (%s)", shell)

    def _exec_cmd(self) -> None:
        cmd = self._term_in.text().strip()
        if not cmd:
            return

        self._cmd_history.insert(0, cmd)
        self._hist_idx = -1
        self._term_in.clear()

        if cmd.lower() in ("clear", "cls"):
            self._clear_terminal()
            return

        # Contrôle préventif des vecteurs d'attaque destructeurs locaux
        for danger in DANGEROUS_COMMANDS:
            if cmd.lower().startswith(danger):
                reply = QMessageBox.warning(
                    self, "⚠️ Interception Administrative",
                    f"L'instruction `{cmd}` présente un risque d'altération système.\n"
                    "Confirmer l'exécution forcée sous votre entière responsabilité ?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
                )
                if reply == QMessageBox.No:
                    return
                break

        ts = datetime.now().strftime("%H:%M:%S")
        self._term_out.append(f"\n[{ts}] [CONSOLE] $ {cmd}")
        if self.process and self.process.state() == QProcess.Running:
            self.process.write((cmd + "\n").encode())
        else:
            self._term_out.append("[ÉCHEC] L'instance du processus d'émulation s'est déconnectée. Veuillez recharger l'interface.")

    def _read_output(self) -> None:
        if not self.process:
            return
        data = self.process.readAllStandardOutput()
        try:
            text = data.data().decode("cp850" if os.name == "nt" else "utf-8")
        except Exception:
            text = data.data().decode("utf-8", errors="replace")
        self._term_out.insertPlainText(text)
        self._term_out.verticalScrollBar().setValue(self._term_out.verticalScrollBar().maximum())

    def _clear_terminal(self) -> None:
        self._term_out.clear()
        self._print_terminal_banner()

    def _copy_terminal_output(self) -> None:
        QGuiApplication.clipboard().setText(self._term_out.toPlainText())

    # -----------------------------------------------------------------------
    # Framework d'Évaluations Pratiques (CTF Dashboard)
    # -----------------------------------------------------------------------
    def _build_ctf(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        missions = _build_missions()
        solved = self.profile.get("ctf_solved", [])
        total_xp = sum(m["xp"] for m in missions)
        solved_xp = sum(m["xp"] for m in missions if m["id"] in solved)
        solved_count = len(solved)

        # Tableau de progression macroscopique
        prog_frame = QFrame()
        prog_frame.setStyleSheet(f"""
            QFrame {{ background: {self.theme.card}; border: 1px solid {self.theme.border}; border-radius: 8px; }}
        """)
        prog_l = QVBoxLayout(prog_frame)
        prog_l.setContentsMargins(16, 14, 16, 14)
        
        top_row = QHBoxLayout()
        prog_title = QLabel("Métriques d'Avancement Global")
        prog_title.setFont(QFont("Consolas", 11, QFont.Bold))
        prog_title.setStyleSheet(f"color: {self.theme.text};")
        top_row.addWidget(prog_title)
        top_row.addStretch()

        xp_badge = QLabel(f"Index de Qualification : {solved_xp} / {total_xp} XP")
        xp_badge.setFont(QFont("Consolas", 11, QFont.Bold))
        xp_badge.setStyleSheet(f"color: {self.theme.warning};")
        top_row.addWidget(xp_badge)
        prog_l.addLayout(top_row)

        progress = QProgressBar()
        pct = int(solved_xp / total_xp * 100) if total_xp > 0 else 0
        progress.setValue(pct)
        progress.setFixedHeight(10)
        progress.setTextVisible(False)
        progress.setStyleSheet(f"""
            QProgressBar {{ background: {self.theme.bg}; border: 1px solid {self.theme.border}; border-radius: 5px; }}
            QProgressBar::chunk {{ background: {self.theme.warning}; border-radius: 5px; }}
        """)
        prog_l.addWidget(progress)

        sub = QLabel(f"Validation : {solved_count} / {len(missions)} modules exécutés avec succès · Taux d'achèvement : {pct}%")
        sub.setFont(QFont("Consolas", 10))
        sub.setStyleSheet(f"color: {self.theme.text_secondary};")
        prog_l.addWidget(sub)
        
        layout.addWidget(prog_frame)

        # Matrice dynamique des modules d'évaluation individuels
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_w = QWidget()
        scroll_w.setStyleSheet("background: transparent;")
        scroll_l = QVBoxLayout(scroll_w)
        scroll_l.setSpacing(14)
        scroll_l.setContentsMargins(0, 0, 0, 0)

        for m in missions:
            m_card = Card()
            is_solved = m["id"] in solved
            m_card.setStyleSheet(f"""
                QFrame {{
                    background: {self.theme.card};
                    border: 1px solid {self.theme.success if is_solved else self.theme.border};
                    border-radius: 8px;
                }}
            """)
            cl = QVBoxLayout(m_card)
            cl.setContentsMargins(16, 16, 16, 16)
            cl.setSpacing(10)

            # En-tête du module d'évaluation
            h_row = QHBoxLayout()
            title_lbl = QLabel(m["title"])
            title_lbl.setFont(QFont("Consolas", 12, QFont.Bold))
            title_lbl.setStyleSheet(f"color: {self.theme.success if is_solved else self.theme.text};")
            h_row.addWidget(title_lbl)
            h_row.addStretch()

            meta_lbl = QLabel(f"[{m['category']} | {m['difficulty']} | +{m['xp']} XP]")
            meta_lbl.setFont(QFont("Consolas", 10, QFont.Bold))
            meta_lbl.setStyleSheet(f"color: {self.theme.text_secondary};")
            h_row.addWidget(meta_lbl)
            cl.addLayout(h_row)

            # Corps
            desc_lbl = QLabel(m["desc"])
            desc_lbl.setFont(QFont("Segoe UI", 11))
            desc_lbl.setStyleSheet(f"color: {self.theme.text};")
            desc_lbl.setWordWrap(True)
            cl.addWidget(desc_lbl)

            if is_solved:
                status_lbl = QLabel("[STATUT : VALIDÉ — CRÉDITS SYNCHRONISÉS]")
                status_lbl.setFont(QFont("Consolas", 10, QFont.Bold))
                status_lbl.setStyleSheet(f"color: {self.theme.success};")
                cl.addWidget(status_lbl)
            else:
                # Bloc de soumission
                act_row = QHBoxLayout()
                inp = QLineEdit()
                inp.setPlaceholderText("Saisir l'artefact de validation (Flag)...")
                inp.setFont(QFont("Consolas", 11))
                inp.setStyleSheet(f"""
                    QLineEdit {{
                        background: {self.theme.bg}; color: {self.theme.text};
                        border: 1px solid {self.theme.border}; border-radius: 4px; padding: 6px 12px;
                    }}
                    QLineEdit:focus {{ border: 1px solid {self.theme.danger}; }}
                """)
                act_row.addWidget(inp, 1)

                val_btn = QPushButton("Soumettre Flag")
                val_btn.setFixedHeight(34)
                val_btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {self.theme.danger}22; color: {self.theme.danger};
                        border: 1px solid {self.theme.danger}44; border-radius: 4px; padding: 0 16px;
                        font-family: Consolas; font-weight: bold; font-size: 11px;
                    }}
                    QPushButton:hover {{ background: {self.theme.danger}44; }}
                """)
                
                hint_btn = QPushButton("Révéler l'Indice Nominale (−10 XP)")
                hint_btn.setFixedHeight(34)
                hint_btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {self.theme.warning}15; color: {self.theme.warning};
                        border: 1px solid {self.theme.warning}33; border-radius: 4px; padding: 0 12px;
                        font-family: Segoe UI; font-size: 11px;
                    }}
                    QPushButton:hover {{ background: {self.theme.warning}33; }}
                """)

                attempt_lbl = QLabel("")
                attempt_lbl.setStyleSheet("color: #E74C3C; font-size: 11px; font-family: Consolas;")
                hint_lbl = QLabel("")
                hint_lbl.setWordWrap(True)
                hint_lbl.setStyleSheet(f"color: {self.theme.warning}; font-size: 11px; font-family: Consolas;")

                # Logique événementielle inline encapsulée
                val_btn.clicked.connect(
                    lambda _, i=inp, m_id=m["id"], m_flag=m["flag"], m_xp=m["xp"], al=attempt_lbl, c=m_card: 
                    self._validate_flag(i.text().strip(), m_id, m_flag, m_xp, al, c)
                )
                hint_btn.clicked.connect(
                    lambda _, h_list=m["hints"], hl=hint_lbl: 
                    hl.setText(f"Analyse préventive : {h_list[0]}")
                )

                act_row.addWidget(val_btn)
                act_row.addWidget(hint_btn)
                cl.addLayout(act_row)
                cl.addWidget(attempt_lbl)
                cl.addWidget(hint_lbl)

            scroll_l.addWidget(m_card)

        scroll_l.addStretch()
        scroll.setWidget(scroll_w)
        layout.addWidget(scroll, 1)
        return w

    def _validate_flag(self, guess: str, m_id: str, flag: str, xp: int, err_label: QLabel, card_widget: Card) -> None:
        """Contrôle la conformité algébrique du flag soumis."""
        if guess == flag:
            if m_id not in self.profile.setdefault("ctf_solved", []):
                self.profile["ctf_solved"].append(m_id)
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.xp_earned.emit(xp, ts)
                QMessageBox.information(self, "Validation Réussie", f" Jeton validé avec succès. Allocation de +{xp} XP au registre.")
                self._show_unlocked()  # Rafraîchissement synchrone
        else:
            err_label.setText(" [Échec] Artefact soumis non conforme. Signature de flag incorrecte.")