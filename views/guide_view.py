"""
Asta Académie — Guide Page v2.5 (PySide6)
=========================================
Documentation technique unifiée et guide opératoire du système.
Intégration d'iconographie vectorielle pure (SVG) et terminologie industrielle.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Tuple, Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
)

from ui.themes.theme_manager import Theme
from ui.components.widgets import SectionHeader, Card, add_shadow
from utils.svg_manager import SVGManager

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Dictionnaire de secours : Icônes SVG Vectorielles (Design Épuré & Cyber)
# ---------------------------------------------------------------------------
FALLBACK_SVGS: Dict[str, str] = {
    "dashboard": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>',
    "ide": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="14" y1="4" x2="10" y2="20"/></svg>',
    "utilities": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    "security": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "analytics": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"/></svg>',
    "config": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'
}

def _get_vector_icon(name: str, color: str, size: int) -> QIcon:
    """Instancie l'icône vectorielle via SVGManager avec interception et reconstruction dynamique inline si absent."""
    icon = SVGManager.get_icon(name, color=color, size=size)
    if not icon.isNull():
        return icon
    
    fallback_template = FALLBACK_SVGS.get(name)
    if fallback_template:
        svg_data = fallback_template.format(color=color).encode('utf-8')
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
# Composant de Rendu : Guide de Documentation Système (Production-Ready)
# ===========================================================================
class GuidePage(QWidget):
    """
    Vue de référence et manuel opératoire de la plateforme Asta Académie.
    Structure de cartes vectorielles dynamiques et typage statique strict.
    """
    def __init__(self, theme: Theme, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.theme: Theme = theme
        self.setStyleSheet("background: transparent;")
        self._build()

    def _build(self) -> None:
        # Zone de défilement principale (ScrollArea unifiée)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self._apply_premium_scrollbar_style(scroll)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        scroll.setWidget(content_widget)
        
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        # En-tête de section
        header = SectionHeader(
            "Manuel d'Utilisation Système", 
            "Spécifications fonctionnelles, protocoles d'exploitation et guide de déploiement des outils d'Asta Académie."
        )
        layout.addWidget(header)

        # Matrice de données documentaires (Textes mis à jour au standard professionnel)
        guides: List[Tuple[str, str, str, str]] = [
            (
                "dashboard",
                "Centre de Pilotage & Métriques (Dashboard)", 
                self.theme.accent,
                "Console centrale d'analyse comportementale et de suivi d'activité :\n"
                "• Synthèse en temps réel de l'indice d'expérience (XP) et statut de qualification du profil.\n"
                "• Index d'assiduité numérique (Série Active) calculé par incrémentation journalière stricte.\n"
                "• Registre d'authentification des distinctions (Badges) et des objectifs opérationnels validés.\n"
                "• Représentation cartographique de la courbe de progression hebdomadaire.\n"
                "• Flux de métaphores heuristiques extrait dynamiquement du cluster synaptique de l'Oracle."
            ),
            (
                "ide",
                "Espace de R&D Intégré (SpaceCode IDE)", 
                self.theme.accent,
                "Environnement d'ingénierie logicielle et d'édition de scripts Python autonomes :\n"
                "• Interfaçage d'écriture de code source avec isolation d'exécution en tâche de fond (Background Worker).\n"
                "• Analyseur lexical et moteur de coloration syntaxique avancée pour une lisibilité optimale.\n"
                "• Arborescence de fichiers et persistance des entrées/sorties pour l'implémentation de vos algorithmes.\n"
                "• Terminal d'exécution virtualisé capturant les flux d'E/S standards (stdout/stderr) et les traces de débogage."
            ),
            (
                "utilities",
                "Suite d'Utilitaires Systèmes & Réseaux", 
                self.theme.accent,
                "Arsenal d'outils analytiques critiques optimisés pour les architectures informatiques :\n"
                "• Shell d'interfaçage : Passerelle d'exécution pour les commandes système fondamentales.\n"
                "• Convertisseur de Bases : Traduction algorithmique instantanée (Décimal, Binaire, Hexadécimal).\n"
                "• Segmentateur Réseau : Calculateur CIDR d'adressage logique et d'analyse de masques de sous-réseaux.\n"
                "• Référentiel Algorithmique : Tables de logique booléenne et modèles théoriques de complexité (Big O Notation).\n"
                "• Générateur de Canevas : Injection de structures algorithmiques types complexes multi-langages."
            ),
            (
                "security",
                "Laboratoire de Sécurité Offensive & Cyberdéfense", 
                self.theme.danger,
                "Zone d'analyse d'élite accessible exclusivement via l'injection d'un jeton clé cryptographique valide :\n"
                "• Modules d'apprentissage dédiés à la sécurité des systèmes d'information, vecteurs d'attaque et remédiation.\n"
                "• Liseuse asynchrone optimisée pour l'analyse des documentations techniques au format Markdown.\n"
                "• Chiffrement de bout en bout : Déchiffrement à la volée en mémoire volatile (RAM) pour interdire toute persistance suspecte."
            ),
            (
                "analytics",
                "Module d'Évaluation & Traçabilité Académique", 
                self.theme.accent,
                "Interface de calcul d'indicateurs de performance et d'extrapolation des résultats académiques :\n"
                "• Saisie structurée des évaluations intermédiaires (Sessions Intra sur 40) et terminales (Sessions Finales sur 60).\n"
                "• Calcul de pondération automatisé, modélisation de la moyenne générale et attribution des mentions officielles.\n"
                "• Persistance décentralisée : Synchronisation chiffrée avec le cluster central via des requêtes d'API asynchrones (Go/PostgreSQL)."
            ),
            (
                "config",
                "Console de Configuration Globale", 
                self.theme.accent,
                "Paramétrage avancé de la matrice applicative et contrôle de l'environnement graphique :\n"
                "• Gestionnaire de thèmes à haut contraste pour l'optimisation visuelle en environnement basse luminosité (Cyber-sécurité).\n"
                "• Module de localisation linguistique prenant en charge le Français, le Kreyòl et l'English.\n"
                "• Algorithme de mise à l'échelle d'interface (Zoom dynamique) pour affichages haute densité (High-DPI).\n"
                "• Registre de conformité légale et validation des accords de licence de l'écosystème."
            )
        ]

        # Construction dynamique de l'interface graphique
        for svg_name, title, color, desc in guides:
            card = Card()
            add_shadow(card, blur=12, y=2)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(12)
            
            # En-tête de la carte (Icône SVG + Titre)
            title_layout = QHBoxLayout()
            title_layout.setContentsMargins(0, 0, 0, 0)
            title_layout.setSpacing(10)
            
            icon_lbl = QLabel()
            vector_icon = _get_vector_icon(svg_name, color=color, size=24)
            if not vector_icon.isNull():
                icon_lbl.setPixmap(vector_icon.pixmap(24, 24))
            icon_lbl.setStyleSheet("border: none; background: transparent;")
            title_layout.addWidget(icon_lbl)
            
            t_lbl = QLabel(title)
            t_lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
            t_lbl.setStyleSheet(f"color: {color}; border: none; background: transparent;")
            title_layout.addWidget(t_lbl)
            title_layout.addStretch()
            
            card_layout.addLayout(title_layout)
            
            # Corps descriptif
            d_lbl = QLabel(desc)
            d_lbl.setFont(QFont("Segoe UI", 12))
            d_lbl.setStyleSheet(f"color: {self.theme.text}; border: none; background: transparent; line-height: 1.4;")
            d_lbl.setWordWrap(True)
            card_layout.addWidget(d_lbl)
            
            layout.addWidget(card)
            
        layout.addStretch()

    def _apply_premium_scrollbar_style(self, scroll_widget: QScrollArea) -> None:
        """Injecte les règles CSS d'affichage de la scrollbar cyber-invisible de la plateforme."""
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