export type Column = { name: string; type: string; description: string; nullable?: boolean; example?: string | number };
export type Table = { name: string; rowCount: number; description: string; columns: Column[] };
export type Dataset = {
  id: string; title: string; description: string; tables: Table[];
  relationships: { from: string; to: string; type: string }[]; qualityIssues: string[]; er: string;
  downloads: { sqlite: string; csv: string[] };
};
// datasets.json is written by the data-generator agent. Missing file => empty list (pages stay robust).
// datasets.test.json is a tiny stand-in used only in dev or when USE_TEST_DATASETS=1.
const real = import.meta.glob('../data/datasets.json', { eager: true, import: 'default' }) as Record<string, Dataset[]>;
const test = import.meta.glob('../data/datasets.test.json', { eager: true, import: 'default' }) as Record<string, Dataset[]>;
const useTest = import.meta.env.DEV || process.env.USE_TEST_DATASETS === '1';
export const datasets: Dataset[] = Object.values(real)[0] ?? (useTest ? Object.values(test)[0] ?? [] : []);
