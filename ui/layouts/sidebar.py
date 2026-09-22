from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                               QSpacerItem, QSizePolicy, QButtonGroup)
from PySide6.QtCore import Qt, Signal
import qtawesome as qta

class Sidebar(QWidget):
    # Signal émis lors du clic sur un bouton du menu (envoie l'ID de la vue)
    nav_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("SidebarWidget")
        self.setFixedWidth(260)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)

        self._build_header()
        
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)
        
        self._build_menu()
        
        # Spacer pour pousser le footer vers le bas
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self._build_footer()

    def _build_header(self):
        # Titre / Logo
        self.logo_lbl = QLabel("Asta Académie")
        self.logo_lbl.setObjectName("LogoLabel")
        self.layout.addWidget(self.logo_lbl)
        
        # Sous-titre
        self.promo_lbl = QLabel("UNASMOH • Promo 2028")
        self.promo_lbl.setObjectName("PromoLabel")
        self.layout.addWidget(self.promo_lbl)

    def _build_menu(self):
        menu_items = [
            ("dashboard", "Dashboard", "fa5s.home"),
            ("courses", "Mes Cours", "fa5s.book-open"),
            ("spacecode", "SpaceCode IDE", "fa5s.code"),
            ("hacking", "DevSecurity", "fa5s.shield-alt"),
            ("shortcuts", "Raccourcis", "fa5s.bolt"),
        ]

        for idx, (view_id, text, icon_name) in enumerate(menu_items):
            btn = QPushButton(f"  {text}")
            btn.setObjectName("SidebarButton")
            
            # Utilisation de qtawesome pour les icônes vectorielles nettes
            icon = qta.icon(icon_name, color="#94a3b8", color_active="#22c55e")
            btn.setIcon(icon)
            
            btn.setCheckable(True)
            if idx == 0:
                btn.setChecked(True)
                
            self.btn_group.addButton(btn)
            self.layout.addWidget(btn)
            
            # Capture de l'identifiant via une closure ou lambda
            btn.clicked.connect(lambda checked, vid=view_id: self.nav_clicked.emit(vid))

    def _build_footer(self):
        footer_btn = QPushButton(" Paramètres")
        footer_btn.setObjectName("SidebarButton")
        footer_btn.setIcon(qta.icon("fa5s.cog", color="#94a3b8"))
        self.layout.addWidget(footer_btn)
        # Marges au fond
        self.layout.addSpacing(15)
