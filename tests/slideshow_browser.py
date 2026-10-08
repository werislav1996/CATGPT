"""Focused production-HTML checks for the new photographic story and readback UI.
No mock story logic; checkpoints are imported through the actual game input.
Storage is an explicit in-memory adapter because managed file navigation is blocked.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,shutil,traceback
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
HTML=(ROOT/'catgpt.html').read_text();fixtures={k:json.loads((OUT/'fixtures'/f'{k}.json').read_text()) for k in ('founder','human','rest','exit')}
results=[];errors=[];network=[]
def record(name,fn):
 try:
  fn();results.append({'name':name,'passed':True});print('PASS',name,flush=True)
 except Exception as e:
  results.append({'name':name,'passed':False,'error':str(e)[:1200]});print('FAIL',name,str(e)[:300],flush=True)
def check(value,message='Assertion failed'):
 assert value,message
def state():return page.evaluate('CatGameUI.getState()')
def choose(id):
 page.wait_for_timeout(210);old=state()['node'];page.locator(f'#choices [data-choice="{id}"]').click();page.wait_for_function('n=>CatGameUI.getState().node!==n',arg=old)
def go(node,route='founder'):
 packed=page.evaluate('''({fixture,node})=>{let s=CatGame.fresh();for(const e of fixture.events){s=CatGame.reduce(s,e);if(s.node===node)return CatGame.pack(s);}throw new Error('Missing fixture '+node);}''',{'fixture':fixtures[route],'node':node})
 page.locator('#saveFile').set_input_files({'name':'checkpoint.json','mimeType':'application/json','buffer':json.dumps(packed).encode()});page.locator('#confirmYes').click();page.wait_for_function('n=>CatGameUI.getState().node===n',arg=node);page.wait_for_timeout(100)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':960},device_scale_factor=1)
 page.set_default_timeout(8000);page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
 page.evaluate('''()=>{window.__store=new Map([['catgpt.game.v1','old-game-not-overwritten']]);Object.defineProperty(window,'localStorage',{value:{getItem:k=>window.__store.get(k)||null,setItem:(k,v)=>window.__store.set(k,String(v)),removeItem:k=>window.__store.delete(k)},configurable:true});}''')
 page.set_content(HTML,wait_until='load');page.locator('#startButton').click()
 record('One full scene on screen, not an accumulating chat transcript',lambda:check(page.locator('#transcript article').count()==1))
 record('Initial image uses the curated presentation crop',lambda:check(page.evaluate('document.querySelector(".slide-image").src===JSON.parse(document.getElementById("catAssets").textContent).photos.find(p=>p.id==="judge").sceneSrc')))
 choose('role');choose('scope');snapshot=state()
 record('The chosen answer and Ted reaction are present beside the new image',lambda:check(page.locator('#turnStart').count()==1 and 'Aufgabe' in page.locator('#turnStart').inner_text()))
 page.locator('#slidePrev').click()
 record('Previous-slide navigation changes only the view',lambda:check(state()==snapshot and page.locator('#currentScene').get_attribute('data-scene')=='c1_role'))
 record('Readback removes active answer buttons',lambda:check(page.locator('#choices .choice').count()==0 and page.locator('.review-dock').count()==1))
 page.keyboard.press('1')
 record('Answer shortcut cannot alter state while reading an old slide',lambda:check(state()==snapshot))
 record('Dispatch rejects a decision while the interface is in readback',lambda:check(page.evaluate('()=>{const s=CatGameUI.getState();return CatGameUI.dispatch({type:"choose",node:s.node,id:CatGame.choices(s)[0].id})}') is False and state()==snapshot))
 page.locator('#choices button').filter(has_text='Zur aktuellen Szene').click()
 record('Returning to the present preserves all flags, statistics and history',lambda:check(state()==snapshot and page.locator('#choices .choice').count()==3 and page.locator('#currentScene').get_attribute('data-scene')=='c1_org'))
 page.keyboard.press('ArrowLeft');page.keyboard.press('ArrowRight')
 record('Arrow-key readback never awards points or consumes a story choice',lambda:check(state()==snapshot and page.evaluate('CatGameUI.getReviewIndex()') is None))
 page.locator('#storyLog').click()
 record('Dialog history contains the real earlier choices and responses',lambda:check('Was genau ist meine Aufgabe?' in page.locator('#historyBody').inner_text() and 'ungewöhnlich' not in page.locator('#historyTitle').inner_text()))
 page.locator('.history-heading').first.click()
 record('A history heading opens the matching old slide without rewinding gameplay',lambda:check(state()==snapshot and page.locator('#currentScene').get_attribute('data-scene')=='c1_welcome'))
 page.locator('#choices button').filter(has_text='Zur aktuellen Szene').click()
 page.locator('.top-tools [data-action="gallery"]').click();page.locator('#galleryFilters [data-filter="new"]').click()
 record('New-photo filter contains exactly eleven freely accessible pictures',lambda:check(page.locator('#galleryGrid .gallery-item').count()==11))
 record('Browsing unseen photographs never grants story progress',lambda:check(state()==snapshot))
 page.locator('#galleryGrid [data-photo="portfolio"]').click()
 record('Lightbox shows the full frame, not the cropped slideshow copy',lambda:check(page.evaluate('document.getElementById("lightboxImage").src===JSON.parse(document.getElementById("catAssets").textContent).photos.find(p=>p.id==="portfolio").src')))
 page.keyboard.press('Escape')
 def decode_all():
  result=page.evaluate('''async()=>{const p=JSON.parse(document.getElementById('catAssets').textContent).photos;let n=0;for(const photo of p)for(const src of [photo.src,photo.sceneSrc].filter(Boolean)){const im=new Image();im.src=src;await im.decode();if(!im.naturalWidth||!im.naturalHeight)throw new Error(photo.id);n++;}return n;}''')
  check(result==58)
 record('All 33 full frames and 25 presentation crops decode in Chromium',decode_all)
 go('c2_portfolio');page.screenshot(path=str(OUT/'slideshow-team-desktop.png'))
 record('The toy-team image is the correct main stage picture',lambda:check(page.locator('.slide-media').get_attribute('data-story-photo')=='portfolio' and 'Fisch ist fürs Netz' in page.locator('.slide-copy').inner_text()))
 choose('union')
 record('New team decision changes the immediately following remote-IT story',lambda:check(state()['flags']['teamRespect'] and 'erste Pause' in page.locator('.slide-copy').inner_text()))
 snapshot=state();page.locator('#slidePrev').click()
 record('Photo navigation changes to the right historical photograph',lambda:check(page.locator('.slide-media').get_attribute('data-story-photo')=='portfolio' and state()==snapshot))
 page.evaluate('()=>{const s=CatGameUI.getState();const ix=s.history.filter(h=>h.kind==="scene").findIndex(h=>h.id==="c2_it");CatGameUI.reviewSlide(ix);}')
 record('A completed minigame is a read-only slide, never reactivated',lambda:check(page.locator('#miniGame').count()==0 and page.locator('.mini-summary').count()==1 and state()==snapshot))
 page.evaluate('CatGameUI.showHome()');page.locator('#startButton').click()
 record('Resume from the home page returns to the current decision, not the old slide',lambda:check(page.locator('#currentScene').get_attribute('data-scene')==state()['node'] and page.evaluate('CatGameUI.getReviewIndex()') is None))
 go('c2_desk');page.screenshot(path=str(OUT/'slideshow-office-desktop.png'))
 record('Desk scene preserves the full wide shot and workstation joke',lambda:check(page.locator('.slide-media').get_attribute('data-story-photo')=='desk' and 'Ich bin die Firewall' in page.locator('.slide-copy').inner_text()))
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(OUT/'slideshow-office-mobile.png'));snapshot=state();page.locator('#readScene').click()
 record('Mobile Ted-read button reveals the dialogue without choosing an answer',lambda:check(state()==snapshot and page.evaluate('document.querySelector(".slide-copy").getBoundingClientRect().top<200')))
 page.screenshot(path=str(OUT/'slideshow-dialogue-mobile.png'))
 newmap={'c4_edge':'edge','c4_benefits':'wellness','c3_pivot':'upsidedown','c2_portfolio':'portfolio','c4_security':'security','c2_remoteit':'remoteit','c3_solar':'solar','c3_market':'marketshare','c5_walkover':'walkover','c2_desk':'desk','c4_approval':'approval'}
 for node,photo in newmap.items():
  go(node);page.set_viewport_size({'width':320,'height':700})
  record(f'{node}: matching photo and mobile layout without horizontal overflow',lambda photo=photo:check(page.locator('.slide-media').get_attribute('data-story-photo')==photo and page.evaluate('document.documentElement.scrollWidth<=innerWidth && document.getElementById("decisionDock").getBoundingClientRect().bottom<=innerHeight+1')))
 go('c4_approval','human');before=state()['inventory'];choose('paw')
 record('A joke paw stamp does not silently grant a binding recognition document',lambda:check(state()['flags']['pawStamp'] and state()['inventory']==before and 'credit' not in state()['inventory']))
 page.set_viewport_size({'width':1440,'height':960});go('c2_hq');page.screenshot(path=str(OUT/'slideshow-closet-desktop.png'))
 page.locator('.top-tools [data-action="gallery"]').click();page.locator('#gallerySearch').fill('');page.locator('#galleryFilters [data-filter="all"]').click();page.screenshot(path=str(OUT/'slideshow-gallery-desktop.png'));page.keyboard.press('Escape')
 page.locator('.top-tools [data-action="settings"]').click();page.locator('#settingSave').check()
 record('New-version saving leaves the previous game key untouched',lambda:check(page.evaluate('window.__store.get("catgpt.game.v1")==="old-game-not-overwritten"&&window.__store.has("catgpt.game.v2")')))
 page.keyboard.press('Escape');snapshot=state()
 old=json.dumps({'format':'CATGPT_TED_GAME','schema':1,'build':'0.3.0','events':[],'endings':[]}).encode()
 page.locator('#saveFile').set_input_files({'name':'old.json','mimeType':'application/json','buffer':old});page.wait_for_timeout(250)
 record('Old-schema import gives a precise 0.3 explanation and never replaces the run',lambda:check(state()==snapshot and '0.3' in page.locator('#toast').inner_text()))
 record('Slideshow, gallery, history and readback generate no JavaScript errors',lambda:check(not errors,str(errors)))
 record('No external network calls in new photo-story scenarios',lambda:check(not network,str(network)))
 browser.close()
report={'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'total':len(results),'results':results,'runtime_errors':errors,'network_requests':network,'environment':'Chromium; unmodified delivered HTML loaded with set_content; explicit memory-storage adapter; actual game buttons and JSON import used'}
(OUT/'slideshow-browser-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False,indent=2));raise SystemExit(1 if report['failed'] else 0)
