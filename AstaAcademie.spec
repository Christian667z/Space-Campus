# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_qt.py'],
    pathex=[],
    binaries=[],
    datas=[('security\\security_auth.py', 'security'), ('security\\crypto_manager.py', 'security'), ('database\\db_manager.py', 'database'), ('core\\config.py', 'core'), ('core\\logic_tools.py', 'core'), ('ui\\themes\\theme_manager.py', 'ui/themes'), ('ui\\components\\widgets.py', 'ui/components'), ('core\\voice_assistant.py', 'core'), ('core\\local_llm.py', 'core'), ('utils\\shortcuts_data.py', 'utils'), ('utils\\oracle_hub.py', 'utils'), ('core\\space_code.py', 'core'), ('lessons\\cours_data.py', 'lessons'), ('utils\\updates_asta.py', 'utils'), ('assets\\offline_docs\\legal.md', 'assets/offline_docs'), ('assets\\offline_docs\\faq.md', 'assets/offline_docs'), ('assets\\hacking_payloads.zip', 'assets'), ('assets\\Space_logo.ico', 'assets'), ('assets\\Space_logo_256.png', 'assets'), ('assets\\space_ai_logo.svg', 'assets'), ('assets\\asta_academie_mark.svg', 'assets'), ('core\\space_ai_bridge.py', 'core'), ('hacking', 'hacking'), ('cours', 'cours'), ('core\\health_manager.py', 'core'), ('core\\auth_manager.py', 'core'), ('core\\memory.py', 'core'), ('core\\synonym_map.py', 'core'), ('core\\intent_parser.py', 'core'), ('core\\math_solver.py', 'core'), ('core\\knowledge_base.py', 'core'), ('core\\ai_engine.py', 'core'), ('core\\chatbot_patterns.py', 'core'), ('views\\auth_view.py', 'views'), ('utils\\cache_manager.py', 'utils'), ('utils\\status_manager.py', 'utils'), ('utils\\event_bus.py', 'utils')],
    hiddenimports=['views.dashboard_view', 'views.courses_view', 'views.notes_view', 'views.quiz_view', 'views.profile_view', 'views.settings_view', 'views.tools_view', 'views.grades_view', 'views.shortcuts_view', 'views.about_view', 'views.space_ai_view', 'views.oracle_view', 'views.guide_view', 'views.hacking_view', 'views.career_view', 'views.legal_view', 'views.auth_view', 'core.config', 'core.space_ai_bridge', 'core.local_llm', 'google.genai', 'google.genai.types', 'PySide6.QtSvg', 'speech_recognition', 'pyttsx3', 'core.voice_assistant', 'bcrypt'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide6.QtWebEngine', 'PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets', 'PySide6.QtNetwork', 'PySide6.QtQml', 'PySide6.QtQuick', 'PySide6.Qt3D', 'PySide6.QtMultimedia', 'tkinter'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AstaAcademie',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\Space_logo.ico'],
)
