"""
Space AI Engine - Knowledge Base Module
Indexation et recherche par similarité cosinus (TF-IDF léger manuel)
sur les leçons de cours de l'Asta Académie.
"""
import math
from lessons.cours_data import PROGRAMME_COMPLET
from core.intent_parser import tokenize, STOP_WORDS, remove_accents
from core.synonym_map import standardize_tokens

class KnowledgeBase:
    def __init__(self):
        self.documents = []       # Liste des documents indexés
        self.vocab = set()        # Vocabulaire global
        self.idf = {}             # Inverse Document Frequency de chaque terme
        self.doc_vectors = []     # Représentations TF-IDF de chaque document
        self.doc_lengths = []     # Norme euclidienne de chaque vecteur document (pour cosinus)
        self._build_index()

    def _build_index(self):
        """Indexation complète de tous les cours et leçons du programme."""
        raw_docs = []
        for niveau_key, niveau_data in PROGRAMME_COMPLET.items():
            cours_dict = niveau_data.get("cours", {})
            for matiere_nom, matiere_data in cours_dict.items():
                for lecon in matiere_data.get("lecons", []):
                    # Récupération des différents champs
                    titre = lecon.get("titre", "")
                    theorie = lecon.get("theorie", "")
                    points = " ".join(lecon.get("points_cles", []))
                    exercice = lecon.get("exercice", "")
                    correction = lecon.get("correction", "")
                    piege = lecon.get("piege_prof", "")
                    
                    # Construction d'un texte de recherche (avec poids supplémentaire sur le titre)
                    search_text = f"{titre} {titre} {titre} {theorie} {points} {exercice} {correction} {piege}"
                    
                    # Nettoyage et tokenisation
                    raw_tokens = tokenize(search_text)
                    tokens = [t for t in raw_tokens if t not in STOP_WORDS and len(t) > 1]
                    tokens = standardize_tokens(tokens)
                    
                    doc_entry = {
                        "niveau": niveau_key,
                        "matiere": matiere_nom,
                        "lecon": lecon,
                        "tokens": tokens,
                    }
                    raw_docs.append(doc_entry)
                    
        self.documents = raw_docs
        num_docs = len(self.documents)
        if num_docs == 0:
            return

        # 1. Calcul du Document Frequency (DF)
        df = {}
        for doc in self.documents:
            unique_terms = set(doc["tokens"])
            for term in unique_terms:
                df[term] = df.get(term, 0) + 1
                
        # 2. Calcul du IDF
        for term, count in df.items():
            self.idf[term] = math.log(1.0 + (num_docs / (1.0 + count)))
            
        # 3. Calcul des vecteurs TF-IDF pour chaque document
        for doc in self.documents:
            tf = {}
            for term in doc["tokens"]:
                tf[term] = tf.get(term, 0) + 1
                
            tf_idf = {}
            vector_sum_sq = 0.0
            for term, count in tf.items():
                val = count * self.idf.get(term, 0.0)
                tf_idf[term] = val
                vector_sum_sq += val ** 2
                
            self.doc_vectors.append(tf_idf)
            self.doc_lengths.append(math.sqrt(vector_sum_sq))

    def search(self, query_tokens: list, threshold: float = 0.05) -> tuple:
        """Recherche la leçon la plus pertinente avec la similarité cosinus."""
        if not self.documents or not query_tokens:
            return None, 0.0
            
        # 1. Calcul du vecteur TF-IDF de la requête
        query_tf = {}
        for term in query_tokens:
            query_tf[term] = query_tf.get(term, 0) + 1
            
        query_tf_idf = {}
        query_sum_sq = 0.0
        for term, count in query_tf.items():
            if term in self.idf:
                val = count * self.idf[term]
                query_tf_idf[term] = val
                query_sum_sq += val ** 2
                
        query_len = math.sqrt(query_sum_sq)
        
        best_doc_idx = -1
        best_score = 0.0
        
        if query_len > 0.0:
            # 2. Comparaison avec les documents (Similarité Cosinus)
            for idx, doc_vector in enumerate(self.doc_vectors):
                doc_len = self.doc_lengths[idx]
                if doc_len == 0.0:
                    continue
                    
                dot_product = 0.0
                for term, val in query_tf_idf.items():
                    if term in doc_vector:
                        dot_product += val * doc_vector[term]
                        
                similarity = dot_product / (query_len * doc_len)
                
                # Bonus de pertinence si un terme de la requête est présent dans le titre de la leçon
                titre_brut = self.documents[idx]["lecon"].get("titre", "")
                title_tokens = standardize_tokens([t for t in tokenize(titre_brut) if t not in STOP_WORDS])
                title_matches = sum(1 for q in query_tokens if q in title_tokens)
                if title_matches > 0:
                    similarity += 0.15 * title_matches
                    
                if similarity > best_score:
                    best_score = similarity
                    best_doc_idx = idx

        # 3. Recherche directe par mot-clé dans les titres des leçons comme fallback de secours
        if best_score < 0.20:
            best_fallback_idx = -1
            best_fallback_match_count = 0
            for idx, doc in enumerate(self.documents):
                titre_clean = remove_accents(doc["lecon"].get("titre", "").lower())
                matches = 0
                for q in query_tokens:
                    # On cherche des correspondances partielles et entières
                    if len(q) > 1 and (q in titre_clean or titre_clean in q):
                        matches += 1
                if matches > best_fallback_match_count:
                    best_fallback_match_count = matches
                    best_fallback_idx = idx
            
            if best_fallback_idx != -1 and best_fallback_match_count > 0:
                best_doc_idx = best_fallback_idx
                best_score = 0.50 + 0.10 * best_fallback_match_count
                
        if best_score >= threshold and best_doc_idx != -1:
            return self.documents[best_doc_idx], best_score
            
        return None, best_score
