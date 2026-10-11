import {createRequire} from 'node:module';
import os from 'node:os';
const require=createRequire((process.env.WORKSHOP_UI_TOOLS || os.homedir()+'/scratch/rumoca-workshop/browser')+'/package.json');
const {chromium}=require('playwright-core');
import fs from 'node:fs';
import assert from 'node:assert/strict';
const [root]=process.argv.slice(2);
const source=fs.readFileSync(root+'/browser/Quadrotor_browser.mo','utf8');
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH,args:['--no-sandbox'],headless:true});
const page=await browser.newPage({viewport:{width:1600,height:1000}});
await page.goto('https://rumoca.cognipilot.org/playground/',{waitUntil:'domcontentloaded',timeout:60000});
await page.waitForTimeout(3000);
const frame=page.frames().find(f=>f.url().includes('/app/index.html'));
await frame.waitForFunction(()=>window.monaco?.editor?.getModels().length>0,{timeout:30000});
const runs=[];
for(const k of [0,0.08]){
 const code=k===0?source:source.replace('= 0.0 "EXERCISE','= 0.08 "EXERCISE');
 await frame.evaluate(s=>window.monaco.editor.getModels()[0].setValue(s),code);
 await page.waitForTimeout(1000);
 await frame.getByText(/Compile: Balanced/).waitFor({timeout:30000});
 await frame.locator('#editorSimSettingsBtn').click();
 let settings;
 for(let attempt=0;attempt<50&&!settings;attempt++){
  settings=page.frames().find(f=>f.url().startsWith('about:'));
  if(!settings) await page.waitForTimeout(100);
 }
 assert.ok(settings,'Visible simulation settings frame must open: '+page.frames().map(f=>f.url()).join(', '));
 await settings.locator('#modelSelect').selectOption({label:'BrowserFlight'});
 await frame.locator('#simulationSettingsCloseBtn').click();
 const started=Date.now();
 await frame.locator('#editorRunBtn').click();
 await frame.getByText(/\d+ pts, \d+ vars/).last().waitFor({timeout:30000});
 await page.waitForTimeout(1200);
 const text=await frame.locator('body').innerText();
 assert.ok(text.includes('BrowserFlight Results'));
 assert.ok(text.includes('Compile: Balanced'));
 runs.push({k_quad:k,elapsed_seconds:(Date.now()-started)/1000,summary:text.match(/\d+ pts, \d+ vars \([^)]*\)/)?.[0],runtime:text.match(/Rumoca v[^\n]+/)?.[0]});
 await page.screenshot({path:root+`/slides/assets/browser-drag-${k===0?'linear':'quadratic'}.png`,fullPage:true});
}
// Exercise invalid syntax and observe browser LSP markers, then restore.
await frame.evaluate(()=>window.monaco.editor.getModels()[0].setValue('model Broken\n Real x = ;\nend Broken;'));
await frame.waitForFunction(()=>window.monaco.editor.getModelMarkers({owner:'rumoca'}).length>0,{timeout:10000});
const markers=await frame.evaluate(()=>window.monaco.editor.getModelMarkers({owner:'rumoca'}).map(m=>({message:m.message,startLineNumber:m.startLineNumber})));
fs.writeFileSync(root+'/verification/browser.json',JSON.stringify({tested_at:new Date().toISOString(),url:page.url(),frame_url:frame.url(),browser:'Chromium',source:'browser/Quadrotor_browser.mo',runs,syntax_error_markers:markers,scope:'Actual public playground UI; pasted model, used visible gear/settings model selector, selected BrowserFlight, clicked Play at both drag settings; screenshot and plot produced. Python backends execute separately.'},null,2)+'\n');
await browser.close();
console.log(runs);
