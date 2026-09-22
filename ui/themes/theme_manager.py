"""
Asta Académie — Système de Thèmes Qt Moderne
Design System cohérent avec variables CSS-like
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class Theme:
    name: str
    bg: str
    bg_alt: str
    sidebar: str
    card: str
    card_hover: str
    border: str
    accent: str
    accent2: str
    accent_hover: str
    text: str
    text_secondary: str
    text_disabled: str
    success: str
    warning: str
    danger: str
    info: str
    # Fonts
    font_primary: str = "Segoe UI"
    font_mono: str = "Consolas"
    # Radius
    radius_sm: int = 6
    radius_md: int = 10
    radius_lg: int = 16
    # Spacing
    spacing_xs: int = 4
    spacing_sm: int = 8
    spacing_md: int = 16
    spacing_lg: int = 24
    spacing_xl: int = 32


THEMES: Dict[str, Theme] = {
    "noir_vert": Theme(
        name="Noir & Vert",
        bg="#0f172a",
        bg_alt="#080e1c",
        sidebar="#1e293b",
        card="#1a2235",
        card_hover="#212f45",
        border="#2d3f55",
        accent="#10b981",
        accent2="#0ea5e9",
        accent_hover="#0d9f70",
        text="#f1f5f9",
        text_secondary="#94a3b8",
        text_disabled="#475569",
        success="#10b981",
        warning="#f59e0b",
        danger="#ef4444",
        info="#0ea5e9",
    ),
    "bleu_nuit": Theme(
        name="Bleu Nuit",
        bg="#030712",
        bg_alt="#020510",
        sidebar="#0c1628",
        card="#0e1e3a",
        card_hover="#132548",
        border="#1e3a5f",
        accent="#60a5fa",
        accent2="#a78bfa",
        accent_hover="#3b82f6",
        text="#e2e8f0",
        text_secondary="#7099c0",
        text_disabled="#334e68",
        success="#34d399",
        warning="#fbbf24",
        danger="#f87171",
        info="#60a5fa",
    ),
    "violet_cyber": Theme(
        name="Violet Cyber",
        bg="#0a0014",
        bg_alt="#060009",
        sidebar="#13002a",
        card="#1a003a",
        card_hover="#220050",
        border="#3d006e",
        accent="#c084fc",
        accent2="#f472b6",
        accent_hover="#a855f7",
        text="#faf0ff",
        text_secondary="#9b72c8",
        text_disabled="#5b3a7a",
        success="#4ade80",
        warning="#facc15",
        danger="#fb7185",
        info="#818cf8",
    ),
    "clair_pro": Theme(
        name="Clair Professionnel",
        bg="#f8fafc",
        bg_alt="#f1f5f9",
        sidebar="#ffffff",
        card="#ffffff",
        card_hover="#f8fafc",
        border="#e2e8f0",
        accent="#0f766e",
        accent2="#0284c7",
        accent_hover="#0d6460",
        text="#0f172a",
        text_secondary="#64748b",
        text_disabled="#94a3b8",
        success="#16a34a",
        warning="#d97706",
        danger="#dc2626",
        info="#0284c7",
    ),
    "ocean": Theme(
        name="Océan",
        bg="#001a2c",
        bg_alt="#00131f",
        sidebar="#002540",
        card="#003050",
        card_hover="#003d66",
        border="#005080",
        accent="#00d4aa",
        accent2="#00b4d8",
        accent_hover="#00b894",
        text="#e0f7f4",
        text_secondary="#5b9cb8",
        text_disabled="#2d6a80",
        success="#00e5cc",
        warning="#ffb703",
        danger="#ef476f",
        info="#00b4d8",
    ),
}

DEFAULT_THEME = "noir_vert"


def get_stylesheet(theme: Theme) -> str:
    """Génère la feuille de style Qt complète pour un thème."""
    is_dark = theme.bg < "#888888"  # heuristique simple pour dark/light

    scrollbar_bg = theme.sidebar if is_dark else "#e2e8f0"
    scrollbar_handle = theme.border if is_dark else "#94a3b8"

    return f"""
/* ═══════════════════════════════════════════════════════
   ASTA ACADÉMIE — Design System Qt
   Thème: {theme.name}
═══════════════════════════════════════════════════════ */

/* ── Base ─────────────────────────────────────────────── */
QWidget {{
    background-color: {theme.bg};
    color: {theme.text};
    font-family: "{theme.font_primary}", "Segoe UI", sans-serif;
    font-size: 13px;
}}

QMainWindow, QDialog {{
    background-color: {theme.bg};
}}

/* ── Sidebar ──────────────────────────────────────────── */
#SidebarWidget {{
    background-color: {theme.sidebar};
    border-right: 1px solid {theme.border};
    min-width: 220px;
    max-width: 220px;
}}

#SidebarWidget QLabel#LogoLabel {{
    font-size: 16px;
    font-weight: 700;
    color: {theme.accent};
    letter-spacing: 1px;
}}

#SidebarWidget QLabel#PromoLabel {{
    font-size: 10px;
    color: {theme.text_secondary};
}}

/* ── NavButtons ───────────────────────────────────────── */
QPushButton.nav_btn {{
    background-color: transparent;
    color: {theme.text_secondary};
    border: none;
    border-radius: {theme.radius_sm}px;
    padding: 10px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton.nav_btn:hover {{
    background-color: {theme.card_hover};
    color: {theme.text};
}}

QPushButton.nav_btn[active="true"] {{
    background-color: {theme.accent}22;
    color: {theme.accent};
    border-left: 4px solid {theme.accent};
    font-weight: 600;
}}

/* ── TopBar ───────────────────────────────────────────── */
#TopbarWidget {{
    background-color: {theme.sidebar};
    border-bottom: 1px solid {theme.border};
    min-height: 54px;
    max-height: 54px;
}}

/* ── StatusBar ────────────────────────────────────────── */
#statusbar {{
    background-color: {theme.sidebar};
    border-top: 1px solid {theme.border};
    min-height: 28px;
    max-height: 28px;
}}

/* ── Cards ────────────────────────────────────────────── */
QFrame.card {{
    background-color: {theme.card};
    border: 1px solid {theme.border};
    border-radius: {theme.radius_lg}px;
}}

QFrame.card:hover {{
    border-color: {theme.accent}55;
    background-color: {theme.card_hover};
}}

QFrame.card_flat {{
    background-color: {theme.card};
    border: none;
    border-radius: {theme.radius_md}px;
}}

/* ── Boutons Principaux ───────────────────────────────── */
QPushButton.primary {{
    background-color: {theme.accent};
    color: #ffffff;
    border: none;
    border-radius: {theme.radius_sm}px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
}}

QPushButton.primary:hover {{
    background-color: {theme.accent_hover};
}}

QPushButton.primary:pressed {{
    background-color: {theme.accent2};
}}

QPushButton.primary:disabled {{
    background-color: {theme.text_disabled};
    color: {theme.bg};
}}

QPushButton.secondary {{
    background-color: transparent;
    color: {theme.accent};
    border: 1px solid {theme.accent};
    border-radius: {theme.radius_sm}px;
    padding: 9px 19px;
    font-weight: 500;
}}

QPushButton.secondary:hover {{
    background-color: {theme.accent}22;
}}

QPushButton#IconButton {{
    background-color: transparent;
    color: {theme.text_secondary};
    border: none;
    border-radius: {theme.radius_sm}px;
    padding: 8px 14px;
}}

QPushButton#IconButton:hover {{
    background-color: {theme.card_hover};
    color: {theme.text};
}}

QPushButton.danger_btn {{
    background-color: {theme.danger};
    color: #ffffff;
    border: none;
    border-radius: {theme.radius_sm}px;
    padding: 9px 18px;
    font-weight: 600;
}}

QPushButton.danger_btn:hover {{
    background-color: #dc2626;
}}

/* ── Inputs ───────────────────────────────────────────── */
QLineEdit#SearchBox, QTextEdit, QPlainTextEdit {{
    background-color: {theme.card};
    color: {theme.text};
    border: 1px solid {theme.border};
    border-radius: {theme.radius_sm}px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: {theme.accent}44;
}}

QLineEdit#SearchBox:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {theme.accent};
    outline: none;
}}

QLineEdit::placeholder {{
    color: {theme.text_disabled};
}}

/* ── ComboBox ─────────────────────────────────────────── */
QComboBox {{
    background-color: {theme.card};
    color: {theme.text};
    border: 1px solid {theme.border};
    border-radius: {theme.radius_sm}px;
    padding: 8px 12px;
    font-size: 13px;
    min-width: 120px;
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
}}

QComboBox:hover {{
    border-color: {theme.accent};
}}

QComboBox QAbstractItemView {{
    background-color: {theme.card};
    color: {theme.text};
    border: 1px solid {theme.border};
    selection-background-color: {theme.accent}33;
    outline: none;
}}

/* ── Labels spéciaux ──────────────────────────────────── */
QLabel#HeroTitle {{
    font-size: 32px;
    font-weight: 800;
    color: {theme.text};
}}

QLabel#HeroSubtitle {{
    font-size: 14px;
    font-weight: 600;
    color: {theme.text_secondary};
}}

QLabel#SectionTitle {{
    font-size: 20px;
    font-weight: 700;
    color: {theme.text};
    margin-top: 15px;
}}

QLabel#CardTitle {{
    font-size: 11px;
    font-weight: 600;
    color: {theme.text_secondary};
    text-transform: uppercase;
    letter-spacing: 1px;
}}

QLabel#CardValue {{
    font-size: 24px;
    font-weight: 700;
    color: {theme.text};
}}

QLabel.accent {{
    color: {theme.accent};
    font-weight: 600;
}}

QLabel.success {{
    color: {theme.success};
    font-weight: 600;
}}

QLabel.warning {{
    color: {theme.warning};
    font-weight: 600;
}}

QLabel.danger {{
    color: {theme.danger};
    font-weight: 600;
}}

QLabel.mono {{
    font-family: "{theme.font_mono}", "Courier New", monospace;
    font-size: 13px;
}}

/* ── Tables ───────────────────────────────────────────── */
QTableWidget {{
    background-color: {theme.card};
    color: {theme.text};
    border: 1px solid {theme.border};
    border-radius: {theme.radius_md}px;
    gridline-color: {theme.border};
    font-size: 13px;
}}

QTableWidget::item {{
    padding: 8px 12px;
    border: none;
}}

QTableWidget::item:selected {{
    background-color: {theme.accent}33;
    color: {theme.text};
}}

QHeaderView::section {{
    background-color: {theme.sidebar};
    color: {theme.text_secondary};
    padding: 8px 12px;
    border: none;
    border-bottom: 1px solid {theme.border};
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* ── Scrollbars ───────────────────────────────────────── */
QScrollBar:vertical {{
    background-color: {scrollbar_bg};
    width: 8px;
    border: none;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background-color: {scrollbar_handle};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {theme.accent}88;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {scrollbar_bg};
    height: 8px;
    border: none;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal {{
    background-color: {scrollbar_handle};
    border-radius: 4px;
    min-width: 30px;
}}

/* ── Tabs ─────────────────────────────────────────────── */
QTabWidget::pane {{
    border: 1px solid {theme.border};
    border-radius: {theme.radius_md}px;
    background-color: {theme.card};
    top: -1px;
}}

QTabBar::tab {{
    background-color: transparent;
    color: {theme.text_secondary};
    padding: 10px 20px;
    border: none;
    border-bottom: 2px solid transparent;
    font-weight: 500;
    font-size: 13px;
}}

QTabBar::tab:selected {{
    color: {theme.accent};
    border-bottom-color: {theme.accent};
    font-weight: 600;
}}

QTabBar::tab:hover:!selected {{
    color: {theme.text};
    background-color: {theme.card_hover};
}}

/* ── Progress Bar ─────────────────────────────────────── */
QProgressBar {{
    background-color: {theme.border};
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
    font-size: 0px;
}}

QProgressBar::chunk {{
    background-color: {theme.accent};
    border-radius: 4px;
}}

/* ── Slider ───────────────────────────────────────────── */
QSlider::groove:horizontal {{
    background-color: {theme.border};
    height: 4px;
    border-radius: 2px;
}}

QSlider::handle:horizontal {{
    background-color: {theme.accent};
    border: 2px solid {theme.accent};
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}

QSlider::sub-page:horizontal {{
    background-color: {theme.accent};
    border-radius: 2px;
}}

/* ── CheckBox / RadioButton ───────────────────────────── */
QCheckBox, QRadioButton {{
    color: {theme.text};
    spacing: 8px;
    font-size: 13px;
}}

QCheckBox::indicator, QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {theme.border};
    border-radius: 4px;
    background-color: {theme.card};
}}

QCheckBox::indicator:checked {{
    background-color: {theme.accent};
    border-color: {theme.accent};
}}

QRadioButton::indicator {{
    border-radius: 9px;
}}

QRadioButton::indicator:checked {{
    background-color: {theme.accent};
    border-color: {theme.accent};
}}

/* ── ToolTip ──────────────────────────────────────────── */
QToolTip {{
    background-color: {theme.card};
    color: {theme.text};
    border: 1px solid {theme.border};
    border-radius: {theme.radius_sm}px;
    padding: 6px 10px;
    font-size: 12px;
}}

/* ── MessageBox ───────────────────────────────────────── */
QMessageBox {{
    background-color: {theme.bg};
    color: {theme.text};
}}

QMessageBox QPushButton {{
    background-color: {theme.accent};
    color: #ffffff;
    border: none;
    border-radius: {theme.radius_sm}px;
    padding: 8px 20px;
    font-weight: 600;
    min-width: 80px;
}}

QMessageBox QPushButton:hover {{
    background-color: {theme.accent_hover};
}}

/* ── Splitter ─────────────────────────────────────────── */
QSplitter::handle {{
    background-color: {theme.border};
}}

/* ── GroupBox ─────────────────────────────────────────── */
QGroupBox {{
    border: 1px solid {theme.border};
    border-radius: {theme.radius_md}px;
    margin-top: 12px;
    padding-top: 10px;
    color: {theme.text_secondary};
    font-weight: 600;
    font-size: 12px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: {theme.accent};
}}

/* ── Stacked Pages ────────────────────────────────────── */
QStackedWidget {{
    background-color: {theme.bg};
}}

/* ── Stat Badge ───────────────────────────────────────── */
QLabel.badge {{
    background-color: {theme.accent}22;
    color: {theme.accent};
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}}

QLabel.badge_success {{
    background-color: {theme.success}22;
    color: {theme.success};
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}}

QLabel.badge_warning {{
    background-color: {theme.warning}22;
    color: {theme.warning};
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}}

QLabel.badge_danger {{
    background-color: {theme.danger}22;
    color: {theme.danger};
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}}
"""
