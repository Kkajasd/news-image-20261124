// The World Today — Tuesday, 24 November 2026 (rebuild, v2 layout).
// The front page is pre-rendered by tools/draw_frontpage_v2.py into
// entry.png; this program only copies that image to the output directory,
// so repeated runs write byte-identical output.
import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

const bytes = readFileSync(source);
if (!isPng(bytes)) {
  throw new Error("entry.png is not a PNG file");
}
mkdirSync(outDir, { recursive: true });
writeFileSync(target, bytes);
if (statSync(target).size !== bytes.length) {
  throw new Error("copied entry.png size mismatch");
}
console.log(`Wrote ${target} (${bytes.length} bytes)`);

// Guard: the copied file must start with the PNG signature, so a
// truncated or wrong-format image fails loudly instead of shipping.
function isPng(buf: Buffer): boolean {
  const sig = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  return sig.every((b, i) => buf[i] === b);
}
