use aes_gcm::aead::{Aead, KeyInit};
use aes_gcm::{Aes256Gcm, Nonce};
use base64::engine::general_purpose::STANDARD as BASE64;
use base64::Engine;
use rand::RngCore;
use sha2::{Digest, Sha256};
use std::env;

pub struct SecurityManager;

impl SecurityManager {
    /// Calcule le SHA-256 d'une chaîne
    pub fn sha256_hex(input: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(input.as_bytes());
        hex::encode(hasher.finalize())
    }

    /// Dérive une clé AES 256-bit à partir d'une phrase secrète et d'un sel
    pub fn derive_key(passphrase: &str, salt: &[u8]) -> [u8; 32] {
        let mut hasher = Sha256::new();
        hasher.update(passphrase.as_bytes());
        hasher.update(salt);
        let mut key = [0u8; 32];
        key.copy_from_slice(&hasher.finalize());
        key
    }

    /// Chiffre un texte avec AES-256-GCM.
    /// Format retourné: ASTA-AES256GCM:<base64(salt[16] + nonce[12] + ciphertext)>
    pub fn encrypt_aes_gcm(plaintext: &str, passphrase: &str) -> Result<String, String> {
        let mut salt = [0u8; 16];
        let mut nonce_bytes = [0u8; 12];
        rand::thread_rng().fill_bytes(&mut salt);
        rand::thread_rng().fill_bytes(&mut nonce_bytes);

        let key_bytes = Self::derive_key(passphrase, &salt);
        let cipher = Aes256Gcm::new_from_slice(&key_bytes)
            .map_err(|e| format!("Erreur initialisation AES-GCM: {}", e))?;
        let nonce = Nonce::from_slice(&nonce_bytes);

        let ciphertext = cipher
            .encrypt(nonce, plaintext.as_bytes())
            .map_err(|e| format!("Erreur chiffrement: {}", e))?;

        let mut payload = Vec::with_capacity(salt.len() + nonce_bytes.len() + ciphertext.len());
        payload.extend_from_slice(&salt);
        payload.extend_from_slice(&nonce_bytes);
        payload.extend_from_slice(&ciphertext);

        let b64 = BASE64.encode(&payload);
        Ok(format!("ASTA-AES256GCM:{}", b64))
    }

    /// Déchiffre un message au format ASTA-AES256GCM:<base64>
    pub fn decrypt_aes_gcm(encrypted_b64: &str, passphrase: &str) -> Result<String, String> {
        let clean = encrypted_b64.trim().trim_start_matches("ASTA-AES256GCM:");
        let raw = BASE64
            .decode(clean)
            .map_err(|e| format!("Encodage Base64 invalide: {}", e))?;

        if raw.len() < 28 {
            return Err("Données chiffrées corrompues ou trop courtes".to_string());
        }

        let salt = &raw[0..16];
        let nonce_bytes = &raw[16..28];
        let ciphertext = &raw[28..];

        let key_bytes = Self::derive_key(passphrase, salt);
        let cipher = Aes256Gcm::new_from_slice(&key_bytes)
            .map_err(|e| format!("Erreur initialisation AES-GCM: {}", e))?;
        let nonce = Nonce::from_slice(nonce_bytes);

        let decrypted = cipher
            .decrypt(nonce, ciphertext)
            .map_err(|_| "Échec d'authentification GCM: phrase secrète incorrecte ou données altérées".to_string())?;

        String::from_utf8(decrypted).map_err(|e| format!("Texte déchiffré invalide (non UTF-8): {}", e))
    }

    /// Génère une empreinte matérielle sécurisée
    pub fn get_hardware_fingerprint() -> String {
        let hostname = env::var("COMPUTERNAME")
            .or_else(|_| env::var("HOSTNAME"))
            .unwrap_or_else(|_| "ASTA_DEFAULT_HOST".to_string());
        let username = env::var("USERNAME")
            .or_else(|_| env::var("USER"))
            .unwrap_or_else(|_| "UNKNOWN_USER".to_string());

        let raw_identity = format!("ASTA-ACADEMIE-UNASMOH:{}:{}:2028", hostname, username);
        let hash = Self::sha256_hex(&raw_identity);
        format!(
            "ASTA-HWID-{}-{}",
            &hash[0..8].to_uppercase(),
            &hash[8..16].to_uppercase()
        )
    }
}
