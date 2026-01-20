'use client';

import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

interface LanguageSelectorProps {
  value: string;
  onChange: (language: string) => void;
  languages: string[];
}

const languageLabels: Record<string, string> = {
  python: 'Python',
  java: 'Java',
  cpp: 'C++',
};

export default function LanguageSelector({
  value,
  onChange,
  languages,
}: LanguageSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-2 rounded-lg border border-border bg-card hover:bg-muted transition-colors flex items-center justify-between text-foreground"
      >
        <span className="font-medium">{languageLabels[value]}</span>
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-card border border-border rounded-lg shadow-lg z-10">
          {languages.map((lang) => (
            <button
              key={lang}
              onClick={() => {
                onChange(lang);
                setIsOpen(false);
              }}
              className={`w-full text-left px-4 py-2 hover:bg-muted transition-colors first:rounded-t-lg last:rounded-b-lg ${
                value === lang ? 'bg-primary/10 text-primary font-medium' : 'text-foreground'
              }`}
            >
              {languageLabels[lang]}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
