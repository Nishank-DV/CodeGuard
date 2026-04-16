import React, { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { Download, Filter, History, Search, Trash2 } from 'lucide-react';
import { Card, Footer, Navbar, PageLayout, SeverityBadge } from '@/components';
import { apiFetch, readApiError, readApiJson, reportDownloadUrl } from '@/utils/api';

type FindingStatus = 'open' | 'reviewing' | 'resolved' | 'ignored';

interface ScanListItem {
  id: string;
  filename?: string | null;
  language: string;
  scanned_at: string;
  duration_ms: number;
  total_issues: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  info_count: number;
  risk_score: number;
  finding_summary: string;
}

interface Vulnerability {
  id: string;
  title: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  cwe_id: string;
  line_number: number;
  confidence: number;
  status: FindingStatus;
  remediation_notes?: string | null;
  fix_suggestion?: string;
  detailed_remediation?: string;
}

interface ScanDetail {
  id: string;
  filename?: string | null;
  language: string;
  scanned_at: string;
  risk_score: number;
  total_issues: number;
  findings: Vulnerability[];
}

export const ScanHistoryPage: React.FC = () => {
  const [items, setItems] = useState<ScanListItem[]>([]);
  const [selected, setSelected] = useState<ScanDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [languageFilter, setLanguageFilter] = useState('all');
  const [query, setQuery] = useState('');

  const loadScans = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ page: '1', page_size: '50', sort_by: 'scanned_at', sort_dir: 'desc' });
      if (languageFilter !== 'all') params.set('language', languageFilter);
      const response = await apiFetch(`/scans?${params.toString()}`);
      if (!response.ok) throw new Error(await readApiError(response, 'Failed to load scans'));
      const data = await readApiJson<{ items?: ScanListItem[] }>(response, 'Scan history API returned an empty response');
      setItems(data.items || []);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load scan history';
      setError(message);
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadScans();
  }, [languageFilter]);

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    if (!q) return items;
    return items.filter((item) =>
      item.id.toLowerCase().includes(q) ||
      item.language.toLowerCase().includes(q) ||
      (item.filename || '').toLowerCase().includes(q) ||
      item.finding_summary.toLowerCase().includes(q)
    );
  }, [items, query]);

  const loadDetail = async (scanId: string) => {
    const response = await apiFetch(`/scans/${scanId}`);
    if (!response.ok) {
      setError(await readApiError(response, 'Failed to load scan details'));
      return;
    }
    const data = await readApiJson<ScanDetail>(response, 'Scan detail API returned an empty response');
    setSelected(data);
  };

  const downloadReport = (scanId: string, format: 'json' | 'md') => {
    window.open(reportDownloadUrl(scanId, format), '_blank');
  };

  const deleteScan = async (scanId: string) => {
    const confirmed = window.confirm('Delete this scan history entry?');
    if (!confirmed) return;
    await apiFetch(`/scans/${scanId}`, {
      method: 'DELETE',
    });
    if (selected?.id === scanId) setSelected(null);
    await loadScans();
  };

  const updateStatus = async (findingId: string, status: FindingStatus, remediation_notes?: string) => {
    if (!selected) return;
    const response = await apiFetch(`/scans/${selected.id}/findings/${findingId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, remediation_notes }),
    });
    if (response.ok) await loadDetail(selected.id);
  };

  return (
    <div className="bg-cyber-bg text-white min-h-screen">
      <Navbar />
      <PageLayout title="Scan History" subtitle="Persistent scans, reports, and remediation tracking">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
          <Card className="p-4 mb-6">
            <div className="flex flex-col md:flex-row gap-3 md:items-center md:justify-between">
              <div className="flex items-center gap-2 text-gray-300"><Filter size={16} /> Filters</div>
              <div className="flex gap-2">
                <div className="relative">
                  <Search className="w-4 h-4 absolute left-2 top-2.5 text-gray-500" />
                  <input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search scans..."
                    className="pl-8 pr-3 py-2 bg-cyber-surface border border-cyber-border rounded text-sm"
                  />
                </div>
                <select
                  value={languageFilter}
                  onChange={(e) => setLanguageFilter(e.target.value)}
                  className="px-3 py-2 bg-cyber-surface border border-cyber-border rounded text-sm"
                >
                  <option value="all">All Languages</option>
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                </select>
              </div>
            </div>
          </Card>

          <div className="grid lg:grid-cols-2 gap-6">
            <Card className="p-4">
              <h2 className="font-semibold mb-4 flex items-center gap-2"><History size={16} /> Recent Scans</h2>
              {loading ? (
                <p className="text-gray-400">Loading scan history...</p>
              ) : error ? (
                <p className="text-red-300">{error}</p>
              ) : filtered.length === 0 ? (
                <p className="text-gray-400">No scans found.</p>
              ) : (
                <div className="space-y-2 max-h-[600px] overflow-y-auto">
                  {filtered.map((item) => (
                    <motion.div
                      key={item.id}
                      onClick={() => loadDetail(item.id)}
                      className="p-3 rounded border border-cyber-border bg-cyber-surface/40 hover:border-cyan-500/50 cursor-pointer"
                    >
                      <div className="flex justify-between items-center mb-1">
                        <div className="font-semibold text-sm">{item.filename || item.id.slice(0, 8)}</div>
                        <div className="text-xs text-gray-400">{new Date(item.scanned_at).toLocaleString()}</div>
                      </div>
                      <div className="text-xs text-gray-400 mb-1">{item.language} • Risk {item.risk_score.toFixed(1)} • {item.total_issues} issues</div>
                      <div className="text-xs text-cyan-300 truncate">{item.finding_summary}</div>
                    </motion.div>
                  ))}
                </div>
              )}
            </Card>

            <Card className="p-4">
              {!selected ? (
                <p className="text-gray-400">Select a scan to inspect findings and update remediation status.</p>
              ) : (
                <>
                  <div className="flex flex-wrap justify-between items-center gap-2 mb-3">
                    <div>
                      <h2 className="font-semibold">Scan Details</h2>
                      <p className="text-xs text-gray-400">{selected.filename || selected.id}</p>
                    </div>
                    <div className="flex gap-2">
                      <button className="px-2 py-1 text-xs bg-cyan-700 rounded" onClick={() => downloadReport(selected.id, 'json')}><Download className="w-3 h-3 inline" /> JSON</button>
                      <button className="px-2 py-1 text-xs bg-purple-700 rounded" onClick={() => downloadReport(selected.id, 'md')}><Download className="w-3 h-3 inline" /> Markdown</button>
                      <button className="px-2 py-1 text-xs bg-red-700 rounded" onClick={() => deleteScan(selected.id)}><Trash2 className="w-3 h-3 inline" /> Delete</button>
                    </div>
                  </div>

                  <div className="text-xs text-gray-400 mb-3">{selected.language} • Risk {selected.risk_score.toFixed(1)} • {selected.total_issues} findings</div>

                  <div className="space-y-3 max-h-[560px] overflow-y-auto pr-1">
                    {selected.findings.map((f) => (
                      <div key={f.id} className="p-3 rounded border border-cyber-border bg-cyber-surface/30">
                        <div className="flex justify-between gap-2 items-start mb-1">
                          <div>
                            <div className="text-sm font-semibold">{f.title}</div>
                            <div className="text-xs text-gray-400">{f.cwe_id} • L{f.line_number}</div>
                          </div>
                          <SeverityBadge severity={f.severity}>{f.severity}</SeverityBadge>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2">
                          <select
                            value={f.status || 'open'}
                            onChange={(e) => updateStatus(f.id, e.target.value as FindingStatus, f.remediation_notes || undefined)}
                            className="px-2 py-1 text-xs bg-cyber-surface border border-cyber-border rounded"
                          >
                            <option value="open">Open</option>
                            <option value="reviewing">Reviewing</option>
                            <option value="resolved">Resolved</option>
                            <option value="ignored">Ignored</option>
                          </select>
                          <button
                            className="px-2 py-1 text-xs bg-cyan-800 rounded"
                            onClick={() => {
                              const notes = window.prompt('Enter remediation notes', f.remediation_notes || '');
                              if (notes !== null) updateStatus(f.id, f.status || 'open', notes);
                            }}
                          >
                            Notes
                          </button>
                        </div>

                        {f.remediation_notes && <p className="text-xs text-gray-300 mt-2">Note: {f.remediation_notes}</p>}
                      </div>
                    ))}
                  </div>
                </>
              )}
            </Card>
          </div>
        </div>
      </PageLayout>
      <Footer />
    </div>
  );
};
