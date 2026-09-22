import React, { useState, useEffect } from 'react';
import { Minus, Square, X, Cpu, ShieldCheck, Database, Terminal } from 'lucide-react';
import { tauriBridge, type SystemMetrics } from '../services/tauriBridge';

export const DesktopTitlebar: React.FC = () => {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);

  useEffect(() => {
    tauriBridge.getSystemMetrics().then(setMetrics).catch(() => {});
  }, []);

  return (
    <header
      id="desktop-titlebar"
      style={{
        height: '34px',
        background: '#070a11',
        borderBottom: '1px solid rgba(255, 255, 255, 0.07)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 0.5rem',
        userSelect: 'none',
        fontSize: '0.75rem',
        color: '#94a3b8',
        zIndex: 50,
      }}
    >
      {/* App brand & identity */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
          <img
            src="/Space_logo_256.png"
            alt="Logo"
            style={{ width: '16px', height: '16px', objectFit: 'contain' }}
            onError={(e) => { (e.target as HTMLElement).style.display = 'none'; }}
          />
          <span style={{ fontWeight: 600, color: '#f8fafc', letterSpacing: '0.3px' }}>
            Asta Académie Desktop
          </span>
          <span style={{
            fontSize: '0.65rem',
            background: 'rgba(56, 189, 248, 0.15)',
            color: '#38bdf8',
            padding: '1px 5px',
            borderRadius: '4px',
            fontWeight: 500,
            border: '1px solid rgba(56, 189, 248, 0.3)'
          }}>
            Rust Core v2.0
          </span>
        </div>

        {/* Status badges */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginLeft: '0.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: '#22c55e' }}>
            <Cpu size={12} />
            <span style={{ fontSize: '0.68rem' }}>Rust/Tauri IPC</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: '#38bdf8' }}>
            <Database size={12} />
            <span style={{ fontSize: '0.68rem' }}>SQLite Chiffré</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: '#a855f7' }}>
            <ShieldCheck size={12} />
            <span style={{ fontSize: '0.68rem' }}>C/C++ FFI Armé</span>
          </div>
        </div>
      </div>

      {/* Center info */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', opacity: 0.8, fontSize: '0.7rem' }}>
        <Terminal size={12} color="#f59e0b" />
        <span>{metrics?.hardwareId || 'HWID: ASTA-2028-PROMO'}</span>
      </div>

      {/* Desktop Window Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
        <button
          id="btn-win-minimize"
          onClick={() => tauriBridge.minimizeWindow()}
          title="Réduire"
          style={{
            background: 'transparent',
            border: 'none',
            color: '#94a3b8',
            width: '28px',
            height: '24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            borderRadius: '3px',
            transition: 'background 0.15s',
          }}
          onMouseEnter={(e) => { e.currentTarget.style.background = 'rgba(255,255,255,0.08)'; }}
          onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
        >
          <Minus size={13} />
        </button>

        <button
          id="btn-win-maximize"
          onClick={() => tauriBridge.toggleMaximizeWindow()}
          title="Agrandir / Restaurer"
          style={{
            background: 'transparent',
            border: 'none',
            color: '#94a3b8',
            width: '28px',
            height: '24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            borderRadius: '3px',
            transition: 'background 0.15s',
          }}
          onMouseEnter={(e) => { e.currentTarget.style.background = 'rgba(255,255,255,0.08)'; }}
          onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
        >
          <Square size={11} />
        </button>

        <button
          id="btn-win-close"
          onClick={() => tauriBridge.closeWindow()}
          title="Fermer"
          style={{
            background: 'transparent',
            border: 'none',
            color: '#94a3b8',
            width: '28px',
            height: '24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            borderRadius: '3px',
            transition: 'background 0.15s',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#ef4444';
            e.currentTarget.style.color = '#fff';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'transparent';
            e.currentTarget.style.color = '#94a3b8';
          }}
        >
          <X size={13} />
        </button>
      </div>
    </header>
  );
};
