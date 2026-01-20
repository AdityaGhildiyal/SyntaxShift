'use client';

import { useState } from 'react';
import { Copy, Check, Download } from 'lucide-react';
import EditorPanel from './EditorPanel';

type TabType = 'code' | 'ast' | 'ir';

interface OutputTabsProps {
  code: string;
  language: string;
  isLoading: boolean;
  onCopy: () => void;
  copied: boolean;
}

export default function OutputTabs({ code, language, isLoading, onCopy, copied }: OutputTabsProps) {
  const [activeTab, setActiveTab] = useState<TabType>('code');

  const tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'code', label: 'Code', icon: '💻' },
    { id: 'ast', label: 'AST', icon: '🌲' },
    { id: 'ir', label: 'IR', icon: '⚙️' },
  ];

  // Mock AST data
  const mockAST = JSON.stringify(
    {
      type: 'Program',
      body: [
        {
          type: 'FunctionDef',
          name: 'fibonacci',
          params: ['n'],
          body: [
            {
              type: 'IfStatement',
              condition: { type: 'BinaryOp', left: 'n', op: '<=', right: '1' },
              consequent: { type: 'Return', value: 'n' },
            },
            {
              type: 'Return',
              value: {
                type: 'BinaryOp',
                left: { type: 'Call', name: 'fibonacci', args: ['n - 1'] },
                op: '+',
                right: { type: 'Call', name: 'fibonacci', args: ['n - 2'] },
              },
            },
          ],
        },
      ],
    },
    null,
    2
  );

  // Mock IR data
  const mockIR = `; Generated IR Code
define i32 @fibonacci(i32 %n) {
entry:
  %cmp = icmp sle i32 %n, 1
  br i1 %cmp, label %if.then, label %if.else

if.then:
  ret i32 %n

if.else:
  %sub1 = sub i32 %n, 1
  %call1 = call i32 @fibonacci(i32 %sub1)
  %sub2 = sub i32 %n, 2
  %call2 = call i32 @fibonacci(i32 %sub2)
  %add = add i32 %call1, %call2
  ret i32 %add
}`;

  const getTabContent = () => {
    switch (activeTab) {
      case 'code':
        return code;
      case 'ast':
        return mockAST;
      case 'ir':
        return mockIR;
    }
  };

  const isEmpty = !code;

  return (
    <div className="rounded-lg border border-border bg-card overflow-hidden flex flex-col h-full animate-in fade-in slide-in-from-right-4 duration-500">
      {/* Tabs Header */}
      <div className="bg-muted px-4 py-3 border-b border-border flex items-center justify-between">
        {/* Tabs */}
        <div className="flex items-center gap-2 relative">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-t-lg text-sm font-medium transition-all duration-300 flex items-center gap-2 ${
                activeTab === tab.id
                  ? 'text-primary bg-primary/10'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
          {/* Animated underline */}
          <div
            className="absolute bottom-0 h-1 bg-gradient-to-r from-primary to-accent transition-all duration-300"
            style={{
              left: `${tabs.findIndex((t) => t.id === activeTab) * 90}px`,
              width: '90px',
            }}
          ></div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={onCopy}
            disabled={isEmpty}
            className="flex items-center gap-2 px-3 py-1 rounded-md bg-primary/10 hover:bg-primary/20 text-primary transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                Copied
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copy
              </>
            )}
          </button>
          <button
            disabled={isEmpty}
            className="flex items-center gap-2 px-3 py-1 rounded-md bg-primary/10 hover:bg-primary/20 text-primary transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed group"
            title="Download"
          >
            <Download className="w-4 h-4 group-hover:translate-y-1 transition-transform duration-300" />
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-hidden relative">
        {isEmpty && !isLoading ? (
          <div className="flex flex-col items-center justify-center h-full gap-4 text-center py-12 px-4">
            <div className="text-5xl text-muted-foreground/40">📄</div>
            <div>
              <p className="text-lg font-semibold text-foreground">Converted code will appear here</p>
              <p className="text-sm text-muted-foreground">Click Convert to start the transformation</p>
            </div>
          </div>
        ) : isLoading ? (
          <div className="flex flex-col items-center justify-center h-full gap-4">
            <div className="w-12 h-12 rounded-lg border-2 border-primary/20 border-t-primary animate-spin"></div>
            <p className="text-sm text-muted-foreground">Converting code...</p>
          </div>
        ) : (
          <div className="h-full overflow-auto" key={activeTab}>
            <pre className="p-4 font-mono text-sm whitespace-pre-wrap break-words">
              <code style={{ color: 'var(--code-text)' }}>{getTabContent()}</code>
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
