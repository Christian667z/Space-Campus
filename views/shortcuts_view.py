"""
Asta Académie — Shortcuts Page (PySide6)
Base de connaissances rapides.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QScrollArea, QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.themes.theme_manager import Theme
from ui.components.widgets import SectionHeader, Card

try:
    from utils.shortcuts_data import EXCEL_SHORTCUTS, EXCEL_FORMULAS, PROF_TRAPS, LINUX_COMMANDS, OSI_LAYERS, NETWORK_PROTOCOLS
except ImportError:
    EXCEL_SHORTCUTS = []
    EXCEL_FORMULAS = []
    PROF_TRAPS = []
    LINUX_COMMANDS = []
    OSI_LAYERS = []
    NETWORK_PROTOCOLS = []

class ShortcutsPage(QWidget):
    def __init__(self, theme: Theme, parent=None):
        super().__init__(parent)
        self.theme = theme
        self.setStyleSheet("background: transparent;")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = SectionHeader("⚡ Raccourcis & Références", "Excel, Pièges Profs, Linux, Modèle OSI, Protocoles Réseau")
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
        
        self.tabs.addTab(self._build_excel(), "📊 Excel")
        self.tabs.addTab(self._build_traps(), "⚠️ Pièges Profs")
        self.tabs.addTab(self._build_linux(), "🐧 Linux")
        self.tabs.addTab(self._build_osi(), "🌐 Modèle OSI")
        self.tabs.addTab(self._build_protocols(), "📡 Protocoles")

        layout.addWidget(self.tabs)

    def _create_scroll(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        l = QVBoxLayout(w)
        scroll.setWidget(w)
        return scroll, l

    def _build_excel(self):
        scroll, l = self._create_scroll()
        
        lbl_s = QLabel("Raccourcis Excel Essentiels")
        lbl_s.setFont(QFont("Segoe UI", 14, QFont.Bold))
        lbl_s.setStyleSheet(f"color: {self.theme.accent}; margin-top: 10px; margin-bottom: 10px;")
        l.addWidget(lbl_s)
        
        lv_color = {"Essentiel": "#f85149", "Intermédiaire": "#d29922", "Basique": "#3fb950", "Avancé": "#7c3aed"}
        
        for s in EXCEL_SHORTCUTS:
            c = QFrame()
            c.setStyleSheet(f"background: {self.theme.bg}; border-radius: 6px; border: 1px solid {self.theme.border};")
            cl = QHBoxLayout(c)
            
            klbl = QLabel(s.get("key", ""))
            klbl.setFont(QFont("Consolas", 12, QFont.Bold))
            klbl.setStyleSheet(f"color: {self.theme.accent};")
            klbl.setFixedWidth(160)
            cl.addWidget(klbl)
            
            dlbl = QLabel(s.get("action", ""))
            dlbl.setFont(QFont("Segoe UI", 12))
            dlbl.setStyleSheet(f"color: {self.theme.text};")
            cl.addWidget(dlbl, 1)
            
            nlbl = QLabel(s.get("niveau", ""))
            nlbl.setStyleSheet(f"color: {lv_color.get(s.get('niveau',''), '#888')};")
            cl.addWidget(nlbl)
            
            l.addWidget(c)
            
        lbl_f = QLabel("Formules Excel Vitales")
        lbl_f.setFont(QFont("Segoe UI", 14, QFont.Bold))
        lbl_f.setStyleSheet(f"color: {self.theme.accent}; margin-top: 20px; margin-bottom: 10px;")
        l.addWidget(lbl_f)
        
        for f in EXCEL_FORMULAS:
            c = QFrame()
            c.setStyleSheet(f"background: {self.theme.bg}; border-radius: 6px; border: 1px solid {self.theme.border};")
            cl = QHBoxLayout(c)
            
            flbl = QLabel(f.get("formule", ""))
            flbl.setFont(QFont("Consolas", 12, QFont.Bold))
            flbl.setStyleSheet("color: #4fc3f7;")
            flbl.setFixedWidth(260)
            cl.addWidget(flbl)
            
            dlbl = QLabel(f.get("description", ""))
            dlbl.setFont(QFont("Segoe UI", 12))
            dlbl.setStyleSheet(f"color: {self.theme.text};")
            cl.addWidget(dlbl, 1)
            
            l.addWidget(c)
            
        l.addStretch()
        return scroll

    def _build_traps(self):
        scroll, l = self._create_scroll()
        
        lbl = QLabel("⚠️ Alertes Anti-Pièges — Questions Fréquentes en Examen")
        lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
        lbl.setStyleSheet(f"color: {self.theme.warning}; margin-top: 10px; margin-bottom: 10px;")
        l.addWidget(lbl)
        
        for t in PROF_TRAPS:
            c = QFrame()
            c.setStyleSheet(f"background: {self.theme.bg}; border-radius: 8px; border: 1px solid {self.theme.warning};")
            cl = QVBoxLayout(c)
            
            tlbl = QLabel(f"{t.get('danger','⚠️')} [{t.get('matiere','')}] — {t.get('piege','')}")
            tlbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
            tlbl.setStyleSheet(f"color: {self.theme.warning};")
            cl.addWidget(tlbl)
            
            qlbl = QLabel(f"❓ {t.get('question_type','')}")
            qlbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-style: italic;")
            cl.addWidget(qlbl)
            
            elbl = QLabel(f"❌ Erreur classique : {t.get('erreur_classique','')}")
            elbl.setStyleSheet(f"color: {self.theme.danger}; margin-top: 5px;")
            cl.addWidget(elbl)
            
            blbl = QLabel(f"✅ Bonne réponse : {t.get('bonne_reponse','')}")
            blbl.setStyleSheet(f"color: {self.theme.success}; margin-top: 5px;")
            blbl.setWordWrap(True)
            cl.addWidget(blbl)
            
            l.addWidget(c)
            
        l.addStretch()
        return scroll

    def _build_linux(self):
        scroll, l = self._create_scroll()
        
        for c in LINUX_COMMANDS:
            fr = QFrame()
            fr.setStyleSheet(f"background: {self.theme.bg}; border-radius: 6px; border: 1px solid {self.theme.border};")
            fl = QHBoxLayout(fr)
            
            clbl = QLabel(c.get("cmd", ""))
            clbl.setFont(QFont("Consolas", 12, QFont.Bold))
            clbl.setStyleSheet("color: #00ff41;")
            clbl.setFixedWidth(240)
            fl.addWidget(clbl)
            
            dlbl = QLabel(c.get("description", ""))
            dlbl.setFont(QFont("Segoe UI", 12))
            dlbl.setStyleSheet(f"color: {self.theme.text};")
            fl.addWidget(dlbl, 1)
            
            if "exemple" in c:
                elbl = QLabel(f"ex: {c['exemple']}")
                elbl.setFont(QFont("Consolas", 10))
                elbl.setStyleSheet(f"color: {self.theme.text_secondary};")
                fl.addWidget(elbl)
                
            l.addWidget(fr)
            
        l.addStretch()
        return scroll

    def _build_osi(self):
        scroll, l = self._create_scroll()
        
        lbl = QLabel("Modèle OSI — Les 7 Couches")
        lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
        lbl.setStyleSheet(f"color: {self.theme.accent}; margin-top: 10px; margin-bottom: 10px;")
        l.addWidget(lbl)
        
        for layer in reversed(OSI_LAYERS):
            fr = QFrame()
            fr.setStyleSheet(f"background: {self.theme.bg}; border-radius: 8px; border: 1px solid {self.theme.border};")
            fl = QHBoxLayout(fr)
            
            num = QLabel(f"C{layer.get('numero','')}")
            num.setFont(QFont("Consolas", 14, QFont.Bold))
            num.setStyleSheet(f"color: {self.theme.accent};")
            num.setFixedWidth(40)
            fl.addWidget(num)
            
            nlbl = QLabel(layer.get("nom", ""))
            nlbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
            nlbl.setStyleSheet(f"color: {self.theme.text};")
            nlbl.setFixedWidth(130)
            fl.addWidget(nlbl)
            
            rlbl = QLabel(layer.get("role", ""))
            rlbl.setStyleSheet(f"color: {self.theme.text_secondary};")
            fl.addWidget(rlbl, 1)
            
            elbl = QLabel(layer.get("exemples", ""))
            elbl.setStyleSheet("color: #4fc3f7;")
            fl.addWidget(elbl)
            
            l.addWidget(fr)
            
        l.addStretch()
        return scroll

    def _build_protocols(self):
        scroll, l = self._create_scroll()
        
        for p in NETWORK_PROTOCOLS:
            fr = QFrame()
            fr.setStyleSheet(f"background: {self.theme.bg}; border-radius: 6px; border: 1px solid {self.theme.border};")
            fl = QHBoxLayout(fr)
            
            port = QLabel(f":{p.get('port','')}")
            port.setFont(QFont("Consolas", 12, QFont.Bold))
            port.setStyleSheet(f"color: {self.theme.accent};")
            port.setFixedWidth(70)
            fl.addWidget(port)
            
            prot = QLabel(p.get("protocole", ""))
            prot.setFont(QFont("Segoe UI", 12, QFont.Bold))
            prot.setStyleSheet(f"color: {self.theme.text};")
            prot.setFixedWidth(80)
            fl.addWidget(prot)
            
            desc = QLabel(p.get("description", ""))
            desc.setStyleSheet(f"color: {self.theme.text_secondary};")
            fl.addWidget(desc, 1)
            
            typ = QLabel(p.get("type", ""))
            typ.setStyleSheet(f"color: {self.theme.accent2};")
            fl.addWidget(typ)
            
            l.addWidget(fr)
            
        l.addStretch()
        return scroll
