import React, { useState } from 'react';
import {
  Home,
  BookOpen,
  Bot,
  Code,
  ShieldAlert,
  Zap,
  UserCheck,
  Settings,
  Search,
  Bell,
  Cpu,
} from 'lucide-react';

import { ALL_COURSES } from './data/coursesData';
import { DashboardView } from './components/DashboardView';
import { CoursesView } from './components/CoursesView';
import { SpaceAiView } from './components/SpaceAiView';
import { SpaceCodeView } from './components/SpaceCodeView';
import { HackingView } from './components/HackingView';
import { ShortcutsView } from './components/ShortcutsView';
import { AuthView } from './components/AuthView';
import { AdminView } from './components/AdminView';
import { DesktopTitlebar } from './components/DesktopTitlebar';
import { NativeArchitectureView } from './components/NativeArchitectureView';

export type TabId = 'dashboard' | 'admin' | 'native' | 'chat' | 'auth' | 'courses' | 'spacecode' | 'hacking' | 'shortcuts';

interface UserProfile {
  username: string;
  matricule: string;
  role: 'Étudiant' | 'Administrateur';
  promotion: string;
  avatar: string;
}

const DEFAULT_USER: UserProfile = {
  username: 'Christian Alvaro',
  matricule: 'ASTA-20281',
  role: 'Administrateur',
  promotion: '2024-2028 UNASMOH',
  avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=Christian',
};

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabId>('dashboard');
  const [currentUser, setCurrentUser] = useState<UserProfile>(DEFAULT_USER);
  const [globalSearch, setGlobalSearch] = useState<string>('');

  const handleGlobalSearch = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && globalSearch.trim()) {
      setActiveTab('courses');
    }
  };

  const navItems: { id: TabId; label: string; icon: React.ReactNode }[] = [
    { id: 'dashboard', label: 'Tableau de Bord', icon: <Home size={19} /> },
    { id: 'courses', label: 'Mes Cours', icon: <BookOpen size={19} /> },
    { id: 'chat', label: 'Space AI', icon: <Bot size={19} /> },
    { id: 'spacecode', label: 'SpaceCode', icon: <Code size={19} /> },
    { id: 'hacking', label: 'Cyber Security', icon: <ShieldAlert size={19} /> },
    { id: 'shortcuts', label: 'Raccourcis & Pièges', icon: <Zap size={19} /> },
    { id: 'native', label: 'Architecture & Rust', icon: <Cpu size={19} /> },
    { id: 'admin', label: 'Administration', icon: <Settings size={19} /> },
    { id: 'auth', label: 'Profil Étudiant', icon: <UserCheck size={19} /> },
  ];

  return (
    <div className="desktop-app-shell">
      <DesktopTitlebar />
      <div className="app-container">
        {/* Sidebar */}
        <nav className="sidebar">
        <div className="logo-container" onClick={() => setActiveTab('dashboard')} style={{ cursor: 'pointer' }}>
          <div className="logo-icon" style={{ overflow: 'hidden', padding: '4px' }}>
            <img
              src="/Space_logo_256.png"
              alt="Asta Logo"
              style={{ width: '100%', height: '100%', objectFit: 'contain' }}
              onError={(e) => {
                // Fallback if image not rendered
                (e.target as HTMLElement).style.display = 'none';
              }}
            />
          </div>
          <div className="logo-text">
            <h1>Asta Académie</h1>
            <span>UNASMOH • Promo 2028</span>
          </div>
        </div>

        <div className="nav-menu">
          {navItems.map((item) => (
            <div
              key={item.id}
              className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              {item.icon}
              <span>{item.label}</span>
            </div>
          ))}
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="main-content">
        <header className="topbar">
          <div className="search-bar">
            <Search size={18} />
            <input
              placeholder="Recherche rapide (Entrée pour chercher dans les cours)..."
              value={globalSearch}
              onChange={(e) => setGlobalSearch(e.target.value)}
              onKeyDown={handleGlobalSearch}
            />
          </div>

          <div className="topbar-actions">
            <button
              className="icon-button"
              onClick={() => setActiveTab('shortcuts')}
              title="Aide-Mémoire"
            >
              <Zap size={18} />
            </button>
            <button
              className="icon-button"
              onClick={() => setActiveTab('admin')}
              title="Supervision"
            >
              <Bell size={18} />
            </button>
            <div
              onClick={() => setActiveTab('auth')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.6rem',
                cursor: 'pointer',
                background: 'rgba(255, 255, 255, 0.04)',
                padding: '0.35rem 0.75rem',
                borderRadius: '8px',
                border: '1px solid var(--border)',
              }}
            >
              <img
                src={currentUser.avatar}
                alt="Profile"
                className="profile-pic"
                style={{ width: '28px', height: '28px', borderRadius: '50%' }}
              />
              <div style={{ textAlign: 'left', lineHeight: '1.2' }}>
                <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#f8fafc' }}>
                  {currentUser.username}
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--accent)' }}>
                  {currentUser.role}
                </div>
              </div>
            </div>
          </div>
        </header>

        <div className="content-area">
          {activeTab === 'dashboard' && (
            <DashboardView onNavigate={setActiveTab} coursesCount={ALL_COURSES.length} />
          )}
          {activeTab === 'courses' && <CoursesView />}
          {activeTab === 'chat' && <SpaceAiView />}
          {activeTab === 'spacecode' && <SpaceCodeView />}
          {activeTab === 'hacking' && <HackingView />}
          {activeTab === 'shortcuts' && <ShortcutsView />}
          {activeTab === 'native' && <NativeArchitectureView />}
          {activeTab === 'admin' && <AdminView />}
          {activeTab === 'auth' && (
            <AuthView
              currentUser={currentUser}
              onLogin={setCurrentUser}
              onLogout={() =>
                setCurrentUser({
                  username: 'Visiteur',
                  matricule: 'NON-INSCRIT',
                  role: 'Étudiant',
                  promotion: '2024-2028 UNASMOH',
                  avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=Guest',
                })
              }
            />
          )}
        </div>
      </main>
      </div>
    </div>
  );
};

export default App;
