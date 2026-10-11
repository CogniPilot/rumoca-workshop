// Small public-UI rehearsal of the optional app gallery; no accounts/API keys.
import {createRequire} from 'node:module';
import os from 'node:os';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const require=createRequire((process.env.WORKSHOP_UI_TOOLS || os.homedir()+'/scratch/rumoca-workshop/browser')+'/package.json');
const {chromium}=require('playwright-core');
const root=process.argv[2];
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH,args:['--no-sandbox','--enable-unsafe-swiftshader'],headless:true});
async function check(name,action){
 if(process.argv[3]&&process.argv[3]!==name)return {name,status:'SKIP'};
 const page=await browser.newPage({viewport:{width:1600,height:1000}});
 const wasm=[],errors=[];const started=Date.now();
 page.on('response',r=>{if(r.url().includes('.wasm'))wasm.push({url:r.url(),status:r.status()});});
 page.on('pageerror',e=>errors.push(e.message));
 const result={name,url:`https://cognipilot.github.io/${name}/`,tested_at:new Date().toISOString(),browser:'Chromium, software WebGL fallback'};
 try{
  await page.goto(result.url,{waitUntil:'domcontentloaded',timeout:60000});
  Object.assign(result,await action(page));
  assert.equal(errors.length,0,errors.join('\n'));
  result.status='PASS';
 }catch(error){result.status='FAIL';result.failure=error.message;}
 result.elapsed_seconds=(Date.now()-started)/1000;result.wasm=wasm;result.page_errors=errors;
 await page.evaluate(()=>window.scrollTo(0,0));
 await page.screenshot({path:`${root}/slides/assets/app-${name}.png`,fullPage:name!=='rumoca_fixed_wing'});
 fs.writeFileSync(`${root}/verification/app-${name}.json`,JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify(result));await page.close();return result;
}
const results=await Promise.all([
 check('rumoca_fixed_wing',async page=>{
  await page.waitForFunction(()=>document.querySelector('#run-meta')?.textContent.includes('schema'),{timeout:60000});
  await page.locator('[data-playback-view="autopilot"]').click();
  await page.locator('#autopilot-overlay-start').click();
  await page.waitForFunction(()=>/running lockstep/.test(document.querySelector('#modelica-flight-status').textContent),{timeout:120000});
  await page.waitForFunction(()=>/sim [1-9]/.test(document.querySelector('#waypoint-readout').textContent),{timeout:30000});
  const status=await page.locator('#modelica-flight-status').innerText();
  const waypoint=await page.locator('#waypoint-readout').innerText();
  await page.locator('[data-autopilot-rate="20"]').click();
  await page.locator('#autopilot-overlay-start').click();
  await page.waitForFunction(()=>/running lockstep at 20 Hz/.test(document.querySelector('#modelica-flight-status').textContent),{timeout:120000});
  await page.waitForFunction(()=>/20 Hz/.test(document.querySelector('#waypoint-readout').textContent)&&Number(document.querySelector('#waypoint-readout').textContent.match(/sim ([\d.]+) s/)?.[1])>.2,{timeout:30000});
  await page.locator('#autopilot-pause').click();
  return {steps:['Autopilot tab','Start sim','compiled Modelica controller + plant','simulation advances','change controller rate 50 → 20 Hz','Start sim again to recompile at new rate','simulation advances at 20 Hz','Pause'],status_text:status,waypoint_before:waypoint,waypoint_after:await page.locator('#waypoint-readout').innerText(),scope:'Public default autopilot UI execution only; no validation of real aircraft or arbitrary edits.'};
 }),
 check('slam_web',async page=>{
  await page.waitForFunction(()=>document.querySelector('#run')&&!document.querySelector('#run').disabled,{timeout:90000});
  await page.locator('#run').click();
  await page.waitForFunction(()=>/t = (?!0\.00)\d/.test(document.body.innerText),{timeout:60000});
  await page.waitForTimeout(3000);
  await page.locator('#run').click();
  const before=(await page.locator('body').innerText()).match(/t = [\d.]+ s/)?.[0];
  await page.locator('#run-model').selectOption('SLAM.Examples.ResponsiveInertial');
  await page.waitForFunction(()=>document.querySelector('#run')&&!document.querySelector('#run').disabled,{timeout:90000});
  await page.locator('#run').click();
  await page.waitForFunction(()=>/t = (?!0\.00)\d/.test(document.body.innerText),{timeout:60000});
  await page.waitForTimeout(3000);
  await page.locator('#run').click();
  const body=await page.locator('body').innerText();
  assert.ok(body.includes('integration pending')||body.includes('SLAM pending'));
  return {steps:['Run default InertialOnly','time advances; pause','select ResponsiveInertial','Run; time advances; pause'],default_time:before,variant_time:body.match(/t = [\d.]+ s/)?.[0],model:await page.locator('#run-model').inputValue(),rendering_warning:body.match(/Software rendering detected:[^\n]+/)?.[0],scope:'Inertial baseline + variant, camera/depth scene; full connected visual SLAM is pending. No mapping/loop-closure or deployment claim.'};
 }),
 check('mocap_sysid',async page=>{
  await page.waitForFunction(()=>document.querySelector('#run-meta')?.textContent.includes('schema'),{timeout:60000});
  await page.locator('#scenario-select').selectOption('aircraft_6dof_open_loop');
  await page.getByRole('button',{name:'Time Histories',exact:true}).click();
  await page.waitForTimeout(1000);
  const history=await page.locator('body').innerText();
  await page.getByRole('button',{name:'Data Splits',exact:true}).click();
  await page.waitForTimeout(1000);
  const splits=await page.locator('body').innerText();
  await page.getByRole('button',{name:'Models',exact:true}).click();
  await page.locator('#model-inspect-select').selectOption({label:'LinearSS'});
  await page.waitForTimeout(1000);
  const models=await page.locator('body').innerText();
  assert.ok(history.includes('Method Comparisons')&&splits.includes('validation')&&models.includes('LinearSS'));
  return {steps:['choose synthetic open-loop dataset','Time Histories','Data Splits','Models → LinearSS'],dataset:await page.locator('#scenario-select').inputValue(),run_metadata:await page.locator('#run-meta').innerText(),models_status:await page.locator('#models-status').innerText(),scope:'Explore stored benchmark traces/splits/model information. Training and benchmark metrics were not regenerated or independently audited here.'};
 })
]);
await browser.close();
if(results.some(r=>r.status==='FAIL'))process.exitCode=1;
