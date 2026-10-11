import {createRequire} from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
const root=path.resolve(fileURLToPath(new URL('..',import.meta.url)));
const scratch=path.join(os.homedir(),'scratch','rumoca-workshop');
const require=createRequire(path.join(process.env.WORKSHOP_UI_TOOLS || path.join(scratch,'ui-tools'),'package.json'));
const {downloadAndUnzipVSCode,runTests,runVSCodeCommand}=require('@vscode/test-electron');
const target=process.env.WORKSHOP_VSIX_TARGET || `${process.platform==='win32'?'win32':process.platform==='darwin'?'darwin':'linux'}-${process.arch}`;
const dir=path.join(scratch,'editor',target);
for(const folder of ['harness','workspace','user/User','extensions','downloads'])fs.mkdirSync(path.join(dir,folder),{recursive:true});
fs.writeFileSync(path.join(dir,'harness/package.json'),JSON.stringify({name:'workshop-verifier',version:'1.0.0',publisher:'workshop',engines:{vscode:'^1.75.0'},main:'extension.js',activationEvents:['*']}));
fs.writeFileSync(path.join(dir,'harness/extension.js'),'exports.activate=()=>{};');
fs.writeFileSync(path.join(dir,'user/User/settings.json'),JSON.stringify({'update.mode':'none','extensions.autoUpdate':false,'workbench.startupEditor':'none','telemetry.telemetryLevel':'off'}));
const model=path.join(dir,'workspace/Quadrotor.mo');
fs.copyFileSync(path.join(root,'models/Quadrotor.mo'),model);
const name=`rumoca-modelica-${target}-0.10.2.vsix`;
const vsix=path.join(dir,'downloads',name);
if(!fs.existsSync(vsix)){
 const response=await fetch(`https://github.com/CogniPilot/rumoca/releases/download/v0.10.2/${name}`);
 if(!response.ok)throw Error(`VSIX download failed: ${response.status}`);
 fs.writeFileSync(vsix,Buffer.from(await response.arrayBuffer()));
}
const options={version:'1.119.0',cachePath:path.join(scratch,'vscode-downloads'),reuseMachineInstall:true};
const executable=process.env.VSCODE_PATH || await downloadAndUnzipVSCode(options);
await runVSCodeCommand(['--user-data-dir',path.join(dir,'user'),'--extensions-dir',path.join(dir,'extensions'),'--install-extension',vsix,'--force','--no-sandbox'],options);
const result=path.join(root,'verification',`vscode-${target}.json`);
const args=[path.join(dir,'workspace'),'--user-data-dir',path.join(dir,'user'),'--extensions-dir',path.join(dir,'extensions'),'--no-sandbox','--disable-gpu','--disable-workspace-trust'];
if(process.env.WORKSHOP_SCREENSHOT==='1')args.push('--remote-debugging-port=9237');
const running=runTests({...options,vscodeExecutablePath:executable,
 extensionDevelopmentPath:path.join(dir,'harness'),extensionTestsPath:path.join(root,'verification/vscode-test.cjs'),
 launchArgs:args,extensionTestsEnv:{...process.env,WORKSHOP_MODEL:model,WORKSHOP_RESULT:result}});
if(process.env.WORKSHOP_SCREENSHOT==='1'){
 const {chromium}=require('playwright-core');
 for(let i=0;i<400;i++){
  if(fs.existsSync(result)&&fs.statSync(result).mtimeMs>Date.now()-3000){
   const browser=await chromium.connectOverCDP('http://127.0.0.1:9237');
   for(const context of browser.contexts())for(const page of context.pages())
    if(page.url().includes('workbench'))await page.screenshot({path:path.join(root,'slides/assets/vscode-quadrotor.png')});
   await browser.close();break;
  }
  await new Promise(r=>setTimeout(r,100));
 }
}
await running;
console.log(fs.readFileSync(result,'utf8'));
