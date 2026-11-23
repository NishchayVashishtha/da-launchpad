import { marked } from 'marked';
marked.setOptions({ gfm: true, breaks: false });
/** Renders trusted markdown (content from our own collections). */
export default function Md({ children, inline = false, className = '' }: { children: string; inline?: boolean; className?: string }) {
  const html = inline ? (marked.parseInline(children ?? '') as string) : (marked.parse(children ?? '') as string);
  return <div className={`prose prose-sm max-w-none ${className}`} dangerouslySetInnerHTML={{ __html: html }} />;
}
