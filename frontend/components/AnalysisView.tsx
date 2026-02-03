"use client";

import { useState } from "react";
import { ArrowLeft, Loader2, TrendingUp, BarChart3, Newspaper, Globe, FileText } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface AnalysisViewProps {
  ticker: string;
  isLoading: boolean;
  data: any;
  onNewSearch: () => void;
}

export default function AnalysisView({ ticker, isLoading, data, onNewSearch }: AnalysisViewProps) {
  const [activeTab, setActiveTab] = useState("report");

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-12">
          <div className="flex flex-col items-center justify-center space-y-6">
            <div className="relative">
              <Loader2 className="h-16 w-16 text-blue-500 animate-spin" />
              <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-xl animate-pulse" />
            </div>
            <div className="text-center space-y-2">
              <h3 className="text-2xl font-bold text-slate-900 dark:text-white">
                Analyzing {ticker}
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                Running parallel analyses across 4 dimensions...
              </p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full max-w-2xl">
              <LoadingCard icon={<BarChart3 />} label="Fundamental" />
              <LoadingCard icon={<TrendingUp />} label="Technical" />
              <LoadingCard icon={<Newspaper />} label="Sentiment" />
              <LoadingCard icon={<Globe />} label="Macro" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const tabs = [
    { id: "report", label: "Final Report", icon: <FileText className="h-4 w-4" /> },
    { id: "fundamental", label: "Fundamental", icon: <BarChart3 className="h-4 w-4" /> },
    { id: "technical", label: "Technical", icon: <TrendingUp className="h-4 w-4" /> },
    { id: "sentiment", label: "Sentiment", icon: <Newspaper className="h-4 w-4" /> },
    { id: "macro", label: "Macro", icon: <Globe className="h-4 w-4" /> },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <button
          onClick={onNewSearch}
          className="flex items-center space-x-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
        >
          <ArrowLeft className="h-5 w-5" />
          <span>New Search</span>
        </button>
        <div className="text-right">
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white">{ticker}</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Analysis completed at {new Date(data.timestamp).toLocaleString()}
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg overflow-hidden">
        <div className="border-b border-slate-200 dark:border-slate-700">
          <div className="flex overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-6 py-4 font-medium transition-colors whitespace-nowrap ${
                  activeTab === tab.id
                    ? "text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400"
                    : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                }`}
              >
                {tab.icon}
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          <div className="prose prose-slate dark:prose-invert max-w-none">
            {activeTab === "report" && (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {data.final_report}
              </ReactMarkdown>
            )}
            {activeTab === "fundamental" && (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {data.fundamental_analysis}
              </ReactMarkdown>
            )}
            {activeTab === "technical" && (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {data.technical_analysis}
              </ReactMarkdown>
            )}
            {activeTab === "sentiment" && (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {data.sentiment_analysis}
              </ReactMarkdown>
            )}
            {activeTab === "macro" && (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {data.macro_analysis}
              </ReactMarkdown>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function LoadingCard({ icon, label }: { icon: React.ReactNode; label: string }) {
  return (
    <div className="bg-slate-50 dark:bg-slate-700/50 rounded-lg p-4 flex flex-col items-center space-y-2">
      <div className="text-slate-400 dark:text-slate-500 animate-pulse">{icon}</div>
      <span className="text-xs text-slate-600 dark:text-slate-400">{label}</span>
    </div>
  );
}

