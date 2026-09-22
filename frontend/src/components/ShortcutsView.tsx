import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Zap, Search, AlertOctagon, Layers, Terminal, FileSpreadsheet } from 'lucide-react';
import {
  EXCEL_SHORTCUTS,
  EXCEL_FORMULAS,
  PROF_TRAPS,
  LINUX_COMMANDS,
  OSI_LAYERS,
  NETWORK_PROTOCOLS,
} from '../data/shortcutsData';

type SubTab = 'excel_keys' | 'excel_formulas' | 'linux' | 'osi' | 'traps';

interface ExcelShortcut {
  key: string;
  action: string;
  niveau?: string;
}

interface ExcelFormula {
  formule: string;
  description: string;
}

interface LinuxCommand {
  commande?: string;
  action?: string;
  description?: string;
  syntaxe?: string;
  exemple?: string;
}

interface OsiLayer {
  couche?: number;
  numero?: number;
  nom: string;
  role?: string;
  description?: string;
  protocoles?: string;
  pdu?: string;
}

interface NetworkProtocol {
  nom?: string;
  protocol?: string;
  port?: string | number;
  role?: string;
  description?: string;
}

interface ProfTrap {
  titre?: string;
  question?: string;
  matiere?: string;
  piege?: string;
  erreur?: string;
  correction?: string;
  solution?: string;
}

export const ShortcutsView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<SubTab>('excel_keys');
  const [search, setSearch] = useState<string>('');

  const q = search.toLowerCase().trim();

  const filteredExcelShortcuts = useMemo(() => {
    return (EXCEL_SHORTCUTS as ExcelShortcut[]).filter((item) =>
      !q || item.key?.toLowerCase().includes(q) || item.action?.toLowerCase().includes(q) || item.niveau?.toLowerCase().includes(q)
    );
  }, [q]);

  const filteredExcelFormulas = useMemo(() => {
    return (EXCEL_FORMULAS as ExcelFormula[]).filter((item) =>
      !q || item.formule?.toLowerCase().includes(q) || item.description?.toLowerCase().includes(q)
    );
  }, [q]);

  const filteredLinux = useMemo(() => {
    return (LINUX_COMMANDS as LinuxCommand[]).filter((item) =>
      !q || item.commande?.toLowerCase().includes(q) || item.action?.toLowerCase().includes(q) || item.description?.toLowerCase().includes(q) || item.syntaxe?.toLowerCase().includes(q)
    );
  }, [q]);

  const filteredOsi = useMemo(() => {
    return (OSI_LAYERS as OsiLayer[]).filter((item) =>
      !q || item.nom?.toLowerCase().includes(q) || item.role?.toLowerCase().includes(q) || item.protocoles?.toLowerCase().includes(q)
    );
  }, [q]);

  const filteredTraps = useMemo(() => {
    return (PROF_TRAPS as ProfTrap[]).filter((item) =>
      !q ||
      item.titre?.toLowerCase().includes(q) ||
      item.piege?.toLowerCase().includes(q) ||
      item.matiere?.toLowerCase().includes(q) ||
      item.correction?.toLowerCase().includes(q)
    );
  }, [q]);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="view-header">
        <h2><Zap size={24} color="#eab308" /> Fiches Mémo & Pièges d'Examens</h2>
        <p>Répertoire express pour les examens théoriques et pratiques à l'UNASMOH.</p>
      </div>

      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center', marginBottom: '1.25rem' }}>
        <div className="filter-tabs" style={{ marginBottom: 0 }}>
          <button
            className={`filter-tab ${activeTab === 'excel_keys' ? 'active' : ''}`}
            onClick={() => setActiveTab('excel_keys')}
          >
            <FileSpreadsheet size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'text-top' }} /> Raccourcis Excel ({EXCEL_SHORTCUTS.length})
          </button>
          <button
            className={`filter-tab ${activeTab === 'excel_formulas' ? 'active' : ''}`}
            onClick={() => setActiveTab('excel_formulas')}
          >
            <FileSpreadsheet size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'text-top' }} /> Formules Excel ({EXCEL_FORMULAS.length})
          </button>
          <button
            className={`filter-tab ${activeTab === 'linux' ? 'active' : ''}`}
            onClick={() => setActiveTab('linux')}
          >
            <Terminal size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'text-top' }} /> Commandes Linux ({LINUX_COMMANDS.length})
          </button>
          <button
            className={`filter-tab ${activeTab === 'osi' ? 'active' : ''}`}
            onClick={() => setActiveTab('osi')}
          >
            <Layers size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'text-top' }} /> Modèle OSI & Réseaux ({OSI_LAYERS.length})
          </button>
          <button
            className={`filter-tab ${activeTab === 'traps' ? 'active' : ''}`}
            onClick={() => setActiveTab('traps')}
          >
            <AlertOctagon size={14} style={{ display: 'inline', marginRight: '4px', verticalAlign: 'text-top' }} /> Pièges Profs Examens ({PROF_TRAPS.length})
          </button>
        </div>

        <div className="search-bar" style={{ width: '280px', height: '38px' }}>
          <Search size={16} />
          <input
            placeholder="Rechercher une touche, formule, commande..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div style={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px', padding: '1.25rem', overflowX: 'auto' }}>
        {/* EXCEL SHORTCUTS */}
        {activeTab === 'excel_keys' && (
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: '180px' }}>Raccourci Clavier</th>
                <th>Action & Résultat</th>
                <th style={{ width: '120px' }}>Niveau</th>
              </tr>
            </thead>
            <tbody>
              {filteredExcelShortcuts.map((item, idx) => (
                <tr key={idx}>
                  <td>
                    <span style={{
                      background: '#1e293b',
                      color: '#38bdf8',
                      fontFamily: 'monospace',
                      padding: '0.2rem 0.6rem',
                      borderRadius: '4px',
                      border: '1px solid rgba(56, 189, 248, 0.3)',
                      fontWeight: 600,
                    }}>
                      {item.key}
                    </span>
                  </td>
                  <td>{item.action}</td>
                  <td>
                    <span className={`badge-tag ${item.niveau === 'Essentiel' ? '' : item.niveau === 'Avancé' ? 'badge-orange' : 'badge-blue'}`}>
                      {item.niveau || 'Standard'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* EXCEL FORMULAS */}
        {activeTab === 'excel_formulas' && (
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: '260px' }}>Formule Excel</th>
                <th>Description & Utilisation</th>
              </tr>
            </thead>
            <tbody>
              {filteredExcelFormulas.map((item, idx) => (
                <tr key={idx}>
                  <td>
                    <span style={{
                      background: '#132e1e',
                      color: '#4ade80',
                      fontFamily: 'monospace',
                      padding: '0.25rem 0.6rem',
                      borderRadius: '4px',
                      border: '1px solid rgba(74, 222, 128, 0.3)',
                      fontWeight: 600,
                    }}>
                      {item.formule}
                    </span>
                  </td>
                  <td>{item.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* LINUX COMMANDS */}
        {activeTab === 'linux' && (
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: '180px' }}>Commande</th>
                <th>Action / Description</th>
                <th style={{ width: '260px' }}>Exemple de Syntaxe</th>
              </tr>
            </thead>
            <tbody>
              {filteredLinux.map((item, idx) => (
                <tr key={idx}>
                  <td>
                    <span style={{
                      background: '#1e1b4b',
                      color: '#c084fc',
                      fontFamily: 'monospace',
                      padding: '0.25rem 0.6rem',
                      borderRadius: '4px',
                      border: '1px solid rgba(192, 132, 252, 0.3)',
                      fontWeight: 600,
                    }}>
                      {item.commande}
                    </span>
                  </td>
                  <td>{item.action || item.description}</td>
                  <td>
                    <code style={{ color: '#94a3b8', fontSize: '0.82rem' }}>
                      {item.syntaxe || item.exemple || '-'}
                    </code>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* OSI LAYERS */}
        {activeTab === 'osi' && (
          <div>
            <h3 style={{ fontSize: '1rem', color: '#fff', marginBottom: '1rem' }}>Les 7 Couches du Modèle OSI (Open Systems Interconnection)</h3>
            <table className="data-table">
              <thead>
                <tr>
                  <th style={{ width: '100px' }}>Couche</th>
                  <th style={{ width: '180px' }}>Nom</th>
                  <th>Rôle Principal</th>
                  <th style={{ width: '220px' }}>Protocoles & Unités</th>
                </tr>
              </thead>
              <tbody>
                {filteredOsi.map((item, idx) => (
                  <tr key={idx}>
                    <td>
                      <span className="badge-tag badge-purple">N° {item.couche || item.numero || idx + 1}</span>
                    </td>
                    <td style={{ fontWeight: 600, color: '#f8fafc' }}>{item.nom}</td>
                    <td>{item.role || item.description}</td>
                    <td>
                      <span style={{ fontFamily: 'monospace', color: '#38bdf8', fontSize: '0.8rem' }}>
                        {item.protocoles || item.pdu || '-'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {NETWORK_PROTOCOLS.length > 0 && (
              <div style={{ marginTop: '2rem' }}>
                <h3 style={{ fontSize: '1rem', color: '#fff', marginBottom: '1rem' }}>Protocoles Réseau Majeurs & Ports Standards</h3>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Protocole</th>
                      <th>Port par défaut</th>
                      <th>Rôle & Couche</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(NETWORK_PROTOCOLS as NetworkProtocol[]).slice(0, 10).map((p, i) => (
                      <tr key={i}>
                        <td style={{ fontWeight: 600, color: '#4ade80' }}>{p.nom || p.protocol}</td>
                        <td><span className="badge-tag">{p.port || 'N/A'}</span></td>
                        <td>{p.role || p.description}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* PROF TRAPS */}
        {activeTab === 'traps' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1rem' }}>
            {filteredTraps.map((trap, idx) => (
              <div
                key={idx}
                style={{
                  background: '#131722',
                  border: '1px solid rgba(239, 68, 68, 0.25)',
                  borderRadius: '10px',
                  padding: '1.25rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.5rem',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span className="badge-tag badge-orange">{trap.matiere || 'Informatique'}</span>
                  <span style={{ fontSize: '0.75rem', color: '#ef4444', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                    <AlertOctagon size={14} /> Piège Fréquent
                  </span>
                </div>
                <h4 style={{ fontSize: '1rem', fontWeight: 600, color: '#fca5a5' }}>
                  {trap.titre || trap.question || `Piège #${idx + 1}`}
                </h4>
                <p style={{ fontSize: '0.85rem', color: 'var(--subtext)', lineHeight: '1.5' }}>
                  {trap.piege || trap.erreur}
                </p>
                <div style={{ marginTop: 'auto', paddingTop: '0.5rem', borderTop: '1px solid rgba(255, 255, 255, 0.05)' }}>
                  <span style={{ fontSize: '0.75rem', color: '#4ade80', fontWeight: 600 }}>Bonne réponse / Astuce : </span>
                  <span style={{ fontSize: '0.82rem', color: '#e2e8f0' }}>{trap.correction || trap.solution}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
};
