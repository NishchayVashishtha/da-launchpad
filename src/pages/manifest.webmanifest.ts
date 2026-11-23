import { url } from '../lib/url';
export function GET() {
  return new Response(JSON.stringify({
    name: 'DA Launchpad', short_name: 'DA Launchpad', description: 'Offline-capable Data Analyst study site.',
    start_url: url('/'), scope: url('/'), display: 'standalone', background_color: '#0f1220', theme_color: '#4338ca',
    icons: [
      { src: url('/icons/icon-192.png'), sizes: '192x192', type: 'image/png' },
      { src: url('/icons/icon-512.png'), sizes: '512x512', type: 'image/png' },
      { src: url('/icons/icon.svg'), sizes: 'any', type: 'image/svg+xml', purpose: 'any maskable' },
    ],
  }), { headers: { 'Content-Type': 'application/manifest+json' } });
}
