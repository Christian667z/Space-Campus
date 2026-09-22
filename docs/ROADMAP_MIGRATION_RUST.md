# Feuille de Route : Refonte Architecturale Majeure "Asta Campus"
## Transition vers Rust, Tauri v2, Multi-Langages (C/C++/C#) et Frontend Moderne

---

### 1. Vision et Objectifs de la Refonte

L'application **Asta Campus** passe d'un prototype basé sur Python (CustomTkinter/Qt) à une architecture logicielle de niveau professionnel, ultra-réactive, sécurisée hors-ligne et modulaire.

```
+─────────────────────────────────────────────────────────────────────────+
|               FRONTEND MODERNE (HTML5 / TypeScript / CSS3)              |
|        UI Desktop Sombre • Tailwind • React • Animations Fluides        |
+─────────────────────────────────────────────────────────────────────────+
                                    │
                         IPC Tauri v2 (Type-Safe)
                                    │
+─────────────────────────────────────────────────────────────────────────+
|                     CORE APPLICATIF RUST (src-tauri)                    |
|   • Gestionnaire de fenêtres & Cycle de vie Desktop                     |
|   • Moteur SQLite Offline (rusqlite) & Audits Chiffrés                  |
|   • Cryptographie Haute Sécurité : AES-256-GCM & SHA-256                |
|   • Empreinte Machine (Hardware ID / UUID) & Licence Offline            |
+─────────────────────────────────────────────────────────────────────────+
          │                                              │
     Rust FFI (extern "C")                         C# P/Invoke
          │                                              │
+───────────────────────────+                  +──────────────────────────+
|  MODULES NATIFS C / C++   |                  |    MODULE C# (.NET 8)    |
| • c/ : asta_crypto (C99)  |                  | • Interopérabilité Win32 |
|   Zero-alloc & Memzero    |                  | • AstaAdminSecurity.cs   |
| • cpp/ : asta_engine (17) |                  | • Launcher & Fallback    |
|   Indexation SIMD/Cache   |                  |   WPF natif              |
+───────────────────────────+                  +──────────────────────────+
```

---

### 2. Planning d'Exécution en 4 Phases

#### Phase 1 : Cœur Rust & Cryptographie Native (Jalon Actuel)
1. Mise en place du module `src-tauri/` avec Cargo, configuration Tauri v2, et gestionnaire de commandes IPC.
2. Implémentation du moteur SQLite embarqué (`asta_offline.db`) avec table des administrateurs et audits inviolables.
3. Implémentation du chiffrement AES-256-GCM natif et de la dérivation d'empreinte matérielle pour le contrôle administrateur hors-ligne.

#### Phase 2 : Modules Bas Niveau C / C++ & FFI
1. **Dossier `c/`** : Bibliothèque `asta_crypto` (C99/C11) pour l'empreinte matérielle brute, le hachage sécurisé et le nettoyage de mémoire volatile (`asta_secure_zero`).
2. **Dossier `cpp/`** : Moteur de recherche et d'indexation en mémoire (`asta_engine`) pour les cours et les bases de données volumineuses.
3. Liaison FFI (`extern "C"`) liant Rust aux DLLs/librairies partagées C et C++.

#### Phase 3 : Couche d'Interopérabilité C# (.NET)
1. Consolidation du dossier `interop/NativeInterop.cs` avec les signatures complètes P/Invoke (`[DllImport]`).
2. Création de la couche de service `AstaAdminSecurity.cs` pour le support Windows natif hors-ligne.

#### Phase 4 : Frontend Desktop & Interface
1. Intégration du pont IPC (`tauriBridge.ts`) avec détection automatique d'environnement (Desktop Tauri vs Web Preview).
2. Ajout de la barre de titre desktop avec contrôles natifs de fenêtre (réduction, plein écran, fermeture).
3. Panneau de supervision de l'architecture native et tests cryptographiques directs dans l'interface administrateur.

---

### 3. Modèle de Données SQLite Sécurisé (Offline Admin)

```sql
-- Table des identifiants Administrateur Offline
CREATE TABLE IF NOT EXISTS admin_credentials (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,       -- Hachage SHA-256 salé (ou Argon2id)
    salt TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'SuperAdmin',
    hardware_lock TEXT,                -- Empreinte machine autorisée
    created_at INTEGER NOT NULL,
    last_login INTEGER
);

-- Table du journal d'audit de sécurité
CREATE TABLE IF NOT EXISTS security_audit_logs (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,          -- LOGIN_SUCCESS, LOGIN_FAIL, KEY_EXPORT...
    details TEXT NOT NULL,
    severity TEXT NOT NULL,            -- INFO, WARN, CRITICAL
    timestamp INTEGER NOT NULL,
    signature TEXT NOT NULL            -- Signature HMAC pour intégrité
);

-- Table des licences offline
CREATE TABLE IF NOT EXISTS offline_licenses (
    license_key TEXT PRIMARY KEY,
    owner_name TEXT NOT NULL,
    hardware_id TEXT NOT NULL,
    features_mask INTEGER NOT NULL,
    expires_at INTEGER NOT NULL,
    is_revoked INTEGER NOT NULL DEFAULT 0
);
```

---

### 4. Spécifications des Signatures Cryptographiques & FFI

- **Algorithme de chiffrement** : AES-256-GCM (Nonce 12 octets, Tag d'authentification 16 octets).
- **Hachage de mot de passe** : PBKDF2-HMAC-SHA256 (100 000 itérations) ou Argon2id avec sel cryptographique de 16 octets.
- **Empreinte machine** : SHA-256 du CPU-ID + UUID Carte mère + Nom machine.
- **Conventions d'appel FFI** : `cdecl` / standard C ABI (`#[no_mangle] extern "C"` en Rust).
