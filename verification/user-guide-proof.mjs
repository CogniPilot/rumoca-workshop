// Rehearse the deployed guide's embedded editor and NACA visualization.
// Software WebGPU is used for portability; this is a UI check, not a CFD audit.
import {createRequire} from 'node:module';
import os from 'node:os';
import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const require=createRequire((process.env.WORKSHOP_UI_TOOLS || os.homedir()+'/scratch/rumoca-workshop/browser')+'/package.json');
const {chromium}=require('playwright-core');
const root=process.argv[2];
assert.ok(root,'Pass repository root as first argument');
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH,
 args:['--no-sandbox','--enable-unsafe-swiftshader','--enable-unsafe-webgpu','--use-angle=swiftshader','--enable-features=Vulkan'],headless:true});
const page=await browser.newPage({viewport:{width:1600,height:1000}});
const errors=[],wasm=[];
page.on('pageerror',e=>errors.push(e.message));
page.on('response',r=>{if(r.url().includes('.wasm'))wasm.push({url:r.url(),status:r.status()});});
const url='https://cognipilot.github.io/rumoca/user-guide/language/arrays-pde.html#2-d-navierstokes-flow-over-a-naca-2412-airfoil';
const started=Date.now();
try {
 await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
 await page.waitForFunction(()=>window.monaco?.editor?.getModels().some(m=>m.getValue().includes('model AirfoilFlow')),null,{timeout:90000});
 const original=await page.evaluate(()=>window.monaco.editor.getModels().find(m=>m.getValue().includes('model AirfoilFlow')).getValue());
 assert.ok(original.includes('StopTime = 30'));
 await page.evaluate(()=>{const m=window.monaco.editor.getModels().find(m=>m.getValue().includes('model AirfoilFlow'));m.setValue(m.getValue().replace('StopTime = 30','StopTime = 2'));});
 const widget=page.locator('.rumoca-live').filter({hasText:'model AirfoilFlow'});
 await widget.scrollIntoViewIfNeeded();
 const adapter=await page.evaluate(async()=>!!await navigator.gpu?.requestAdapter());
 assert.ok(adapter,'This receipt requires a software WebGPU adapter');
 await widget.getByRole('button',{name:'▶ Simulate',exact:true}).click();
 for(let i=0;i<180;i++) {
  const text=await widget.locator('.rumoca-live-status').first().innerText();
  if(text.includes('21 points'))break;
  assert.ok(!/Failed|error/i.test(text),text);
  await page.waitForTimeout(1000);
 }
 const status=await widget.locator('.rumoca-live-status').first().innerText();
 assert.match(status,/wgsl-ode RK4 \(f32\).*t = 0…2 s/);
 const frame=widget.locator('input[type=range]').first();
 await frame.evaluate(e=>{e.value=e.max;e.dispatchEvent(new Event('input',{bubbles:true}));});
 await widget.locator('select').nth(1).selectOption({label:'Pressure'});
 await page.waitForTimeout(300);
 assert.match(await widget.innerText(),/t = 2\.0 s · Pressure/);
 await widget.locator('select').nth(1).selectOption({label:'Vorticity'});
 await widget.locator('.rumoca-live-output').scrollIntoViewIfNeeded();
 await page.waitForTimeout(500);
 const toolbar=await widget.locator('.rumoca-live-toolbar').boundingBox();
 await page.screenshot({path:`${root}/slides/assets/user-guide-naca.png`,
  clip:{x:toolbar.x,y:Math.max(0,toolbar.y),width:toolbar.width,height:Math.min(555,1000-Math.max(0,toolbar.y))}});
 assert.equal(errors.length,0,errors.join('\n'));
 const result={status:'PASS',url,tested_at:new Date().toISOString(),
  browser:'Chromium 150, software WebGPU (SwiftShader)',
  original_source_sha256:crypto.createHash('sha256').update(original).digest('hex'),
  source_edit:'StopTime = 30 → StopTime = 2; default NX=30, NY=18 unchanged',
  steps:['Open embedded Monaco editor','Shorten StopTime','Simulate on WebGPU','Select final frame','Switch Pressure → Vorticity'],
  status_text:status,elapsed_seconds:(Date.now()-started)/1000,wasm,page_errors:errors,
  scope:'Deployed guide UI and a short default-grid simulation. Artificial-compressibility, penalized coarse-grid teaching visualization; no aerodynamic-accuracy, stability, lift/drag or hardware-performance validation.'};
 fs.writeFileSync(`${root}/verification/user-guide.json`,JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify(result));
} finally {await browser.close();}
