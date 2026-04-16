import React, { useEffect, useMemo, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { Navbar, Footer, PageLayout, Button, SeverityBadge, Card } from '@/components';
import { Play, Copy, Zap, AlertCircle, CheckCircle, Loader, TrendingUp, Shield, Download, Upload } from 'lucide-react';
import { apiFetch, reportDownloadUrl, API_BASE, readApiError, readApiJson } from '@/utils/api';

interface Vulnerability {
  id: string;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  cwe_id: string;
  owasp_category: string;
  line_number: number;
  code_snippet: string;
  fix_suggestion: string;
  secure_fix_code: string;
  confidence: number;
  confidence_reason?: string;
  priority_score?: number;
  exploitability?: 'low' | 'medium' | 'high';
  remediation_priority?: 'critical' | 'high' | 'medium' | 'low';
  business_impact?: string;
  detailed_remediation?: string;
  status?: 'open' | 'reviewing' | 'resolved' | 'ignored';
  remediation_notes?: string;
  rule_id?: string;
}

interface AnalysisResult {
  id: string;
  language: string;
  vulnerabilities: Vulnerability[];
  total_issues: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  info_count: number;
  risk_score: number;
  deduplication_info?: { total_merged?: number };
  scanned_at: string;
}

interface AnalysisResponse {
  success: boolean;
  data?: AnalysisResult;
  error?: string;
  message: string;
}

interface BatchFileResult {
  filename: string;
  language: string;
  success: boolean;
  duration_ms: number;
  issues_found: number;
  risk_score: number;
  analysis_id?: string;
  error?: string;
}

interface BatchScanResult {
  batch_id: string;
  processed_files: number;
  successful_files: number;
  failed_files: number;
  total_issues: number;
  avg_risk_score: number;
  language_breakdown: Record<string, number>;
  files: BatchFileResult[];
  scanned_at: string;
}

interface BatchScanResponse {
  success: boolean;
  data?: BatchScanResult;
  error?: string;
  message: string;
}

const sampleCodes = {
  python_vulnerabilities: `# Multiple Vulnerabilities Example
import sqlite3
import os  

def get_user_data(user_id):
    # CRITICAL: SQL Injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def dangerous_code():
    # HIGH: eval() usage
    user_input = input("> ")
    result = eval(user_input)
    
    # HIGH: Command injection
    filename = input("file: ")
    os.system("cat " + filename)
    
    # HIGH: Hardcoded secret
    api_key = "sk_live_1234567890"
    return api_key

DEBUG = True  # MEDIUM: Debug mode in production`,

  javascript_vulnerabilities: `// Multiple JavaScript Vulnerabilities
function processUserContent(userData) {
  // HIGH: XSS via innerHTML
  const container = document.getElementById('content');
  container.innerHTML = '<div>' + userData.html + '</div>';
  
  // HIGH: Evaluation of user code
  eval(userData.code);
}

// HIGH: Hardcoded credentials
const DATABASE_URL = "postgresql://admin:password123@db.example.com";
const API_KEYS = {
  stripe: "sk_live_123456789",
  sendgrid: "SG.abc123def456"
};

// HIGH: Insecure random
Math.random() * 100000;

// MEDIUM: Missing auth check
function deleteRecord(id) {
  database.delete(id);  // Should check user permissions
}`,

  python_relatively_safe: `# Better security practices example
import json
import bcrypt
import os
from pathlib import Path

def get_user_safely(user_id):
    # SAFE: Use parameterized queries
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

def hash_password(password):
    # SAFE: Use bcrypt instead of MD5
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def get_config():
    # SAFE: Secrets from environment
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY not configured")
    return api_key

DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'`,

  javascript_best_practices: `// JavaScript Security Best Practices
import DOMPurify from 'dompurify';

function displayContent(userData) {
  // SAFE: Use textContent for plain text
  if (userData.type === 'text') {
    document.getElementById('content').textContent = userData.text;
  }
  
  // SAFE: Sanitize HTML with DOMPurify  
  if (userData.type === 'html') {
    const clean = DOMPurify.sanitize(userData.html);
    document.getElementById('content').innerHTML = clean;
  }
}

// SAFE: Use environment variables
const config = {
  apiKey: process.env.REACT_APP_API_KEY,
  apiUrl: process.env.REACT_APP_API_URL,
};

// SAFE: Use strong crypto
const crypto = require('crypto');
const token = crypto.randomBytes(32).toString('hex');`,
};

type SampleCodeKey = keyof typeof sampleCodes;
const LIVE_ANALYZE_DEBOUNCE_MS = 650;
type AnalysisMode = 'manual_live' | 'file_upload';
type AnalysisSource = 'manual' | 'live_editor' | 'uploaded_file';

export const AnalyzePage: React.FC = () => {
  const [code, setCode] = useState(sampleCodes.python_vulnerabilities);
  const [language, setLanguage] = useState('python');
  const [copied, setCopied] = useState(false);
  const [activeMode, setActiveMode] = useState<AnalysisMode>('manual_live');
  const [isManualAnalyzing, setIsManualAnalyzing] = useState(false);
  const [isUploadAnalyzing, setIsUploadAnalyzing] = useState(false);
  const [isBatchAnalyzing, setIsBatchAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastSuccessMessage, setLastSuccessMessage] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [analysisSource, setAnalysisSource] = useState<AnalysisSource | null>(null);
  const [expandedVuln, setExpandedVuln] = useState<string | null>(null);
  const [filterSeverity, setFilterSeverity] = useState<string>('all');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [batchFiles, setBatchFiles] = useState<FileList | null>(null);
  const [batchResult, setBatchResult] = useState<BatchScanResult | null>(null);
  const [liveModeEnabled, setLiveModeEnabled] = useState(true);
  const [liveStatus, setLiveStatus] = useState<'idle' | 'analyzing' | 'ready' | 'error'>('idle');
  const [liveError, setLiveError] = useState<string | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const liveAbortRef = useRef<AbortController | null>(null);
  const liveRequestIdRef = useRef(0);

  const languages = [
    { value: 'python', label: 'Python' },
    { value: 'javascript', label: 'JavaScript' },
  ];

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleAnalyze = async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze');
      return;
    }

    setIsManualAnalyzing(true);
    setError(null);
    setLastSuccessMessage(null);
    setAnalysisResult(null);
    setBatchResult(null);

    try {
      const response = await apiFetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language, filename: selectedFile?.name || null }),
      });

      if (!response.ok) {
        throw new Error(await readApiError(response, 'Analysis failed'));
      }

      const data = await readApiJson<AnalysisResponse>(response, 'Analysis API returned an empty response');
      
      if (data.success && data.data) {
        setAnalysisResult(data.data);
        setAnalysisSource('manual');
        setLastSuccessMessage('Manual code analysis completed.');
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to connect';
      setError(message);
      console.error('Analysis error:', err);
    } finally {
      setIsManualAnalyzing(false);
    }
  };

  const handleFileAnalyze = async () => {
    if (!selectedFile) {
      setError('Select a source file before running file scan');
      return;
    }

    setIsUploadAnalyzing(true);
    setError(null);
    setLastSuccessMessage(null);
    setAnalysisResult(null);
    setBatchResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await apiFetch('/analyze/file', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await readApiError(response, 'File analysis failed'));
      }

      const data = await readApiJson<AnalysisResponse>(response, 'File analysis API returned an empty response');
      if (data.success && data.data) {
        setAnalysisResult(data.data);
        setAnalysisSource('uploaded_file');
        setLastSuccessMessage(`Uploaded file analyzed: ${selectedFile.name}`);
        setLanguage(data.data.language);
      } else {
        setError(data.error || 'File analysis failed');
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to upload file';
      setError(message);
    } finally {
      setIsUploadAnalyzing(false);
    }
  };

  const downloadReport = (format: 'json' | 'md') => {
    if (!analysisResult) return;
    window.open(reportDownloadUrl(analysisResult.id, format), '_blank');
  };

  const updateFindingStatus = async (
    findingId: string,
    status: 'open' | 'reviewing' | 'resolved' | 'ignored',
    remediation_notes?: string
  ) => {
    if (!analysisResult) return;

    const response = await apiFetch(`/scans/${analysisResult.id}/findings/${findingId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, remediation_notes }),
    });

    if (!response.ok) return;

    setAnalysisResult((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        vulnerabilities: prev.vulnerabilities.map((v) =>
          v.id === findingId ? { ...v, status, remediation_notes: remediation_notes ?? v.remediation_notes } : v
        ),
      };
    });
  };

  const handleBatchAnalyze = async () => {
    if (!batchFiles || batchFiles.length === 0) {
      setError('Select one or more files for batch scan');
      return;
    }

    setIsBatchAnalyzing(true);
    setError(null);
    setLastSuccessMessage(null);
    setBatchResult(null);
    setAnalysisResult(null);

    try {
      const formData = new FormData();
      Array.from(batchFiles).forEach((file) => formData.append('files', file));

      const response = await apiFetch('/analyze/batch-files?continue_on_error=true', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(await readApiError(response, 'Batch scan failed'));
      }

      const data = await readApiJson<BatchScanResponse>(response, 'Batch scan API returned an empty response');
      if (data.success && data.data) {
        setBatchResult(data.data);
        setLastSuccessMessage(`Batch scan completed: ${data.data.successful_files} success, ${data.data.failed_files} failed.`);
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Batch scan failed';
      setError(message);
    } finally {
      setIsBatchAnalyzing(false);
    }
  };

  const handleDroppedFiles = (incoming: FileList | null) => {
    if (!incoming || incoming.length === 0) return;
    setError(null);
    setLastSuccessMessage(null);

    if (incoming.length > 1) {
      setBatchFiles(incoming);
      setSelectedFile(incoming[0]);
      return;
    }

    setSelectedFile(incoming[0]);
  };

  useEffect(() => {
    if (activeMode !== 'manual_live' || !liveModeEnabled) {
      if (liveAbortRef.current) {
        liveAbortRef.current.abort();
      }
      setLiveStatus('idle');
      setLiveError(null);
      return;
    }

    const trimmedCode = code.trim();
    if (trimmedCode.length < 8 || isManualAnalyzing) {
      if (liveAbortRef.current) {
        liveAbortRef.current.abort();
      }
      setLiveStatus('idle');
      setLiveError(null);
      return;
    }

    const timer = window.setTimeout(async () => {
      const requestId = liveRequestIdRef.current + 1;
      liveRequestIdRef.current = requestId;

      setLiveStatus('analyzing');
      setLiveError(null);

      if (liveAbortRef.current) {
        liveAbortRef.current.abort();
      }

      const controller = new AbortController();
      liveAbortRef.current = controller;

      try {
        const response = await apiFetch('/analyze/live', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code: trimmedCode, language }),
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(await readApiError(response, 'Live analysis failed'));
        }

        const data = await readApiJson<AnalysisResponse>(response, 'Live analysis API returned an empty response');
        if (requestId !== liveRequestIdRef.current) return;

        if (data.success && data.data) {
          setAnalysisResult(data.data);
          setAnalysisSource('live_editor');
          setBatchResult(null);
          setError(null);
          setLastSuccessMessage(null);
          setLiveStatus('ready');
        } else {
          setLiveStatus('error');
          setLiveError(data.error || 'Live analysis failed');
        }
      } catch (err) {
        if (controller.signal.aborted) {
          return;
        }
        if (requestId !== liveRequestIdRef.current) return;
        const message = err instanceof Error ? err.message : 'Live analysis failed';
        setLiveStatus('error');
        setLiveError(message);
      }
    }, LIVE_ANALYZE_DEBOUNCE_MS);

    return () => {
      window.clearTimeout(timer);
    };
  }, [code, language, activeMode, liveModeEnabled, isManualAnalyzing]);

  const loadSample = (sampleKey: SampleCodeKey) => {
    setCode(sampleCodes[sampleKey]);
    if (sampleKey.includes('javascript')) {
      setLanguage('javascript');
    } else {
      setLanguage('python');
    }
    setAnalysisResult(null);
    setAnalysisSource(null);
    setError(null);
    setLastSuccessMessage(null);
    setFilterSeverity('all');
  };

  const getSourceLabel = () => {
    if (analysisSource === 'live_editor') return 'Analysis Source: Live Editor';
    if (analysisSource === 'uploaded_file') return 'Analysis Source: Uploaded File';
    if (analysisSource === 'manual') return 'Analysis Source: Manual Code Scan';
    return null;
  };

  // Filter and sort vulnerabilities
  const filteredAndSorted = useMemo(() => {
    if (!analysisResult) return [];
    
    let filtered = analysisResult.vulnerabilities;
    
    if (filterSeverity !== 'all') {
      filtered = filtered.filter(v => v.severity === filterSeverity);
    }
    
    // Sort by priority score (if available) or confidence
    return filtered.sort((a, b) => {
      const aPriority = a.priority_score ?? (a.confidence * 100);
      const bPriority = b.priority_score ?? (b.confidence * 100);
      return bPriority - aPriority;
    });
  }, [analysisResult, filterSeverity]);

  const getRiskColor = (score: number) => {
    if (score >= 70) return 'text-red-400';
    if (score >= 40) return 'text-orange-400';
    if (score >= 10) return 'text-yellow-400';
    return 'text-green-400';
  };

  const getRiskBgColor = (score: number) => {
    if (score >= 70) return 'bg-red-900/20 border-red-900';
    if (score >= 40) return 'bg-orange-900/20 border-orange-900';
    if (score >= 10) return 'bg-yellow-900/20 border-yellow-900';
    return 'bg-green-900/20 border-green-900';
  };

  const getExploitabilityColor = (level?: string) => {
    if (level === 'high') return 'text-red-400';
    if (level === 'medium') return 'text-orange-400';
    return 'text-yellow-400';
  };

  const getMostUrgent = () => {
    if (!filteredAndSorted || filteredAndSorted.length === 0) return null;
    return filteredAndSorted[0];
  };

  const mostUrgent = getMostUrgent();

  return (
    <div className="bg-cyber-bg text-white">
      <Navbar />
      <PageLayout
        title="Code Analysis"
        subtitle="Real-time vulnerability detection with contextual reasoning"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-8 mb-8">
            {/* Code Editor */}
            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
              <Card className="h-full flex flex-col">
                <div className="mb-4 rounded-lg border border-cyber-border bg-cyber-surface/30 p-2">
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      type="button"
                      className={`px-3 py-2 rounded text-sm font-medium transition ${
                        activeMode === 'manual_live'
                          ? 'bg-cyan-700 text-white'
                          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                      }`}
                      onClick={() => setActiveMode('manual_live')}
                    >
                      Live Code Analysis
                    </button>
                    <button
                      type="button"
                      className={`px-3 py-2 rounded text-sm font-medium transition ${
                        activeMode === 'file_upload'
                          ? 'bg-purple-700 text-white'
                          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                      }`}
                      onClick={() => setActiveMode('file_upload')}
                    >
                      Upload File Analysis
                    </button>
                  </div>
                  <p className="text-xs text-gray-400 mt-2">
                    {activeMode === 'manual_live'
                      ? 'Type or paste code and optionally enable live detection while editing.'
                      : 'Upload one file for focused analysis or multiple files for batch scanning.'}
                  </p>
                </div>

                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold">Source Code</h2>
                  <button
                    onClick={handleCopy}
                    className="p-2 hover:bg-cyber-surface rounded"
                    title="Copy code"
                  >
                    <Copy size={18} className={copied ? 'text-cyan-400' : 'text-gray-400'} />
                  </button>
                </div>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-400 mb-2">Language</label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full px-3 py-2 bg-cyber-surface border border-cyber-border rounded-lg text-white focus:outline-none focus:border-cyan-500"
                  >
                    {languages.map((lang) => (
                      <option key={lang.value} value={lang.value}>{lang.label}</option>
                    ))}
                  </select>
                  <label className="mt-3 flex items-center gap-2 text-sm text-gray-300">
                    <input
                      type="checkbox"
                      checked={liveModeEnabled}
                      onChange={(e) => setLiveModeEnabled(e.target.checked)}
                      disabled={activeMode !== 'manual_live'}
                      className="accent-cyan-500"
                    />
                    Live detect while typing
                  </label>
                </div>

                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="Paste your source code here..."
                  disabled={activeMode !== 'manual_live'}
                  className="flex-1 p-4 bg-gray-900 border border-cyber-border rounded-lg text-white font-mono text-sm focus:outline-none focus:border-cyan-500 resize-none min-h-96"
                />

                <div className="mt-2 text-xs">
                  {activeMode !== 'manual_live' ? (
                    <span className="text-gray-400">Live detection is paused in upload mode.</span>
                  ) : !liveModeEnabled ? (
                    <span className="text-gray-400">Live detection is off.</span>
                  ) : liveStatus === 'analyzing' ? (
                    <span className="text-cyan-300">Detecting issues as you type...</span>
                  ) : liveStatus === 'ready' ? (
                    <span className="text-green-300">Live analysis updated.</span>
                  ) : liveStatus === 'error' ? (
                    <span className="text-red-300">{liveError || 'Live analysis failed.'}</span>
                  ) : (
                    <span className="text-gray-400">Type code to get instant issue detection.</span>
                  )}
                </div>

                <div
                  className={`mt-3 rounded-lg border p-3 transition ${
                    isDragOver
                      ? 'border-cyan-500 bg-cyan-900/20'
                      : 'border-cyber-border bg-cyber-surface/20'
                  }`}
                  onDragOver={(e) => {
                    if (activeMode !== 'file_upload') return;
                    e.preventDefault();
                    setIsDragOver(true);
                  }}
                  onDragLeave={() => setIsDragOver(false)}
                  onDrop={(e) => {
                    if (activeMode !== 'file_upload') return;
                    e.preventDefault();
                    setIsDragOver(false);
                    handleDroppedFiles(e.dataTransfer.files);
                  }}
                >
                  <label className="block text-sm font-medium text-gray-400 mb-2">Single File Scan</label>
                  <input
                    type="file"
                    accept=".py,.js,.ts,.jsx,.tsx"
                    onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                    disabled={activeMode !== 'file_upload'}
                    className="w-full text-sm text-gray-300 file:mr-3 file:px-3 file:py-1.5 file:rounded file:border-0 file:bg-cyan-700 file:text-white"
                  />
                  {selectedFile && <p className="text-xs text-gray-400 mt-2">Selected: {selectedFile.name}</p>}
                  <p className="text-xs text-gray-500 mt-2">Drag and drop a file here or use the file picker.</p>
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-400 mb-2">Batch Scan (Multiple Files)</label>
                  <input
                    type="file"
                    multiple
                    accept=".py,.js,.ts,.jsx,.tsx"
                    onChange={(e) => setBatchFiles(e.target.files)}
                    disabled={activeMode !== 'file_upload'}
                    className="w-full text-sm text-gray-300 file:mr-3 file:px-3 file:py-1.5 file:rounded file:border-0 file:bg-purple-700 file:text-white"
                  />
                  {batchFiles && batchFiles.length > 0 && <p className="text-xs text-gray-400 mt-1">{batchFiles.length} files selected.</p>}
                  <p className="text-xs text-gray-500 mt-1">Scans files independently and returns partial results if some files fail validation.</p>
                </div>

                <Button
                  variant="primary"
                  size="lg"
                  className="w-full mt-4 flex items-center justify-center gap-2"
                  onClick={handleAnalyze}
                  disabled={activeMode !== 'manual_live' || isManualAnalyzing}
                >
                  {isManualAnalyzing ? (
                    <>
                      <Loader size={20} className="animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Play size={20} />
                      Analyze Code
                    </>
                  )}
                </Button>

                <Button
                  variant="secondary"
                  size="lg"
                  className="w-full mt-2 flex items-center justify-center gap-2"
                  onClick={handleFileAnalyze}
                  disabled={activeMode !== 'file_upload' || isUploadAnalyzing || !selectedFile}
                >
                  {isUploadAnalyzing ? (
                    <>
                      <Loader size={18} className="animate-spin" />
                      Uploading & Scanning...
                    </>
                  ) : (
                    <>
                      <Upload size={18} />
                      Scan Uploaded File
                    </>
                  )}
                </Button>

                <Button
                  variant="ghost"
                  size="lg"
                  className="w-full mt-2 flex items-center justify-center gap-2"
                  onClick={handleBatchAnalyze}
                  disabled={activeMode !== 'file_upload' || isBatchAnalyzing || !batchFiles || batchFiles.length === 0}
                >
                  {isBatchAnalyzing ? (
                    <>
                      <Loader size={18} className="animate-spin" />
                      Batch Scanning...
                    </>
                  ) : (
                    <>
                      <Upload size={18} />
                      Batch Scan Files
                    </>
                  )}
                </Button>
              </Card>
            </motion.div>

            {/* Results Panel */}
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
              <Card className="h-full flex flex-col">
                {error ? (
                  <div className="flex flex-col items-center justify-center h-full">
                    <AlertCircle className="w-12 h-12 text-red-400 mb-4" />
                    <p className="text-red-400 text-center mb-2">{error}</p>
                    <p className="text-gray-400 text-sm text-center">
                      Make sure backend is running at {API_BASE}
                    </p>
                  </div>
                ) : !analysisResult ? (
                  <div className="flex flex-col items-center justify-center h-full">
                    <Zap className="w-12 h-12 text-gray-500 mb-4" />
                    <p className="text-gray-400 text-center">
                      {activeMode === 'manual_live'
                        ? (liveModeEnabled ? 'Paste code to begin live analysis, or click Analyze Code.' : 'Paste code and click Analyze Code to scan.')
                        : 'Upload a source file to analyze.'}
                    </p>
                  </div>
                ) : (
                  <>
                    <div className="mb-6">
                      <div className="flex items-center gap-2 mb-2">
                        <CheckCircle className="w-5 h-5 text-cyan-400" />
                        <h2 className="text-xl font-semibold">Analysis Results</h2>
                      </div>
                      <p className="text-gray-400 text-sm">
                        {analysisResult.total_issues} {analysisResult.total_issues === 1 ? 'issue' : 'issues'} found
                        {analysisResult.deduplication_info?.total_merged ? ` (${analysisResult.deduplication_info.total_merged} merged)` : ''}
                      </p>
                      {getSourceLabel() && <p className="text-xs text-cyan-300 mt-1">{getSourceLabel()}</p>}
                      {lastSuccessMessage && <p className="text-xs text-green-300 mt-1">{lastSuccessMessage}</p>}
                      <div className="mt-3 flex gap-2">
                        <button onClick={() => downloadReport('json')} className="px-2 py-1 text-xs rounded bg-cyan-700 hover:bg-cyan-600">
                          <Download size={12} className="inline mr-1" /> JSON Report
                        </button>
                        <button onClick={() => downloadReport('md')} className="px-2 py-1 text-xs rounded bg-purple-700 hover:bg-purple-600">
                          <Download size={12} className="inline mr-1" /> Markdown Report
                        </button>
                      </div>
                    </div>

                    {/* Summary Stats */}
                    <div className="grid grid-cols-3 gap-3 mb-6">
                      <div className={`p-3 border rounded-lg text-center ${analysisResult.critical_count > 0 ? 'bg-red-900/20 border-red-900' : 'bg-gray-900/20 border-gray-700'}`}>
                        <div className={`text-2xl font-bold ${analysisResult.critical_count > 0 ? 'text-red-400' : 'text-gray-400'}`}>
                          {analysisResult.critical_count}
                        </div>
                        <div className="text-xs text-gray-400">Critical</div>
                      </div>
                      <div className={`p-3 border rounded-lg text-center ${analysisResult.high_count > 0 ? 'bg-orange-900/20 border-orange-900' : 'bg-gray-900/20 border-gray-700'}`}>
                        <div className={`text-2xl font-bold ${analysisResult.high_count > 0 ? 'text-orange-400' : 'text-gray-400'}`}>
                          {analysisResult.high_count}
                        </div>
                        <div className="text-xs text-gray-400">High</div>
                      </div>
                      <div className={`p-3 border rounded-lg text-center ${analysisResult.medium_count > 0 ? 'bg-yellow-900/20 border-yellow-900' : 'bg-gray-900/20 border-gray-700'}`}>
                        <div className={`text-2xl font-bold ${analysisResult.medium_count > 0 ? 'text-yellow-400' : 'text-gray-400'}`}>
                          {analysisResult.medium_count}
                        </div>
                        <div className="text-xs text-gray-400">Medium</div>
                      </div>
                    </div>

                    {/* Risk Score */}
                    <div className={`p-4 border rounded-lg mb-6 ${getRiskBgColor(analysisResult.risk_score)}`}>
                      <div className="text-sm text-gray-400 mb-1">Overall Risk Score</div>
                      <div className={`text-3xl font-bold ${getRiskColor(analysisResult.risk_score)}`}>
                        {analysisResult.risk_score.toFixed(1)} / 100
                      </div>
                    </div>

                    {/* Most Urgent Highlight */}
                    {mostUrgent && (
                      <div className="p-3 bg-red-900/20 border border-red-900 rounded-lg mb-4">
                        <div className="flex items-center gap-2 text-red-400 text-sm font-semibold mb-1">
                          <TrendingUp size={14} />
                          Most Urgent
                        </div>
                        <div className="text-white text-sm">{mostUrgent.title}</div>
                      </div>
                    )}

                    {/* Filter Buttons */}
                    <div className="flex gap-2 mb-4">
                      {['all', 'critical', 'high', 'medium'].map((sev) => (
                        <button
                          key={sev}
                          onClick={() => setFilterSeverity(sev)}
                          className={`px-3 py-1 text-xs rounded transition ${
                            filterSeverity === sev
                              ? 'bg-cyan-600 text-white'
                              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                          }`}
                        >
                          {sev === 'all' ? 'All' : sev.charAt(0).toUpperCase() + sev.slice(1)}
                        </button>
                      ))}
                    </div>

                    {/* Vulnerabilities List */}
                    <div className="space-y-2 flex-1 overflow-y-auto">
                      {filteredAndSorted.length === 0 ? (
                        <p className="text-green-400 text-center py-8">✓ No issues found!</p>
                      ) : (
                        filteredAndSorted.map((vuln) => (
                          <motion.div
                            key={vuln.id}
                            className="p-3 bg-cyber-surface/50 border border-cyber-border rounded-lg hover:border-cyan-500/50 transition cursor-pointer"
                            onClick={() => setExpandedVuln(expandedVuln === vuln.id ? null : vuln.id)}
                          >
                            <div className="flex items-start justify-between gap-2 mb-1">
                              <h3 className="font-semibold text-white text-sm flex-1 line-clamp-1">{vuln.title}</h3>
                              <SeverityBadge severity={vuln.severity} className="text-xs">
                                {vuln.severity}
                              </SeverityBadge>
                            </div>
                            <div className="flex gap-2 flex-wrap text-xs text-gray-400 mb-1">
                              <span>{vuln.cwe_id}</span>
                              <span>L{vuln.line_number}</span>
                              <span className="text-cyan-400">{(vuln.confidence * 100).toFixed(0)}% conf</span>
                              {vuln.priority_score && <span className="text-orange-400">P{(vuln.priority_score).toFixed(0)}</span>}
                              {vuln.exploitability && <span className={getExploitabilityColor(vuln.exploitability)}>{vuln.exploitability}</span>}
                            </div>

                            {expandedVuln === vuln.id && (
                              <motion.div
                                className="border-t border-cyber-border pt-3 mt-2 text-xs"
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                              >
                                {vuln.description && <p className="text-gray-300 mb-2">{vuln.description}</p>}
                                {vuln.confidence_reason && <p className="text-gray-400 mb-2">Reason: {vuln.confidence_reason}</p>}
                                {vuln.code_snippet && (
                                  <div className="mb-2">
                                    <p className="text-gray-400 mb-1">Code:</p>
                                    <code className="text-cyan-300 bg-gray-900 p-2 rounded block whitespace-pre-wrap leading-tight">
                                      {vuln.code_snippet.substring(0, 150)}{vuln.code_snippet.length > 150 ? '...' : ''}
                                    </code>
                                  </div>
                                )}
                                {vuln.fix_suggestion && (
                                  <div className="mb-2 p-2 bg-green-900/20 rounded border border-green-900">
                                    <p className="text-green-400 font-semibold mb-1">Fix:</p>
                                    <p className="text-green-300">{vuln.fix_suggestion}</p>
                                  </div>
                                )}
                                {vuln.business_impact && <p className="text-gray-400">Impact: {vuln.business_impact}</p>}

                                <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-2">
                                  <select
                                    value={vuln.status || 'open'}
                                    onChange={(e) => updateFindingStatus(vuln.id, e.target.value as 'open' | 'reviewing' | 'resolved' | 'ignored', vuln.remediation_notes)}
                                    className="px-2 py-1 bg-cyber-surface border border-cyber-border rounded text-white"
                                  >
                                    <option value="open">Open</option>
                                    <option value="reviewing">Reviewing</option>
                                    <option value="resolved">Resolved</option>
                                    <option value="ignored">Ignored</option>
                                  </select>
                                  <button
                                    className="px-2 py-1 bg-cyan-800 rounded"
                                    onClick={() => {
                                      const notes = window.prompt('Remediation notes', vuln.remediation_notes || '');
                                      if (notes !== null) {
                                        updateFindingStatus(vuln.id, vuln.status || 'open', notes);
                                      }
                                    }}
                                  >
                                    Add Notes
                                  </button>
                                </div>
                                {vuln.remediation_notes && <p className="text-gray-300 mt-2">Notes: {vuln.remediation_notes}</p>}
                              </motion.div>
                            )}
                          </motion.div>
                        ))
                      )}
                    </div>
                  </>
                )}
              </Card>
            </motion.div>
          </div>

          {batchResult && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
              <Card className="p-5">
                <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
                  <h3 className="text-lg font-semibold">Batch Scan Summary</h3>
                  <span className="text-xs text-gray-400">Batch ID: {batchResult.batch_id}</span>
                </div>
                <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-3 mb-4 text-sm">
                  <div className="p-3 rounded border border-cyber-border bg-cyber-surface/30">
                    <div className="text-gray-400">Processed</div>
                    <div className="text-xl font-semibold">{batchResult.processed_files}</div>
                  </div>
                  <div className="p-3 rounded border border-green-800 bg-green-900/20">
                    <div className="text-gray-300">Successful</div>
                    <div className="text-xl font-semibold text-green-300">{batchResult.successful_files}</div>
                  </div>
                  <div className="p-3 rounded border border-red-800 bg-red-900/20">
                    <div className="text-gray-300">Failed</div>
                    <div className="text-xl font-semibold text-red-300">{batchResult.failed_files}</div>
                  </div>
                  <div className="p-3 rounded border border-cyber-border bg-cyber-surface/30">
                    <div className="text-gray-400">Total Issues</div>
                    <div className="text-xl font-semibold">{batchResult.total_issues}</div>
                  </div>
                  <div className="p-3 rounded border border-cyber-border bg-cyber-surface/30">
                    <div className="text-gray-400">Avg Risk</div>
                    <div className="text-xl font-semibold">{batchResult.avg_risk_score.toFixed(1)}</div>
                  </div>
                </div>

                <div className="mb-4">
                  <div className="text-sm text-gray-400 mb-2">Languages</div>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(batchResult.language_breakdown).map(([lang, count]) => (
                      <span key={lang} className="px-2 py-1 rounded border border-cyan-700 bg-cyan-900/30 text-cyan-200 text-xs">
                        {lang}: {count}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {batchResult.files.map((item) => (
                    <div key={`${item.filename}-${item.analysis_id || 'err'}`} className="p-3 rounded border border-cyber-border bg-cyber-surface/20 text-sm">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <span className="font-medium">{item.filename}</span>
                        <span className={item.success ? 'text-green-300' : 'text-red-300'}>
                          {item.success ? 'Success' : 'Failed'}
                        </span>
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        {item.language} | {item.issues_found} issues | risk {item.risk_score.toFixed(1)} | {item.duration_ms} ms
                      </div>
                      {!item.success && item.error && <div className="text-xs text-red-300 mt-1">{item.error}</div>}
                    </div>
                  ))}
                </div>
              </Card>
            </motion.div>
          )}

          {/* Sample Code Section */}
          <motion.section className="mt-20 border-t border-cyber-border pt-20" initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
            <h2 className="text-3xl font-bold mb-8">Sample Code</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { title: 'Python: Vulnerabilities', sample: 'python_vulnerabilities' as SampleCodeKey, icon: '⚠️' },
                { title: 'JavaScript: Vulnerabilities', sample: 'javascript_vulnerabilities' as SampleCodeKey, icon: '🕷️' },
                { title: 'Python: Best Practices', sample: 'python_relatively_safe' as SampleCodeKey, icon: '✅' },
                { title: 'JavaScript: Best Practices', sample: 'javascript_best_practices' as SampleCodeKey, icon: '✅' },
              ].map((sample, index) => (
                <Card key={index} className="cursor-pointer hover:border-cyan-500/50" onClick={() => loadSample(sample.sample)}>
                  <div className="mb-3 text-2xl">{sample.icon}</div>
                  <h3 className="font-semibold text-white mb-2">{sample.title}</h3>
                  <p className="text-sm text-cyan-400">Load →</p>
                </Card>
              ))}
            </div>
          </motion.section>

          {/* Features Section */}
          <motion.section className="mt-20 border-t border-cyber-border pt-20 mb-20" initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
            <h2 className="text-3xl font-bold mb-8">Phase 3: Intelligent Analysis</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold mb-4 text-cyan-400 flex items-center gap-2"><Shield size={20} /> Smart Detection</h3>
                <ul className="space-y-2 text-gray-300 text-sm">
                  <li>✓ Context-aware vulnerability analysis</li>
                  <li>✓ Automatic false-positive filtering</li>
                  <li>✓ Confidence-based prioritization</li>
                  <li>✓ Exploitability assessment</li>
                  <li>✓ Deduplication of similar findings</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-4 text-purple-400 flex items-center gap-2"><TrendingUp size={20} /> Rich Insights</h3>
                <ul className="space-y-2 text-gray-300 text-sm">
                  <li>✓ Detailed remediation guidance</li>
                  <li>✓ CWE and OWASP classification</li>
                  <li>✓ Business impact analysis</li>
                  <li>✓ Priority scoring (0-100)</li>
                  <li>✓ Confidence reasoning</li>
                </ul>
              </div>
            </div>
          </motion.section>
        </div>
      </PageLayout>

      <Footer />
    </div>
  );
};
