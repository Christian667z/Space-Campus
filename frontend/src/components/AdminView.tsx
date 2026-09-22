import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { UserCheck, Trash2, Plus, RefreshCw, CheckCircle2, HardDrive } from 'lucide-react';

interface ManagedUser {
  id: string;
  username: string;
  matricule: string;
  role: 'Étudiant' | 'Administrateur';
  status: 'Actif' | 'En attente';
  date: string;
}

const INITIAL_USERS: ManagedUser[] = [
  { id: '1', username: 'Christian (Admin Space)', matricule: 'ASTA-20281', role: 'Administrateur', status: 'Actif', date: '2024-10-01' },
  { id: '2', username: 'Jean-Baptiste P.', matricule: 'ASTA-20282', role: 'Étudiant', status: 'Actif', date: '2024-10-05' },
  { id: '3', username: 'Marie D. Dorval', matricule: 'ASTA-20283', role: 'Étudiant', status: 'Actif', date: '2024-10-12' },
  { id: '4', username: 'Alexandre Charles', matricule: 'ASTA-20284', role: 'Étudiant', status: 'Actif', date: '2024-10-18' },
  { id: '5', username: 'Nathalie Joseph', matricule: 'ASTA-20285', role: 'Étudiant', status: 'Actif', date: '2024-11-02' },
];

export const AdminView: React.FC = () => {
  const [users, setUsers] = useState<ManagedUser[]>(INITIAL_USERS);
  const [newUsername, setNewUsername] = useState<string>('');
  const [newRole, setNewRole] = useState<'Étudiant' | 'Administrateur'>('Étudiant');
  const [cleanMessage, setCleanMessage] = useState<string>('');

  const handleAddUser = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUsername.trim()) return;

    const user: ManagedUser = {
      id: Date.now().toString(),
      username: newUsername.trim(),
      matricule: `ASTA-${Math.floor(20280 + users.length + 1)}`,
      role: newRole,
      status: 'Actif',
      date: new Date().toISOString().split('T')[0],
    };

    setUsers([user, ...users]);
    setNewUsername('');
  };

  const handleDeleteUser = (id: string) => {
    setUsers(users.filter((u) => u.id !== id));
  };

  const handleToggleRole = (id: string) => {
    setUsers(
      users.map((u) =>
        u.id === id ? { ...u, role: u.role === 'Étudiant' ? 'Administrateur' : 'Étudiant' } : u
      )
    );
  };

  const handleCleanCache = () => {
    setCleanMessage('Nettoyage du cache applicatif et des logs en cours...');
    setTimeout(() => {
      setCleanMessage('Cache vidé avec succès ! 14.8 Mo libérés.');
      setTimeout(() => setCleanMessage(''), 3500);
    }, 600);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="view-header">
        <h2><UserCheck size={24} color="#10b981" /> Administration & Supervision Système</h2>
        <p>Gestion des effectifs étudiants UNASMOH, attributions des privilèges et maintenance de la plateforme.</p>
      </div>

      {/* System Actions Bar */}
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
        <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '1rem', flex: 1, minWidth: '280px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h4 style={{ fontSize: '0.95rem', color: '#fff', marginBottom: '0.2rem' }}>Maintenance du Cache</h4>
            <p style={{ fontSize: '0.8rem', color: 'var(--subtext)' }}>Nettoyer les fichiers temporaires et sessions expirées</p>
          </div>
          <button className="btn-primary" onClick={handleCleanCache} style={{ padding: '0.45rem 0.9rem', fontSize: '0.82rem' }}>
            <RefreshCw size={14} /> Vider le cache
          </button>
        </div>

        <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '1rem', flex: 1, minWidth: '280px', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <HardDrive size={24} color="#38bdf8" />
          <div>
            <h4 style={{ fontSize: '0.95rem', color: '#fff' }}>Base de Données Asta</h4>
            <p style={{ fontSize: '0.8rem', color: '#4ade80' }}>● En ligne • Synchronisation locale instantanée</p>
          </div>
        </div>
      </div>

      {cleanMessage && (
        <div style={{ background: 'rgba(34, 197, 94, 0.1)', border: '1px solid var(--accent)', color: '#86efac', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.88rem' }}>
          <CheckCircle2 size={16} /> {cleanMessage}
        </div>
      )}

      {/* Add User Form */}
      <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '1.25rem', marginBottom: '1.5rem' }}>
        <h3 style={{ fontSize: '1rem', color: '#fff', marginBottom: '0.75rem' }}>Inscrire un nouvel utilisateur</h3>
        <form onSubmit={handleAddUser} style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <input
            style={{
              flex: 1,
              minWidth: '200px',
              background: '#0f131a',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              padding: '0.55rem 0.85rem',
              color: 'var(--text)',
              fontSize: '0.85rem',
              outline: 'none',
            }}
            placeholder="Nom complet ou Identifiant étudiant..."
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
          />

          <select
            style={{
              background: '#0f131a',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              padding: '0.55rem 0.85rem',
              color: 'var(--text)',
              fontSize: '0.85rem',
              outline: 'none',
            }}
            value={newRole}
            onChange={(e) => setNewRole(e.target.value as 'Étudiant' | 'Administrateur')}
          >
            <option value="Étudiant">Rôle: Étudiant</option>
            <option value="Administrateur">Rôle: Administrateur</option>
          </select>

          <button type="submit" className="btn-primary" style={{ padding: '0.55rem 1rem', fontSize: '0.85rem' }}>
            <Plus size={16} /> Ajouter l'étudiant
          </button>
        </form>
      </div>

      {/* Users Table */}
      <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '1.25rem', overflowX: 'auto' }}>
        <h3 style={{ fontSize: '1rem', color: '#fff', marginBottom: '0.5rem' }}>Registre des Comptes ({users.length})</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>Étudiant / Utilisateur</th>
              <th>Matricule</th>
              <th>Rôle</th>
              <th>Statut</th>
              <th>Date d'Inscription</th>
              <th style={{ textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td style={{ fontWeight: 600, color: '#f8fafc' }}>{u.username}</td>
                <td><code style={{ color: '#38bdf8' }}>{u.matricule}</code></td>
                <td>
                  <button
                    onClick={() => handleToggleRole(u.id)}
                    className={`badge-tag ${u.role === 'Administrateur' ? 'badge-purple' : ''}`}
                    style={{ cursor: 'pointer', border: 'none' }}
                    title="Cliquer pour changer de rôle"
                  >
                    {u.role}
                  </button>
                </td>
                <td>
                  <span style={{ color: '#4ade80', fontSize: '0.8rem', fontWeight: 600 }}>● {u.status}</span>
                </td>
                <td style={{ color: 'var(--subtext)', fontSize: '0.82rem' }}>{u.date}</td>
                <td style={{ textAlign: 'right' }}>
                  <button
                    onClick={() => handleDeleteUser(u.id)}
                    className="icon-button"
                    style={{ color: '#ef4444' }}
                    title="Supprimer le compte"
                  >
                    <Trash2 size={16} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
};
