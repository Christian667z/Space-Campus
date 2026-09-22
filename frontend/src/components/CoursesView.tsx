import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Search, Copy, Check } from 'lucide-react';
import { ALL_COURSES, type CourseItem } from '../data/coursesData';

export const CoursesView: React.FC = () => {
  const [selectedLevel, setSelectedLevel] = useState<string>('Tous');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeCourse, setActiveCourse] = useState<CourseItem>(ALL_COURSES[0]);
  const [copied, setCopied] = useState<boolean>(false);

  const levels = ['Tous', 'L1', 'L2', 'L3', 'L4', 'PYTHON'];

  const filteredCourses = useMemo(() => {
    return ALL_COURSES.filter((course) => {
      const matchLevel = selectedLevel === 'Tous' || course.level === selectedLevel;
      const q = searchQuery.toLowerCase().trim();
      const matchSearch =
        !q ||
        course.title.toLowerCase().includes(q) ||
        course.subject.toLowerCase().includes(q) ||
        course.content.toLowerCase().includes(q);
      return matchLevel && matchSearch;
    });
  }, [selectedLevel, searchQuery]);

  const handleCopy = () => {
    if (activeCourse) {
      navigator.clipboard.writeText(activeCourse.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <div className="view-header">
        <h2><BookOpen size={24} color="#22c55e" /> Catalogue des Cours Universitaires</h2>
        <p>Programme officiel UNASMOH L1 à L4 et cursus complet de spécialisation Python.</p>
      </div>

      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center', marginBottom: '1rem' }}>
        <div className="filter-tabs" style={{ marginBottom: 0 }}>
          {levels.map((lvl) => (
            <button
              key={lvl}
              className={`filter-tab ${selectedLevel === lvl ? 'active' : ''}`}
              onClick={() => setSelectedLevel(lvl)}
            >
              {lvl === 'PYTHON' ? '🐍 Python' : lvl}
            </button>
          ))}
        </div>

        <div className="search-bar" style={{ width: '280px', height: '38px' }}>
          <Search size={16} />
          <input
            placeholder="Filtrer dans les cours..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="split-container">
        {/* Left list */}
        <div className="panel-list">
          <div style={{ fontSize: '0.8rem', color: 'var(--subtext)', padding: '0.25rem 0.5rem', fontWeight: 600 }}>
            {filteredCourses.length} COURS DISPONIBLE{filteredCourses.length > 1 ? 'S' : ''}
          </div>
          {filteredCourses.map((course) => {
            const isSelected = activeCourse?.id === course.id;
            return (
              <div
                key={course.id}
                className={`panel-item ${isSelected ? 'active' : ''}`}
                onClick={() => setActiveCourse(course)}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                  <span className={`badge-tag ${course.level === 'PYTHON' ? 'badge-blue' : course.level === 'L4' ? 'badge-purple' : ''}`}>
                    {course.level}
                  </span>
                  <span style={{ fontSize: '0.72rem', color: 'var(--subtext)' }}>{course.subject}</span>
                </div>
                <div className="panel-item-title">{course.title}</div>
              </div>
            );
          })}
          {filteredCourses.length === 0 && (
            <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--subtext)', fontSize: '0.9rem' }}>
              Aucun cours ne correspond à votre recherche.
            </div>
          )}
        </div>

        {/* Right reader */}
        <div className="panel-reader">
          {activeCourse ? (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '1px solid var(--border)', paddingBottom: '1rem', marginBottom: '1.5rem' }}>
                <div>
                  <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <span className="badge-tag">{activeCourse.level}</span>
                    <span className="badge-tag badge-blue">{activeCourse.subject}</span>
                  </div>
                  <h1 style={{ fontSize: '1.6rem', fontWeight: 700, color: '#fff' }}>{activeCourse.title}</h1>
                </div>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button
                    onClick={handleCopy}
                    className="icon-button"
                    style={{
                      padding: '0.5rem 0.8rem',
                      background: 'rgba(255, 255, 255, 0.05)',
                      borderRadius: '8px',
                      display: 'flex',
                      gap: '0.4rem',
                      fontSize: '0.85rem',
                      color: copied ? '#4ade80' : 'var(--text)'
                    }}
                    title="Copier le contenu"
                  >
                    {copied ? <Check size={16} /> : <Copy size={16} />}
                    <span>{copied ? 'Copié !' : 'Copier'}</span>
                  </button>
                </div>
              </div>

              {/* Render content */}
              <div className="markdown-body">
                <pre style={{
                  lineHeight: '1.65',
                  fontFamily: 'inherit',
                  whiteSpace: 'pre-wrap',
                  background: 'transparent',
                  border: 'none',
                  padding: 0,
                  color: 'var(--text)',
                  fontSize: '0.92rem'
                }}>
                  {activeCourse.content}
                </pre>
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--subtext)' }}>
              Sélectionnez un cours pour commencer la lecture.
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};
