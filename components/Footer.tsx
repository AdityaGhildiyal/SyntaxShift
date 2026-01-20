'use client';

import { Github } from 'lucide-react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full border-t border-border/30 bg-gradient-to-b from-background to-muted/20 transition-colors duration-300">
      <div className="container mx-auto px-4 py-12">
        {/* Main Footer Content */}
        <div className="flex flex-col items-center gap-6 mb-8">
          {/* Icon and Title */}
          <div className="flex items-center gap-3 mb-2">
            <div className="w-8 h-8 flex items-center justify-center text-primary text-lg">💡</div>
            <h3 className="text-lg font-semibold text-foreground">SyntaxShift</h3>
          </div>

          {/* Subtitle */}
          <p className="text-sm text-muted-foreground text-center max-w-2xl">
            Lexical Analysis → Parsing → Semantic Analysis → IR → Code Generation
          </p>

          {/* Links */}
          <div className="flex flex-wrap justify-center gap-6 items-center">
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors duration-300 group"
            >
              <Github className="w-4 h-4 group-hover:rotate-12 transition-transform duration-300" />
              <span className="text-sm">GitHub</span>
            </a>
            <div className="w-px h-4 bg-border/50"></div>
            <a
              href="/documentation"
              className="text-sm text-muted-foreground hover:text-primary transition-colors duration-300 group relative"
            >
              Documentation
              <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-primary to-accent group-hover:w-full transition-all duration-300"></span>
            </a>
            <div className="w-px h-4 bg-border/50"></div>
            <a
              href="/about"
              className="text-sm text-muted-foreground hover:text-primary transition-colors duration-300 group relative"
            >
              About
              <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-primary to-accent group-hover:w-full transition-all duration-300"></span>
            </a>
          </div>
        </div>

        {/* Divider */}
        <div className="h-px bg-gradient-to-r from-transparent via-border to-transparent mb-6"></div>

        {/* Copyright */}
        <div className="text-center text-xs text-muted-foreground/70">
          <p>© {currentYear} SyntaxShift. All rights reserved.</p>
        </div>
      </div>

      {/* Gradient Background Animation */}
      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        footer {
          animation: fadeInUp 0.8s ease-out 0.6s both;
        }
      `}</style>
    </footer>
  );
}
