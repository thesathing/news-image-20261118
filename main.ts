// news-image-20261118: "THE WORLD TODAY" — Wednesday 18 November 2026 in one image.
//
// The entry is a front page drawn for the day's news: 43 stories across
// 6 continents — a dark masthead with a red news ticker, three rich lead
// diagrams (the Kerch Bridge, the Gulf, the Shenzhen summit), ten
// illustrated story cards with captioned scenes, a world map with
// colour-coded pins, and a numbered also-list of the rest of the day.
// main.ts copies the finished page (entry.png, beside this file) to
// /output/entry.png, verifying it first so a corrupt or oversized file
// can never reach the judge. Node 22, standard library only, no network.
//
// Run it outside the grader's container with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1024 * 1024;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(message: string): never {
  throw new Error(`news-image-20261118: ${message}`);
}

function pngDimensions(bytes: Buffer): { width: number; height: number } {
  if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail('entry.png is not a PNG file');
  }
  if (bytes.toString('ascii', 12, 16) !== 'IHDR') {
    fail('entry.png has no IHDR chunk');
  }
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

// A PNG is only whole when it ends with its IEND trailer: a length of 0,
// the letters IEND, and the fixed CRC AE426082. Without this check a file
// cut short mid-write would still pass the header checks above.
const IEND_TRAILER = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);

function pngIsComplete(bytes: Buffer): boolean {
  return (
    bytes.length >= IEND_TRAILER.length &&
    bytes.subarray(bytes.length - IEND_TRAILER.length).equals(IEND_TRAILER)
  );
}

const here = fileURLToPath(new URL('.', import.meta.url));
const sourcePath = join(here, 'entry.png');
const source = readFileSync(sourcePath);
const stat = statSync(sourcePath);

if (stat.size > MAX_BYTES) {
  fail(`entry.png is ${stat.size} bytes, over the 1 MiB limit`);
}
const { width, height } = pngDimensions(source);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  fail(`entry.png is ${width}x${height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`);
}
if (!pngIsComplete(source)) {
  fail('entry.png is truncated: missing IEND trailer');
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, 'entry.png');
writeFileSync(outPath, source);

// The grader runs this program twice and both runs must write the same
// bytes, so read the copy back and compare it with the source byte for byte.
const written = readFileSync(outPath);
if (!written.equals(source)) {
  fail('the written entry.png differs from the source');
}

const sha256 = createHash('sha256').update(source).digest('hex');
console.log(`wrote ${outPath} (${source.length} bytes, sha256 ${sha256})`);
