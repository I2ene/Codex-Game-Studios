"""Exercise installed v1.3 helpers in temporary synthetic consumers, not model/game quality.

Use --keep DIR (must not exist) for inspectable logs/screenshots. Node/npm, Git Bash
on Windows and Chrome/Edge/Chromium are required for the complete browser/Grow lane.
The framework itself never installs these tools. --base-source is an archived real
previous release for ownership upgrade checks. No real consumer is modified.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.game-studio/runtime'))
from installer import install

BRIEF = '''# Game Brief: Signal Garden

## In your words
Move the square and count distance.

**Pitch:** A deterministic movement fixture for framework verification.
**Genre:** movement sandbox (synthetic, not a quality claim).
**Controls:** Enter to start, arrow keys to move.
**Core loop:** Move and observe distance.
**Goal & fail state:** Observe motion; no claim of a finished game.
**Look and references:** Cyan square on a dark background.
**First minute:** Start and move to the right.
**Challenge:** Stay within the playfield.

## Features
- [x] Move the square.
- [x] Count distance.
- [ ] Add a bonus marker.

## Your systems
- Movement: in the slice.

## Keep
- Preserve movement and volume. pins: volume 0.4

## Avoid
- No network calls.

## Out of scope
- Online play: needs a server.

## Build order
Movement, then distance, then optional bonus marker.
'''

GAME = '''<!doctype html>
<!-- PROTOTYPE - NOT FOR PRODUCTION -->
<!-- Question: Does the installed browser and replay path retain movement? -->
<!-- Date: fixture -->
<html lang="en"><head><meta charset="utf-8"><title>Signal Garden</title>
<style>html,body{margin:0;background:#101827;color:#fff;font-family:sans-serif}canvas{display:block;width:100vw;height:100vh}</style></head><body>
<canvas id="game" width="1280" height="720"></canvas>
<script src="config.js"></script>
<script>
'use strict';
const params = new URLSearchParams(location.search);
const visit=Number(localStorage.getItem('fixture-visit')||0)+1;
localStorage.setItem('fixture-visit',String(visit));console.log('fixture-visit:'+visit);
const config = window.CONFIG;
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const clock = window.GAME_CLOCK || {now: () => performance.now()/1000};
const keys = new Set();
let scene = params.get('scene') || 'title';
let state = {x:100,y:360,score:0,t:0};
function clamp(x, low, high) { return Math.max(low, Math.min(high,x)); }
function press(key) { if(key === 'Enter') scene = 'play'; }
function hold(key,on) { if(on) keys.add(key); else keys.delete(key); }
function update() {
 if(scene !== 'play') return;
 const dx = Number(keys.has('ArrowRight'))-Number(keys.has('ArrowLeft'));
 const dy = Number(keys.has('ArrowDown'))-Number(keys.has('ArrowUp'));
 const before = state.x;
 state.x = clamp(state.x + dx*config.speed.value/60, 20, 1230);
 state.y = clamp(state.y + dy*config.speed.value/60, 80, 650);
 state.score += Math.abs(state.x-before); state.t += 1/60;
}
function draw() {
 ctx.fillStyle='#101827';ctx.fillRect(0,0,1280,720);
 ctx.fillStyle='#edf5ff';ctx.font='32px sans-serif';ctx.fillText('Signal Garden',40,48);
 ctx.font='24px sans-serif';ctx.fillText(scene==='title'?'Enter to start · Arrows to move':'Distance '+Math.round(state.score),40,95);
 ctx.fillStyle='#4cd9f3';ctx.fillRect(state.x,state.y,40,40);
 if(scene==='figures'){ctx.fillStyle='#edf5ff';ctx.fillText('Player',80,440);}
}
function step(n=1,render=true) { for(let i=0;i<n;i++) update(); if(render) draw(); }
window.game = {get scene(){return scene;},get state(){return state;},press,hold,step,events:[]};
addEventListener('keydown',e=>{press(e.code);hold(e.code,true);e.preventDefault();});
addEventListener('keyup',e=>hold(e.code,false));
let last=clock.now(),acc=0;
function frame(){const now=clock.now();acc+=Math.min(now-last,.25);last=now;while(acc>=1/60){step(1,false);acc-=1/60;}draw();requestAnimationFrame(frame);}
draw();if(params.get('manual')!=='1')requestAnimationFrame(frame);
</script>
</body></html>
'''


def digest_tree(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def exercise(source, directory, bash, npm, base_source=None):
    directory = Path(directory).resolve()
    if directory.exists():
        raise ValueError('--keep must name a new temporary fixture directory')
    directory.mkdir(parents=True)
    consumer = directory/'consumer'
    logs = directory/'logs';logs.mkdir()
    evidence = []
    env = os.environ.copy();env['GAME_STUDIO_PYTHON']=sys.executable
    env['PAGE_SHOT_BROWSER'] = env.get('PAGE_SHOT_BROWSER','')
    def command(label, argv, expected=(0,), cwd=consumer, timeout=240):
        result=subprocess.run([str(x) for x in argv],cwd=cwd,env=env,stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',timeout=timeout)
        (logs/(label+'.txt')).write_text(result.stdout,encoding='utf-8')
        evidence.append({'step':label,'exit':result.returncode,'expected':list(expected)})
        if result.returncode not in expected:
            raise RuntimeError(label+' failed: '+str(result.returncode)+'\n'+result.stdout[-3500:])
        return result.stdout
    install(source,consumer)
    def shell(label,name,*args,expected=(0,)):
        return command(label,[bash,consumer/'.game-studio/scripts'/name,*args,'--root',consumer],expected)
    def write(rel,text):
        p=consumer/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')
    def git(label,*args):
        return command(label,['git','-c','user.name=Framework Fixture','-c','user.email=fixture@example.invalid',*args])
    write('.gitignore','.game-studio/\n.agents/\n.codex/\nnode_modules/\ndist/\ndist-single/\nproduction/qa/evidence/\n')
    write('design/game-brief.md',BRIEF)
    git('git-init','init','-q')
    shell('one-shot-new','one-shot-new.sh','signal-garden','--title','Signal Garden')
    write('prototypes/signal-garden/index.html',GAME)
    write('prototypes/signal-garden/config.js','window.CONFIG = {\n seed:1,\n volume:{value:0.4,min:0,max:1,step:0.1},\n speed:{value:200,min:100,max:300,step:10},\n};\n')
    saved_browser=env.get('PAGE_SHOT_BROWSER','')
    env['PAGE_SHOT_BROWSER']=str(directory/'missing-browser')
    absent=shell('browser-absent','page-shot.sh','prototypes/signal-garden/index.html','production/qa/evidence/absent.png',expected=(3,))
    assert 'not_assessed' in absent
    env['PAGE_SHOT_BROWSER']=saved_browser
    first=shell('profile-first','page-shot.sh','prototypes/signal-garden/index.html','production/qa/evidence/profile-1.png','--profile','production/qa/evidence/browser-profile','--wait','100')
    second=shell('profile-second','page-shot.sh','prototypes/signal-garden/index.html','production/qa/evidence/profile-2.png','--profile','production/qa/evidence/browser-profile','--wait','100')
    assert 'fixture-visit:1' in first and 'fixture-visit:2' in second
    shell('keep-read-only','one-shot-check.sh','prototypes/signal-garden','--keep')
    shell('initial-check','one-shot-check.sh','prototypes/signal-garden','--keys','Enter ArrowRight:1')
    shell('figures','page-shot.sh','prototypes/signal-garden/index.html','prototypes/signal-garden/evidence/figures.png','--query','scene=figures','--wait','100')
    # The fixture is authored by this verification tool. Visual assessment is separate.
    write('prototypes/signal-garden/.user-note.txt','Preserve this hand edit.\n')
    shell('tune','one-shot-tune.sh','prototypes/signal-garden','speed 200 -> 220','--said','--why','Fixture requests quicker movement.')
    shell('iterate-check','one-shot-run.sh','prototypes/signal-garden','prototypes/signal-garden/evidence/iteration.png','--log','Enter ArrowRight:1','--limit','30')
    shell('share','one-shot-share.sh','prototypes/signal-garden')
    assert (consumer/'prototypes/signal-garden/.user-note.txt').read_text()=='Preserve this hand edit.\n'
    assert not (consumer/'prototypes/signal-garden/dist/brief.md').exists()
    assert not (consumer/'prototypes/signal-garden/dist/.user-note.txt').exists()
    git('baseline-add','add','--','prototypes/signal-garden','design/game-brief.md','.gitignore','project.yaml','AGENTS.md')
    git('baseline-commit','commit','-qm','one-shot fixture baseline')
    git('baseline-tag','tag','one-shot/signal-garden')
    baseline=digest_tree(consumer/'prototypes/signal-garden')
    shell('grow-guard','one-shot-grow.sh','guard','signal-garden')
    shell('grow-reference','one-shot-grow.sh','replay','signal-garden','--as','reference','--stop','180','--log','Enter ArrowRight:1')
    shell('grow-copy','one-shot-grow.sh','copy','signal-garden')
    command('npm-ci',[*npm,'ci','--no-audit','--no-fund'],timeout=600)
    command('grow-build-copy',[*npm,'run','build:single'])
    replay=shell('grow-copy-replay','one-shot-grow.sh','replay','signal-garden','--as','copy')
    assert 'match\tyes' in replay,replay
    # Actual TypeScript conversion, preserving the copied drawing/input behavior.
    p=consumer/'src/main.js';code=p.read_text(encoding='utf-8')
    code=code.replace("import './config.js';","import config from '../data/config.json';\nimport { clamp } from './game/rules';")
    code=code.replace('const config = window.CONFIG;','')
    code=code.replace("const canvas = document.getElementById('game');","const canvas = document.getElementById('game') as HTMLCanvasElement;")
    code=code.replace("const ctx = canvas.getContext('2d');","const ctx = canvas.getContext('2d')!;")
    code=code.replace('const keys = new Set();','const keys = new Set<string>();')
    code=code.replace('function clamp(x, low, high) { return Math.max(low, Math.min(high,x)); }','')
    code=code.replace('function press(key)','function press(key: string)').replace('function hold(key,on)','function hold(key: string,on: boolean)')
    code=code.replace('window.GAME_CLOCK','(window as any).GAME_CLOCK').replace('window.game =','(window as any).game =')
    write('src/main.ts',code);p.unlink()
    page=(consumer/'index.html').read_text();write('index.html',page.replace('./src/main.js','./src/main.ts'))
    write('src/game/rules.ts','export function clamp(x:number,low:number,high:number):number{return Math.max(low,Math.min(high,x));}\n')
    write('tests/unit/rules.test.ts',"import { expect,test } from 'vitest';\nimport { clamp } from '../../src/game/rules';\ntest('bounds movement at both edges',()=>{expect(clamp(-3,0,10)).toBe(0);expect(clamp(14,0,10)).toBe(10);expect(clamp(4,0,10)).toBe(4);});\n")
    write('tests/integration/boot.spec.ts',"import {test,expect} from '@playwright/test';\nimport {pathToFileURL} from 'node:url';import {resolve} from 'node:path';\ntest('@boot accepts input and preserves sampled movement',async({page})=>{await page.goto(pathToFileURL(resolve('dist-single/index.html')).href+'?manual=1');await page.evaluate(()=>{const g=(window as any).game;g.press('Enter');g.hold('ArrowRight',true);g.step(60);});expect(await page.evaluate(()=>(window as any).game.state.x)).toBeCloseTo(320,5);});\n")
    command('grow-unit',[*npm,'run','test:unit'])
    command('grow-build-typescript',[*npm,'run','build:single'])
    replay=shell('grow-typescript-replay','one-shot-grow.sh','replay','signal-garden','--as','typescript')
    assert 'match\tyes' in replay,replay
    command('grow-smoke',[*npm,'run','smoke'])
    shell('grow-record','one-shot-grow.sh','record','signal-garden')
    # A later feature produces a visible change that is accepted explicitly in this fixture.
    code=(consumer/'src/main.ts').read_text().replace("ctx.fillStyle='#4cd9f3';","ctx.fillStyle='#70edb7';")
    write('src/main.ts',code)
    command('feature-build',[*npm,'run','build:single'])
    changed=shell('feature-replay','one-shot-grow.sh','replay','signal-garden','--as','story')
    assert 'match\tno' in changed,changed
    shell('feature-accept','one-shot-grow.sh','accept','signal-garden')
    command('feature-smoke',[*npm,'run','smoke'])
    # Imported original source is an explicit fixture, never a real project.
    original=directory/'original';original.mkdir();(original/'index.html').write_text(GAME,encoding='utf-8');(original/'config.js').write_bytes((consumer/'prototypes/signal-garden/config.js').read_bytes())
    original_hash=digest_tree(original)
    shell('import-preview','door-in.sh',original,'--dry-run')
    shell('import-copy','door-in.sh',original,'--name','imported')
    assert digest_tree(original)==original_hash
    write('production/epics/fixture/story-3-bonus.md','# Bonus\n\nStatus: Ready\nRequirement: Brief MVP feature 3\n')
    shell('cut-read','cut-read.sh')
    cut=shell('cut-apply','cut-apply.sh','--brief','design/game-brief.md','--cut','3','Optional fixture scope cut')
    assert 'cut:' in (consumer/'design/game-brief.md').read_text()
    assert 'story\tblocked' in cut,cut
    assert 'BLOCKED: cut by' in (consumer/'production/epics/fixture/story-3-bonus.md').read_text()
    shell('cut-restore','cut-apply.sh','--brief','design/game-brief.md','--back','Add a bonus marker.','not_yet')
    restored=(consumer/'production/epics/fixture/story-3-bonus.md').read_text()
    assert 'Brief MVP feature 3' in restored and 'Status: Ready' in restored
    assert digest_tree(consumer/'prototypes/signal-garden')==baseline,'Grow mutated original one-shot'
    # Real nondeterministic state makes exact replay unassessed, never a sampled pass.
    shell('nonrepeat-new','one-shot-new.sh','nonrepeat','--title','Nonrepeat fixture')
    write('prototypes/nonrepeat/index.html',GAME.replace('score:0,t:0','score:0,t:0,nonce:crypto.getRandomValues(new Uint32Array(1))[0]'))
    write('prototypes/nonrepeat/config.js',(consumer/'prototypes/signal-garden/config.js').read_text())
    nonrepeat=shell('nonrepeat-reference','one-shot-grow.sh','replay','nonrepeat','--as','reference','--stop','180','--log','Enter ArrowRight:1')
    assert 'exact\tno' in nonrepeat and 'errors\t0' in nonrepeat
    unknown=shell('nonrepeat-copy','one-shot-grow.sh','replay','nonrepeat','--as','copy')
    assert 'match\tnot_assessed' in unknown
    recovered=command('recover',[sys.executable,consumer/'.game-studio/runtime/studio.py','recover','--root',consumer])
    assert install(source,consumer)['write']==[]
    if base_source:
        upgrade=directory/'upgrade';install(base_source,upgrade)
        for rel,text in {'AGENTS.md':(upgrade/'AGENTS.md').read_text()+'\nUser instructions.\n','project.yaml':'schema_version: 1\nengine: {name: Godot, version: "4.7"}\ncode_root: scripts\nfeatures: {session_state: on}\n','project.local.yaml':'modes: {automation: guided}\n','.game-studio/context.json':'{"checkpoint":"workbench/custom.md","records":[]}\n','workbench/custom.md':'User checkpoint\n','.agents/skills/user-example/SKILL.md':'User skill\n','workbench/notes.md':'User workbench\n'}.items():
            p=upgrade/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
        protected={rel:(upgrade/rel).read_bytes() for rel in ['project.yaml','project.local.yaml','.game-studio/context.json','workbench/custom.md','.agents/skills/user-example/SKILL.md','workbench/notes.md']}
        install(source,upgrade,dry_run=True);install(source,upgrade)
        assert all((upgrade/rel).read_bytes()==data for rel,data in protected.items())
        assert 'User instructions.' in (upgrade/'AGENTS.md').read_text()
        assert install(source,upgrade)['write']==[]
        command('upgrade-recover',[sys.executable,upgrade/'.game-studio/runtime/studio.py','recover','--root',upgrade],cwd=upgrade)
        edited=upgrade/'.agents/skills/gs-start/SKILL.md';edited.write_bytes(edited.read_bytes()+b'\nConsumer edit\n')
        before=digest_tree(upgrade)
        try:install(source,upgrade)
        except ValueError:pass
        else:raise AssertionError('Edited managed file was overwritten')
        assert digest_tree(upgrade)==before
        evidence.append({'step':'real-previous-release-upgrade-and-conflict','status':'EXECUTED'})
    report={'status':'EXECUTED','steps':evidence,'screenshots':[str(p.relative_to(directory)) for p in directory.rglob('*.png')],
            'not_assessed':['All model scenario behavior','Human playtest/fun','Real engine export/build','Trusted host callback delivery'],
            'boundary':'Installed helper and authored synthetic fixture execution; visual inspection is recorded separately.'}
    (directory/'result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT)
    parser.add_argument('--base-source',type=Path)
    parser.add_argument('--keep',type=Path)
    parser.add_argument('--bash',default=shutil.which('bash'))
    parser.add_argument('--npm-cli',type=Path,help='Isolated official npm-cli.js, invoked with Node')
    args=parser.parse_args()
    npm=[shutil.which('node'),args.npm_cli.resolve()] if args.npm_cli else [shutil.which('npm')]
    if not args.bash or not all(npm):parser.error('Explicit Bash and npm/Node tools are required')
    if args.keep:result=exercise(args.source.resolve(),args.keep,args.bash,npm,args.base_source.resolve() if args.base_source else None)
    else:
        with tempfile.TemporaryDirectory(prefix='studio-v13-') as t:
            result=exercise(args.source,Path(t)/'exercise',args.bash,npm,args.base_source)
    print(json.dumps(result,indent=2))
