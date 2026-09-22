use serde::{Deserialize, Serialize};
use std::fmt;

/// Erreur unifiée du cœur Asta Campus
#[derive(Debug, Serialize, Deserialize)]
pub enum AstaError {
    /// Erreur liée à la base de données SQLite
    Database(String),
    /// Erreur liée aux opérations cryptographiques
    Crypto(String),
    /// Erreur de validation des entrées
    Validation(String),
    /// Erreur d'accès au système de fichiers
    Io(String),
    /// Erreur d'autorisation / authentification
    Auth(String),
    /// Erreur générique non catégorisée
    General(String),
}

impl fmt::Display for AstaError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AstaError::Database(msg) => write!(f, "[DB] {}", msg),
            AstaError::Crypto(msg) => write!(f, "[CRYPTO] {}", msg),
            AstaError::Validation(msg) => write!(f, "[VALIDATION] {}", msg),
            AstaError::Io(msg) => write!(f, "[IO] {}", msg),
            AstaError::Auth(msg) => write!(f, "[AUTH] {}", msg),
            AstaError::General(msg) => write!(f, "[ERREUR] {}", msg),
        }
    }
}

impl From<rusqlite::Error> for AstaError {
    fn from(e: rusqlite::Error) -> Self {
        AstaError::Database(e.to_string())
    }
}

impl From<std::io::Error> for AstaError {
    fn from(e: std::io::Error) -> Self {
        AstaError::Io(e.to_string())
    }
}

/// Type de résultat standard utilisé dans tout le projet Asta
pub type AstaResult<T> = Result<T, AstaError>;
