from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLineEdit, QPushButton, 
                               QSpacerItem, QSizePolicy, QLabel)
from PySide6.QtCore import Qt
import qtawesome as qta
from ui.components.ui_components import PomodoroWidget, NetworkIndicator

class Topbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("TopbarWidget")
        self.setFixedHeight(70)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        
        self._build_search()
        
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self._build_actions()

    def _build_search(self):
        self.search_box = QLineEdit()
        self.search_box.setObjectName("SearchBox")
        self.search_box.setPlaceholderText("Rechercher un cours, un raccourci...")
        self.search_box.setFixedWidth(350)
        self.search_box.setFixedHeight(36)
        
        # Icône dans la barre de recherche (PySide6 permet d'ajouter des actions dans le QLineEdit)
        search_icon = qta.icon("fa5s.search", color="#94a3b8")
        self.search_box.addAction(search_icon, QLineEdit.LeadingPosition)
        
        self.layout.addWidget(self.search_box)

    def _build_actions(self):
        # Pomodoro
        self.pomodoro = PomodoroWidget()
        self.layout.addWidget(self.pomodoro)
        
        self.layout.addSpacing(15)
        
        # Network Indicator
        self.network = NetworkIndicator()
        self.network.set_online(True)
        self.layout.addWidget(self.network)
        
        self.layout.addSpacing(15)
        
        # Notification Button
        self.bell_btn = QPushButton()
        self.bell_btn.setObjectName("IconButton")
        self.bell_btn.setIcon(qta.icon("fa5s.bell", color="#94a3b8"))
        self.bell_btn.setFixedSize(36, 36)
        self.layout.addWidget(self.bell_btn)
        
        # Profile Indicator (just a colored label or icon for now)
        self.profile_lbl = QLabel()
        self.profile_lbl.setFixedSize(36, 36)
        self.profile_lbl.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b82f6, stop:1 #8b5cf6);
            border-radius: 18px;
            border: 2px solid rgba(255,255,255,0.05);
        """)
        self.layout.addWidget(self.profile_lbl)
