'use client';

import { Moon, Sun } from 'lucide-react';

interface HeaderProps {
  isDark: boolean;
  setIsDark: (isDark: boolean) => void;
}

export default function Header({ isDark, setIsDark }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 transition-colors duration-300">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center text-white font-bold text-lg">
            {'<>'}
          </div>
          <div>
            <h1 className="font-bold text-lg text-foreground">SyntaxShift</h1>
            <p className="text-xs text-muted-foreground">Multi-Language Translation</p>
          </div>
        </div>

        <button
          onClick={() => setIsDark(!isDark)}
          className="p-2 rounded-lg border border-border bg-card hover:bg-muted transition-colors duration-200"
          aria-label="Toggle theme"
        >
          {isDark ? (
            <Sun className="w-5 h-5 text-primary" />
          ) : (
            <Moon className="w-5 h-5 text-primary" />
          )}
        </button>
      </div>
    </header>
  );
}
