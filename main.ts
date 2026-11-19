// gta6-meme-x-01 entry (Node 22, standard library only).
// Reads POST.json at the repository root, validates that it names a real X post,
// copies it to the output directory where the gate reads it, then prints the URL
// back exactly as written plus one handover line.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const postPath = join(BOT_DIR, 'POST.json');
let url: string;
try {
  const parsed = JSON.parse(readFileSync(postPath, 'utf8')) as { url?: unknown };
  if (typeof parsed.url !== 'string') throw new Error('POST.json has no string "url"');
  url = parsed.url;
} catch (err) {
  console.error(`POST.json could not be read from ${postPath}: ${(err as Error).message}`);
  process.exit(1);
}

const match = /^https:\/\/(x\.com|twitter\.com)\/[^/]+\/status\/(\d+)$/.exec(url);
if (!match) {
  console.error(`POST.json url is not an X post address: ${url}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(postPath, join(OUTPUT_DIR, 'POST.json'));

console.log(url);
console.log('Entry handed over: the post above is the gta6-meme-x-01 submission.');
