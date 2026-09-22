use aes_gcm::{
    aead::{Aead, KeyInit},
    Aes256Gcm, Nonce,
};
use rand::RngCore;
use sha2::{Digest, Sha256};
use std::env;

pub struct SecurityManager;

impl SecurityManager {
    /// Génère un hachage SHA-256 hexadécimal
    pub fn hash_sha256(data: &[u8]) -> String {
        let mut hasher = Sha256::new();
        hasher.update(data);
        hex::encode(hasher.finalize())
    }

    /// Dérive une clé AES de 32 octets à partir d'une phrase secrète et d'un sel
    pub fn derive_key(passphrase: &str, salt: &[u8]) -> [u8; 32] {
        let mut hasher = Sha256::new();
        hasher.update(passphrase.as_bytes());
        hasher.update(salt);
        hasher.finalize().into()
    }

    /// Chiffre un texte brut en AES-256-GCM avec un sel et un nonce aléatoires
    /// Format de sortie: BASE64(sel 16o + nonce 12o + ciphertext)
    pub fn encrypt_aes_gcm(plaintext: &str, passphrase: &str) -> Result<String, String> {
        let mut salt = [0u8; 16];
        let mut nonce_bytes = [0u8; 12];
        rand::thread_rng().fill_bytes(&mut salt);
        rand::thread_rng().fill_bytes(&mut nonce_bytes);

        let key = Self::derive_key(passphrase, &salt);
        let cipher = Aes256Gcm::new_from_slice(&key)
            .map_err(|e| format!("Erreur initialisation cipher: {}", e))?;
        let nonce = Nonce::from_slice(&nonce_bytes);

        let ciphertext = cipher
            .encrypt(nonce, plaintext.as_bytes())
            .map_err(|e| format!("Échec du chiffrement: {}", e))?;

        let mut payload = Vec::with_capacity(16 + 12 + ciphertext.len());
        payload.extend_from_slice(&salt);
        payload.extend_from_slice(&nonce_bytes);
        payload.extend_from_slice(&ciphertext);

        Ok(base64::Engine::encode(
            &base64::engine::general_purpose::STANDARD,
            &payload,
        ))
    }

    /// Déchiffre un blob BASE64 chiffré en AES-256-GCM
    pub fn decrypt_aes_gcm(encrypted_b64: &str, passphrase: &str) -> Result<String, String> {
        let payload = base64::Engine::decode(
            &base64::engine::general_purpose::STANDARD,
            encrypted_b64,
        )
        .map_err(|e| format!("Base64 invalide: {}", e))?;

        if payload.len() < 28 {
            return Err("Payload corrompu ou trop court".into());
        }

        let salt = &payload[0..16];
        let nonce_bytes = &payload[16..28];
        let ciphertext = &payload[28..];

        let key = Self::derive_key(passphrase, salt);
        let cipher = Aes256Gcm::new_from_slice(&key)
            .map_err(|e| format!("Erreur initialisation cipher: {}", e))?;
        let nonce = Nonce::from_slice(nonce_bytes);

        let decrypted_bytes = cipher
            .decrypt(nonce, ciphertext)
            .map_err(|_| "Clé ou phrase secrète incorrecte (Authentification GCM échouée)".to_string())?;

        String::from_utf8(decrypted_bytes)
            .map_err(|e| format!("Texte déchiffré UTF-8 invalide: {}", e))
    }

    /// Calcule l'empreinte matérielle de la machine hôte pour le verrouillage offline
    pub fn get_hardware_fingerprint() -> String {
        let os = env::consts::OS;
        let arch = env::consts::ARCH;
        let hostname = env::var("COMPUTERNAME")
            .or_else(|_| env::var("HOSTNAME"))
            .unwrap_or_else(|_| "ASTA_STATION".to_string());
        
        let raw_id = format!("HW-{}-{}-{}-ASTA2028", os, arch, hostname);
        Self::hash_sha256(raw_id.as_bytes())
    }
}
