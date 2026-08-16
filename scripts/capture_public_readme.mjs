#!/usr/bin/env node
/** Capture the public README first viewport for the five-second comprehension check. */

import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const output = "output/playwright/github-readme.png";
await mkdir("output/playwright", { recursive: true });

const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  await page.goto("https://github.com/lavine888/ship-pretty", { waitUntil: "networkidle", timeout: 60000 });
  await page.screenshot({ path: output, fullPage: false });
  console.log(`Public README captured: ${output}`);
  console.log(`Title: ${await page.title()}`);
} finally {
  await browser.close();
}
