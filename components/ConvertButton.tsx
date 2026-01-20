'use client';

import { useState, useEffect } from 'react';
import { Zap, Loader2, Check } from 'lucide-react';

interface ConvertButtonProps {
  onClick: () => void;
  isLoading: boolean;
  sourceLanguage: string;
  targetLanguage: string;
}

const languageLabels: Record<string, string> = {
  python: 'Python',
  java: 'Java',
  cpp: 'C++',
  javascript: 'JavaScript',
  typescript: 'TypeScript',
  go: 'Go',
  rust: 'Rust',
  csharp: 'C#',
};

export default function ConvertButton({
  onClick,
  isLoading,
  sourceLanguage,
  targetLanguage,
}: ConvertButtonProps) {
  const [isConverted, setIsConverted] = useState(false);

  useEffect(() => {
    if (!isLoading && isConverted) {
      const timer = setTimeout(() => setIsConverted(false), 2000);
      return () => clearTimeout(timer);
    }
  }, [isLoading, isConverted]);

  const handleClick = async () => {
    onClick();
    if (!isLoading) {
      // Will be updated when conversion completes
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={isLoading}
      className="relative group px-8 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-primary to-accent hover:shadow-lg hover:shadow-primary/50 disabled:opacity-70 disabled:cursor-not-allowed transition-all duration-300 overflow-hidden"
    >
      <div className="absolute inset-0 bg-gradient-to-r from-accent to-primary opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="relative flex items-center gap-2">
        {isLoading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Converting...</span>
          </>
        ) : (
          <>
            <Zap className="w-5 h-5" />
            <span>Convert {languageLabels[sourceLanguage]} to {languageLabels[targetLanguage]}</span>
          </>
        )}
      </div>
    </button>
  );
}
