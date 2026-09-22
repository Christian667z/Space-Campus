"""
Asta Académie — Quiz Page (PySide6)
Interface de quiz interactif.
"""
import random
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QScrollArea, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from ui.themes.theme_manager import Theme
from ui.components.widgets import SectionHeader, Card

try:
    from core.logic_tools import QUIZ_QUESTIONS
except ImportError:
    QUIZ_QUESTIONS = {
        "Général": [
            {"question": "Pas de données trouvées", "options": ["A", "B", "C", "D"], "correct": 0, "explication": "Erreur DB"}
        ]
    }

class QuizPage(QWidget):
    def __init__(self, theme: Theme, user_id: int, parent=None):
        super().__init__(parent)
        self.theme = theme
        self.user_id = user_id
        
        self.quiz_score = 0
        self.quiz_total = 0
        self.quiz_asked = set()
        self.current_q = None
        self.quiz_answered = False
        
        self.setStyleSheet("background: transparent;")
        self._build()

    def _build(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)
        
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = SectionHeader("Quiz — Teste tes Connaissances", "Questions de niveau universitaire sur toutes les matières L1→L4")
        layout.addWidget(header)

        # ── Score Panel ──
        score_card = Card()
        score_layout = QHBoxLayout(score_card)
        score_layout.setContentsMargins(20, 15, 20, 15)
        
        self.lbl_score = QLabel(f"✅ Score : {self.quiz_score} / {self.quiz_total}")
        self.lbl_score.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.lbl_score.setStyleSheet(f"color: {self.theme.success};")
        score_layout.addWidget(self.lbl_score)
        
        self.lbl_pct = QLabel("  (0%)")
        self.lbl_pct.setFont(QFont("Segoe UI", 12))
        self.lbl_pct.setStyleSheet(f"color: {self.theme.accent};")
        score_layout.addWidget(self.lbl_pct)
        
        score_layout.addStretch()
        
        btn_reset = QPushButton("🔄 Reset Score")
        btn_reset.setProperty("class", "danger_btn")
        btn_reset.clicked.connect(self._reset_score)
        score_layout.addWidget(btn_reset)
        
        layout.addWidget(score_card)

        # ── Filters ──
        filter_layout = QHBoxLayout()
        filter_lbl = QLabel("Filtrer par matière :")
        filter_lbl.setStyleSheet(f"color: {self.theme.text_secondary};")
        filter_layout.addWidget(filter_lbl)
        
        self.cb_filter = QComboBox()
        matieres = sorted(list(QUIZ_QUESTIONS.keys()))
        self.cb_filter.addItems(["Toutes"] + matieres)
        filter_layout.addWidget(self.cb_filter)
        
        btn_next = QPushButton("Nouvelle Question")
        btn_next.setProperty("class", "primary")
        btn_next.clicked.connect(self._next_question)
        filter_layout.addWidget(btn_next)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)

        # ── Question Card ──
        q_card = Card()
        q_card.setStyleSheet(f"background: {self.theme.card}; border: 1px solid {self.theme.accent}; border-radius: 8px;")
        q_layout = QVBoxLayout(q_card)
        q_layout.setContentsMargins(20, 20, 20, 20)
        
        self.lbl_matiere = QLabel("")
        self.lbl_matiere.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.lbl_matiere.setStyleSheet(f"color: {self.theme.accent};")
        q_layout.addWidget(self.lbl_matiere)
        
        self.lbl_question = QLabel("Clique sur 'Nouvelle Question' pour commencer !")
        self.lbl_question.setFont(QFont("Segoe UI", 14))
        self.lbl_question.setStyleSheet(f"color: {self.theme.text}; margin-top: 10px; margin-bottom: 10px;")
        self.lbl_question.setWordWrap(True)
        q_layout.addWidget(self.lbl_question)
        
        layout.addWidget(q_card)

        # ── Options ──
        self.btn_options = []
        for i in range(4):
            btn = QPushButton("")
            btn.setFont(QFont("Segoe UI", 12))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {self.theme.bg};
                    color: {self.theme.text};
                    border: 1px solid {self.theme.border};
                    border-radius: 6px;
                    padding: 15px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background: {self.theme.card_hover};
                }}
            """)
            btn.clicked.connect(lambda checked=False, idx=i: self._answer(idx))
            layout.addWidget(btn)
            self.btn_options.append(btn)

        # ── Result & Explication ──
        self.lbl_result = QLabel("")
        self.lbl_result.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.lbl_result.setWordWrap(True)
        layout.addWidget(self.lbl_result)
        
        self.lbl_expl = QLabel("")
        self.lbl_expl.setFont(QFont("Segoe UI", 11))
        self.lbl_expl.setStyleSheet(f"color: {self.theme.text_secondary};")
        self.lbl_expl.setWordWrap(True)
        layout.addWidget(self.lbl_expl)
        
        layout.addStretch()
        
        self._next_question()

    def _next_question(self):
        filtre = self.cb_filter.currentText()
        matiere = None if filtre == "Toutes" else filtre
        
        all_q = QUIZ_QUESTIONS.get(matiere, []) if matiere else [q for qs in QUIZ_QUESTIONS.values() for q in qs]
        available_q = [q for q in all_q if str(q) not in self.quiz_asked]
        
        if not available_q:
            self.quiz_asked.clear()
            available_q = all_q
            if not available_q:
                return

        self.current_q = random.choice(available_q)
        self.quiz_asked.add(str(self.current_q))
        self.quiz_answered = False
        
        q = self.current_q
        self.lbl_question.setText(q.get("question", ""))
        self.lbl_matiere.setText(f"Matière : {q.get('matiere', filtre)} | Niveau : {q.get('niveau', '?')}")
        self.lbl_result.setText("")
        self.lbl_expl.setText("")
        
        for i, btn in enumerate(self.btn_options):
            if i < len(q.get("options", [])):
                btn.setText(f" {chr(65+i)}. {q['options'][i]}")
                btn.setVisible(True)
            else:
                btn.setVisible(False)
            btn.setEnabled(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {self.theme.bg};
                    color: {self.theme.text};
                    border: 1px solid {self.theme.border};
                    border-radius: 6px;
                    padding: 15px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background: {self.theme.card_hover};
                }}
            """)

    def _answer(self, idx):
        if not self.current_q or self.quiz_answered:
            return
            
        self.quiz_answered = True
        self.quiz_total += 1
        correct_idx = self.current_q.get("correct", 0)
        
        for i, btn in enumerate(self.btn_options):
            btn.setEnabled(False)
            if i == correct_idx:
                btn.setStyleSheet(f"background: {self.theme.success}; color: #ffffff; border: none; border-radius: 6px; padding: 15px; text-align: left;")
            elif i == idx and idx != correct_idx:
                btn.setStyleSheet(f"background: {self.theme.danger}; color: #ffffff; border: none; border-radius: 6px; padding: 15px; text-align: left;")

        if idx == correct_idx:
            self.quiz_score += 1
            self.lbl_result.setText("✅ Correct ! +10 pts")
            self.lbl_result.setStyleSheet(f"color: {self.theme.success};")
            self._add_xp(10)
        else:
            correct_text = self.current_q['options'][correct_idx]
            self.lbl_result.setText(f"❌ Incorrect. La bonne réponse était : {correct_text}")
            self.lbl_result.setStyleSheet(f"color: {self.theme.danger};")
            
        self.lbl_expl.setText(f"💡 {self.current_q.get('explication', '')}")
        self._update_score_ui()
        
        # Save to SQLite
        try:
            from database.db_manager import update_quiz_stats
            from core.config import DB_FILE
            update_quiz_stats(DB_FILE, self.user_id, self.quiz_score, self.quiz_total)
        except Exception:
            pass

    def _update_score_ui(self):
        self.lbl_score.setText(f"✅ Score : {self.quiz_score} / {self.quiz_total}")
        pct = int(self.quiz_score / self.quiz_total * 100) if self.quiz_total > 0 else 0
        self.lbl_pct.setText(f"  ({pct}%)")

    def _reset_score(self):
        self.quiz_score = 0
        self.quiz_total = 0
        self._update_score_ui()
        self.lbl_result.setText("")
        self.lbl_expl.setText("")
        try:
            from database.db_manager import update_quiz_stats
            from core.config import DB_FILE
            update_quiz_stats(DB_FILE, self.user_id, 0, 0)
        except Exception:
            pass

    def _add_xp(self, points):
        try:
            from database.db_manager import log_xp_earned
            from core.config import DB_FILE
            from datetime import datetime
            today = datetime.now().strftime('%Y-%m-%d')
            log_xp_earned(DB_FILE, self.user_id, today, points)
        except Exception:
            pass
