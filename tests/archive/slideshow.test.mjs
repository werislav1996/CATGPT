import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const html=fs.readFileSync(path.join(ROOT,'catgpt.html'),'utf8');
vm.runInThisContext(html.match(/<script id="gameCore">([\s\S]*?)<\/script>/)[1]);
const G=globalThis.CatGame;
const assets=JSON.parse(html.match(/<script type="application\/json" id="catAssets">([\s\S]*?)<\/script>/)[1]);
const newScenes={edge:'c4_edge',wellness:'c4_benefits',upsidedown:'c3_pivot',portfolio:'c2_portfolio',security:'c4_security',remoteit:'c2_remoteit',solar:'c3_solar',marketshare:'c3_market',walkover:'c5_walkover',desk:'c2_desk',approval:'c4_approval'};
const apply=(s,e)=>G.reduce(s,{...e,r:s.events.length});
function walk(overrides={}){
 let s=apply(G.fresh(),{type:'start'}),guard=0;
 while(!s.complete){assert.ok(++guard<90);const node=G.STORY[s.node];if(node.game){s=apply(s,{type:'skip',game:node.game});continue;}const c=overrides[s.node]||G.choices(s)[0].id;s=apply(s,{type:'choose',node:s.node,id:c});}
 return s;
}
test('All 68 scenes have an explicit approved photo instead of a random mood fallback',()=>{for(const n of Object.values(G.STORY))assert.ok(assets.photos.some(p=>p.id===n.photo),n.id);});
for(const [photo,scene] of Object.entries(newScenes))test(`New photo ${photo} has its own selectable story scene ${scene}`,()=>{const p=assets.photos.find(p=>p.id===photo);assert.ok(p&&p.isNew);assert.equal(G.STORY[scene].photo,photo);assert.ok(G.STORY[scene].choices.length>=2);assert.ok(G.PHOTO_STORY[photo].note.length>80);});
test('All eleven new photographs occur even when every minigame is skipped',()=>{const s=walk();for(const id of Object.keys(newScenes))assert.ok(s.photos.includes(id),id);assert.equal(s.photos.length,33);});
test('Respecting the IT team changes remote-work dialogue and the later crisis',()=>{const s=walk({c2_portfolio:'union'});assert.ok(s.flags.teamRespect);assert.match(s.history.find(h=>h.id==='c2_remoteit').text.join(' '),/erste Pause/);assert.match(s.history.find(h=>h.id==='c4_crisis').text.join(' '),/Mitarbeitervertretung/);assert.match(s.history.find(h=>h.id==='c5_epilogue').text.join(' '),/Gewerkschaft/);});
test('The ball may remain remote and this decision survives into the epilogue',()=>{const s=walk({c2_remoteit:'remote'});assert.ok(s.flags.remoteAllowed);assert.match(s.history.find(h=>h.id==='c5_epilogue').text.join(' '),/IT bleibt remote/);});
test('Requesting desk space is remembered on the final presentation slide',()=>{const s=walk({c2_desk:'space'});assert.ok(s.flags.workspace);assert.match(s.history.find(h=>h.id==='c5_review').text.join(' '),/vom Arbeitsplatz/);});
test('Protecting a human seat has a later home-office callback',()=>{const s=walk({c3_market:'reserve'});assert.ok(s.flags.seatProtected);assert.match(s.history.find(h=>h.id==='c5_home').text.join(' '),/Sitzplatz für Menschen/);});
test('A staged paw stamp never forges the formal recognition document',()=>{const s=walk({c4_request:'friendly',c4_friendly:'title',c4_approval:'paw'});assert.ok(s.flags.pawStamp);assert.ok(!s.inventory.includes('credit'));});
test('Photo-story saves use a separate schema and storage key',()=>{assert.equal(G.CONFIG.schema,2);assert.equal(G.CONFIG.storageKey,'catgpt.game.v2');assert.throws(()=>G.unpack(JSON.stringify({format:'CATGPT_TED_GAME',schema:1,build:'0.3.0',events:[],endings:[]})),/0.3/);});
test('The extended story still replays exactly and reaches every chapter checkpoint',()=>{const s=walk({c2_portfolio:'union',c2_desk:'space',c3_market:'reserve',c4_approval:'paw',c5_walkover:'stop'});const packed=G.pack(s);assert.deepEqual(G.unpack(JSON.stringify(packed)).state,s);for(let ch=1;ch<=5;ch++)assert.equal(G.checkpoint(s,ch).node,G.CHAPTERS[ch-1].start);});
test('All full-frame originals remain embedded alongside the presentation crops',()=>{assert.equal(assets.photos.filter(p=>p.sceneSrc).length,25);for(const p of assets.photos){assert.ok(p.src.startsWith('data:image/webp;base64,'));assert.ok(p.width>0&&p.height>0);if(p.sceneSrc){assert.ok(p.sceneSrc.startsWith('data:image/webp;base64,'));assert.ok(p.sceneWidth>0&&p.sceneHeight>0);}}});
test('Static entry points to the sole game file instead of duplicating 33 images',()=>{const index=fs.readFileSync(path.join(ROOT,'index.html'),'utf8');assert.ok(index.includes('url=./catgpt.html'));assert.ok(index.includes('href="./catgpt.html"'));assert.ok(index.length<2000);});
test('No automatic slideshow timer and no unknown-image requests',()=>{assert.ok(!/setInterval\(/.test(html));assert.ok(!/<img[^>]+src="https?:/.test(html));assert.ok(html.includes('CATGPT_SLIDESHOW'));});
