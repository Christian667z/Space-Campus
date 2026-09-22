use rusqlite::{params, Connection, Result};
use serde::{Deserialize, Serialize};
use std::path::Path;
use crate::security::SecurityManager;

#[derive(Debug, Serialize, Deserialize)]
pub struct AdminRecord {
    pub id: String,
    pub username: String,
    pub role: String,
    pub hardware_lock: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AuditLog {
    pub id: String,
    pub event_type: String,
    pub details: String,
    pub severity: String,
    pub timestamp: i64,
}

pub struct DatabaseManager {
    conn: Connection,
}

impl DatabaseManager {
    /// Initialise la base SQLite locale chiffrée ou standard
    pub fn init<P: AsRef<Path>>(path: P) -> Result<Self> {
        let conn = Connection::open(path)?;
        let manager = Self { conn };
        manager.migrate()?;
        manager.seed_defaults()?;
        Ok(manager)
    }

    /// Applique les schémas de sécurité offline
    fn migrate(&self) -> Result<()> {
        self.conn.execute_batch(
            "
            CREATE TABLE IF NOT EXISTS admin_credentials (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Administrateur',
                hardware_lock TEXT,
                created_at INTEGER NOT NULL,
                last_login INTEGER
            );

            CREATE TABLE IF NOT EXISTS security_audit_logs (
                id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                details TEXT NOT NULL,
                severity TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                signature TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS offline_licenses (
                license_key TEXT PRIMARY KEY,
                owner_name TEXT NOT NULL,
                hardware_id TEXT NOT NULL,
                features_mask INTEGER NOT NULL,
                expires_at INTEGER NOT NULL,
                is_revoked INTEGER NOT NULL DEFAULT 0
            );
            "
        )?;
        Ok(())
    }

    /// Alimente le compte administrateur initial si absent
    fn seed_defaults(&self) -> Result<()> {
        let mut check_stmt = self.conn.prepare("SELECT COUNT(*) FROM admin_credentials")?;
        let count: i64 = check_stmt.query_row([], |row| row.get(0))?;

        if count == 0 {
            let salt = "ASTA_SALT_SECURE_2028";
            // Mot de passe par défaut: "unashmoh2028"
            let salted_pwd = format!("unashmoh2028{}", salt);
            let pwd_hash = SecurityManager::hash_sha256(salted_pwd.as_bytes());
            let now = chrono::Utc::now().timestamp();
            let hw_id = SecurityManager::get_hardware_fingerprint();

            self.conn.execute(
                "INSERT INTO admin_credentials (id, username, password_hash, salt, role, hardware_lock, created_at)
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
                params![
                    "admin-01",
                    "Christian Alvaro",
                    pwd_hash,
                    salt,
                    "Administrateur Principal",
                    hw_id,
                    now
                ],
            )?;

            self.log_event("SYSTEM_INIT", "Création automatique du compte Administrateur Offline", "INFO")?;
        }
        Ok(())
    }

    /// Vérifie les identifiants d'un administrateur hors-ligne
    pub fn verify_admin(&self, username: &str, password_attempt: &str) -> Result<Option<AdminRecord>> {
        let mut stmt = self.conn.prepare(
            "SELECT id, username, password_hash, salt, role, hardware_lock FROM admin_credentials WHERE username = ?1"
        )?;

        let result = stmt.query_row(params![username], |row| {
            let id: String = row.get(0)?;
            let uname: String = row.get(1)?;
            let stored_hash: String = row.get(2)?;
            let salt: String = row.get(3)?;
            let role: String = row.get(4)?;
            let hw_lock: Option<String> = row.get(5)?;

            let attempt_salted = format!("{}{}", password_attempt, salt);
            let attempt_hash = SecurityManager::hash_sha256(attempt_salted.as_bytes());

            if attempt_hash == stored_hash {
                Ok(Some(AdminRecord {
                    id,
                    username: uname,
                    role,
                    hardware_lock: hw_lock,
                }))
            } else {
                Ok(None)
            }
        });

        match result {
            Ok(admin_opt) => {
                if admin_opt.is_some() {
                    let _ = self.log_event("AUTH_SUCCESS", &format!("Connexion réussie pour {}", username), "INFO");
                } else {
                    let _ = self.log_event("AUTH_FAIL", &format!("Échec mot de passe pour {}", username), "WARN");
                }
                Ok(admin_opt)
            }
            Err(rusqlite::Error::QueryReturnedNoRows) => {
                let _ = self.log_event("AUTH_FAIL", &format!("Utilisateur inconnu: {}", username), "WARN");
                Ok(None)
            }
            Err(e) => Err(e),
        }
    }

    /// Enregistre un événement dans les logs d'audit avec signature inviolable
    pub fn log_event(&self, event_type: &str, details: &str, severity: &str) -> Result<()> {
        let now = chrono::Utc::now().timestamp();
        let log_id = format!("LOG-{}", now);
        let raw_signature = format!("{}:{}:{}:{}", log_id, event_type, details, now);
        let signature = SecurityManager::hash_sha256(raw_signature.as_bytes());

        self.conn.execute(
            "INSERT INTO security_audit_logs (id, event_type, details, severity, timestamp, signature)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
            params![log_id, event_type, details, severity, now, signature],
        )?;
        Ok(())
    }

    /// Récupère les derniers événements de sécurité
    pub fn get_recent_logs(&self, limit: usize) -> Result<Vec<AuditLog>> {
        let mut stmt = self.conn.prepare(
            "SELECT id, event_type, details, severity, timestamp FROM security_audit_logs ORDER BY timestamp DESC LIMIT ?1"
        )?;

        let log_iter = stmt.query_map(params![limit as i64], |row| {
            Ok(AuditLog {
                id: row.get(0)?,
                event_type: row.get(1)?,
                details: row.get(2)?,
                severity: row.get(3)?,
                timestamp: row.get(4)?,
            })
        })?;

        let mut logs = Vec::new();
        for log in log_iter {
            logs.push(log?);
        }
        Ok(logs)
    }
}
