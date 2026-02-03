"use client";

import { useState } from "react";
import { Search, Loader2 } from "lucide-react";

interface SearchBarProps {
  onAnalyze: (ticker: string) => void;
  isLoading: boolean;
}

export default function SearchBar({ onAnalyze, isLoading }: SearchBarProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onAnalyze(input.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          {isLoading ? (
            <Loader2 className="h-5 w-5 text-slate-400 animate-spin" />
          ) : (
            <Search className="h-5 w-5 text-slate-400" />
          )}
        </div>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value.toUpperCase())}
          placeholder="Enter stock ticker (e.g., AAPL, TSLA, MSFT)..."
          className="w-full pl-12 pr-32 py-4 text-lg rounded-xl border-2 border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isLoading ? "Analyzing..." : "Analyze"}
        </button>
      </div>
      <p className="mt-2 text-sm text-slate-500 dark:text-slate-400 text-center">
        Enter any publicly traded stock ticker to get a comprehensive AI-powered analysis
      </p>
    </form>
  );
}

