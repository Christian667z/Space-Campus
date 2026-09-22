"""
Asta Académie — Profile Page (PySide6)
Mon Profil Étudiant et Statistiques.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, 
    QComboBox, QScrollArea, QFrame, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.themes.theme_manager import Theme
from ui.components.widgets import SectionHeader, Card

class ProfilePage(QWidget):
    def __init__(self, profile: dict, user_id: int, theme: Theme, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.user_id = user_id
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
        layout.setSpacing(20)

        header = SectionHeader("👤 Mon Profil Étudiant", "Personnalise ton expérience Asta Académie")
        layout.addWidget(header)

        # ── Formulaire ──
        form_card = Card()
        form_l = QVBoxLayout(form_card)
        form_l.setContentsMargins(20, 20, 20, 20)
        form_l.setSpacing(12)
        
        self.entries = {}
        fields = [("Nom :", "nom", "Ton nom..."), ("Prénom :", "prenom", "Ton prénom..."), ("Matricule :", "matricule", "ex: 2024-001")]
        
        for lbl_text, key, placeholder in fields:
            row = QHBoxLayout()
            lbl = QLabel(lbl_text)
            lbl.setFixedWidth(120)
            lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-weight: bold;")
            row.addWidget(lbl)
            
            ent = QLineEdit(self.profile.get(key, ""))
            ent.setPlaceholderText(placeholder)
            ent.setStyleSheet(f"background: {self.theme.bg}; color: {self.theme.text}; border: 1px solid {self.theme.border}; border-radius: 6px; padding: 8px;")
            row.addWidget(ent)
            self.entries[key] = ent
            form_l.addLayout(row)
            
        row_niv = QHBoxLayout()
        lbl_niv = QLabel("Classe (Niveau) :")
        lbl_niv.setFixedWidth(120)
        lbl_niv.setStyleSheet(f"color: {self.theme.text_secondary}; font-weight: bold;")
        row_niv.addWidget(lbl_niv)
        
        self.cb_niv = QComboBox()
        self.cb_niv.addItems(["L1", "L2", "L3", "L4"])
        self.cb_niv.setCurrentText(self.profile.get("niveau", "L2"))
        row_niv.addWidget(self.cb_niv)
        row_niv.addStretch()
        form_l.addLayout(row_niv)
        
        btn_save = QPushButton("💾 Sauvegarder le Profil")
        btn_save.setProperty("class", "success_btn")
        btn_save.clicked.connect(self._save)
        form_l.addWidget(btn_save)
        layout.addWidget(form_card)

        # ── Stats ──
        stats_card = Card()
        stats_l = QVBoxLayout(stats_card)
        stats_l.setContentsMargins(20, 20, 20, 20)
        stats_l.setSpacing(10)
        
        t_stats = QLabel("📊 Mes Statistiques")
        t_stats.setFont(QFont("Segoe UI", 14, QFont.Bold))
        t_stats.setStyleSheet(f"color: {self.theme.accent};")
        stats_l.addWidget(t_stats)
        
        points = self.profile.get("points", 0)
        streak = self.profile.get("streak", 0)
        badges = self.profile.get("badges", [])
        quiz_total = 0
        try:
            from database.db_manager import get_quiz_stats
            from core.config import DB_FILE
            _, quiz_total = get_quiz_stats(DB_FILE, self.user_id)
        except Exception:
            pass
            
        stats_data = [
            ("⭐ Points totaux", str(points)),
            ("🧠 Quiz répondus", str(quiz_total)),
            ("🔥 Streak actuel", f"{streak} jours"),
            ("🏅 Badges obtenus", str(len(badges)))
        ]
        
        for k, v in stats_data:
            fr = QFrame()
            fr.setStyleSheet(f"background: {self.theme.bg}; border-radius: 6px; border: 1px solid {self.theme.border};")
            fl = QHBoxLayout(fr)
            
            lbl_k = QLabel(k)
            lbl_k.setStyleSheet(f"color: {self.theme.text};")
            fl.addWidget(lbl_k)
            
            lbl_v = QLabel(v)
            lbl_v.setFont(QFont("Segoe UI", 12, QFont.Bold))
            lbl_v.setStyleSheet(f"color: {self.theme.accent};")
            fl.addWidget(lbl_v, 0, Qt.AlignRight)
            
            stats_l.addWidget(fr)
            
        layout.addWidget(stats_card)
        
        # ── Badges ──
        badge_card = Card()
        badge_l = QVBoxLayout(badge_card)
        badge_l.setContentsMargins(20, 20, 20, 20)
        
        t_badge = QLabel("🏅 Badges Débloqués")
        t_badge.setFont(QFont("Segoe UI", 14, QFont.Bold))
        t_badge.setStyleSheet(f"color: {self.theme.accent}; margin-bottom: 10px;")
        badge_l.addWidget(t_badge)
        
        if badges:
            for b in badges:
                lbl = QLabel(f"🏅 {b}")
                lbl.setFont(QFont("Segoe UI", 11))
                lbl.setStyleSheet(f"color: {self.theme.text}; padding: 4px;")
                badge_l.addWidget(lbl)
        else:
            lbl = QLabel("Aucun badge encore. Réponds à des quiz pour en débloquer !")
            lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-style: italic;")
            badge_l.addWidget(lbl)
            
        layout.addWidget(badge_card)
        layout.addStretch()

    def _save(self):
        for k, ent in self.entries.items():
            self.profile[k] = ent.text().strip()
        self.profile["niveau"] = self.cb_niv.currentText()
        
        try:
            from core.config import PROFILE_FILE, save_json
            save_json(PROFILE_FILE, self.profile)
            QMessageBox.information(self, "Sauvegardé", "Profil mis à jour avec succès !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de sauvegarder: {e}")
