"""
Asta Académie — Career Page v2.0 (PySide6)
==========================================
Interface d'orientation professionnelle et certifications post-UNASMOH.
Intègre un design de défilement immersif et une tolérance aux pannes de données.
"""

from __future__ import annotations

import logging
from typing import Dict, List

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
)

# Imports de l'écosystème Asta Académie
from ui.themes.theme_manager import Theme
from ui.components.widgets import SectionHeader, Card

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Données de secours (Fallback de résilience)
# ---------------------------------------------------------------------------
try:
    from utils.oracle_hub import CAREER_ADVICE
except ImportError:
    logger.warning("utils.oracle_hub introuvable ou CAREER_ADVICE manquant. Activation du fallback d'orientation.")
    CAREER_ADVICE = []

DEFAULT_CAREER_ADVICE: List[Dict[str, any]] = [
    {
        "titre": "🥇 Certifications Internationales Prioritaires",
        "items": [
            "Cisco CCNA (200-301) : La fondation absolue pour maîtriser l'infrastructure réseau et les protocoles de routage.",
            "CompTIA Security+ / CEH : Pour valider vos compétences pratiques en Hacking Éthique et SecDev.",
            "AWS Certified Cloud Practitioner : Indispensable pour l'architecture Cloud et la virtualisation moderne."
        ]
    },
    {
        "titre": "💼 Opportunités Freelance & Marché Local/Remote",
        "items": [
            "Plateformes Distribuées (Upwork, GitHub Jobs) : Valorisez vos projets en Python, C# et Go auprès de clients internationaux.",
            "Ingénierie Réseau & DevOps : Rejoignez les infrastructures critiques des institutions télécoms et bancaires en Haïti.",
            "Consultant en Cybersécurité : Accompagnez la transformation numérique et la sécurisation des données des PME locales."
        ]
    }
]


class CareerPage(QWidget):
    """
    Page d'orientation professionnelle et certifications de l'Asta Académie.
    Affiche dynamiquement les conseils de carrière avec un défilement ultra-fluide.
    """

    def __init__(self, theme: Theme, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.theme = theme
        self.setStyleSheet("background: transparent;")
        self._build()

    def _build(self) -> None:
        """Initialise la mise en page et applique le système de design."""
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Zone de défilement principale
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self._apply_premium_scrollbar_style(scroll)
        outer_layout.addWidget(scroll)

        # Conteneur des composants internes
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        scroll.setWidget(content_widget)

        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # En-tête de section unifié
        header = SectionHeader(
            "🎯 Carrière & Certifications", 
            "Stratégies post-UNASMOH : Certifications d'élite, opportunités de freelance et insertion en Haïti."
        )
        layout.addWidget(header)

        # Sélection de la source de données sécurisée
        data_source = CAREER_ADVICE if CAREER_ADVICE else DEFAULT_CAREER_ADVICE

        # Génération modulaire des cartes de carrière
        for idx, item in enumerate(data_source):
            card = Card()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(24, 20, 24, 24)
            card_layout.setSpacing(12)

            # Titre de la thématique
            titre_lbl = QLabel(item.get("titre", f"Option Conseil #{idx + 1}"))
            titre_lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
            titre_lbl.setStyleSheet(f"color: {self.theme.accent}; background: transparent;")
            card_layout.addWidget(titre_lbl)

            # Séparateur horizontal discret sous le titre
            divider = QFrame()
            divider.setFixedHeight(1)
            divider.setStyleSheet(f"background-color: {self.theme.border}; border: none;")
            card_layout.addWidget(divider)

            # Liste des recommandations
            for line in item.get("items", []):
                item_container = QWidget()
                item_container.setStyleSheet("background: transparent;")
                item_layout = QHBoxLayout(item_container)
                item_layout.setContentsMargins(0, 4, 0, 4)
                item_layout.setSpacing(12)

                # Badge vertical d'ancrage visuel (Cyber accent bar)
                indicator_bar = QFrame()
                indicator_bar.setFixedWidth(3)
                indicator_bar.setFixedHeight(22)
                indicator_bar.setStyleSheet(f"background-color: {self.theme.accent}; border-radius: 1.5px;")
                item_layout.addWidget(indicator_bar, 0, Qt.AlignTop)

                # Libellé textuel informatif
                desc_lbl = QLabel(line)
                desc_lbl.setFont(QFont("Segoe UI", 11))
                desc_lbl.setStyleSheet(f"color: {self.theme.text}; background: transparent;")
                desc_lbl.setWordWrap(True)
                item_layout.addWidget(desc_lbl, 1)

                card_layout.addWidget(item_container)

            layout.addWidget(card)

        # Ressort de rappel pour maintenir le tout parfaitement aligné vers le haut
        layout.addStretch()

    def _apply_premium_scrollbar_style(self, scroll_area: QScrollArea) -> None:
        """Injecte une feuille de style CSS avancée pour masquer et styliser la Scrollbar."""
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 6px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme.border};
                min-height: 30px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme.accent};
            """ + """
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)