import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const html=fs.readFileSync(path.join(root,'catgpt.html'),'utf8');
vm.runInThisContext(html.match(/<script id="gameCore">([\s\S]*?)<\/script>/)[1]);
const G=globalThis.CatGame;
const act=(s,e)=>G.reduce(s,{...e,r:s.events.length});
function foodStart(){let s=act(G.fresh(),{type:'start'});let guard=0;while(s.node!=='c3_food'){assert.ok(++guard<80);if(s.pending)s=act(s,{type:'advance'});else if(G.STORY[s.node].game)s=act(s,{type:'skip',game:G.STORY[s.node].game});else{const c=G.choices(s)[0];s=act(s,{type:'choose',node:s.node,id:c.id});}}return s;}
function serve(){let s=foodStart();for(const e of [{type:'food_pick',group:'menu',id:'house'},{type:'food_pick',group:'bowl',id:'blue'},{type:'food_scoop',delta:1},{type:'food_scoop',delta:1},{type:'food_water'},{type:'food_serve'}])s=act(s,e);return s;}
test('New edition uses a separate save key and explicitly rejects format 3',()=>{assert.equal(G.CONFIG.schema,4);assert.equal(G.CONFIG.storageKey,'catgpt.game.v4');assert.throws(()=>G.unpack(JSON.stringify({format:'CATGPT_TED_GAME',schema:3,events:[],endings:[]})),/Format 4/);});
test('Fast tour reaches the office after three answers and retains all intro photos',()=>{let s=act(G.fresh(),{type:'start'});for(const id of ['job','line','go'])s=act(s,{type:'choose',node:s.node,id});assert.equal(s.pending.next,'c2_office');assert.deepEqual([...s.photos].sort(),['judge','director','alert','tilt'].sort());});
for(const brand of ['Chefedition','Napf Royal','Mousse de Miau'])test(`Brand ${brand}: validated choice, exact reply, export/replay`,()=>{let s=serve();s=act(s,{type:'food_brand',id:brand});s=act(s,{type:'food_finish',method:'label'});assert.equal(s.games.food.brand,brand);assert.ok(s.history.findLast(h=>h.kind==='reply').text.join(' ').includes(brand));assert.deepEqual(G.unpack(JSON.stringify(G.pack(s))).state,s);});
test('Branding cannot replace food preparation or inject arbitrary strings',()=>{assert.throws(()=>act(foodStart(),{type:'food_brand',id:'Napf Royal'}));assert.throws(()=>act(serve(),{type:'food_brand',id:'<script>alert(1)</script>'}));});
test('Embedded assets are generated from committed source without remote dependencies',()=>{for(const [file,marker,end]of [['mobile.css','<style id="mobileStyle">','</style>'],['audio.js','<script id="catAudio">','</script>'],['story.js','/* BEGIN STORY_EDITION */','/* END STORY_EDITION */'],['scene-ui.js','/* BEGIN SCENE_EDITION */','/* END SCENE_EDITION */']]){const source=fs.readFileSync(path.join(root,'src',file),'utf8').trim();const a=html.indexOf(marker)+marker.length,b=html.indexOf(end,a);assert.equal(html.slice(a,b).trim(),source,file);}});
test('All executable inline scripts parse',()=>{for(const m of html.matchAll(/<script id="([^"]+)">([\s\S]*?)<\/script>/g))new vm.Script(m[2],{filename:m[1]});});
