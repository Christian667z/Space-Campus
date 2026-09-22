"""
Asta Académie — Oracle Page (PySide6)
L'Oracle : Faits, citations, histoire.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.themes.theme_manager import Theme
from ui.components.widgets import SectionHeader, Card

try:
    from utils.oracle_hub import get_daily_tip, get_random_fact, get_random_quote, TECH_TIMELINE, HAITI_TECH_HISTORY
except ImportError:
    get_daily_tip = lambda: "L'intelligence n'est pas de tout savoir, mais de savoir où chercher."
    get_random_fact = lambda: "Le premier bug informatique était un vrai papillon de nuit."
    get_random_quote = lambda: {"citation": "Talk is cheap. Show me the code.", "auteur": "Linus Torvalds", "role": "Créateur de Linux"}
    TECH_TIMELINE = []
    HAITI_TECH_HISTORY = []

class OraclePage(QWidget):
    def __init__(self, theme: Theme, parent=None):
        super().__init__(parent)
        self.theme = theme
        self.setStyleSheet("background: transparent;")
        self._build()

    def _build(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        
        w = QWidget()
        scroll.setWidget(w)
        layout = QVBoxLayout(w)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = SectionHeader("L'Oracle — Savoir", "Faits, citations et histoire de l'informatique")
        layout.addWidget(header)

        # ── Astuce du jour ──
        tip_card = Card()
        tip_l = QVBoxLayout(tip_card)
        tip_l.setContentsMargins(20, 15, 20, 15)
        lbl_tip = QLabel(f"💡 {get_daily_tip()}")
        lbl_tip.setFont(QFont("Segoe UI", 12))
        lbl_tip.setStyleSheet(f"color: {self.theme.accent};")
        lbl_tip.setWordWrap(True)
        tip_l.addWidget(lbl_tip)
        layout.addWidget(tip_card)

        # ── Fait du moment ──
        fact_card = Card()
        fact_l = QVBoxLayout(fact_card)
        fact_l.setContentsMargins(20, 20, 20, 20)
        fact_l.setSpacing(10)
        
        lbl_f_t = QLabel("⚡ Fait du Moment")
        lbl_f_t.setFont(QFont("Segoe UI", 14, QFont.Bold))
        lbl_f_t.setStyleSheet(f"color: {self.theme.accent};")
        fact_l.addWidget(lbl_f_t)
        
        self.lbl_fact = QLabel(get_random_fact())
        self.lbl_fact.setFont(QFont("Segoe UI", 12))
        self.lbl_fact.setStyleSheet(f"color: {self.theme.text};")
        self.lbl_fact.setWordWrap(True)
        fact_l.addWidget(self.lbl_fact)
        
        btn_fact = QPushButton("🔄 Nouveau Fait")
        btn_fact.setProperty("class", "primary")
        btn_fact.setFixedWidth(160)
        btn_fact.clicked.connect(lambda: self.lbl_fact.setText(get_random_fact()))
        fact_l.addWidget(btn_fact)
        layout.addWidget(fact_card)

        # ── Citation ──
        quote_card = Card()
        quote_l = QVBoxLayout(quote_card)
        quote_l.setContentsMargins(20, 20, 20, 20)
        
        q = get_random_quote()
        lbl_q = QLabel(f'❝ {q["citation"]} ❞')
        lbl_q.setFont(QFont("Segoe UI", 14, italic=True))
        lbl_q.setStyleSheet(f"color: {self.theme.text};")
        lbl_q.setAlignment(Qt.AlignCenter)
        lbl_q.setWordWrap(True)
        quote_l.addWidget(lbl_q)
        
        lbl_a = QLabel(f"— {q['auteur']}, {q['role']}")
        lbl_a.setFont(QFont("Segoe UI", 11))
        lbl_a.setStyleSheet(f"color: {self.theme.text_secondary};")
        lbl_a.setAlignment(Qt.AlignCenter)
        quote_l.addWidget(lbl_a)
        layout.addWidget(quote_card)

        # ── Chronologie ──
        lbl_chron = QLabel("🕰️ Chronologie des Génies de l'Informatique")
        lbl_chron.setFont(QFont("Segoe UI", 16, QFont.Bold))
        lbl_chron.setStyleSheet(f"color: {self.theme.accent}; margin-top: 10px;")
        layout.addWidget(lbl_chron)
        
        for entry in TECH_TIMELINE:
            fr = QFrame()
            fr.setStyleSheet(f"background: {self.theme.card}; border-radius: 8px; border: 1px solid {self.theme.border};")
            fl = QHBoxLayout(fr)
            
            annee = QLabel(entry.get("annee", ""))
            annee.setFont(QFont("Consolas", 14, QFont.Bold))
            annee.setStyleSheet(f"color: {self.theme.accent};")
            annee.setFixedWidth(60)
            fl.addWidget(annee)
            
            pays = QLabel(entry.get("pays", ""))
            pays.setFixedWidth(40)
            fl.addWidget(pays)
            
            desc = QLabel(f"{entry.get('personne', '')} — {entry.get('contribution', '')}")
            desc.setFont(QFont("Segoe UI", 12))
            desc.setStyleSheet(f"color: {self.theme.text};")
            desc.setWordWrap(True)
            fl.addWidget(desc, 1)
            layout.addWidget(fr)

        # ── Haïti Tech ──
        lbl_ht = QLabel("🇭🇹 Haïti & l'Informatique")
        lbl_ht.setFont(QFont("Segoe UI", 16, QFont.Bold))
        lbl_ht.setStyleSheet(f"color: {self.theme.accent}; margin-top: 10px;")
        layout.addWidget(lbl_ht)
        
        for item in HAITI_TECH_HISTORY:
            ht = Card()
            ht_l = QVBoxLayout(ht)
            
            titre = QLabel(item.get("titre", ""))
            titre.setFont(QFont("Segoe UI", 13, QFont.Bold))
            titre.setStyleSheet(f"color: {self.theme.accent};")
            ht_l.addWidget(titre)
            
            cont = QLabel(item.get("contenu", ""))
            cont.setFont(QFont("Segoe UI", 12))
            cont.setStyleSheet(f"color: {self.theme.text};")
            cont.setWordWrap(True)
            ht_l.addWidget(cont)
            layout.addWidget(ht)
            
        layout.addStretch()
