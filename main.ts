// The World Today - Tuesday, 24 November 2026.
// Copies the pre-rendered front page (entry.png, drawn by
// tools/draw_frontpage.py) to the output directory. The copy is
// byte-for-byte, so repeated runs write identical output.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error("entry.png not found next to main.ts");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`Wrote ${target}`);
