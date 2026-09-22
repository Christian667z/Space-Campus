"""
Asta Académie — AuthWindow Premium (CustomTkinter)
==================================================
Interface d'authentification robuste, asynchrone et thread-safe.
Intègre le bus d'événements global et élimine les popups natifs obsolètes.
"""

from __future__ import annotations

import sys
import logging
import threading
from typing import Optional

import customtkinter as ctk

# Imports de l'architecture Asta Académie
from core.auth_manager import AuthManager
from utils.event_bus import EventBus, AppEvents

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes de Design Universelles
# ---------------------------------------------------------------------------
COLOR_BG = "#0f172a"          # Fond d'écran profond Slate
COLOR_CARD = "#111827"        # Carte centrale
COLOR_ACCENT = "#10b981"      # Émeraude Cyber Asta
COLOR_HOVER = "#059669"       # Émeraude assombri au survol
COLOR_BORDER = "#1e293b"      # Bordure de champ par défaut
COLOR_BORDER_ERR = "#ef4444"  # Bordure en cas d'erreur
COLOR_TEXT_MUTED = "#94a3b8"  # Sous-titres et placeholders


class AuthWindow(ctk.CTk):
    """
    Fenêtre maîtresse d'authentification CustomTkinter.
    Gère la connexion, l'inscription et la communication par EventBus.
    """

    def __init__(self) -> None:
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.title("Asta Académie — Authentification")
        self.geometry("420x560")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        # États internes de la machine à états de l'UI
        self.success: bool = False
        self.mode: str = "login"  # 'login' ou 'register'

        # Centrage de la fenêtre à l'écran
        self._center_on_screen()
        
        # Assemblage des composants graphiques
        self._build_ui()

    def _center_on_screen(self) -> None:
        """Calcule et positionne la fenêtre au centre exact de l'écran."""
        self.update_idletasks()
        width = 420
        height = 560
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self) -> None:
        """Construit le layout de l'interface en split modulaire."""
        # Conteneur principal de type "Card"
        self.card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=16, border_width=1, border_color="#1e293b")
        self.card.pack(padx=24, pady=24, fill="both", expand=True)

        # En-tête / Titre
        self.title_lbl = ctk.CTkLabel(
            self.card, text="Connexion", 
            font=("Segoe UI", 26, "bold"), text_color=COLOR_ACCENT
        )
        self.title_lbl.pack(pady=(36, 8))

        self.subtitle_lbl = ctk.CTkLabel(
            self.card, text="Accédez à votre espace informatique L1-L4",
            font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED
        )
        self.subtitle_lbl.pack(pady=(0, 24))

        # Zone d'affichage des messages d'erreur/succès intégrée (Adieu les popups !)
        self.status_lbl = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 12, "medium"), text_color=COLOR_BORDER_ERR)
        self.status_lbl.pack(fill="x", padx=32, pady=(0, 12))

        # Champ d'authentification : Identifiant
        self.nom_entry = ctk.CTkEntry(
            self.card, placeholder_text="Nom d'utilisateur", 
            height=44, fg_color=COLOR_BG, border_color=COLOR_BORDER, corner_radius=8
        )
        self.nom_entry.pack(fill="x", padx=32, pady=6)

        # Champ d'authentification : Mot de passe
        self.pass_entry = ctk.CTkEntry(
            self.card, placeholder_text="Mot de passe", show="*", 
            height=44, fg_color=COLOR_BG, border_color=COLOR_BORDER, corner_radius=8
        )
        self.pass_entry.pack(fill="x", padx=32, pady=6)
        
        # Raccourci de validation par touche Entrée
        self.nom_entry.bind("<Return>", lambda e: self._handle_action())
        self.pass_entry.bind("<Return>", lambda e: self._handle_action())

        # Bouton d'action principal (Call To Action)
        self.btn_action = ctk.CTkButton(
            self.card, text="Se connecter", height=46, 
            font=("Segoe UI", 13, "bold"), fg_color=COLOR_ACCENT, 
            hover_color=COLOR_HOVER, corner_radius=8, command=self._handle_action
        )
        self.btn_action.pack(fill="x", padx=32, pady=(20, 16))

        # Liens d'assistance et basculement de mode
        self.switch_mode_btn = ctk.CTkButton(
            self.card, text="Pas encore de compte ? Créer un espace", 
            font=("Segoe UI", 11, "underline"), fg_color="transparent", 
            text_color=COLOR_TEXT_MUTED, hover_color="#1e293b", command=self._switch_view_mode
        )
        self.switch_mode_btn.pack(pady=4)

        self.forgot_pwd_btn = ctk.CTkButton(
            self.card, text="Besoin d'aide ou clé d'activation manquante ?", 
            font=("Segoe UI", 10), fg_color="transparent", 
            text_color="#4b5563", hover_color="#1e293b", command=self._show_help_message
        )
        self.forgot_pwd_btn.pack(pady=(8, 16))

    def _switch_view_mode(self) -> None:
        """Alterne dynamiquement l'interface entre le mode Connexion et Inscription."""
        self._clear_status()
        if self.mode == "login":
            self.mode = "register"
            self.title_lbl.configure(text="Inscription")
            self.btn_action.configure(text="Créer mon compte étudiant")
            self.switch_mode_btn.configure(text="Déjà inscrit ? Retour à la connexion")
            self.forgot_pwd_btn.pack_forget()  # Masquer l'aide sur le formulaire d'inscription
        else:
            self.mode = "login"
            self.title_lbl.configure(text="Connexion")
            self.btn_action.configure(text="Se connecter")
            self.switch_mode_btn.configure(text="Pas encore de compte ? Créer un espace")
            self.forgot_pwd_btn.pack(pady=(8, 16))

    def _show_status(self, message: str, is_error: bool = True) -> None:
        """Affiche un message d'information ou d'erreur stylisé directement dans la vue."""
        color = COLOR_BORDER_ERR if is_error else COLOR_ACCENT
        self.status_lbl.configure(text=message, text_color=color)
        
        # Changement de couleur de bordure des inputs si erreur générale de saisie
        if is_error:
            self.nom_entry.configure(border_color=COLOR_BORDER_ERR)
            self.pass_entry.configure(border_color=COLOR_BORDER_ERR)

    def _clear_status(self) -> None:
        """Réinitialise les indicateurs visuels d'erreur."""
        self.status_lbl.configure(text="")
        self.nom_entry.configure(border_color=COLOR_BORDER)
        self.pass_entry.configure(border_color=COLOR_BORDER)

    def _show_help_message(self) -> None:
        """Affiche les coordonnées du support technique en cas de blocage."""
        self._show_status("💡 Support UNASMOH : Contactez le +509 3567-2037", is_error=False)

    def _set_ui_lock(self, locked: bool) -> None:
        """Verrouille ou déverrouille les contrôles graphiques pour empêcher le multi-clic."""
        state = "disabled" if locked else "normal"
        self.btn_action.configure(state=state)
        self.nom_entry.configure(state=state)
        self.pass_entry.configure(state=state)
        self.switch_mode_btn.configure(state=state)
        
        if locked:
            self.btn_action.configure(text="⏳ Traitement sécurisé...")
        else:
            self.btn_action.configure(text="Se connecter" if self.mode == "login" else "Créer mon compte étudiant")

    def _handle_action(self) -> None:
        """Valide les entrées et délègue l'authentification à un thread d'arrière-plan."""
        self._clear_status()
        nom = self.nom_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        # Validation de premier niveau (Client-side validation)
        if not nom or not pwd:
            self._show_status("❌ Tous les champs requis doivent être remplis.")
            return

        # Verrouillage défensif de l'UI
        self._set_ui_lock(True)

        # Worker asynchrone pour l'exécution réseau/base de données sans figer la fenêtre
        def _auth_worker() -> None:
            try:
                if self.mode == "login":
                    success, msg = AuthManager.login(nom, pwd, "Asta_Desktop_App")
                    if success:
                        self.success = True
                        # Publication sur le Bus d'événements global de l'application
                        EventBus.publish(AppEvents.AUTH_SUCCESS, {"username": nom})
                        self.after(0, self.destroy)
                    else:
                        self.after(0, lambda m=msg: self._safe_ui_failure(f"❌ {m}"))
                else:
                    # Traitement du workflow d'inscription
                    success, msg = AuthManager.register(nom, pwd)
                    if success:
                        # Auto-login immédiat après création réussie
                        log_success, log_msg = AuthManager.login(nom, pwd, "Asta_Desktop_App")
                        if log_success:
                            self.success = True
                            EventBus.publish(AppEvents.AUTH_SUCCESS, {"username": nom})
                            self.after(0, self.destroy)
                        else:
                            self.after(0, lambda m=log_msg: self._safe_ui_failure(f"❌ Inscription OK mais login échoué : {m}"))
                    else:
                        self.after(0, lambda m=msg: self._safe_ui_failure(f"❌ Échec de la création : {m}"))
            except Exception as e:
                logger.error("Erreur critique d'authentification : %s", e)
                self.after(0, lambda: self._safe_ui_failure("❌ Erreur de communication serveur."))

        threading.Thread(target=_auth_worker, daemon=True).start()

    def _safe_ui_failure(self, error_message: str) -> None:
        """Méthode thread-safe appelée pour déverrouiller l'UI et afficher l'échec."""
        self._set_ui_lock(False)
        self._show_status(error_message, is_error=True)


# Module de test autonome
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")  # Thème émeraude par défaut de CustomTkinter
    
    # Simulation du bus et gestionnaire si lancé de manière isolée pour debug
    if not hasattr(AppEvents, "AUTH_SUCCESS"):
        class FakeEvents: AUTH_SUCCESS = "auth_success"
        class FakeBus: 
            @staticmethod
            def publish(e, d): print(f"[Bus Event] {e} tiré avec les données: {d}")
        AppEvents = FakeEvents
        EventBus = FakeBus

    app = AuthWindow()
    app.mainloop()