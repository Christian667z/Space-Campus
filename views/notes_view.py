"""
Asta Académie — Notes Page v2.0 (PySide6)
==========================================
Éditeur de notes avancé avec gestion CRUD SQLite.

Améliorations v2.0 :
  - Barre de recherche en temps réel (filtre la liste instantanément)
  - Toolbar de formatage : Gras, Italique, Souligné, Barré, Titre H1/H2,
    Liste à puces, Alignements, couleur de texte
  - Auto-save toutes les 30 secondes si des changements sont détectés
  - Indicateur de modifications non sauvegardées (titre avec astérisque *)
  - Avertissement si on quitte une note non sauvegardée
  - Aperçu du contenu dans la sidebar (50 premiers caractères)
  - Timestamps (date de création / dernière modification) dans la sidebar
  - Compteur de mots et de caractères dans la barre de statut
  - Tri des notes : par date ou par titre (A→Z)
  - Raccourcis clavier : Ctrl+S (sauv.), Ctrl+N (nouvelle), Delete (suppr.),
    Ctrl+F (focus recherche), Ctrl+B/I/U (formatage)
  - État vide illustré (placeholder quand aucune note n'existe)
  - Export de la note active au format .txt
  - Gestion d'erreurs explicite avec logging (plus de except: pass silencieux)
  - Rétrocompatibilité totale avec l'API de la v1
"""

import logging
# removed unused datetime import per cleanup
from typing import Optional

from PySide6.QtCore import (
    QSize, Qt, QTimer, Signal,
)
from PySide6.QtGui import (
    QColor, QFont, QKeySequence, QShortcut,
    QTextCharFormat, QTextCursor, QTextListFormat,
)
from PySide6.QtWidgets import (
    QColorDialog, QComboBox, QFileDialog,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMessageBox,
    QPushButton, QSizePolicy, QSplitter,
    QTextEdit, QToolButton,
    QVBoxLayout, QWidget,
)

from core.config import DB_FILE
from database.db_manager import delete_note, get_notes, save_note
from ui.components.widgets import SectionHeader
from ui.themes.theme_manager import Theme

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

AUTO_SAVE_INTERVAL_MS   = 30_000   # 30 secondes
SIDEBAR_PREVIEW_CHARS   = 60       # longueur du preview dans la sidebar
SIDEBAR_MIN_WIDTH       = 220
EDITOR_MIN_WIDTH        = 400
TOOLBAR_ICON_SIZE       = QSize(18, 18)

SORT_OPTIONS = {
    "Date (récent)": lambda n: n.get("date_modif", ""),
    "Date (ancien)": lambda n: n.get("date_modif", ""),
    "Titre (A→Z)":   lambda n: n.get("titre", "").lower(),
    "Titre (Z→A)":   lambda n: n.get("titre", "").lower(),
}


# ===========================================================================
# Widget : Carte note dans la sidebar
# ===========================================================================

class NoteListItem(QListWidgetItem):
    """Item de liste enrichi avec aperçu et timestamp."""

    def __init__(self, note_id: int, titre: str, preview: str, date: str) -> None:
        super().__init__()
        self.note_id = note_id

        label = titre.strip() or "Sans titre"
        short_preview = (preview[:SIDEBAR_PREVIEW_CHARS] + "…") if len(preview) > SIDEBAR_PREVIEW_CHARS else preview
        short_date = date[:10] if date else ""

        self.setText(f"{label}")
        self.setToolTip(f"{label}\n{short_preview}\nDate: {short_date}")
        self.setData(Qt.UserRole, note_id)
        self.setData(Qt.UserRole + 1, short_preview)
        self.setData(Qt.UserRole + 2, short_date)
        self.setSizeHint(QSize(200, 58))


# ===========================================================================
# Delegate personnalisé pour la sidebar
# ===========================================================================

from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import QRect
from PySide6.QtGui import QPainter


class NoteDelegate(QStyledItemDelegate):
    """Rendu personnalisé : titre en gras + aperçu en gris + date à droite."""

    def __init__(self, theme: Theme, parent=None) -> None:
        super().__init__(parent)
        self.theme = theme

    def paint(self, painter: QPainter, option, index) -> None:
        painter.save()
        rect: QRect = option.rect

        # Fond sélectionné / hover
        if int(option.state) & 0x0200:  # QStyle.State_MouseOver
            painter.fillRect(rect, QColor(self.theme.card_hover))
        if int(option.state) & 0x0002:  # QStyle.State_Selected
            painter.fillRect(rect, QColor(self.theme.accent + "33"))

        title    = index.data(Qt.DisplayRole) or "Sans titre"
        preview  = index.data(Qt.UserRole + 1) or ""
        date_str = index.data(Qt.UserRole + 2) or ""

        padding = 10
        x = rect.x() + padding
        y = rect.y()
        w = rect.width() - padding * 2

        # Titre (gras, couleur principale)
        font_title = QFont("Segoe UI", 10, QFont.Bold)
        painter.setFont(font_title)
        painter.setPen(QColor(self.theme.text))
        painter.drawText(x, y + 18, w - 60, 20, Qt.AlignLeft | Qt.AlignVCenter, title)

        # Date (droite, petite)
        font_small = QFont("Segoe UI", 8)
        painter.setFont(font_small)
        painter.setPen(QColor(self.theme.text_secondary))
        painter.drawText(x, y + 18, w, 20, Qt.AlignRight | Qt.AlignVCenter, date_str)

        # Aperçu (gris, italique)
        font_preview = QFont("Segoe UI", 9)
        font_preview.setItalic(True)
        painter.setFont(font_preview)
        painter.setPen(QColor(self.theme.text_secondary))
        painter.drawText(x, y + 36, w, 18, Qt.AlignLeft | Qt.AlignVCenter, preview)

        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        return QSize(200, 60)


# ===========================================================================
# Widget principal : NotesPage
# ===========================================================================

class NotesPage(QWidget):
    """
    Page de gestion des notes pour Asta Académie.
    Compatible avec l'interface existante (theme, user_id).
    """

    # Signal émis quand le nombre de notes change (pour le badge dans la nav)
    notes_count_changed = Signal(int)

    def __init__(self, theme: Theme, user_id: int, parent=None) -> None:
        super().__init__(parent)
        self.theme = theme
        self.user_id = user_id
        self.selected_note_id: Optional[int] = None
        self.notes_data: dict = {}
        self._unsaved = False
        self._current_sort = "Date (récent)"

        self.setStyleSheet("background: transparent;")
        self._build_ui()
        self._setup_shortcuts()
        self._setup_autosave()
        self._refresh_list()

    # -----------------------------------------------------------------------
    # Construction de l'interface
    # -----------------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(12)

        # En-tête
        header = SectionHeader(
            "Mes Notes",
            "Rédigez, organisez et retrouvez toutes vos notes de cours.",
        )
        root.addWidget(header)

        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {self.theme.border};
                width: 2px;
            }}
        """)
        splitter.setChildrenCollapsible(False)

        # --- Sidebar ---
        splitter.addWidget(self._build_sidebar())

        # --- Éditeur ---
        splitter.addWidget(self._build_editor())

        splitter.setSizes([260, 740])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        root.addWidget(splitter, 1)

        # Barre de statut
        root.addWidget(self._build_statusbar())

    # ── Sidebar ─────────────────────────────────────────────────────────────

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setMinimumWidth(SIDEBAR_MIN_WIDTH)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.card};
                border: 1px solid {self.theme.border};
                border-radius: 10px;
            }}
        """)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 12, 10, 10)
        layout.setSpacing(8)

        # Titre sidebar + compteur
        hdr = QHBoxLayout()
        lbl = QLabel("Fichiers")
        lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        lbl.setStyleSheet(f"color: {self.theme.accent}; border: none;")
        hdr.addWidget(lbl)
        hdr.addStretch()
        self._count_label = QLabel("0 note")
        self._count_label.setStyleSheet(f"""
            color: {self.theme.text_secondary};
            font-size: 11px;
            background: {self.theme.border};
            border-radius: 10px;
            padding: 2px 8px;
            border: none;
        """)
        hdr.addWidget(self._count_label)
        layout.addLayout(hdr)

        # Barre de recherche
        self._search_bar = QLineEdit()
        self._search_bar.setPlaceholderText("Rechercher une note...")
        # (We could set a search icon using QAction on the QLineEdit, but for simplicity we keep text clear)
        self._search_bar.setStyleSheet(f"""
            QLineEdit {{
                background: {self.theme.bg};
                color: {self.theme.text};
                border: 1px solid {self.theme.border};
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.theme.accent};
            }}
        """)
        self._search_bar.textChanged.connect(self._filter_list)
        layout.addWidget(self._search_bar)

        # Tri
        self._sort_combo = QComboBox()
        self._sort_combo.addItems(list(SORT_OPTIONS.keys()))
        self._sort_combo.setStyleSheet(f"""
            QComboBox {{
                background: {self.theme.bg};
                color: {self.theme.text_secondary};
                border: 1px solid {self.theme.border};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 11px;
            }}
            QComboBox::drop-down {{ border: none; }}
        """)
        self._sort_combo.currentTextChanged.connect(self._on_sort_changed)
        layout.addWidget(self._sort_combo)

        # Liste
        self._list_widget = QListWidget()
        self._list_widget.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                color: {self.theme.text};
                outline: none;
            }}
            QListWidget::item {{
                border-radius: 6px;
                margin: 2px 0px;
            }}
            QListWidget::item:hover {{ background: {self.theme.card_hover}; }}
            QListWidget::item:selected {{
                background: {self.theme.accent}22;
                border-left: 3px solid {self.theme.accent};
            }}
        """)
        self._list_widget.setItemDelegate(NoteDelegate(self.theme, self._list_widget))
        self._list_widget.itemClicked.connect(self._on_note_selected)
        layout.addWidget(self._list_widget, 1)

        # Boutons action
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        btn_new = self._make_btn("Nouvelle", "success_btn", self._new_note, icon="edit")
        btn_del = self._make_btn("Supprimer", "danger_btn", self._delete_note, icon="trash")
        btn_exp = self._make_btn("Exporter sur PC", "secondary_btn", self._export_note, icon="export")

        btn_row.addWidget(btn_new)
        btn_row.addWidget(btn_del)
        btn_row.addWidget(btn_exp)
        layout.addLayout(btn_row)

        return sidebar

    # ── Éditeur ─────────────────────────────────────────────────────────────

    def _build_editor(self) -> QFrame:
        frame = QFrame()
        frame.setMinimumWidth(EDITOR_MIN_WIDTH)
        frame.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.bg};
                border: 1px solid {self.theme.border};
                border-radius: 10px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar formatage
        layout.addWidget(self._build_toolbar())

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background: {self.theme.border}; border: none; max-height: 1px;")
        layout.addWidget(sep)

        # Ligne titre
        title_bar = QWidget()
        title_bar.setStyleSheet(f"background: {self.theme.card}; border: none;")
        t_layout = QHBoxLayout(title_bar)
        t_layout.setContentsMargins(16, 10, 16, 10)
        t_layout.setSpacing(10)

        lbl_titre = QLabel("Titre :")
        lbl_titre.setStyleSheet(f"color: {self.theme.text_secondary}; font-weight: bold; border: none;")
        t_layout.addWidget(lbl_titre)

        self._title_input = QLineEdit()
        self._title_input.setPlaceholderText("Titre de la note…")
        self._title_input.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                color: {self.theme.text};
                border: none;
                border-bottom: 2px solid {self.theme.border};
                font-size: 16px;
                font-weight: bold;
                padding: 4px 0;
            }}
            QLineEdit:focus {{
                border-bottom: 2px solid {self.theme.accent};
            }}
        """)
        self._title_input.textChanged.connect(self._on_content_changed)
        # Also catch editingFinished to ensure changes are noted when the field loses focus
        self._title_input.editingFinished.connect(self._on_content_changed)
        t_layout.addWidget(self._title_input, 1)

        self._save_btn = QPushButton(" Sauvegarder")
        from utils.svg_manager import SVGManager
        self._save_btn.setIcon(SVGManager.get_icon("save", color="#ffffff", size=18))
        self._save_btn.setProperty("class", "primary")
        self._save_btn.clicked.connect(self._save_note)
        self._save_btn.setFixedHeight(34)
        t_layout.addWidget(self._save_btn)

        layout.addWidget(title_bar)

        # Zone de texte riche
        self._editor = QTextEdit()
        self._editor.setPlaceholderText(
            "Commencez à écrire votre note ici…\n\n"
            "💡 Astuce : Ctrl+S pour sauvegarder, Ctrl+B pour mettre en gras."
        )
        self._editor.setStyleSheet(f"""
            QTextEdit {{
                background: {self.theme.card};
                color: {self.theme.text};
                border: none;
                border-radius: 0 0 10px 10px;
                padding: 16px 20px;
                font-size: 14px;
                line-height: 1.6;
                selection-background-color: {self.theme.accent}44;
            }}
        """)
        font = QFont("Segoe UI", 13)
        self._editor.setFont(font)
        self._editor.textChanged.connect(self._on_content_changed)
        # Also listen to the document's contentsChanged signal to capture programmatic edits
        self._editor.document().contentsChanged.connect(self._on_content_changed)
        self._editor.cursorPositionChanged.connect(self._update_status)
        layout.addWidget(self._editor, 1)

        return frame

    # ── Toolbar ─────────────────────────────────────────────────────────────

    def _build_toolbar(self) -> QWidget:
        bar = QWidget()
        bar.setStyleSheet(f"""
            QWidget {{
                background: {self.theme.card};
                border: none;
                border-radius: 10px 10px 0 0;
            }}
            QToolButton {{
                background: transparent;
                border: none;
                border-radius: 5px;
                padding: 4px 6px;
                color: {self.theme.text};
                font-size: 13px;
            }}
            QToolButton:hover {{ background: {self.theme.card_hover}; }}
            QToolButton:checked {{ background: {self.theme.accent}33; color: {self.theme.accent}; }}
        """)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(2)

        def tb(label: str, tip: str, callback, checkable=False) -> QToolButton:
            btn = QToolButton()
            btn.setText(label)
            btn.setToolTip(tip)
            btn.setCheckable(checkable)
            btn.clicked.connect(callback)
            btn.setIconSize(TOOLBAR_ICON_SIZE)
            return btn

        # Formatage de base
        layout.addWidget(tb("𝐁",  "Gras (Ctrl+B)",         self._fmt_bold,          True))
        layout.addWidget(tb("𝐼",  "Italique (Ctrl+I)",     self._fmt_italic,        True))
        layout.addWidget(tb("U̲",  "Souligné (Ctrl+U)",     self._fmt_underline,     True))
        layout.addWidget(tb("S̶",  "Barré",                  self._fmt_strikethrough, True))

        layout.addWidget(self._vline())

        # Titres
        layout.addWidget(tb("H1", "Titre principal",        self._fmt_h1))
        layout.addWidget(tb("H2", "Sous-titre",             self._fmt_h2))
        layout.addWidget(tb("¶",  "Corps de texte",         self._fmt_body))

        layout.addWidget(self._vline())

        # Listes
        layout.addWidget(tb("≡",  "Liste à puces",          self._fmt_bullet_list))
        layout.addWidget(tb("①",  "Liste numérotée",        self._fmt_ordered_list))

        layout.addWidget(self._vline())

        # Alignements
        layout.addWidget(tb("⬛◼",  "Aligner à gauche",     self._align_left))
        layout.addWidget(tb("◼⬛◼", "Centrer",              self._align_center))
        layout.addWidget(tb("◼⬛",  "Aligner à droite",     self._align_right))

        layout.addWidget(self._vline())

        # Couleur de texte
        btn_color = tb("🎨", "Couleur du texte", self._pick_color)
        layout.addWidget(btn_color)

        layout.addStretch()

        # Indicateur de sauvegarde auto
        self._autosave_label = QLabel("Sauvegardé")
        self._autosave_label.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 11px; border: none;")
        layout.addWidget(self._autosave_label)

        return bar

    # ── Barre de statut ─────────────────────────────────────────────────────

    def _build_statusbar(self) -> QFrame:
        bar = QFrame()
        bar.setFixedHeight(28)
        bar.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.card};
                border: 1px solid {self.theme.border};
                border-radius: 6px;
            }}
            QLabel {{ border: none; color: {self.theme.text_secondary}; font-size: 11px; }}
        """)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 0, 12, 0)

        self._word_count_lbl = QLabel("0 mot · 0 caractère")
        self._cursor_pos_lbl = QLabel("Ligne 1, Colonne 1")

        layout.addWidget(self._word_count_lbl)
        layout.addStretch()
        layout.addWidget(self._cursor_pos_lbl)

        return bar

    # -----------------------------------------------------------------------
    # Raccourcis & Auto-save
    # -----------------------------------------------------------------------

    def _setup_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self._save_note)
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self._new_note)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(
            lambda: self._search_bar.setFocus()
        )
        QShortcut(QKeySequence("Ctrl+B"), self).activated.connect(self._fmt_bold)
        QShortcut(QKeySequence("Ctrl+I"), self).activated.connect(self._fmt_italic)
        QShortcut(QKeySequence("Ctrl+U"), self).activated.connect(self._fmt_underline)
        QShortcut(QKeySequence("Delete"), self).activated.connect(self._delete_note_shortcut)

    def _setup_autosave(self) -> None:
        self._autosave_timer = QTimer(self)
        self._autosave_timer.setInterval(AUTO_SAVE_INTERVAL_MS)
        self._autosave_timer.timeout.connect(self._auto_save)
        self._autosave_timer.start()

    # -----------------------------------------------------------------------
    # Logique de liste
    # -----------------------------------------------------------------------

    def _refresh_list(self) -> None:
        """Recharge les notes depuis la BDD et rafraîchit la sidebar."""
        try:
            notes = get_notes(DB_FILE, self.user_id)
            self.notes_data = {n["id"]: n for n in notes}
        except Exception as e:
            logger.error("Erreur lors du chargement des notes (user=%d): %s", self.user_id, e)
            self.notes_data = {}

        self._apply_list(list(self.notes_data.values()))
        self.notes_count_changed.emit(len(self.notes_data))

    def _apply_list(self, notes: list) -> None:
        """Applique le tri et le filtre, puis remplit la liste."""
        query = self._search_bar.text().lower().strip() if hasattr(self, "_search_bar") else ""
        sort_key = SORT_OPTIONS.get(self._current_sort, lambda n: "")

        # Filtre
        if query:
            notes = [
                n for n in notes
                if query in n.get("titre", "").lower()
                or query in n.get("contenu", "").lower()
            ]

        # Tri
        reverse = "récent" in self._current_sort or "Z→A" in self._current_sort
        notes = sorted(notes, key=sort_key, reverse=reverse)

        self._list_widget.clear()
        if not notes:
            self._show_empty_state()
            return

        for n in notes:
            item = NoteListItem(
                note_id=n["id"],
                titre=n.get("titre", "Sans titre"),
                preview=n.get("contenu", "").replace("\n", " "),
                date=n.get("date_modif", n.get("date_creation", "")),
            )
            self._list_widget.addItem(item)

        total = len(self.notes_data)
        shown = len(notes)
        self._count_label.setText(
            f"{shown}/{total} note{'s' if total > 1 else ''}" if query else
            f"{total} note{'s' if total > 1 else ''}"
        )

    def _show_empty_state(self) -> None:
        """Affiche un item indicateur quand aucune note n'existe."""
        item = QListWidgetItem("Aucune note\nCliquez sur « Nouvelle » pour commencer")
        item.setFlags(Qt.NoItemFlags)
        item.setForeground(QColor(self.theme.text_secondary))
        item.setSizeHint(QSize(200, 70))
        self._list_widget.addItem(item)
        self._count_label.setText("0 note")

    def _filter_list(self) -> None:
        self._apply_list(list(self.notes_data.values()))

    def _on_sort_changed(self, value: str) -> None:
        self._current_sort = value
        self._apply_list(list(self.notes_data.values()))

    # -----------------------------------------------------------------------
    # Actions CRUD
    # -----------------------------------------------------------------------

    def _new_note(self) -> None:
        if not self._confirm_unsaved():
            return
        self.selected_note_id = None
        self._title_input.setText("")
        self._editor.clear()
        self._unsaved = False
        self._update_save_indicator()
        self._title_input.setFocus()

    def _save_note(self) -> None:
        titre   = self._title_input.text().strip() or "Sans titre"
        contenu = self._editor.toHtml()   # on sauvegarde le HTML riche

        try:
            new_id = save_note(
                DB_FILE,
                self.user_id,
                self.selected_note_id or -1,
                titre,
                contenu,
            )
            self.selected_note_id = new_id
            self._unsaved = False
            self._update_save_indicator(saved=True)
            logger.info("Note '%s' (id=%d) sauvegardée.", titre, new_id)
            self._refresh_list()
        except Exception as e:
            logger.error("Erreur de sauvegarde note : %s", e)
            QMessageBox.critical(self, "Erreur de sauvegarde", str(e))

    def _auto_save(self) -> None:
        """Sauvegarde automatique silencieuse si des modifications sont détectées."""
        if self._unsaved and self.selected_note_id is not None:
            logger.debug("Auto-save de la note id=%d", self.selected_note_id)
            self._save_note()
            self._autosave_label.setText("Auto-sauvé")
            QTimer.singleShot(3000, lambda: self._autosave_label.setText("Sauvegardé"))

    def _on_note_selected(self, item: QListWidgetItem) -> None:
        if not self._confirm_unsaved():
            return

        nid = item.data(Qt.UserRole)
        if nid is None:
            return

        self.selected_note_id = nid
        note = self.notes_data.get(nid, {})

        self._title_input.setText(note.get("titre", ""))
        contenu = note.get("contenu", "")
        # Support HTML (notes sauvegardées en v2) et texte brut (notes v1)
        if contenu.strip().startswith("<"):
            self._editor.setHtml(contenu)
        else:
            self._editor.setPlainText(contenu)

        self._unsaved = False
        self._update_save_indicator()
        self._update_status()

    def _delete_note(self) -> None:
        if not self.selected_note_id:
            return
        # Récupérer le titre courant depuis l'UI (sécurisé si widget absent)
        titre = getattr(self, '_title_input', None)
        if titre is not None:
            titre = self._title_input.text().strip() or "cette note"
        else:
            titre = "cette note"
        reply = QMessageBox.question(
            self,
            "Supprimer la note",
            f"Voulez-vous vraiment supprimer <b>{titre}</b> ?\nCette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            try:
                delete_note(DB_FILE, self.selected_note_id)
                logger.info("Note id=%d supprimée.", self.selected_note_id)
                self.selected_note_id = None
                self._title_input.clear()
                self._editor.clear()
                self._unsaved = False
                self._refresh_list()
            except Exception as e:
                logger.error("Erreur suppression note : %s", e)
                QMessageBox.critical(self, "Erreur de suppression", str(e))

    def _delete_note_shortcut(self) -> None:
        """Delete supprime uniquement si le focus est sur la liste."""
        if self._list_widget.hasFocus():
            self._delete_note()

    def _export_note(self) -> None:
        """Exporte la note active en fichier .txt sur le disque."""
        if not self.selected_note_id:
            QMessageBox.information(self, "Export", "Sélectionnez d'abord une note à exporter.")
            return
        from PySide6.QtCore import QStandardPaths
        import os
        docs_dir = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        # récupérer le titre courant de la note (sécurisé)
        titre = getattr(self, '_title_input', None)
        if titre is not None:
            titre = self._title_input.text().strip() or "Sans titre"
        else:
            titre = "Sans titre"
        default_path = os.path.join(docs_dir, f"{titre}.txt")
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter la note (PC)", default_path, "Fichiers texte (*.txt)"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"{titre}\n{'='*len(titre)}\n\n")
                    f.write(self._editor.toPlainText())
                logger.info("Note exportée vers '%s'", path)
                QMessageBox.information(self, "Export réussi", f"Note exportée vers :\n{path}")
            except OSError as e:
                logger.error("Erreur export : %s", e)
                QMessageBox.critical(self, "Erreur d'export", str(e))

    # -----------------------------------------------------------------------
    # Formatage de texte
    # -----------------------------------------------------------------------

    def _fmt(self, fmt: QTextCharFormat) -> None:
        cursor = self._editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self._editor.mergeCurrentCharFormat(fmt)

    def _fmt_bold(self) -> None:
        fmt = QTextCharFormat()
        current = self._editor.currentCharFormat().fontWeight()
        fmt.setFontWeight(QFont.Normal if current == QFont.Bold else QFont.Bold)
        self._fmt(fmt)

    def _fmt_italic(self) -> None:
        fmt = QTextCharFormat()
        fmt.setFontItalic(not self._editor.currentCharFormat().fontItalic())
        self._fmt(fmt)

    def _fmt_underline(self) -> None:
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not self._editor.currentCharFormat().fontUnderline())
        self._fmt(fmt)

    def _fmt_strikethrough(self) -> None:
        fmt = QTextCharFormat()
        fmt.setFontStrikeOut(not self._editor.currentCharFormat().fontStrikeOut())
        self._fmt(fmt)

    def _fmt_h1(self) -> None:
        cursor = self._editor.textCursor()
        # block_fmt is unused; commented out to avoid linter warning
        # block_fmt = cursor.blockFormat()
        char_fmt = QTextCharFormat()
        char_fmt.setFontPointSize(22)
        char_fmt.setFontWeight(QFont.Bold)
        cursor.setCharFormat(char_fmt)
        self._editor.setTextCursor(cursor)

    def _fmt_h2(self) -> None:
        cursor = self._editor.textCursor()
        char_fmt = QTextCharFormat()
        char_fmt.setFontPointSize(17)
        char_fmt.setFontWeight(QFont.DemiBold)
        cursor.setCharFormat(char_fmt)
        self._editor.setTextCursor(cursor)

    def _fmt_body(self) -> None:
        cursor = self._editor.textCursor()
        char_fmt = QTextCharFormat()
        char_fmt.setFontPointSize(13)
        char_fmt.setFontWeight(QFont.Normal)
        char_fmt.setFontItalic(False)
        char_fmt.setFontUnderline(False)
        cursor.setCharFormat(char_fmt)
        self._editor.setTextCursor(cursor)

    def _fmt_bullet_list(self) -> None:
        cursor = self._editor.textCursor()
        list_fmt = QTextListFormat()
        list_fmt.setStyle(QTextListFormat.ListDisc)
        cursor.createList(list_fmt)

    def _fmt_ordered_list(self) -> None:
        cursor = self._editor.textCursor()
        list_fmt = QTextListFormat()
        list_fmt.setStyle(QTextListFormat.ListDecimal)
        cursor.createList(list_fmt)

    def _align_left(self)   -> None: self._editor.setAlignment(Qt.AlignLeft)
    def _align_center(self) -> None: self._editor.setAlignment(Qt.AlignCenter)
    def _align_right(self)  -> None: self._editor.setAlignment(Qt.AlignRight)

    def _pick_color(self) -> None:
        color = QColorDialog.getColor(Qt.black, self, "Choisir une couleur de texte")
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self._fmt(fmt)

    # -----------------------------------------------------------------------
    # Indicateurs & statut
    # -----------------------------------------------------------------------

    def _on_content_changed(self) -> None:
        self._unsaved = True
        self._update_save_indicator()
        self._update_status()

    def _update_save_indicator(self, saved: bool = False) -> None:
        if saved:
            self._autosave_label.setText("Sauvegardé")
            self._save_btn.setText(" Sauvegarder")
        elif self._unsaved:
            self._autosave_label.setText("Non sauvegardé")
            self._save_btn.setText(" Sauvegarder *")
        else:
            self._autosave_label.setText("Sauvegardé")
            self._save_btn.setText(" Sauvegarder")

    def _update_status(self) -> None:
        """Met à jour le compteur de mots et la position du curseur."""
        plain = self._editor.toPlainText()
        words = len(plain.split()) if plain.strip() else 0
        chars = len(plain)
        self._word_count_lbl.setText(f"{words} mot{'s' if words != 1 else ''} · {chars} caractère{'s' if chars != 1 else ''}")

        cursor = self._editor.textCursor()
        line = cursor.blockNumber() + 1
        col  = cursor.columnNumber() + 1
        self._cursor_pos_lbl.setText(f"Ligne {line}, Colonne {col}")

    def _confirm_unsaved(self) -> bool:
        """Demande confirmation si des modifications non sauvegardées existent. Retourne True si on peut continuer."""
        if not self._unsaved:
            return True
        reply = QMessageBox.question(
            self,
            "Modifications non sauvegardées",
            "Vous avez des modifications non sauvegardées.\nVoulez-vous les sauvegarder avant de continuer ?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save,
        )
        if reply == QMessageBox.Save:
            self._save_note()
            return True
        elif reply == QMessageBox.Discard:
            self._unsaved = False
            return True
        return False  # Cancel → on reste

    # -----------------------------------------------------------------------
    # Utilitaires
    # -----------------------------------------------------------------------

    def _make_btn(self, text: str, cls: str, slot, icon: str = None) -> QPushButton:
        btn = QPushButton(text)
        btn.setProperty("class", cls)
        if icon:
            from utils.svg_manager import SVGManager
            # Text is generally white or light for primary/danger/success buttons
            btn.setIcon(SVGManager.get_icon(icon, color="#ffffff", size=18))
        btn.clicked.connect(slot)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.setFixedHeight(30)
        return btn

    def _vline(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet(f"background: {self.theme.border}; border: none; max-width: 1px;")
        line.setFixedHeight(22)
        return line
