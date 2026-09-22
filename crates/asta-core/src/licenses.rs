use chrono::Utc;
use rusqlite::{params, Result};
use serde::{Deserialize, Serialize};

use crate::db::DatabaseManager;
use crate::security::SecurityManager;

/// Représente une licence hors-ligne activée pour Asta Campus
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct License {
    pub license_key: String,
    pub owner_name: String,
    pub machine_fingerprint: String,
    pub is_active: bool,
    pub activation_date: String,
}

/// Résultat de validation d'une licence
#[derive(Debug, Serialize, Deserialize)]
pub struct LicenseValidation {
    pub valid: bool,
    pub message: String,
    pub owner: Option<String>,
    pub machine_match: bool,
}

/// Gestionnaire de licences offline pour Asta Campus
pub struct LicenseManager<'a> {
    db: &'a DatabaseManager,
}

impl<'a> LicenseManager<'a> {
    pub fn new(db: &'a DatabaseManager) -> Self {
        Self { db }
    }

    /// Génère une clé de licence basée sur le nom du propriétaire et l'empreinte machine
    pub fn generate_license_key(owner_name: &str, machine_fingerprint: &str) -> String {
        let raw = format!(
            "ASTA-LICENSE:{}:{}:{}:UNASMOH2028",
            owner_name,
            machine_fingerprint,
            Utc::now().timestamp()
        );
        let hash = SecurityManager::sha256_hex(&raw);
        // Format: ASTA-XXXX-XXXX-XXXX-XXXX
        format!(
            "ASTA-{}-{}-{}-{}",
            &hash[0..4].to_uppercase(),
            &hash[4..8].to_uppercase(),
            &hash[8..12].to_uppercase(),
            &hash[12..16].to_uppercase(),
        )
    }

    /// Enregistre une nouvelle licence dans la base SQLite
    pub fn register_license(
        &self,
        owner_name: &str,
        license_key: &str,
    ) -> Result<()> {
        let hwid = SecurityManager::get_hardware_fingerprint();
        let now = Utc::now().to_rfc3339();

        self.db.execute(
            "INSERT OR IGNORE INTO offline_licenses
             (license_key, machine_fingerprint, is_active, activation_date)
             VALUES (?1, ?2, 1, ?3)",
            params![license_key, hwid, now],
        )?;

        self.db.log_event(
            "LICENSE_ACTIVATED",
            &format!("Licence enregistrée pour {} : {}", owner_name, license_key),
            "INFO",
        )?;

        Ok(())
    }

    /// Valide si une licence est active et correspond à la machine actuelle
    pub fn validate_license(&self, license_key: &str) -> Result<LicenseValidation> {
        let current_hwid = SecurityManager::get_hardware_fingerprint();

        let result = self.db.query_license(license_key);

        match result {
            Ok(Some(lic)) => {
                let machine_match = lic.machine_fingerprint == current_hwid;
                let valid = lic.is_active && machine_match;

                let message = if !lic.is_active {
                    "Licence révoquée ou désactivée.".to_string()
                } else if !machine_match {
                    "Licence non valide pour cette machine (empreinte différente).".to_string()
                } else {
                    "Licence valide et active.".to_string()
                };

                Ok(LicenseValidation {
                    valid,
                    message,
                    owner: None,
                    machine_match,
                })
            }
            Ok(None) => Ok(LicenseValidation {
                valid: false,
                message: "Clé de licence introuvable dans la base locale.".to_string(),
                owner: None,
                machine_match: false,
            }),
            Err(e) => Err(e),
        }
    }

    /// Liste toutes les licences actives enregistrées localement
    pub fn list_licenses(&self) -> Result<Vec<License>> {
        self.db.get_all_licenses()
    }
}
