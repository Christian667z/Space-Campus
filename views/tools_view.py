"""
Asta Académie — Tools Page (PySide6)
Boîte à outils pour développeurs.
"""
import os
import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton,
    QLineEdit, QComboBox, QTextEdit, QScrollArea, QGridLayout, QMessageBox,
    QApplication
)
from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QFont, QTextCursor, QColor

from ui.themes.theme_manager import Theme
from ui.components.widgets import SectionHeader, Card

try:
    from core.logic_tools import convert_all, calculate_subnet, BOOL_LAWS, BIG_O_TABLE, ASCII_TABLE, CODE_TEMPLATES
except ImportError:
    convert_all = lambda v, b: {"error": "Module introuvable"}
    calculate_subnet = lambda i, c: {"error": "Module introuvable"}
    BOOL_LAWS = []
    BIG_O_TABLE = []
    ASCII_TABLE = []
    CODE_TEMPLATES = {"Template par défaut": {"code": "# Données indisponibles"}}

class ToolsPage(QWidget):
    def __init__(self, theme: Theme, parent=None):
        super().__init__(parent)
        self.theme = theme
        self.setStyleSheet("background: transparent;")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = SectionHeader("Boîte à Outils", 
                               "Terminal, Convertisseur, Sous-réseaux, Logique, Complexité, ASCII")
        layout.addWidget(header)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {self.theme.border};
                border-radius: 8px;
                background: {self.theme.card};
                top: -1px;
            }}
            QTabBar::tab {{
                background: {self.theme.bg};
                color: {self.theme.text_secondary};
                border: 1px solid {self.theme.border};
                border-bottom-color: {self.theme.border};
                padding: 10px 18px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-family: 'Segoe UI';
                font-size: 13px;
            }}
            QTabBar::tab:selected {{
                background: {self.theme.card};
                color: {self.theme.accent};
                border-bottom-color: {self.theme.card};
                font-weight: bold;
            }}
            QTabBar::tab:hover:!selected {{
                background: {self.theme.card_hover};
            }}
        """)
        
        self.tabs.addTab(self._build_terminal(), "Terminal")
        self.tabs.addTab(self._build_converter(), "Convertisseur")
        self.tabs.addTab(self._build_subnet(), "Sous-réseaux")
        self.tabs.addTab(self._build_boole(), "Logique")
        self.tabs.addTab(self._build_bigo(), "Complexité")
        self.tabs.addTab(self._build_ascii(), "ASCII")
        self.tabs.addTab(self._build_codegen(), "Générateur de code")

        layout.addWidget(self.tabs)

    # ── Onglet 1: Terminal ──────────────────────────────────────────────────
    def _build_terminal(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        
        self.term = QTextEdit()
        self.term.setStyleSheet("""
            QTextEdit {
                background-color: #0c0c0c;
                color: #cccccc;
                font-family: Consolas, monospace;
                font-size: 13px;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        self._print_motd()
        self._input_start_pos = 0
        self.is_red_mode = False
        
        # Initialisation du processus shell persistant (Stateful Terminal)
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self._read_term)
        self.process.start("cmd.exe" if os.name == "nt" else "bash")
        
        # Intercepter la touche Entrée et autres touches clavier
        self.term.keyPressEvent = self._handle_term_input
        l.addWidget(self.term)
        return w

    def _print_motd(self):
        self.term.append(
            "<font color='#f1c40f'>Asta Académie Terminal<br>"
            "(c) Space Dev. Tous droits réservés.</font><br>"
        )
        
    def _handle_term_input(self, event):
        cursor = self.term.textCursor()
        
        # Bloquer toute modification en dehors de la zone d'input active
        if cursor.anchor() < getattr(self, '_input_start_pos', 0) or cursor.position() < getattr(self, '_input_start_pos', 0):
            if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                # Laisser passer le copier/coller ou copier standard
                pass
            else:
                # Repositionner le curseur à la fin de l'input
                cursor.movePosition(QTextCursor.End)
                self.term.setTextCursor(cursor)
                if event.key() in [Qt.Key_Backspace, Qt.Key_Delete] or len(event.text()) > 0:
                    return
                    
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Récupérer la commande entrée par l'utilisateur
            cursor.setPosition(self._input_start_pos)
            cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
            cmd = cursor.selectedText().strip()
            self.term.moveCursor(QTextCursor.End)
            
            if cmd.lower() in ["clear", "cls"]:
                self.term.clear()
                self._print_motd()
                
            self.process.write((cmd + "\n").encode())
            
            # Détecter si la commande requiert l'affichage rouge (build, install, etc.)
            cmd_lower = cmd.lower()
            self.is_red_mode = any(kw in cmd_lower for kw in ["build", "install", "setup", "compile", "pyinstaller", "pip", "uv", "npm", "yarn"])
            return
            
        elif event.key() == Qt.Key_Backspace:
            if cursor.position() <= getattr(self, '_input_start_pos', 0):
                return
                
        QTextEdit.keyPressEvent(self.term, event)

    def _read_term(self):
        data = self.process.readAllStandardOutput()
        try:
            text = data.data().decode("cp850" if os.name == "nt" else "utf-8", errors="replace")
        except Exception:
            text = data.data().decode("utf-8", errors="replace")
            
        # Formatage HTML de la sortie du terminal
        html_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html_text = html_text.replace('\r\n', '<br>').replace('\n', '<br>').replace(' ', '&nbsp;')
        
        color = "#ff4444" if self.is_red_mode else "#cccccc"
        wrapped_text = f"<font color='{color}'>{html_text}</font>"
        
        # Colorisation du prompt en bleu (Windows et Unix)
        prompt_pattern = r'([A-Za-z]:\\[^&]*&gt;|[\w.-]+@[\w.-]+:?[^$#]*[$#])'
        final_html = re.sub(prompt_pattern, r"<font color='#3498db'>\1</font>", wrapped_text)
        
        self.term.insertHtml(final_html)
        self.term.moveCursor(QTextCursor.End)
        self._input_start_pos = self.term.textCursor().position()

    # ── Onglet 2: Convertisseur ──────────────────────────────────────────────
    def _build_converter(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(20, 20, 20, 20)
        
        form = QHBoxLayout()
        form.addWidget(QLabel("Valeur :"))
        self.conv_val = QLineEdit()
        self.conv_val.setPlaceholderText("ex: 255 ou FF")
        self.conv_val.returnPressed.connect(self._do_conv)
        form.addWidget(self.conv_val)
        
        form.addWidget(QLabel("Base d'entrée :"))
        self.conv_base = QComboBox()
        self.conv_base.addItems(["decimal", "binary", "hex", "octal"])
        form.addWidget(self.conv_base)
        
        btn = QPushButton("🔄 Convertir")
        btn.setProperty("class", "primary")
        btn.clicked.connect(self._do_conv)
        form.addWidget(btn)
        l.addLayout(form)
        
        self.conv_res = QTextEdit()
        self.conv_res.setReadOnly(True)
        self.conv_res.setFont(QFont("Consolas", 14))
        self.conv_res.setStyleSheet(f"background: {self.theme.bg}; border: 1px solid {self.theme.border}; border-radius: 6px;")
        l.addWidget(self.conv_res)
        return w
        
    def _do_conv(self):
        val = self.conv_val.text().strip()
        base = self.conv_base.currentText()
        res = convert_all(val, base)
        self.conv_res.clear()
        if "error" in res:
            self.conv_res.setTextColor(QColor(self.theme.danger))
            self.conv_res.append(f"❌ Erreur: {res['error']}")
        else:
            self.conv_res.setTextColor(QColor(self.theme.success))
            for k, v in res.items():
                self.conv_res.append(f"{k.upper():15}: {v}")

    # ── Onglet 3: Sous-réseaux ───────────────────────────────────────────────
    def _build_subnet(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(20, 20, 20, 20)
        
        form = QHBoxLayout()
        form.addWidget(QLabel("IP :"))
        self.ip_val = QLineEdit()
        self.ip_val.setPlaceholderText("192.168.1.100")
        self.ip_val.returnPressed.connect(self._do_subnet)
        form.addWidget(self.ip_val)
        
        form.addWidget(QLabel("CIDR :"))
        self.cidr_val = QLineEdit()
        self.cidr_val.setPlaceholderText("24")
        self.cidr_val.setMaximumWidth(80)
        self.cidr_val.returnPressed.connect(self._do_subnet)
        form.addWidget(self.cidr_val)
        
        btn = QPushButton("📡 Calculer")
        btn.setProperty("class", "primary")
        btn.clicked.connect(self._do_subnet)
        form.addWidget(btn)
        l.addLayout(form)
        
        self.subnet_res = QTextEdit()
        self.subnet_res.setReadOnly(True)
        self.subnet_res.setFont(QFont("Consolas", 13))
        self.subnet_res.setStyleSheet(f"background: {self.theme.bg}; border: 1px solid {self.theme.border}; border-radius: 6px;")
        l.addWidget(self.subnet_res)
        return w
        
    def _do_subnet(self):
        ip = self.ip_val.text().strip()
        try:
            cidr = int(self.cidr_val.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Le CIDR doit être un entier.")
            return
            
        res = calculate_subnet(ip, cidr)
        self.subnet_res.clear()
        if "error" in res:
            self.subnet_res.setTextColor(QColor(self.theme.danger))
            self.subnet_res.append(f"❌ {res['error']}")
        else:
            self.subnet_res.setTextColor(QColor(self.theme.info))
            for k, v in res.items():
                self.subnet_res.append(f"{k.upper():20}: {v}")

    # ── Onglet 4: Booléen ────────────────────────────────────────────────────
    def _build_boole(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        l = QGridLayout(w)
        l.setSpacing(10)
        
        headers = ["Loi", "Forme AND", "Forme OR"]
        for col, h in enumerate(headers):
            lbl = QLabel(h)
            lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
            lbl.setStyleSheet(f"color: {self.theme.accent}; padding: 8px; background: {self.theme.sidebar}; border-radius: 4px;")
            l.addWidget(lbl, 0, col)
            
        for row, law in enumerate(BOOL_LAWS, 1):
            bg = self.theme.card if row % 2 == 0 else self.theme.card_hover
            for col, key in enumerate(["loi", "and_form", "or_form"]):
                lbl = QLabel(law.get(key, ""))
                lbl.setFont(QFont("Consolas", 11))
                lbl.setStyleSheet(f"background: {bg}; padding: 8px; border-radius: 4px; color: {self.theme.text};")
                l.addWidget(lbl, row, col)
                
        scroll.setWidget(w)
        return scroll

    # ── Onglet 5: Big O ──────────────────────────────────────────────────────
    def _build_bigo(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        l = QVBoxLayout(w)
        
        for entry in BIG_O_TABLE:
            card = Card()
            card.setStyleSheet(f"background: {self.theme.bg}; border: 1px solid {self.theme.border}; border-radius: 6px;")
            c_l = QHBoxLayout(card)
            
            lbl_not = QLabel(entry.get("notation", "?"))
            lbl_not.setFont(QFont("Consolas", 14, QFont.Bold))
            lbl_not.setStyleSheet(f"color: {self.theme.warning};")
            lbl_not.setFixedWidth(100)
            c_l.addWidget(lbl_not)
            
            lbl_desc = QLabel(f"<b>{entry.get('nom','')}</b> — {entry.get('exemple','')}")
            lbl_desc.setWordWrap(True)
            lbl_desc.setStyleSheet(f"color: {self.theme.text};")
            c_l.addWidget(lbl_desc, 1)
            
            lbl_vit = QLabel(entry.get("vitesse",""))
            lbl_vit.setStyleSheet(f"color: {self.theme.text_secondary};")
            c_l.addWidget(lbl_vit)
            
            l.addWidget(card)
            
        l.addStretch()
        scroll.setWidget(w)
        return scroll

    # ── Onglet 6: ASCII ──────────────────────────────────────────────────────
    def _build_ascii(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        l = QGridLayout(w)
        l.setSpacing(4)
        
        headers = ["Char", "Déc", "Hex", "Bin"]
        for col, h in enumerate(headers):
            lbl = QLabel(h)
            lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
            lbl.setStyleSheet(f"color: {self.theme.accent}; padding: 4px; background: {self.theme.sidebar};")
            l.addWidget(lbl, 0, col)
            
        for row, entry in enumerate(ASCII_TABLE, 1):
            bg = self.theme.card if row % 2 == 0 else self.theme.card_hover
            vals = [str(entry.get("char","")), str(entry.get("decimal","")),
                    str(entry.get("hex","")), str(entry.get("binaire",""))]
            for col, val in enumerate(vals):
                lbl = QLabel(val)
                lbl.setFont(QFont("Consolas", 10))
                lbl.setStyleSheet(f"background: {bg}; padding: 4px; color: {self.theme.text};")
                l.addWidget(lbl, row, col)
                
        scroll.setWidget(w)
        return scroll

    # ── Onglet 7: Génér. Code ────────────────────────────────────────────────
    def _build_codegen(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(20, 20, 20, 20)
        
        top = QHBoxLayout()
        top.addWidget(QLabel("Template :"))
        self.tpl_cb = QComboBox()
        self.tpl_cb.addItems(list(CODE_TEMPLATES.keys()))
        self.tpl_cb.currentTextChanged.connect(self._load_tpl)
        top.addWidget(self.tpl_cb, 1)
        
        btn = QPushButton("📋 Copier")
        btn.setProperty("class", "secondary")
        btn.clicked.connect(self._copy_code)
        top.addWidget(btn)
        l.addLayout(top)
        
        self.tpl_code = QTextEdit()
        self.tpl_code.setReadOnly(True)
        self.tpl_code.setFont(QFont("Consolas", 12))
        self.tpl_code.setStyleSheet(f"background: #0d1117; color: #c9d1d9; border: 1px solid {self.theme.border}; border-radius: 6px;")
        l.addWidget(self.tpl_code)
        
        if CODE_TEMPLATES:
            self._load_tpl(list(CODE_TEMPLATES.keys())[0])
            
        return w
        
    def _load_tpl(self, name):
        tpl = CODE_TEMPLATES.get(name, {})
        self.tpl_code.setPlainText(tpl.get("code", "# Vide"))
        
    def _copy_code(self):
        QApplication.clipboard().setText(self.tpl_code.toPlainText())
        QMessageBox.information(self, "Copié", "Le template a été copié dans le presse-papier.")
