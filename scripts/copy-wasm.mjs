// Copies sql-wasm.wasm from node_modules into public/ so the site is fully self-hosted.
import { copyFileSync, mkdirSync } from 'node:fs';
mkdirSync('public', { recursive: true });
copyFileSync('node_modules/sql.js/dist/sql-wasm.wasm', 'public/sql-wasm.wasm');
console.log('copied sql-wasm.wasm -> public/');
