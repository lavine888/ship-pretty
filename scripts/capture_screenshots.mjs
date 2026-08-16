#!/usr/bin/env node
/**
 * Capture deterministic desktop/mobile screenshots for a static benchmark page.
 *
 * Usage:
 *   node scripts/capture_screenshots.mjs examples/demo-ui/index.html output/benchmarks/demo-after
 *
 * The repository does not vendor a browser runner. Make the `playwright` Node
 * package resolvable and install Chromium before invoking this script.
 */

import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const [htmlArg, outputArg] = process.argv.slice(2);
if (!htmlArg || !outputArg) {
  console.error("Usage: node scripts/capture_screenshots.mjs <html-file> <output-dir>");
  process.exit(2);
}

const htmlPath = resolve(htmlArg);
const outputDir = resolve(outputArg);
await mkdir(outputDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
let hasOverflow = false;
try {
  const cases = [
    ["desktop", { width: 1440, height: 1000 }],
    ["mobile", { width: 390, height: 844 }],
  ];

  for (const [label, viewport] of cases) {
    const page = await browser.newPage({ viewport, deviceScaleFactor: 1 });
    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle" });
    const metrics = await page.evaluate(() => ({
      viewportWidth: window.innerWidth,
      scrollWidth: document.documentElement.scrollWidth,
      scrollHeight: document.documentElement.scrollHeight,
    }));
    await page.screenshot({
      path: resolve(outputDir, `${label}.png`),
      fullPage: false,
    });
    const overflow = metrics.scrollWidth > metrics.viewportWidth;
    hasOverflow ||= overflow;
    console.log(`${label}: ${viewport.width}x${viewport.height}, page=${metrics.scrollWidth}x${metrics.scrollHeight}${overflow ? " [HORIZONTAL OVERFLOW]" : ""}`);
    await page.close();
  }
} finally {
  await browser.close();
}

if (hasOverflow) process.exitCode = 1;
