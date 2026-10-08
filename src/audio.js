/* Original Web Audio arrangement of the traditional melody Bruder Jakob.
   Synthesized voices and effects; no recording, sample, external resource or library. */
(()=>{'use strict';
const KEY='catgpt.audio.v1';
let prefs={muted:false,music:.24,effects:.45};
try{const p=JSON.parse(localStorage.getItem(KEY)||'null');if(p){prefs.muted=p.muted===true;for(const k of ['music','effects'])if(Number.isFinite(p[k]))prefs[k]=Math.max(0,Math.min(1,p[k]));}}catch{}
let ctx,master,musicBus,fxBus,timer=null,mode='home',unlocked=false,step=0,next=0,lastFX=0;
const phrase=[[60,1],[62,1],[64,1],[60,1],[60,1],[62,1],[64,1],[60,1],[64,1],[65,1],[67,2],[64,1],[65,1],[67,2],[67,.5],[69,.5],[67,.5],[65,.5],[64,1],[60,1],[67,.5],[69,.5],[67,.5],[65,.5],[64,1],[60,1],[60,1],[55,1],[60,2],[60,1],[55,1],[60,2]];
const hz=n=>440*2**((n-69)/12);
function tone(bus,n,t,d,volume=.1,type='sine',meow=false){
 const o=ctx.createOscillator(),g=ctx.createGain();o.type=type;o.frequency.setValueAtTime(hz(n)*(meow?1.2:1),t);
 if(meow){o.frequency.exponentialRampToValueAtTime(hz(n),t+.075);o.frequency.exponentialRampToValueAtTime(hz(n)*.83,t+d);const f=ctx.createBiquadFilter();f.type='bandpass';f.Q.value=3;f.frequency.setValueAtTime(1250,t);f.frequency.exponentialRampToValueAtTime(430,t+d);o.connect(f);f.connect(g);}else o.connect(g);
 g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(volume,t+.025);g.gain.exponentialRampToValueAtTime(.001,t+d);g.connect(bus);o.start(t);o.stop(t+d+.03);
}
function levels(){if(!ctx)return;const t=ctx.currentTime;master.gain.setTargetAtTime(prefs.muted?0:1,t,.035);musicBus.gain.setTargetAtTime(prefs.music,t,.15);fxBus.gain.setTargetAtTime(prefs.effects,t,.035);}
function schedule(){
 if(!ctx||ctx.state!=='running'||document.hidden||prefs.muted||mode==='home')return;
 if(next<ctx.currentTime)next=ctx.currentTime+.07;
 const beat=mode==='game'?.31:.46;
 while(next<ctx.currentTime+.16){
  const i=step%phrase.length,round=Math.floor(step/phrase.length),[note,length]=phrase[i];
  // Alternate a meowing verse and an instrumental verse to leave room for reading.
  const voice=round%2===0&&i%8<6;
  tone(musicBus,note+12,next,beat*length*.78,voice?.12:.11,voice?'sawtooth':'triangle',voice);
  if(i%4===0){tone(musicBus,i<14?48:43,next,beat*1.6,.13,'sine');tone(musicBus,i<14?55:50,next+.025,beat*.75,.045,'triangle');}
  step++;next+=beat*length;
 }
}
async function sync(){
 if(!ctx)return;
 levels();
 const playing=unlocked&&!document.hidden&&!prefs.muted&&mode!=='home';
 if(!playing){clearInterval(timer);timer=null;try{await ctx.suspend();}catch{}return;}
 try{await ctx.resume();}catch{return;}
 if(ctx.state!=='running'||document.hidden||prefs.muted||mode==='home')return;
 if(!timer){next=ctx.currentTime+.06;schedule();timer=setInterval(schedule,80);}
}
async function unlock(){
 try{if(!ctx){const Audio=window.AudioContext||window.webkitAudioContext;if(!Audio)return false;ctx=new Audio();master=ctx.createGain();musicBus=ctx.createGain();fxBus=ctx.createGain();musicBus.connect(master);fxBus.connect(master);const limit=ctx.createDynamicsCompressor();master.connect(limit);limit.connect(ctx.destination);}unlocked=true;await sync();return ctx.state==='running';}catch{return false;}
}
function effect(kind='tap'){
 if(!ctx||ctx.state!=='running'||prefs.muted||!prefs.effects||document.hidden)return;
 const t=ctx.currentTime;if(t-lastFX<.06)return;lastFX=t;
 if(kind==='success'){[60,64,67,72].forEach((n,i)=>tone(fxBus,n+12,t+i*.09,.24,.15,'triangle'));tone(fxBus,76,t+.38,.33,.16,'sawtooth',true);}
 else if(kind==='meow')tone(fxBus,72,t,.28,.14,'sawtooth',true);
 else if(kind==='water'){[77,81,86].forEach((n,i)=>tone(fxBus,n,t+i*.055,.10,.09,'sine'));}
 else if(kind==='sweep'){tone(fxBus,44,t,.15,.10,'triangle');tone(fxBus,51,t+.04,.08,.07,'triangle');}
 else if(kind==='roll'){tone(fxBus,55,t,.07,.09,'triangle');}
 else if(kind==='bowl'){tone(fxBus,86,t,.35,.10,'sine');tone(fxBus,93,t+.01,.18,.035,'sine');}
 else if(kind==='message'){tone(fxBus,74,t,.12,.09,'sine');tone(fxBus,79,t+.07,.18,.08,'sine');}
 else tone(fxBus,76,t,.065,.07,'sine');
}
function configure(changes){for(const k of ['music','effects'])if(Number.isFinite(changes[k]))prefs[k]=Math.max(0,Math.min(1,changes[k]));if(typeof changes.muted==='boolean')prefs.muted=changes.muted;try{localStorage.setItem(KEY,JSON.stringify(prefs));}catch{}sync();window.dispatchEvent(new Event('cat-audio-change'));}
document.addEventListener('visibilitychange',sync);
window.addEventListener('pagehide',()=>{clearInterval(timer);timer=null;ctx?.suspend().catch(()=>{});});
window.addEventListener('pageshow',()=>{if(ctx)sync();});
globalThis.CatAudio=Object.freeze({unlock,effect,configure,setMode(value){if(mode!==value){mode=value;sync();}},getState:()=>({...prefs,mode,unlocked,running:ctx?.state==='running',scheduled:timer!==null}),melody:'Bruder Jakob – Miau-Runde'});
})();
