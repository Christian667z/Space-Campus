"""
Asta Académie — Legal Page v2.5 (PySide6)
==========================================
Accords légaux, vie privée et conditions d'utilisation.

Améliorations v2.5 (CodeForge AI Max Boost) :
  - 100% Vectoriel : Éradication totale des émojis textuels au profit du SVGManager.
  - Découplage UI/UX : Les blocs d'information utilisent des QGridLayouts pour un alignement pixel-perfect.
  - Architecture Propre : Unification de la logique de mise à jour d'état (State Management).
  - Robustesse UX : Isolation des signaux (blockSignals) lors des modifications programmatiques.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap, QIcon, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QCheckBox, QFileDialog, QFrame, QHBoxLayout,
    QLabel, QMessageBox, QPushButton,
    QScrollArea, QVBoxLayout, QWidget, QGridLayout
)

from ui.components.widgets import Card, SectionHeader, add_shadow
from ui.themes.theme_manager import Theme
from utils.svg_manager import SVGManager

# Importation centralisée des configurations globales de l'application
from core.config import (
    APP_NAME, DEV_NAME, WHATSAPP, UNIVERSITE, EMAIL, PROFILE_FILE, save_json
)

logger = logging.getLogger(__name__)

# Version locale spécifique à la structure actuelle des CGU
CGU_VERSION = "2.0.0"

# ---------------------------------------------------------------------------
# Dictionnaire de secours : Icônes SVG Inline (Résilience absolue)
# ---------------------------------------------------------------------------
FALLBACK_SVGS: Dict[str, str] = {
    "shield-alert": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "clipboard": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>',
    "copyright": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M15 9.354a4 4 0 1 0 0 5.292"/></svg>',
    "database": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
    "smartphone": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>',
    "check-circle": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    "alert-triangle": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "pen-tool": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>',
    "user": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    "file-text": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
    "refresh-cw": '<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>'
}

def _get_vector_icon(name: str, color: str, size: int) -> QIcon:
    """Génère une icône QIcon via SVGManager ou via template de secours inline."""
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
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            return QIcon(pixmap)
            
    return QIcon()

# ---------------------------------------------------------------------------
# Contenu légal
# ---------------------------------------------------------------------------

LEGAL_SECTIONS = [
    {
        "id":       "cybersec",
        "icon":     "shield-alert",
        "title":    "Avertissement Légal : Cyber-Sécurité",
        "color":    "danger",
        "points": [
            "Vous acceptez d'utiliser les outils et connaissances acquis UNIQUEMENT sur des systèmes pour lesquels vous disposez d'une autorisation explicite écrite.",
            "L'accès non autorisé à des systèmes informatiques est un crime punissable par la loi haïtienne et internationale.",
            "Les développeurs d'Asta Académie déclinent toute responsabilité quant à une utilisation malveillante, non éthique ou illégale de ce logiciel.",
            "En activant le module Hacking, votre machine (HWID) et votre identité sont liées à des clés de licence traçables par l'administration.",
            "Tout abus signalé entraînera la révocation immédiate de la licence et pourra faire l'objet de poursuites judiciaires.",
            "Le module DevSecurity est exclusivement destiné à l'apprentissage du Hacking Éthique (Ethical Hacking) dans un cadre académique.",
        ],
    },
    {
        "id":       "privacy",
        "icon":     "lock",
        "title":    "Politique de Vie Privée & Données",
        "color":    "accent",
        "points": [
            "Télémétrie : Asta Académie collecte des statistiques d'utilisation anonymisées (logs d'audit, rapports d'erreurs) pour améliorer la stabilité.",
            "Stockage local : Vos données personnelles (nom, notes, profil) sont stockées exclusivement dans la base de données SQLite sur votre machine.",
            "Kill Switch : En cas d'abus ou comportement suspect, l'Administrateur peut révoquer votre accès à distance via le mécanisme de sécurité intégré.",
            "Chiffrement : Asta Académie utilise des protocoles de chiffrement standards pour stocker vos clés de licence de façon sécurisée.",
            "Aucune donnée personnelle n'est vendue ou transmise à des tiers sans votre consentement explicite.",
            "Vous avez le droit de demander la suppression complète de vos données en contactant l'administrateur.",
        ],
    },
    {
        "id":       "terms",
        "icon":     "clipboard",
        "title":    "Conditions Générales d'Utilisation",
        "color":    "text",
        "points": [
            f"{APP_NAME} est un logiciel éducatif développé pour les étudiants en Sciences Informatiques de {UNIVERSITE}.",
            "La licence d'utilisation est personnelle, non transférable et liée à votre machine via le HWID.",
            "Toute tentative de contournement du système de licence ou de rétro-ingénierie du logiciel est strictement interdite.",
            "L'application peut être mise à jour à tout moment. Les nouvelles versions peuvent modifier les présentes conditions.",
            "L'utilisation continue de l'application après une mise à jour implique l'acceptation des nouvelles conditions.",
            f"{APP_NAME} est fourni « EN L'ÉTAT » sans garantie d'aucune sorte, explicite ou implicite.",
        ],
    },
    {
        "id":       "ip",
        "icon":     "copyright",
        "title":    "Propriété Intellectuelle & Copyright",
        "color":    "text",
        "points": [
            f"© 2024-2028 {DEV_NAME} — Tous droits réservés.",
            f"Le code source, l'interface, le contenu éducatif et les ressources d'Asta Académie sont la propriété exclusive de {DEV_NAME}.",
            "Toute reproduction, distribution, modification ou exploitation commerciale sans autorisation écrite est interdite.",
            "Le contenu pédagogique (cours, exercices, quiz) est protégé par les droits d'auteur haïtiens et internationaux.",
            "Les logos, noms et marques associés à Asta Académie sont des marques déposées de Space | Asta Dev.",
            "Les contributions tierces ou bibliothèques open-source utilisées restent soumises à leurs licences respectives.",
        ],
    },
    {
        "id":       "retention",
        "icon":     "database",
        "title":    "Rétention & Sécurité des Données",
        "color":    "text",
        "points": [
            "Les données d'utilisation (logs) sont conservées localement pendant une durée maximale de 90 jours.",
            "Les données de profil et de notes sont conservées tant que vous utilisez l'application.",
            "À la désinstallation, vos données locales peuvent être supprimées manuellement depuis le dossier de données.",
            "Les clés de licence sont stockées en dehors du profil pour garantir la persistance entre les mises à jour.",
            "En cas de réinitialisation, toutes les données locales sont effacées de façon irréversible.",
            "Aucune sauvegarde automatique n'est effectuée sur des serveurs externes sans votre accord explicite.",
        ],
    },
    {
        "id":       "contact",
        "icon":     "smartphone",
        "title":    "Contact & Réclamations",
        "color":    "success",
        "points": [
            f"Pour toute question légale, contactez {DEV_NAME} sur WhatsApp : {WHATSAPP}.",
            "Les réclamations doivent être soumises par écrit et seront traitées dans un délai de 7 jours ouvrés.",
            "Pour signaler un abus ou une violation de sécurité, contactez immédiatement l'administration.",
            f"Support technique disponible via WhatsApp : {WHATSAPP} (Lundi–Vendredi, 8h–18h).",
            "Toute décision de l'administration concernant l'accès au logiciel est définitive et sans appel.",
            f"{APP_NAME} est développé en Haïti, pour les étudiants haïtiens 🇭🇹.",
        ],
    },
]

def generate_raw_cgu_text() -> str:
    """Génère dynamiquement le flux textuel brut pour l'exportation (sans balises SVG)."""
    lines = [
        "=" * 60,
        f"{APP_NAME} — Conditions d'Utilisation & Politique de Vie Privée",
        f"Version {CGU_VERSION} — {datetime.now().strftime('%Y')}",
        "=" * 60,
        ""
    ]
    for s in LEGAL_SECTIONS:
        # On supprime l'icône dans l'export texte pur
        lines.append(f"\n[ {s['title'].upper()} ]\n{'─' * 50}\n")
        lines.extend(f"  {i+1}. {pt}" for i, pt in enumerate(s["points"]))
    
    lines.extend([
        "",
        "=" * 60,
        f"© 2024-2028 {DEV_NAME} — Tous droits réservés.",
        f"Contact : {WHATSAPP}",
    ])
    return "\n".join(lines)


# ===========================================================================
# Composant : Carte légale
# ===========================================================================

class LegalSection(QFrame):
    """Carte légale avec titre coloré, icône vectorielle et liste de points numérotés."""

    def __init__(self, section: dict, theme: Theme, parent=None) -> None:
        super().__init__(parent)
        color_key = section.get("color", "text")
        color = getattr(theme, color_key, theme.text)

        self.setStyleSheet(f"""
            QFrame {{
                background: {theme.card};
                border: 1px solid {theme.border};
                border-left: 4px solid {color};
                border-radius: 10px;
            }}
        """)
        add_shadow(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        # Titre avec SVG
        title_row = QHBoxLayout()
        icon_lbl = QLabel()
        vector_icon = _get_vector_icon(section["icon"], color=color, size=24)
        if not vector_icon.isNull():
            icon_lbl.setPixmap(vector_icon.pixmap(24, 24))
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        title_row.addWidget(icon_lbl)

        title_lbl = QLabel(self.tr(section["title"]))
        title_lbl.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {color}; border: none; background: transparent;")
        title_row.addWidget(title_lbl, 1)
        layout.addLayout(title_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background: {color}44; border: none; max-height: 1px;")
        layout.addWidget(sep)

        # Points
        for i, point in enumerate(section["points"], start=1):
            row = QHBoxLayout()
            row.setSpacing(8)

            num = QLabel(f"{i}.")
            num.setFixedWidth(22)
            num.setFont(QFont("Segoe UI", 11, QFont.Bold))
            num.setStyleSheet(f"color: {color}; border: none; background: transparent;")
            row.addWidget(num)

            txt = QLabel(self.tr(point))
            txt.setFont(QFont("Segoe UI", 11))
            txt.setWordWrap(True)
            txt.setStyleSheet(f"color: {theme.text}; border: none; background: transparent;")
            row.addWidget(txt, 1)

            layout.addLayout(row)


# ===========================================================================
# Page principale
# ===========================================================================

class LegalPage(QWidget):
    """
    Page des conditions d'utilisation et politique de vie privée.
    Architecture 100% vectorielle.
    """
    legal_status_changed = Signal(bool)

    def __init__(self, profile: dict, theme: Theme, parent=None) -> None:
        super().__init__(parent)
        self.profile = profile
        self.theme = theme
        self.setStyleSheet("background: transparent;")
        self._build_ui()

    def _build_ui(self) -> None:
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self._apply_premium_scrollbar_style(scroll)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 32)
        layout.setSpacing(16)

        header_title = self.tr("Conditions d'Utilisation & Vie Privée")
        header_sub = self.tr("Accords légaux d'Asta Académie · Version %1 · Lisez attentivement avant d'utiliser toutes les fonctionnalités.").arg(CGU_VERSION)
        
        # En-tête manuel avec icône vectorielle pour remplacer SectionHeader basique
        header_layout = QHBoxLayout()
        h_icon = QLabel()
        h_vec = _get_vector_icon("shield-alert", color=self.theme.accent, size=32)
        if not h_vec.isNull():
            h_icon.setPixmap(h_vec.pixmap(32, 32))
        header_layout.addWidget(h_icon)
        
        h_text_lay = QVBoxLayout()
        h_title = QLabel(header_title)
        h_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        h_title.setStyleSheet(f"color: {self.theme.text};")
        h_sub = QLabel(header_sub)
        h_sub.setFont(QFont("Segoe UI", 11))
        h_sub.setStyleSheet(f"color: {self.theme.text_secondary};")
        h_text_lay.addWidget(h_title)
        h_text_lay.addWidget(h_sub)
        header_layout.addLayout(h_text_lay, 1)
        
        layout.addLayout(header_layout)

        # Bannière de statut
        self._status_banner = self._build_status_banner()
        layout.addWidget(self._status_banner)

        for section in LEGAL_SECTIONS:
            layout.addWidget(LegalSection(section, self.theme))

        layout.addWidget(self._build_acceptance_zone())
        layout.addStretch()

    def _build_status_banner(self) -> QFrame:
        banner = QFrame()
        b_layout = QHBoxLayout(banner)
        b_layout.setContentsMargins(16, 12, 16, 12)
        b_layout.setSpacing(12)

        self._status_icon = QLabel()
        b_layout.addWidget(self._status_icon)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        self._status_title = QLabel()
        self._status_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        text_col.addWidget(self._status_title)

        self._status_sub = QLabel()
        self._status_sub.setFont(QFont("Segoe UI", 10))
        text_col.addWidget(self._status_sub)
        b_layout.addLayout(text_col, 1)

        self._refresh_status_banner(banner)
        return banner

    def _build_acceptance_zone(self) -> QFrame:
        zone = QFrame()
        zone.setStyleSheet(f"background: {self.theme.card}; border: 1px solid {self.theme.border}; border-radius: 12px;")
        add_shadow(zone)
        
        layout = QVBoxLayout(zone)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Titre de zone SVG
        t_row = QHBoxLayout()
        t_icon = QLabel()
        t_vec = _get_vector_icon("pen-tool", color=self.theme.text, size=24)
        if not t_vec.isNull():
            t_icon.setPixmap(t_vec.pixmap(24, 24))
        t_row.addWidget(t_icon)
        
        acc_title = QLabel(self.tr("Signature & Accord"))
        acc_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        acc_title.setStyleSheet(f"color: {self.theme.text}; border: none; background: transparent;")
        t_row.addWidget(acc_title, 1)
        layout.addLayout(t_row)

        # Grille d'information utilisateur vectorielle
        nom = self.profile.get("nom", self.tr("Utilisateur inconnu"))
        grid = QGridLayout()
        grid.setSpacing(8)
        
        infos = [
            ("user", self.tr("Utilisateur identifié"), nom),
            ("calendar", self.tr("Date d'aujourd'hui"), datetime.now().strftime('%d/%m/%Y')),
            ("file-text", self.tr("Version des CGU"), CGU_VERSION)
        ]
        
        for row, (icn_name, label_txt, val_txt) in enumerate(infos):
            icn_lbl = QLabel()
            vec = _get_vector_icon(icn_name, color=self.theme.text_secondary, size=16)
            if not vec.isNull():
                icn_lbl.setPixmap(vec.pixmap(16, 16))
            grid.addWidget(icn_lbl, row, 0, Qt.AlignRight | Qt.AlignVCenter)
            
            txt_lbl = QLabel(f"{label_txt} : <span style='color:{self.theme.text};'>{val_txt}</span>")
            txt_lbl.setFont(QFont("Segoe UI", 11))
            txt_lbl.setStyleSheet(f"color: {self.theme.text_secondary};")
            grid.addWidget(txt_lbl, row, 1, Qt.AlignLeft | Qt.AlignVCenter)
            
        layout.addLayout(grid)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background: {self.theme.border}; border: none; max-height: 1px;")
        layout.addWidget(sep)

        # Checkbox
        self._chk = QCheckBox(self.tr(
            "Je certifie avoir lu, compris et accepté l'intégralité des conditions d'utilisation\n"
            "et de la politique de vie privée. Je m'engage à agir de manière éthique et légale."
        ))
        self._chk.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self._chk.setStyleSheet(f"""
            QCheckBox {{ color: {self.theme.warning}; spacing: 10px; border: none; background: transparent; }}
            QCheckBox::indicator {{ width: 20px; height: 20px; border: 2px solid {self.theme.warning}; border-radius: 4px; }}
            QCheckBox::indicator:checked {{ background: {self.theme.warning}; }}
        """)
        self._chk.setChecked(self.profile.get("legal_accepted", False))
        self._chk.toggled.connect(self._on_toggle)
        layout.addWidget(self._chk)

        # Avertissement
        warn_row = QHBoxLayout()
        w_icon = QLabel()
        w_vec = _get_vector_icon("alert-triangle", color=self.theme.danger, size=18)
        if not w_vec.isNull():
            w_icon.setPixmap(w_vec.pixmap(18, 18))
        warn_row.addWidget(w_icon, 0, Qt.AlignTop)
        
        self._warn = QLabel(self.tr(
            "Vous devez accepter ces conditions pour accéder à toutes les fonctionnalités.\n"
            "Le module DevSecurity et certains outils restent verrouillés sans cet accord."
        ))
        self._warn.setFont(QFont("Segoe UI", 10, italic=True))
        self._warn.setWordWrap(True)
        self._warn.setStyleSheet(f"color: {self.theme.danger}; border: none; background: transparent;")
        warn_row.addWidget(self._warn, 1)
        
        self._warn_widget = QWidget()
        self._warn_widget.setLayout(warn_row)
        self._warn_widget.setVisible(not self._chk.isChecked())
        layout.addWidget(self._warn_widget)

        # Boutons avec icônes
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        export_btn = QPushButton(self.tr(" Exporter les CGU"))
        export_btn.setIcon(_get_vector_icon("clipboard", color=self.theme.text, size=16))
        export_btn.setProperty("class", "secondary")
        export_btn.setFixedHeight(34)
        export_btn.clicked.connect(self._export_cgu)
        btn_row.addWidget(export_btn)

        btn_row.addStretch()

        self._revoke_btn = QPushButton(self.tr(" Révoquer mon accord"))
        self._revoke_btn.setIcon(_get_vector_icon("refresh-cw", color="#ffffff", size=16))
        self._revoke_btn.setProperty("class", "danger_btn")
        self._revoke_btn.setFixedHeight(34)
        self._revoke_btn.setEnabled(self.profile.get("legal_accepted", False))
        self._revoke_btn.clicked.connect(self._revoke_agreement)
        btn_row.addWidget(self._revoke_btn)

        layout.addLayout(btn_row)
        return zone

    # -----------------------------------------------------------------------
    # Logique métier & State Management
    # -----------------------------------------------------------------------

    def _refresh_status_banner(self, target_banner: Optional[QFrame] = None) -> None:
        banner = target_banner or self._status_banner
        accepted = self.profile.get("legal_accepted", False)
        ts_raw = self.profile.get("legal_accepted_at", "")
        cgu_ver = self.profile.get("legal_cgu_version", "")
        nom = self.profile.get("nom", "Utilisateur")

        color = "#27AE60" if accepted else "#E74C3C"
        banner.setStyleSheet(f"QFrame {{ background: {color}18; border: 1px solid {color}55; border-radius: 10px; }}")

        if accepted and ts_raw:
            try:
                ts = datetime.fromisoformat(ts_raw).strftime("%d/%m/%Y à %H:%M")
            except Exception:
                ts = ts_raw
                
            icn = _get_vector_icon("check-circle", color="#27AE60", size=28)
            if not icn.isNull(): self._status_icon.setPixmap(icn.pixmap(28, 28))
            
            self._status_title.setText(self.tr("Conditions acceptées par %1").arg(nom))
            self._status_title.setStyleSheet("color: #27AE60; border: none; background: transparent;")
            self._status_sub.setText(self.tr("Le %1 · CGU v%2").arg(ts).arg(cgu_ver or CGU_VERSION))
            self._status_sub.setStyleSheet("color: #27AE60; border: none; background: transparent;")
        else:
            icn = _get_vector_icon("alert-triangle", color=self.theme.danger, size=28)
            if not icn.isNull(): self._status_icon.setPixmap(icn.pixmap(28, 28))
            
            self._status_title.setText(self.tr("Conditions non acceptées"))
            self._status_title.setStyleSheet(f"color: {self.theme.danger}; border: none; background: transparent;")
            self._status_sub.setText(self.tr("Certaines fonctionnalités (module Hacking, DevSecurity) sont restreintes."))
            self._status_sub.setStyleSheet(f"color: {self.theme.danger}; border: none; background: transparent;")

    def _set_agreement_state(self, accepted: bool) -> None:
        self.profile["legal_accepted"] = accepted
        if accepted:
            ts = datetime.now().isoformat()
            self.profile["legal_accepted_at"] = ts
            self.profile["legal_cgu_version"] = CGU_VERSION
        else:
            self.profile.pop("legal_accepted_at", None)
            self.profile.pop("legal_cgu_version", None)
        
        self._save_profile()
        
        self._chk.blockSignals(True)
        self._chk.setChecked(accepted)
        self._chk.blockSignals(False)
        
        self._warn_widget.setVisible(not accepted)
        self._revoke_btn.setEnabled(accepted)
        self._refresh_status_banner()
        self.legal_status_changed.emit(accepted)

    def _on_toggle(self, checked: bool) -> None:
        if checked:
            self._set_agreement_state(True)
            msg = self.tr("Merci %1 !\n\nVotre accord a été enregistré le %2.\nVous avez accès à toutes les fonctionnalités.")
            QMessageBox.information(self, self.tr("Accord enregistré"), msg.arg(self.profile.get('nom', '')).arg(datetime.now().strftime('%d/%m/%Y à %H:%M')))
        else:
            self._set_agreement_state(False)

    def _revoke_agreement(self) -> None:
        reply = QMessageBox.question(self, self.tr("Révoquer l'accord"), self.tr("Êtes-vous sûr de vouloir révoquer votre accord ?\n\nCela désactivera l'accès aux modules avancés."), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._set_agreement_state(False)

    def _export_cgu(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, self.tr("Exporter"), f"CGU_AstaAcademie_v{CGU_VERSION}.txt", self.tr("Fichier texte (*.txt)"))
        if not path: return
            
        try:
            signature = ""
            if self.profile.get("legal_accepted"):
                ts = self.profile.get("legal_accepted_at", "")
                try: ts_fmt = datetime.fromisoformat(ts).strftime("%d/%m/%Y à %H:%M")
                except: ts_fmt = ts
                signature = f"\n\n{'='*60}\nSIGNATURE NUMÉRIQUE\n{'─'*60}\nNom        : {self.profile.get('nom', '')}\nDate       : {ts_fmt}\nCGU Version: {CGU_VERSION}\nStatut     : ACCEPTÉ\n{'='*60}\n"
                
            Path(path).write_text(generate_raw_cgu_text() + signature, encoding="utf-8")
            QMessageBox.information(self, self.tr("Export réussi"), self.tr("Exporté vers :\n%1").arg(path))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erreur"), self.tr("Impossible d'exporter : %1").arg(str(e)))

    def _save_profile(self) -> None:
        try: save_json(PROFILE_FILE, self.profile)
        except Exception as e: logger.error("Erreur sauvegarde : %s", e)

    def check_cgu_version(self) -> bool:
        if not self.profile.get("legal_accepted", False): return False
        if self.profile.get("legal_cgu_version", "") != CGU_VERSION:
            self._set_agreement_state(False)
            return False
        return True

    def _apply_premium_scrollbar_style(self, scroll_widget: QScrollArea) -> None:
        scroll_widget.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{ border: none; background: transparent; width: 5px; margin: 0px; }}
            QScrollBar::handle:vertical {{ background: {self.theme.border}; min-height: 20px; border-radius: 2.5px; }}
            QScrollBar::handle:vertical:hover {{ background: {self.theme.accent}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ border: none; background: none; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
        """)