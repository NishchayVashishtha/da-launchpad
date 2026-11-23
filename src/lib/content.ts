import { getCollection, type CollectionEntry } from 'astro:content';
import { MODULES, MODULE_SLUGS } from './modules';

/** Drafts are visible only in dev or when INCLUDE_DRAFTS=1 (for testing). They never appear in nav. */
export const SHOW_DRAFTS = import.meta.env.DEV || process.env.INCLUDE_DRAFTS === '1';

export const lessonSlug = (id: string) => id.split('/').pop()!.replace(/^\d+-/, '');

export type LessonItem = { entry: CollectionEntry<'lessons'>; module: string; slug: string; id: string; href: string; title: string; order: number };

export async function getLessons(opts: { includeDrafts?: boolean } = {}): Promise<LessonItem[]> {
  const all = await getCollection('lessons');
  const withDrafts = opts.includeDrafts ?? SHOW_DRAFTS;
  return all
    .filter((e) => withDrafts || !e.data.draft)
    .map((entry) => {
      const slug = lessonSlug(entry.id);
      return { entry, module: entry.data.module, slug, id: `${entry.data.module}/${slug}`, href: `/${entry.data.module}/${slug}/`, title: entry.data.title, order: entry.data.order };
    })
    .sort((a, b) => MODULE_SLUGS.indexOf(a.module as any) - MODULE_SLUGS.indexOf(b.module as any) || a.order - b.order);
}

export type NavModule = { slug: string; title: string; lessons: { id: string; title: string; href: string }[] };
/** Sidebar data: visible (non-draft) lessons per module. */
export async function getNav(): Promise<NavModule[]> {
  const lessons = await getLessons({ includeDrafts: false });
  return MODULES.map((m) => ({
    slug: m.slug, title: m.title,
    lessons: lessons.filter((l) => l.module === m.slug).map((l) => ({ id: l.id, title: l.title, href: l.href })),
  }));
}

export async function getPractice() {
  const all = await getCollection('practice');
  return all.map((e) => e.data);
}

export const readingMinutes = (body: string | undefined) => Math.max(1, Math.round((body?.split(/\s+/).length ?? 0) / 200));
