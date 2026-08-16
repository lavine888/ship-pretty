#!/usr/bin/env node
/**
 * Build the README hero from real benchmark captures.
 *
 * This is intentionally a report plate, not a marketing poster: the rendered
 * screenshots are the dominant visual and the surrounding UI only labels the
 * evidence.
 */

import { createRequire } from "node:module";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const assetRoot = resolve(repoRoot, "assets");

async function dataUrl(path) {
  const bytes = await readFile(path);
  return `data:image/png;base64,${bytes.toString("base64")}`;
}

const before = await dataUrl(resolve(assetRoot, "benchmarks/landing-page/before/desktop.png"));
const after = await dataUrl(resolve(assetRoot, "benchmarks/landing-page/after/desktop.png"));

const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <style>
      * { box-sizing: border-box; }
      html, body { margin: 0; background: #f5f5f2; }
      body { color: #111411; font-family: Arial, Helvetica, sans-serif; }
      .plate { width: 1600px; height: 1150px; padding: 58px 64px 56px; background: #f5f5f2; }
      .meta { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #d5d7d2; padding-bottom: 18px; color: #666b66; font: 700 13px/1.2 "Courier New", monospace; letter-spacing: .08em; text-transform: uppercase; }
      .meta strong { color: #111411; }
      .intro { display: grid; grid-template-columns: 1fr auto; align-items: end; gap: 40px; padding: 34px 0 30px; }
      h1 { max-width: 900px; margin: 0; font-size: 62px; line-height: .98; letter-spacing: -.055em; font-weight: 800; }
      .sub { max-width: 500px; margin: 15px 0 0; color: #505651; font-size: 18px; line-height: 1.35; }
      .caption { align-self: end; padding-bottom: 4px; color: #505651; font: 700 13px/1.35 "Courier New", monospace; text-align: right; }
      .caption strong { color: #111411; }
      .compare { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
      .case { min-width: 0; border-top: 6px solid #c9362b; }
      .case.after { border-top-color: #1d6b4c; }
      .case-head { display: flex; justify-content: space-between; align-items: center; min-height: 58px; }
      .case-label { font: 800 15px/1 "Courier New", monospace; letter-spacing: .06em; text-transform: uppercase; }
      .case-status { color: #c9362b; font: 800 14px/1 "Courier New", monospace; letter-spacing: .04em; text-transform: uppercase; }
      .after .case-status { color: #1d6b4c; }
      .shot { display: block; width: 100%; height: 505px; border: 1px solid #c9ccc6; object-fit: cover; object-position: top; background: white; }
      .case-foot { display: flex; justify-content: space-between; align-items: baseline; padding-top: 17px; }
      .score { font-size: 34px; line-height: 1; letter-spacing: -.05em; font-weight: 800; }
      .before .score { color: #c9362b; }
      .after .score { color: #1d6b4c; }
      .score small { margin-left: 7px; color: #5e645e; font: 700 12px/1 "Courier New", monospace; letter-spacing: .06em; text-transform: uppercase; }
      .note { color: #5e645e; font: 700 12px/1.2 "Courier New", monospace; text-align: right; }
      .divider { display: flex; justify-content: center; align-items: center; gap: 20px; height: 50px; color: #5e645e; font: 700 12px/1 "Courier New", monospace; letter-spacing: .08em; text-transform: uppercase; }
      .divider::before, .divider::after { content: ""; width: 40px; height: 1px; background: #b9bdb7; }
      .divider b { color: #111411; font-size: 22px; }
      .footer { display: flex; justify-content: space-between; border-top: 1px solid #d5d7d2; margin-top: 26px; padding-top: 16px; color: #666b66; font: 700 12px/1.2 "Courier New", monospace; letter-spacing: .05em; text-transform: uppercase; }
      .failure { color: #c9362b; }
      .success { color: #1d6b4c; }
    </style>
  </head>
  <body>
    <main class="plate">
      <div class="meta"><span><strong>Ship Pretty</strong> / visual benchmark 001</span><span>Landing page / 1440×1000</span></div>
      <section class="intro">
        <div>
          <h1>Your coding agent is lying to you.</h1>
          <p class="sub">“Done” means the code runs. It doesn't mean the UI is good.</p>
        </div>
        <div class="caption"><strong>Same fixture.</strong><br>One visual QA loop.</div>
      </section>
      <section class="compare" aria-label="Before and after comparison">
        <article class="case before">
          <div class="case-head"><span class="case-label">Without Ship Pretty</span><span class="case-status">Not ready</span></div>
          <img class="shot" src="${before}" alt="Landing page before Ship Pretty">
          <div class="case-foot"><div class="score">43 / 100<small>visual score</small></div><div class="note">runs successfully<br>fails visibly</div></div>
        </article>
        <article class="case after">
          <div class="case-head"><span class="case-label">With Ship Pretty</span><span class="case-status">Ship it</span></div>
          <img class="shot" src="${after}" alt="Landing page after Ship Pretty">
          <div class="case-foot"><div class="score">84 / 100<small>visual score</small></div><div class="note">same fixture<br>after one loop</div></div>
        </article>
      </section>
      <div class="divider"><span>WITHOUT SHIP PRETTY</span><b>→</b><span>WITH SHIP PRETTY</span></div>
      <div class="footer"><span class="failure">43 / 100 · not ready</span><span>render → judge → patch → re-render → gate</span><span class="success">84 / 100 · ship it</span></div>
    </main>
  </body>
</html>`;

const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1600, height: 1150 }, deviceScaleFactor: 1 });
  await page.setContent(html, { waitUntil: "load" });
  await page.screenshot({ path: resolve(assetRoot, "ship-pretty-hero.png"), fullPage: false });
  await page.close();
} finally {
  await browser.close();
}

console.log("Showcase asset written: assets/ship-pretty-hero.png");
