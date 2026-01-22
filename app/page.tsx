'use client';

import { useState, useEffect } from 'react';
import { Moon, Sun, Copy, Check, ArrowRight } from 'lucide-react';
import Header from '@/components/Header';
import EditorPanel from '@/components/EditorPanel';
import LanguageSelector from '@/components/LanguageSelector';
import ConvertButton from '@/components/ConvertButton';
import OutputTabs from '@/components/OutputTabs';
import Footer from '@/components/Footer';
import { mockCodeConversions } from '@/lib/mockConversions';

export default function Home() {
  const [isDark, setIsDark] = useState(true);
  const [inputCode, setInputCode] = useState(`def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(result)`);

  const [sourceLanguage, setSourceLanguage] = useState('python');
  const [targetLanguage, setTargetLanguage] = useState('java');
  const [outputCode, setOutputCode] = useState('');
  const [isConverting, setIsConverting] = useState(false);
  const [copiedOutput, setCopiedOutput] = useState(false);
  const [copiedInput, setCopiedInput] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const handleConvert = async () => {
    setIsConverting(true);
    
    try {
      const response = await fetch('http://localhost:8000/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          source_code: inputCode,
          source_language: sourceLanguage,
          target_language: targetLanguage,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setOutputCode(data.target_code);
      } else {
        setOutputCode(`/* ERROR: \n${data.error} \n*/`);
      }
    } catch (error) {
      console.error('Error during conversion:', error);
      setOutputCode('// Error connecting to the compiler backend.\n// Please ensure the backend server is running (port 8000).');
    } finally {
      setIsConverting(false);
    }
  };

  const handleCopyInput = () => {
    navigator.clipboard.writeText(inputCode);
    setCopiedInput(true);
    setTimeout(() => setCopiedInput(false), 2000);
  };

  const handleCopyOutput = () => {
    navigator.clipboard.writeText(outputCode);
    setCopiedOutput(true);
    setTimeout(() => setCopiedOutput(false), 2000);
  };

  const languages = ['python', 'java', 'cpp'];

  return (
    <main className="min-h-screen bg-background text-foreground transition-colors duration-300">
      <Header isDark={isDark} setIsDark={setIsDark} />

      <div className="container mx-auto px-4 py-8 md:py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            SyntaxShift
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Instantly translate code between Python, Java, and C++
          </p>
        </div>

        {/* Language Selection */}
        <div className="mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-end">
            <div>
              <label className="block text-sm font-semibold mb-3 text-foreground">Source Language</label>
              <LanguageSelector
                value={sourceLanguage}
                onChange={setSourceLanguage}
                languages={languages}
              />
            </div>

            <div className="flex justify-center md:justify-center">
              <div className="bg-primary/10 p-3 rounded-lg">
                <ArrowRight className="w-6 h-6 text-primary" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold mb-3 text-foreground">Target Language</label>
              <LanguageSelector
                value={targetLanguage}
                onChange={setTargetLanguage}
                languages={languages}
              />
            </div>
          </div>
        </div>

        {/* Editor Panels */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8 min-h-96">
          {/* Input Editor */}
          <div className="rounded-lg border border-border bg-card overflow-hidden flex flex-col animate-in fade-in slide-in-from-left-4 duration-500">
            <div className="bg-muted px-4 py-3 border-b border-border flex items-center justify-between">
              <span className="text-sm font-semibold text-foreground">Input Code</span>
              <button
                onClick={handleCopyInput}
                className="flex items-center gap-2 px-3 py-1 rounded-md bg-primary/10 hover:bg-primary/20 text-primary transition-colors text-sm"
              >
                {copiedInput ? (
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
            </div>
            <div className="flex-1 overflow-hidden">
              <EditorPanel
                code={inputCode}
                onChange={setInputCode}
                language={sourceLanguage}
                readOnly={false}
              />
            </div>
          </div>

          {/* Output Tabs Panel */}
          <OutputTabs
            code={outputCode}
            language={targetLanguage}
            isLoading={isConverting}
            onCopy={handleCopyOutput}
            copied={copiedOutput}
          />
        </div>

        {/* Convert Button */}
        <div className="flex justify-center mb-8">
          <ConvertButton
            onClick={handleConvert}
            isLoading={isConverting}
            sourceLanguage={sourceLanguage}
            targetLanguage={targetLanguage}
          />
        </div>

        {/* Info Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="bg-card border border-border rounded-lg p-6">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
              <span className="text-primary font-bold">⚡</span>
            </div>
            <h3 className="font-semibold text-lg mb-2">Instant Conversion</h3>
            <p className="text-muted-foreground text-sm">Convert your code instantly with just one click</p>
          </div>

          <div className="bg-card border border-border rounded-lg p-6">
            <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
              <span className="text-accent font-bold">🎯</span>
            </div>
            <h3 className="font-semibold text-lg mb-2">Three Languages</h3>
            <p className="text-muted-foreground text-sm">Convert between Python, Java, and C++</p>
          </div>

          <div className="bg-card border border-border rounded-lg p-6">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
              <span className="text-primary font-bold">✨</span>
            </div>
            <h3 className="font-semibold text-lg mb-2">Smooth Experience</h3>
            <p className="text-muted-foreground text-sm">Enjoy beautiful animations and smooth interactions</p>
          </div>
        </div>
      </div>

      <Footer />
    </main>
  );
}
