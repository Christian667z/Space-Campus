import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Bot, Send, User, Sparkles, RotateCcw } from 'lucide-react';
import { CHAT_PATTERNS } from '../data/spaceAiPatterns';
import { ALL_COURSES } from '../data/coursesData';

interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  time: string;
}

const findAnswer = (query: string): string => {
  const qClean = query.trim().toLowerCase();

  // 1. Try patterns by priority
  const sortedPatterns = [...CHAT_PATTERNS].sort((a, b) => (b.priority || 1) - (a.priority || 1));
  for (const pattern of sortedPatterns) {
    try {
      const rx = new RegExp(pattern.regex, 'i');
      if (rx.test(qClean)) {
        const randomIndex = Math.floor(Math.random() * pattern.responses.length);
        return pattern.responses[randomIndex];
      }
    } catch {
      continue;
    }
  }

  // 2. RAG search over courses
  const words = qClean.split(/\s+/).filter((w) => w.length > 3);
  if (words.length > 0) {
    let bestCourse = null;
    let highestScore = 0;

    for (const course of ALL_COURSES) {
      let score = 0;
      const text = (course.title + ' ' + course.subject + ' ' + course.content).toLowerCase();
      for (const w of words) {
        if (text.includes(w)) {
          score++;
        }
      }
      if (score > highestScore) {
        highestScore = score;
        bestCourse = course;
      }
    }

    if (bestCourse && highestScore > 0) {
      const snippet = bestCourse.content.slice(0, 1200);
      return `📖 D'après le cours **${bestCourse.title}** (${bestCourse.level} - ${bestCourse.subject}) :\n\n${snippet}...\n\n💡 *Vous pouvez consulter la version intégrale dans l'onglet "Mes Cours".*`;
    }
  }

  // 3. Fallback
  return "Je n'ai pas trouvé de réponse directe dans les archives locales de cours pour cette requête exacte. Essayez de formuler avec des mots-clés comme 'Von Neumann', 'Boole', 'OSI', 'Python', 'SQL', 'Pomodoro' ou consultez directement le catalogue dans l'onglet 'Mes Cours'.";
};

export const SpaceAiView: React.FC = () => {
  const msgCounterRef = useRef<number>(1);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'bot',
      text: "◈ SPACE AI PROTOCOLE ACTIF ◈\n\nBonjour ! Je suis Space AI, l'assistant académique d'Asta Académie. Je peux vous expliquer les cours de l'UNASMOH (L1→L4), résoudre des doutes algorithmiques, réviser l'architecture Von Neumann, le modèle OSI ou vous donner des conseils de productivité. Que souhaitez-vous réviser aujourd'hui ?",
      time: '12:00',
    },
  ]);
  const [input, setInput] = useState<string>('');
  const [isTyping, setIsTyping] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const sampleChips = [
    "Architecture de Von Neumann",
    "Fondements de l'Algèbre de Boole",
    "Différence TCP et UDP",
    "Méthode Pomodoro & Révision",
    "Pièges d'examens fréquents",
    "Les 5 V du Big Data",
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim()) return;

    msgCounterRef.current += 1;
    const currentId = `msg_${msgCounterRef.current}`;

    const userMsg: Message = {
      id: currentId,
      sender: 'user',
      text: query.trim(),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput('');
    setIsTyping(true);

    setTimeout(() => {
      msgCounterRef.current += 1;
      const botId = `msg_${msgCounterRef.current}`;
      const reply = findAnswer(query);
      const botMsg: Message = {
        id: botId,
        sender: 'bot',
        text: reply,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, botMsg]);
      setIsTyping(false);
    }, 450);
  };

  const handleReset = () => {
    setMessages([
      {
        id: 'welcome',
        sender: 'bot',
        text: "◈ SESSION RÉINITIALISÉE ◈\n\nPrêt pour une nouvelle session de révision ! Posez votre question.",
        time: '12:00',
      },
    ]);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="view-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h2><Bot size={24} color="#38bdf8" /> Space AI — Tuteur Informatique</h2>
          <p>Intelligence artificielle académique pour UNASMOH Promo 2028 (Moteur RAG local déterministe).</p>
        </div>
        <button
          onClick={handleReset}
          className="filter-tab"
          style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
          title="Effacer l'historique"
        >
          <RotateCcw size={14} /> Réinitialiser
        </button>
      </div>

      <div className="chat-container">
        <div className="chat-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              background: '#22c55e',
              boxShadow: '0 0 8px #22c55e'
            }} />
            <span style={{ fontSize: '0.85rem', fontWeight: 600, letterSpacing: '0.5px' }}>SPACE AI ONLINE • v4.0</span>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--subtext)' }}>48 Modèles Académiques Actifs</span>
        </div>

        <div className="chat-messages">
          {messages.map((m) => (
            <div
              key={m.id}
              className={`chat-bubble ${m.sender}`}
              style={{ display: 'flex', flexDirection: 'column', gap: '0.3rem' }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', opacity: 0.7, fontSize: '0.75rem' }}>
                {m.sender === 'user' ? <User size={12} /> : <Sparkles size={12} color="#00e5ff" />}
                <span>{m.sender === 'user' ? 'Vous' : 'Space AI'}</span>
                <span>• {m.time}</span>
              </div>
              <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{m.text}</div>
            </div>
          ))}

          {isTyping && (
            <div className="chat-bubble bot" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--subtext)' }}>
              <Sparkles size={14} color="#00e5ff" />
              <span>Space AI analyse la base de connaissances...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Chips */}
        <div className="chat-chips">
          {sampleChips.map((chip, idx) => (
            <button key={idx} className="chat-chip" onClick={() => handleSend(chip)}>
              {chip}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="chat-input-bar">
          <input
            placeholder="Posez une question sur un cours, un concept ou un algorithme..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSend();
            }}
          />
          <button className="btn-primary" onClick={() => handleSend()}>
            <Send size={16} />
            <span>Envoyer</span>
          </button>
        </div>
      </div>
    </motion.div>
  );
};
