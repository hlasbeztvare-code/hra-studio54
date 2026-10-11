import {chromium} from 'playwright';
import assert from 'node:assert/strict';
const browser=await chromium.launch({channel:'chrome',headless:true});
let count=0;
try{
 for(const [width,height] of [[320,568],[390,844],[1440,900]]){
  const p=await browser.newPage({viewport:{width,height}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.route('**/api/hit',r=>r.fulfill({json:{visits:106,plays:51}}));await p.route('https://s54-leaderboard.hlancaric.workers.dev/**',r=>r.fulfill({json:[]}));await p.route('https://fonts.googleapis.com/**',r=>r.abort());
  await p.addInitScript(()=>Math.random=()=>0);await p.goto(process.argv[2]||'http://localhost:5454',{waitUntil:'networkidle'});await p.locator('.s54-start').waitFor();
  await p.locator('.s54-start').click();await p.locator('.in5-nf-in').fill('Kontrola');await p.locator('.in5-nf-in').press('Enter');
  for(const index of [1,0,1,0]){await p.locator('.sa-opt').nth(index).click();}
  await p.locator('.hud-tabs').waitFor();await p.locator('.tab-bar').click();
  const crew=p.locator('.panel-loc img[alt="Péťa"],.panel-loc img[alt="Denisa"],.panel-loc img[alt="Martina"]');
  await crew.first().waitFor();assert.equal(await crew.count(),3);

  await p.waitForFunction(()=>['Péťa','Denisa','Martina'].every(n=>{const i=document.querySelector(`img[alt="${n}"]`);return i?.complete&&i.naturalWidth>0&&i.naturalHeight>0}));
  assert.ok(await crew.evaluateAll(xs=>xs.every(i=>i.getAttribute('src')===i.getAttribute('data-lsrc'))),'inline portrait data must remain intact');
  const testUrl='data:image/svg+xml;base64,PHN2Zy8+';assert.equal(await p.evaluate(s=>window.__res(s),testUrl),testUrl);assert.equal(await p.evaluate(()=>window.__res('blob:https://example.com/id')),'blob:https://example.com/id');assert.match(await p.evaluate(()=>window.__res('/uploads/intro-landchi.jpeg')),/\?v=\d+$/);
  for(const name of ['Péťa','Denisa','Martina']){
   await p.locator(`img[alt="${name}"]`).locator('..').click();
   await p.waitForFunction(()=>{const i=document.querySelector('.gls[class*="mg-"] img');return i?.complete&&i.naturalWidth>0});
   const close=name==='Péťa'?'Teď ne, Péťo':name==='Denisa'?'Utéct od pultu':'Utéct (Martina se urazí)';
   if(name==='Denisa')await p.getByRole('button',{name:'Mám to v hlavě',exact:true}).click();
   await p.getByRole('button',{name:close,exact:true}).click();
  }
  assert.deepEqual(errors,[]);await p.screenshot({path:`shots/crew-${width}x${height}.png`});await p.close();count++;console.log(`PASS crew ${width}×${height}: three portraits, original actions and modal portraits`);
 }
 console.log(`${count}/${count} crew checks PASS`);
}finally{await browser.close()}
