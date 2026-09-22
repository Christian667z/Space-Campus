use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Représente un cours ou une leçon académique (remplace les données JSON Python)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Course {
    pub id: String,
    pub title: String,
    pub subject: String,
    pub level: CourseLevel,
    pub description: String,
    pub chapters: Vec<Chapter>,
    pub tags: Vec<String>,
}

/// Niveau académique d'un cours
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum CourseLevel {
    Debutant,
    Intermediaire,
    Avance,
    Expert,
}

impl std::fmt::Display for CourseLevel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let label = match self {
            CourseLevel::Debutant => "Débutant",
            CourseLevel::Intermediaire => "Intermédiaire",
            CourseLevel::Avance => "Avancé",
            CourseLevel::Expert => "Expert",
        };
        write!(f, "{}", label)
    }
}

/// Chapitre d'un cours
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Chapter {
    pub index: u32,
    pub title: String,
    pub content: String,
    pub code_examples: Vec<CodeExample>,
}

/// Exemple de code dans un chapitre de cours
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CodeExample {
    pub language: String,
    pub description: String,
    pub code: String,
}

/// Catalogue de cours académiques intégrés (remplace les fichiers JSON Python)
pub struct CourseCatalog {
    courses: HashMap<String, Course>,
}

impl CourseCatalog {
    /// Initialise le catalogue avec les cours intégrés UNASMOH
    pub fn new() -> Self {
        let mut catalog = Self {
            courses: HashMap::new(),
        };
        catalog.load_builtin_courses();
        catalog
    }

    /// Charge les cours intégrés dans la mémoire
    fn load_builtin_courses(&mut self) {
        let courses = vec![
            Course {
                id: "cs101-algo".to_string(),
                title: "Algorithmique & Structures de Données".to_string(),
                subject: "Informatique".to_string(),
                level: CourseLevel::Debutant,
                description: "Introduction aux algorithmes fondamentaux : tri, recherche, récursivité et complexité.".to_string(),
                chapters: vec![
                    Chapter {
                        index: 1,
                        title: "Introduction à la complexité algorithmique".to_string(),
                        content: "La complexité algorithmique mesure l'efficacité d'un algorithme en termes de temps (O(n)) et d'espace mémoire. La notation Big-O est utilisée pour exprimer le comportement asymptotique.".to_string(),
                        code_examples: vec![
                            CodeExample {
                                language: "rust".to_string(),
                                description: "Recherche linéaire O(n)".to_string(),
                                code: "fn linear_search(arr: &[i32], target: i32) -> Option<usize> {\n    arr.iter().position(|&x| x == target)\n}".to_string(),
                            },
                        ],
                    },
                    Chapter {
                        index: 2,
                        title: "Tri par insertion et tri rapide".to_string(),
                        content: "Le tri par insertion a une complexité O(n²) dans le pire cas, alors que le tri rapide (QuickSort) atteint O(n log n) en moyenne.".to_string(),
                        code_examples: vec![],
                    },
                ],
                tags: vec!["algorithme".to_string(), "complexité".to_string(), "tri".to_string()],
            },
            Course {
                id: "net101-subnetting".to_string(),
                title: "Réseaux : Adressage IPv4 & Sous-Réseaux".to_string(),
                subject: "Réseaux".to_string(),
                level: CourseLevel::Intermediaire,
                description: "Maîtrise de l'adressage IPv4, des masques CIDR, et du découpage en sous-réseaux.".to_string(),
                chapters: vec![
                    Chapter {
                        index: 1,
                        title: "Adressage IPv4 et classes".to_string(),
                        content: "Une adresse IPv4 est composée de 32 bits divisés en 4 octets. Les classes A, B et C définissent la partition réseau/hôte. Le CIDR (Classless Inter-Domain Routing) remplace ce système rigide.".to_string(),
                        code_examples: vec![
                            CodeExample {
                                language: "bash".to_string(),
                                description: "Calcul d'un sous-réseau avec asta-cli".to_string(),
                                code: "asta-cli subnet --ip 192.168.10.0 --cidr 26\n# Résultat:\n# Masque     : 255.255.255.192\n# Réseau     : 192.168.10.0\n# Broadcast  : 192.168.10.63\n# Hôtes      : 62 utilisables".to_string(),
                            },
                        ],
                    },
                ],
                tags: vec!["réseau".to_string(), "ipv4".to_string(), "cidr".to_string(), "subnetting".to_string()],
            },
            Course {
                id: "sec101-crypto".to_string(),
                title: "Sécurité Informatique & Cryptographie".to_string(),
                subject: "Sécurité".to_string(),
                level: CourseLevel::Avance,
                description: "Principes de la cryptographie moderne : hachage, chiffrement symétrique AES-GCM, et signatures numériques.".to_string(),
                chapters: vec![
                    Chapter {
                        index: 1,
                        title: "Hachage SHA-256 et intégrité des données".to_string(),
                        content: "SHA-256 produit un condensé de 256 bits à sens unique. Il est utilisé pour vérifier l'intégrité des données et stocker des mots de passe de façon sécurisée avec salage.".to_string(),
                        code_examples: vec![
                            CodeExample {
                                language: "rust".to_string(),
                                description: "Hachage SHA-256 avec le moteur Asta".to_string(),
                                code: "use asta_core::security::SecurityManager;\nlet hash = SecurityManager::sha256_hex(\"mot_de_passe_secret\");\nprintln!(\"SHA-256: {}\", hash);".to_string(),
                            },
                        ],
                    },
                    Chapter {
                        index: 2,
                        title: "Chiffrement AES-256-GCM".to_string(),
                        content: "AES-256-GCM est un mode de chiffrement authentifié qui garantit à la fois la confidentialité et l'intégrité des données. Il utilise un nonce de 96 bits et produit un tag d'authentification de 128 bits.".to_string(),
                        code_examples: vec![
                            CodeExample {
                                language: "bash".to_string(),
                                description: "Chiffrement avec asta-cli".to_string(),
                                code: "asta-cli encrypt --text \"Données secrètes\" --key \"ma_phrase_secrète\"\n# Résultat: ASTA-AES256GCM:<base64>".to_string(),
                            },
                        ],
                    },
                ],
                tags: vec!["cryptographie".to_string(), "aes".to_string(), "sha256".to_string(), "sécurité".to_string()],
            },
            Course {
                id: "sys101-os".to_string(),
                title: "Systèmes d'Exploitation : Concepts Fondamentaux".to_string(),
                subject: "Systèmes".to_string(),
                level: CourseLevel::Intermediaire,
                description: "Gestion des processus, mémoire virtuelle, ordonnancement et appels système dans les OS modernes.".to_string(),
                chapters: vec![
                    Chapter {
                        index: 1,
                        title: "Processus et threads".to_string(),
                        content: "Un processus est une instance d'un programme en exécution avec son propre espace mémoire. Un thread partage l'espace mémoire du processus père et permet la concurrence légère.".to_string(),
                        code_examples: vec![
                            CodeExample {
                                language: "rust".to_string(),
                                description: "Thread léger avec Tokio".to_string(),
                                code: "use tokio::task;\n\n#[tokio::main]\nasync fn main() {\n    let handle = task::spawn(async {\n        println!(\"Thread asynchrone Rust\");\n    });\n    handle.await.unwrap();\n}".to_string(),
                            },
                        ],
                    },
                ],
                tags: vec!["OS".to_string(), "processus".to_string(), "mémoire".to_string(), "threads".to_string()],
            },
        ];

        for course in courses {
            self.courses.insert(course.id.clone(), course);
        }
    }

    /// Récupère un cours par son ID
    pub fn get_course(&self, id: &str) -> Option<&Course> {
        self.courses.get(id)
    }

    /// Liste tous les cours disponibles (sans les chapitres complets)
    pub fn list_courses(&self) -> Vec<CourseSummary> {
        self.courses
            .values()
            .map(|c| CourseSummary {
                id: c.id.clone(),
                title: c.title.clone(),
                subject: c.subject.clone(),
                level: c.level.to_string(),
                chapter_count: c.chapters.len(),
                tags: c.tags.clone(),
            })
            .collect()
    }

    /// Recherche des cours par mot-clé dans le titre, sujet ou tags
    pub fn search_courses(&self, query: &str) -> Vec<CourseSummary> {
        let q = query.to_lowercase();
        self.courses
            .values()
            .filter(|c| {
                c.title.to_lowercase().contains(&q)
                    || c.subject.to_lowercase().contains(&q)
                    || c.tags.iter().any(|t| t.to_lowercase().contains(&q))
                    || c.description.to_lowercase().contains(&q)
            })
            .map(|c| CourseSummary {
                id: c.id.clone(),
                title: c.title.clone(),
                subject: c.subject.clone(),
                level: c.level.to_string(),
                chapter_count: c.chapters.len(),
                tags: c.tags.clone(),
            })
            .collect()
    }
}

/// Résumé d'un cours pour les listes et la recherche
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CourseSummary {
    pub id: String,
    pub title: String,
    pub subject: String,
    pub level: String,
    pub chapter_count: usize,
    pub tags: Vec<String>,
}

impl Default for CourseCatalog {
    fn default() -> Self {
        Self::new()
    }
}
