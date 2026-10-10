import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { readFileSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';

const original=JSON.parse(readFileSync('scripts/fixtures/intro-original-copy.json','utf8'));
const current=readFileSync('src/template.html','utf8');
const copy=JSON.parse(current.match(/const INTRO_COPY=(.*);/)[1]);
assert.equal(copy.pepa,original.pepa);
assert.deepEqual(copy.information,original.information);
assert.deepEqual(copy.rules,original.rules);
const gameData=current.slice(current.indexOf('const QS='),current.indexOf('const INIT='));
assert.equal(createHash('sha256').update(gameData).digest('hex'),original.gameDataHash);
console.log('PASS: original copy, rules and game data preserved');

mkdirSync('shots',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
let checks=1;
const top=['Jose Madeira','Yan Lan','Rio','Mark Evill','Landchi','Mazer','Terran','Jerome Levis','Bema One','Peet V'].map((n,i)=>({n,s:50615-i*3210,t:i+1}));
async function open(width,height,options={}){
 const p=await browser.newPage({viewport:{width,height},...options});
 await p.route('**/api/hit',r=>r.fulfill({json:{visits:106,plays:51}}));
 await p.route('https://s54-leaderboard.hlancaric.workers.dev/**',r=>r.fulfill({json:r.request().url().endsWith('/top')?top:{run:'preview'}}));
 await p.route('https://fonts.googleapis.com/**',r=>r.abort());
 await p.addInitScript(()=>localStorage.setItem('s54g_best','36847'));
 p.errors=[];p.on('pageerror',e=>p.errors.push(e.message));
 await p.goto('http://localhost:5454',{waitUntil:'networkidle'});
 await p.locator('.s54-start').waitFor();await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(650);
 return p;
}
const overlap=(a,b)=>Math.min(a.x+a.width,b.x+b.width)>Math.max(a.x,b.x)&&Math.min(a.y+a.height,b.y+b.height)>Math.max(a.y,b.y);
try{
 for(const [width,height] of [[1920,1080],[1440,900]]){
  const p=await open(width,height);
  assert.deepEqual(p.errors,[]);
  const scene=await p.locator('.s54-scene').boundingBox();
  assert.ok(scene.x>=-1&&scene.y>=-1&&scene.x+scene.width<=width+1&&scene.y+scene.height<=height+1,'uncropped stage');
  const boxes={};for(const k of ['top','stats','pepa','woman','poster-left','poster-right','start','hud']) boxes[k]=await p.locator('.s54-'+(k==='pepa'||k==='woman'?k:k)).boundingBox();
  for(const [a,b] of [['top','stats'],['woman','poster-right'],['stats','woman'],['top','woman'],['pepa','poster-left'],['start','hud']]) assert.ok(!overlap(boxes[a],boxes[b]),`${a} overlaps ${b}`);
  assert.equal(boxes['poster-left'].width,boxes['poster-right'].width);assert.equal(boxes['poster-left'].height,boxes['poster-right'].height);
  // Artwork bounds are manually reviewed: faces and car must remain clear.
  const region=(x,y,w,h)=>({x:scene.x+x*scene.width,y:scene.y+y*scene.height,width:w*scene.width,height:h*scene.height});
  for(const subject of [region(.245,.355,.065,.105),region(.706,.365,.08,.115),region(.335,.535,.38,.277)]){
   for(const k of ['top','stats','pepa','woman','poster-left','poster-right','start','hud'])assert.ok(!overlap(boxes[k],subject),`${k} covers protected artwork`);
  }
  assert.equal(await p.locator('.s54-row').count(),10);assert.equal(await p.locator('.s54-row').last().locator('span').first().textContent(),'10');
  assert.equal(await p.locator('.s54-pepa').textContent(),copy.pepa);
  assert.equal(await p.locator('.s54-woman').textContent(),copy.information[0]);
  assert.ok(await p.locator('.s54-stats').isVisible());
  assert.ok((await p.locator('.s54-poster img').evaluateAll(xs=>xs.every(i=>i.complete&&i.naturalWidth>1000))));
  assert.ok(await p.evaluate(async()=>{const i=new Image();i.src=getComputedStyle(document.querySelector('.s54-art')).backgroundImage.match(/url\("?(.*?)"?\)/)[1];try{await i.decode();return i.naturalWidth>1600}catch{return false}}));
  const animation=await p.locator('.s54-ticker-track').evaluate(el=>{const a=el.getAnimations()[0];a.pause();a.currentTime=1000;const first=new DOMMatrix(getComputedStyle(el).transform).m41;a.currentTime=2000;return {first,second:new DOMMatrix(getComputedStyle(el).transform).m41,frames:a.effect.getKeyframes(),timing:a.effect.getTiming()}});
  assert.ok(animation.second<animation.first,'ticker only moves left');assert.equal(animation.timing.easing,'linear');assert.equal(animation.timing.iterations,Infinity);assert.equal(animation.frames.at(-1).transform,'translateX(-50%)');
  await p.locator('.s54-ticker-track').evaluate(el=>{const a=el.getAnimations()[0];a.currentTime=0;a.play()});
  await p.screenshot({path:`shots/check-intro-${width}x${height}.png`});
  const toggle=p.locator('.s54-hud-left button').first();await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert.ok(!await p.locator('.s54-top').isVisible());await toggle.click();assert.ok(await p.locator('.s54-top').isVisible());
  await p.locator('.s54-top-close').click();assert.ok(!await p.locator('.s54-top').isVisible());await toggle.click();
  await p.locator('.s54-hud-right button').click();await p.locator('.h7-box').waitFor();await p.locator('.h7-x').click();
  await p.getByRole('button',{name:'Uložit na plochu',exact:true}).click();assert.ok(await p.locator('.h7-os').isVisible());await p.locator('.h7-x').click();
  await p.locator('.s54-start').click();await p.locator('.in5-nf').waitFor();await p.locator('.in5-nf-go').click();assert.match(await p.locator('.in5-nf-err').textContent(),/Nejdřív se zapiš/);await p.locator('.in5-nf-in').fill('Rio');await p.locator('.in5-nf-in').press('Enter');await p.locator('[data-screen-label="Pepa"]').waitFor();assert.equal(await p.locator('.sa-opt').count(),3);
  assert.deepEqual(p.errors,[]);await p.close();checks++;console.log(`PASS: ${width}×${height}, layout, motion, controls, original start/gate flow`);
 }
 const mobile=await open(390,844);assert.ok(await mobile.evaluate(()=>document.documentElement.scrollWidth<=390));await mobile.locator('.s54-hud').scrollIntoViewIfNeeded();await mobile.screenshot({path:'shots/check-intro-390x844.png',fullPage:true});assert.deepEqual(mobile.errors,[]);await mobile.close();checks++;console.log('PASS: mobile fallback and no horizontal overflow');
 const reduced=await open(1440,900,{reducedMotion:'reduce'});assert.equal(await reduced.locator('.s54-ticker-track').evaluate(e=>getComputedStyle(e).animationName),'none');const before=await reduced.locator('.s54-woman').textContent();await reduced.waitForTimeout(9500);assert.equal(await reduced.locator('.s54-woman').textContent(),before);await reduced.close();checks++;console.log('PASS: reduced motion disables ticker and phrase rotation');
 const dynamic=await open(1440,900);await dynamic.mouse.move(0,0);await dynamic.waitForTimeout(9500);assert.equal(await dynamic.locator('.s54-woman').textContent(),copy.information[1]);assert.notEqual(await dynamic.locator('.s54-pepa').textContent(),copy.pepa);assert.ok(gameData.includes(await dynamic.locator('.s54-pepa').textContent()));await dynamic.close();checks++;console.log('PASS: both bubbles rotate existing text');
 const empty=await browser.newPage({viewport:{width:1440,height:900}});await empty.route('**/api/hit',r=>r.fulfill({status:503,body:''}));await empty.route('https://s54-leaderboard.hlancaric.workers.dev/**',r=>r.abort());await empty.goto('http://localhost:5454');await empty.locator('.s54-row').waitFor();assert.match(await empty.locator('.s54-top').textContent(),/Zatím nikdo/);assert.equal(await empty.locator('.s54-stats').count(),0);await empty.close();checks++;console.log('PASS: offline leaderboard and missing stats fallback');
 const xss=await open(1440,900);await xss.route('**/top',r=>r.fulfill({json:[{n:'<img src=x onerror="window.pwned=1">',s:1,t:1}]}));await xss.locator('.s54-top-head button').first().click();await xss.waitForTimeout(400);assert.equal(await xss.locator('.s54-row img').count(),0);assert.equal(await xss.evaluate(()=>window.pwned),undefined);await xss.close();checks++;console.log('PASS: leaderboard renders untrusted names as text');
 console.log(`${checks}/${checks} PASS`);
}finally{await browser.close()}
