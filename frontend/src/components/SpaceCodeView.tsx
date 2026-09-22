import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Code, Play, Copy, Check, Terminal } from 'lucide-react';

interface CodeSnippet {
  title: string;
  lang: 'python' | 'javascript' | 'cpp' | 'sql';
  code: string;
  expectedOutput: string;
}

const SNIPPETS: CodeSnippet[] = [
  {
    title: 'Python: Liste Chaînée & Inversion',
    lang: 'python',
    code: `# Structure de liste chaînée fondamentale (Cours L2)
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

def reverse_list(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

# Démonstration
head = Node("L1: Algo", Node("L2: Web", Node("L3: Réseaux", Node("L4: BigData"))))
reversed_head = reverse_list(head)

curr = reversed_head
while curr:
    print(f"-> {curr.value}")
    curr = curr.next
`,
    expectedOutput: `[Processus Python 3.12 démarré]
-> L4: BigData
-> L3: Réseaux
-> L2: Web
-> L1: Algo
[Processus terminé avec succès - Code retour: 0]`,
  },
  {
    title: 'C++: Algorithme de Recherche Dichotomique',
    lang: 'cpp',
    code: `#include <iostream>
#include <vector>

int binarySearch(const std::vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

int main() {
    std::vector<int> notes = {8, 11, 14, 16, 18, 20};
    int target = 16;
    int idx = binarySearch(notes, target);
    std::cout << "Element " << target << " trouve a l'index: " << idx << std::endl;
    return 0;
}
`,
    expectedOutput: `[Compilation G++ 14.1 via LLVM]
[Exécution binaire native]
Element 16 trouve a l'index: 3
[Processus terminé avec code retour: 0]`,
  },
  {
    title: 'SQL: Modélisation & Jointure UNASMOH',
    lang: 'sql',
    code: `-- Schéma Relationnel Asta Académie (Cours L3 MySQL)
SELECT 
    etudiants.matricule,
    etudiants.nom,
    cours.intitule,
    examens.note
FROM etudiants
JOIN examens ON etudiants.id = examens.etudiant_id
JOIN cours ON examens.cours_id = cours.id
WHERE examens.note >= 12
ORDER BY examens.note DESC;
`,
    expectedOutput: `+------------+--------------------+-------------------------+------+
| matricule  | nom                | intitule                | note |
+------------+--------------------+-------------------------+------+
| ASTA-20281 | Christian Alvaro   | Architecture Ordinateur | 18.5 |
| ASTA-20284 | Marie Dorval       | Algèbre de Boole        | 17.0 |
| ASTA-20287 | Jean-Baptiste P.   | Structure de Données    | 15.0 |
+------------+--------------------+-------------------------+------+
3 lignes renvoyées en 4.2ms.`,
  },
  {
    title: 'JavaScript: Calculateur de Moyenne Promotion',
    lang: 'javascript',
    code: `// Calcul de la moyenne générale d'un semestre
const matieres = [
  { nom: "Algo & Boole", coef: 4, note: 16 },
  { nom: "Architecture", coef: 3, note: 15 },
  { nom: "Web Dev HTML/CSS", coef: 3, note: 17 },
  { nom: "Systemes Exploitation", coef: 3, note: 14 }
];

const totalPoints = matieres.reduce((acc, m) => acc + m.note * m.coef, 0);
const totalCoef = matieres.reduce((acc, m) => acc + m.coef, 0);
const moyenne = (totalPoints / totalCoef).toFixed(2);

console.log("Total Coefficients:", totalCoef);
console.log("Moyenne Générale UNASMOH:", moyenne + " / 20");
console.log(moyenne >= 16 ? "Mention: Très Bien 🌟" : "Mention: Bien ✅");
`,
    expectedOutput: `[V8 Node Runtime Active]
Total Coefficients: 13
Moyenne Générale UNASMOH: 15.54 / 20
Mention: Bien ✅
[Execution completed successfully]`,
  },
];

export const SpaceCodeView: React.FC = () => {
  const [selectedSnippetIdx, setSelectedSnippetIdx] = useState<number>(0);
  const [currentCode, setCurrentCode] = useState<string>(SNIPPETS[0].code);
  const [consoleOutput, setConsoleOutput] = useState<string>(SNIPPETS[0].expectedOutput);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  const handleSelectSnippet = (idx: number) => {
    setSelectedSnippetIdx(idx);
    setCurrentCode(SNIPPETS[idx].code);
    setConsoleOutput(SNIPPETS[idx].expectedOutput);
  };

  const handleRun = () => {
    setIsRunning(true);
    setConsoleOutput("Exécution du code en cours...\n");

    setTimeout(() => {
      // Check if javascript, can run console logs
      if (SNIPPETS[selectedSnippetIdx].lang === 'javascript') {
        try {
          const logs: string[] = [];
          const customConsole = {
            log: (...args: unknown[]) => logs.push(args.map(String).join(' ')),
            error: (...args: unknown[]) => logs.push('[ERROR] ' + args.map(String).join(' ')),
            warn: (...args: unknown[]) => logs.push('[WARN] ' + args.map(String).join(' ')),
          };
          const runner = new Function('console', currentCode);
          runner(customConsole);
          setConsoleOutput(logs.join('\n') || '[Code exécuté sans sortie console]');
        } catch (err: unknown) {
          const errMsg = err instanceof Error ? err.message : String(err);
          setConsoleOutput(`[Erreur d'exécution]: ${errMsg}`);
        }
      } else {
        setConsoleOutput(SNIPPETS[selectedSnippetIdx].expectedOutput);
      }
      setIsRunning(false);
    }, 400);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(currentCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="view-header">
        <h2><Code size={24} color="#a855f7" /> SpaceCode Studio PRO</h2>
        <p>Environnement interactif de programmation et d'expérimentation d'algorithmes informatiques.</p>
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
        {SNIPPETS.map((snip, idx) => (
          <button
            key={idx}
            className={`filter-tab ${selectedSnippetIdx === idx ? 'active' : ''}`}
            onClick={() => handleSelectSnippet(idx)}
          >
            {snip.title}
          </button>
        ))}
      </div>

      <div className="code-container">
        {/* Editor Box */}
        <div className="editor-box">
          <div className="editor-top">
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--subtext)' }}>
              ÉDITEUR • {SNIPPETS[selectedSnippetIdx].lang.toUpperCase()}
            </span>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                onClick={handleCopy}
                className="icon-button"
                style={{ fontSize: '0.8rem', color: copied ? '#4ade80' : 'var(--subtext)', display: 'flex', gap: '0.3rem', alignItems: 'center' }}
                title="Copier le code"
              >
                {copied ? <Check size={14} /> : <Copy size={14} />}
                <span>{copied ? 'Copié' : 'Copier'}</span>
              </button>
              <button className="btn-primary" style={{ padding: '0.35rem 0.85rem', fontSize: '0.8rem' }} onClick={handleRun} disabled={isRunning}>
                <Play size={14} />
                <span>{isRunning ? 'Calcul...' : 'Exécuter'}</span>
              </button>
            </div>
          </div>
          <textarea
            className="editor-textarea"
            value={currentCode}
            onChange={(e) => setCurrentCode(e.target.value)}
            spellCheck={false}
          />
        </div>

        {/* Terminal Box */}
        <div className="terminal-box">
          <div className="editor-top" style={{ background: '#0c0f16' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Terminal size={14} color="#4ade80" />
              <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#4ade80' }}>
                CONSOLE TERMINAL (STDOUT)
              </span>
            </div>
            <button
              onClick={() => setConsoleOutput('')}
              className="icon-button"
              style={{ fontSize: '0.75rem', color: 'var(--subtext)' }}
            >
              Effacer
            </button>
          </div>
          <div className="terminal-content">
            {consoleOutput || '[En attente d\'exécution...]'}
          </div>
        </div>
      </div>
    </motion.div>
  );
};
