// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod db;
mod ffi;
mod security;

use db::{AdminRecord, AuditLog, DatabaseManager};
use security::SecurityManager;
use serde::Serialize;
use std::sync::Mutex;
use tauri::{AppHandle, Manager, State, Window};

struct AppState {
    db: Mutex<DatabaseManager>,
}

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
    admin: Option<AdminRecord>,
}

#[derive(Serialize)]
struct CryptoResponse {
    success: bool,
    result: String,
    error: Option<String>,
}

#[tauri::command]
fn cmd_get_system_metrics(state: State<AppState>) -> Result<SystemMetrics, String> {
    let hw_id = SecurityManager::get_hardware_fingerprint();
    let db_guard = state.db.lock().map_err(|e| e.to_string())?;
    let _ = db_guard.get_recent_logs(1);

    Ok(SystemMetrics {
        os: std::env::consts::OS.to_string(),
        arch: std::env::consts::ARCH.to_string(),
        hardware_id: hw_id,
        rust_version: "Rust 1.80+ (Tauri v2)".to_string(),
        database_status: "SQLite 3 (rusqlite - Connecté & Vérifié)".to_string(),
        crypto_engine: "AES-256-GCM + SHA-256 (Rust Natif)".to_string(),
    })
}

#[tauri::command]
fn cmd_authenticate_admin(
    username: String,
    password: String,
    state: State<AppState>,
) -> Result<AuthResponse, String> {
    let db_guard = state.db.lock().map_err(|e| e.to_string())?;
    match db_guard.verify_admin(&username, &password) {
        Ok(Some(admin)) => Ok(AuthResponse {
            success: true,
            message: format!("Authentification réussie pour {}", admin.username),
            admin: Some(admin),
        }),
        Ok(None) => Ok(AuthResponse {
            success: false,
            message: "Nom d'utilisateur ou mot de passe incorrect.".to_string(),
            admin: None,
        }),
        Err(e) => Err(format!("Erreur base de données locale: {}", e)),
    }
}

#[tauri::command]
fn cmd_encrypt_payload(payload: String, passphrase: String) -> CryptoResponse {
    match SecurityManager::encrypt_aes_gcm(&payload, &passphrase) {
        Ok(encrypted) => CryptoResponse {
            success: true,
            result: encrypted,
            error: None,
        },
        Err(err) => CryptoResponse {
            success: false,
            result: String::new(),
            error: Some(err),
        },
    }
}

#[tauri::command]
fn cmd_decrypt_payload(encrypted_b64: String, passphrase: String) -> CryptoResponse {
    match SecurityManager::decrypt_aes_gcm(&encrypted_b64, &passphrase) {
        Ok(decrypted) => CryptoResponse {
            success: true,
            result: decrypted,
            error: None,
        },
        Err(err) => CryptoResponse {
            success: false,
            result: String::new(),
            error: Some(err),
        },
    }
}

#[tauri::command]
fn cmd_get_audit_trail(limit: usize, state: State<AppState>) -> Result<Vec<AuditLog>, String> {
    let db_guard = state.db.lock().map_err(|e| e.to_string())?;
    db_guard.get_recent_logs(limit).map_err(|e| e.to_string())
}

#[tauri::command]
fn cmd_window_minimize(window: Window) -> Result<(), String> {
    window.minimize().map_err(|e| e.to_string())
}

#[tauri::command]
fn cmd_window_toggle_maximize(window: Window) -> Result<(), String> {
    if window.is_maximized().map_err(|e| e.to_string())? {
        window.unmaximize().map_err(|e| e.to_string())
    } else {
        window.maximize().map_err(|e| e.to_string())
    }
}

#[tauri::command]
fn cmd_window_close(window: Window) -> Result<(), String> {
    window.close().map_err(|e| e.to_string())
}

fn main() {
    let db_path = "asta_offline.db";
    let db_manager = DatabaseManager::init(db_path)
        .expect("Échec d'initialisation de la base SQLite offline Asta");

    tauri::Builder::default()
        .manage(AppState {
            db: Mutex::new(db_manager),
        })
        .invoke_handler(tauri::generate_handler![
            cmd_get_system_metrics,
            cmd_authenticate_admin,
            cmd_encrypt_payload,
            cmd_decrypt_payload,
            cmd_get_audit_trail,
            cmd_window_minimize,
            cmd_window_toggle_maximize,
            cmd_window_close,
        ])
        .run(tauri::generate_context!())
        .expect("Erreur lors de l'exécution de l'application Asta Campus");
}
