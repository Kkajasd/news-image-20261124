// "The World Today" — front page for Tuesday 24 November 2026 (v2 layout).
//
// Entry program: renders the front page by invoking the deterministic
// renderer (tools/draw_frontpage_v2.py) and writes the finished image to
// the grader's output directory. The repository is mounted read-only in
// the grading sandbox, so NOTHING is ever written into the repo itself:
// the output path is passed to the renderer as its argv[1] argument and
// the program only reads the result back for verification afterwards.

import { execFileSync, execSync } from "node:child_process";
import { mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const REPO_DIR = dirname(fileURLToPath(import.meta.url));
const RENDERER = join(REPO_DIR, "tools", "draw_frontpage_v2.py");

// The grader mounts the output directory (default /output) as a writable
// bind mount. Create it if missing; NEVER delete it or anything in it.
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUTPUT_PATH = join(OUTPUT_DIR, "entry.png");

mkdirSync(OUTPUT_DIR, { recursive: true });

// The grading sandbox (node22 image) ships python3 but no Pillow and no
// Liberation fonts, so the renderer cannot import PIL there — round 2
// failed run_completes with exit 1 for exactly this. Vendor both: the
// Pillow wheel matching the runtime's python version is extracted to
// /tmp and put on PYTHONPATH; the fonts live in tools/fonts.
const PY_VERSION = execSync(
  "python3 -c \"import sys; print(f'{sys.version_info.major}{sys.version_info.minor}')\"",
  { encoding: "utf8" },
).trim();
const WHEEL = join(
  REPO_DIR,
  "tools",
  "vendor",
  `pillow-10.2.0-cp${PY_VERSION}-cp${PY_VERSION}-manylinux_2_28_x86_64.whl`,
);
const PIL_DIR = join("/tmp", `pillow-cp${PY_VERSION}`);
execFileSync("python3", ["-m", "zipfile", "-e", WHEEL, PIL_DIR], {
  stdio: "inherit",
});

// Render straight into the output directory: argv[1] is the output path
// the renderer writes to (default would be entry.png in the repo root,
// which is read-only in the sandbox and made the dev run exit 1).
execFileSync("python3", [RENDERER, OUTPUT_PATH], {
  cwd: REPO_DIR,
  stdio: "inherit",
  env: { ...process.env, PYTHONPATH: PIL_DIR },
});

// Verify the rendered image: PNG signature, dimensions from the IHDR
// chunk (must be 1024x1024), and a non-trivial file size. Reading the
// file back is a read, not a write — the repo stays untouched.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
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
