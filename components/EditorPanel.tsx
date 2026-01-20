'use client';

import React from "react"

import { useState, useRef, useEffect } from 'react';
import { Loader2 } from 'lucide-react';

interface EditorPanelProps {
  code: string;
  onChange: (code: string) => void;
  language: string;
  readOnly: boolean;
  isLoading?: boolean;
}

export default function EditorPanel({
  code,
  onChange,
  language,
  readOnly,
  isLoading = false,
}: EditorPanelProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [lineNumbers, setLineNumbers] = useState<number[]>([]);

  useEffect(() => {
    const lines = code.split('\n').length;
    setLineNumbers(Array.from({ length: lines }, (_, i) => i + 1));
  }, [code]);

  const handleScroll = (e: React.UIEvent<HTMLTextAreaElement>) => {
    const pre = e.currentTarget.parentElement?.querySelector('pre');
    if (pre) {
      pre.scrollTop = (e.target as HTMLTextAreaElement).scrollTop;
      pre.scrollLeft = (e.target as HTMLTextAreaElement).scrollLeft;
    }
  };

  return (
    <div className="relative w-full h-96 overflow-hidden bg-background/50">
      {isLoading && (
        <div className="absolute inset-0 bg-background/50 backdrop-blur-sm flex items-center justify-center z-10">
          <div className="flex flex-col items-center gap-2">
            <Loader2 className="w-6 h-6 animate-spin text-primary" />
            <span className="text-sm text-muted-foreground">Converting...</span>
          </div>
        </div>
      )}
      
      <div className="flex h-full">
        {/* Line Numbers */}
        <div className="bg-muted/50 border-r border-border px-4 py-4 select-none overflow-hidden">
          <div className="font-mono text-xs text-muted-foreground leading-relaxed">
            {lineNumbers.map((num) => (
              <div key={num}>{num}</div>
            ))}
          </div>
        </div>

        {/* Code Content */}
        <div className="flex-1 relative overflow-hidden">
          <pre className="absolute inset-0 p-4 font-mono text-sm leading-relaxed text-transparent bg-transparent pointer-events-none overflow-hidden whitespace-pre-wrap break-words">
            {code}
          </pre>
          
          <textarea
            ref={textareaRef}
            value={code}
            onChange={(e) => onChange(e.target.value)}
            onScroll={handleScroll}
            readOnly={readOnly}
            spellCheck="false"
            className="absolute inset-0 p-4 font-mono text-sm leading-relaxed bg-transparent resize-none outline-none border-none overflow-auto"
            style={{
              color: 'var(--code-text)',
              backgroundColor: 'transparent',
              caretColor: readOnly ? 'transparent' : 'rgb(102 126 234 / 1)',
              fontFamily: 'JetBrains Mono, monospace',
              width: '100%',
              height: '100%',
            }}
          />
        </div>
      </div>
    </div>
  );
}
