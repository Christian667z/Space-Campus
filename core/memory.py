"""
Space AI Engine - Memory Module v2.0
======================================
Système de mémoire à deux niveaux pour Asta Académie :

  • SessionMemory   — Mémoire de session (RAM, rapide, volatile).
                      Compatible 100 % avec le code existant (même API).

  • LongTermMemory  — Mémoire persistante (fichier JSON sur disque).
                      Survit aux redémarrages de l'application.
                      Stocke : historique des conversations, leçons consultées,
                      résultats des quiz, sujets favoris, préférences utilisateur.

  • MemoryManager   — Façade unifiée. Utilisez cette classe dans AiEngine
                      à la place de SessionMemory pour bénéficier des deux niveaux.

Améliorations v2.0 :
  - Mémoire à long terme persistante (JSON structuré)
  - Historique complet des conversations horodatées
  - Tracking de fréquence des sujets (sujets favoris)
  - Historique détaillé des quiz (résultats, tentatives, points gagnés)
  - Leçons consultées avec timestamps
  - Recherche dans l'historique (fulltext)
  - Résumé de session et statistiques globales
  - Nettoyage automatique (rotation des entrées trop anciennes)
  - Thread-safe (verrou par fichier)
  - Migrations de schéma (ajout de nouveaux champs sans casser l'existant)
  - Logging structuré
  - Type hints complets
"""

import json
import logging
import os
import threading
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Taille maximale des historiques (pour éviter une croissance infinie)
MAX_SESSION_QUESTIONS     = 10     # questions en mémoire de session
MAX_LT_CONVERSATIONS      = 500   # entrées dans l'historique long terme
MAX_LT_QUIZ_HISTORY       = 200   # résultats de quiz en long terme
MAX_LT_LESSONS_VISITED    = 300   # leçons visitées en long terme
MAX_SEARCH_RESULTS        = 20    # résultats de recherche dans l'historique

# Version du schéma JSON (pour les migrations futures)
SCHEMA_VERSION = 2


# ===========================================================================
# 1. MÉMOIRE DE SESSION (RAM, volatile)
# ===========================================================================

class SessionMemory:
    """
    Mémoire volatile pour la session en cours.
    Conserve les dernières questions, le sujet actif et le contexte du quiz.

    Interface identique à la v1 → aucun changement requis dans le code appelant.
    """

    def __init__(self) -> None:
        self._questions: List[str] = []
        self._topic: Optional[str] = None
        self._context: Dict[str, Any] = {}

    # --- Questions -----------------------------------------------------------

    def add_question(self, question: str) -> None:
        """Ajoute une question à l'historique (rotation automatique)."""
        question = question.strip()
        if question:
            self._questions.append(question)
            if len(self._questions) > MAX_SESSION_QUESTIONS:
                self._questions.pop(0)

    def get_questions(self) -> List[str]:
        """Retourne une copie de l'historique des questions de la session."""
        return list(self._questions)

    def get_last_question(self) -> Optional[str]:
        """Retourne la dernière question posée."""
        return self._questions[-1] if self._questions else None

    # --- Sujet actif ---------------------------------------------------------

    def set_topic(self, topic: str) -> None:
        self._topic = topic.strip() if topic else None

    def get_topic(self) -> Optional[str]:
        return self._topic

    def clear_topic(self) -> None:
        self._topic = None

    # --- Contexte clé/valeur (quiz, état, etc.) ------------------------------

    def update_context(self, key: str, value: Any) -> None:
        self._context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        return self._context.get(key, default)

    def delete_context(self, key: str) -> None:
        self._context.pop(key, None)

    def get_all_context(self) -> Dict[str, Any]:
        return dict(self._context)

    # --- Reset ---------------------------------------------------------------

    def clear(self) -> None:
        """Réinitialise complètement la mémoire de session."""
        self._questions.clear()
        self._topic = None
        self._context.clear()

    def __repr__(self) -> str:
        return (
            f"<SessionMemory topic={self._topic!r} "
            f"questions={len(self._questions)} "
            f"context_keys={list(self._context.keys())}>"
        )


# ===========================================================================
# 2. MÉMOIRE LONG TERME (JSON, persistante)
# ===========================================================================

class LongTermMemory:
    """
    Mémoire persistante sauvegardée sur disque au format JSON.

    Structure du fichier JSON :
    {
        "schema_version": 2,
        "user_id": 1,
        "created_at": "2024-01-01T00:00:00",
        "last_seen": "2024-01-15T10:30:00",
        "session_count": 42,
        "preferences": { ... },
        "conversations": [
            { "ts": "...", "question": "...", "intent": "...", "topic": "..." }
        ],
        "lessons_visited": [
            { "ts": "...", "matiere": "...", "titre": "...", "niveau": "..." }
        ],
        "quiz_history": [
            { "ts": "...", "lecon": "...", "correct": true, "attempts": 1, "points": 15 }
        ],
        "topic_frequency": { "Von Neumann": 5, "Algorithme": 3, ... },
        "notes": [ { "ts": "...", "content": "..." } ]
    }
    """

    def __init__(self, filepath: str, user_id: int = 1) -> None:
        self._path = Path(filepath)
        self._user_id = user_id
        self._lock = threading.Lock()
        self._data: Dict[str, Any] = {}
        self._load()

    # -----------------------------------------------------------------------
    # Chargement / Sauvegarde
    # -----------------------------------------------------------------------

    def _default_data(self) -> Dict[str, Any]:
        """Retourne la structure JSON vide par défaut."""
        now = self._now()
        return {
            "schema_version": SCHEMA_VERSION,
            "user_id": self._user_id,
            "created_at": now,
            "last_seen": now,
            "session_count": 0,
            "preferences": {},
            "conversations": [],
            "lessons_visited": [],
            "quiz_history": [],
            "topic_frequency": {},
            "notes": [],
        }

    def _load(self) -> None:
        """Charge le fichier JSON, le crée s'il n'existe pas."""
        with self._lock:
            if self._path.exists():
                try:
                    with open(self._path, "r", encoding="utf-8") as f:
                        raw = json.load(f)
                    self._data = self._migrate(raw)
                    logger.info(
                        "Mémoire long terme chargée depuis '%s' (%d conversations, %d quiz).",
                        self._path,
                        len(self._data.get("conversations", [])),
                        len(self._data.get("quiz_history", [])),
                    )
                except (json.JSONDecodeError, OSError) as e:
                    logger.error("Erreur de chargement de la mémoire LT (%s) : %s", self._path, e)
                    self._data = self._default_data()
            else:
                self._data = self._default_data()
                self._path.parent.mkdir(parents=True, exist_ok=True)
                self._persist_unsafe()
                logger.info("Nouvelle mémoire long terme créée : '%s'", self._path)

    def _migrate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migre les données d'un schéma plus ancien vers la version actuelle.
        Garantit que tous les champs requis existent.
        """
        defaults = self._default_data()
        for key, default_val in defaults.items():
            if key not in raw:
                raw[key] = default_val
                logger.debug("Migration : champ '%s' ajouté avec valeur par défaut.", key)
        raw["schema_version"] = SCHEMA_VERSION
        return raw

    def _persist_unsafe(self) -> None:
        """Sauvegarde sur disque SANS verrou (doit être appelée sous lock)."""
        try:
            tmp = self._path.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            tmp.replace(self._path)
        except OSError as e:
            logger.error("Impossible de sauvegarder la mémoire LT : %s", e)

    def save(self) -> None:
        """Sauvegarde thread-safe sur disque."""
        with self._lock:
            self._data["last_seen"] = self._now()
            self._persist_unsafe()

    @staticmethod
    def _now() -> str:
        return datetime.now().isoformat(timespec="seconds")

    # -----------------------------------------------------------------------
    # Session
    # -----------------------------------------------------------------------

    def start_session(self) -> None:
        """À appeler au démarrage d'une nouvelle session utilisateur."""
        with self._lock:
            self._data["session_count"] = self._data.get("session_count", 0) + 1
            self._data["last_seen"] = self._now()
            self._persist_unsafe()
        logger.info(
            "Session #%d démarrée (user_id=%d).",
            self._data["session_count"],
            self._user_id,
        )

    def get_session_count(self) -> int:
        return self._data.get("session_count", 0)

    def get_last_seen(self) -> Optional[str]:
        return self._data.get("last_seen")

    def get_created_at(self) -> Optional[str]:
        return self._data.get("created_at")

    # -----------------------------------------------------------------------
    # Conversations
    # -----------------------------------------------------------------------

    def log_conversation(
        self,
        question: str,
        intent: str = "UNKNOWN",
        topic: Optional[str] = None,
    ) -> None:
        """Enregistre une question dans l'historique long terme."""
        entry = {
            "ts": self._now(),
            "question": question[:500],  # tronquer les très longues questions
            "intent": intent,
            "topic": topic,
        }
        with self._lock:
            convs: List = self._data.setdefault("conversations", [])
            convs.append(entry)
            # Rotation : garder seulement les N plus récentes
            if len(convs) > MAX_LT_CONVERSATIONS:
                self._data["conversations"] = convs[-MAX_LT_CONVERSATIONS:]
            self._persist_unsafe()

    def get_conversation_history(self, limit: int = 20) -> List[Dict]:
        """Retourne les `limit` dernières conversations (les plus récentes en tête)."""
        convs = self._data.get("conversations", [])
        return list(reversed(convs[-limit:]))

    def search_history(self, query: str, limit: int = MAX_SEARCH_RESULTS) -> List[Dict]:
        """
        Recherche fulltext dans l'historique des conversations.
        Retourne les entrées dont la question contient le terme (insensible à la casse).
        """
        from core.intent_parser import remove_accents  # import local pour éviter les dépendances circulaires
        query_clean = remove_accents(query.lower().strip())
        results = []
        for entry in reversed(self._data.get("conversations", [])):
            q_clean = remove_accents(entry.get("question", "").lower())
            if query_clean in q_clean:
                results.append(entry)
                if len(results) >= limit:
                    break
        return results

    # -----------------------------------------------------------------------
    # Leçons visitées
    # -----------------------------------------------------------------------

    def log_lesson_visit(
        self,
        titre: str,
        matiere: str = "",
        niveau: str = "",
    ) -> None:
        """Enregistre la consultation d'une leçon."""
        entry = {
            "ts": self._now(),
            "titre": titre,
            "matiere": matiere,
            "niveau": niveau,
        }
        with self._lock:
            visited: List = self._data.setdefault("lessons_visited", [])
            visited.append(entry)
            if len(visited) > MAX_LT_LESSONS_VISITED:
                self._data["lessons_visited"] = visited[-MAX_LT_LESSONS_VISITED:]

            # Incrémenter la fréquence du sujet
            freq: Dict = self._data.setdefault("topic_frequency", {})
            freq[titre] = freq.get(titre, 0) + 1

            self._persist_unsafe()

    def get_lessons_visited(self, limit: int = 20) -> List[Dict]:
        """Retourne les `limit` dernières leçons visitées."""
        visited = self._data.get("lessons_visited", [])
        return list(reversed(visited[-limit:]))

    def get_favorite_topics(self, top_n: int = 5) -> List[Tuple[str, int]]:
        """
        Retourne les N sujets les plus souvent consultés.
        Format : [(titre, count), ...]
        """
        freq = self._data.get("topic_frequency", {})
        return Counter(freq).most_common(top_n)

    def was_lesson_visited(self, titre: str) -> bool:
        """Retourne True si la leçon a déjà été consultée au moins une fois."""
        freq = self._data.get("topic_frequency", {})
        return freq.get(titre, 0) > 0

    def get_lesson_visit_count(self, titre: str) -> int:
        """Retourne le nombre de fois que la leçon a été consultée."""
        return self._data.get("topic_frequency", {}).get(titre, 0)

    # -----------------------------------------------------------------------
    # Historique des quiz
    # -----------------------------------------------------------------------

    def log_quiz_result(
        self,
        lecon: str,
        correct: bool,
        attempts: int = 1,
        points: int = 0,
    ) -> None:
        """Enregistre le résultat d'un quiz."""
        entry = {
            "ts": self._now(),
            "lecon": lecon,
            "correct": correct,
            "attempts": attempts,
            "points": points,
        }
        with self._lock:
            history: List = self._data.setdefault("quiz_history", [])
            history.append(entry)
            if len(history) > MAX_LT_QUIZ_HISTORY:
                self._data["quiz_history"] = history[-MAX_LT_QUIZ_HISTORY:]
            self._persist_unsafe()

    def get_quiz_history(self, limit: int = 20) -> List[Dict]:
        """Retourne les `limit` derniers résultats de quiz."""
        history = self._data.get("quiz_history", [])
        return list(reversed(history[-limit:]))

    def get_quiz_stats(self) -> Dict[str, Any]:
        """
        Calcule les statistiques globales des quiz.

        Retour
        ------
        {
            "total": int,
            "correct": int,
            "wrong": int,
            "success_rate": float,   # 0.0 à 1.0
            "total_points": int,
            "avg_attempts": float,
            "best_lecon": str | None,   # leçon avec le + de bonnes réponses
            "worst_lecon": str | None,  # leçon avec le + de mauvaises réponses
        }
        """
        history = self._data.get("quiz_history", [])
        if not history:
            return {
                "total": 0, "correct": 0, "wrong": 0,
                "success_rate": 0.0, "total_points": 0,
                "avg_attempts": 0.0, "best_lecon": None, "worst_lecon": None,
            }

        total   = len(history)
        correct = sum(1 for e in history if e.get("correct"))
        wrong   = total - correct
        total_points = sum(e.get("points", 0) for e in history)
        avg_attempts = sum(e.get("attempts", 1) for e in history) / total

        # Meilleure et pire leçon
        lecon_correct: Counter = Counter()
        lecon_wrong:   Counter = Counter()
        for e in history:
            lecon = e.get("lecon", "?")
            if e.get("correct"):
                lecon_correct[lecon] += 1
            else:
                lecon_wrong[lecon] += 1

        best_lecon  = lecon_correct.most_common(1)[0][0] if lecon_correct else None
        worst_lecon = lecon_wrong.most_common(1)[0][0]   if lecon_wrong   else None

        return {
            "total": total,
            "correct": correct,
            "wrong": wrong,
            "success_rate": correct / total,
            "total_points": total_points,
            "avg_attempts": round(avg_attempts, 2),
            "best_lecon": best_lecon,
            "worst_lecon": worst_lecon,
        }

    # -----------------------------------------------------------------------
    # Préférences utilisateur
    # -----------------------------------------------------------------------

    def set_preference(self, key: str, value: Any) -> None:
        """Sauvegarde une préférence utilisateur persistante."""
        with self._lock:
            self._data.setdefault("preferences", {})[key] = value
            self._persist_unsafe()

    def get_preference(self, key: str, default: Any = None) -> Any:
        return self._data.get("preferences", {}).get(key, default)

    def get_all_preferences(self) -> Dict[str, Any]:
        return dict(self._data.get("preferences", {}))

    # -----------------------------------------------------------------------
    # Notes personnelles
    # -----------------------------------------------------------------------

    def add_note(self, content: str) -> None:
        """Ajoute une note personnelle horodatée."""
        if not content.strip():
            return
        with self._lock:
            notes: List = self._data.setdefault("notes", [])
            notes.append({"ts": self._now(), "content": content[:1000]})
            self._persist_unsafe()

    def get_notes(self, limit: int = 10) -> List[Dict]:
        """Retourne les `limit` dernières notes."""
        notes = self._data.get("notes", [])
        return list(reversed(notes[-limit:]))

    def delete_note(self, index: int) -> bool:
        """Supprime la note à l'index donné (0 = la plus récente). Retourne True si succès."""
        with self._lock:
            notes = self._data.get("notes", [])
            reversed_idx = len(notes) - 1 - index
            if 0 <= reversed_idx < len(notes):
                notes.pop(reversed_idx)
                self._persist_unsafe()
                return True
        return False

    # -----------------------------------------------------------------------
    # Rapport global
    # -----------------------------------------------------------------------

    def get_global_report(self) -> Dict[str, Any]:
        """
        Retourne un rapport complet sur l'utilisation de l'application.
        Utile pour afficher un tableau de bord de progression.
        """
        quiz_stats = self.get_quiz_stats()
        favorites  = self.get_favorite_topics(5)

        return {
            "user_id":          self._user_id,
            "created_at":       self.get_created_at(),
            "last_seen":        self.get_last_seen(),
            "session_count":    self.get_session_count(),
            "conversations_total": len(self._data.get("conversations", [])),
            "lessons_visited_total": len(self._data.get("lessons_visited", [])),
            "favorite_topics":  [{"topic": t, "count": c} for t, c in favorites],
            "quiz":             quiz_stats,
            "notes_count":      len(self._data.get("notes", [])),
        }

    # -----------------------------------------------------------------------
    # Nettoyage / Archivage
    # -----------------------------------------------------------------------

    def purge_old_entries(self, days: int = 90) -> int:
        """
        Supprime les conversations et résultats de quiz plus anciens que `days` jours.
        Retourne le nombre d'entrées supprimées.
        """
        cutoff = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
        removed = 0
        with self._lock:
            for key in ("conversations", "quiz_history", "lessons_visited"):
                before = len(self._data.get(key, []))
                self._data[key] = [
                    e for e in self._data.get(key, [])
                    if e.get("ts", "9999") >= cutoff
                ]
                removed += before - len(self._data[key])
            if removed:
                self._persist_unsafe()
        logger.info("Nettoyage mémoire LT : %d entrées supprimées (> %d jours).", removed, days)
        return removed

    def export_json(self) -> str:
        """Retourne la mémoire complète sérialisée en JSON (pour backup/export)."""
        with self._lock:
            return json.dumps(self._data, indent=2, ensure_ascii=False)

    def reset(self, confirm: bool = False) -> None:
        """
        Efface TOUTE la mémoire long terme.
        Nécessite `confirm=True` pour éviter les suppressions accidentelles.
        """
        if not confirm:
            raise ValueError(
                "Appelez reset(confirm=True) pour confirmer la suppression complète."
            )
        with self._lock:
            self._data = self._default_data()
            self._persist_unsafe()
        logger.warning("Mémoire long terme réinitialisée pour user_id=%d.", self._user_id)

    def __repr__(self) -> str:
        return (
            f"<LongTermMemory path={self._path} "
            f"sessions={self.get_session_count()} "
            f"conversations={len(self._data.get('conversations', []))} "
            f"quiz={len(self._data.get('quiz_history', []))}>"
        )


# ===========================================================================
# 3. MEMORY MANAGER — Façade unifiée
# ===========================================================================

class MemoryManager:
    """
    Façade unifiée combinant SessionMemory (RAM) et LongTermMemory (disque).

    Usage recommandé dans AiEngine :
    ---------------------------------
        from core.memory import MemoryManager

        class AiEngine:
            def __init__(self, profile, user_id=1):
                self.memory = MemoryManager(user_id=user_id)
                self.memory.start_session()

    Interface SessionMemory (rétrocompatibilité totale) :
    -------------------------------------------------
        memory.add_question(q)
        memory.get_topic() / set_topic(t)
        memory.update_context(k, v) / get_context(k)
        memory.clear()

    Interface LongTermMemory (nouvelles fonctionnalités) :
    -------------------------------------------------------
        memory.lt.log_conversation(q, intent, topic)
        memory.lt.log_lesson_visit(titre, matiere, niveau)
        memory.lt.log_quiz_result(lecon, correct, attempts, points)
        memory.lt.get_favorite_topics()
        memory.lt.get_quiz_stats()
        memory.lt.get_global_report()
        memory.lt.search_history(query)
        memory.lt.add_note(content)
        memory.summary()  # rapport textuel formaté
    """

    def __init__(
        self,
        user_id: int = 1,
        lt_filepath: Optional[str] = None,
    ) -> None:
        # Chemin du fichier par défaut : data/memory_<user_id>.json
        if lt_filepath is None:
            lt_filepath = os.path.join(
                os.path.dirname(__file__), "..", "data", f"memory_{user_id}.json"
            )

        self._session = SessionMemory()
        self.lt = LongTermMemory(filepath=lt_filepath, user_id=user_id)

    # -----------------------------------------------------------------------
    # Délégation vers SessionMemory (interface rétrocompatible)
    # -----------------------------------------------------------------------

    def start_session(self) -> None:
        """À appeler une fois au démarrage de l'AiEngine."""
        self.lt.start_session()

    def add_question(self, question: str) -> None:
        self._session.add_question(question)

    def get_questions(self) -> List[str]:
        return self._session.get_questions()

    def get_last_question(self) -> Optional[str]:
        return self._session.get_last_question()

    def set_topic(self, topic: str) -> None:
        self._session.set_topic(topic)

    def get_topic(self) -> Optional[str]:
        return self._session.get_topic()

    def clear_topic(self) -> None:
        self._session.clear_topic()

    def update_context(self, key: str, value: Any) -> None:
        self._session.update_context(key, value)

    def get_context(self, key: str, default: Any = None) -> Any:
        return self._session.get_context(key, default)

    def delete_context(self, key: str) -> None:
        self._session.delete_context(key)

    def clear(self) -> None:
        """Efface la mémoire de session (la mémoire long terme est conservée)."""
        self._session.clear()

    # -----------------------------------------------------------------------
    # Méthodes enrichies (combinent les deux niveaux)
    # -----------------------------------------------------------------------

    def log_interaction(
        self,
        question: str,
        intent: str = "UNKNOWN",
        topic: Optional[str] = None,
    ) -> None:
        """
        Enregistre une interaction dans les deux mémoires.
        Remplace `add_question()` dans le code amélioré pour un tracking complet.
        """
        self._session.add_question(question)
        self.lt.log_conversation(question, intent=intent, topic=topic)

    def log_lesson(self, lecon_data: Dict[str, Any]) -> None:
        """
        Enregistre une leçon consultée dans la mémoire long terme.
        Appeler après chaque résultat RAG positif.
        """
        titre   = lecon_data.get("titre", "")
        matiere = lecon_data.get("matiere", "")
        niveau  = lecon_data.get("niveau", "")
        if titre:
            self.lt.log_lesson_visit(titre, matiere, niveau)

    def log_quiz(self, lecon: str, correct: bool, attempts: int, points: int) -> None:
        """Enregistre un résultat de quiz dans la mémoire long terme."""
        self.lt.log_quiz_result(lecon, correct=correct, attempts=attempts, points=points)

    def recommend_revision(self, top_n: int = 3) -> List[str]:
        """
        Suggère les leçons à réviser en priorité, basé sur :
        1. Les leçons avec le plus de mauvaises réponses au quiz
        2. Les leçons consultées le plus souvent (indice de difficulté perçue)

        Retour
        ------
        Liste de titres de leçons à réviser (max `top_n`).
        """
        history = self.lt.get_quiz_history(limit=MAX_LT_QUIZ_HISTORY)
        wrong_counter: Counter = Counter()
        for entry in history:
            if not entry.get("correct"):
                wrong_counter[entry.get("lecon", "?")] += 1

        # Priorité aux leçons les plus souvent ratées
        recommendations = [lecon for lecon, _ in wrong_counter.most_common(top_n)]

        # Compléter avec les leçons fréquemment consultées si nécessaire
        if len(recommendations) < top_n:
            for titre, _ in self.lt.get_favorite_topics(top_n * 2):
                if titre not in recommendations:
                    recommendations.append(titre)
                if len(recommendations) >= top_n:
                    break

        return recommendations[:top_n]

    def get_welcome_back_message(self) -> Optional[str]:
        """
        Génère un message de bienvenue personnalisé basé sur la mémoire long terme.
        Retourne None si c'est la première session.
        """
        count = self.lt.get_session_count()
        if count <= 1:
            return None

        last_seen_str = self.lt.get_last_seen()
        favorites     = self.lt.get_favorite_topics(3)
        quiz_stats    = self.lt.get_quiz_stats()
        revisions     = self.recommend_revision(2)

        # Calcul du temps écoulé depuis la dernière visite
        since_msg = ""
        if last_seen_str:
            try:
                last_seen_dt = datetime.fromisoformat(last_seen_str)
                delta = datetime.now() - last_seen_dt
                if delta.days >= 1:
                    since_msg = f"Il y a **{delta.days} jour(s)**"
                elif delta.seconds >= 3600:
                    since_msg = f"Il y a **{delta.seconds // 3600} heure(s)**"
                else:
                    since_msg = "Il y a quelques minutes"
            except ValueError:
                pass

        parts = [f"🎉 **Bon retour !** Vous êtes à votre **session #{count}**."]

        if since_msg:
            parts.append(f"Dernière visite : {since_msg}.")

        if favorites:
            fav_str = ", ".join(f"*{t}*" for t, _ in favorites[:2])
            parts.append(f"📚 Vos sujets favoris : {fav_str}.")

        if quiz_stats["total"] > 0:
            pct = int(quiz_stats["success_rate"] * 100)
            parts.append(
                f"📊 Score quiz global : **{pct}%** "
                f"({quiz_stats['correct']}/{quiz_stats['total']}) — "
                f"**{quiz_stats['total_points']} pts** accumulés."
            )

        if revisions:
            rev_str = ", ".join(f"*{r}*" for r in revisions)
            parts.append(f"🔁 À réviser en priorité : {rev_str}.")

        return "\n".join(parts)

    def summary(self) -> str:
        """
        Retourne un résumé textuel formaté pour l'affichage dans l'app
        (commande 'stats' ou 'mémoire').
        """
        report     = self.lt.get_global_report()
        quiz       = report["quiz"]
        favorites  = report["favorite_topics"]
        revisions  = self.recommend_revision(3)

        pct = int(quiz["success_rate"] * 100) if quiz["total"] > 0 else 0

        fav_str = "\n".join(
            [f"  {i+1}. *{t['topic']}* ({t['count']} fois)"
             for i, t in enumerate(favorites)]
        ) or "  *(aucun cours consulté)*"

        rev_str = "\n".join(
            [f"  • *{r}*" for r in revisions]
        ) or "  *(aucune révision suggérée)*"

        history_preview = self.lt.get_conversation_history(limit=3)
        hist_str = "\n".join(
            [f"  [{e['ts'][:16]}] {e['question'][:60]}..."
             if len(e['question']) > 60 else f"  [{e['ts'][:16]}] {e['question']}"
             for e in history_preview]
        ) or "  *(aucune conversation enregistrée)*"

        return (
            f"🧠 **Rapport Mémoire Complète — Asta AI**\n\n"
            f"**📅 Profil**\n"
            f"  • Sessions : **{report['session_count']}**\n"
            f"  • Première utilisation : {(report['created_at'] or '?')[:10]}\n"
            f"  • Dernière connexion : {(report['last_seen'] or '?')[:10]}\n"
            f"  • Conversations totales : {report['conversations_total']}\n"
            f"  • Leçons visitées : {report['lessons_visited_total']}\n\n"
            f"**🏆 Quiz**\n"
            f"  • Total : {quiz['total']} | ✅ {quiz['correct']} | ❌ {quiz['wrong']}\n"
            f"  • Taux de réussite : **{pct}%**\n"
            f"  • Points accumulés : **{quiz['total_points']} ⭐**\n"
            f"  • Tentatives moyennes : {quiz['avg_attempts']}\n"
            f"  • Meilleure leçon : *{quiz['best_lecon'] or 'N/A'}*\n"
            f"  • Leçon à améliorer : *{quiz['worst_lecon'] or 'N/A'}*\n\n"
            f"**📚 Sujets favoris**\n{fav_str}\n\n"
            f"**🔁 Révisions suggérées**\n{rev_str}\n\n"
            f"**🕒 Dernières questions**\n{hist_str}"
        )

    def __repr__(self) -> str:
        return f"<MemoryManager session={self._session} lt={self.lt}>"


# ===========================================================================
# Rétrocompatibilité : export de SessionMemory pour le code existant
# ===========================================================================
# Le code existant fait : from core.memory import SessionMemory
# Aucun changement nécessaire dans le code appelant si vous n'utilisez pas LT.
# Pour utiliser les deux niveaux, remplacez SessionMemory par MemoryManager.

__all__ = ["SessionMemory", "LongTermMemory", "MemoryManager"]
