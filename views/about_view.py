"""
Asta Académie — About Page (PySide6)
=====================================
Crédits, manifeste et informations sur l'application avec animations fluides.
"""

from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, 
    QGraphicsOpacityEffect, QSizePolicy
)

# Imports de l'écosystème Asta Académie
from ui.themes.theme_manager import Theme
from ui.components.widgets import Card, SectionHeader
from core.config import VERSION, PROMO, DEV_REAL, WHATSAPP

logger = logging.getLogger(__name__)


class AboutPage(QWidget):
    """
    Vue informative présentant l'identité d'Asta Académie.
    Intègre des transitions douces et un agencement adaptatif (responsive).
    """

    def __init__(self, theme: Theme, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.theme = theme
        
        # Configuration de base de la vue
        self.setStyleSheet("background: transparent;")
        
        # Initialisation de l'interface et des transitions
        self._build_ui()
        self._animate_entrance()

    def _build_ui(self) -> None:
        """Configure l'agencement principal et assemble les composants."""
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setAlignment(Qt.AlignCenter)

        # Conteneur central (Card héritée du Design System)
        self.card = Card()
        self.card.setMinimumWidth(450)
        self.card.setMaximumWidth(620)
        self.card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(24)
        card_layout.setAlignment(Qt.AlignCenter)

        # Assemblage des sections de la carte
        self._build_header(card_layout)
        self._build_divider(card_layout)
        self._build_manifesto(card_layout)
        self._build_credits_box(card_layout)
        self._build_footer(card_layout)

        root_layout.addWidget(self.card)

    def _build_header(self, layout: QVBoxLayout) -> None:
        """Génère la section d'en-tête avec le titre et la version."""
        title = QLabel("Asta Académie")
        title.setFont(QFont("Segoe UI", 30, QFont.Bold))
        title.setStyleSheet(f"color: {self.theme.accent}; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        version = QLabel(f"Version {VERSION}")
        version.setFont(QFont("Segoe UI", 10, QFont.Medium))
        version.setStyleSheet(f"color: {self.theme.text_secondary}; background: transparent;")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

    def _build_divider(self, layout: QVBoxLayout) -> None:
        """Ajoute une ligne de séparation subtile."""
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet(f"background: {self.theme.border}; border: none; max-height: 1px;")
        layout.addWidget(div)

    def _build_manifesto(self, layout: QVBoxLayout) -> None:
        """Affiche le texte de présentation de la plateforme."""
        desc = QLabel(
            "Plateforme éducative d'excellence conçue pour les étudiants de l'UNASMOH.\n\n"
            "Une interface moderne, un apprentissage gamifié, et des outils puissants "
            "pour propulser votre carrière en informatique et réseaux."
        )
        desc.setFont(QFont("Segoe UI", 11))
        desc.setStyleSheet(f"color: {self.theme.text}; background: transparent; line-height: 140%;")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

    def _build_credits_box(self, layout: QVBoxLayout) -> None:
        """Construit le bloc technique contenant les signatures des développeurs."""
        credits_box = QFrame()
        credits_box.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.bg}; 
                border: 1px solid {self.theme.border};
                border-radius: 8px; 
            }}
        """)
        cb_layout = QVBoxLayout(credits_box)
        cb_layout.setContentsMargins(16, 16, 16, 16)
        cb_layout.setSpacing(6)
        
        dev_lbl = QLabel(f"Développeur Principal : {DEV_REAL} (Lucky Luke)")
        dev_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        dev_lbl.setStyleSheet(f"color: {self.theme.accent}; background: transparent;")
        dev_lbl.setAlignment(Qt.AlignCenter)
        cb_layout.addWidget(dev_lbl)
        
        promo_lbl = QLabel(f"Promotion : {PROMO}  ·  Support : {WHATSAPP}")
        promo_lbl.setFont(QFont("Segoe UI", 9.5))
        promo_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; background: transparent;")
        promo_lbl.setAlignment(Qt.AlignCenter)
        cb_layout.addWidget(promo_lbl)

        layout.addWidget(credits_box)

    def _build_footer(self, layout: QVBoxLayout) -> None:
        """Génère la signature culturelle de fin de page."""
        footer = QLabel("🇭🇹 Fait en Haïti, pour l'excellence haïtienne 🇭🇹")
        footer.setFont(QFont("Segoe UI", 11, QFont.Bold))
        footer.setStyleSheet(f"color: {self.theme.success}; background: transparent;")
        footer.setAlignment(Qt.AlignCenter)
        
        # Ajout d'un léger effet de transparence sur le footer pour le rendre plus discret
        opacity_effect = QGraphicsOpacityEffect(self)
        opacity_effect.setOpacity(0.85)
        footer.setGraphicsEffect(opacity_effect)
        
        layout.addWidget(footer)

    def _animate_entrance(self) -> None:
        """Déclenche une transition d'opacité fluide lors du chargement de la vue."""
        opacity_effect = QGraphicsOpacityEffect(self.card)
        self.card.setGraphicsEffect(opacity_effect)
        
        self._anim = QPropertyAnimation(opacity_effect, b"opacity", self)
        self._anim.setDuration(400)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.OutQuad)
        self._anim.start()