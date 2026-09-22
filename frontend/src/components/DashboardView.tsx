import React from 'react';
import { motion } from 'framer-motion';
import {
  TrendingUp,
  Award,
  BookOpen,
  Bot,
  Code,
  ShieldAlert,
  Zap,
  UserCheck,
  ChevronRight,
} from 'lucide-react';

interface DashboardViewProps {
  onNavigate: (tab: 'dashboard' | 'admin' | 'chat' | 'auth' | 'courses' | 'spacecode' | 'hacking' | 'shortcuts') => void;
  coursesCount: number;
}

export const DashboardView: React.FC<DashboardViewProps> = ({ onNavigate, coursesCount }) => {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-bg-shape" />
        <div className="hero-content">
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <span className="badge-tag">UNASMOH • Promo 2028</span>
            <span className="badge-tag badge-blue">Sciences Informatiques</span>
          </div>
          <h1 className="hero-title">Bienvenue sur Asta Académie</h1>
          <p className="hero-subtitle">
            Votre plateforme universitaire centralisée : révisez vos cours de la L1 à la L4, explorez le laboratoire de cybersécurité, entraînez-vous avec SpaceCode et posez vos questions à Space AI.
          </p>
        </div>
      </section>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card" onClick={() => onNavigate('auth')} style={{ cursor: 'pointer' }}>
          <div className="stat-icon blue"><TrendingUp /></div>
          <div className="stat-info">
            <h3>Étudiants Inscrits</h3>
            <p>48</p>
          </div>
        </div>

        <div className="stat-card" onClick={() => onNavigate('courses')} style={{ cursor: 'pointer' }}>
          <div className="stat-icon green"><BookOpen /></div>
          <div className="stat-info">
            <h3>Cours Disponibles</h3>
            <p>{coursesCount}</p>
          </div>
        </div>

        <div className="stat-card" onClick={() => onNavigate('hacking')} style={{ cursor: 'pointer' }}>
          <div className="stat-icon purple"><ShieldAlert /></div>
          <div className="stat-info">
            <h3>Labs Sécurité</h3>
            <p>12</p>
          </div>
        </div>

        <div className="stat-card" onClick={() => onNavigate('shortcuts')} style={{ cursor: 'pointer' }}>
          <div className="stat-icon orange"><Award /></div>
          <div className="stat-info">
            <h3>Raccourcis & Pièges</h3>
            <p>110+</p>
          </div>
        </div>
      </div>

      {/* Modules Grid */}
      <div className="modules-section">
        <h2>Modules de la Plateforme</h2>
        <div className="modules-grid">
          <div className="module-card" onClick={() => onNavigate('courses')}>
            <div className="module-card-content">
              <div className="module-header">
                <div className="module-icon"><BookOpen size={22} color="#22c55e" /></div>
                <span className="badge-tag">L1 → L4</span>
              </div>
              <h3 className="module-title">Mes Cours Universitaires</h3>
              <p className="module-desc">
                Algèbre de Boole, Von Neumann, Algorithmique, Web HTML/CSS, MySQL, Réseaux OSI, Big Data et 23 chapitres Python.
              </p>
              <div className="module-action">
                Accéder aux cours <ChevronRight size={16} />
              </div>
            </div>
          </div>

          <div className="module-card" onClick={() => onNavigate('chat')}>
            <div className="module-card-content">
              <div className="module-header">
                <div className="module-icon"><Bot size={22} color="#38bdf8" /></div>
                <span className="badge-tag badge-blue">RAG Local</span>
              </div>
              <h3 className="module-title">Space AI Assistant</h3>
              <p className="module-desc">
                Assistant académique intelligent pour répondre à vos questions de révision, clarifier des concepts et résoudre des exercices.
              </p>
              <div className="module-action">
                Discuter avec l'IA <ChevronRight size={16} />
              </div>
            </div>
          </div>

          <div className="module-card" onClick={() => onNavigate('spacecode')}>
            <div className="module-card-content">
              <div className="module-header">
                <div className="module-icon"><Code size={22} color="#a855f7" /></div>
                <span className="badge-tag badge-purple">Éditeur & Runner</span>
              </div>
              <h3 className="module-title">SpaceCode Studio</h3>
              <p className="module-desc">
                Bac à sable de programmation pour expérimenter des snippets Python, algorithmes C++, structures de données et requêtes SQL.
              </p>
              <div className="module-action">
                Lancer l'éditeur <ChevronRight size={16} />
              </div>
            </div>
          </div>

          <div className="module-card" onClick={() => onNavigate('hacking')}>
            <div className="module-card-content">
              <div className="module-header">
                <div className="module-icon"><ShieldAlert size={22} color="#f97316" /></div>
                <span className="badge-tag badge-orange">Éthique</span>
              </div>
              <h3 className="module-title">Cyber Security Lab</h3>
              <p className="module-desc">
                Laboratoire pratique : vulnérabilités OWASP (SQLi, XSS, CSRF, Path Traversal), techniques défensives et challenges CTF.
              </p>
              <div className="module-action">
                Explorer le lab <ChevronRight size={16} />
              </div>
            </div>
          </div>

          <div className="module-card" onClick={() => onNavigate('shortcuts')}>
            <div className="module-card-content">
              <div className="module-header">
                <div className="module-icon"><Zap size={22} color="#eab308" /></div>
                <span className="badge-tag">Aide-Mémoire</span>
              </div>
              <h3 className="module-title">Raccourcis & Pièges d'Examens</h3>
              <p className="module-desc">
                Formules Excel avancées, commandes Linux indispensables, 7 couches OSI et les pièges classiques posés par les professeurs.
              </p>
              <div className="module-action">
                Consulter les fiches <ChevronRight size={16} />
              </div>
            </div>
          </div>

          <div className="module-card" onClick={() => onNavigate('admin')}>
            <div className="module-card-content">
              <div className="module-header">
                <div className="module-icon"><UserCheck size={22} color="#10b981" /></div>
                <span className="badge-tag">Gestion</span>
              </div>
              <h3 className="module-title">Administration & Profil</h3>
              <p className="module-desc">
                Supervision des utilisateurs, paramètres du profil académique UNASMOH et maintenance du cache local.
              </p>
              <div className="module-action">
                Gérer le compte <ChevronRight size={16} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
