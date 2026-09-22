"""
Asta Académie — Dashboard Page v2.5 (PySide6)
==============================================
Tableau de bord centralisé et réactif.
Optimisation vectorielle (SVG), gestion défensive de la DB et design haut de gamme.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QColor, QPixmap, QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QSizePolicy
)

from ui.themes.theme_manager import Theme
from ui.components.widgets import (
    Card, StatCard, SectionHeader, XPGraph, Badge, add_shadow
)
from utils.svg_manager import SVGManager

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Dictionnaire de secours : Icônes SVG Inline (Poids plume, Résilience absolue)
# ---------------------------------------------------------------------------
FALLBACK_SVGS: Dict[str, str] = {
    "flame": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "badge": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "graph": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    "oracle": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M12 2a10 10 0 0 1 7.54 16.59c-.4.45-.64 1.04-.64 1.66V22H5.1v-1.75c0-.62-.24-1.21-.64-1.66A10 10 0 0 1 12 2z"/></svg>',
    "zap": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "trophy": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16M10 14.66V17c0 .55-.45 1-1 1H4v2h16v-2h-5c-.55 0-1-.45-1-1v-2.34M12 2a5 5 0 0 0-5 5v4c0 2.76 2.24 5 5 5s5-2.24 5-5V7a5 5 0 0 0-5-5z"/></svg>'
}

def _get_vector_icon(name: str, color: str, size: int) -> QIcon:
    """Génère une icône QIcon via SVGManager, avec un fallback vectoriel natif inline garanti."""
    icon = SVGManager.get_icon(name, color=color, size=size)
    if not icon.isNull():
        return icon
    
    # Stratégie de secours : Reconstruction dynamique par template SVG si la ressource manque sur le disque
    fallback_template = FALLBACK_SVGS.get(name)
    if fallback_template:
        svg_data = fallback_template.format(color=color).encode('utf-8')
        from PySide6.QtSvg import QSvgRenderer
        renderer = QSvgRenderer(svg_data)
        if renderer.isValid():
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            from PySide6.QtGui import QPainter
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            return QIcon(pixmap)
            
    return QIcon()


# ===========================================================================
# Composant de Rendu : Dashboard Principal (Production-Ready)
# ===========================================================================
class DashboardPage(QWidget):
    """
    Vue principale réactive de l'écosystème Asta Académie.
    Contient le suivi de l'expérience, l'analyse comportementale et le module Oracle.
    """
    def __init__(self, profile: dict[str, Any], user_id: int, theme: Theme, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.profile: dict[str, Any] = profile
        self.user_id: int = user_id
        self.theme: Theme = theme
        
        self.xp_card: Optional[StatCard] = None
        self.streak_card: Optional[StatCard] = None
        self.badge_card: Optional[StatCard] = None
        self.oracle_lbl: Optional[QLabel] = None
        self.xp_graph: Optional[XPGraph] = None

        self.setStyleSheet("background: transparent;")
        self._build()
        
        # Déclenchement de l'animation de manière asynchrone sécurisée
        QTimer.singleShot(300, self._animate_stats)

    def _build(self) -> None:
        # Zone de défilement principale (ScrollArea)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self._apply_premium_scrollbar_style(scroll)
        scroll.setStyleSheet("background: transparent; border: none;")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Injection des sous-modules d'interface
        self._build_header(layout)
        self._build_stat_cards(layout)
        self._build_main_content(layout)
        self._build_badges_section(layout)

        layout.addStretch()

    # ── MODULE 1 : HEADER & BANNER VECTORIELLE ─────────────────────────────

    def _build_header(self, parent_layout: QVBoxLayout) -> None:
        header = Card()
        add_shadow(header, blur=16, y=4)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(28, 22, 28, 22)

        left = QVBoxLayout()
        left.setSpacing(4)

        nom: str = self.profile.get("nom", "Étudiant")
        niveau: str = self.profile.get("niveau", "L2")

        welcome = QLabel(f"Bienvenue, {nom} !")
        welcome.setFont(QFont("Segoe UI", 22, QFont.Bold))
        welcome.setStyleSheet(f"color: {self.theme.text}; border: none; background: transparent;")
        left.addWidget(welcome)

        subtitle = QLabel(f"Prêt à apprendre aujourd'hui ?   •   Niveau actuel : {niveau}")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {self.theme.text_secondary}; border: none; background: transparent;")
        left.addWidget(subtitle)

        # Date localisée robuste
        now = datetime.now()
        date_lbl = QLabel(f"{now.strftime('%A %d %B %Y').capitalize()}")
        date_lbl.setFont(QFont("Segoe UI", 10))
        date_lbl.setStyleSheet(f"color: {self.theme.text_disabled}; border: none; background: transparent;")
        left.addWidget(date_lbl)

        h_layout.addLayout(left, 1)

        # Bloc de suivi de la Flamme (Streak / Série Active)
        streak = self.profile.get("streak", 0)
        streak_widget = QWidget()
        streak_widget.setStyleSheet("background: transparent;")
        streak_layout = QVBoxLayout(streak_widget)
        streak_layout.setAlignment(Qt.AlignCenter)
        streak_layout.setSpacing(4)

        flame = QLabel()
        flame_icon = _get_vector_icon("flame", color=self.theme.warning, size=48)
        if not flame_icon.isNull():
            flame.setPixmap(flame_icon.pixmap(48, 48))
        flame.setAlignment(Qt.AlignCenter)
        flame.setStyleSheet("border: none; background: transparent;")
        streak_layout.addWidget(flame)

        streak_lbl = QLabel(f"{streak}")
        streak_lbl.setFont(QFont("Consolas", 28, QFont.Bold))
        streak_lbl.setStyleSheet(f"color: {self.theme.warning}; border: none; background: transparent;")
        streak_lbl.setAlignment(Qt.AlignCenter)
        streak_layout.addWidget(streak_lbl)

        streak_txt = QLabel("Jours consécutifs")
        streak_txt.setFont(QFont("Segoe UI", 9))
        streak_txt.setStyleSheet(f"color: {self.theme.text_secondary}; border: none; background: transparent;")
        streak_txt.setAlignment(Qt.AlignCenter)
        streak_layout.addWidget(streak_txt)

        h_layout.addWidget(streak_widget)
        parent_layout.addWidget(header)

    # ── MODULE 2 : KIP / METRICS DISPLAY SYSTEM ─────────────────────────────

    def _build_stat_cards(self, parent_layout: QVBoxLayout) -> None:
        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid = QHBoxLayout(grid_widget)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(16)

        # Extraction sécurisée de la base SQLite
        try:
            from database.db_manager import get_progress, get_completed_missions
            from main_qt import DB_FILE
            progress = get_progress(DB_FILE, self.user_id)
            missions = get_completed_missions(DB_FILE, self.user_id)
        except Exception as e:
            logger.warning("Défaillance IO/DB d'indexation des métriques (Utilisation Fallbacks) : %s", e)
            progress = {"points": self.profile.get("points", 0), "streak": 0, "niveau": "L2"}
            missions = []

        badges_count: int = len(self.profile.get("badges", []))
        points: int = progress.get("points", 0)
        streak: int = progress.get("streak", self.profile.get("streak", 0))

        # Instanciation des cartes avec injection d'icônes vectorielles standardisées
        self.xp_card = StatCard("star", "Points d'Expérience", f"{points} XP", self.theme.warning)
        self.streak_card = StatCard("flame", "Série Active (Streak)", f"{streak} Jours", self.theme.danger)
        self.badge_card = StatCard("badge", "Badges Obtenus", f"{badges_count} Badges", self.theme.success)
        mission_card = StatCard("target", "Missions Complètes", f"{len(missions)} Missions", self.theme.info)

        for card in [self.xp_card, self.streak_card, self.badge_card, mission_card]:
            grid.addWidget(card)

        parent_layout.addWidget(grid_widget)

    # ── MODULE 3 : GRAPH & MODULE ORACLE ORACLE INTÉGRÉ ────────────────────

    def _build_main_content(self, parent_layout: QVBoxLayout) -> None:
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(16)

        # ── Sous-Panneau GAUCHE : Graphique XP Vectoriel ──
        graph_card = Card()
        add_shadow(graph_card, blur=12)
        graph_layout = QVBoxLayout(graph_card)
        graph_layout.setContentsMargins(20, 16, 20, 16)

        graph_header = QHBoxLayout()
        icon_graph = QLabel()
        graph_icon = _get_vector_icon("graph", color=self.theme.text, size=24)
        if not graph_icon.isNull():
            icon_graph.setPixmap(graph_icon.pixmap(24, 24))
        icon_graph.setStyleSheet("border: none; background: transparent;")
        graph_header.addWidget(icon_graph)
        
        graph_title = QLabel("Progression Hebdomadaire (XP)")
        graph_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        graph_title.setStyleSheet(f"color: {self.theme.text}; border: none; background: transparent;")
        graph_header.addWidget(graph_title)
        graph_header.addStretch()
        
        graph_header.addWidget(Badge("Cette semaine", "accent"))
        graph_layout.addLayout(graph_header)

        self.xp_graph = XPGraph()
        self.xp_graph.setMinimumHeight(180)
        graph_layout.addWidget(self.xp_graph)
        self._load_weekly_xp()

        row_layout.addWidget(graph_card, 3)

        # ── Sous-Panneau DROIT : L'Oracle Académique ──
        oracle_card = Card()
        add_shadow(oracle_card, blur=12)
        oracle_layout = QVBoxLayout(oracle_card)
        oracle_layout.setContentsMargins(20, 20, 20, 20)
        oracle_layout.setSpacing(12)
        oracle_layout.setAlignment(Qt.AlignTop)

        oracle_header = QHBoxLayout()
        oracle_header.setAlignment(Qt.AlignCenter)
        
        icon_oracle = QLabel()
        oracle_icon = _get_vector_icon("oracle", color=self.theme.accent, size=24)
        if not oracle_icon.isNull():
            icon_oracle.setPixmap(oracle_icon.pixmap(24, 24))
        icon_oracle.setStyleSheet("border: none; background: transparent;")
        oracle_header.addWidget(icon_oracle)

        oracle_title = QLabel("L'Oracle")
        oracle_title.setFont(QFont("Consolas", 15, QFont.Bold))
        oracle_title.setStyleSheet(f"color: {self.theme.accent}; border: none; background: transparent;")
        oracle_header.addWidget(oracle_title)
        oracle_layout.addLayout(oracle_header)

        # Traitement sécurisé de la chaîne Oracle Hub
        try:
            from utils.oracle_hub import get_daily_tip
            tip_text: str = get_daily_tip()
        except Exception as e:
            logger.warning("Impossible de joindre OracleHub : %s", e)
            tip_text = "« La connaissance s'acquiert par l'expérience, tout le reste n'est qu'information. »\n— Albert Einstein"

        self.oracle_lbl = QLabel(tip_text)
        self.oracle_lbl.setFont(QFont("Segoe UI", 12))
        self.oracle_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-style: italic; border: none; background: transparent;")
        self.oracle_lbl.setWordWrap(True)
        self.oracle_lbl.setAlignment(Qt.AlignCenter)
        oracle_layout.addWidget(self.oracle_lbl)

        oracle_layout.addStretch()

        refresh_btn = QPushButton("Nouvelle Citation")
        zap_icon = _get_vector_icon("zap", color="#ffffff", size=18)
        if not zap_icon.isNull():
            refresh_btn.setIcon(zap_icon)
        refresh_btn.setProperty("class", "secondary")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.theme.accent}; color: #ffffff;
                border: 1px solid {self.theme.border}; border-radius: 6px;
                padding: 6px 12px; font-size: 12px; font-weight: bold;
            }}
            QPushButton:hover {{ background: {self.theme.accent}cc; }}
        """)
        refresh_btn.clicked.connect(self._refresh_oracle)
        oracle_layout.addWidget(refresh_btn)

        row_layout.addWidget(oracle_card, 1)
        parent_layout.addWidget(row)

    # ── MODULE 4 : GAMIFICATION BADGES DISPLAYER ───────────────────────────

    def _build_badges_section(self, parent_layout: QVBoxLayout) -> None:
        badges: List[str] = self.profile.get("badges", [])
        if not badges:
            return

        section = Card()
        s_layout = QVBoxLayout(section)
        s_layout.setContentsMargins(20, 16, 20, 16)
        s_layout.setSpacing(12)

        t_layout = QHBoxLayout()
        icon_trophy = QLabel()
        trophy_icon = _get_vector_icon("trophy", color=self.theme.text, size=24)
        if not trophy_icon.isNull():
            icon_trophy.setPixmap(trophy_icon.pixmap(24, 24))
        icon_trophy.setStyleSheet("border: none; background: transparent;")
        t_layout.addWidget(icon_trophy)

        title = QLabel("Mes Badges")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet(f"color: {self.theme.text}; border: none; background: transparent;")
        t_layout.addWidget(title)
        t_layout.addStretch()
        s_layout.addLayout(t_layout)

        badges_row = QHBoxLayout()
        badges_row.setSpacing(8)
        for badge_text in badges:
            badge = Badge(badge_text, "success")
            badges_row.addWidget(badge)
        badges_row.addStretch()
        s_layout.addLayout(badges_row)
        
        parent_layout.addWidget(section)

    # ── ROUTINES SYSTÈMES & PIPELINES DE FLUX ───────────────────────────────

    def _load_weekly_xp(self) -> None:
        try:
            from database.db_manager import get_weekly_xp
            from main_qt import DB_FILE
            today = datetime.now().date()
            dates = [(today - timedelta(days=6 - i)).strftime('%Y-%m-%d') for i in range(7)]
            labels = [(today - timedelta(days=6 - i)).strftime('%a')[:1] for i in range(7)]
            xp_data = get_weekly_xp(DB_FILE, self.user_id, dates)
            if self.xp_graph:
                self.xp_graph.set_data(xp_data, labels, self.theme.accent)
        except Exception as e:
            logger.error("Défaillance de chargement de l'historique hebdomadaire d'XP : %s", e)
            if self.xp_graph:
                self.xp_graph.set_data([0] * 7, list("LMMJVSD"), self.theme.accent)

    def _animate_stats(self) -> None:
        try:
            from database.db_manager import get_progress
            from main_qt import DB_FILE
            progress = get_progress(DB_FILE, self.user_id)
            points = progress.get("points", 0)
            if self.xp_card:
                self.xp_card.update_value(f"{points} XP")
        except Exception as e:
            logger.warning("Échec de l'animation de rafraîchissement des stats : %s", e)

    def _refresh_oracle(self) -> None:
        try:
            from utils.oracle_hub import get_random_fact
            if self.oracle_lbl:
                self.oracle_lbl.setText(get_random_fact())
        except Exception as e:
            logger.error("Échec de la mutation Oracle : %s", e)

    def _apply_premium_scrollbar_style(self, scroll_widget: QScrollArea) -> None:
        scroll_widget.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{
                border: none; background: transparent; width: 5px; margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme.border}; min-height: 20px; border-radius: 2.5px;
            }}
            QScrollBar::handle:vertical:hover {{ background: {self.theme.accent}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ border: none; background: none; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
        """)