import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, AlertTriangle, BarChart3, Bug, Database, ShieldCheck } from 'lucide-react';
import { Card, Footer, Navbar, PageLayout } from '@/components';
import { apiFetch, readApiError, readApiJson } from '@/utils/api';

interface ScanSummary {
  total_scans: number;
  total_vulnerabilities: number;
  average_risk_score: number;
  most_common_language?: string;
  highest_risk_scan_id?: string;
  highest_risk_score: number;
  top_cwe_ids: string[];
  top_finding_titles: string[];
  severity_distribution: Record<string, number>;
  language_distribution: Record<string, number>;
  avg_findings_per_scan: number;
  scans_last_7_days: number;
  open_findings: number;
  reviewing_findings: number;
  resolved_findings: number;
  ignored_findings: number;
  generated_at: string;
}

export const DashboardPage: React.FC = () => {
  const [summary, setSummary] = useState<ScanSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadSummary = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiFetch('/scans/summary');
        if (!response.ok) throw new Error(await readApiError(response, 'Failed to load dashboard analytics'));
        const data = await readApiJson<ScanSummary>(response, 'Dashboard returned an empty response');
        setSummary(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load analytics');
      } finally {
        setLoading(false);
      }
    };

    loadSummary();
  }, []);

  const riskLevel = summary?.average_risk_score ?? 0;
  const riskColor = riskLevel >= 70 ? 'text-red-400' : riskLevel >= 40 ? 'text-orange-400' : 'text-yellow-400';

  return (
    <div className="bg-cyber-bg text-white min-h-screen">
      <Navbar />
      <PageLayout title="Security Dashboard" subtitle="Persistent analytics across all scans">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
          {loading ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              {Array.from({ length: 8 }).map((_, idx) => (
                <Card key={idx} className="h-32 animate-pulse bg-cyber-surface/40">
                  <span className="sr-only">loading</span>
                </Card>
              ))}
            </div>
          ) : error ? (
            <Card className="p-8 text-center border-red-500/40">
              <AlertTriangle className="w-8 h-8 mx-auto text-red-400 mb-3" />
              <p className="text-red-300">{error}</p>
              <p className="text-sm text-gray-400 mt-2">Verify backend is running and Phase 4 APIs are available.</p>
            </Card>
          ) : !summary ? (
            <Card className="p-8 text-center">
              <Database className="w-8 h-8 mx-auto text-cyan-400 mb-3" />
              <p className="text-gray-300">No analytics available yet.</p>
            </Card>
          ) : (
            <>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                <Card className="p-5">
                  <div className="text-sm text-gray-400">Total Scans</div>
                  <div className="text-3xl font-bold text-cyan-400">{summary.total_scans}</div>
                </Card>
                <Card className="p-5">
                  <div className="text-sm text-gray-400">Total Vulnerabilities</div>
                  <div className="text-3xl font-bold text-red-400">{summary.total_vulnerabilities}</div>
                </Card>
                <Card className="p-5">
                  <div className="text-sm text-gray-400">Average Risk Score</div>
                  <div className={`text-3xl font-bold ${riskColor}`}>{summary.average_risk_score.toFixed(1)}</div>
                </Card>
                <Card className="p-5">
                  <div className="text-sm text-gray-400">Scans (7 days)</div>
                  <div className="text-3xl font-bold text-purple-400">{summary.scans_last_7_days}</div>
                </Card>
              </div>

              <div className="grid lg:grid-cols-2 gap-6 mb-6">
                <Card className="p-5">
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2"><BarChart3 size={18} /> Severity Distribution</h3>
                  <div className="space-y-2">
                    {Object.entries(summary.severity_distribution).map(([level, count]) => (
                      <div key={level} className="flex justify-between text-sm">
                        <span className="capitalize text-gray-300">{level}</span>
                        <span className="text-white font-semibold">{count}</span>
                      </div>
                    ))}
                  </div>
                </Card>

                <Card className="p-5">
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2"><Activity size={18} /> Remediation Workflow</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between"><span className="text-gray-300">Open</span><span className="text-red-300">{summary.open_findings}</span></div>
                    <div className="flex justify-between"><span className="text-gray-300">Reviewing</span><span className="text-yellow-300">{summary.reviewing_findings}</span></div>
                    <div className="flex justify-between"><span className="text-gray-300">Resolved</span><span className="text-green-300">{summary.resolved_findings}</span></div>
                    <div className="flex justify-between"><span className="text-gray-300">Ignored</span><span className="text-gray-300">{summary.ignored_findings}</span></div>
                  </div>
                </Card>
              </div>

              <div className="grid lg:grid-cols-3 gap-6">
                <Card className="p-5 lg:col-span-2">
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2"><Bug size={18} /> Top CWE IDs</h3>
                  <div className="flex flex-wrap gap-2">
                    {summary.top_cwe_ids.length === 0 ? (
                      <span className="text-sm text-gray-400">No findings yet.</span>
                    ) : (
                      summary.top_cwe_ids.map((cwe) => (
                        <span key={cwe} className="px-3 py-1 rounded-full bg-cyan-900/30 border border-cyan-700 text-cyan-300 text-sm">
                          {cwe}
                        </span>
                      ))
                    )}
                  </div>
                </Card>
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                  <Card className="p-5">
                    <h3 className="text-lg font-semibold mb-3 flex items-center gap-2"><ShieldCheck size={18} /> Insights</h3>
                    <ul className="space-y-2 text-sm text-gray-300">
                      <li>Most scanned language: <span className="text-cyan-300">{summary.most_common_language || 'N/A'}</span></li>
                      <li>Avg findings/scan: <span className="text-cyan-300">{summary.avg_findings_per_scan.toFixed(2)}</span></li>
                      <li>Highest risk score: <span className="text-red-300">{summary.highest_risk_score.toFixed(1)}</span></li>
                      <li>Highest risk scan: <span className="text-cyan-300">{summary.highest_risk_scan_id || 'N/A'}</span></li>
                    </ul>
                  </Card>
                </motion.div>
              </div>

              <div className="grid lg:grid-cols-2 gap-6 mt-6">
                <Card className="p-5">
                  <h3 className="text-lg font-semibold mb-3">Language Distribution</h3>
                  <div className="space-y-2 text-sm">
                    {Object.entries(summary.language_distribution).length === 0 ? (
                      <span className="text-gray-400">No language data available.</span>
                    ) : (
                      Object.entries(summary.language_distribution).map(([lang, count]) => (
                        <div key={lang} className="flex justify-between">
                          <span className="text-gray-300">{lang}</span>
                          <span className="text-cyan-300 font-semibold">{count}</span>
                        </div>
                      ))
                    )}
                  </div>
                </Card>

                <Card className="p-5">
                  <h3 className="text-lg font-semibold mb-3">Top Finding Titles</h3>
                  <div className="space-y-2 text-sm">
                    {summary.top_finding_titles.length === 0 ? (
                      <span className="text-gray-400">No findings yet.</span>
                    ) : (
                      summary.top_finding_titles.map((title) => (
                        <div key={title} className="text-gray-300 border-b border-cyber-border/50 pb-2 last:border-b-0">
                          {title}
                        </div>
                      ))
                    )}
                  </div>
                </Card>
              </div>
            </>
          )}
        </div>
      </PageLayout>
      <Footer />
    </div>
  );
};
