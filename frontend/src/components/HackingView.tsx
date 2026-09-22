import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ShieldAlert, CheckCircle2, AlertTriangle, Key } from 'lucide-react';

interface CTFChallenge {
  id: string;
  title: string;
  category: string;
  difficulty: string;
  desc: string;
  flag: string;
  xp: number;
  hint: string;
}

const CTF_CHALLENGES: CTFChallenge[] = [
  {
    id: 'ctf_01',
    title: 'Mission 01 : Reconnaissance d\'Adressage IPv4 Local',
    category: 'Réseaux & Reconnaissance',
    difficulty: 'Facile',
    desc: "Identifier l'adresse de bouclage standard (loopback) utilisée par convention dans la pile TCP/IP.",
    flag: '127.0.0.1',
    xp: 50,
    hint: "Consultez le cours L3 Réseaux ou tapez l'adresse IP locale réservée pour 'localhost'.",
  },
  {
    id: 'ctf_02',
    title: 'Mission 02 : Injection SQL Basique (Auth Bypass)',
    category: 'Web Exploitation',
    difficulty: 'Facile',
    desc: "Quel est le payload d'authentification SQL le plus célèbre qui force une condition toujours vraie ('OR 1=1') ?",
    flag: "' OR 1=1 --",
    xp: 75,
    hint: "Composé d'un guillemet simple, du mot-clé OR, de 1=1 et du symbole de commentaire SQL.",
  },
  {
    id: 'ctf_03',
    title: 'Mission 03 : Modèle OSI - Couche Transport',
    category: 'Architecture Réseau',
    difficulty: 'Moyen',
    desc: "Quel est le numéro de couche dans le modèle OSI (1 à 7) correspondant au protocole TCP et UDP (Transport) ?",
    flag: '4',
    xp: 50,
    hint: "Couches : 1: Physique, 2: Liaison, 3: Réseau, 4: Transport...",
  },
  {
    id: 'ctf_04',
    title: 'Mission 04 : Cryptographie - Hash SHA-256 Longueur',
    category: 'Cryptographie',
    difficulty: 'Moyen',
    desc: "Combien de caractères hexadécimaux compose exactement la signature d'un hash SHA-256 ?",
    flag: '64',
    xp: 80,
    hint: "256 bits divisés par 4 bits par caractère hexadécimal = ?",
  },
];

const SECURITY_TOPICS = [
  {
    id: 'sqli',
    title: '1. Injection SQL (SQLi)',
    tag: 'OWASP #03',
    desc: "L'injection SQL se produit lorsque des entrées utilisateur non assainies sont concaténées directement dans des requêtes SQL dynamiques.",
    vulnExample: `// Vulnérable:
const query = "SELECT * FROM users WHERE email = '" + req.body.email + "' AND pass = '" + req.body.pass + "'";`,
    remedy: `// Sécurisé (Requêtes préparées / Parameterized Queries):
const query = "SELECT * FROM users WHERE email = ? AND pass = ?";
db.execute(query, [req.body.email, hashedPass]);`,
  },
  {
    id: 'xss',
    title: '2. Cross-Site Scripting (XSS)',
    tag: 'OWASP #03',
    desc: "L'injection de scripts malveillants exécutés côté client par le navigateur de victimes légitimes.",
    vulnExample: `<!-- Vulnérable dans le DOM -->
<div dangerouslySetInnerHTML={{ __html: userComment }} />`,
    remedy: `<!-- Sécurisé : encodage des entités HTML automatique -->
<div>{userComment}</div>`,
  },
  {
    id: 'csrf',
    title: '3. Cross-Site Request Forgery (CSRF)',
    tag: 'OWASP #01',
    desc: "Attaque incitant l'utilisateur authentifié à soumettre involontairement des requêtes HTTP privilégiées.",
    vulnExample: `<!-- Requête forgée sans jeton anti-CSRF -->
<img src="https://banque.com/transfert?montant=1000&dest=hacker" />`,
    remedy: `// Protection : Tokens anti-CSRF synchronisés & cookies SameSite=Strict
app.use(cookieParser());
app.use(csrfProtection);`,
  },
  {
    id: 'brute',
    title: '4. Attaques par Force Brute & Rate Limiting',
    tag: 'OWASP #07',
    desc: "Tentatives massives de devinette de mots de passe ou tokens sans restriction de fréquence.",
    vulnExample: `// Pas de limitation : 100 000 requêtes / seconde acceptées`,
    remedy: `// Mise en place de rate limiter (ex: express-rate-limit)
const limiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 5 });`,
  },
];

export const HackingView: React.FC = () => {
  const [activeSubTab, setActiveSubTab] = useState<'labs' | 'ctf'>('labs');
  const [flags, setFlags] = useState<{ [key: string]: string }>({});
  const [solved, setSolved] = useState<{ [key: string]: boolean }>({});
  const [revealedHints, setRevealedHints] = useState<{ [key: string]: boolean }>({});
  const [scoreXP, setScoreXP] = useState<number>(0);

  const handleVerifyFlag = (challenge: CTFChallenge) => {
    const inputFlag = (flags[challenge.id] || '').trim();
    if (inputFlag === challenge.flag) {
      if (!solved[challenge.id]) {
        setSolved((prev) => ({ ...prev, [challenge.id]: true }));
        setScoreXP((prev) => prev + challenge.xp);
      }
    } else {
      alert("Flag incorrect ! Consultez l'indice si nécessaire.");
    }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="view-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h2><ShieldAlert size={24} color="#f97316" /> Laboratoire de Cybersécurité & CTF</h2>
          <p>Sensibilisation éthique aux vulnérabilités logicielles et entraînement pratique aux concepts de sécurité.</p>
        </div>
        <div style={{ background: 'rgba(249, 115, 22, 0.1)', border: '1px solid rgba(249, 115, 22, 0.3)', borderRadius: '10px', padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Key size={16} color="#fb923c" />
          <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#fb923c' }}>Score CTF : {scoreXP} XP</span>
        </div>
      </div>

      <div className="filter-tabs">
        <button
          className={`filter-tab ${activeSubTab === 'labs' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('labs')}
        >
          Vulnérabilités & Bonnes Pratiques
        </button>
        <button
          className={`filter-tab ${activeSubTab === 'ctf' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('ctf')}
        >
          Missions CTF Pratiques
        </button>
      </div>

      {activeSubTab === 'labs' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.25rem' }}>
          {SECURITY_TOPICS.map((topic) => (
            <div
              key={topic.id}
              style={{
                background: 'var(--card)',
                border: '1px solid var(--border)',
                borderRadius: '12px',
                padding: '1.25rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.75rem',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 600, color: '#f8fafc' }}>{topic.title}</h3>
                <span className="badge-tag badge-orange">{topic.tag}</span>
              </div>
              <p style={{ fontSize: '0.85rem', color: 'var(--subtext)', lineHeight: '1.5' }}>{topic.desc}</p>

              <div>
                <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#ef4444', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                  <AlertTriangle size={12} /> Exemple Vulnérable :
                </div>
                <div style={{ background: '#0f131a', padding: '0.75rem', borderRadius: '6px', fontSize: '0.8rem', fontFamily: 'monospace', color: '#fca5a5', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>
                  {topic.vulnExample}
                </div>
              </div>

              <div>
                <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#22c55e', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                  <CheckCircle2 size={12} /> Remédiation Sécurisée :
                </div>
                <div style={{ background: '#0f131a', padding: '0.75rem', borderRadius: '6px', fontSize: '0.8rem', fontFamily: 'monospace', color: '#86efac', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>
                  {topic.remedy}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeSubTab === 'ctf' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.25rem' }}>
          {CTF_CHALLENGES.map((ch) => {
            const isSolved = solved[ch.id];
            return (
              <div
                key={ch.id}
                style={{
                  background: isSolved ? 'rgba(34, 197, 94, 0.05)' : 'var(--card)',
                  border: isSolved ? '1px solid rgba(34, 197, 94, 0.4)' : '1px solid var(--border)',
                  borderRadius: '12px',
                  padding: '1.25rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.75rem',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span className="badge-tag badge-blue">{ch.category}</span>
                  <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#fb923c' }}>+{ch.xp} XP</span>
                </div>
                <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc' }}>{ch.title}</h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--subtext)', lineHeight: '1.5' }}>{ch.desc}</p>

                {revealedHints[ch.id] && (
                  <div style={{ background: 'rgba(59, 130, 246, 0.1)', padding: '0.6rem 0.8rem', borderRadius: '6px', fontSize: '0.8rem', color: '#93c5fd' }}>
                    💡 <strong>Indice :</strong> {ch.hint}
                  </div>
                )}

                <div style={{ display: 'flex', gap: '0.5rem', marginTop: 'auto', paddingTop: '0.5rem' }}>
                  <input
                    style={{
                      flex: 1,
                      background: '#0f131a',
                      border: '1px solid var(--border)',
                      borderRadius: '6px',
                      padding: '0.5rem 0.75rem',
                      color: 'var(--text)',
                      fontSize: '0.85rem',
                      outline: 'none',
                    }}
                    placeholder={isSolved ? 'Validé !' : 'Entrez le flag...'}
                    disabled={isSolved}
                    value={flags[ch.id] || ''}
                    onChange={(e) => setFlags({ ...flags, [ch.id]: e.target.value })}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') handleVerifyFlag(ch);
                    }}
                  />
                  <button
                    className="btn-primary"
                    style={{ padding: '0.5rem 0.85rem', fontSize: '0.8rem', background: isSolved ? '#16a34a' : undefined }}
                    onClick={() => handleVerifyFlag(ch)}
                    disabled={isSolved}
                  >
                    {isSolved ? <CheckCircle2 size={16} /> : 'Valider'}
                  </button>
                  <button
                    className="icon-button"
                    style={{ fontSize: '0.75rem', color: 'var(--subtext)' }}
                    onClick={() => setRevealedHints({ ...revealedHints, [ch.id]: !revealedHints[ch.id] })}
                    title="Afficher/Masquer indice"
                  >
                    💡
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </motion.div>
  );
};
