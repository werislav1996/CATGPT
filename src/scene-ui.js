/* Current-scene presentation. The full, replayable conversation stays in state.history. */
let sceneFlow={node:null,photo:0,review:null},walking=false,walkToken=0,lastBallPosition=null;
function sceneEntry(){return state.history.findLast(h=>h.kind==='scene');}
function savePresentation(){return {node:sceneFlow.node,photo:sceneFlow.photo,review:sceneFlow.review,revision:state.events.length};}
function restorePresentation(p){
 sceneFlow={node:state.node,photo:0,review:null};
 if(!p||p.revision!==state.events.length||p.node!==state.node)return;
 const count=sceneEntry()?.photos?.length||1;
 if(Number.isInteger(p.photo)&&p.photo>=0&&p.photo<count)sceneFlow.photo=p.photo;
 const r=p.review;
 if(r&&Number.isInteger(r.sceneIndex)&&Number.isInteger(r.replyIndex)&&state.history[r.sceneIndex]?.kind==='scene'&&state.history[r.replyIndex]?.kind==='player'&&r.replyIndex>r.sceneIndex&&r.replyIndex<state.history.length)sceneFlow.review={sceneIndex:r.sceneIndex,replyIndex:r.replyIndex};
}
function resetScene(){sceneFlow={node:state.node,photo:0,review:null};}
function stagePhoto(id){const b=chatPhoto(id);b.className='scene-photo';b.querySelector('img').loading='eager';return b;}
function renderTranscript(force=false){
 if(!state.started)return;
 if(force)resetScene();
 if(sceneFlow.node!==state.node&&!sceneFlow.review)resetScene();
 const root=$('transcript');root.replaceChildren();
 const review=sceneFlow.review,h=review?state.history[review.sceneIndex]:sceneEntry();
 if(!h)return;
 const stage=el('article','scene-stage'+(review?' review':''));stage.id='currentStage';
 const currentId=review?h.photos?.at(-1):h.photos?.[sceneFlow.photo];
 const kicker=el('div','scene-kicker');kicker.append(el('span','',review?'TED HAT GEANTWORTET':G.CHAPTERS[h.chapter-1].short.toUpperCase()),el('span','',currentId?`FOTO ${String(PHOTO.get(currentId).number).padStart(2,'0')}`:'TED HAT NOCH WAS'));stage.append(kicker);
 const heading=el('h2','scene-title',h.title);heading.id='currentTitle';heading.tabIndex=-1;stage.append(heading);
 const photos=h.photos||[],photo=review?photos.at(-1):photos[Math.min(sceneFlow.photo,photos.length-1)];
 if(photo)stage.append(stagePhoto(photo));
 if(review){
  const added=state.history.slice(review.replyIndex),player=added.find(x=>x.kind==='player'),reply=added.find(x=>x.kind==='reply');
  if(player){const bubble=el('div','review-player');bubble.append(el('small','','DU'),document.createTextNode(player.text));stage.append(bubble);}
  const copy=paragraphBlock(reply?.text||['Ted hat deine Antwort notiert. Mit einer Pfote.'],'scene-copy');copy.prepend(el('strong','ted-label','TED / GESCHÄFTSFÜHRUNG'));stage.append(copy);
  const effects=added.filter(x=>x.kind==='effect').flatMap(x=>x.text||[]);if(effects.length)stage.append(el('p','review-effects',effects.join(' · ')));
 }else if(!h.game||state.pending){
  if(photos.length>1){const dots=el('div','scene-progress');dots.setAttribute('aria-label',`Bild ${sceneFlow.photo+1} von ${photos.length}`);photos.forEach((_,i)=>dots.append(el('i',i===sceneFlow.photo?'active':'')));stage.append(dots);}
  const text=photo&&sceneFlow.photo<photos.length-1?[G.PHOTO_STORY[photo].note]:h.text;
  const copy=paragraphBlock(text,'scene-copy');copy.prepend(el('strong','ted-label','TED / CEO, ANGEBLICH'));stage.append(copy);
  if(h.document)stage.append(button('Beweisstück ansehen','btn',()=>openDocuments(h.document),'document'));
 }
 if(!h.game||review||state.pending)root.append(stage);
 if(!review&&G.STORY[state.node]?.game&&!state.pending){renderMini();animateBall();}
 if(!review&&state.complete)root.append(receipt());
 renderChoices();updateJump();
 CatAudio.setMode(view==='home'?'home':!review&&G.STORY[state.node]?.game&&!state.pending?'game':'story');
}
function continueScene(){
 if(walking)return;
 if(sceneFlow.review){sceneFlow.review=null;sceneFlow.node=state.node;sceneFlow.photo=0;if(state.pending){send({type:'advance',r:state.events.length});return;}renderFrame();renderTranscript();}
 else{sceneFlow.photo++;renderTranscript();}
 $('storyScroll').scrollTop=0;persist();$('currentTitle')?.focus({preventScroll:true});CatAudio.effect('message');
}
function renderChoices(){
 const root=$('choices');root.replaceChildren();$('readScene').hidden=true;
 const n=G.STORY[state.node],rev=state.events.length;root.classList.toggle('game-dock',Boolean(n?.game&&!state.pending&&!sceneFlow.review));
 if(!state.started)return;
 if(sceneFlow.review){$('decisionLabel').textContent='Ted ist fertig. Du bestimmst das Tempo.';const b=button(state.pending?state.pending.label:'Weiter geht’s','btn primary',continueScene,'arrow');b.id='continueScene';root.append(b);return;}
 const photos=sceneEntry()?.photos||[];
 if(sceneFlow.photo<photos.length-1){$('decisionLabel').textContent='Die Firmenführung geht weiter.';const b=button('Nächstes Beweisfoto','btn primary',continueScene,'images');b.id='nextScenePhoto';root.append(b);return;}
 if(state.complete){$('decisionLabel').textContent='Schicht beendet. Ted übt schon Nichtstun.';root.append(button('Deine Bilanz mitnehmen','btn primary',exportReceipt,'download'),button('Noch eine Schicht?','btn',askNew,'restart'));return;}
 if(state.pending){$('decisionLabel').textContent='Bereit für den nächsten Moment?';const b=button(state.pending.label,'btn primary',()=>send({type:'advance',r:rev}),'arrow');b.id='advanceButton';root.append(b);return;}
 if(n.game){$('decisionLabel').textContent='Du spielst. Ted beaufsichtigt.';root.append(button('Hinweis','btn',()=>{if(!state.games[n.game].hint)send({type:'hint',game:n.game,r:state.events.length});else toast({ball:'Tippe auf den Ball, dann auf den Startplatz. Möbel und Ted bleiben im Weg.',food:'Hausmenü, blaue Schale, zwei Portionen, Wasser. Der Name der Chefedition ist dir überlassen.',litter:'Schaufel für Klumpen, Besen für Spuren. Danach Streu ergänzen und abnehmen.'}[n.game]);},'info'),button('Abkürzen','btn',()=>askSkip(n.game),'right'));return;}
 $('decisionLabel').textContent='Was antwortest du?';
 G.choices(state).forEach((c,i)=>{const b=button('','choice-card',()=>{if(performance.now()<choiceLockUntil)return;send({type:'choose',node:n.id,id:c.id,r:rev});});b.dataset.choice=c.id;b.id=`choice-${i}`;b.append(el('span','choice-label',c.label),icon('arrow'));root.append(b);});
}
function send(event){
 if((sceneFlow.review&&event.type==='choose')||(walking&&event.type!=='ball_move'&&!['skip','hint'].includes(event.type)))return false;
 const scroll=$('storyScroll'),top=scroll.scrollTop,before=state.history.length,oldNode=state.node,oldScene=state.history.findLastIndex(h=>h.kind==='scene'),activeId=document.activeElement?.id;
 try{state=G.reduce(state,{...event,r:event.r===undefined?state.events.length:event.r});}catch(error){toast(error.message);return false;}
 if(state.complete&&!endings.includes(state.ending))endings.push(state.ending);
 const added=state.history.slice(before),hasReply=added.some(h=>h.kind==='reply');
 if(hasReply&&oldScene>=0){sceneFlow={node:state.node,photo:0,review:{sceneIndex:oldScene,replyIndex:before}};CatAudio.effect(state.complete||state.pending?.kind==='game'?'success':'message');}
 else if(oldNode!==state.node){resetScene();CatAudio.effect('message');}
 else CatAudio.effect(event.type.startsWith('ball_')?'roll':event.type==='food_water'?'water':event.type.startsWith('food_')?'bowl':event.type.startsWith('litter_')?'sweep':'tap');
 renderFrame();renderTranscript();
 // Choosing an answer never asks the browser to scroll to another history entry.
 scroll.scrollTop=event.type==='start'||event.type==='advance'?0:top;
 if(activeId&&!hasReply)focusMini(activeId);
 if(hasReply)announce('Ted: '+added.find(h=>h.kind==='reply').text.join(' '));else if(G.STORY[state.node]?.game)announce(state.games[G.STORY[state.node].game].feedback);
 choiceLockUntil=performance.now()+130;persist();return true;
}
function begin(){closeDialogs();view='game';CatAudio.setMode('story');CatAudio.unlock();if(!state.started)send({type:'start',r:0});else{renderFrame();renderTranscript();$('storyScroll').scrollTop=0;}}
function scrollToEntry(){openHistory();}
function scrollCurrent(){if(view==='game')$('storyScroll').scrollTop=0;}
function scrollMini(){if(view==='game')$('storyScroll').scrollTop=0;}
function updateJump(){$('jumpCurrent').hidden=true;}
function openHistory(){
 const root=$('historyBody');root.replaceChildren();
 if(!state.started)root.append(el('p','','Ted übt das Vorstellungsgespräch noch an sich selbst.'));
 state.history.forEach(h=>{if(h.kind==='chapter')root.append(el('h3','log-chapter',h.title));if(h.kind==='scene'){root.append(el('h4','log-heading',h.title));for(const id of h.photos||[]){const b=button('','',()=>openPhoto(id));b.setAttribute('aria-label',PHOTO.get(id).alt);b.append(image(id,'history-photo'));root.append(b);}root.append(paragraphBlock(h.text,'log-text'));}if(h.kind==='player')root.append(el('p','log-user','DU: '+h.text));if(h.kind==='reply')root.append(paragraphBlock(h.text,'log-reply'));});openDialog('historyDialog');
}
async function walkTo(x,y){
 if(walking||sceneFlow.review||state.pending||state.node!=='c2_ball')return;
 const g=state.games.ball;if(g.phase!=='fetch')return;
 const q=[[g.x,g.y,[]]],seen=new Set();let path=null;
 while(q.length){const [cx,cy,p]=q.shift(),key=cx+','+cy;if(seen.has(key))continue;seen.add(key);if(cx===x&&cy===y){path=p;break;}for(const [dir,[dx,dy]]of Object.entries(G.DIRECTIONS)){const nx=cx+dx,ny=cy+dy;if(nx>=0&&ny>=0&&nx<G.ROOM.width&&ny<G.ROOM.height&&!G.ROOM.blocks.some(b=>b.x===nx&&b.y===ny))q.push([nx,ny,[...p,dir]]);}}
 if(path===null){toast('Da liegt ein Möbelstück. Oder Ted. Beides bewegt sich beruflich nicht.');return;}
 const token=++walkToken;walking=true;const node=state.node;
 try{for(const dir of path){if(token!==walkToken||state.node!==node||state.pending||view!=='game'||document.querySelector('dialog[open]'))break;if(!send({type:'ball_move',dir,r:state.events.length}))break;await new Promise(r=>setTimeout(r,settings.reduceMotion?0:100));}}finally{walking=false;if(state.node===node&&!sceneFlow.review)renderTranscript();}
}
function animateBall(){
 if(state.node!=='c2_ball'){lastBallPosition=null;return;}
 const g=state.games.ball,cell=$('roomGrid')?.querySelector('.is-player'),avatar=cell?.querySelector('svg');
 if(avatar&&lastBallPosition&&!settings.reduceMotion){const dx=lastBallPosition.x-g.x,dy=lastBallPosition.y-g.y;if(Math.abs(dx)+Math.abs(dy)===1)avatar.animate([{transform:`translate(${dx*(cell.offsetWidth+3)}px,${dy*(cell.offsetHeight+3)}px)`},{transform:'translate(0,0)'}],{duration:95,easing:'ease-out'});}
 lastBallPosition={x:g.x,y:g.y};
}
function syncAudioUI(){const a=CatAudio.getState();$('soundToggle').textContent=a.muted?'Ton aus':'Ton an';$('soundToggle').setAttribute('aria-label',a.muted?'Ton einschalten':'Ton ausschalten');$('soundToggle').setAttribute('aria-pressed',String(!a.muted));$('audioMuted').checked=a.muted;$('musicVolume').value=String(Math.round(a.music*100));$('effectsVolume').value=String(Math.round(a.effects*100));$('musicValue').textContent=`${Math.round(a.music*100)} %`;$('effectsValue').textContent=`${Math.round(a.effects*100)} %`;}
$('soundToggle').addEventListener('click',()=>{CatAudio.configure({muted:!CatAudio.getState().muted});CatAudio.unlock();});
$('audioMuted').addEventListener('change',e=>{CatAudio.configure({muted:e.target.checked});CatAudio.unlock();});
$('musicVolume').addEventListener('input',e=>{CatAudio.configure({music:Number(e.target.value)/100});CatAudio.unlock();});
$('effectsVolume').addEventListener('input',e=>{CatAudio.configure({effects:Number(e.target.value)/100});CatAudio.unlock();CatAudio.effect('bowl');});
window.addEventListener('cat-audio-change',syncAudioUI);syncAudioUI();
document.addEventListener('click',e=>{if(e.target.closest('button'))CatAudio.effect('tap');});
