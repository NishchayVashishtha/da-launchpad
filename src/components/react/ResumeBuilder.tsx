import React, { useState, useEffect } from 'react';

interface ProjectEntry {
  title: string;
  tools: string;
  bullets: string[];
}

const BULLET_EXAMPLES = [
  { cat: 'SQL & Database', text: 'Queried 22,000+ UPI transactions in PostgreSQL using CTEs and window functions to isolate bank switch timeout bottlenecks, identifying a 6.1% failure rate.' },
  { cat: 'SQL & Database', text: 'Automated weekly revenue reconciliation across 10,000 orders using SQL views and multi-table joins, reducing reporting discrepancy from 4.2% to under 0.1%.' },
  { cat: 'SQL & Database', text: 'Optimized complex SQL queries using indexing and partitioning, reducing query execution time by 65% on a 5M-row customer events table.' },
  { cat: 'SQL & Database', text: 'Engineered RFM customer segmentation logic in PostgreSQL using NTILE(5) and conditional aggregation, identifying a top 8% VIP tier driving 34% of GMV.' },
  { cat: 'Python & EDA', text: 'Conducted exploratory data analysis (EDA) in Python (pandas, NumPy) on 15,000 deliveries, identifying that heavy rain increased late delivery share from 15% to 53%.' },
  { cat: 'Python & EDA', text: 'Modeled customer satisfaction drop using linear regression in statsmodels, establishing that delivery ratings decline by 0.075 stars per minute of transit delay.' },
  { cat: 'Python & EDA', text: 'Built an automated data validation pipeline in Python with regex and datetime parsing to sanitize 36,000 messy event logs, eliminating 100+ duplicate events.' },
  { cat: 'Power BI & Dashboards', text: 'Designed an interactive 3-page Power BI executive dashboard with 12 custom DAX measures, tracking on-time delivery rates, driver tenure, and regional SLAs.' },
  { cat: 'Power BI & Dashboards', text: 'Modeled star schema data architectures in Power BI Desktop connecting 6 dimension and fact tables with row-level security (RLS) for 5 regional sales managers.' },
  { cat: 'Power BI & Dashboards', text: 'Built dynamic DAX measures for Net Revenue Retention (NRR) and Logo Churn %, enabling product teams to track monthly recurring revenue decay curves.' },
  { cat: 'Statistics & A/B Testing', text: 'Evaluated a 12,000-user checkout free shipping banner A/B test using a two-proportion z-test, proving a statistically significant +1.15% conversion lift (p=0.046).' },
  { cat: 'Statistics & A/B Testing', text: 'Verified experimental integrity by performing chi-square Sample Ratio Mismatch (SRM) tests (p=0.73), confirming unbiased 50/50 traffic randomization.' },
  { cat: 'Business & Retention', text: 'Diagnosed a 62.2% monthly subscriber churn rate, modeling lifetime value (LTV) curves across Basic, Standard, and Premium subscription tiers.' },
  { cat: 'Business & Retention', text: 'Quantified inventory working capital tied up in slow-moving stock, identifying 7.3 months of excess coverage and formulating a Rs 65 Lakhs clearance roadmap.' },
  { cat: 'Business & Retention', text: 'Formulated an automated payment retry dunning strategy that rescued 40% of involuntary payment failures, protecting Rs 38,000 in monthly recurring revenue.' },
];

export default function ResumeBuilder() {
  const [profile, setProfile] = useState({
    fullName: 'Ananya Sharma',
    title: 'Data Analyst | SQL • Python • Power BI',
    email: 'ananya.sharma@example.com',
    phone: '+91 98765 43210',
    location: 'Bengaluru, India',
    linkedin: 'linkedin.com/in/ananya-data',
    github: 'github.com/ananya-analyst',
    portfolio: 'ananya-portfolio.dev',
    summary: 'Detail-oriented Data Analyst with hands-on proficiency in PostgreSQL, Python (pandas, NumPy), Power BI, and statistical modeling. Proven experience analyzing 15,000+ transactional records, designing KPI dashboards, and evaluating controlled A/B experiments to drive revenue optimization.',
    skills: 'SQL (PostgreSQL, SQLite), Python (pandas, NumPy, statsmodels), Power BI, DAX, Excel (XLOOKUP, Pivot Tables), A/B Testing, Data Cleaning, Git',
    education: 'Bachelor of Technology (B.Tech) in Computer Science | CGPA: 8.4/10\nNational Institute of Technology (2020 – 2024)',
    certifications: 'Google Data Analytics Professional Certificate | Coursera (2024)\nMicrosoft Certified: Power BI Data Analyst Associate (PL-300)',
    projects: [
      {
        title: 'Food Delivery Delay Diagnostics & Rating Regression',
        tools: 'SQL, Python (pandas, statsmodels), Power BI',
        bullets: [
          'Analyzed 15,000 food delivery transactions across 5 Indian metro cities to isolate drivers of delivery delays and customer ratings.',
          'Quantified through linear regression that delivery satisfaction drops by 0.075 stars per minute of delay, while food quality ratings remained unaffected.',
          'Built an interactive 3-page Power BI operational dashboard with custom DAX measures, recommending dynamic weather buffers to recover 22% of delayed orders.'
        ]
      },
      {
        title: 'E-Commerce Returns Diagnostics & RFM Segmentation',
        tools: 'PostgreSQL, Python, Power BI, RFM Modeling',
        bullets: [
          'Investigated 10,000 orders across 4,500 customers, diagnosing a 21.7% return rate in Fashion driven by sizing mismatches (64% of return claims).',
          'Uncovered that Cash-on-Delivery (COD) orders suffer an 11.2% cancellation rate and 7.1% RTO rate compared to 3.5% for prepaid transactions.',
          'Constructed an RFM customer segmentation engine in Python, isolating a top 8.4% "Champions" cohort that contributes 34.2% of delivered GMV.'
        ]
      }
    ]
  });

  const [activeTab, setActiveTab] = useState<'edit' | 'bullets' | 'rules'>('edit');

  const updateField = (field: string, val: any) => {
    setProfile((prev) => ({ ...prev, [field]: val }));
  };

  const updateProject = (idx: number, key: string, val: any) => {
    const updated = [...profile.projects];
    updated[idx] = { ...updated[idx], [key]: val };
    setProfile((prev) => ({ ...prev, projects: updated }));
  };

  const updateBullet = (pIdx: number, bIdx: number, val: string) => {
    const updated = [...profile.projects];
    const b = [...updated[pIdx].bullets];
    b[bIdx] = val;
    updated[pIdx].bullets = b;
    setProfile((prev) => ({ ...prev, projects: updated }));
  };

  const addProject = () => {
    setProfile((prev) => ({
      ...prev,
      projects: [
        ...prev.projects,
        {
          title: 'SaaS Subscription Churn & Cohort Retention Analysis',
          tools: 'SQL, Python (pandas, seaborn), Power BI',
          bullets: [
            'Analyzed 5,200 users and 36,000 behavioral telemetry logs to identify free-to-paid trial drop-offs (63.6% trial start vs 36.1% paid conversion).',
            'Constructed a monthly cohort retention matrix in Python, diagnosing a severe 2.7x retention collapse in the March 2024 cohort.',
            'Recommended automated dunning retry workflows to rescue 40% of involuntary payment failures, saving Rs 38,000 in monthly recurring revenue.'
          ]
        }
      ]
    }));
  };

  return (
    <div style={{ display: 'grid', gap: '1.5rem', marginTop: '1rem' }}>
      {/* Navigation Controls */}
      <div style={{ display: 'flex', gap: '0.5rem', borderBottom: '1px solid var(--border)', paddingBottom: '0.75rem', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            type="button"
            className={activeTab === 'edit' ? 'btn btn-primary' : 'btn'}
            onClick={() => setActiveTab('edit')}
          >
            ✏️ Edit Resume
          </button>
          <button
            type="button"
            className={activeTab === 'bullets' ? 'btn btn-primary' : 'btn'}
            onClick={() => setActiveTab('bullets')}
          >
            📋 30 ATS Bullet Bank
          </button>
          <button
            type="button"
            className={activeTab === 'rules' ? 'btn btn-primary' : 'btn'}
            onClick={() => setActiveTab('rules')}
          >
            🛡️ ATS Rules & Checklist
          </button>
        </div>
        <button
          type="button"
          className="btn btn-primary"
          style={{ background: '#16a34a', borderColor: '#16a34a', fontWeight: 600 }}
          onClick={() => window.print()}
        >
          🖨️ Print / Save as PDF
        </button>
      </div>

      {activeTab === 'bullets' && (
        <div className="card" style={{ padding: '1.25rem' }}>
          <h3>30 High-Impact ATS Resume Bullets (Action + Task + Result + Number)</h3>
          <p className="muted" style={{ fontSize: '0.9rem' }}>
            Copy and adapt these proven bullet points into your projects and work experience. Each bullet uses the gold-standard <strong>Action Verb + Technical Method + Quantified Metric</strong> structure.
          </p>
          <div style={{ display: 'grid', gap: '0.8rem', marginTop: '1rem' }}>
            {BULLET_EXAMPLES.map((b, i) => (
              <div key={i} style={{ padding: '0.75rem', background: 'var(--bg-subtle, #f8fafc)', borderRadius: '6px', borderLeft: '3px solid #4f46e5' }}>
                <span className="chip" style={{ fontSize: '0.75rem', marginBottom: '0.3rem', display: 'inline-block' }}>{b.cat}</span>
                <p style={{ margin: 0, fontSize: '0.92rem' }}>{b.text}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'rules' && (
        <div className="card" style={{ padding: '1.25rem' }}>
          <h3>ATS (Applicant Tracking System) Rules & Checklist for Freshers</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
            <div style={{ padding: '1rem', background: 'var(--bg-subtle, #f8fafc)', borderRadius: '6px' }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#16a34a' }}>✅ DO (ATS Best Practices)</h4>
              <ul style={{ paddingLeft: '1.2rem', margin: 0, fontSize: '0.88rem', lineHeight: 1.6 }}>
                <li>Keep to exactly 1 single page for candidates with under 4 years experience.</li>
                <li>Use standard single-column layout without tables, graphics, icons, or text boxes.</li>
                <li>Format every project bullet with numbers (%, Rs, time saved, sample size).</li>
                <li>List exact keywords from job descriptions (PostgreSQL, DAX, pandas, CTEs, Power BI).</li>
                <li>Export as a standard clean PDF with selectable text.</li>
              </ul>
            </div>
            <div style={{ padding: '1rem', background: 'var(--bg-subtle, #f8fafc)', borderRadius: '6px' }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#dc2626' }}>❌ DON'T (Instant Rejection Traps)</h4>
              <ul style={{ paddingLeft: '1.2rem', margin: 0, fontSize: '0.88rem', lineHeight: 1.6 }}>
                <li>Don't use rating skill bars (e.g. "SQL: 4/5 stars") — ATS parsers cannot read them.</li>
                <li>Don't include profile photos, marital status, full home address, or DOB.</li>
                <li>Don't list generic tutorial copies ("Titanic survival", "Iris flowers", "House price prediction").</li>
                <li>Don't use headers or footers for essential contact info (parsers often skip headers).</li>
                <li>Don't write passive duty lists ("Responsible for writing queries").</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Main Form & Live Preview Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem' }}>
        {activeTab === 'edit' && (
          <div className="card" style={{ padding: '1.25rem' }}>
            <h3>Candidate Information</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.8rem', marginTop: '0.8rem' }}>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Full Name</label>
                <input style={{ width: '100%', padding: '0.4rem' }} value={profile.fullName} onChange={(e) => updateField('fullName', e.target.value)} />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Professional Headline</label>
                <input style={{ width: '100%', padding: '0.4rem' }} value={profile.title} onChange={(e) => updateField('title', e.target.value)} />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Email Address</label>
                <input style={{ width: '100%', padding: '0.4rem' }} value={profile.email} onChange={(e) => updateField('email', e.target.value)} />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Phone Number</label>
                <input style={{ width: '100%', padding: '0.4rem' }} value={profile.phone} onChange={(e) => updateField('phone', e.target.value)} />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Location (City, Country)</label>
                <input style={{ width: '100%', padding: '0.4rem' }} value={profile.location} onChange={(e) => updateField('location', e.target.value)} />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>LinkedIn Profile</label>
                <input style={{ width: '100%', padding: '0.4rem' }} value={profile.linkedin} onChange={(e) => updateField('linkedin', e.target.value)} />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>GitHub Profile</label>
                <input style={{ width: '100%', padding: '0.4rem' }} value={profile.github} onChange={(e) => updateField('github', e.target.value)} />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Portfolio Website</label>
                <input style={{ width: '100%', padding: '0.4rem' }} value={profile.portfolio} onChange={(e) => updateField('portfolio', e.target.value)} />
              </div>
            </div>

            <div style={{ marginTop: '0.8rem' }}>
              <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Professional Summary (3–4 lines)</label>
              <textarea rows={3} style={{ width: '100%', padding: '0.4rem' }} value={profile.summary} onChange={(e) => updateField('summary', e.target.value)} />
            </div>

            <div style={{ marginTop: '0.8rem' }}>
              <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Technical Skills</label>
              <input style={{ width: '100%', padding: '0.4rem' }} value={profile.skills} onChange={(e) => updateField('skills', e.target.value)} />
            </div>

            <h4 style={{ marginTop: '1.25rem' }}>Portfolio Projects</h4>
            {profile.projects.map((proj, pIdx) => (
              <div key={pIdx} style={{ padding: '0.8rem', background: 'var(--bg-subtle, #f8fafc)', borderRadius: '6px', marginBottom: '0.8rem' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <input style={{ padding: '0.4rem', fontWeight: 600 }} value={proj.title} onChange={(e) => updateProject(pIdx, 'title', e.target.value)} placeholder="Project Title" />
                  <input style={{ padding: '0.4rem' }} value={proj.tools} onChange={(e) => updateProject(pIdx, 'tools', e.target.value)} placeholder="Tools Used" />
                </div>
                {proj.bullets.map((b, bIdx) => (
                  <div key={bIdx} style={{ marginBottom: '0.3rem' }}>
                    <input style={{ width: '100%', padding: '0.35rem', fontSize: '0.88rem' }} value={b} onChange={(e) => updateBullet(pIdx, bIdx, e.target.value)} placeholder={`Bullet ${bIdx + 1}`} />
                  </div>
                ))}
              </div>
            ))}
            {profile.projects.length < 3 && (
              <button type="button" className="btn" onClick={addProject}>+ Add 3rd Project</button>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem', marginTop: '1rem' }}>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Education</label>
                <textarea rows={2} style={{ width: '100%', padding: '0.4rem', fontSize: '0.88rem' }} value={profile.education} onChange={(e) => updateField('education', e.target.value)} />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>Certifications</label>
                <textarea rows={2} style={{ width: '100%', padding: '0.4rem', fontSize: '0.88rem' }} value={profile.certifications} onChange={(e) => updateField('certifications', e.target.value)} />
              </div>
            </div>
          </div>
        )}

        {/* Live Resume Sheet (Print Ready) */}
        <div
          id="resume-sheet"
          style={{
            background: '#ffffff',
            color: '#0f172a',
            padding: '2.5rem',
            borderRadius: '4px',
            boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            maxWidth: '850px',
            margin: '0 auto',
            border: '1px solid #e2e8f0'
          }}
        >
          {/* Header */}
          <div style={{ textAlign: 'center', borderBottom: '2px solid #0f172a', paddingBottom: '0.8rem', marginBottom: '1rem' }}>
            <h1 style={{ margin: '0 0 0.2rem 0', fontSize: '1.8rem', fontWeight: 700, letterSpacing: '-0.02em', color: '#0f172a' }}>{profile.fullName}</h1>
            <p style={{ margin: '0 0 0.4rem 0', fontSize: '0.95rem', fontWeight: 600, color: '#334155' }}>{profile.title}</p>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '0.8rem', flexWrap: 'wrap', fontSize: '0.82rem', color: '#475569' }}>
              <span>📍 {profile.location}</span>
              <span>✉️ {profile.email}</span>
              <span>📱 {profile.phone}</span>
              <span>🔗 {profile.linkedin}</span>
              <span>🐙 {profile.github}</span>
            </div>
          </div>

          {/* Professional Summary */}
          <div style={{ marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '0.95rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', margin: '0 0 0.3rem 0', borderBottom: '1px solid #cbd5e1', paddingBottom: '0.2rem' }}>
              Professional Summary
            </h3>
            <p style={{ margin: 0, fontSize: '0.88rem', lineHeight: 1.5, color: '#1e293b' }}>
              {profile.summary}
            </p>
          </div>

          {/* Technical Skills */}
          <div style={{ marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '0.95rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', margin: '0 0 0.3rem 0', borderBottom: '1px solid #cbd5e1', paddingBottom: '0.2rem' }}>
              Technical Skills
            </h3>
            <p style={{ margin: 0, fontSize: '0.88rem', lineHeight: 1.5, color: '#1e293b' }}>
              <strong>Core Competencies:</strong> {profile.skills}
            </p>
          </div>

          {/* Projects */}
          <div style={{ marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '0.95rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', margin: '0 0 0.4rem 0', borderBottom: '1px solid #cbd5e1', paddingBottom: '0.2rem' }}>
              Portfolio Projects
            </h3>
            {profile.projects.map((proj, idx) => (
              <div key={idx} style={{ marginBottom: '0.8rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '0.2rem' }}>
                  <span style={{ fontSize: '0.92rem', fontWeight: 700, color: '#0f172a' }}>{proj.title}</span>
                  <span style={{ fontSize: '0.8rem', fontStyle: 'italic', color: '#475569' }}>{proj.tools}</span>
                </div>
                <ul style={{ margin: 0, paddingLeft: '1.2rem', fontSize: '0.86rem', lineHeight: 1.45, color: '#1e293b' }}>
                  {proj.bullets.map((b, bIdx) => (
                    <li key={bIdx} style={{ marginBottom: '0.15rem' }}>{b}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Education & Certifications */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '0.5rem' }}>
            <div>
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', margin: '0 0 0.3rem 0', borderBottom: '1px solid #cbd5e1', paddingBottom: '0.2rem' }}>
                Education
              </h3>
              <p style={{ margin: 0, fontSize: '0.84rem', lineHeight: 1.45, whiteSpace: 'pre-line', color: '#1e293b' }}>
                {profile.education}
              </p>
            </div>
            <div>
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', margin: '0 0 0.3rem 0', borderBottom: '1px solid #cbd5e1', paddingBottom: '0.2rem' }}>
                Certifications
              </h3>
              <p style={{ margin: 0, fontSize: '0.84rem', lineHeight: 1.45, whiteSpace: 'pre-line', color: '#1e293b' }}>
                {profile.certifications}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
