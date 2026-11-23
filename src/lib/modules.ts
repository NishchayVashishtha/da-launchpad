export const MODULES = [
  { slug: 'start-here', title: 'Start Here', blurb: 'Role, job market, 12-week plan, study method and tool setup.' },
  { slug: 'excel', title: 'Excel', blurb: 'Clean, analyse and present data in Excel.' },
  { slug: 'sql', title: 'SQL', blurb: 'The most important skill. From SELECT to window functions and interview patterns.' },
  { slug: 'power-bi', title: 'Power BI', blurb: 'Data modelling, DAX and dashboards.' },
  { slug: 'python', title: 'Python', blurb: 'pandas, NumPy, EDA and visualisation.' },
  { slug: 'statistics', title: 'Statistics', blurb: 'Statistics, probability and A/B testing for analysts.' },
  { slug: 'business', title: 'Business Thinking', blurb: 'KPIs, metrics, root cause analysis and case studies.' },
  { slug: 'interview', title: 'Interview Prep', blurb: 'Every interview round in one place.' },
  { slug: 'projects', title: 'Projects', blurb: 'Portfolio-grade projects with full build guides.' },
  { slug: 'job-search', title: 'Job Search', blurb: 'Resume, LinkedIn, applications and offers.' },
  { slug: 'cheat-sheets', title: 'Cheat Sheets', blurb: 'Printable one-pagers and glossary.' },
] as const;

export type ModuleSlug = (typeof MODULES)[number]['slug'];
export const MODULE_SLUGS = MODULES.map((m) => m.slug) as unknown as [ModuleSlug, ...ModuleSlug[]];
export const moduleTitle = (slug: string) => MODULES.find((m) => m.slug === slug)?.title ?? slug;
