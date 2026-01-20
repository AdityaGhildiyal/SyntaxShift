'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, Target, Users, Lightbulb, Zap, Globe, Award, Moon, Sun } from 'lucide-react';

export default function About() {
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
  const team = [
    {
      name: 'Project Goals',
      description: 'Build a production-grade compiler with complete pipeline implementation',
      icon: Target,
    },
    {
      name: 'Educational Focus',
      description: 'Demonstrate compiler design principles through practical application',
      icon: Lightbulb,
    },
    {
      name: 'Open Source',
      description: 'Community-driven development with transparent architecture',
      icon: Globe,
    },
  ];

  const features = [
    {
      title: 'Complete Compiler Pipeline',
      description:
        'Implements all major stages of compilation from lexical analysis to code generation.',
    },
    {
      title: 'Multi-Language Support',
      description: 'Supports Python, Java, and C++ with potential for future language additions.',
    },
    {
      title: 'AST Visualization',
      description:
        'View the Abstract Syntax Tree to understand how the compiler parses code structure.',
    },
    {
      title: 'Intermediate Representation',
      description:
        'Explore the language-agnostic IR layer that bridges different programming languages.',
    },
    {
      title: 'Semantic Analysis',
      description:
        'Type checking and semantic validation ensure correctness across language boundaries.',
    },
    {
      title: 'Clean Architecture',
      description: 'Well-structured, maintainable codebase following compiler design best practices.',
    },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="border-b border-border bg-gradient-to-b from-card to-background sticky top-0 z-40">
        <div className="container mx-auto px-4 py-6 flex justify-between items-start">
          <div>
            <Link
              href="/"
              className="inline-flex items-center gap-2 text-primary hover:text-accent transition-colors mb-4"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Converter
            </Link>
            <h1 className="text-4xl font-bold mb-2">About SyntaxShift</h1>
            <p className="text-muted-foreground">A comprehensive compiler design implementation</p>
          </div>
          <button
            onClick={handleThemeToggle}
            className="p-2 rounded-lg border border-border bg-card hover:bg-muted transition-colors duration-200 mt-2"
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

      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <section className="mb-16">
          <div className="bg-gradient-to-r from-primary/10 via-accent/10 to-primary/10 border border-border rounded-lg p-8 md:p-12">
            <h2 className="text-3xl font-bold mb-4">What is SyntaxShift?</h2>
            <p className="text-lg text-muted-foreground max-w-3xl leading-relaxed">
              SyntaxShift is an advanced compiler design project that demonstrates a complete translation pipeline
              for converting source code between different programming languages. By implementing a full-featured
              compiler frontend, the project showcases fundamental computer science concepts including lexical analysis,
              parsing, semantic analysis, intermediate representation, and code generation.
            </p>
          </div>
        </section>

        {/* Mission & Values */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8">Our Mission</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {team.map((item, index) => {
              const Icon = item.icon;
              return (
                <div key={index} className="bg-card border border-border rounded-lg p-6 hover:border-primary/50 transition-colors">
                  <div className="flex items-center justify-center h-12 w-12 rounded-lg bg-primary/10 mb-4">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2">{item.name}</h3>
                  <p className="text-muted-foreground text-sm">{item.description}</p>
                </div>
              );
            })}
          </div>
        </section>

        {/* Features Section */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8">Core Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <div key={index} className="bg-card border border-border rounded-lg p-6 group hover:border-primary/50 transition-colors">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <div className="flex items-center justify-center h-10 w-10 rounded-lg bg-primary/10 group-hover:bg-primary/20 transition-colors">
                      <Zap className="h-5 w-5 text-primary" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                    <p className="text-muted-foreground text-sm">{feature.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Technology Stack */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8">Technology Stack</h2>
          <div className="bg-card border border-border rounded-lg p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
                  <span className="text-primary">⚙️</span> Frontend
                </h3>
                <ul className="space-y-2 text-muted-foreground">
                  <li>• React 19 with TypeScript</li>
                  <li>• Next.js 16 App Router</li>
                  <li>• Tailwind CSS v4</li>
                  <li>• Modern UI Components</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
                  <span className="text-accent">🔧</span> Compiler
                </h3>
                <ul className="space-y-2 text-muted-foreground">
                  <li>• Lexical Analyzer</li>
                  <li>• Parser (Recursive Descent)</li>
                  <li>• AST Construction</li>
                  <li>• Code Generation Engine</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Architecture Section */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8">Architecture Overview</h2>
          <div className="space-y-4">
            <div className="bg-card border border-border rounded-lg p-6">
              <h3 className="font-semibold text-lg mb-4">Design Principles</h3>
              <div className="space-y-3 text-muted-foreground">
                <p>
                  <strong className="text-foreground">Modularity:</strong> Each compilation stage is isolated and independently
                  testable, following the single responsibility principle.
                </p>
                <p>
                  <strong className="text-foreground">Extensibility:</strong> Adding new languages or compilation stages requires
                  minimal changes to existing code.
                </p>
                <p>
                  <strong className="text-foreground">Performance:</strong> Optimized token processing and AST traversal for
                  real-time conversion feedback.
                </p>
                <p>
                  <strong className="text-foreground">Correctness:</strong> Comprehensive error handling and semantic validation
                  throughout the pipeline.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Use Cases */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8">Use Cases</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <Award className="w-5 h-5 text-primary" />
                <h3 className="font-semibold">Learning Tool</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Understand compiler design through practical implementation and visual debugging tools.
              </p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <Users className="w-5 h-5 text-primary" />
                <h3 className="font-semibold">Code Migration</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Assist in migrating codebases between Python, Java, and C++ with structural preservation.
              </p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <Lightbulb className="w-5 h-5 text-primary" />
                <h3 className="font-semibold">Research Platform</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                A foundation for experimenting with compiler optimizations and transformations.
              </p>
            </div>
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <Globe className="w-5 h-5 text-primary" />
                <h3 className="font-semibold">Educational Reference</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                A well-documented example of modern compiler design principles in action.
              </p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-gradient-to-r from-primary/10 via-accent/10 to-primary/10 border border-border rounded-lg p-8 text-center">
          <h2 className="text-2xl font-bold mb-4">Get Started</h2>
          <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
            Ready to explore code conversion? Try converting your first piece of code or dive into the documentation to learn
            more about how the compiler works.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/"
              className="px-6 py-2 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-accent transition-colors"
            >
              Try Converter
            </Link>
            <Link
              href="/documentation"
              className="px-6 py-2 border border-primary text-primary rounded-lg font-semibold hover:bg-primary/10 transition-colors"
            >
              Read Documentation
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}
