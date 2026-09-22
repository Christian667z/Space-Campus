use crate::security::SecurityManager;
use chrono::Utc;
use rusqlite::{params, Connection, Result};
use serde::{Deserialize, Serialize};
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AdminRecord {
    pub id: i64,
    pub username: String,
    pub role: String,
    pub created_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditLog {
    pub id: i64,
    pub event_type: String,
    pub details: String,
    pub severity: String,
    pub timestamp: String,
}

pub struct DatabaseManager {
    conn: Connection,
}

impl DatabaseManager {
    pub fn init<P: AsRef<Path>>(db_path: P) -> Result<Self> {
        let conn = Connection::open(db_path)?;
        let manager = Self { conn };
        manager.migrate()?;
        manager.seed_default_admin()?;
        Ok(manager)
    }

    fn migrate(&self) -> Result<()> {
        self.conn.execute_batch(
            "
            CREATE TABLE IF NOT EXISTS admin_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Administrateur',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS security_audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                details TEXT NOT NULL,
                severity TEXT NOT NULL DEFAULT 'INFO',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                hmac_signature TEXT
            );

            CREATE TABLE IF NOT EXISTS offline_licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_key TEXT UNIQUE NOT NULL,
                machine_fingerprint TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                activation_date DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            ",
        )?;
        Ok(())
    }

    fn seed_default_admin(&self) -> Result<()> {
        let mut check_stmt = self
            .conn
            .prepare("SELECT COUNT(*) FROM admin_credentials WHERE username = ?1")?;
        let count: i64 = check_stmt.query_row(params!["Christian Alvaro"], |row| row.get(0))?;

        if count == 0 {
            let salt = "ASTA_SALT_SECURE_2028";
            let raw_pwd = "unashmoh2028";
            let hash = SecurityManager::sha256_hex(&format!("{}{}", raw_pwd, salt));

            self.conn.execute(
                "INSERT INTO admin_credentials (username, password_hash, salt, role) VALUES (?1, ?2, ?3, ?4)",
                params!["Christian Alvaro", hash, salt, "Administrateur Principal"],
            )?;

            self.log_event(
                "INIT_ADMIN",
                "Compte administrateur local initialisé pour Christian Alvaro",
                "INFO",
            )?;
        }

        Ok(())
    }

    pub fn verify_admin(&self, username: &str, raw_password: &str) -> Result<Option<AdminRecord>> {
        let mut stmt = self.conn.prepare(
            "SELECT id, username, password_hash, salt, role, created_at FROM admin_credentials WHERE username = ?1",
        )?;

        let mut rows = stmt.query(params![username])?;
        if let Some(row) = rows.next()? {
            let id: i64 = row.get(0)?;
            let uname: String = row.get(1)?;
            let stored_hash: String = row.get(2)?;
            let salt: String = row.get(3)?;
            let role: String = row.get(4)?;
            let created_at: String = row.get(5)?;

            let computed = SecurityManager::sha256_hex(&format!("{}{}", raw_password, salt));
            if computed == stored_hash {
                let _ = self.log_event(
                    "AUTH_SUCCESS",
                    &format!("Connexion réussie pour: {}", uname),
                    "INFO",
                );
                return Ok(Some(AdminRecord {
                    id,
                    username: uname,
                    role,
                    created_at,
                }));
            }
        }

        let _ = self.log_event(
            "AUTH_FAILED",
            &format!("Tentative de connexion échouée pour: {}", username),
            "WARN",
        );
        Ok(None)
    }

    pub fn log_event(&self, event_type: &str, details: &str, severity: &str) -> Result<()> {
        let now = Utc::now().to_rfc3339();
        let payload = format!("{}:{}:{}:{}", event_type, details, severity, now);
        let signature = SecurityManager::sha256_hex(&payload);

        self.conn.execute(
            "INSERT INTO security_audit_logs (event_type, details, severity, timestamp, hmac_signature)
             VALUES (?1, ?2, ?3, ?4, ?5)",
            params![event_type, details, severity, now, signature],
        )?;

        Ok(())
    }

    pub fn get_recent_logs(&self, limit: usize) -> Result<Vec<AuditLog>> {
        let mut stmt = self.conn.prepare(
            "SELECT id, event_type, details, severity, timestamp
             FROM security_audit_logs ORDER BY id DESC LIMIT ?1",
        )?;

        let rows = stmt.query_map(params![limit as i64], |row| {
            Ok(AuditLog {
                id: row.get(0)?,
                event_type: row.get(1)?,
                details: row.get(2)?,
                severity: row.get(3)?,
                timestamp: row.get(4)?,
            })
        })?;

        let mut logs = Vec::new();
        for r in rows {
            logs.push(r?);
        }
        Ok(logs)
    }

    /// Exécute une requête SQL avec paramètres (helper pour les sous-modules)
    pub fn execute(&self, sql: &str, params: impl rusqlite::Params) -> Result<usize> {
        self.conn.execute(sql, params)
    }

    /// Recherche une licence dans la base par sa clé
    pub fn query_license(&self, license_key: &str) -> Result<Option<crate::licenses::License>> {
        let mut stmt = self.conn.prepare(
            "SELECT license_key, machine_fingerprint, is_active, activation_date
             FROM offline_licenses WHERE license_key = ?1",
        )?;

        let result = stmt.query_row(params![license_key], |row| {
            let is_active_int: i32 = row.get(2)?;
            Ok(crate::licenses::License {
                license_key: row.get(0)?,
                owner_name: String::new(),
                machine_fingerprint: row.get(1)?,
                is_active: is_active_int != 0,
                activation_date: row.get(3)?,
            })
        });

        match result {
            Ok(lic) => Ok(Some(lic)),
            Err(rusqlite::Error::QueryReturnedNoRows) => Ok(None),
            Err(e) => Err(e),
        }
    }

    /// Retourne toutes les licences enregistrées localement
    pub fn get_all_licenses(&self) -> Result<Vec<crate::licenses::License>> {
        let mut stmt = self.conn.prepare(
            "SELECT license_key, machine_fingerprint, is_active, activation_date
             FROM offline_licenses ORDER BY activation_date DESC",
        )?;

        let iter = stmt.query_map([], |row| {
            let is_active_int: i32 = row.get(2)?;
            Ok(crate::licenses::License {
                license_key: row.get(0)?,
                owner_name: String::new(),
                machine_fingerprint: row.get(1)?,
                is_active: is_active_int != 0,
                activation_date: row.get(3)?,
            })
        })?;

        let mut result = Vec::new();
        for item in iter {
            result.push(item?);
        }
        Ok(result)
    }
}
