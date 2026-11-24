import { getCollection } from 'astro:content';

/** Interview questions (samples excluded), plain data for islands. */
export async function getInterviewItems() {
  return (await getCollection('interview')).map((e) => e.data).filter((d) => !d.id.startsWith('sample-'));
}
export async function getMcqItems(module: string) {
  return (await getCollection('mcq')).map((e) => e.data).filter((d) => d.module === module && !d.id.startsWith('sample-'));
}
export const catLabel = (c: string) => c.replace(/-/g, ' ').replace(/\b\w/g, (m) => m.toUpperCase());
