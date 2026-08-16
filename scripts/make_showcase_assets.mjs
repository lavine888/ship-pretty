#!/usr/bin/env node
/**
 * Build the README showcase images from the real landing-page captures.
 * The screenshots stay truthful; the surrounding poster layout supplies the
 * visual story that a plain Markdown table cannot.
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

const base = `
  * { box-sizing: border-box; }
  html, body { margin: 0; background: #0d1020; }
  body { color: #f8f4ed; font-family: Arial, Helvetica, sans-serif; }
  .canvas { position: relative; overflow: hidden; width: 1600px; background: #0d1020; }
  .canvas::before { content: ""; position: absolute; inset: 0; opacity: .22; background-image: linear-gradient(#ffffff12 1px, transparent 1px), linear-gradient(90deg, #ffffff12 1px, transparent 1px); background-size: 36px 36px; mask-image: linear-gradient(to bottom, black, transparent 80%); }
  .canvas::after { content: ""; position: absolute; width: 520px; height: 520px; right: -130px; top: -160px; border-radius: 50%; background: #e75c7f; filter: blur(8px); opacity: .83; }
  .inner { position: relative; z-index: 1; padding: 52px 66px 50px; }
  .top { display: flex; justify-content: space-between; align-items: center; color: #b6c1b8; font: 700 12px/1.2 "Courier New", monospace; letter-spacing: .14em; text-transform: uppercase; }
  .brand { display: flex; align-items: center; gap: 12px; color: #f8f4ed; }
  .mark { display: grid; place-items: center; width: 31px; height: 31px; background: #d9f45a; color: #0d1020; font: 900 11px Arial, sans-serif; letter-spacing: -.05em; }
  .eyebrow { margin-top: 74px; color: #d9f45a; font: 700 13px/1.2 "Courier New", monospace; letter-spacing: .16em; text-transform: uppercase; }
  .title { max-width: 840px; margin: 18px 0 0; font-size: 88px; line-height: .89; letter-spacing: -.085em; }
  .title em { color: #d9f45a; font-style: normal; }
  .sub { max-width: 650px; margin: 25px 0 0; color: #c3c7cd; font-size: 18px; line-height: 1.45; }
  .flow { display: flex; align-items: center; gap: 10px; margin-top: 32px; color: #0d1020; font: 900 11px/1 "Courier New", monospace; letter-spacing: .08em; }
  .flow span { padding: 10px 12px; background: #f8f4ed; }
  .flow span:nth-child(2) { background: #ff806b; }
  .flow span:nth-child(3) { background: #d9f45a; }
  .flow span:nth-child(4) { background: #bd93ff; }
  .arrow { color: #f8f4ed; font-size: 18px; }
  .compare { display: flex; align-items: center; justify-content: center; gap: 18px; margin: 54px 0 0 236px; }
  .shot { width: 480px; padding: 13px 13px 17px; background: #f8f4ed; color: #0d1020; box-shadow: 12px 14px 0 #00000040; }
  .shot.before { transform: rotate(-2.3deg) translateY(12px); }
  .shot.after { transform: rotate(2.3deg) translateY(-8px); }
  .shot-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 11px; font: 900 11px/1 "Courier New", monospace; letter-spacing: .08em; text-transform: uppercase; }
  .shot-head .tag { padding: 6px 8px; background: #0d1020; color: #f8f4ed; }
  .shot.after .shot-head .tag { background: #d9f45a; color: #0d1020; }
  .shot img { display: block; width: 100%; height: 250px; object-fit: cover; object-position: top; border: 1px solid #0d1020; }
  .shot-foot { display: flex; justify-content: space-between; margin-top: 12px; font: 700 11px/1.1 "Courier New", monospace; }
  .shot-foot strong { color: #e75c7f; }
  .shot.after .shot-foot strong { color: #17634b; }
  .verdict { display: flex; flex: 0 0 106px; flex-direction: column; align-items: center; gap: 11px; color: #f8f4ed; font: 900 10px/1.2 "Courier New", monospace; letter-spacing: .08em; text-align: center; text-transform: uppercase; }
  .verdict b { display: grid; place-items: center; width: 72px; height: 72px; border-radius: 50%; background: #ff806b; color: #0d1020; font: 900 16px/1 Arial, sans-serif; transform: rotate(-8deg); }
  .verdict i { font-size: 32px; font-style: normal; color: #d9f45a; }
  .caption { margin-top: 44px; color: #a9b1b8; font: 700 12px/1.4 "Courier New", monospace; letter-spacing: .08em; text-transform: uppercase; }
`;

const hero = `<!doctype html><html><head><style>${base}
  .hero-canvas { height: 900px; }
  .hero-canvas .compare { margin-top: 54px; }
</style></head><body><section class="canvas hero-canvas"><div class="inner">
  <div class="top"><div class="brand"><span class="mark">SP</span> Ship Pretty</div><div>Case 001 / visual QA</div></div>
  <div class="eyebrow">The visual quality gate for AI-built interfaces</div>
  <h1 class="title">AI can generate.<br><em>Ship Pretty decides.</em></h1>
  <p class="sub">A screenshot-backed loop that turns “looks good in code” into a decision you can actually inspect.</p>
  <div class="flow"><span>RENDER</span><b class="arrow">→</b><span>JUDGE</span><b class="arrow">→</b><span>PATCH</span><b class="arrow">→</b><span>RE-RENDER</span></div>
  <div class="compare">
    <article class="shot before"><div class="shot-head"><span>Without Ship Pretty</span><span class="tag">Not ready</span></div><img src="${before}" alt="Generic AI landing page before refinement"><div class="shot-foot"><span>centered stack / equal cards</span><strong>43 / 100</strong></div></article>
    <div class="verdict"><b>PATCH<br>THE<br>BIGGEST</b><i>→</i><span>same fixture<br>better decision</span></div>
    <article class="shot after"><div class="shot-head"><span>With Ship Pretty</span><span class="tag">Ready to ship</span></div><img src="${after}" alt="Refined Ship Pretty landing page"><div class="shot-foot"><span>hierarchy / evidence / intent</span><strong>84 / 100</strong></div></article>
  </div>
  <div class="caption">One rendered frame is a claim. Before / after evidence is a case.</div>
</div></section></body></html>`;

const loop = `<!doctype html><html><head><style>${base}
  .loop-canvas { height: 650px; background: #f8f4ed; color: #0d1020; }
  .loop-canvas::before { opacity: .35; background-image: linear-gradient(#0d102012 1px, transparent 1px), linear-gradient(90deg, #0d102012 1px, transparent 1px); }
  .loop-canvas::after { right: -230px; top: 350px; width: 460px; height: 460px; background: #ff806b; opacity: .35; }
  .loop-canvas .top { color: #68716f; }
  .loop-canvas .brand { color: #0d1020; }
  .loop-canvas .mark { background: #0d1020; color: #d9f45a; }
  .loop-canvas .eyebrow { margin-top: 58px; color: #e75c7f; }
  .loop-canvas .title { color: #0d1020; font-size: 66px; }
  .loop-canvas .title em { color: #17634b; }
  .loop { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin-top: 52px; }
  .step { position: relative; min-height: 185px; padding: 18px; border: 2px solid #0d1020; background: #ffffff; box-shadow: 8px 9px 0 #0d1020; }
  .step:nth-child(2) { background: #ffddd2; transform: translateY(18px); }
  .step:nth-child(3) { background: #d9f45a; transform: translateY(-8px); }
  .step:nth-child(4) { background: #d9ccff; transform: translateY(22px); }
  .step:nth-child(5) { background: #bdebd2; transform: translateY(-2px); }
  .step-num { font: 900 12px/1 "Courier New", monospace; }
  .step h2 { margin: 34px 0 8px; font-size: 28px; line-height: .92; letter-spacing: -.07em; }
  .step p { margin: 0; color: #4e5b58; font-size: 12px; line-height: 1.35; }
  .step:not(:last-child)::after { content: "→"; position: absolute; right: -31px; top: 75px; z-index: 2; color: #e75c7f; font-size: 30px; font-weight: 900; }
  .loop-note { display: flex; justify-content: space-between; margin-top: 56px; color: #4e5b58; font: 700 12px/1.4 "Courier New", monospace; letter-spacing: .04em; }
</style></head><body><section class="canvas loop-canvas"><div class="inner">
  <div class="top"><div class="brand"><span class="mark">SP</span> Ship Pretty</div><div>How the gate works</div></div>
  <div class="eyebrow">Not a style checklist / a stopping condition</div>
  <h1 class="title">The loop is the product.<br><em>The screenshot is the evidence.</em></h1>
  <div class="loop">
    <article class="step"><div class="step-num">01 / SEE IT</div><h2>Render</h2><p>Make the browser show the actual interface.</p></article>
    <article class="step"><div class="step-num">02 / NAME IT</div><h2>Judge</h2><p>Find the biggest visible problem, not the easiest CSS tweak.</p></article>
    <article class="step"><div class="step-num">03 / FIX IT</div><h2>Patch</h2><p>Change one to three high-leverage decisions.</p></article>
    <article class="step"><div class="step-num">04 / SEE AGAIN</div><h2>Re-render</h2><p>Compare the new frame against the evidence.</p></article>
    <article class="step"><div class="step-num">05 / DECIDE</div><h2>Gate</h2><p>Pass, keep iterating, or report the blocker.</p></article>
  </div>
  <div class="loop-note"><span>DESKTOP 1440×1000 + MOBILE 390×844</span><span>NO CODE-ONLY CLAIMS</span></div>
</div></section></body></html>`;

const browser = await chromium.launch({ headless: true });
try {
  const heroPage = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  await heroPage.setContent(hero, { waitUntil: "load" });
  await heroPage.screenshot({ path: resolve(assetRoot, "ship-pretty-hero.png"), fullPage: false });
  await heroPage.close();

  const loopPage = await browser.newPage({ viewport: { width: 1600, height: 650 }, deviceScaleFactor: 1 });
  await loopPage.setContent(loop, { waitUntil: "load" });
  await loopPage.screenshot({ path: resolve(assetRoot, "ship-pretty-loop.png"), fullPage: false });
  await loopPage.close();
} finally {
  await browser.close();
}

console.log("Showcase assets written: assets/ship-pretty-hero.png, assets/ship-pretty-loop.png");
