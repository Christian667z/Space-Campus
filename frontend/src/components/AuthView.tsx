import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { UserCheck, LogIn, UserPlus, LogOut } from 'lucide-react';
import '../auth.css';

interface UserProfile {
  username: string;
  matricule: string;
  role: 'Étudiant' | 'Administrateur';
  promotion: string;
  avatar: string;
}

interface AuthViewProps {
  currentUser: UserProfile;
  onLogin: (user: UserProfile) => void;
  onLogout: () => void;
}

export const AuthView: React.FC<AuthViewProps> = ({ currentUser, onLogin, onLogout }) => {
  const [isRegister, setIsRegister] = useState<boolean>(false);
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [matricule, setMatricule] = useState<string>('');
  const [msg, setMsg] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim()) {
      setMsg('Veuillez entrer un nom d\'utilisateur valide.');
      return;
    }

    const newUser: UserProfile = {
      username: username.trim(),
      matricule: matricule.trim() || `ASTA-${Math.floor(1000 + Math.random() * 9000)}`,
      role: username.toLowerCase().includes('admin') ? 'Administrateur' : 'Étudiant',
      promotion: '2024-2028 UNASMOH',
      avatar: `https://api.dicebear.com/7.x/bottts/svg?seed=${encodeURIComponent(username.trim())}`,
    };

    onLogin(newUser);
    setMsg(`Connexion réussie en tant que ${newUser.username} !`);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="view-header">
        <h2><UserCheck size={24} color="#22c55e" /> Authentification & Profil Étudiant</h2>
        <p>Espace de session pour enregistrer votre progression et accéder aux services Asta Académie.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem', maxWidth: '900px' }}>
        {/* Form Panel */}
        <div className="auth-panel" style={{ border: '1px solid var(--border)', borderRadius: '14px' }}>
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
            <button
              className={`filter-tab ${!isRegister ? 'active' : ''}`}
              onClick={() => { setIsRegister(false); setMsg(''); }}
              type="button"
            >
              <LogIn size={14} style={{ display: 'inline', marginRight: '4px' }} /> Connexion
            </button>
            <button
              className={`filter-tab ${isRegister ? 'active' : ''}`}
              onClick={() => { setIsRegister(true); setMsg(''); }}
              type="button"
            >
              <UserPlus size={14} style={{ display: 'inline', marginRight: '4px' }} /> Inscription
            </button>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <label style={{ fontSize: '0.85rem', color: 'var(--subtext)' }}>Nom d'utilisateur ou Matricule</label>
            <input
              type="text"
              placeholder="ex: Christian ou ASTA-2028"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />

            {isRegister && (
              <>
                <label style={{ fontSize: '0.85rem', color: 'var(--subtext)' }}>Matricule UNASMOH (Optionnel)</label>
                <input
                  type="text"
                  placeholder="ex: 24-INFO-0042"
                  value={matricule}
                  onChange={(e) => setMatricule(e.target.value)}
                />
              </>
            )}

            <label style={{ fontSize: '0.85rem', color: 'var(--subtext)' }}>Mot de passe</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <button type="submit" style={{ cursor: 'pointer', marginTop: '0.5rem' }}>
              {isRegister ? "Créer mon compte étudiant" : "Se connecter"}
            </button>

            {msg && (
              <div style={{ color: '#4ade80', fontSize: '0.85rem', marginTop: '0.5rem', textAlign: 'center' }}>
                {msg}
              </div>
            )}
          </form>
        </div>

        {/* Current Profile Card */}
        <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '14px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <img
              src={currentUser.avatar}
              alt="Avatar"
              style={{ width: '64px', height: '64px', borderRadius: '50%', background: '#1e293b', border: '2px solid var(--accent)' }}
            />
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <h3 style={{ fontSize: '1.2rem', color: '#fff' }}>{currentUser.username}</h3>
                <span className="badge-tag">{currentUser.role}</span>
              </div>
              <p style={{ fontSize: '0.85rem', color: 'var(--subtext)' }}>Matricule : {currentUser.matricule}</p>
            </div>
          </div>

          <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--subtext)' }}>Établissement :</span>
              <span style={{ fontWeight: 600 }}>UNASMOH Port-au-Prince</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--subtext)' }}>Faculté :</span>
              <span style={{ fontWeight: 600 }}>Génie & Sciences Informatiques</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--subtext)' }}>Promotion :</span>
              <span style={{ fontWeight: 600 }}>{currentUser.promotion}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--subtext)' }}>Statut :</span>
              <span style={{ color: '#4ade80', fontWeight: 600 }}>Actif & Vérifié</span>
            </div>
          </div>

          <button
            onClick={onLogout}
            className="filter-tab"
            style={{ marginTop: 'auto', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', color: '#ef4444', borderColor: 'rgba(239, 68, 68, 0.3)' }}
          >
            <LogOut size={16} /> Déconnexion de la session
          </button>
        </div>
      </div>
    </motion.div>
  );
};
