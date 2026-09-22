use asta_core::db::DatabaseManager;
use asta_core::logic_tools::{calculate_subnet, convert_all};
use asta_core::security::SecurityManager;
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "asta-cli")]
#[command(about = "Utilitaire d'administration et de sécurité Asta Académie (Rust Natif)", long_about = None)]
#[command(version = "2.0.0")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialise la base de données SQLite hors-ligne (remplaçant init_db.py)
    InitDb {
        #[arg(short, long, default_value = "asta_offline.db")]
        path: String,
    },
    /// Affiche l'identifiant matériel unique de la machine (Hardware ID)
    Hwid,
    /// Chiffre un bloc de texte ou de code en AES-256-GCM
    Encrypt {
        #[arg(short, long)]
        text: String,
        #[arg(short, long)]
        key: String,
    },
    /// Déchiffre un bloc au format ASTA-AES256GCM:<base64>
    Decrypt {
        #[arg(short, long)]
        payload: String,
        #[arg(short, long)]
        key: String,
    },
    /// Convertit un nombre sous toutes les bases (Dec, Bin, Hex, Oct)
    Convert {
        #[arg(short, long)]
        value: String,
    },
    /// Calcule le masque, réseau, broadcast et plages pour un sous-réseau IPv4
    Subnet {
        #[arg(short, long)]
        ip: String,
        #[arg(short, long)]
        cidr: u8,
    },
    /// Affiche les derniers événements de la table d'audit SQLite
    Audit {
        #[arg(short, long, default_value_t = 10)]
        limit: usize,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::InitDb { path } => {
            println!("Initialisation de la base SQLite native : {}...", path);
            match DatabaseManager::init(&path) {
                Ok(_) => println!("✅ Base de données initialisée avec succès avec compte admin et tables d'audit."),
                Err(e) => eprintln!("❌ Échec d'initialisation : {}", e),
            }
        }
        Commands::Hwid => {
            let hwid = SecurityManager::get_hardware_fingerprint();
            println!("Empreinte matérielle (HWID) : {}", hwid);
        }
        Commands::Encrypt { text, key } => {
            match SecurityManager::encrypt_aes_gcm(&text, &key) {
                Ok(res) => println!("Résultat chiffré :\n{}", res),
                Err(e) => eprintln!("Erreur de chiffrement : {}", e),
            }
        }
        Commands::Decrypt { payload, key } => {
            match SecurityManager::decrypt_aes_gcm(&payload, &key) {
                Ok(res) => println!("Résultat déchiffré :\n{}", res),
                Err(e) => eprintln!("Erreur de déchiffrement : {}", e),
            }
        }
        Commands::Convert { value } => {
            let res = convert_all(&value);
            println!("{}", serde_json::to_string_pretty(&res).unwrap());
        }
        Commands::Subnet { ip, cidr } => {
            match calculate_subnet(&ip, cidr) {
                Ok(res) => println!("{}", serde_json::to_string_pretty(&res).unwrap()),
                Err(e) => eprintln!("Erreur sous-réseau : {}", e),
            }
        }
        Commands::Audit { limit } => {
            if let Ok(db) = DatabaseManager::init("asta_offline.db") {
                if let Ok(logs) = db.get_recent_logs(limit) {
                    println!("Derniers {} enregistrements d'audit :", logs.len());
                    for log in logs {
                        println!("[{}] [{}] {} - {}", log.timestamp, log.severity, log.event_type, log.details);
                    }
                }
            } else {
                eprintln!("Impossible d'ouvrir asta_offline.db");
            }
        }
    }
}
