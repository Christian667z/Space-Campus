// ─── Modules publics de asta-core ────────────────────────────────────────────

/// Module de gestion de la base de données SQLite offline
pub mod db;

/// Module de cours et catalogue académique UNASMOH
pub mod courses;

/// Module de gestion des erreurs unifiées
pub mod errors;

/// Module de gestion des licences hors-ligne
pub mod licenses;

/// Module d'outils logiques (conversion de bases, sous-réseaux IPv4, algèbre booléenne)
pub mod logic_tools;

/// Moteur RAG local Space AI (recherche dans les notes étudiantes)
pub mod rag;

/// Module de sécurité cryptographique (AES-256-GCM, SHA-256, HWID)
pub mod security;

// ─── Réexportations pratiques ─────────────────────────────────────────────────

pub use courses::{CourseCatalog, CourseSummary, Course, Chapter, CourseLevel};
pub use db::DatabaseManager;
pub use errors::{AstaError, AstaResult};
pub use licenses::{License, LicenseManager, LicenseValidation};
pub use logic_tools::{convert_all, calculate_subnet, get_boolean_laws, ConversionResult, SubnetResult, BooleanLaw};
pub use rag::LocalRagEngine;
pub use security::SecurityManager;
