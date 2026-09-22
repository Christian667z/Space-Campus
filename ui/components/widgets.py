"""
Asta Académie — Composants UI Réutilisables
Cards, Badges, Stat Tiles, Charts, Animations
"""
from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QProgressBar
)
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer, Signal, QRect,
    QSize, Property
)
from PySide6.QtGui import (
    QColor, QPainter, QPen, QBrush, QFont, QFontMetrics,
    QPaintEvent, QLinearGradient, QIcon, QPixmap
)
from pathlib import Path
import math

from utils.svg_manager import SVGManager


# ── Utilitaire : ombre portée ────────────────────────────────────────
def add_shadow(widget: QWidget, blur: int = 18, x: int = 0, y: int = 4,
               color: str = "#00000033"):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setOffset(x, y)
    shadow.setColor(QColor(color))
    widget.setGraphicsEffect(shadow)


# ── Card ──────────────────────────────────────────────────────────────
class Card(QFrame):
    """Carte moderne avec coins arrondis et ombre légère."""
    def __init__(self, parent=None, hover=True):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setFrameShape(QFrame.NoFrame)
        if hover:
            add_shadow(self, blur=12, y=3, color="#00000028")


class FlatCard(QFrame):
    """Carte plate sans bordure."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card_flat")
        self.setFrameShape(QFrame.NoFrame)


# ── StatCard ─────────────────────────────────────────────────────────
class StatCard(Card):
    """Tuile de statistique : icône + titre + valeur."""
    clicked = Signal()

    def __init__(self, icon: str, title: str, value: str, color: str,
                 parent=None):
        super().__init__(parent)
        self.color = color
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)

        # Icône (utilisation de SVGManager)
        icon_lbl = QLabel()
        qicon = SVGManager.get_icon(icon, color=color, size=32)
        if not qicon.isNull():
            icon_lbl.setPixmap(qicon.pixmap(32, 32))
        else:
            icon_lbl.setText(icon)
            icon_lbl.setFont(QFont("Segoe UI Emoji", 26))
            
        icon_lbl.setAlignment(Qt.AlignLeft)
        layout.addWidget(icon_lbl)

        # Titre
        self.title_lbl = QLabel(title)
        self.title_lbl.setProperty("class", "caption")
        self.title_lbl.setWordWrap(True)
        layout.addWidget(self.title_lbl)

        # Valeur
        self.value_lbl = QLabel(value)
        self.value_lbl.setFont(QFont("Consolas", 24, QFont.Bold))
        self.value_lbl.setStyleSheet(f"color: {color};")
        layout.addWidget(self.value_lbl)

    def update_value(self, value: str):
        self.value_lbl.setText(value)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


# ── Badge ─────────────────────────────────────────────────────────────
class Badge(QLabel):
    """Badge coloré compact."""
    def __init__(self, text: str, style: str = "accent", parent=None):
        super().__init__(text, parent)
        style_map = {
            "accent": "badge",
            "success": "badge_success",
            "warning": "badge_warning",
            "danger": "badge_danger",
        }
        self.setProperty("class", style_map.get(style, "badge"))
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


# ── Section Header ────────────────────────────────────────────────────
class SectionHeader(QWidget):
    """En-tête de section avec titre et sous-titre."""
    def __init__(self, title: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        # support optional icon names in title (icon can be a short id resolved to svg)
        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_lbl.setProperty("class", "title")
        layout.addWidget(title_lbl)

        if subtitle:
            sub_lbl = QLabel(subtitle)
            sub_lbl.setProperty("class", "caption")
            layout.addWidget(sub_lbl)


# ── Mini XP Bar ───────────────────────────────────────────────────────
class XPBar(QProgressBar):
    """Barre XP avec animation fluide."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)
        self.setFixedHeight(6)
        self._anim = QPropertyAnimation(self, b"value")
        self._anim.setDuration(800)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def animate_to(self, value: int):
        self._anim.setStartValue(self.value())
        self._anim.setEndValue(value)
        self._anim.start()


# ── Animated Counter ──────────────────────────────────────────────────
class AnimatedCounter(QLabel):
    """Label qui anime le changement de valeur numérique."""
    def __init__(self, value: int = 0, suffix: str = "", parent=None):
        super().__init__(parent)
        self._value = value
        self._target = value
        self._suffix = suffix
        self.setText(f"{value}{suffix}")
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._step = 0
        self._steps = 30

    def animate_to(self, target: int):
        self._start = self._value
        self._target = target
        self._step = 0
        self._timer.start(16)  # ~60fps

    def _tick(self):
        self._step += 1
        t = self._step / self._steps
        # Ease out cubic
        t = 1 - (1 - t) ** 3
        self._value = int(self._start + (self._target - self._start) * t)
        self.setText(f"{self._value}{self._suffix}")
        if self._step >= self._steps:
            self._value = self._target
            self.setText(f"{self._target}{self._suffix}")
            self._timer.stop()


# ── Network Indicator ─────────────────────────────────────────────────
class NetworkIndicator(QWidget):
    """Indicateur de connexion avec animation pulse."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._online = False
        self._pulse = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_pulse)
        self.setFixedSize(80, 22)

    def set_online(self, online: bool):
        self._online = online
        if online:
            self._timer.start(50)
        else:
            self._timer.stop()
        self.update()

    def _update_pulse(self):
        self._pulse = (self._pulse + 0.1) % (2 * math.pi)
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dot
        if self._online:
            alpha = int(180 + 75 * math.sin(self._pulse))
            color = QColor(16, 185, 129, alpha)
            text = "En ligne"
        else:
            color = QColor(239, 68, 68)
            text = "Hors ligne"

        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 7, 8, 8)

        # Text
        painter.setPen(QPen(color))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(QRect(14, 0, 66, 22), Qt.AlignVCenter | Qt.AlignLeft, text)


# ── XP Graph (Canvas 7 jours) ─────────────────────────────────────────
class XPGraph(QWidget):
    """Graphique de progression XP sur 7 jours."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = [0] * 7
        self._labels = ["L", "M", "M", "J", "V", "S", "D"]
        self._accent = "#10b981"
        self.setMinimumHeight(140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_data(self, data: list, labels: list, accent: str):
        self._data = data
        self._labels = labels
        self._accent = accent
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        pad = 28
        bar_w = max(8, (w - pad * 2) // len(self._data) - 8)
        max_val = max(self._data) if any(v > 0 for v in self._data) else 1

        accent = QColor(self._accent)

        for i, val in enumerate(self._data):
            x = pad + i * ((w - pad * 2) // len(self._data)) + 4
            bar_h = int((val / max_val) * (h - pad - 30)) if max_val > 0 else 0

            # Gradient bar
            grad = QLinearGradient(x, h - pad - bar_h, x, h - pad)
            grad.setColorAt(0, QColor(accent.red(), accent.green(), accent.blue(), 220))
            grad.setColorAt(1, QColor(accent.red(), accent.green(), accent.blue(), 60))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.NoPen)
            r = min(bar_w // 2, 5)
            painter.drawRoundedRect(x, h - pad - bar_h, bar_w, bar_h, r, r)

            # Label
            painter.setPen(QPen(QColor("#94a3b8")))
            painter.setFont(QFont("Segoe UI", 10))
            if i < len(self._labels):
                painter.drawText(QRect(x, h - pad + 5, bar_w, 18),
                                 Qt.AlignCenter, self._labels[i])

            # Value (si non-zéro)
            if val > 0:
                painter.setPen(QPen(accent))
                painter.setFont(QFont("Segoe UI", 8, QFont.Bold))
                painter.drawText(QRect(x - 4, h - pad - bar_h - 18, bar_w + 8, 16),
                                 Qt.AlignCenter, str(val))

        # Baseline
        painter.setPen(QPen(QColor("#334155"), 1))
        painter.drawLine(pad, h - pad, w - pad, h - pad)


# Helper to resolve lightweight SVG/icon placeholders (fallback to text)
def _make_icon_label(icon: str, size: int = 32, color: str = "#ffffff") -> QLabel:
    lbl = QLabel()
    # If icon is registered in SVGManager
    qicon = SVGManager.get_icon(icon, color=color, size=size)
    if not qicon.isNull():
        lbl.setPixmap(qicon.pixmap(size, size))
    else:
        # Fallback PNG check
        ico_path = Path(__file__).parent.parent.joinpath('assets', 'icons', f"{icon}.png")
        if ico_path.exists():
            pix = QIcon(str(ico_path)).pixmap(size, size)
            lbl.setPixmap(pix)
        else:
            lbl.setText(icon)
            lbl.setFont(QFont("Segoe UI Symbol", int(size * 0.7)))
    lbl.setFixedWidth(size)
    lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    return lbl


# ── PomodoroWidget ────────────────────────────────────────────────────
class PomodoroWidget(QWidget):
    """Timer Pomodoro compact pour la topbar."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._seconds = 25 * 60
        self._running = False
        self._mode = "work"
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.setInterval(1000)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.time_lbl = QLabel("25:00")
        self.time_lbl.setFont(QFont("Consolas", 11, QFont.Bold))
        self.time_lbl.setStyleSheet("color: #10b981;")
        layout.addWidget(self.time_lbl)

        self.toggle_btn = QPushButton("▶")
        self.toggle_btn.setFixedSize(26, 26)
        self.toggle_btn.setProperty("class", "ghost")
        self.toggle_btn.clicked.connect(self.toggle)
        layout.addWidget(self.toggle_btn)

        reset_btn = QPushButton("↺")
        reset_btn.setFixedSize(26, 26)
        reset_btn.setProperty("class", "ghost")
        reset_btn.clicked.connect(self.reset)
        layout.addWidget(reset_btn)

    def toggle(self):
        self._running = not self._running
        if self._running:
            self._timer.start()
            self.toggle_btn.setText("⏸")
        else:
            self._timer.stop()
            self.toggle_btn.setText("▶")

    def reset(self):
        self._running = False
        self._timer.stop()
        self._seconds = 25 * 60
        self._mode = "work"
        self.toggle_btn.setText("Start")
        self._update_display()

    def _tick(self):
        if self._seconds > 0:
            self._seconds -= 1
            self._update_display()
        else:
            self._timer.stop()
            self._running = False
            if self._mode == "work":
                self._mode = "break"
                self._seconds = 5 * 60
                self.time_lbl.setStyleSheet("color: #f59e0b;")
            else:
                self._mode = "work"
                self._seconds = 25 * 60
                self.time_lbl.setStyleSheet("color: #10b981;")
            self.toggle_btn.setText("▶")

    def _update_display(self):
        m, s = divmod(self._seconds, 60)
        self.time_lbl.setText(f"⏱ {m:02d}:{s:02d}")
