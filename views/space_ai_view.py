"""
Asta Académie — Space AI (chat + commandes vocales integrees).
"""
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QFrame, QComboBox, QCheckBox,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap, QPainter

from ui.themes.theme_manager import Theme
from ui.components.widgets import SectionHeader, Card, add_shadow
from core.space_ai_bridge import asset_path, is_cloud_available, load_space_ai_env, launch_jarvis_app
from core.voice_assistant import (
    VoiceListenWorker,
    VoiceSpeakWorker,
    microphone_available,
    speech_available,
    tts_available,
)

try:
    from PySide6.QtSvg import QSvgRenderer
    _HAS_SVG = True
except ImportError:
    _HAS_SVG = False


def _load_logo_pixmap(size: int = 48) -> QPixmap | None:
    candidates = [
        asset_path("space_ai_logo.svg"),
        Path(__file__).resolve().parent.parent / "assets" / "space_ai_logo.svg",
        Path(__file__).resolve().parent.parent / "assets" / "Space_logo_256.png",
    ]
    for path in candidates:
        if not path.is_file():
            continue
        if path.suffix.lower() == ".svg" and _HAS_SVG:
            renderer = QSvgRenderer(str(path))
            if renderer.isValid():
                pix = QPixmap(size, size)
                pix.fill(Qt.transparent)
                painter = QPainter(pix)
                renderer.render(painter)
                painter.end()
                return pix
        elif path.suffix.lower() in (".png", ".jpg", ".ico"):
            pix = QPixmap(str(path))
            if not pix.isNull():
                return pix.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return None


class ChatBubble(QWidget):
    def __init__(self, text: str, is_user: bool, theme: Theme, avatar: QPixmap | None = None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 6)

        bubble = QFrame()
        b_layout = QVBoxLayout(bubble)
        b_layout.setContentsMargins(16, 12, 16, 12)

        lbl = QLabel(text)
        lbl.setFont(QFont("Segoe UI", 11))
        lbl.setWordWrap(True)
        lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)

        if is_user:
            bubble.setStyleSheet(f"""
                QFrame {{
                    background-color: {theme.accent};
                    border-radius: 18px;
                    border-top-right-radius: 4px;
                }}
            """)
            lbl.setStyleSheet("color: #ffffff;")
            lbl.setMinimumWidth(150)
            lbl.setMaximumWidth(600)
            b_layout.addWidget(lbl)
            layout.addStretch(1)
            layout.addWidget(bubble, 0, Qt.AlignRight)
        else:
            bubble.setStyleSheet(f"""
                QFrame {{
                    background-color: {theme.card};
                    border: 1px solid {theme.border};
                    border-radius: 18px;
                    border-top-left-radius: 4px;
                }}
            """)
            lbl.setStyleSheet(f"color: {theme.text};")
            lbl.setMinimumWidth(350)
            lbl.setMaximumWidth(650)
            b_layout.addWidget(lbl)

            layout.setSpacing(12)

            # Avatar OUTSIDE the bubble
            av_lbl = QLabel()
            if avatar and not avatar.isNull():
                av_lbl.setPixmap(avatar)
            else:
                av_lbl.setText("🤖")
                av_lbl.setFont(QFont("Segoe UI Emoji", 14))
                av_lbl.setAlignment(Qt.AlignCenter)
            av_lbl.setFixedSize(36, 36)
            av_lbl.setStyleSheet(f"""
                QLabel {{
                    border-radius: 18px;
                    background: {theme.card};
                    border: 1px solid {theme.border};
                }}
            """)

            layout.addWidget(av_lbl, 0, Qt.AlignTop)
            layout.addWidget(bubble, 0, Qt.AlignLeft)
            layout.addStretch(1)


class SpaceAiPage(QWidget):
    MODES = [
        ("hybrid", "Hybride (cours + Gemini)"),
        ("cloud", "Cloud Gemini"),
        ("local", "Local (hors-ligne)"),
    ]

    def __init__(self, profile: dict, user_id: int, theme: Theme, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.user_id = user_id
        self.theme = theme
        self.state_setup = not bool(self.profile.get("ai_memory"))
        load_space_ai_env()

        from core.ai_engine import AiEngine
        self.engine = AiEngine(self.profile, self.user_id)
        self._avatar = _load_logo_pixmap(36)
        self._listen_worker: Optional[VoiceListenWorker] = None
        self._speak_worker: Optional[VoiceSpeakWorker] = None
        self._voice_enabled = self.profile.get("space_ai_voice", True)
        self.setStyleSheet("background: transparent;")
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 24)
        root.setSpacing(14)

        toolbar = Card(self)
        add_shadow(toolbar, blur=10, y=2, color="#00000022")
        tb = QHBoxLayout(toolbar)
        tb.setContentsMargins(16, 12, 16, 12)

        logo_lbl = QLabel()
        logo_pix = _load_logo_pixmap(44)
        if logo_pix and not logo_pix.isNull():
            logo_lbl.setPixmap(logo_pix)
        else:
            logo_lbl.setText("🤖")
            logo_lbl.setFont(QFont("Segoe UI Emoji", 28))
        logo_lbl.setFixedSize(48, 48)
        tb.addWidget(logo_lbl)

        title_col = QVBoxLayout()
        t1 = QLabel("Space AI")
        t1.setFont(QFont("Segoe UI", 15, QFont.Bold))
        t1.setStyleSheet(f"color: {self.theme.text};")
        cloud_ok = is_cloud_available()
        mic_ok = microphone_available()
        parts = []
        parts.append("Gemini OK" if cloud_ok else "Cle GEMINI : %APPDATA%\\AstaAcademie\\space_ai.env")
        parts.append("Micro OK" if mic_ok else "Micro : pip install pyaudio")
        t2 = QLabel(" · ".join(parts))
        t2.setFont(QFont("Segoe UI", 9))
        t2.setStyleSheet(f"color: {self.theme.text_secondary};")
        title_col.addWidget(t1)
        title_col.addWidget(t2)
        tb.addLayout(title_col, 1)

        tb.addWidget(QLabel("Mode :"))
        self.mode_combo = QComboBox()
        self.mode_combo.setMinimumWidth(200)
        current = (self.profile.get("space_ai_mode") or "hybrid").lower()
        idx = 0
        for i, (key, label) in enumerate(self.MODES):
            self.mode_combo.addItem(label, key)
            if key == current:
                idx = i
        self.mode_combo.setCurrentIndex(idx)
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        tb.addWidget(self.mode_combo)

        # Bouton Premium pour lancer Space AI en version autonome (Desktop)
        self.jarvis_btn = QPushButton("Lancer Space AI")
        self.jarvis_btn.setToolTip("Lancer l'assistant vocal complet Space AI (Fenêtre externe)")
        self.jarvis_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme.accent};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme.accent_hover};
            }}
        """)
        self.jarvis_btn.clicked.connect(self._on_launch_space_ai)
        tb.addWidget(self.jarvis_btn)

        root.addWidget(toolbar)

        root.addWidget(SectionHeader(
            "Assistant d'etudes",
            "Texte ou micro : dites « Space » puis votre question. Reponse vocale optionnelle.",
        ))

        self.voice_status = QLabel("")
        self.voice_status.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 10px;")
        root.addWidget(self.voice_status)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{
                background: {self.theme.bg};
                border: 1px solid {self.theme.border};
                border-radius: 12px;
            }}
        """)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(8)
        self.chat_layout.setContentsMargins(16, 16, 16, 16)
        self.scroll.setWidget(self.chat_container)
        root.addWidget(self.scroll, 1)

        self.typing_lbl = QLabel("Space AI reflechit...")
        self.typing_lbl.setVisible(False)
        self.typing_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-style: italic;")
        root.addWidget(self.typing_lbl)

        input_frame = QFrame()
        input_frame.setStyleSheet(f"""
            QFrame {{
                background: {self.theme.card};
                border: 1px solid {self.theme.border};
                border-radius: 28px;
            }}
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(12, 8, 8, 8)

        self.mic_btn = QPushButton("🎤")
        self.mic_btn.setFixedSize(44, 44)
        self.mic_btn.setToolTip("Parler (dites « Space » + votre question)")
        self.mic_btn.setEnabled(microphone_available())
        self.mic_btn.clicked.connect(self._start_voice_input)
        self.mic_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.theme.card_hover};
                border: 1px solid {self.theme.border};
                border-radius: 22px;
                font-size: 18px;
            }}
            QPushButton:hover {{ background: {self.theme.accent}; }}
            QPushButton:disabled {{ color: {self.theme.text_disabled}; }}
        """)
        input_layout.addWidget(self.mic_btn)

        self.tts_check = QCheckBox("Voix")
        self.tts_check.setChecked(self._voice_enabled and tts_available())
        self.tts_check.setEnabled(tts_available())
        self.tts_check.setStyleSheet(f"color: {self.theme.text};")
        self.tts_check.toggled.connect(self._on_voice_toggle)
        input_layout.addWidget(self.tts_check)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Question, quiz, va sur les cours...")
        self.input_field.returnPressed.connect(self._send_message)
        input_layout.addWidget(self.input_field, 1)
        send_btn = QPushButton("Envoyer")
        send_btn.clicked.connect(self._send_message)
        send_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.theme.accent};
                color: #fff;
                border-radius: 20px;
                padding: 8px 18px;
            }}
            QPushButton:hover {{ background: {self.theme.accent_hover}; }}
        """)
        input_layout.addWidget(send_btn)
        root.addWidget(input_frame)

        nom = self.profile.get("nom", "Etudiant")
        if self.state_setup:
            self._add_bubble(
                f"Bonjour {nom} ! Indiquez vos langages ou centres d'interet pour personnaliser Space AI.",
                False,
            )
        else:
            self._add_bubble(f"Bonjour {nom} ! Posez une question ou tapez quiz / stats.", False)
        if not speech_available():
            self._add_bubble(
                "Module vocal non installe. Relancez install_asta.bat pour activer le micro.",
                False,
            )

    def _on_voice_toggle(self, checked: bool) -> None:
        self._voice_enabled = checked
        self.profile["space_ai_voice"] = checked
        from core.config import save_json, PROFILE_FILE
        save_json(PROFILE_FILE, self.profile)

    def _set_voice_status(self, msg: str) -> None:
        self.voice_status.setText(msg)

    def _start_voice_input(self) -> None:
        if self._listen_worker and self._listen_worker.isRunning():
            return
        self._set_voice_status("Ecoute... parlez maintenant (francais).")
        self.mic_btn.setEnabled(False)
        self._listen_worker = VoiceListenWorker(parent=self)
        self._listen_worker.heard.connect(self._on_voice_heard)
        self._listen_worker.error.connect(self._on_voice_error)
        self._listen_worker.state_changed.connect(self._on_listening_state)
        self._listen_worker.finished.connect(lambda: self.mic_btn.setEnabled(microphone_available()))
        self._listen_worker.start()

    def _on_listening_state(self, active: bool) -> None:
        if active:
            self.mic_btn.setText("🔴")
            self._set_voice_status("Ecoute en cours...")
        else:
            self.mic_btn.setText("🎤")

    def _on_voice_error(self, msg: str) -> None:
        self._set_voice_status("")
        self._add_bubble(f"Micro : {msg}", False)

    def _on_voice_heard(self, text: str) -> None:
        self._set_voice_status(f"Entendu : {text}")
        self.input_field.setText(text)
        self._submit_text(text)

    def _on_mode_changed(self):
        key = self.mode_combo.currentData()
        if key:
            self.profile["space_ai_mode"] = key
            from core.config import save_json, PROFILE_FILE
            save_json(PROFILE_FILE, self.profile)

    def _send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return
        self.input_field.clear()
        self._submit_text(text)

    def _submit_text(self, text: str) -> None:
        self._add_bubble(text, True)
        self.input_field.setEnabled(False)
        self.mic_btn.setEnabled(False)
        self.typing_lbl.setVisible(True)
        QTimer.singleShot(500, lambda t=text: self._process_ai_response(t))

    def _add_bubble(self, text: str, is_user: bool):
        self.chat_layout.addWidget(ChatBubble(text, is_user, self.theme, self._avatar if not is_user else None))
        QTimer.singleShot(50, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    def _process_ai_response(self, user_text: str):
        self.input_field.setEnabled(True)
        self.mic_btn.setEnabled(microphone_available())
        self.typing_lbl.setVisible(False)
        self.input_field.setFocus()
        try:
            response = self.engine.process(user_text)
        except Exception as exc:
            response = f"Erreur Space AI : {exc}"

        if response.startswith("NAVIGATE:"):
            target = response.split(":", 1)[1]
            win = self.window()
            if hasattr(win, "_show_section"):
                win._show_section(target)
            self._add_bubble(f"Ouverture de l'onglet {target}.", False)
            if self._voice_enabled and tts_available():
                self._speak_response(f"Ouverture de {target}")
            return

        if self.state_setup and self.profile.get("ai_memory"):
            self.state_setup = False
        self._add_bubble(response, False)
        if self._voice_enabled and tts_available() and not response.startswith("NAVIGATE:"):
            self._speak_response(response)

        win = self.window()
        if win and hasattr(win, "status_bar_widget") and win.status_bar_widget:
            win.status_bar_widget.refresh_profile(self.profile)

    def _speak_response(self, text: str) -> None:
        if self._speak_worker and self._speak_worker.isRunning():
            self._speak_worker.request_stop()
            self._speak_worker.wait(500)
        self._set_voice_status("Space AI parle...")
        self._speak_worker = VoiceSpeakWorker(text, parent=self)
        self._speak_worker.finished_ok.connect(lambda: self._set_voice_status(""))
        self._speak_worker.error.connect(lambda m: self._set_voice_status(m))
        self._speak_worker.start()

    def _on_launch_space_ai(self) -> None:
        from PySide6.QtWidgets import QMessageBox
        ok, msg = launch_jarvis_app(detached=True)
        if ok:
            QMessageBox.information(
                self,
                "Space AI",
                "Space AI (version complète) est en cours de lancement dans une fenêtre séparée.\n"
                "Veuillez patienter..."
            )
        else:
            QMessageBox.warning(
                self,
                "Erreur de lancement",
                f"Impossible de lancer Space AI :\n{msg}\n\n"
                "Astuce : assurez-vous d'avoir lancé install.bat dans le dossier 'Space AI'."
            )

    def closeEvent(self, event):
        for worker in (self._listen_worker, self._speak_worker):
            if worker and worker.isRunning():
                worker.wait(2000)
        super().closeEvent(event)
