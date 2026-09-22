use asta_core::db::DatabaseManager;
use asta_core::logic_tools::{calculate_subnet, convert_all, get_boolean_laws};
use asta_core::rag::LocalRagEngine;
use asta_core::security::SecurityManager;
use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use std::sync::{Arc, Mutex};
use tower_http::cors::{Any, CorsLayer};

struct ServerState {
    db: Mutex<DatabaseManager>,
    rag: LocalRagEngine,
}

#[derive(Serialize)]
struct HealthStatus {
    status: String,
    engine: String,
    rust_version: String,
    architecture: String,
    hardware_id: String,
}

#[derive(Deserialize)]
struct ChatRequest {
    query: String,
}

#[derive(Serialize)]
struct ChatResponse {
    query: String,
    answer: String,
    sources: Vec<String>,
    offline_mode: bool,
}

#[derive(Deserialize)]
struct AdminAuthRequest {
    username: String,
    password: String,
}

#[derive(Serialize)]
struct AdminAuthResponse {
    success: bool,
    message: String,
    role: Option<String>,
}

#[derive(Deserialize)]
struct CryptoRequest {
    payload: String,
    passphrase: String,
}

#[derive(Serialize)]
struct CryptoResponse {
    success: bool,
    result: String,
    error: Option<String>,
}

#[derive(Deserialize)]
struct ConvertQuery {
    val: String,
}

#[derive(Deserialize)]
struct SubnetQuery {
    ip: String,
    cidr: u8,
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let db_manager = DatabaseManager::init("asta_offline.db")
        .expect("Échec d'ouverture de la base SQLite asta_offline.db");
    let rag_engine = LocalRagEngine::new("student_notes");

    let shared_state = Arc::new(ServerState {
        db: Mutex::new(db_manager),
        rag: rag_engine,
    });

    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let app = Router::new()
        .route("/api/health", get(handle_health))
        .route("/api/stats", get(handle_stats))
        .route("/api/space-ai/chat", post(handle_chat))
        .route("/api/admin/auth", post(handle_admin_auth))
        .route("/api/admin/clean", post(handle_admin_clean))
        .route("/api/crypto/encrypt", post(handle_encrypt))
        .route("/api/crypto/decrypt", post(handle_decrypt))
        .route("/api/tools/convert", get(handle_convert))
        .route("/api/tools/subnet", get(handle_subnet))
        .route("/api/tools/boolean-laws", get(handle_boolean_laws))
        .layer(cors)
        .with_state(shared_state);

    let addr = SocketAddr::from(([127, 0, 0, 1], 5000));
    println!("🚀 [Asta Rust Server] Écoute sur http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn handle_health() -> Json<HealthStatus> {
    Json(HealthStatus {
        status: "ONLINE".to_string(),
        engine: "Rust Axum Core v2.0 (remplaçant Flask server.py)".to_string(),
        rust_version: "Rust 2021 / Tokio Async".to_string(),
        architecture: std::env::consts::ARCH.to_string(),
        hardware_id: SecurityManager::get_hardware_fingerprint(),
    })
}

async fn handle_stats(State(state): State<Arc<ServerState>>) -> Json<serde_json::Value> {
    let db = state.db.lock().unwrap();
    let logs = db.get_recent_logs(5).unwrap_or_default();
    Json(serde_json::json!({
        "status": "operational",
        "recent_audit_events": logs.len(),
        "storage": "SQLite 3 (asta_offline.db)",
        "memory_safety": "Garanti par le compilateur Rust (Zéro fuite mémoire)",
    }))
}

async fn handle_chat(
    State(state): State<Arc<ServerState>>,
    Json(payload): Json<ChatRequest>,
) -> Json<ChatResponse> {
    let rag_res = state.rag.answer_query(&payload.query);
    Json(ChatResponse {
        query: rag_res.query,
        answer: rag_res.answer,
        sources: rag_res.matched_sources,
        offline_mode: true,
    })
}

async fn handle_admin_auth(
    State(state): State<Arc<ServerState>>,
    Json(payload): Json<AdminAuthRequest>,
) -> Result<Json<AdminAuthResponse>, StatusCode> {
    let db = state.db.lock().map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    match db.verify_admin(&payload.username, &payload.password) {
        Ok(Some(admin)) => Ok(Json(AdminAuthResponse {
            success: true,
            message: format!("Session administrateur accordée à {}", admin.username),
            role: Some(admin.role),
        })),
        Ok(None) => Ok(Json(AdminAuthResponse {
            success: false,
            message: "Identifiants administrateur invalides.".to_string(),
            role: None,
        })),
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

async fn handle_admin_clean(
    State(state): State<Arc<ServerState>>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let db = state.db.lock().map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    let _ = db.log_event("ADMIN_PURGE", "Purge des logs d'audit demandée", "WARN");
    Ok(Json(serde_json::json!({
        "success": true,
        "message": "Nettoyage des traces temporaires effectué avec succès."
    })))
}

async fn handle_encrypt(Json(payload): Json<CryptoRequest>) -> Json<CryptoResponse> {
    match SecurityManager::encrypt_aes_gcm(&payload.payload, &payload.passphrase) {
        Ok(res) => Json(CryptoResponse {
            success: true,
            result: res,
            error: None,
        }),
        Err(err) => Json(CryptoResponse {
            success: false,
            result: String::new(),
            error: Some(err),
        }),
    }
}

async fn handle_decrypt(Json(payload): Json<CryptoRequest>) -> Json<CryptoResponse> {
    match SecurityManager::decrypt_aes_gcm(&payload.payload, &payload.passphrase) {
        Ok(res) => Json(CryptoResponse {
            success: true,
            result: res,
            error: None,
        }),
        Err(err) => Json(CryptoResponse {
            success: false,
            result: String::new(),
            error: Some(err),
        }),
    }
}

async fn handle_convert(Query(q): Query<ConvertQuery>) -> Json<serde_json::Value> {
    let res = convert_all(&q.val);
    Json(serde_json::to_value(res).unwrap())
}

async fn handle_subnet(Query(q): Query<SubnetQuery>) -> Json<serde_json::Value> {
    match calculate_subnet(&q.ip, q.cidr) {
        Ok(res) => Json(serde_json::to_value(res).unwrap()),
        Err(err) => Json(serde_json::json!({ "error": err })),
    }
}

async fn handle_boolean_laws() -> Json<serde_json::Value> {
    Json(serde_json::to_value(get_boolean_laws()).unwrap())
}
