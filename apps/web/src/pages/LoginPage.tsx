import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { KeyRound, Shield, UserCog, UserSearch } from 'lucide-react';

import { Card, Footer, Navbar, PageLayout } from '@/components';
import { DemoRole, defaultKeyForRole, setAuth } from '@/utils/auth';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState<DemoRole>('analyst');
  const [apiKey, setApiKey] = useState(defaultKeyForRole('analyst'));

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    setAuth(role, apiKey);
    if (role === 'viewer') {
      navigate('/dashboard');
    } else {
      navigate('/analyze');
    }
  };

  const roles: Array<{ value: DemoRole; icon: React.ReactNode; description: string }> = [
    { value: 'admin', icon: <UserCog size={16} />, description: 'Full platform control' },
    { value: 'analyst', icon: <Shield size={16} />, description: 'Analyze and triage findings' },
    { value: 'viewer', icon: <UserSearch size={16} />, description: 'Read-only dashboard/history access' },
  ];

  return (
    <div className="bg-cyber-bg text-white min-h-screen">
      <Navbar />
      <PageLayout title="Demo Access" subtitle="Select a role for faculty-demo workflows">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
          <Card className="p-8">
            <form onSubmit={submit} className="space-y-6">
              <div>
                <label className="text-sm text-gray-300 mb-2 block">Role</label>
                <div className="grid md:grid-cols-3 gap-3">
                  {roles.map((r) => (
                    <button
                      key={r.value}
                      type="button"
                      onClick={() => {
                        setRole(r.value);
                        setApiKey(defaultKeyForRole(r.value));
                      }}
                      className={`p-3 border rounded-lg text-left ${role === r.value ? 'border-cyan-400 bg-cyan-900/20' : 'border-cyber-border bg-cyber-surface/40'}`}
                    >
                      <div className="flex items-center gap-2 mb-1">{r.icon}<span className="capitalize font-semibold">{r.value}</span></div>
                      <div className="text-xs text-gray-400">{r.description}</div>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm text-gray-300 mb-2 block">API Key</label>
                <div className="relative">
                  <KeyRound size={14} className="absolute left-3 top-3 text-gray-500" />
                  <input
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    className="w-full pl-9 pr-3 py-2 bg-cyber-surface border border-cyber-border rounded"
                    placeholder="Enter API key"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <p className="text-xs text-gray-400">Tip: default keys auto-fill per selected role for demo use.</p>
                <button type="submit" className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded font-semibold">Continue</button>
              </div>
            </form>
          </Card>
        </div>
      </PageLayout>
      <Footer />
    </div>
  );
};
