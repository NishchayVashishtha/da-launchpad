import { getCollection } from 'astro:content';
// Full practice data (including solutions), fetched lazily by the Practice hub and Bookmarks pages.
export async function GET() {
  const all = await getCollection('practice');
  const map = Object.fromEntries(all.map((e) => [e.data.id, e.data]));
  return new Response(JSON.stringify(map), { headers: { 'Content-Type': 'application/json' } });
}
