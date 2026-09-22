import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Cpu,
  Lock,
  Unlock,
  ShieldCheck,
  HardDrive,
  Key,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Terminal,
  Layers,
  FileCode,
} from 'lucide-react';
import { tauriBridge, type SystemMetrics, type AdminAuthResult, type CryptoResult } from '../services/tauriBridge';

export const NativeArchitectureView: React.FC = () => {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [loadingMetrics, setLoadingMetrics] = useState<boolean>(false);

  // Formulaire d'authentification admin offline
  const [adminUsername, setAdminUsername] = useState<string>('Christian Alvaro');
  const [adminPassword, setAdminPassword] = useState<string>('unashmoh2028');
  const [authStatus, setAuthStatus] = useState<AdminAuthResult | null>(null);
  const [isVerifying, setIsVerifying] = useState<boolean>(false);

  // Atelier Cryptographique AES-256-GCM
  const [rawText, setRawText] = useState<string>(
    '// EXAMEN PRATIQUE UNASMOH 2028\nint main() { printf("Asta Secure Core\\n"); return 0; }'
  );
  const [passphrase, setPassphrase] = useState<string>('AstaSecKey_2028_Unasmoh');
  const [encryptedPayload, setEncryptedPayload] = useState<string>('');
  const [decryptedText, setDecryptedText] = useState<string>('');
  const [cryptoError, setCryptoError] = useState<string>('');

  const refreshMetrics = async () => {
    setLoadingMetrics(true);
    try {
      const data = await tauriBridge.getSystemMetrics();
      setMetrics(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingMetrics(false);
    }
  };

  useEffect(() => {
    let isMounted = true;
    tauriBridge.getSystemMetrics().then((data) => {
      if (isMounted) setMetrics(data);
    }).catch(console.error);

    return () => {
      isMounted = false;
    };
  }, []);

  const handleTestAuth = async () => {
    setIsVerifying(true);
    setAuthStatus(null);
    try {
      const result = await tauriBridge.authenticateAdmin(adminUsername, adminPassword);
      setAuthStatus(result);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : String(e);
      setAuthStatus({
        success: false,
        message: `Erreur d'exécution: ${msg}`,
      });
    } finally {
      setIsVerifying(false);
    }
  };

  const handleEncrypt = async () => {
    setCryptoError('');
    if (!passphrase.trim()) {
      setCryptoError('Veuillez spécifier une phrase secrète de dérivation.');
      return;
    }
    const res: CryptoResult = await tauriBridge.encryptPayload(rawText, passphrase);
    if (res.success) {
      setEncryptedPayload(res.result);
      setDecryptedText('');
    } else {
      setCryptoError(res.error || 'Échec du chiffrement.');
    }
  };

  const handleDecrypt = async () => {
    setCryptoError('');
    if (!encryptedPayload.trim()) {
      setCryptoError('Aucun bloc chiffré à déchiffrer.');
      return;
    }
    const res: CryptoResult = await tauriBridge.decryptPayload(encryptedPayload, passphrase);
    if (res.success) {
      setDecryptedText(res.result);
    } else {
      setCryptoError(res.error || 'Échec du déchiffrement.');
    }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      {/* Header */}
      <div className="view-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h2>
            <Cpu size={24} color="#38bdf8" /> Architecture Native & Sécurité Offline (Rust / C++ / C#)
          </h2>
          <p>
            Moteur de performance de nouvelle génération : Core Rust (Tauri v2), SQLite chiffré, ponts FFI et cryptographie matérielle.
          </p>
        </div>
        <button
          onClick={refreshMetrics}
          className="btn-primary"
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.45rem 0.9rem', fontSize: '0.85rem' }}
          disabled={loadingMetrics}
        >
          <RefreshCw size={14} className={loadingMetrics ? 'animate-spin' : ''} />
          <span>Rafraîchir les sondes</span>
        </button>
      </div>

      {/* Cartes de statuts multi-langages */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        {/* Module Rust */}
        <div style={{ background: '#0e1526', border: '1px solid rgba(56, 189, 248, 0.25)', borderRadius: '10px', padding: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#38bdf8', fontWeight: 600 }}>
              <Cpu size={16} />
              <span>Rust Core (src-tauri)</span>
            </div>
            <span style={{ fontSize: '0.7rem', background: '#0369a1', color: '#fff', padding: '2px 6px', borderRadius: '4px' }}>
              Actif
            </span>
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--subtext)', lineHeight: '1.4' }}>
            Gestionnaire IPC Tauri v2, allocation mémoire sécurisée, threads asynchrones et boucle d'événements.
          </div>
          <div style={{ marginTop: '0.6rem', fontSize: '0.72rem', fontFamily: 'monospace', color: '#7dd3fc' }}>
            {metrics?.rustVersion || 'Rust 1.80+ / Cargo Engine'}
          </div>
        </div>

        {/* Module SQLite Offline */}
        <div style={{ background: '#0e1526', border: '1px solid rgba(34, 197, 94, 0.25)', borderRadius: '10px', padding: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#22c55e', fontWeight: 600 }}>
              <HardDrive size={16} />
              <span>SQLite 3 Offline</span>
            </div>
            <span style={{ fontSize: '0.7rem', background: '#15803d', color: '#fff', padding: '2px 6px', borderRadius: '4px' }}>
              Chiffré
            </span>
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--subtext)', lineHeight: '1.4' }}>
            Persistance locale sans serveur (rusqlite), tables de clés, licences machines et audit trail inviolable.
          </div>
          <div style={{ marginTop: '0.6rem', fontSize: '0.72rem', fontFamily: 'monospace', color: '#86efac' }}>
            Fichier : asta_offline.db (WAL Mode)
          </div>
        </div>

        {/* Module C (C99) */}
        <div style={{ background: '#0e1526', border: '1px solid rgba(245, 158, 11, 0.25)', borderRadius: '10px', padding: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#f59e0b', fontWeight: 600 }}>
              <FileCode size={16} />
              <span>Module C (c/asta_crypto)</span>
            </div>
            <span style={{ fontSize: '0.7rem', background: '#b45309', color: '#fff', padding: '2px 6px', borderRadius: '4px' }}>
              Zero-Alloc
            </span>
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--subtext)', lineHeight: '1.4' }}>
            Fonctions <code style={{ color: '#fcd34d' }}>asta_secure_zero</code>, empreinte machine bas niveau et checksums polynomiaux.
          </div>
          <div style={{ marginTop: '0.6rem', fontSize: '0.72rem', fontFamily: 'monospace', color: '#fde68a' }}>
            ABI : C99 standard (libasta_crypto.a)
          </div>
        </div>

        {/* Module C++17 & C# */}
        <div style={{ background: '#0e1526', border: '1px solid rgba(168, 85, 247, 0.25)', borderRadius: '10px', padding: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#a855f7', fontWeight: 600 }}>
              <Layers size={16} />
              <span>C++17 & C# Interop</span>
            </div>
            <span style={{ fontSize: '0.7rem', background: '#7e22ce', color: '#fff', padding: '2px 6px', borderRadius: '4px' }}>
              P/Invoke
            </span>
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--subtext)', lineHeight: '1.4' }}>
            Indexeur ultra-rapide <code style={{ color: '#d8b4fe' }}>FastIndexEngine</code> (cpp/) et ponts managés C# (.NET 8).
          </div>
          <div style={{ marginTop: '0.6rem', fontSize: '0.72rem', fontFamily: 'monospace', color: '#e9d5ff' }}>
            NativeInterop.cs & asta_engine.dll
          </div>
        </div>
      </div>

      {/* Grille de 2 colonnes : Sécurité Offline & Atelier Crypto */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '1.25rem' }}>
        {/* COLONNE 1 : Contrôle Administrateur Offline & Empreinte Machine */}
        <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <ShieldCheck size={18} color="#22c55e" />
            <h3 style={{ fontSize: '1.05rem', color: '#f8fafc', fontWeight: 600 }}>
              Contrôle Administrateur Offline (SQLite & HWID)
            </h3>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--subtext)', marginBottom: '1rem', lineHeight: '1.5' }}>
            Vérification cryptographique locale sans connexion Internet. Le compte administrateur est salé et lié à l'empreinte matérielle de la machine.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--subtext)', marginBottom: '0.3rem' }}>
                Empreinte Machine Détectée (HWID Matériel)
              </label>
              <div style={{
                background: '#070a11',
                border: '1px solid rgba(255, 255, 255, 0.08)',
                padding: '0.5rem 0.75rem',
                borderRadius: '6px',
                fontFamily: 'monospace',
                fontSize: '0.78rem',
                color: '#38bdf8',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
              }}>
                <span>{metrics?.hardwareId || 'ASTA-HWID-CALCULATING...'}</span>
                <span style={{ fontSize: '0.68rem', color: '#22c55e' }}>Verrouillé</span>
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--subtext)', marginBottom: '0.3rem' }}>
                Identifiant Administrateur
              </label>
              <input
                type="text"
                value={adminUsername}
                onChange={(e) => setAdminUsername(e.target.value)}
                style={{
                  width: '100%',
                  background: '#070a11',
                  border: '1px solid var(--border)',
                  color: '#fff',
                  padding: '0.5rem 0.75rem',
                  borderRadius: '6px',
                  fontSize: '0.85rem',
                  outline: 'none',
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--subtext)', marginBottom: '0.3rem' }}>
                Mot de Passe Hors-Ligne (Défaut démo: unashmoh2028)
              </label>
              <input
                type="password"
                value={adminPassword}
                onChange={(e) => setAdminPassword(e.target.value)}
                style={{
                  width: '100%',
                  background: '#070a11',
                  border: '1px solid var(--border)',
                  color: '#fff',
                  padding: '0.5rem 0.75rem',
                  borderRadius: '6px',
                  fontSize: '0.85rem',
                  outline: 'none',
                }}
              />
            </div>

            <button
              onClick={handleTestAuth}
              disabled={isVerifying}
              className="btn-primary"
              style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', marginTop: '0.4rem' }}
            >
              <Key size={15} />
              <span>{isVerifying ? 'Vérification en cours...' : 'Tester Authentification SQLite Offline'}</span>
            </button>

            {authStatus && (
              <div
                style={{
                  padding: '0.75rem',
                  borderRadius: '8px',
                  fontSize: '0.82rem',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.5rem',
                  background: authStatus.success ? 'rgba(34, 197, 94, 0.12)' : 'rgba(239, 68, 68, 0.12)',
                  border: `1px solid ${authStatus.success ? 'rgba(34, 197, 94, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
                  color: authStatus.success ? '#86efac' : '#fca5a5',
                }}
              >
                {authStatus.success ? <CheckCircle2 size={16} /> : <AlertTriangle size={16} />}
                <div>
                  <div style={{ fontWeight: 600 }}>{authStatus.message}</div>
                  {authStatus.role && (
                    <div style={{ fontSize: '0.72rem', marginTop: '0.2rem', opacity: 0.9 }}>
                      Rôle validé : {authStatus.role} • Table SQLite : <code style={{ color: '#fff' }}>admin_credentials</code>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* COLONNE 2 : Chiffrement Local de Codes & Payloads (AES-256-GCM) */}
        <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <Lock size={18} color="#f59e0b" />
            <h3 style={{ fontSize: '1.05rem', color: '#f8fafc', fontWeight: 600 }}>
              Atelier Cryptographique Natif (AES-256-GCM)
            </h3>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--subtext)', marginBottom: '1rem', lineHeight: '1.5' }}>
            Chiffrement authentifié de code source, devoirs et clés locales. Protège les données contre les altérations et l'extraction non autorisée.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--subtext)', marginBottom: '0.3rem' }}>
                Code source ou Payload à protéger
              </label>
              <textarea
                rows={3}
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                style={{
                  width: '100%',
                  background: '#070a11',
                  border: '1px solid var(--border)',
                  color: '#4ade80',
                  padding: '0.5rem 0.75rem',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  fontFamily: 'monospace',
                  outline: 'none',
                  resize: 'none',
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--subtext)', marginBottom: '0.3rem' }}>
                Phrase secrète de dérivation (PBKDF2 / SHA-256)
              </label>
              <input
                type="text"
                value={passphrase}
                onChange={(e) => setPassphrase(e.target.value)}
                style={{
                  width: '100%',
                  background: '#070a11',
                  border: '1px solid var(--border)',
                  color: '#f59e0b',
                  padding: '0.45rem 0.75rem',
                  borderRadius: '6px',
                  fontSize: '0.85rem',
                  fontFamily: 'monospace',
                  outline: 'none',
                }}
              />
            </div>

            <div style={{ display: 'flex', gap: '0.6rem' }}>
              <button
                onClick={handleEncrypt}
                className="btn-primary"
                style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem', background: '#0284c7' }}
              >
                <Lock size={14} /> Chiffrer (AES-GCM)
              </button>
              <button
                onClick={handleDecrypt}
                className="filter-tab"
                style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}
              >
                <Unlock size={14} /> Déchiffrer
              </button>
            </div>

            {cryptoError && (
              <div style={{ color: '#ef4444', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <AlertTriangle size={14} /> {cryptoError}
              </div>
            )}

            {encryptedPayload && (
              <div>
                <label style={{ display: 'block', fontSize: '0.75rem', color: '#38bdf8', marginBottom: '0.25rem', fontWeight: 600 }}>
                  Résultat Chiffré Base64 (IV 12o + Tag 16o + Ciphertext) :
                </label>
                <div style={{
                  background: '#070a11',
                  border: '1px solid rgba(56, 189, 248, 0.3)',
                  padding: '0.5rem',
                  borderRadius: '6px',
                  fontSize: '0.72rem',
                  fontFamily: 'monospace',
                  color: '#94a3b8',
                  wordBreak: 'break-all',
                  maxHeight: '70px',
                  overflowY: 'auto',
                }}>
                  {encryptedPayload}
                </div>
              </div>
            )}

            {decryptedText && (
              <div>
                <label style={{ display: 'block', fontSize: '0.75rem', color: '#4ade80', marginBottom: '0.25rem', fontWeight: 600 }}>
                  Code déchiffré avec succès (Intégrité confirmée) :
                </label>
                <pre style={{
                  background: '#070a11',
                  border: '1px solid rgba(74, 222, 128, 0.3)',
                  padding: '0.5rem',
                  borderRadius: '6px',
                  fontSize: '0.75rem',
                  color: '#e2e8f0',
                  margin: 0,
                  whiteSpace: 'pre-wrap',
                }}>
                  {decryptedText}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Journal d'audit & sécurité SQLite en direct */}
      <div style={{ marginTop: '1.25rem', background: '#0b0f19', border: '1px solid var(--border)', borderRadius: '10px', padding: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#f8fafc', fontWeight: 600, fontSize: '0.9rem' }}>
            <Terminal size={16} color="#38bdf8" />
            <span>Journal d'Audit de Sécurité SQLite (Table: security_audit_logs)</span>
          </div>
          <span style={{ fontSize: '0.72rem', color: 'var(--subtext)' }}>Signatures HMAC SHA-256 Actives</span>
        </div>

        <table className="data-table" style={{ fontSize: '0.78rem' }}>
          <thead>
            <tr>
              <th style={{ width: '120px' }}>Type d'Événement</th>
              <th>Détails de l'Audit</th>
              <th style={{ width: '90px' }}>Gravité</th>
              <th style={{ width: '130px' }}>Signature intégrité</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span className="badge-tag badge-blue">SYSTEM_INIT</span></td>
              <td>Création automatique du compte Administrateur Offline (Christian Alvaro)</td>
              <td><span style={{ color: '#38bdf8' }}>INFO</span></td>
              <td><code style={{ color: '#64748b' }}>e4b9...120f</code></td>
            </tr>
            <tr>
              <td><span className="badge-tag badge-purple">DB_MIGRATE</span></td>
              <td>Initialisation des tables: admin_credentials, security_audit_logs, offline_licenses</td>
              <td><span style={{ color: '#38bdf8' }}>INFO</span></td>
              <td><code style={{ color: '#64748b' }}>7f1a...998c</code></td>
            </tr>
            <tr>
              <td><span className="badge-tag badge-green">CRYPTO_ARMED</span></td>
              <td>Moteur AES-256-GCM armé avec dérivation PBKDF2 et sel machine</td>
              <td><span style={{ color: '#22c55e' }}>INFO</span></td>
              <td><code style={{ color: '#64748b' }}>33cd...aa41</code></td>
            </tr>
          </tbody>
        </table>
      </div>
    </motion.div>
  );
};
