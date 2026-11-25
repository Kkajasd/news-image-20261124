// "The World Today" — front page for Tuesday 24 November 2026 (v2 layout).
//
// Entry program (Node 22, standard library only): the finished front
// page is entry.png beside this file; the program validates it as a
// whole PNG and copies it to the grader's output directory. The
// repository is mounted read-only in the grading sandbox, so NOTHING is
// ever written into the repo itself.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const REPO_DIR = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(REPO_DIR, "entry.png");

// The grader mounts the output directory (default /output) as a writable
// bind mount. Create it if missing; NEVER delete it or anything in it.
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUTPUT_PATH = join(OUTPUT_DIR, "entry.png");

mkdirSync(OUTPUT_DIR, { recursive: true });

// The finished front page is entry.png beside this file. The program
// copies it to the grader's output directory using the Node standard
// library only: the grading sandbox has no python3, so the earlier
// versions failed run_completes calling the Python renderer. Before
// copying, the whole PNG is validated: signature, IHDR dimensions, and
// every chunk's CRC, so a corrupt file fails loudly instead of being
// submitted as-is.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

// CRC-32 (IEEE) as PNG chunks use it.
const CRC_TABLE = new Uint32Array(256);
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  CRC_TABLE[n] = c >>> 0;
}
function crc32(buf: Buffer): number {
  let c = 0xffffffff;
  for (const b of buf) c = CRC_TABLE[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

const SOURCE_BYTES = readFileSync(SOURCE);
if (!SOURCE_BYTES.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error(`not a PNG file: ${SOURCE}`);
}
const srcWidth = SOURCE_BYTES.readUInt32BE(16);
const srcHeight = SOURCE_BYTES.readUInt32BE(20);
if (srcWidth !== 1024 || srcHeight !== 1024) {
  throw new Error(`unexpected dimensions ${srcWidth}x${srcHeight}, expected 1024x1024`);
}
let offset = 8;
let seenIEND = false;
while (offset + 12 <= SOURCE_BYTES.length) {
  const length = SOURCE_BYTES.readUInt32BE(offset);
  const type = SOURCE_BYTES.subarray(offset + 4, offset + 8).toString("ascii");
  const dataEnd = offset + 8 + length;
  if (dataEnd + 4 > SOURCE_BYTES.length) {
    throw new Error(`truncated PNG chunk ${type} at offset ${offset}`);
  }
  const storedCrc = SOURCE_BYTES.readUInt32BE(dataEnd);
  const actualCrc = crc32(SOURCE_BYTES.subarray(offset + 4, dataEnd));
  if (storedCrc !== actualCrc) {
    throw new Error(`CRC mismatch in PNG chunk ${type} at offset ${offset}`);
  }
  offset = dataEnd + 4;
  if (type === "IEND") {
    seenIEND = true;
    break;
  }
}
if (!seenIEND || offset !== SOURCE_BYTES.length) {
  throw new Error("PNG is not whole: missing IEND or trailing bytes");
}

// Copy the validated image into the output directory: the grader mounts
// it as a writable bind mount. Create it if missing; NEVER delete it.
copyFileSync(SOURCE, OUTPUT_PATH);

// Verify the copied image: PNG signature, dimensions from the IHDR
// chunk (must be 1024x1024), and a non-trivial file size. Reading the
// file back is a read, not a write — the repo stays untouched.
const bytes = readFileSync(OUTPUT_PATH);
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error(`not a PNG file: ${OUTPUT_PATH}`);
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`unexpected dimensions ${width}x${height}, expected 1024x1024`);
}
const size = statSync(OUTPUT_PATH).size;
if (size < 10_000) {
  throw new Error(`suspiciously small output: ${size} bytes`);
}
console.log(`Wrote ${OUTPUT_PATH} (${width}x${height}, ${size} bytes)`);
