import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import assert from 'node:assert/strict';

const leaderboardUrl='https://s54-leaderboard.hlancaric.workers.dev/top';
const statsUrl='https://hra.l-code-dynamics.com/api/stats';
async function json(url){const r=await fetch(url);if(!r.ok)throw new Error(`${url}: ${r.status}`);return r.json()}
// Read existing production data only. Preview traffic never writes visits or scores.
const [top,stats]=await Promise.all([json(leaderboardUrl),json(statsUrl)]);
assert.ok(Array.isArray(top),'Leaderboard must be an array');
const seen=new Set();
const expected=top.slice().sort((a,b)=>b.s-a.s).filter(r=>{const k=String(r.n||'').trim().toLowerCase();if(!k||seen.has(k))return false;seen.add(k);return true}).slice(0,10);
await mkdir('shots',{recursive:true});
await writeFile('shots/live-preview-data.json',JSON.stringify({capturedAt:new Date().toISOString(),leaderboardUrl,statsUrl,top,stats},null,2));
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
 for(const [width,height] of [[1920,1080],[1440,900],[390,844]]){
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
  await page.route('**/api/hit',r=>r.fulfill({json:stats}));
  await page.route('https://s54-leaderboard.hlancaric.workers.dev/**',r=>r.request().url().endsWith('/top')?r.fulfill({json:top}):r.abort());
  await page.route('https://fonts.googleapis.com/**',r=>r.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://localhost:5454',{waitUntil:'networkidle'});
  await page.locator('.s54-start').waitFor();await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(650);
  const actual=await page.locator('.s54-row').evaluateAll(rows=>rows.map(row=>({n:row.children[1].textContent,s:Number(row.children[2].textContent)})));
  assert.deepEqual(actual,expected.map(({n,s})=>({n,s})),`Original leaderboard at ${width}×${height}`);
  assert.deepEqual(errors,[]);
  await page.screenshot({path:`shots/intro-${width}x${height}.png`,fullPage:true});
  console.log(`PASS: ${width}×${height}, original live names and scores (${expected[0]?.n}: ${expected[0]?.s})`);
  await page.close();
 }
}finally{await browser.close()}
