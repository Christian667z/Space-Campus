// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use asta_core::db::{AuditLog, DatabaseManager};
use asta_core::logic_tools::{calculate_subnet, convert_all, get_boolean_laws, BooleanLaw, ConversionResult, SubnetResult};
use asta_core::rag::LocalRagEngine;
use asta_core::security::SecurityManager;
use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use tauri::{Manager, State, Window};

// ─── État global de l'application ────────────────────────────────────────────

struct AppState {
    db: Mutex<DatabaseManager>,
    rag: Mutex<LocalRagEngine>,
}

// ─── Structures de réponse IPC ────────────────────────────────────────────────

#[derive(Serialize)]
struct SystemMetrics {
    os: String,
    arch: String,
    hardware_id: String,
    rust_version: String,
    database_status: String,
    crypto_engine: String,
}

#[derive(Serialize)]
struct AuthResponse {
    success: bool,
    message: String,
    role: Option<String>,
}

#[derive(Serialize)]
struct CryptoResponse {
    success: bool,
    result: String,
    error: Option<String>,
}

#[derive(Serialize)]
struct ChatResponse {
    query: String,
    answer: String,
    sources: Vec<String>,
    score: f32,
}

// ─── Commandes Tauri IPC ──────────────────────────────────────────────────────

/// Retourne les métriques système de la machine hôte
#[tauri::command]
fn cmd_get_system_metrics(state: State<AppState>) -> Result<SystemMetrics, String> {
    let hw_id = SecurityManager::get_hardware_fingerprint();
    let db = state.db.lock().map_err(|e| e.to_string())?;
    // Ping DB pour vérifier l'état
    let db_ok = db.get_recent_logs(1).is_ok();

    Ok(SystemMetrics {
        os: std::env::consts::OS.to_string(),
        arch: std::env::consts::ARCH.to_string(),
        hardware_id: hw_id,
        rust_version: "Rust 1.98+ (Tauri v2 — asta-core)".to_string(),
        database_status: if db_ok {
            "SQLite 3 (rusqlite bundled) — Connecté ✓".to_string()
        } else {
            "SQLite — Erreur de connexion".to_string()
        },
        crypto_engine: "AES-256-GCM + SHA-256 (Rust Natif)".to_string(),
    })
}

/// Authentifie un administrateur local via la base SQLite offline
#[tauri::command]
fn cmd_authenticate_admin(
    username: String,
    password: String,
    state: State<AppState>,
) -> Result<AuthResponse, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    match db.verify_admin(&username, &password) {
        Ok(Some(admin)) => Ok(AuthResponse {
            success: true,
            message: format!("Bienvenue, {} — Session active.", admin.username),
            role: Some(admin.role),
        }),
        Ok(None) => Ok(AuthResponse {
            success: false,
            message: "Identifiants incorrects. Accès refusé.".to_string(),
            role: None,
        }),
        Err(e) => Err(format!("Erreur base de données: {}", e)),
    }
}

/// Chiffre un payload texte avec AES-256-GCM
#[tauri::command]
fn cmd_encrypt_payload(payload: String, passphrase: String) -> CryptoResponse {
    match SecurityManager::encrypt_aes_gcm(&payload, &passphrase) {
        Ok(encrypted) => CryptoResponse {
            success: true,
            result: encrypted,
            error: None,
        },
        Err(e) => CryptoResponse {
            success: false,
            result: String::new(),
            error: Some(e),
        },
    }
}

/// Déchiffre un payload au format ASTA-AES256GCM:<base64>
#[tauri::command]
fn cmd_decrypt_payload(encrypted_b64: String, passphrase: String) -> CryptoResponse {
    match SecurityManager::decrypt_aes_gcm(&encrypted_b64, &passphrase) {
        Ok(decrypted) => CryptoResponse {
            success: true,
            result: decrypted,
            error: None,
        },
        Err(e) => CryptoResponse {
            success: false,
            result: String::new(),
            error: Some(e),
        },
    }
}

/// Récupère les derniers enregistrements de la table d'audit SQLite
#[tauri::command]
fn cmd_get_audit_trail(limit: usize, state: State<AppState>) -> Result<Vec<AuditLog>, String> {
    let db = state.db.lock().map_err(|e| e.to_string())?;
    db.get_recent_logs(limit).map_err(|e| e.to_string())
}

/// Convertit un nombre dans toutes les bases (Déc, Bin, Hex, Oct)
#[tauri::command]
fn cmd_convert_number(value: String) -> ConversionResult {
    convert_all(&value)
}

/// Calcule les caractéristiques d'un sous-réseau IPv4 avec CIDR
#[tauri::command]
fn cmd_calculate_subnet(ip: String, cidr: u8) -> Result<SubnetResult, String> {
    calculate_subnet(&ip, cidr)
}

/// Retourne la liste des lois d'algèbre booléenne (De Morgan, Absorption…)
#[tauri::command]
fn cmd_get_boolean_laws() -> Vec<BooleanLaw> {
    get_boolean_laws()
}

/// Interroge le moteur RAG local Space AI (basé sur les notes étudiantes)
#[tauri::command]
fn cmd_space_ai_query(query: String, state: State<AppState>) -> ChatResponse {
    let rag = state.rag.lock().unwrap();
    let res = rag.answer_query(&query);
    ChatResponse {
        query: res.query,
        answer: res.answer,
        sources: res.matched_sources,
        score: res.score,
    }
}

/// Contrôles de fenêtre — minimiser
#[tauri::command]
fn cmd_window_minimize(window: Window) -> Result<(), String> {
    window.minimize().map_err(|e| e.to_string())
}

/// Contrôles de fenêtre — maximiser / restaurer
#[tauri::command]
fn cmd_window_toggle_maximize(window: Window) -> Result<(), String> {
    if window.is_maximized().map_err(|e| e.to_string())? {
        window.unmaximize().map_err(|e| e.to_string())
    } else {
        window.maximize().map_err(|e| e.to_string())
    }
}

/// Contrôles de fenêtre — fermer
#[tauri::command]
fn cmd_window_close(window: Window) -> Result<(), String> {
    window.close().map_err(|e| e.to_string())
}

// ─── Point d'entrée principal ─────────────────────────────────────────────────

fn main() {
    let db_path = "asta_offline.db";
    let db_manager = DatabaseManager::init(db_path)
        .expect("Échec d'initialisation de la base SQLite offline Asta Campus");

    let rag_engine = LocalRagEngine::new("student_notes");

    tauri::Builder::default()
        .manage(AppState {
            db: Mutex::new(db_manager),
            rag: Mutex::new(rag_engine),
        })
        .invoke_handler(tauri::generate_handler![
            // Système
            cmd_get_system_metrics,
            // Authentification
            cmd_authenticate_admin,
            // Cryptographie
            cmd_encrypt_payload,
            cmd_decrypt_payload,
            // Audit & Logs
            cmd_get_audit_trail,
            // Outils logiques
            cmd_convert_number,
            cmd_calculate_subnet,
            cmd_get_boolean_laws,
            // Space AI (RAG)
            cmd_space_ai_query,
            // Contrôles fenêtre
            cmd_window_minimize,
            cmd_window_toggle_maximize,
            cmd_window_close,
        ])
        .run(tauri::generate_context!())
        .expect("Erreur lors de l'exécution d'Asta Campus Desktop");
}
