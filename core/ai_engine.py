"""
Space AI Engine v2.0 - Orchestrator (Facade)
Coordonne l'intent_parser, le synonym_map, la memory, la knowledge_base,
le math_solver et le chatbot_patterns.

Améliorations v2.0 :
  - Refactorisation en méthodes privées (méthode process() allégée)
  - Imports au niveau module (plus d'imports à l'intérieur des méthodes)
  - Système de quiz multi-tentatives avec indices progressifs
  - Bonus de série (streaks) et multiplicateurs de points
  - Navigation floue (fuzzy matching par Levenshtein léger)
  - Historique de conversation enrichi (5 dernières questions)
  - Statistiques de session (bonnes/mauvaises réponses, temps)
  - Logging structuré (plus de print() bruts)
  - Validation et nettoyage de l'entrée utilisateur
  - Variété de réponses (rotation des messages)
  - Meilleure détection des questions de suivi
  - Seuil de confiance RAG ajustable
  - Gestion d'erreurs explicite (pas de except: pass silencieux)
"""

import json
import logging
import random
from datetime import datetime
from typing import Optional

from core.chatbot_patterns import match_conversational_pattern
from core.config import PROFILE_FILE
from core.intent_parser import parse_intent, remove_accents
from core.knowledge_base import KnowledgeBase
from core.math_solver import safe_eval
from core.memory import SessionMemory
from core.space_ai_bridge import generate_cloud_response, is_cloud_available
from core import local_llm
from core.config import LLM_MAX_TOKENS, LLM_TIMEOUT
from core.knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes globales
# ---------------------------------------------------------------------------

PAGE_MAPPING: dict[str, str] = {
    "accueil": "dashboard", "dashboard": "dashboard", "home": "dashboard",
    "cours": "courses", "course": "courses", "lecon": "courses", "lecons": "courses",
    "note": "notes", "notes": "notes",
    "quiz": "quiz",
    "profil": "profile", "profile": "profile",
    "parametre": "settings", "parametres": "settings",
    "setting": "settings", "settings": "settings",
    "outil": "tools", "outils": "tools", "tool": "tools", "tools": "tools",
    "moyenne": "grades", "moyennes": "grades", "grade": "grades", "grades": "grades",
    "raccourci": "shortcuts", "raccourcis": "shortcuts",
    "shortcut": "shortcuts", "shortcuts": "shortcuts",
    "about": "about", "propos": "about",
    "oracle": "oracle",
    "guide": "guide",
    "hacking": "hacking", "devsecurity": "hacking",
    "security": "hacking", "securite": "hacking",
    "carriere": "career", "career": "career",
}

FOLLOW_UP_KEYWORDS: frozenset[str] = frozenset([
    "detail", "details", "plus de details", "plus d'infos", "plus d'informations",
    "explique", "en savoir plus", "developpe", "ca", "cela", "precedente",
    "encore", "continue", "suite", "resumé", "résumé", "rappelle",
])

QUIZ_CANCEL_KEYWORDS: frozenset[str] = frozenset([
    "annuler", "quitter", "stop", "exit", "abandonner", "passer",
])

# Points de base par réponse correcte
BASE_QUIZ_POINTS = 15
# Seuil minimum de similarité RAG pour accepter un résultat
RAG_SCORE_THRESHOLD = 0.15
# Nombre maximum de tentatives pour un quiz
MAX_QUIZ_ATTEMPTS = 3
# Longueur maximale d'une entrée utilisateur (caractères)
MAX_INPUT_LENGTH = 800

# Messages de succès variés pour le quiz
QUIZ_SUCCESS_MESSAGES = [
    "🎉 **Félicitations !** C'est une excellente réponse !",
    "🌟 **Bravo !** Vous avez parfaitement répondu !",
    "✅ **Exact !** Quelle maîtrise du sujet !",
    "🚀 **Parfait !** Vous êtes sur la bonne voie !",
    "💎 **Impressionnant !** Réponse parfaite !",
]

# Messages d'échec variés pour le quiz
QUIZ_FAILURE_MESSAGES = [
    "❌ Oups ! Ce n'est pas tout à fait ça.",
    "💭 Presque ! Mais il manque quelque chose.",
    "📖 Révisez encore un peu ! La réponse n'est pas celle-là.",
]

# Messages de fallback variés
FALLBACK_MESSAGES = [
    "Je n'ai pas trouvé de cours exact pour votre question. Essayez des mots-clés plus précis (ex: 'Von Neumann', 'HTML', 'Algorithme').",
    "Aucune leçon correspondante dans ma base. Reformulez ou utilisez un terme du cours (ex: 'pointeur', 'réseau', 'protocole').",
    "Je ne reconnais pas ce sujet dans ma base de connaissances. Essayez un mot-clé du cours ou tapez 'cours' pour voir les matières disponibles.",
]

# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def _levenshtein(a: str, b: str) -> int:
    """Distance de Levenshtein entre deux chaînes (pour la navigation floue)."""
    if len(a) < len(b):
        return _levenshtein(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = curr
    return prev[-1]


def _fuzzy_page_lookup(text_clean: str, threshold: int = 2) -> Optional[str]:
    """
    Recherche floue dans PAGE_MAPPING.
    Retourne la page cible si un mot du texte est proche d'une cle connue.
    """
    words = text_clean.split()
    for word in words:
        if len(word) < 3:
            continue
        best_key, best_dist = None, threshold + 1
        for key in PAGE_MAPPING:
            d = _levenshtein(word, key)
            if d < best_dist:
                best_dist, best_key = d, key
        if best_key and best_dist <= threshold:
            return PAGE_MAPPING[best_key]
    return None


def _keyword_match_ratio(user_tokens: set[str], correct_tokens: set[str]) -> float:
    """Ratio de correspondance entre les tokens utilisateur et les tokens de la réponse correcte."""
    significant = {t for t in correct_tokens if len(t) > 2}
    if not significant:
        return 1.0
    return len(user_tokens.intersection(significant)) / len(significant)

    


# ---------------------------------------------------------------------------
# Classe principale
# ---------------------------------------------------------------------------

class AiEngine:
    """
    Orchestrateur du moteur IA Space.

    Paramètres
    ----------
    profile : dict
        Profil utilisateur chargé depuis le fichier JSON.
    user_id : int
        Identifiant de l'utilisateur (pour la base SQLite).
    """

    def __init__(self, profile: dict, user_id: int = 1) -> None:
        self.profile = profile
        self.user_id = user_id
        self.memory = SessionMemory()
        self.kb = KnowledgeBase()
        # Statistiques de session
        self._session_correct = 0
        self._session_wrong = 0
        self._streak = 0

    # -----------------------------------------------------------------------
    # Point d'entrée public
    # -----------------------------------------------------------------------

    def process(self, user_text: str) -> str:
        """
        Traite le texte de l'utilisateur et retourne la réponse de l'IA.
        Les étapes sont clairement séparées en méthodes privées.
        """
        # Validation de l'entrée
        user_text = self._sanitize_input(user_text)
        if not user_text:
            return "Je n'ai pas compris votre message. Pouvez-vous reformuler ?"

        text_lower = user_text.lower()
        text_clean = remove_accents(text_lower)

        # 1. Premier lancement : configuration de la mémoire IA
        if not self.profile.get("ai_memory"):
            res = self._handle_first_config(user_text)

        # 2. Quiz actif : traiter la réponse de l'étudiant
        elif self.memory.get_context("quiz_active") == "True":
            res = self._handle_quiz_response(user_text, text_clean)

        # 3. Demande d'accès à la mémoire
        elif any(w in text_clean for w in ["qui suis", "souviens", "connais", "memoire", "rappelle toi"]):
            res = self._recall_memory()

        # 4. Déclenchement explicite d'un quiz
        elif any(w in text_clean for w in {"quiz", "test-moi", "test moi", "evalue moi", "evalue-moi",
                                          "exercice", "exercices", "question", "interroge moi", "interroge-moi"}):
            res = self._trigger_quiz()

        # 5. Statistiques de session
        elif any(w in text_clean for w in ["stats", "statistiques", "score", "progression", "mes points"]):
            res = self._show_session_stats()

        # 6. Analyse de l'intention et dispatch
        else:
            intent, tokens = parse_intent(user_text)
            self.memory.add_question(user_text)

            if intent == "GREETING":
                res = self._handle_greeting()
            elif intent == "TIME":
                res = self._handle_time()
            elif intent == "MATHS" and tokens:
                res = self._handle_math(tokens[0])
            elif intent == "NAVIGATE":
                res = self._handle_navigate(tokens, text_clean)
            else:
                res = self._handle_knowledge(user_text, text_clean, tokens)

        if isinstance(res, str):
            res = res.replace("**", "")
        return res

    # -----------------------------------------------------------------------
    # Méthodes privées — Étapes du pipeline
    # -----------------------------------------------------------------------

    def _sanitize_input(self, text: str) -> str:
        """Nettoie et valide l'entrée utilisateur."""
        text = text.strip()
        if len(text) > MAX_INPUT_LENGTH:
            text = text[:MAX_INPUT_LENGTH]
            logger.warning("Entrée tronquée à %d caractères.", MAX_INPUT_LENGTH)
        return text

    def _handle_first_config(self, user_text: str) -> str:
        """Enregistre la première configuration mémorielle de l'utilisateur."""
        self.profile["ai_memory"] = user_text
        self._save_profile()
        nom = self.profile.get("nom", "")
        intro = f"Bonjour {nom} ! " if nom else ""
        return (
            f"{intro}C'est noté ! J'ai enregistré votre profil dans ma mémoire permanente. 🧠\n\n"
            "Vous pouvez maintenant me poser des questions sur vos cours (ex: 'algorithme', 'html', 'Von Neumann').\n"
            "Tapez 'quiz' pour vous entraîner, ou **'stats' pour voir votre progression !"
        )

    def _handle_quiz_response(self, user_text: str, text_clean: str) -> str:
        """Gère la réponse d'un étudiant à une question de quiz (multi-tentatives)."""
        # Annulation
        if any(w in text_clean for w in QUIZ_CANCEL_KEYWORDS):
            self._reset_quiz()
            return "Le quiz a été annulé. Tapez 'quiz' quand vous serez prêt à recommencer ! 👍"

        correct_ans: str = self.memory.get_context("quiz_answer") or ""
        attempts: int = int(self.memory.get_context("quiz_attempts") or "0")
        attempts += 1
        self.memory.update_context("quiz_attempts", str(attempts))

        user_tokens = set(parse_intent(text_clean)[1])
        correct_tokens = set(parse_intent(remove_accents(correct_ans.lower()))[1])
        ratio = _keyword_match_ratio(user_tokens, correct_tokens)
        is_correct = ratio >= 0.4

        if is_correct:
            return self._quiz_success(correct_ans, attempts)

        # Mauvaise réponse — donner des indices progressifs
        if attempts < MAX_QUIZ_ATTEMPTS:
            return self._quiz_hint(correct_ans, attempts)
        else:
            return self._quiz_failure(user_text, correct_ans)

    def _quiz_success(self, correct_ans: str, attempts: int) -> str:
        """Récompense une bonne réponse avec bonus de série."""
        self._streak += 1
        self._session_correct += 1

        # Calcul des points avec multiplicateur de série
        multiplier = min(1 + (self._streak - 1) * 0.25, 2.5)  # max x2.5
        points_earned = int(BASE_QUIZ_POINTS * multiplier)

        self.profile["points"] = self.profile.get("points", 0) + points_earned
        self._save_profile()
        self._log_xp(points_earned)
        self._reset_quiz()

        streak_msg = ""
        if self._streak >= 3:
            streak_msg = f"\n🔥 Série de {self._streak} bonnes réponses ! (x{multiplier:.1f} bonus actif)"

        attempt_msg = ""
        if attempts > 1:
            attempt_msg = f"\n(Obtenu en {attempts} tentatives)"

        return (
            f"{random.choice(QUIZ_SUCCESS_MESSAGES)}\n\n"
            f"La réponse attendue était :\n{correct_ans}\n\n"
            f"⭐ Vous gagnez +{points_earned} points !"
            f"{streak_msg}{attempt_msg}\n"
            f"(Total : {self.profile.get('points', 0)} pts)"
        )

    def _quiz_hint(self, correct_ans: str, attempts: int) -> str:
        """Génère un indice progressif basé sur le nombre de tentatives."""
        words = correct_ans.split()
        if attempts == 1 and len(words) > 2:
            # Indice 1 : première lettre du premier mot significatif
            hint_word = next((w for w in words if len(w) > 3), words[0])
            hint = f"Le premier mot-clé commence par '{hint_word[0].upper()}'..."
        elif len(words) > 0:
            # Indice 2 : révéler le premier mot
            hint = f"Indice : la réponse commence par '{words[0]}'..."
        else:
            hint = "Relisez attentivement la théorie de cette leçon."

        remaining = MAX_QUIZ_ATTEMPTS - attempts
        return (
            f"❌ Pas encore ! Tentative {attempts}/{MAX_QUIZ_ATTEMPTS}.\n\n"
            f"💡 Indice : {hint}\n\n"
            f"Il vous reste {remaining} tentative(s). Tapez 'annuler' pour abandonner."
        )

    def _quiz_failure(self, user_text: str, correct_ans: str) -> str:
        """Gère l'échec définitif après épuisement des tentatives."""
        self._streak = 0
        self._session_wrong += 1
        self._reset_quiz()

        return (
            f"{random.choice(QUIZ_FAILURE_MESSAGES)}\n\n"
            f"Votre réponse : {user_text}\n\n"
            f"La réponse attendue était :\n{correct_ans}\n\n"
            "Ne vous découragez pas ! Relisez la leçon et retentez le quiz. 💪\n"
            "Tapez 'quiz' pour recommencer."
        )

    def _reset_quiz(self) -> None:
        """Réinitialise l'état du quiz dans la mémoire."""
        self.memory.update_context("quiz_active", "False")
        self.memory.update_context("quiz_attempts", "0")

    def _trigger_quiz(self) -> str:
        """Lance un quiz basé sur la dernière leçon consultée."""
        last_lecon = self.memory.get_context("last_lecon_data")
        if not last_lecon:
            return (
                "Veuillez d'abord consulter un cours avant de lancer un quiz ! 📚\n"
                "Posez-moi une question comme 'qu'est-ce qu'un algorithme ?' et je vous préparerai un quiz."
            )

        exercice = last_lecon.get("exercice")
        correction = last_lecon.get("correction")
        titre = last_lecon.get("titre", "cette leçon")

        if not exercice:
            return f"Il n'y a pas d'exercice disponible pour la leçon {titre}. Consultez une autre leçon !"

        self.memory.update_context("quiz_active", "True")
        self.memory.update_context("quiz_question", exercice)
        self.memory.update_context("quiz_answer", correction)
        self.memory.update_context("quiz_attempts", "0")

        return (
            f"📝 Quiz Interactif : {titre}\n\n"
            f"Question :\n{exercice}\n\n"
            f"Vous avez {MAX_QUIZ_ATTEMPTS} tentatives. Tapez 'annuler' pour quitter. ✏️"
        )

    def _recall_memory(self) -> str:
        """Rappelle la configuration mémorielle enregistrée."""
        mem = self.profile.get("ai_memory", "Vous ne m'avez pas encore configuré.")
        nom = self.profile.get("nom", "mon ami")
        return (
            f"Bien sûr {nom} ! Lors de notre première discussion, tu m'as confié ceci :\n\n"
            f"*\"{mem}\"*\n\n"
            "Je m'en souviens parfaitement ! 😉"
        )

    def _show_session_stats(self) -> str:
        """Affiche les statistiques de la session en cours."""
        total = self._session_correct + self._session_wrong
        ratio = f"{(self._session_correct / total * 100):.0f}%" if total > 0 else "N/A"
        pts = self.profile.get("points", 0)
        return (
            f"📊 Statistiques de session\n\n"
            f"• Bonnes réponses : {self._session_correct}\n"
            f"• Mauvaises réponses : {self._session_wrong}\n"
            f"• Taux de réussite : {ratio}\n"
            f"• Série en cours : {self._streak} 🔥\n"
            f"• Points totaux : {pts} ⭐\n\n"
            f"Continuez à réviser pour améliorer votre score !"
        )

    def _handle_greeting(self) -> str:
        """Répond à un salut."""
        nom = self.profile.get("nom", "Étudiant")
        heure = datetime.now().hour
        if heure < 12:
            salutation = "Bonjour"
        elif heure < 18:
            salutation = "Bon après-midi"
        else:
            salutation = "Bonsoir"
        pts = self.profile.get("points", 0)
        return (
            f"{salutation} {nom} ! 👋 Comment puis-je vous aider aujourd'hui ?\n\n"
            f"• Posez-moi une question de cours (ex: algorithme, html, Von Neumann)\n"
            f"• Tapez 'quiz' pour vous tester\n"
            f"• Tapez 'stats' pour voir votre progression\n\n"
            f"Vous avez actuellement {pts} points ⭐"
        )

    def _handle_time(self) -> str:
        """Répond à une demande d'heure/date."""
        now = datetime.now()
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        mois = ["janvier", "février", "mars", "avril", "mai", "juin",
                "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        jour_semaine = jours[now.weekday()]
        mois_nom = mois[now.month - 1]
        return (
            f"🕒 {jour_semaine} {now.day} {mois_nom} {now.year}\n"
            f"Il est {now.strftime('%H:%M')}."
        )

    def _handle_math(self, expr: str) -> str:
        """Calcule une expression mathématique de façon sécurisée."""
        try:
            result = safe_eval(expr)
            return (
                f"🧮 Calculatrice Spatiale\n\n"
                f"Expression : `{expr}`\n"
                f"Résultat : {result}"
            )
        except Exception as e:
            logger.warning("Erreur de calcul pour l'expression '%s': %s", expr, e)
            return (
                f"⚠️ Impossible de calculer `{expr}`.\n"
                "Vérifiez la syntaxe (ex: `3 + 4 * 2`, `sqrt(16)`)."
            )

    def _handle_navigate(self, tokens: list[str], text_clean: str) -> str:
        """Résout la navigation avec correspondance exacte puis floue."""
        # 1. Correspondance exacte sur les tokens
        for token in tokens:
            if token in PAGE_MAPPING:
                return f"NAVIGATE:{PAGE_MAPPING[token]}"

        # 2. Correspondance exacte par scan du texte complet
        for key, page in PAGE_MAPPING.items():
            if key in text_clean:
                return f"NAVIGATE:{page}"

        # 3. Navigation floue (Levenshtein)
        fuzzy_page = _fuzzy_page_lookup(text_clean)
        if fuzzy_page:
            return f"NAVIGATE:{fuzzy_page}"

        return (
            "Je n'ai pas compris vers quel onglet vous souhaitez naviguer.\n"
            "Essayez : 'va sur les cours', 'ouvre les notes', 'accède au quiz'."
        )

    def _get_ai_mode(self) -> str:
        """local | cloud | hybrid — défaut intelligent selon la clé API."""
        mode = (self.profile.get("space_ai_mode") or "").strip().lower()
        if mode in ("local", "cloud", "hybrid"):
            return mode
        return "hybrid" if is_cloud_available() else "local"

    def _try_cloud_answer(self, user_text: str, tokens: list[str]) -> Optional[str]:
        """Réponse Gemini avec contexte RAG si le mode cloud/hybrid est actif."""
        mode = self._get_ai_mode()
        if mode == "local" or not is_cloud_available():
            return None

        rag_context = ""
        best_match, score = self.kb.search(tokens)
        if best_match and score >= RAG_SCORE_THRESHOLD:
            lecon = best_match["lecon"]
            rag_context = (
                f"Matière: {best_match.get('matiere', '')} | "
                f"Titre: {lecon.get('titre', '')}\n"
                f"{lecon.get('theorie', '')[:2000]}"
            )

        cloud = generate_cloud_response(user_text, self.profile, rag_context)
        if cloud:
            if best_match and score >= RAG_SCORE_THRESHOLD:
                self.memory.set_topic(best_match["lecon"].get("titre"))
                self.memory.update_context("last_lecon_data", best_match["lecon"])
            return f"🌐 Space AI (Gemini)\n\n{cloud}"
        return None if mode == "cloud" else None

    def _handle_knowledge(self, user_text: str, text_clean: str, tokens: list[str]) -> str:
        """Pipeline RAG : follow-up → patterns → cloud → TF-IDF → fallback."""

        # 6.1 Question de suivi
        is_follow_up = (
            any(w in text_clean for w in FOLLOW_UP_KEYWORDS)
            or (not tokens and self.memory.get_topic())
        )
        if is_follow_up:
            follow_up_resp = self._handle_follow_up()
            if follow_up_resp:
                return follow_up_resp

        # 6.2 Pattern matching conversationnel
        conv_response = match_conversational_pattern(user_text)
        if conv_response:
            return conv_response

        # 6.3 Fallbacks sémantiques rapides
        semantic = self._check_semantic_fallbacks(text_clean)
        if semantic:
            return semantic

        cloud_resp = self._try_cloud_answer(user_text, tokens)
        if cloud_resp:
            return cloud_resp

        mode = self._get_ai_mode()
        if mode == "cloud" and is_cloud_available():
            return (
                "⚠️ La connexion à Gemini a échoué. Passez en mode Hybride ou Local, "
                "ou ajoutez GEMINI_API_KEY dans %APPDATA%\\AstaAcademie\\space_ai.env"
            )

        # 6.4 Recherche RAG par TF-IDF
        best_match, score = self.kb.search(tokens)
        if best_match and score >= RAG_SCORE_THRESHOLD:
            return self._format_lesson_response(best_match)

        # 6.5 Fallback générique
        return random.choice(FALLBACK_MESSAGES)

    def _handle_follow_up(self) -> Optional[str]:
        """Retourne les détails de la dernière leçon consultée, si disponible."""
        last_lecon = self.memory.get_context("last_lecon_data")
        if not last_lecon:
            return None

        title = last_lecon.get("titre", "cette leçon")
        theory = last_lecon.get("theorie", "").strip()
        piege = last_lecon.get("piege_prof", "").strip()
        exemples = last_lecon.get("exemples", [])

        response = f"📚 Approfondissement : {title}\n\n{theory}"

        if exemples:
            ex_list = "\n".join([f"  → {ex}" for ex in exemples[:3]])
            response += f"\n\n🔍 Exemples :\n{ex_list}"

        if piege:
            response += f"\n\n⚠️ Piège classique à l'examen :\n{piege}"

        response += "\n\n💡 Tapez 'quiz'pour vous tester sur cette leçon et gagner des points ⭐"
        return response

    def _format_lesson_response(self, best_match: dict) -> str:
        """Formate la réponse à partir d'un résultat RAG."""
        lecon = best_match["lecon"]
        matiere = best_match["matiere"]
        niveau = best_match["niveau"]

        # Mettre à jour la mémoire
        self.memory.set_topic(lecon.get("titre"))
        self.memory.update_context("last_lecon_data", lecon)

        pts_list = "\n".join([f"• {p}" for p in lecon.get("points_cles", [])])
        theory = lecon.get("theorie", "").strip()
        piege = lecon.get("piege_prof", "").strip()
        exemples = lecon.get("exemples", [])

        # Recommandations de cours connexes
        reco = self._get_recommendations(matiere, niveau, lecon.get("titre"))
        reco_str = ""
        if reco:
            reco_str = "\n\n📖 Cours connexes suggérés :\n" + "\n".join([f"- {r}" for r in reco])

        response = (
            f"📚 {matiere} (Niveau : {niveau})\n"
            f"📌 Leçon : {lecon.get('titre')}\n\n"
            f"{theory}"
        )

        if exemples:
            ex_list = "\n".join([f"  → {ex}" for ex in exemples[:2]])
            response += f"\n\n🔍 Exemple(s) :\n{ex_list}"

        if pts_list:
            response += f"\n\n💡 Points clés à retenir :\n{pts_list}"

        if piege:
            response += f"\n\n⚠️ Question a veiller à l'examen de l'UNASMOH:\n{piege}"

        response += f"\n\n📝 Tapez **'quiz'** pour vous tester et gagner des points !*{reco_str}"
        return response

    def _get_recommendations(self, matiere: str, niveau: str, current_title: str) -> list[str]:
        """Retourne jusqu'à 2 recommandations de cours connexes."""
        reco: list[str] = []
        # Priorité : même matière
        for doc in self.kb.documents:
            if doc["matiere"] == matiere and doc["lecon"]["titre"] != current_title:
                reco.append(doc["lecon"]["titre"])
                if len(reco) >= 2:
                    return reco
        # Compléter avec le même niveau
        for doc in self.kb.documents:
            titre = doc["lecon"]["titre"]
            if doc["niveau"] == niveau and titre != current_title and titre not in reco:
                reco.append(titre)
                if len(reco) >= 2:
                    return reco
        return reco

    def _check_semantic_fallbacks(self, text_clean: str) -> Optional[str]:
        """Réponses prédéfinies pour des sujets connus sans entrée dans la KB."""
        if "unasmoh" in text_clean:
            return (
                "UNASMOH (Université Américaine des Sciences Modernes d'Haïti) "
                "est l'institution accueillant la promotion 2024-2028. 🎓"
            )
        if any(w in text_clean for w in ["asta", "createur", "space", "lucky"]):
            return (
                "J'ai été développé par Space Dev (Lucky Luke), "
                "Ingénieur en Informatique de la promotion 2024-2028 de l'UNASMOH. "
                "Il m'a créé pour aider les étudiants de l'UNASMOH à exceller et aider d'autre étudiants en Science Informatique ! 🚀"
            )
        if "spacecode" in text_clean or ("python" in text_clean and "editeur" in text_clean):
            return (
                "SpaceCode est l'éditeur de code intégré dans l'onglet Outils, il sera intégrer dans une prochaine mise a jours qui arrive prochainement. "
                "Testez vos scripts Python directement depuis l'application ! 🐍"
            )
        if any(w in text_clean for w in ["hacking", "cyber", "securite", "pentest"]):
            return (
                "Le module DevSecurity est la section cybersécurité de l'application. Il est protéger par une licence qui sera fournit par les développeur. "
                "Souvenez-vous : toujours agir de manière éthique et légale. Le créateur de Asta Academie ainsi que ses développeur seront pas résponsable de vos choix.🛡️"
                "Noublier pas : toutes les actions ilégale que vous faites sont tracable et peut avoir des lourdes conséquences. "
            )
        return None

    # -----------------------------------------------------------------------
    # Méthodes utilitaires
    # -----------------------------------------------------------------------

    def _save_profile(self) -> None:
        """Persiste le profil utilisateur sur disque de façon sécurisée."""
        try:
            with open(PROFILE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.profile, f, indent=4, ensure_ascii=False)
        except OSError as e:
            logger.error("Impossible de sauvegarder le profil (%s): %s", PROFILE_FILE, e)

    def _log_xp(self, points: int) -> None:
        """Enregistre les XP gagnés dans la base SQLite."""
        try:
            from database.db_manager import DBManager
            today_str = datetime.now().strftime("%Y-%m-%d")
            DBManager.log_xp_earned(self.user_id, today_str, points)
        except Exception as e:
            logger.warning("Impossible d'écrire les XP en base SQLite: %s", e)
