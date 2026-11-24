// Per-file MDX compile gate.
// Usage: node scripts/check-mdx.mjs [file ...]   (default: all src/content/**/*.mdx)
// Compiles with satteri's mdxToJs, the compiler Astro uses by default
// (@astrojs/markdown-satteri). @mdx-js/mdx is not installed in this project.
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { mdxToJs } from 'satteri';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const contentDir = path.join(root, 'src', 'content');

async function listMdx(dir) {
	const out = [];
	for (const entry of await readdir(dir, { withFileTypes: true })) {
		const full = path.join(dir, entry.name);
		if (entry.isDirectory()) out.push(...(await listMdx(full)));
		else if (entry.name.endsWith('.mdx')) out.push(full);
	}
	return out.sort();
}

// Strip YAML frontmatter the way Astro does, but keep line numbers stable.
function stripFrontmatter(src) {
	const m = /^---\r?\n[\s\S]*?\r?\n---(\r?\n|$)/.exec(src);
	if (!m) return src;
	const blank = m[0].split('\n').length - 1;
	return '\n'.repeat(blank) + src.slice(m[0].length);
}

function locate(err) {
	const msg = String(err?.message ?? err);
	const m = /^(\d+):(\d+):\s*/.exec(msg);
	if (m) return { line: Number(m[1]), col: Number(m[2]), msg: msg.slice(m[0].length) };
	const line = err?.line ?? err?.position?.start?.line ?? 1;
	const col = err?.column ?? err?.position?.start?.column ?? 1;
	return { line, col, msg: msg.split('\n')[0] };
}

const args = process.argv.slice(2);
const files = args.length
	? args.map((f) => path.resolve(process.cwd(), f))
	: await listMdx(contentDir);

let failures = 0;
for (const file of files) {
	const rel = path.relative(root, file);
	const src = stripFrontmatter(await readFile(file, 'utf8'));
	try {
		mdxToJs(src);
	} catch (err) {
		failures++;
		const { line, col, msg } = locate(err);
		console.log(`${rel}:${line}:${col} ${msg}`);
	}
}

console.log(`check:mdx ${files.length} files, ${failures} failed`);
process.exit(failures ? 1 : 0);
