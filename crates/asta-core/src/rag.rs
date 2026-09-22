use regex::Regex;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RagResponse {
    pub query: String,
    pub answer: String,
    pub matched_sources: Vec<String>,
    pub score: f32,
}

pub struct LocalRagEngine {
    notes_dir: PathBuf,
    keyword_regex: Regex,
}

impl LocalRagEngine {
    pub fn new<P: AsRef<Path>>(notes_dir: P) -> Self {
        let dir = notes_dir.as_ref().to_path_buf();
        let _ = fs::create_dir_all(&dir);
        Self {
            notes_dir: dir,
            keyword_regex: Regex::new(r"\b([a-zA-ZÀ-ÿ0-9]{3,})\b").unwrap(),
        }
    }

    /// Récupère l'ensemble des jetons clés de la requête
    fn extract_keywords(&self, text: &str) -> HashSet<String> {
        self.keyword_regex
            .find_iter(text)
            .map(|m| m.as_str().to_lowercase())
            .collect()
    }

    /// Effectue une recherche RAG locale et produit une réponse synthétisée
    pub fn answer_query(&self, query: &str) -> RagResponse {
        let keywords = self.extract_keywords(query);
        if keywords.is_empty() {
            return RagResponse {
                query: query.to_string(),
                answer: "Votre requête ne contient pas de mots-clés distincts pour rechercher dans la documentation locale d'Asta Académie.".to_string(),
                matched_sources: Vec::new(),
                score: 0.0,
            };
        }

        let mut best_score: f32 = 0.0;
        let mut best_snippets: Vec<String> = Vec::new();
        let mut matched_files: Vec<String> = Vec::new();

        if let Ok(entries) = fs::read_dir(&self.notes_dir) {
            for entry in entries.flatten() {
                let path = entry.path();
                if path.extension().and_then(|e| e.to_str()) == Some("txt")
                    || path.extension().and_then(|e| e.to_str()) == Some("md")
                {
                    if let Ok(content) = fs::read_to_string(&path) {
                        let file_keywords = self.extract_keywords(&content);
                        let intersection_count = keywords.intersection(&file_keywords).count();

                        if intersection_count > 0 {
                            let file_score = intersection_count as f32 / keywords.len() as f32;
                            if file_score > best_score {
                                best_score = file_score;
                            }

                            // Extraire le premier paragraphe contenant un mot-clé
                            for para in content.split("\n\n") {
                                let para_lower = para.to_lowercase();
                                if keywords.iter().any(|k| para_lower.contains(k)) {
                                    let clean = para.trim();
                                    if !clean.is_empty() && clean.len() > 20 {
                                        best_snippets.push(clean.chars().take(280).collect::<String>());
                                        break;
                                    }
                                }
                            }

                            if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
                                matched_files.push(name.to_string());
                            }
                        }
                    }
                }
            }
        }

        let answer = if best_snippets.is_empty() {
            format!(
                "Space AI (Moteur Rust Hors-Ligne) : Aucun extrait direct trouvé dans vos notes locales pour '{}'. Vous pouvez poser une question générale ou consulter les fiches de cours intégrées.",
                query
            )
        } else {
            format!(
                "Space AI (Contexte Local trouvé dans {} fichier(s)) :\n\n{}",
                matched_files.len(),
                best_snippets.join("\n\n---\n\n")
            )
        };

        RagResponse {
            query: query.to_string(),
            answer,
            matched_sources: matched_files,
            score: best_score,
        }
    }
}
