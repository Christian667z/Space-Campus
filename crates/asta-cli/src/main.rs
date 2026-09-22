use asta_core::db::DatabaseManager;
use asta_core::logic_tools::{calculate_subnet, convert_all};
use asta_core::courses::CourseCatalog;
use asta_core::licenses::{LicenseManager, LicenseValidation};
use asta_core::security::SecurityManager;
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "asta-cli")]
#[command(about = "Utilitaire d'administration et de sécurité Asta Académie (Rust Natif)", long_about = None)]
#[command(version = "2.0.0")]
#[command(author = "Christian Alvaro <christian7alvaro@gmail.com>")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialise la base de données SQLite hors-ligne
    InitDb {
        #[arg(short, long, default_value = "asta_offline.db")]
        path: String,
    },

    /// Affiche l'identifiant matériel unique de la machine (Hardware ID)
    Hwid,

    /// Chiffre un bloc de texte ou de code en AES-256-GCM
    Encrypt {
        #[arg(short, long, help = "Texte à chiffrer")]
        text: String,
        #[arg(short, long, help = "Phrase secrète de chiffrement")]
        key: String,
    },

    /// Déchiffre un bloc au format ASTA-AES256GCM:<base64>
    Decrypt {
        #[arg(short, long, help = "Payload chiffré (format ASTA-AES256GCM:...)")]
        payload: String,
        #[arg(short, long, help = "Phrase secrète de déchiffrement")]
        key: String,
    },

    /// Convertit un nombre sous toutes les bases (Dec, Bin, Hex, Oct, ASCII)
    Convert {
        #[arg(short, long, help = "Valeur à convertir (ex: 42, 0xFF, 0b1010)")]
        value: String,
    },

    /// Calcule le masque, réseau, broadcast et plages pour un sous-réseau IPv4
    Subnet {
        #[arg(short, long, help = "Adresse IP (ex: 192.168.1.0)")]
        ip: String,
        #[arg(short, long, help = "Préfixe CIDR (0-32)")]
        cidr: u8,
    },

    /// Affiche les derniers événements de la table d'audit SQLite
    Audit {
        #[arg(short, long, default_value_t = 10, help = "Nombre d'événements à afficher")]
        limit: usize,
        #[arg(short, long, default_value = "asta_offline.db")]
        db: String,
    },

    /// Génère une clé de licence hors-ligne pour un utilisateur
    License {
        #[command(subcommand)]
        action: LicenseAction,
    },

    /// Affiche le catalogue des cours académiques intégrés
    Courses {
        #[arg(short, long, help = "Rechercher un cours par mot-clé")]
        search: Option<String>,
        #[arg(short, long, help = "Afficher le détail complet d'un cours (ID)")]
        id: Option<String>,
    },
}

#[derive(Subcommand)]
enum LicenseAction {
    /// Génère une nouvelle clé de licence
    Generate {
        #[arg(short, long, help = "Nom du propriétaire de la licence")]
        owner: String,
    },
    /// Enregistre une licence dans la base de données locale
    Register {
        #[arg(short, long, help = "Clé de licence à enregistrer")]
        key: String,
        #[arg(short, long, default_value = "asta_offline.db")]
        db: String,
    },
    /// Valide une licence existante sur cette machine
    Validate {
        #[arg(short, long, help = "Clé de licence à valider")]
        key: String,
        #[arg(short, long, default_value = "asta_offline.db")]
        db: String,
    },
    /// Liste toutes les licences enregistrées localement
    List {
        #[arg(short, long, default_value = "asta_offline.db")]
        db: String,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        // ── Base de données ───────────────────────────────────────────────────
        Commands::InitDb { path } => {
            println!("🗄️  Initialisation de la base SQLite : {}...", path);
            match DatabaseManager::init(&path) {
                Ok(_) => println!("✅ Base de données initialisée avec succès (tables : admin_credentials, security_audit_logs, offline_licenses)."),
                Err(e) => eprintln!("❌ Échec d'initialisation : {}", e),
            }
        }

        // ── Empreinte matérielle ──────────────────────────────────────────────
        Commands::Hwid => {
            let hwid = SecurityManager::get_hardware_fingerprint();
            println!("🔐 Empreinte matérielle (HWID) :");
            println!("   {}", hwid);
        }

        // ── Cryptographie ─────────────────────────────────────────────────────
        Commands::Encrypt { text, key } => {
            match SecurityManager::encrypt_aes_gcm(&text, &key) {
                Ok(res) => {
                    println!("🔒 Résultat chiffré (AES-256-GCM) :");
                    println!("   {}", res);
                }
                Err(e) => eprintln!("❌ Erreur de chiffrement : {}", e),
            }
        }

        Commands::Decrypt { payload, key } => {
            match SecurityManager::decrypt_aes_gcm(&payload, &key) {
                Ok(res) => {
                    println!("🔓 Résultat déchiffré :");
                    println!("   {}", res);
                }
                Err(e) => eprintln!("❌ Erreur de déchiffrement : {}", e),
            }
        }

        // ── Conversion de bases ───────────────────────────────────────────────
        Commands::Convert { value } => {
            let res = convert_all(&value);
            println!("🔢 Conversion de « {} » :", value);
            if let Some(dec) = res.decimal {
                println!("   Décimal     : {}", dec);
                println!("   Binaire     : 0b{}", res.binary.unwrap_or_default());
                println!("   Octal       : 0o{}", res.octal.unwrap_or_default());
                println!("   Hexadécimal : 0x{}", res.hexadecimal.unwrap_or_default());
                if let Some(ascii) = res.ascii {
                    println!("   ASCII       : '{}'", ascii);
                }
            } else if let Some(err) = res.error {
                eprintln!("❌ {}", err);
            }
        }

        // ── Sous-réseaux IPv4 ─────────────────────────────────────────────────
        Commands::Subnet { ip, cidr } => {
            match calculate_subnet(&ip, cidr) {
                Ok(res) => {
                    println!("🌐 Sous-réseau IPv4 — {}/{}", ip, cidr);
                    println!("   Masque de sous-réseau : {}", res.netmask);
                    println!("   Adresse réseau        : {}", res.network_address);
                    println!("   Adresse de broadcast  : {}", res.broadcast_address);
                    println!("   Premier hôte          : {}", res.first_host);
                    println!("   Dernier hôte          : {}", res.last_host);
                    println!("   Hôtes totaux          : {}", res.total_hosts);
                    println!("   Hôtes utilisables     : {}", res.usable_hosts);
                }
                Err(e) => eprintln!("❌ Erreur : {}", e),
            }
        }

        // ── Audit ─────────────────────────────────────────────────────────────
        Commands::Audit { limit, db } => {
            match DatabaseManager::init(&db) {
                Ok(manager) => match manager.get_recent_logs(limit) {
                    Ok(logs) => {
                        println!("📋 Derniers {} événements d'audit :", logs.len());
                        println!("{:-<80}", "");
                        for log in logs {
                            println!(
                                "[{}] [{:>4}] {:20} — {}",
                                log.timestamp, log.severity, log.event_type, log.details
                            );
                        }
                    }
                    Err(e) => eprintln!("❌ Erreur lecture logs : {}", e),
                },
                Err(e) => eprintln!("❌ Impossible d'ouvrir {} : {}", db, e),
            }
        }

        // ── Licences ──────────────────────────────────────────────────────────
        Commands::License { action } => match action {
            LicenseAction::Generate { owner } => {
                let hwid = SecurityManager::get_hardware_fingerprint();
                let key = LicenseManager::generate_license_key(&owner, &hwid);
                println!("🪪  Nouvelle clé de licence générée pour « {} » :", owner);
                println!("   {}", key);
                println!("   HWID verrouillé : {}", hwid);
            }

            LicenseAction::Register { key, db } => {
                match DatabaseManager::init(&db) {
                    Ok(manager) => {
                        let lm = LicenseManager::new(&manager);
                        match lm.register_license("Utilisateur", &key) {
                            Ok(_) => println!("✅ Licence {} enregistrée avec succès.", key),
                            Err(e) => eprintln!("❌ Erreur d'enregistrement : {}", e),
                        }
                    }
                    Err(e) => eprintln!("❌ Impossible d'ouvrir {} : {}", db, e),
                }
            }

            LicenseAction::Validate { key, db } => {
                match DatabaseManager::init(&db) {
                    Ok(manager) => {
                        let lm = LicenseManager::new(&manager);
                        match lm.validate_license(&key) {
                            Ok(LicenseValidation { valid, message, machine_match, .. }) => {
                                let icon = if valid { "✅" } else { "❌" };
                                println!("{} Validation de la licence {} :", icon, key);
                                println!("   Valide          : {}", valid);
                                println!("   Machine correcte: {}", machine_match);
                                println!("   Message         : {}", message);
                            }
                            Err(e) => eprintln!("❌ Erreur de validation : {}", e),
                        }
                    }
                    Err(e) => eprintln!("❌ Impossible d'ouvrir {} : {}", db, e),
                }
            }

            LicenseAction::List { db } => {
                match DatabaseManager::init(&db) {
                    Ok(manager) => {
                        let lm = LicenseManager::new(&manager);
                        match lm.list_licenses() {
                            Ok(licenses) => {
                                println!("📄 Licences enregistrées ({}) :", licenses.len());
                                println!("{:-<80}", "");
                                for lic in licenses {
                                    let status = if lic.is_active { "ACTIVE" } else { "RÉVOQUÉE" };
                                    println!("[{}] {} — Activée le: {}", status, lic.license_key, lic.activation_date);
                                }
                            }
                            Err(e) => eprintln!("❌ Erreur : {}", e),
                        }
                    }
                    Err(e) => eprintln!("❌ Impossible d'ouvrir {} : {}", db, e),
                }
            }
        },

        // ── Cours ─────────────────────────────────────────────────────────────
        Commands::Courses { search, id } => {
            let catalog = CourseCatalog::new();

            if let Some(course_id) = id {
                match catalog.get_course(&course_id) {
                    Some(course) => {
                        println!("📚 {} [{}]", course.title, course.level);
                        println!("   Matière     : {}", course.subject);
                        println!("   Description : {}", course.description);
                        println!("   Tags        : {}", course.tags.join(", "));
                        println!("\n   Chapitres ({}) :", course.chapters.len());
                        for ch in &course.chapters {
                            println!("\n   {}. {}", ch.index, ch.title);
                            println!("      {}", ch.content);
                            for ex in &ch.code_examples {
                                println!("\n      [{}] {}", ex.language.to_uppercase(), ex.description);
                                println!("      ```{}", ex.language);
                                for line in ex.code.lines() {
                                    println!("      {}", line);
                                }
                                println!("      ```");
                            }
                        }
                    }
                    None => eprintln!("❌ Aucun cours trouvé avec l'ID : {}", course_id),
                }
            } else {
                let courses = if let Some(q) = search {
                    println!("🔍 Résultats pour « {} » :", q);
                    catalog.search_courses(&q)
                } else {
                    println!("📚 Catalogue des cours UNASMOH ({}) :", catalog.list_courses().len());
                    catalog.list_courses()
                };

                println!("{:-<80}", "");
                for c in &courses {
                    println!(
                        "  [{:25}] {:40} | {:^15} | {} chapitres",
                        c.id, c.title, c.level, c.chapter_count
                    );
                    println!("                              Tags: {}", c.tags.join(", "));
                }
                if courses.is_empty() {
                    println!("  Aucun cours trouvé.");
                } else {
                    println!("\n  💡 Utilisez --id <ID> pour afficher le détail complet d'un cours.");
                }
            }
        }
    }
}
