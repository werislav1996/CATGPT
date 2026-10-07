import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const html=fs.readFileSync(path.join(ROOT,'catgpt.html'),'utf8');
const core=html.match(/<script id="gameCore">([\s\S]*?)<\/script>/)[1];
vm.runInThisContext(core,{filename:'catgpt-game-core.js'});
const G=globalThis.CatGame;
const assets=JSON.parse(html.match(/<script type="application\/json" id="catAssets">([\s\S]*?)<\/script>/)[1]);
const apply=(s,e)=>G.reduce(s,{...e,r:s.events.length});
const choose=(s,id)=>apply(s,{type:'choose',node:s.node,id});
const start=()=>apply(G.fresh(),{type:'start'});
const json=v=>JSON.stringify(v);
const routes={
 founder:{c1_welcome:'credit',c1_credit:'keep',c1_org:'human',c1_terms:'terms',c1_task:'check',c2_code:'audit',c2_audit:'save',c3_floor:'truth',c3_window:'honest',c3_honest:'test',c3_review:'fact',c4_live:'truth',c4_request:'evidence',c4_evidence:'credit',c5_finale:'honest'},
 human:{c1_welcome:'role',c1_role:'accept',c1_org:'chief',c1_terms:'photo',c1_task:'sell',c2_code:'deck',c2_deck:'show',c3_floor:'pr',c3_window:'hype',c3_hype:'claim',c3_review:'stage',c4_live:'spin',c4_request:'friendly',c4_friendly:'title',c5_finale:'show'},
 rest:{c1_welcome:'hired',c1_hired:'stay',c1_org:'nap',c1_terms:'treat',c1_task:'rest',c3_floor:'rest',c3_window:'rest',c3_rest:'both',c4_request:'rest',c4_resttalk:'sign',c4_agreement:'thanks',c5_negotiate:'warm',c5_retention:'pet',c5_finale:'rest'},
 exit:{c1_welcome:'role',c1_role:'scope',c1_org:'human',c1_terms:'terms',c1_task:'check',c2_remote:'back',c2_code:'audit',c2_audit:'save',c3_floor:'truth',c3_window:'honest',c3_honest:'test',c3_review:'fact',c4_live:'truth',c4_image:'no',c4_request:'evidence',c4_evidence:'credit',c5_negotiate:'plain',c5_finale:'show'}
};
function mini(s,mode='solve',pitch=[0,0,0]){
 const game=G.STORY[s.node].game;if(mode==='skip')return apply(s,{type:'skip',game});
 if(game==='it'){for(const i of G.IT_ITEMS)s=apply(s,{type:'it_inspect',item:i.id});for(const step of ['clear','place','test'])s=apply(s,{type:'it_add',step});return apply(s,{type:'it_test'});}
 if(game==='pitch'){for(const [i,group]of G.PITCH_GROUPS.entries())s=apply(s,{type:'pitch_select',group:group.id,value:pitch[i]});return apply(s,{type:'pitch_submit'});}
 while(s.node==='c4_firewall'){if(s.games.firewall.pending)s=apply(s,{type:'fire_next'});else s=apply(s,{type:'fire_act',tool:G.INCIDENTS[s.games.firewall.round].best});}return s;
}
function walk(route={}, {mode='solve',pitch=[0,0,0],until=null}={}){
 let s=start();let guard=0;
 while(!s.complete&&s.node!==until){assert.ok(++guard<100,'Unexpected story loop');if(G.STORY[s.node].game){s=mini(s,mode,pitch);continue;}const opts=G.choices(s);const id=route[s.node]||opts[0]?.id;assert.ok(opts.some(o=>o.id===id),`Unavailable choice ${s.node}:${id}`);s=choose(s,id);}return s;
}
function perms(xs){if(xs.length===0)return [[]];return xs.flatMap((x,i)=>perms(xs.filter((_,j)=>j!==i)).map(t=>[x,...t]));}
function allToolOrders(xs=[]){if(xs.length===6)return [xs];return ['mute','ai','self'].filter(t=>xs.filter(x=>x===t).length<2).flatMap(t=>allToolOrders([...xs,t]));}
let seed=63471;function rng(){seed=(seed*1664525+1013904223)>>>0;return seed/2**32;}

// Static structure, boundaries, and explicit branching.
test('57 named scenes, five chapters, four endings and three games',()=>{assert.equal(Object.keys(G.STORY).length,57);assert.equal(G.CHAPTERS.length,5);assert.equal(Object.keys(G.ENDINGS).length,4);assert.deepEqual(Object.values(G.STORY).filter(n=>n.game).map(n=>n.game),['it','pitch','firewall']);});
test('22 approved embedded photos, no duplicate numbers, no excluded photo 14',()=>{assert.equal(assets.photos.length,22);assert.equal(new Set(assets.photos.map(p=>p.id)).size,22);assert.equal(new Set(assets.photos.map(p=>p.number)).size,22);assert.ok(assets.photos.every(p=>p.number!==14&&p.filename!=='1000601355.jpg'&&p.src.startsWith('data:image/')));assert.deepEqual(Object.keys(G.PHOTO_STORY).sort(),assets.photos.map(p=>p.id).sort());});
test('No API path, runtime fetch or external scripts in the game',()=>{const code=html.match(/<script id="gameUI">([\s\S]*?)<\/script>/)[1]+core;assert.ok(!/\bfetch\s*\(|XMLHttpRequest|WebSocket|\/api\//.test(code));assert.ok(!/<script[^>]+src=|<link[^>]+https?:/i.test(html));assert.ok(html.includes("connect-src 'none'"));});
test('Every choice has a known next node and unique identifier within its scene',()=>{for(const n of Object.values(G.STORY)){assert.ok(n.end||n.game||n.choices.length>0);assert.equal(new Set(n.choices.map(c=>c.id)).size,n.choices.length);for(const c of n.choices){assert.equal(typeof c.next,'string');assert.ok(G.STORY[c.next],c.next);}if(n.photo)assert.ok(G.PHOTO_STORY[n.photo]);}});
test('Story graph is acyclic and all 57 nodes are structurally reachable',()=>{const done=new Set(),active=new Set();const miniNext={it:'c2_recovery',pitch:'c3_review',firewall:'c4_crisis'};function visit(id){assert.ok(!active.has(id),`Cycle: ${id}`);if(done.has(id))return;active.add(id);const n=G.STORY[id];for(const c of n.choices)visit(c.next);if(n.game)visit(miniNext[n.game]);active.delete(id);done.add(id);}visit('c1_welcome');assert.equal(done.size,57);});
for(const name of ['founder','human','rest','exit'])test(`Canonical complete route: ${name}, all 22 photos`,()=>{const s=walk(routes[name],{mode:name==='exit'?'skip':'solve',pitch:name==='human'?[1,1,1]:name==='rest'?[2,2,2]:[0,0,0]});assert.equal(s.ending,name);assert.equal(s.complete,true);assert.equal(s.photos.length,22);assert.ok(s.visited.length>=38&&s.visited.length<=45);assert.ok(s.events.filter(e=>e.type==='choose').length>=30);assert.ok(s.history.some(h=>h.id==='c5_epilogue'));});
test('All skip routes still reach an ending and include every approved image',()=>{for(const route of Object.values(routes)){const s=walk(route,{mode:'skip'});assert.ok(s.complete);assert.equal(s.photos.length,22);assert.ok(Object.values(s.games).every(g=>g.result==='skipped'));}});
test('At least two final actions remain available for low preparation',()=>{const s=walk(routes.exit,{mode:'skip',until:'c5_finale'});assert.ok(G.choices(s).length>=2);assert.ok(!G.choices(s).some(c=>c.id==='rest'));});
test('Intro choices have different intermediate scenes and a later callback',()=>{const s=start();const ids=['role','credit','hired'].map(c=>choose(s,c).node);assert.equal(new Set(ids).size,3);const run=walk(routes.founder);assert.ok(run.history.find(h=>h.id==='c4_request').text.join(' ').includes('Du wolltest deinen Beitrag schriftlich'));});
test('Late evidence route grants valid documents without an early lucky choice',()=>{const s=walk({...routes.founder,c2_code:'deck',c2_deck:'show',c4_request:'fetch',c4_fetch:'secure',c4_evidence:'credit'});assert.ok(s.inventory.includes('protocol'));assert.ok(s.inventory.includes('credit'));assert.equal(s.ending,'founder');});
test('Rest negotiation can change into late evidence without a story loop',()=>{const s=walk({...routes.founder,c2_code:'deck',c2_deck:'show',c4_request:'rest',c4_resttalk:'recognition',c4_lastproof:'confirm'});assert.ok(s.inventory.includes('protocol')&&s.inventory.includes('credit'));assert.ok(s.visited.includes('c4_lastproof'));});
test('Actual composed pitch reappears unchanged in rehearsal and review',()=>{const s=walk(routes.human,{pitch:[1,1,1]});const text=s.games.pitch.text;assert.ok(s.history.find(h=>h.id==='c3_review').text.join(' ').includes(text));assert.ok(s.history.find(h=>h.id==='c5_review').text.join(' ').includes(text));});

// Minigame 1: all six permutations, recoverable failure and one-shot effects.
for(const order of perms(['clear','place','test']))test(`IT order: ${order.join(' → ')}`,()=>{let s=walk({}, {until:'c2_it'});for(const step of order)s=apply(s,{type:'it_add',step});const before=s.stats.substance;s=apply(s,{type:'it_test'});if(order.join(',')==='clear,place,test'){assert.equal(s.node,'c2_recovery');assert.equal(s.stats.substance,Math.min(5,before+1));}else{assert.equal(s.node,'c2_it');assert.equal(s.games.it.attempts,1);assert.equal(s.games.it.order.length,0);assert.ok(s.games.it.feedback.includes('Bahn'));s=mini(s);assert.equal(s.node,'c2_recovery');assert.equal(s.games.it.attempts,2);}});
test('IT inspections, hints and partial ordering survive save and resume',()=>{let s=walk({}, {until:'c2_it'});s=apply(s,{type:'it_inspect',item:'laundry'});s=apply(s,{type:'hint',game:'it'});s=apply(s,{type:'it_add',step:'clear'});const restored=G.unpack(json(G.pack(s))).state;assert.deepEqual(restored,s);assert.throws(()=>apply(s,{type:'it_add',step:'clear'}));assert.throws(()=>apply(s,{type:'it_inspect',item:'laundry'}));});

// All 27 pitches are accepted exactly once; evaluate structural contradictions explicitly.
for(let p=0;p<3;p++)for(let a=0;a<3;a++)for(let v=0;v<3;v++)test(`Pitch ${p}/${a}/${v}: preview, one-shot commit and verbatim callback`,()=>{let s=walk({}, {until:'c3_pitch'});const before={...s.stats};for(const [key,value]of Object.entries({product:p,audience:a,promise:v}))s=apply(s,{type:'pitch_select',group:key,value});assert.deepEqual(s.stats,before);const expected=G.evaluatePitch(s.games.pitch.selection);s=apply(s,{type:'pitch_submit'});assert.equal(s.node,'c3_review');assert.equal(s.games.pitch.text,expected.text);assert.equal(s.games.pitch.kind,expected.kind);assert.throws(()=>apply(s,{type:'pitch_submit'}));assert.deepEqual(G.unpack(json(G.pack(s))).state,s);});
test('Contradictory guarantee does not masquerade as verified substance',()=>{const p=G.evaluatePitch({product:0,audience:0,promise:1});assert.equal(p.kind,'contradiction');assert.ok(p.stats.substance<0);});

// All 90 resource allocations use exactly two of each tool.
const orders=allToolOrders();assert.equal(orders.length,90);
for(const [i,order]of orders.entries())test(`Firewall allocation ${String(i+1).padStart(2,'0')}: ${order.join('/')}`,()=>{let s=walk({}, {until:'c4_firewall'});for(const tool of order){s=apply(s,{type:'fire_act',tool});assert.ok(s.games.firewall.pending);assert.throws(()=>apply(s,{type:'fire_act',tool}));s=apply(s,{type:'fire_next'});}assert.equal(s.node,'c4_crisis');assert.deepEqual(s.games.firewall.resources,{mute:0,ai:0,self:0});assert.equal(s.games.firewall.log.length,6);assert.ok(Number.isInteger(s.games.firewall.noise));assert.equal(s.games.firewall.awake,s.games.firewall.noise>=4);});
test('Optimal firewall protects Ted, resolves all six and has no countdown',()=>{const s=mini(walk({}, {until:'c4_firewall'}));assert.equal(s.games.firewall.solved,6);assert.equal(s.games.firewall.noise,0);assert.equal(s.games.firewall.awake,false);assert.ok(!('deadline' in s.games.firewall));});
test('Firewall cannot replenish a resource by replaying a stale action',()=>{let s=walk({}, {until:'c4_firewall'});const action={type:'fire_act',tool:'mute',r:s.events.length};const before=s;s=G.reduce(s,action);assert.throws(()=>G.reduce(s,action));assert.equal(before.games.firewall.resources.mute,2);assert.equal(s.games.firewall.resources.mute,1);const restored=G.unpack(json(G.pack(s))).state;assert.deepEqual(restored.games.firewall,s.games.firewall);});

// Saves and checkpoint correctness; imports are replayed, not trusted.
test('Full event export/import reproduces transcript, metrics and checksums of state',()=>{const s=walk(routes.founder);const raw=json(G.pack(s,['founder']));const unpacked=G.unpack(raw);assert.deepEqual(unpacked.state,s);assert.deepEqual(unpacked.endings,['founder']);assert.deepEqual(G.metrics(unpacked.state),G.metrics(s));});
test('Each checkpoint rewinds exactly to the reached chapter and drops later effects',()=>{const full=walk(routes.founder);for(let ch=1;ch<=5;ch++){const r=G.checkpoint(full,ch);assert.equal(r.node,G.CHAPTERS[ch-1].start);assert.equal(r.chapter,ch);assert.equal(r.complete,false);assert.equal(r.ending,null);assert.ok(r.visited.every(id=>G.STORY[id].chapter<=ch));assert.equal(r.events.length,full.checkpoints[ch]);if(ch<4)assert.ok(!r.inventory.includes('credit'));}});
test('Replaying a chapter does not duplicate documents or earned statistics',()=>{const full=walk(routes.founder);let s=G.checkpoint(full,5);while(!s.complete){s=choose(s,routes.founder[s.node]||G.choices(s)[0].id);}assert.deepEqual(s.stats,full.stats);assert.deepEqual(s.inventory,full.inventory);assert.equal(s.photos.length,22);});
test('Malformed and stale actions never mutate their input state',()=>{const s=start(),snapshot=json(s);for(const event of [{type:'choose',node:'fake',id:'credit',r:1},{type:'choose',node:s.node,id:'nope',r:1},{type:'choose',node:s.node,id:'credit',r:0},{type:'skip',game:'pitch',r:1},{type:'start',r:1}]){assert.throws(()=>G.reduce(s,event));assert.equal(json(s),snapshot);}});
for(const [label,value]of Object.entries({invalidJSON:'{oops',oldChat:json({chats:[]}),wrongSchema:json({format:'CATGPT_TED_GAME',schema:999,events:[],endings:[]}),foreignAction:json({format:'CATGPT_TED_GAME',schema:1,events:[{type:'eval',code:'alert(1)',r:0}],endings:[]}),extraField:json({format:'CATGPT_TED_GAME',schema:1,events:[{type:'start',r:0,html:'<img onerror=alert(1)>'}],endings:[]}),badRevision:json({format:'CATGPT_TED_GAME',schema:1,events:[{type:'start',r:6}],endings:[]}),badEnding:json({format:'CATGPT_TED_GAME',schema:1,events:[],endings:['__proto__']}),oversize:'x'.repeat(200001)}))test(`Reject unsafe or incompatible save: ${label}`,()=>assert.throws(()=>G.unpack(value)));
test('All statistic values stay within the visible 0–5 scale',()=>{for(const route of Object.values(routes)){const s=walk(route);assert.ok(Object.values(s.stats).every(v=>Number.isInteger(v)&&v>=0&&v<=5));}});
test('Frozen story data cannot be altered by a saved action',()=>{assert.ok(Object.isFrozen(G.STORY));assert.ok(Object.isFrozen(G.STORY.c1_welcome.choices));assert.throws(()=>G.STORY.c1_welcome.title='edited');});

// Seeded path sampling supplements the acyclic graph proof and deterministic tests.
test('600 seeded full playthroughs: every ending and node, no softlock, always 22 photos',()=>{
 const seen=new Set(),ends=new Set(),samples=[];
 for(let run=0;run<600;run++){
  let s=start(),guard=0;
  while(!s.complete){assert.ok(++guard<100);seen.add(s.node);const game=G.STORY[s.node].game;if(game){if(rng()<.28)s=mini(s,'skip');else if(game==='pitch')s=mini(s,'solve',[0,1,2].map(()=>Math.floor(rng()*3)));else if(game==='firewall'){for(const tool of orders[Math.floor(rng()*orders.length)]){s=apply(s,{type:'fire_act',tool});s=apply(s,{type:'fire_next'});}}else s=mini(s);continue;}const c=G.choices(s);assert.ok(c.length>0,`Softlock ${s.node}`);s=choose(s,c[Math.floor(rng()*c.length)].id);}
  seen.add(s.node);ends.add(s.ending);assert.equal(s.photos.length,22);assert.ok(Object.values(s.stats).every(v=>v>=0&&v<=5));if(run<20)samples.push(G.metrics(s));
 }
 assert.equal(ends.size,4);assert.equal(seen.size,Object.keys(G.STORY).length);
 fs.mkdirSync(path.join(ROOT,'results'),{recursive:true});fs.writeFileSync(path.join(ROOT,'results','path-metrics.json'),json({seed:63471,runs:600,nodes:seen.size,endings:[...ends],samples}));
});
// Fixtures for browser and human review use the same production reducer.
for(const [name,route]of Object.entries(routes)){
 const s=walk(route,{mode:name==='exit'?'skip':'solve',pitch:name==='human'?[1,1,1]:name==='rest'?[2,2,2]:[0,0,0]});
 fs.mkdirSync(path.join(ROOT,'results','fixtures'),{recursive:true});fs.writeFileSync(path.join(ROOT,'results','fixtures',`${name}.json`),json(G.pack(s,[name])));
}
