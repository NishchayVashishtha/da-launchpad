import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';

// SITE_BASE: e.g. "/da-launchpad/" for GitHub Pages project sites. Default "/".
let base = process.env.SITE_BASE || '/';
if (!base.startsWith('/')) base = '/' + base;
if (!base.endsWith('/')) base += '/';

export default defineConfig({
  base,
  site: process.env.SITE_URL || undefined,
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [mdx(), react()],
  vite: { plugins: [tailwindcss()] },
});
