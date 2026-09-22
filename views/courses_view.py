"""
Asta Académie — Courses Page v2.5 (PySide6)
=============================================
Liseuse de cours universitaires asynchrone, réactive et hautement immersive.
Optimisation des surlignages, navigation déterministe et design premium unifié.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path
from typing import Optional, List, Dict, Set

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import (
    QColor, QFont, QGuiApplication, QKeySequence, QShortcut,
    QTextCursor, QTextCharFormat, QTextDocument
)
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QScrollArea, QSizePolicy, QSplitter, QTextBrowser, 
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, 
    QProgressBar, QTextEdit
)

from ui.components.widgets import SectionHeader
from ui.themes.theme_manager import Theme

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes de Configuration
# ---------------------------------------------------------------------------
READER_FONT_DEFAULT = 14
READER_FONT_MIN     = 10
READER_FONT_MAX     = 22
HISTORY_MAX         = 10
RECENT_MAX          = 5

LEVEL_ICONS: Dict[str, str] = {
    "l1": "①", "l2": "②", "l3": "③", "l4": "④",
    "master": "🎓", "licence": "📜",
}
FILE_ICONS: Dict[str, str] = {".md": "📄", ".txt": "🗒", ".py": "🐍", ".pdf": "📕"}

_DATA_DIR: Path = Path.home() / ".asta_academie"
_FAV_FILE: Path = _DATA_DIR / "courses_favorites.json"
_HIST_FILE: Path = _DATA_DIR / "courses_history.json"


# ---------------------------------------------------------------------------
# Utilitaires d'Infrastructure
# ---------------------------------------------------------------------------
def _load_json_set(path: Path) -> Set[str]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            return set(json.loads(path.read_text(encoding="utf-8")))
    except Exception as e:
        logger.warning("Erreur chargement Set JSON (%s) : %s", path, e)
    return set()


def _save_json_list(path: Path, data: List[str]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        logger.error("Erreur sauvegarde Liste JSON (%s) : %s", path, e)


def _load_json_list(path: Path) -> List[str]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("Erreur chargement Liste JSON (%s) : %s", path, e)
    return []


def _estimate_reading_time(text: str) -> str:
    words = len(text.split())
    minutes = max(1, round(words / 220))  # 220 mots par minute en moyenne académique
    return f"{minutes} min"


# ===========================================================================
# Composant Principal : Liseuse Professionnelle
# ===========================================================================
class CoursesPage(QWidget):
    """
    Système de lecture et d'analyse de documents académiques.
    Gère le rendu Markdown, Python et Textes bruts avec indexation dynamique.
    """
    file_opened = Signal(str)

    def __init__(self, theme: Theme, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.theme = theme
        self._font_size: int = READER_FONT_DEFAULT
        self._favorites: Set[str] = _load_json_set(_FAV_FILE)
        self._history: List[str] = _load_json_list(_HIST_FILE)
        
        self._nav_stack: List[str] = []   
        self._nav_idx: int = -1           
        self._current_content: str = ""   
        self._search_visible: bool = False

        self.setStyleSheet("background: transparent;")
        self._build_ui()
        self._setup_shortcuts()

    def _build_ui(self) -> None:
        """Assemble l'interface graphique globale de la page."""
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # En-tête Global
        root.addWidget(
            SectionHeader(
                "📚 Programme UNASMOH — Centre d'Excellence L1 à L4",
                "Documentation officielle, architectures de code, fiches de révision et cas pratiques.",
            )
        )

        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{ 
                background-color: {self.theme.border}; 
                width: 1px; 
            }}
        """)

        # Injection des deux sous-panneaux maîtres
        splitter.addWidget(self._build_sidebar())
        splitter.addWidget(self._build_reader_panel())
        splitter.setSizes([280, 740])

        root.addWidget(splitter, 1)

    # ── SIDEBAR : NAVIGATION & FILTRES ──────────────────────────────────────

    def _build_sidebar(self) -> QFrame:
        frame = QFrame()
        frame.setMinimumWidth(240)
        frame.setMaximumWidth(380)
        frame.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.card};
                border: 1px solid {self.theme.border};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 14, 12, 14)
        layout.setSpacing(10)

        # Titre Section
        title = QLabel("🗂 Navigation des Cours")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title.setStyleSheet(f"color: {self.theme.text}; border: none; background: transparent;")
        layout.addWidget(title)

        # Input Recherche Réactive
        self._search_bar = QLineEdit()
        self._search_bar.setPlaceholderText("🔍 Filtrer par titre ou extension...")
        self._search_bar.setClearButtonEnabled(True)
        self._search_bar.setStyleSheet(f"""
            QLineEdit {{
                background: {self.theme.bg};
                color: {self.theme.text};
                border: 1px solid {self.theme.border};
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }}
            QLineEdit:focus {{ border: 1px solid {self.theme.accent}; }}
        """)
        self._search_bar.textChanged.connect(self._filter_tree)
        layout.addWidget(self._search_bar)

        # Contrôles d'arborescence groupés
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        
        self.btn_expand = QPushButton("⊞ Déployer tout")
        self.btn_collapse = QPushButton("⊟ Replier tout")
        
        for btn in (self.btn_expand, self.btn_collapse):
            btn.setFixedHeight(24)
            btn.setStyleSheet(self._get_component_btn_style())
            btn_row.addWidget(btn)
        layout.addLayout(btn_row)

        # Composant central : Arbre des fichiers
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setAnimated(True)
        self._apply_premium_scrollbar_style(self.tree)
        self.tree.setStyleSheet(self.tree.styleSheet() + f"""
            QTreeWidget {{
                background-color: transparent;
                color: {self.theme.text};
                border: none;
                font-size: 12px;
                outline: none;
            }}
            QTreeWidget::item {{ padding: 4px 0px; border-radius: 4px; }}
            QTreeWidget::item:hover {{ background: {self.theme.card_hover}; }}
            QTreeWidget::item:selected {{
                background: {self.theme.accent}22;
                color: {self.theme.accent};
                font-weight: bold;
            }}
        """)
        self.tree.itemClicked.connect(self._on_item_clicked)
        self.btn_expand.clicked.connect(self.tree.expandAll)
        self.btn_collapse.clicked.connect(self.tree.collapseAll)
        layout.addWidget(self.tree, 3)

        # Compteur & Séparations Structurales
        self._file_count_lbl = QLabel("")
        self._file_count_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 10px; border: none;")
        layout.addWidget(self._file_count_lbl)

        self._add_sidebar_divider(layout)

        # Section Favoris Élastique
        layout.addWidget(self._create_sidebar_section_title("🔖 Favoris Enregistrés"))
        self._fav_list = QTreeWidget()
        self._setup_sub_tree_widget(self._fav_list)
        self._fav_list.itemClicked.connect(lambda item, _: self._load_file(item.data(0, Qt.UserRole)))
        layout.addWidget(self._fav_list, 1)

        self._add_sidebar_divider(layout)

        # Section Historique Élastique
        layout.addWidget(self._create_sidebar_section_title("🕐 Récemment Consultés"))
        self._recent_list = QTreeWidget()
        self._setup_sub_tree_widget(self._recent_list)
        self._recent_list.itemClicked.connect(lambda item, _: self._load_file(item.data(0, Qt.UserRole)))
        layout.addWidget(self._recent_list, 1)

        # Initialisation asynchrone des données
        self._load_tree()
        self._refresh_favorites_panel()
        self._refresh_recent_panel()

        return frame

    # ── PANNEAU LECTEUR : AFFICHAGE & OUTILS ────────────────────────────────

    def _build_reader_panel(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.bg};
                border: 1px solid {self.theme.border};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Assemblage des Barres Supérieures
        layout.addWidget(self._build_nav_toolbar())
        layout.addWidget(self._build_content_search_panel())
        
        # Table des matières rétractable
        self._toc_frame = self._build_toc_panel()
        self._toc_frame.setVisible(False)
        layout.addWidget(self._toc_frame)

        # Indicateur Linéaire de Progression de Lecture
        self._read_progress = QProgressBar()
        self._read_progress.setFixedHeight(2)
        self._read_progress.setTextVisible(False)
        self._read_progress.setValue(0)
        self._read_progress.setStyleSheet(f"""
            QProgressBar {{ background: transparent; border: none; }}
            QProgressBar::chunk {{ background: {self.theme.accent}; }}
        """)
        layout.addWidget(self._read_progress)

        # Viewer principal (Moteur Web/Document de rendu Qt)
        self.reader = QTextBrowser()
        self.reader.setOpenExternalLinks(True)
        self._apply_premium_scrollbar_style(self.reader)
        self.reader.setStyleSheet(self.reader.styleSheet() + f"""
            QTextBrowser {{
                background-color: transparent;
                border: none;
                color: {self.theme.text};
                padding: 24px 32px;
                font-size: {self._font_size}px;
                line-height: 1.8;
            }}
        """)
        self.reader.document().setDefaultStyleSheet(self._get_reader_document_stylesheet())
        self.reader.verticalScrollBar().valueChanged.connect(self._update_scroll_progress)
        layout.addWidget(self.reader, 1)

        # Footer technique d'environnement
        layout.addWidget(self._build_status_bar())

        self._show_welcome()
        return frame

    def _build_nav_toolbar(self) -> QFrame:
        tb = QFrame()
        tb.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.card};
                border-bottom: 1px solid {self.theme.border};
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }}
        """)
        layout = QHBoxLayout(tb)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        # Bloc de Navigation Historique
        self._btn_back = QPushButton("←")
        self._btn_fwd = QPushButton("→")
        for btn, tip, slot in [
            (self._btn_back, "Précédent (Alt+Gauche)", self._nav_back),
            (self._btn_fwd, "Suivant (Alt+Droite)", self._nav_forward)
        ]:
            btn.setFixedSize(28, 28)
            btn.setToolTip(tip)
            btn.setEnabled(False)
            btn.setStyleSheet(self._get_component_btn_style())
            btn.clicked.connect(slot)
            layout.addWidget(btn)

        # Fil d'Ariane dynamique
        self._breadcrumb = QLabel("  ► Initialisation de l'espace d'étude...")
        self._breadcrumb.setFont(QFont("Segoe UI", 10))
        self._breadcrumb.setStyleSheet(f"color: {self.theme.text_secondary}; border: none;")
        self._breadcrumb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self._breadcrumb, 1)

        # Estimation temporelle
        self._reading_time = QLabel("")
        self._reading_time.setStyleSheet(f"color: {self.theme.accent}; font-size: 11px; font-weight: bold; border: none;")
        layout.addWidget(self._reading_time)

        self._add_vertical_separator(layout)

        # Actions d'échelle de police
        btn_minus = QPushButton("A−")
        btn_plus = QPushButton("A+")
        btn_minus.clicked.connect(lambda: self._change_font(-1))
        btn_plus.clicked.connect(lambda: self._change_font(+1))
        for btn, tip in [(btn_minus, "Diminuer le texte"), (btn_plus, "Agrandir le texte")]:
            btn.setFixedSize(32, 26)
            btn.setToolTip(tip)
            btn.setStyleSheet(self._get_component_btn_style())
            layout.addWidget(btn)

        self._add_vertical_separator(layout)

        # Toggles technologiques (ToC, Recherche, Favoris, Presse-papier)
        self._btn_toc = QPushButton("☰ Table")
        self._btn_toc.setCheckable(True)
        self._btn_toc.setFixedHeight(26)
        self._btn_toc.setStyleSheet(self._get_component_btn_style())
        self._btn_toc.clicked.connect(lambda checked: self._toc_frame.setVisible(checked))
        layout.addWidget(self._btn_toc)

        self._btn_search_toggle = QPushButton("🔍")
        self._btn_search_toggle.setCheckable(True)
        self._btn_search_toggle.setFixedSize(28, 26)
        self._btn_search_toggle.setStyleSheet(self._get_component_btn_style())
        self._btn_search_toggle.clicked.connect(self._toggle_content_search)
        layout.addWidget(self._btn_search_toggle)

        self._btn_fav = QPushButton("🔖")
        self._btn_fav.setCheckable(True)
        self._btn_fav.setFixedSize(28, 26)
        self._btn_fav.setStyleSheet(self._get_component_btn_style())
        self._btn_fav.clicked.connect(self._toggle_favorite)
        layout.addWidget(self._btn_fav)

        self._btn_copy = QPushButton("📋")
        self._btn_copy.setFixedSize(28, 26)
        self._btn_copy.setToolTip("Copier le code/texte brut (Ctrl+C)")
        self._btn_copy.setStyleSheet(self._get_component_btn_style())
        self._btn_copy.clicked.connect(lambda: QGuiApplication.clipboard().setText(self._current_content))
        layout.addWidget(self._btn_copy)

        return tb

    def _build_content_search_panel(self) -> QFrame:
        self._search_frame = QFrame()
        self._search_frame.setVisible(False)
        self._search_frame.setStyleSheet(f"background: {self.theme.card}; border-bottom: 1px solid {self.theme.border};")
        row = QHBoxLayout(self._search_frame)
        row.setContentsMargins(12, 6, 12, 6)
        row.setSpacing(8)

        self._content_search = QLineEdit()
        self._content_search.setPlaceholderText("Indexation lexicale... (Entrée pour occurrence suivante)")
        self._content_search.setFixedHeight(28)
        self._content_search.setStyleSheet(f"""
            QLineEdit {{
                background: {self.theme.bg};
                color: {self.theme.text};
                border: 1px solid {self.theme.border};
                border-radius: 6px;
                padding: 2px 8px;
                font-size: 12px;
            }}
            QLineEdit:focus {{ border: 1px solid {self.theme.accent}; }}
        """)
        self._content_search.textChanged.connect(self._search_in_content)
        self._content_search.returnPressed.connect(self._find_next)
        row.addWidget(self._content_search, 1)

        self._btn_s_next = QPushButton("↓ Suivant")
        self._btn_s_prev = QPushButton("↑ Précédent")
        for btn, slot in [(self._btn_s_next, self._find_next), (self._btn_s_prev, self._find_prev)]:
            btn.setFixedHeight(26)
            btn.setStyleSheet(self._get_component_btn_style())
            btn.clicked.connect(slot)
            row.addWidget(btn)

        self._search_result_lbl = QLabel("")
        self._search_result_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 11px; font-weight: bold;")
        row.addWidget(self._search_result_lbl)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet(self._get_component_btn_style())
        close_btn.clicked.connect(lambda: self._toggle_content_search(False))
        row.addWidget(close_btn)

        return self._search_frame

    def _build_toc_panel(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(f"background: {self.theme.card}; border-bottom: 1px solid {self.theme.border};")
        frame.setFixedHeight(140)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(6)

        toc_title = QLabel("📑 Index des Sections & Chapitres")
        toc_title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        toc_title.setStyleSheet(f"color: {self.theme.accent}; border: none;")
        layout.addWidget(toc_title)

        toc_scroll = QScrollArea()
        toc_scroll.setWidgetResizable(True)
        toc_scroll.setFrameShape(QFrame.NoFrame)
        self._apply_premium_scrollbar_style(toc_scroll)

        self._toc_widget = QWidget()
        self._toc_widget.setStyleSheet("background: transparent;")
        self._toc_layout = QVBoxLayout(self._toc_widget)
        self._toc_layout.setContentsMargins(0, 0, 0, 0)
        self._toc_layout.setSpacing(4)
        
        toc_scroll.setWidget(self._toc_widget)
        layout.addWidget(toc_scroll)

        return frame

    def _build_status_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.card};
                border-top: 1px solid {self.theme.border};
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }}
        """)
        row = QHBoxLayout(bar)
        row.setContentsMargins(16, 6, 16, 6)

        self._status_words = QLabel("")
        self._status_words.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 10px; border: none;")
        row.addWidget(self._status_words)

        row.addStretch()

        self._status_path = QLabel("")
        self._status_path.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 10px; border: none;")
        row.addWidget(self._status_path)

        return bar

    # ── MOTEUR DE TRAITEMENT DES DOCUMENTS (SÉCURISÉ & DÉTERMINISTE) ─────────

    def _load_tree(self) -> None:
        """Parcourt et indexe l'arborescence des cours de manière récursive."""
        self.tree.clear()
        base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent.parent
        cours_dir = base / "cours"

        if not cours_dir.exists():
            item = QTreeWidgetItem(self.tree, ["⚠ Répertoire /cours introuvable"])
            item.setForeground(0, QColor(self.theme.danger))
            return

        total_files = 0
        for niveau in sorted(cours_dir.iterdir()):
            if not niveau.is_dir() or niveau.name.startswith("."):
                continue
            key = niveau.name.lower()
            icon = LEVEL_ICONS.get(key, "🎓")
            niv_item = QTreeWidgetItem(self.tree, [f"{icon} {niveau.name}"])
            niv_item.setFont(0, QFont("Segoe UI", 11, QFont.Bold))
            niv_item.setForeground(0, QColor(self.theme.accent))
            
            count = self._populate_node(niv_item, niveau)
            total_files += count

        self._file_count_lbl.setText(f"Index de stockage : {total_files} modules chargés")

    def _populate_node(self, parent_item: QTreeWidgetItem, path: Path) -> int:
        count = 0
        items = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        for item in items:
            if item.name.startswith(".") or item.name == "__pycache__":
                continue
            if item.is_dir():
                node = QTreeWidgetItem(parent_item, [f"📂 {item.name}"])
                node.setFont(0, QFont("Segoe UI", 10, QFont.Medium))
                count += self._populate_node(node, item)
            elif item.suffix.lower() in FILE_ICONS:
                icon = FILE_ICONS[item.suffix.lower()]
                node = QTreeWidgetItem(parent_item, [f"{icon} {item.stem}"])
                node.setFont(0, QFont("Segoe UI", 10))
                node.setData(0, Qt.UserRole, str(item))
                count += 1
        return count

    def _load_file(self, filepath: Optional[str], push_nav: bool = False) -> None:
        """Charge, analyse et injecte le document cible dans le moteur de rendu."""
        if not filepath:
            return
        p = Path(filepath)
        if not p.exists():
            logger.error("Fichier introuvable sur le disque : '%s'", filepath)
            return

        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            logger.critical("Échec d'I/O critique sur '%s': %s", filepath, e)
            self.reader.setMarkdown(f"#