'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, Code, Zap, GitBranch, Cpu, Package, FileCode, Moon, Sun } from 'lucide-react';

export default function Documentation() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setIsDark(prefersDark);
    if (prefersDark) {
      document.documentElement.classList.add('dark');
    }
  }, []);

  const handleThemeToggle = () => {
    setIsDark(!isDark);
    if (!isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };
  const stages = [
    {
      icon: Code,
      title: 'Lexical Analysis',
      description: 'The source code is tokenized into meaningful units (tokens) such as keywords, identifiers, operators, and literals.',
      details: [
        'Reads input character by character',
        'Groups characters into tokens',
        'Removes whitespace and comments',
        'Identifies token types (keyword, identifier, etc.)',
      ],
    },
    {
      icon: GitBranch,
      title: 'Parsing',
      description: 'Tokens are organized into a hierarchical structure called an Abstract Syntax Tree (AST) based on grammar rules.',
      details: [
        'Validates token sequence against grammar',
        'Creates Abstract Syntax Tree (AST)',
        'Detects syntax errors',
        'Organizes code structure',
      ],
    },
    {
      icon: Cpu,
      title: 'Semantic Analysis',
      description: 'The AST is analyzed to check for semantic correctness, including type checking and symbol resolution.',
      details: [
        'Type checking and inference',
        'Symbol table management',
        'Scope resolution',
        'Semantic error detection',
      ],
    },
    {
      icon: Zap,
      title: 'Intermediate Representation (IR)',
      description: 'The semantic AST is converted to an intermediate representation that is independent of both source and target languages.',
      details: [
        'Language-agnostic representation',
        'Code optimization opportunities',
        'Simplified structure for translation',
        'Platform-independent format',
      ],
    },
    {
      icon: Package,
      title: 'Code Generation',
      description: 'The IR is transformed into target language code with proper syntax and semantics.',
      details: [
        'Transforms IR to target language',
        'Generates syntactically correct code',
        'Applies language-specific patterns',
        'Maintains semantic correctness',
      ],
    },
  ];

  const supportedLanguages = [
    { name: 'Python', color: 'from-blue-400 to-blue-600' },
    { name: 'Java', color: 'from-red-400 to-red-600' },
    { name: 'C++', color: 'from-cyan-400 to-cyan-600' },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
      {/* Header */}
      <header className="border-b border-border bg-gradient-to-b from-card to-background sticky top-0 z-40 transition-colors duration-300">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between mb-4">
            <Link
              href="/"
              className="inline-flex items-center gap-2 text-primary hover:text-accent transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Converter
            </Link>
            <button
              onClick={handleThemeToggle}
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
          <h1 className="text-4xl font-bold mb-2">Documentation</h1>
          <p className="text-muted-foreground">Understanding the compiler design and architecture</p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        {/* Compiler Pipeline Section */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8 flex items-center gap-3">
            <Code className="w-6 h-6 text-primary" />
            Compiler Pipeline
          </h2>
          <p className="text-muted-foreground mb-8 max-w-2xl">
            The SyntaxShift tool implements a complete compiler frontend that transforms source code from one language to another through a sophisticated multi-stage pipeline.
          </p>

          <div className="space-y-6">
            {stages.map((stage, index) => {
              const Icon = stage.icon;
              return (
                <div
                  key={index}
                  className="bg-card border border-border rounded-lg p-6 hover:border-primary/50 transition-colors animate-in fade-in"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex gap-4">
                    <div className="flex-shrink-0">
                      <div className="flex items-center justify-center h-12 w-12 rounded-lg bg-primary/10">
                        <Icon className="h-6 w-6 text-primary" />
                      </div>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold mb-2">{stage.title}</h3>
                      <p className="text-muted-foreground mb-4">{stage.description}</p>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {stage.details.map((detail, i) => (
                          <div key={i} className="flex items-start gap-2 text-sm">
                            <span className="text-primary mt-1">•</span>
                            <span>{detail}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* Supported Languages */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8 flex items-center gap-3">
            <FileCode className="w-6 h-6 text-primary" />
            Supported Languages
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {supportedLanguages.map((lang, index) => (
              <div
                key={index}
                className="bg-card border border-border rounded-lg p-6 text-center hover:border-primary/50 transition-colors"
              >
                <div className={`h-12 w-12 rounded-lg bg-gradient-to-br ${lang.color} mx-auto mb-4`}></div>
                <h3 className="text-lg font-semibold">{lang.name}</h3>
                <p className="text-sm text-muted-foreground mt-2">Full support for conversion</p>
              </div>
            ))}
          </div>
        </section>

        {/* How It Works */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8">How It Works</h2>
          <div className="bg-card border border-border rounded-lg p-8">
            <div className="space-y-6">
              <div>
                <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">1</span>
                  Input Source Code
                </h3>
                <p className="text-muted-foreground">You paste code in Python, Java, or C++ into the input panel.</p>
              </div>
              <div className="h-8 flex items-center justify-center text-muted-foreground">↓</div>
              <div>
                <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">2</span>
                  Lexical Analysis
                </h3>
                <p className="text-muted-foreground">The input is tokenized into semantic units and analyzed for validity.</p>
              </div>
              <div className="h-8 flex items-center justify-center text-muted-foreground">↓</div>
              <div>
                <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">3</span>
                  AST Construction
                </h3>
                <p className="text-muted-foreground">Tokens are parsed into an Abstract Syntax Tree representing the code structure.</p>
              </div>
              <div className="h-8 flex items-center justify-center text-muted-foreground">↓</div>
              <div>
                <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">4</span>
                  Semantic Analysis
                </h3>
                <p className="text-muted-foreground">Type checking and semantic validation ensure code correctness across languages.</p>
              </div>
              <div className="h-8 flex items-center justify-center text-muted-foreground">↓</div>
              <div>
                <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm">5</span>
                  IR Generation & Target Code
                </h3>
                <p className="text-muted-foreground">The semantic AST is converted to IR and then to the target language.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Key Features */}
        <section>
          <h2 className="text-2xl font-bold mb-8">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-card border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-2">Multi-Language Support</h3>
              <p className="text-sm text-muted-foreground">Convert seamlessly between Python, Java, and C++.</p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-2">Abstract Syntax Tree Visualization</h3>
              <p className="text-sm text-muted-foreground">View the AST structure for deeper understanding of code analysis.</p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-2">Intermediate Representation</h3>
              <p className="text-sm text-muted-foreground">Explore the IR layer showing language-agnostic code structure.</p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <h3 className="font-semibold mb-2">Real-time Conversion</h3>
              <p className="text-sm text-muted-foreground">Instant feedback with animated conversion process.</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
