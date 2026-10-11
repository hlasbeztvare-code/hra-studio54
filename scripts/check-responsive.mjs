import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {mkdirSync} from 'node:fs';

const browser=await chromium.launch({channel:'chrome',headless:true});
mkdirSync('shots',{recursive:true});
const sizes=[[320,568],[360,640],[375,667],[390,844],[430,932],[600,960],[768,1024],[1024,1366],[844,390],[932,430],[1024,600],[1280,720],[1400,800],[1440,900],[1920,1080]];
const top=Array.from({length:10},(_,i)=>({n:i===0?'Asistentka kočičak':`Hráč ${i+1}`,s:50615-i*3000,t:i+1}));
async function pageFor(width,height){
 const p=await browser.newPage({viewport:{width,height},isMobile:width<1400,hasTouch:width<1400,reducedMotion:'reduce'});
 p.errors=[];p.on('pageerror',e=>p.errors.push(e.message));
 await p.route('**/api/hit',r=>r.fulfill({json:{visits:106,plays:51}}));
 await p.route('https://s54-leaderboard.hlancaric.workers.dev/**',r=>r.fulfill({json:r.request().url().endsWith('/top')?top:{run:'check'}}));
 await p.route('https://fonts.googleapis.com/**',r=>r.abort());
 await p.addInitScript(()=>localStorage.setItem('s54g_best','9007199254740991'));
 await p.goto('http://localhost:5454',{waitUntil:'networkidle'});await p.locator('.s54-start').waitFor();await p.evaluate(()=>document.fonts.ready);
 return p;
}
async function noOverflow(p,width){
 const overflow=await p.evaluate(()=>['html','body','.game-root','.in5','.s54-scene','.s54-hud','.s54-posters','.s54-top','.in5-nf','.h7-box','.mg-lb','.s54-poster-view'].flatMap(selector=>[...document.querySelectorAll(selector)].filter(e=>e.clientWidth>0&&e.scrollWidth>e.clientWidth+2).map(e=>({selector,client:e.clientWidth,scroll:e.scrollWidth}))));
 if(overflow.length)await p.screenshot({path:'shots/responsive-debug.png'});
 assert.deepEqual(overflow,[],'horizontal overflow in a content container');
 for(const selector of ['.s54-start','.s54-hud','.s54-pill','.s54-record','.s54-speech','.s54-poster','.s54-top']){
  for(const el of await p.locator(selector).all()){
   if(!await el.isVisible())continue;const b=await el.boundingBox();assert.ok(b.x>=-1&&b.x+b.width<=width+1,`${selector} outside ${width}px: ${JSON.stringify(b)}`);
  }
 }
}
async function visibleDialog(p,selector,width,height){
 const b=await p.locator(selector).boundingBox();assert.ok(b.x>=0&&b.x+b.width<=width+1&&b.y>=0&&b.y+b.height<=height+1,`${selector} outside visible viewport: ${JSON.stringify(b)}`);await noOverflow(p,width);
}
let count=0;
try{
 for(const [width,height] of sizes){
  const p=await pageFor(width,height);await noOverflow(p,width);
  const compact=await p.locator('.s54-visual').evaluate(e=>getComputedStyle(e).display!=='contents');
  if(compact){
   const cta=await p.locator('.s54-start').boundingBox();assert.ok(cta.y>=0&&cta.y+cta.height<=height+1,'START requires scrolling on first view');
   const art=await p.locator('.s54-artframe').boundingBox();for(const bubble of await p.locator('.s54-speech').all()){const b=await bubble.boundingBox();assert.ok(b.y+b.height<=art.y,'bubble must sit above its character');}
   const visual=await p.locator('.s54-visual').boundingBox();assert.ok(visual.height>=100,'scene remains visible');
   for(const button of await p.locator('.s54-pill').all()){const b=await button.boundingBox();assert.ok(b.width>=44&&b.height>=44,'touch target too small')}
   await p.locator('.in5').evaluate(e=>{e.scrollTop=e.scrollHeight});
   assert.ok(await p.locator('.s54-poster-right').evaluate(e=>e.getBoundingClientRect().bottom<=innerHeight+1),'bottom content unreachable');
   await p.locator('.s54-hud-right button').evaluate(e=>e.click());await p.locator('.h7-box').waitFor();await visibleDialog(p,'.h7-ov',width,height);await p.locator('.h7-x').click();
   await p.locator('.in5').evaluate(e=>{e.scrollTop=e.scrollHeight});await p.getByRole('button',{name:'Uložit na plochu',exact:true}).evaluate(e=>e.click());await p.locator('.h7-os').waitFor();await visibleDialog(p,'.h7-ov',width,height);await p.locator('.h7-x').click();
   await p.locator('.in5').evaluate(e=>{e.scrollTop=e.scrollHeight});await p.locator('.s54-start').evaluate(e=>e.click());await p.locator('.in5-nf').waitFor();await visibleDialog(p,'.in5-nf',width,height);await p.locator('.in5-nf-in').fill('Rio');await p.locator('.in5-nf-x').click();
   await p.locator('.in5').evaluate(e=>{e.scrollTop=e.scrollHeight});await p.locator('.s54-top-head button').first().evaluate(e=>e.click());await p.locator('.mg-lb').waitFor();await noOverflow(p,width);assert.ok(await p.locator('.mg-lb').isVisible());await p.getByRole('button',{name:'Zpátky do klubu',exact:true}).click();
   await p.locator('.in5').evaluate(e=>{e.scrollTop=0});
  }
  for(const side of ['left','right']){
   const poster=p.locator('.s54-poster-'+side);await poster.click();await p.locator('.s54-poster-view').waitFor();await visibleDialog(p,'.s54-poster-view',width,height);
   assert.ok(await p.locator('.s54-poster-view img').evaluate(e=>e.complete&&e.naturalWidth>1000));
   await p.keyboard.press('Tab');assert.equal(await p.locator('.s54-poster-x').evaluate(e=>e===document.activeElement),true);
   if(side==='left')await p.keyboard.press('Escape');else await p.locator('.s54-poster-x').click();
   assert.equal(await p.locator('.s54-poster-view').count(),0);
  }
  await p.locator('.in5').evaluate(e=>e.scrollTop=0);
  if([320,390,768,844,1280,1400].includes(width))await p.screenshot({path:`shots/check-responsive-${width}x${height}.png`});
  assert.deepEqual(p.errors,[]);await p.close();count++;console.log(`PASS responsive ${width}×${height}: content bounds, reachable controls and dialogs`);
 }
 const rotated=await pageFor(390,844);await rotated.setViewportSize({width:844,height:390});await noOverflow(rotated,844);await rotated.setViewportSize({width:390,height:844});await noOverflow(rotated,390);await rotated.locator('.s54-start').click();await rotated.setViewportSize({width:390,height:300});await visibleDialog(rotated,'.in5-nf',390,300);await rotated.close();count++;console.log('PASS: live orientation changes and short keyboard viewport');
 console.log(`${count}/${count} responsive checks PASS`);
}finally{await browser.close()}
