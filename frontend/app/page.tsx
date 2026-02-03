"use client";

import { useState } from "react";
import { Search, TrendingUp, BarChart3, Newspaper, Globe } from "lucide-react";
import AnalysisView from "@/components/AnalysisView";
import SearchBar from "@/components/SearchBar";

export default function Home() {
  const [ticker, setTicker] = useState<string>("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState<any>(null);

  const handleAnalyze = async (searchTicker: string) => {
    setTicker(searchTicker.toUpperCase());
    setIsAnalyzing(true);
    setAnalysisData(null);

    try {
      const response = await fetch(`http://localhost:8000/api/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ticker: searchTicker.toUpperCase() }),
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();
      setAnalysisData(data);
    } catch (error) {
      console.error("Error analyzing stock:", error);
      alert("Failed to analyze stock. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="border-b bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-lg">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Trading Research Agent
                </h1>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  AI-Powered Stock Analysis
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {!analysisData && !isAnalyzing && (
          <div className="max-w-4xl mx-auto">
            {/* Hero Section */}
            <div className="text-center mb-12 space-y-4">
              <h2 className="text-5xl font-bold text-slate-900 dark:text-white">
                Comprehensive Stock Analysis
              </h2>
              <p className="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
                Get AI-powered insights combining fundamental, technical, sentiment, and macro analysis
              </p>
            </div>

            {/* Search Bar */}
            <SearchBar onAnalyze={handleAnalyze} isLoading={isAnalyzing} />

            {/* Features Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
              <FeatureCard
                icon={<BarChart3 className="h-8 w-8" />}
                title="Fundamental Analysis"
                description="Deep dive into financials, valuation, and growth metrics"
                color="from-blue-500 to-cyan-500"
              />
              <FeatureCard
                icon={<TrendingUp className="h-8 w-8" />}
                title="Technical Analysis"
                description="Price trends, indicators, and momentum signals"
                color="from-purple-500 to-pink-500"
              />
              <FeatureCard
                icon={<Newspaper className="h-8 w-8" />}
                title="Sentiment Analysis"
                description="Market perception from recent news and headlines"
                color="from-orange-500 to-red-500"
              />
              <FeatureCard
                icon={<Globe className="h-8 w-8" />}
                title="Macro Context"
                description="Economic outlook and market conditions"
                color="from-green-500 to-emerald-500"
              />
            </div>
          </div>
        )}

        {/* Analysis View */}
        {(isAnalyzing || analysisData) && (
          <AnalysisView
            ticker={ticker}
            isLoading={isAnalyzing}
            data={analysisData}
            onNewSearch={() => {
              setAnalysisData(null);
              setTicker("");
            }}
          />
        )}
      </main>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
  color,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  color: string;
}) {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
      <div className={`bg-gradient-to-br ${color} p-3 rounded-lg w-fit mb-4 text-white`}>
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
        {title}
      </h3>
      <p className="text-slate-600 dark:text-slate-400 text-sm">{description}</p>
    </div>
  );
}

