"""
Space AI — assistant vocal integre dans Asta Academie (micro + synthese).
Inspire de JARVIS, sans fenetre externe ni WebSocket.
"""
from __future__ import annotations

import re
import logging
from typing import Optional

from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)

WAKE_WORDS = ("space", "space ai", "spaceai")


def strip_for_speech(text: str) -> str:
    t = text.replace("**", "").replace("*", "").replace("#", "").replace("`", "")
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t.strip()


def speech_available() -> bool:
    try:
        import speech_recognition as sr  # noqa: F401
        return True
    except ImportError:
        return False


def tts_available() -> bool:
    try:
        import pyttsx3  # noqa: F401
        return True
    except ImportError:
        pass
    try:
        import edge_tts  # noqa: F401
        return True
    except ImportError:
        return False
    return False


def microphone_available() -> bool:
    if not speech_available():
        return False
    try:
        import speech_recognition as sr
        sr.Microphone()
        return True
    except Exception as exc:
        logger.info("Micro indisponible : %s", exc)
        return False


class VoiceListenWorker(QThread):
    """Ecoute le micro une fois (Google Speech API, francais)."""

    heard = Signal(str)
    error = Signal(str)
    state_changed = Signal(bool)

    def __init__(self, timeout: float = 10.0, phrase_limit: float = 15.0, parent=None):
        super().__init__(parent)
        self.timeout = timeout
        self.phrase_limit = phrase_limit

    def run(self) -> None:
        self.state_changed.emit(True)
        try:
            import speech_recognition as sr

            recognizer = sr.Recognizer()
            recognizer.pause_threshold = 1.0
            recognizer.dynamic_energy_threshold = True

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = recognizer.listen(
                    source,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_limit,
                )

            text = recognizer.recognize_google(audio, language="fr-FR").strip()
            if not text:
                self.error.emit("Aucune parole detectee.")
                return

            lower = text.lower()
            for wake in WAKE_WORDS:
                if lower.startswith(wake):
                    text = text[len(wake):].strip(" ,.:;-")
                    break

            self.heard.emit(text)
        except Exception as exc:
            name = type(exc).__name__
            if name == "WaitTimeoutError":
                self.error.emit("Temps ecoule — parlez apres avoir clique sur le micro.")
            elif name == "UnknownValueError":
                self.error.emit("Je n'ai pas compris. Repetez plus clairement.")
            elif "PyAudio" in str(exc) or "pyaudio" in str(exc).lower():
                self.error.emit(
                    "PyAudio manquant. Lancez : pip install pyaudio\n"
                    "(ou reparer_venv.bat puis install_asta.bat)"
                )
            else:
                self.error.emit(str(exc))
        finally:
            self.state_changed.emit(False)


class VoiceSpeakWorker(QThread):
    """Lit une reponse a voix haute (pyttsx3 ou edge-tts)."""

    finished_ok = Signal()
    error = Signal(str)

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.text = strip_for_speech(text)
        self._stop = False

    def request_stop(self) -> None:
        self._stop = True

    def run(self) -> None:
        if not self.text:
            self.finished_ok.emit()
            return
        if self._speak_edge():
            self.finished_ok.emit()
            return
        if self._speak_pyttsx3():
            self.finished_ok.emit()
            return
        self.error.emit("Synthese vocale non disponible (pyttsx3 / edge-tts).")

    def _speak_pyttsx3(self) -> bool:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty("voices") or []
            
            # Rechercher d'abord une voix française masculine
            french_male = None
            french_any = None
            for voice in voices:
                v_name = voice.name.lower()
                v_id = voice.id.lower()
                is_french = "french" in v_name or "fr" in v_id
                
                if is_french:
                    if not french_any:
                        french_any = voice.id
                    
                    # Heuristique pour détecter une voix masculine (Paul, Henri, Claude, male)
                    gender = getattr(voice, "gender", "").lower()
                    if "male" in gender or "paul" in v_name or "herv" in v_name or "claude" in v_name or "male" in v_name:
                        french_male = voice.id
                        break
            
            chosen_voice = french_male or french_any
            if chosen_voice:
                engine.setProperty("voice", chosen_voice)
                
            engine.setProperty("rate", 175)
            engine.say(self.text[:500])
            engine.runAndWait()
            return True
        except Exception as exc:
            logger.debug("pyttsx3 : %s", exc)
            return False

    def _speak_edge(self) -> bool:
        try:
            import asyncio
            import edge_tts
            import tempfile
            import os

            async def _go():
                path = os.path.join(
                    tempfile.gettempdir(),
                    f"asta_tts_{os.getpid()}.mp3",
                )
                comm = edge_tts.Communicate(self.text[:500], voice="fr-FR-HenriNeural")
                await comm.save(path)
                try:
                    # Utiliser MCI (Media Control Interface) natif de Windows pour une lecture silencieuse en arriere-plan
                    import ctypes
                    path_w = os.path.normpath(path)
                    ctypes.windll.winmm.mciSendStringW(f'open "{path_w}" type mpegvideo alias mp3', None, 0, 0)
                    ctypes.windll.winmm.mciSendStringW('play mp3', None, 0, 0)
                    
                    while not self._stop:
                        status = ctypes.create_unicode_buffer(128)
                        ctypes.windll.winmm.mciSendStringW('status mp3 mode', status, 128, 0)
                        if status.value != 'playing':
                            break
                        await asyncio.sleep(0.1)
                        
                    ctypes.windll.winmm.mciSendStringW('stop mp3', None, 0, 0)
                    ctypes.windll.winmm.mciSendStringW('close mp3', None, 0, 0)
                except Exception as e:
                    logger.debug("MCI Error, trying Pygame fallback: %s", e)
                    try:
                        import pygame
                        pygame.mixer.init()
                        pygame.mixer.music.load(path)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy() and not self._stop:
                            await asyncio.sleep(0.1)
                        pygame.mixer.music.stop()
                    except Exception:
                        pass
                finally:
                    try:
                        os.remove(path)
                    except OSError:
                        pass

            asyncio.run(_go())
            return True
        except Exception as exc:
            logger.debug("edge-tts : %s", exc)
            return False
