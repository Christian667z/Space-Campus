import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                               QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from ui.layouts.sidebar import Sidebar
from ui.layouts.topbar import Topbar
from ui.views.dashboard import DashboardView
from ui.themes.theme_manager import THEMES, DEFAULT_THEME, get_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asta Académie — PySide6 Modern SaaS")
        self.setMinimumSize(1200, 800)
        
        # Charger le thème QSS
        self._load_stylesheet()
        
        # Widget Central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout Principal Horizontal
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.nav_clicked.connect(self._navigate)
        self.main_layout.addWidget(self.sidebar)
        
        # Zone de contenu principal (Topbar + Stacked Views)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Topbar
        self.topbar = Topbar()
        self.content_layout.addWidget(self.topbar)
        
        # Stacked Widget pour les vues (Lazy Loading natif)
        self.stacked_widget = QStackedWidget()
        
        # Initialisation des vues
        self.views = {
            "dashboard": DashboardView(),
            # "courses": CoursesView(),
            # "spacecode": SpacecodeView(),
            # ...
        }
        
        for view in self.views.values():
            self.stacked_widget.addWidget(view)
            
        self.content_layout.addWidget(self.stacked_widget)
        
        self.main_layout.addWidget(self.content_widget)
        
        # Optionnel: icône
        try:
            self.setWindowIcon(QIcon("assets/Space_logo.ico"))
        except:
            pass

    def _load_stylesheet(self):
        theme = THEMES.get(DEFAULT_THEME, list(THEMES.values())[0])
        qss = get_stylesheet(theme)
        self.setStyleSheet(qss)

    def _navigate(self, view_id):
        if view_id in self.views:
            self.stacked_widget.setCurrentWidget(self.views[view_id])
        else:
            print(f"Vue {view_id} non implémentée !")
