import React, { useState, useEffect } from 'react';

export interface Application {
  id: string;
  company: string;
  role: string;
  location: string;
  salaryLpa: string;
  appliedDate: string;
  status: 'Applied' | 'Screening' | 'Technical Test' | 'Interview' | 'Offer' | 'Rejected';
  contact: string;
  followUpDate: string;
  notes: string;
}

const STORAGE_KEY = 'dal-app-tracker';

const INITIAL_APPS: Application[] = [
  {
    id: 'app-1',
    company: 'PhonePe',
    role: 'Associate Data Analyst',
    location: 'Bengaluru (Hybrid)',
    salaryLpa: '8.5 - 10.5',
    appliedDate: '2024-10-15',
    status: 'Interview',
    contact: 'Pooja Nair (Senior Tech Recruiter)',
    followUpDate: '2024-10-28',
    notes: 'Completed SQL screening test with 100% score; round 2 case discussion on payment rail failure rates.'
  },
  {
    id: 'app-2',
    company: 'Swiggy',
    role: 'Operations Analyst - Logistics',
    location: 'Bengaluru / Remote',
    salaryLpa: '7.5 - 9.0',
    appliedDate: '2024-10-18',
    status: 'Technical Test',
    contact: 'Career Portal (#REQ-8842)',
    followUpDate: '2024-10-25',
    notes: 'Take-home assignment sent: analyze late delivery factors and partner cancellation rates in Python.'
  },
  {
    id: 'app-3',
    company: 'Zepto',
    role: 'Junior BI Analyst',
    location: 'Mumbai (In-office)',
    salaryLpa: '6.5 - 8.0',
    appliedDate: '2024-10-20',
    status: 'Applied',
    contact: 'Employee Referral via Amit Roy',
    followUpDate: '2024-10-27',
    notes: 'Referred directly by alumni senior analyst; tailored resume to highlight SQL window functions and Power BI DAX.'
  },
  {
    id: 'app-4',
    company: 'CRED',
    role: 'Risk Analytics Intern / Trainee',
    location: 'Bengaluru',
    salaryLpa: '6.0 - 7.5',
    appliedDate: '2024-10-10',
    status: 'Screening',
    contact: 'Karan Mehta (Talent Acquisition)',
    followUpDate: '2024-10-24',
    notes: 'Recruiter phone screening passed; discussed my UPI anomaly detection project.'
  }
];

export default function ApplicationTracker() {
  const [apps, setApps] = useState<Application[]>([]);
  const [filter, setFilter] = useState<string>('All');
  const [search, setSearch] = useState<string>('');
  const [showAddForm, setShowAddForm] = useState<boolean>(false);

  const [newApp, setNewApp] = useState<Omit<Application, 'id'>>({
    company: '',
    role: 'Junior Data Analyst',
    location: 'Bengaluru',
    salaryLpa: '',
    appliedDate: new Date().toISOString().split('T')[0],
    status: 'Applied',
    contact: '',
    followUpDate: '',
    notes: ''
  });

  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        setApps(JSON.parse(saved));
      } else {
        setApps(INITIAL_APPS);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(INITIAL_APPS));
      }
    } catch {
      setApps(INITIAL_APPS);
    }
  }, []);

  const saveApps = (updated: Application[]) => {
    setApps(updated);
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    } catch (e) {
      console.error(e);
    }
  };

  const handleAdd = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newApp.company.trim()) return;
    const item: Application = {
      ...newApp,
      id: 'app-' + Date.now()
    };
    const updated = [item, ...apps];
    saveApps(updated);
    setShowAddForm(false);
    setNewApp({
      company: '',
      role: 'Junior Data Analyst',
      location: 'Bengaluru',
      salaryLpa: '',
      appliedDate: new Date().toISOString().split('T')[0],
      status: 'Applied',
      contact: '',
      followUpDate: '',
      notes: ''
    });
  };

  const updateStatus = (id: string, newStatus: Application['status']) => {
    const updated = apps.map((a) => (a.id === id ? { ...a, status: newStatus } : a));
    saveApps(updated);
  };

  const deleteApp = (id: string) => {
    if (confirm('Delete this job application record?')) {
      const updated = apps.filter((a) => a.id !== id);
      saveApps(updated);
    }
  };

  const exportCsv = () => {
    const headers = ['ID', 'Company', 'Role', 'Location', 'Salary (LPA)', 'Applied Date', 'Status', 'Contact', 'Follow-up Date', 'Notes'];
    const rows = apps.map((a) => [
      a.id,
      `"${a.company.replace(/"/g, '""')}"`,
      `"${a.role.replace(/"/g, '""')}"`,
      `"${a.location.replace(/"/g, '""')}"`,
      `"${a.salaryLpa}"`,
      a.appliedDate,
      a.status,
      `"${a.contact.replace(/"/g, '""')}"`,
      a.followUpDate,
      `"${a.notes.replace(/"/g, '""')}"`
    ]);
    const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `job_applications_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const filteredApps = apps.filter((a) => {
    const matchesFilter = filter === 'All' || a.status === filter;
    const matchesSearch =
      a.company.toLowerCase().includes(search.toLowerCase()) ||
      a.role.toLowerCase().includes(search.toLowerCase()) ||
      a.notes.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const counts = {
    total: apps.length,
    active: apps.filter((a) => ['Applied', 'Screening', 'Technical Test', 'Interview'].includes(a.status)).length,
    interviewing: apps.filter((a) => a.status === 'Interview').length,
    offers: apps.filter((a) => a.status === 'Offer').length,
    rejected: apps.filter((a) => a.status === 'Rejected').length
  };

  return (
    <div style={{ display: 'grid', gap: '1.25rem', marginTop: '1rem' }}>
      {/* Metric Cards Header */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '0.8rem' }}>
        <div className="card" style={{ padding: '0.8rem', textAlign: 'center' }}>
          <span className="muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>TOTAL APPLIED</span>
          <p style={{ margin: '0.3rem 0 0', fontSize: '1.6rem', fontWeight: 700 }}>{counts.total}</p>
        </div>
        <div className="card" style={{ padding: '0.8rem', textAlign: 'center', borderTop: '3px solid #3b82f6' }}>
          <span className="muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>IN PIPELINE</span>
          <p style={{ margin: '0.3rem 0 0', fontSize: '1.6rem', fontWeight: 700, color: '#3b82f6' }}>{counts.active}</p>
        </div>
        <div className="card" style={{ padding: '0.8rem', textAlign: 'center', borderTop: '3px solid #8b5cf6' }}>
          <span className="muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>INTERVIEWS</span>
          <p style={{ margin: '0.3rem 0 0', fontSize: '1.6rem', fontWeight: 700, color: '#8b5cf6' }}>{counts.interviewing}</p>
        </div>
        <div className="card" style={{ padding: '0.8rem', textAlign: 'center', borderTop: '3px solid #16a34a' }}>
          <span className="muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>OFFERS</span>
          <p style={{ margin: '0.3rem 0 0', fontSize: '1.6rem', fontWeight: 700, color: '#16a34a' }}>{counts.offers}</p>
        </div>
      </div>

      {/* Control Toolbar */}
      <div className="card" style={{ padding: '1rem', display: 'flex', gap: '0.8rem', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <input
            type="text"
            placeholder="Search company or role..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ padding: '0.4rem 0.6rem', fontSize: '0.88rem', borderRadius: '4px', border: '1px solid var(--border)' }}
          />
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            style={{ padding: '0.4rem 0.6rem', fontSize: '0.88rem', borderRadius: '4px', border: '1px solid var(--border)' }}
          >
            <option value="All">All Statuses</option>
            <option value="Applied">Applied</option>
            <option value="Screening">Screening</option>
            <option value="Technical Test">Technical Test</option>
            <option value="Interview">Interview</option>
            <option value="Offer">Offer</option>
            <option value="Rejected">Rejected</option>
          </select>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button type="button" className="btn btn-primary" onClick={() => setShowAddForm(!showAddForm)}>
            {showAddForm ? 'Close Form' : '+ Add Application'}
          </button>
          <button type="button" className="btn" onClick={exportCsv}>
            📥 Export CSV
          </button>
        </div>
      </div>

      {/* Add New Application Form */}
      {showAddForm && (
        <form onSubmit={handleAdd} className="card" style={{ padding: '1.25rem', display: 'grid', gap: '0.8rem', background: 'var(--bg-subtle, #f8fafc)' }}>
          <h4 style={{ margin: '0 0 0.5rem 0' }}>Log New Job Application</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.8rem' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600 }}>Company Name *</label>
              <input required style={{ width: '100%', padding: '0.4rem' }} value={newApp.company} onChange={(e) => setNewApp({ ...newApp, company: e.target.value })} placeholder="e.g. Razorpay" />
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600 }}>Job Role</label>
              <input style={{ width: '100%', padding: '0.4rem' }} value={newApp.role} onChange={(e) => setNewApp({ ...newApp, role: e.target.value })} />
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600 }}>Location & Mode</label>
              <input style={{ width: '100%', padding: '0.4rem' }} value={newApp.location} onChange={(e) => setNewApp({ ...newApp, location: e.target.value })} placeholder="Bengaluru (Hybrid)" />
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600 }}>Salary Range (LPA)</label>
              <input style={{ width: '100%', padding: '0.4rem' }} value={newApp.salaryLpa} onChange={(e) => setNewApp({ ...newApp, salaryLpa: e.target.value })} placeholder="e.g. 7.0 - 9.5" />
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600 }}>Applied Date</label>
              <input type="date" style={{ width: '100%', padding: '0.4rem' }} value={newApp.appliedDate} onChange={(e) => setNewApp({ ...newApp, appliedDate: e.target.value })} />
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600 }}>Status</label>
              <select style={{ width: '100%', padding: '0.4rem' }} value={newApp.status} onChange={(e) => setNewApp({ ...newApp, status: e.target.value as any })}>
                <option value="Applied">Applied</option>
                <option value="Screening">Screening</option>
                <option value="Technical Test">Technical Test</option>
                <option value="Interview">Interview</option>
                <option value="Offer">Offer</option>
                <option value="Rejected">Rejected</option>
              </select>
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600 }}>Recruiter / Contact</label>
              <input style={{ width: '100%', padding: '0.4rem' }} value={newApp.contact} onChange={(e) => setNewApp({ ...newApp, contact: e.target.value })} placeholder="Name / LinkedIn" />
            </div>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 600 }}>Follow-up Date</label>
              <input type="date" style={{ width: '100%', padding: '0.4rem' }} value={newApp.followUpDate} onChange={(e) => setNewApp({ ...newApp, followUpDate: e.target.value })} />
            </div>
          </div>
          <div>
            <label style={{ fontSize: '0.82rem', fontWeight: 600 }}>Interview / Application Notes</label>
            <textarea rows={2} style={{ width: '100%', padding: '0.4rem' }} value={newApp.notes} onChange={(e) => setNewApp({ ...newApp, notes: e.target.value })} placeholder="Referral details, test links, prep notes..." />
          </div>
          <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
            <button type="button" className="btn" onClick={() => setShowAddForm(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary">Save Application</button>
          </div>
        </form>
      )}

      {/* Applications Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--border)', textAlign: 'left', background: 'var(--bg-subtle, #f8fafc)' }}>
              <th style={{ padding: '0.6rem' }}>Company</th>
              <th style={{ padding: '0.6rem' }}>Role</th>
              <th style={{ padding: '0.6rem' }}>Applied</th>
              <th style={{ padding: '0.6rem' }}>Status</th>
              <th style={{ padding: '0.6rem' }}>Next Step / Notes</th>
              <th style={{ padding: '0.6rem', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredApps.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ padding: '2rem', textAlign: 'center' }} className="muted">
                  No job applications found matching your criteria.
                </td>
              </tr>
            ) : (
              filteredApps.map((a) => (
                <tr key={a.id} style={{ borderBottom: '1px solid var(--border)' }}>
                  <td style={{ padding: '0.6rem' }}>
                    <strong>{a.company}</strong>
                    <div className="muted" style={{ fontSize: '0.78rem' }}>{a.location}</div>
                  </td>
                  <td style={{ padding: '0.6rem' }}>
                    {a.role}
                    {a.salaryLpa && <div className="muted" style={{ fontSize: '0.78rem' }}>₹{a.salaryLpa} LPA</div>}
                  </td>
                  <td style={{ padding: '0.6rem', whiteSpace: 'nowrap' }}>
                    {a.appliedDate}
                  </td>
                  <td style={{ padding: '0.6rem' }}>
                    <select
                      value={a.status}
                      onChange={(e) => updateStatus(a.id, e.target.value as any)}
                      style={{
                        padding: '0.25rem 0.5rem',
                        fontSize: '0.78rem',
                        fontWeight: 600,
                        borderRadius: '4px',
                        border: '1px solid var(--border)',
                        background:
                          a.status === 'Offer' ? '#dcfce7' :
                          a.status === 'Interview' ? '#f3e8ff' :
                          a.status === 'Technical Test' ? '#dbeafe' :
                          a.status === 'Rejected' ? '#fee2e2' : 'inherit'
                      }}
                    >
                      <option value="Applied">Applied</option>
                      <option value="Screening">Screening</option>
                      <option value="Technical Test">Technical Test</option>
                      <option value="Interview">Interview</option>
                      <option value="Offer">Offer</option>
                      <option value="Rejected">Rejected</option>
                    </select>
                  </td>
                  <td style={{ padding: '0.6rem', maxWidth: '280px' }}>
                    <div style={{ fontSize: '0.84rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={a.notes}>
                      {a.notes || '—'}
                    </div>
                    {a.followUpDate && (
                      <div className="muted" style={{ fontSize: '0.76rem', color: '#4f46e5' }}>
                        📅 Follow-up: {a.followUpDate}
                      </div>
                    )}
                  </td>
                  <td style={{ padding: '0.6rem', textAlign: 'right', whiteSpace: 'nowrap' }}>
                    <button
                      type="button"
                      onClick={() => deleteApp(a.id)}
                      style={{ background: 'transparent', border: 'none', color: '#dc2626', cursor: 'pointer', padding: '0.2rem' }}
                      title="Delete entry"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
