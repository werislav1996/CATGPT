"""Chromium checks for the exact delivered single-file game.

The managed execution environment blocks file/http navigation. The unmodified HTML
is therefore loaded with set_content. Explicit adapters exercise storage success,
denial and corruption. No AI/server response is simulated: the game has no network.
"""
from pathlib import Path
import json, os, shutil, traceback
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
HTML=(ROOT/'catgpt.html').read_text()
results=[];errors=[];requests=[]
fixtures={name:json.loads((OUT/'fixtures'/f'{name}.json').read_text()) for name in ['founder','human','rest','exit']}
def check(value,message='Assertion failed'):
    assert value,message

def record(name,fn):
    try:
        fn();results.append({'name':name,'passed':True});print('PASS',name,flush=True)
    except Exception as ex:
        results.append({'name':name,'passed':False,'error':str(ex)[:1200]});print('FAIL',name,str(ex)[:220],flush=True)

def s(page):return page.evaluate('CatGameUI.getState()')
def ui_choose(page,id):
    page.wait_for_timeout(190)
    old=s(page)['node']
    page.locator(f'#choices [data-choice="{id}"]').click()
    page.wait_for_function('(old)=>CatGameUI.getState().node!==old',arg=old)

def export_at_node(page,fixture,node,after=0):
    return page.evaluate('''({fixture,node,after})=>{let s=CatGame.fresh();let reached=-1;
      for(let i=0;i<fixture.events.length;i++){s=CatGame.reduce(s,fixture.events[i]);if(s.node===node&&reached<0)reached=i;if(reached>=0&&i===reached+after)return CatGame.pack(s,[]);}throw new Error('Missing fixture node');}''',{'fixture':fixture,'node':node,'after':after})

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('chromium-browser'),headless=True,args=['--no-sandbox'])
    def new_page(width=1440,height=960,stored=None,storage='memory'):
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,has_touch=width<=700,is_mobile=width<=700)
        page.set_default_timeout(6500)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
        if storage=='memory':
            page.evaluate('''(initial)=>{window.__store=new Map(Object.entries(initial||{}));window.__failWrites=false;window.__silentWrites=false;
            Object.defineProperty(window,'localStorage',{value:{getItem:k=>window.__store.get(k)||null,setItem:(k,v)=>{if(window.__failWrites)throw new Error('Test storage quota');if(!window.__silentWrites)window.__store.set(k,String(v));},removeItem:k=>window.__store.delete(k)},configurable:true});}''',stored or {})
        elif storage=='denied':
            page.evaluate('''()=>{Object.defineProperty(window,'localStorage',{get:()=>{throw new DOMException('Test storage denied','SecurityError');},configurable:true});}''')
        page.set_content(HTML,wait_until='load')
        return page

    page=new_page()
    record('Startup: game UI and all embedded assets initialize without errors',lambda:check(page.evaluate('!!CatGameUI') and page.locator('#app').is_visible()))
    record('Home: one Ted, no character selector or old free-text field',lambda:(check(page.locator('#chatInput').count()==0),check('Ted' in page.locator('.top-id').inner_text())))
    record('Home desktop: no horizontal overflow',lambda:check(page.evaluate('document.documentElement.scrollWidth<=innerWidth')))
    record('Default: persistence remains opt-in',lambda:check(not page.locator('#landingSave').is_checked() and 'Nur dieser Tab' in page.locator('#saveState').inner_text()))
    page.screenshot(path=str(OUT/'home-desktop.png'),full_page=True)
    page.locator('#startButton').click()
    record('Start button opens the first story with three real choices',lambda:(check(s(page)['node']=='c1_welcome'),check(page.locator('#choices .choice').count()==3)))
    page.screenshot(path=str(OUT/'story-desktop.png'),full_page=True)
    ui_choose(page,'credit')
    record('Branch choice enters its own scene and stores the intention',lambda:check(s(page)['node']=='c1_credit' and s(page)['flags']['askedCredit']))
    record('Immediate Ted response remains visible in the new reading turn',lambda:check(page.locator('#turnStart').count()==1 and page.evaluate('document.getElementById("turnStart").getBoundingClientRect().top>=document.getElementById("storyScroll").getBoundingClientRect().top-2')))
    ui_choose(page,'keep')
    record('Choice effect updates substance exactly once',lambda:check(s(page)['stats']['substance']==1))
    page.wait_for_timeout(220)
    page.keyboard.press('3')
    record('Keyboard 3 chooses the third story answer',lambda:check(s(page)['node']=='c1_org_rest'))
    record('Only reached chapters are replayable',lambda:check(page.locator('#chapterNav [data-chapter="1"]').is_enabled() and page.locator('#chapterNav [data-chapter="2"]').is_disabled()))
    snapshot=s(page)
    page.locator('#chapterNav [data-chapter="1"]').click();page.locator('#confirmNo').click()
    record('Cancelling a chapter restart preserves every event',lambda:check(s(page)==snapshot))
    page.locator('#chapterNav [data-chapter="1"]').click();page.locator('#confirmYes').click()
    record('Confirmed chapter restart resets only its later consequences',lambda:check(s(page)['node']=='c1_welcome' and s(page)['stats']=={'favor':2,'substance':0,'show':0}))
    page.wait_for_timeout(220)
    page.locator('#choices [data-choice="role"]').dblclick(delay=30)
    record('Double-click does not consume a second decision',lambda:check(s(page)['node']=='c1_role' and len([e for e in s(page)['events'] if e['type']=='choose'])==1))

    # Full gallery and modal keyboard behavior.
    page.locator('.top-tools [data-action="gallery"]').click()
    record('Gallery is immediately complete: 22 accessible cards',lambda:check(page.locator('#galleryGrid .gallery-item').count()==22))
    page.locator('#gallerySearch').fill('14')
    record('Excluded original number 14 is not returned',lambda:check(page.locator('#galleryGrid .gallery-item').count()==0))
    page.locator('#gallerySearch').fill('1000601348')
    record('Gallery filename search finds the exact approved photo',lambda:check(page.locator('#galleryGrid .gallery-item').count()==1 and page.locator('#galleryGrid .gallery-item').get_attribute('data-photo')=='paws'))
    page.locator('#gallerySearch').fill('')
    page.locator('#galleryFilters [data-filter="2"]').click()
    record('Chapter filter exposes all four HQ photos',lambda:check(page.locator('#galleryGrid .gallery-item').count()==4))
    page.locator('#galleryGrid .gallery-item').first.click()
    record('Filtered lightbox uses only its matching gallery set',lambda:check(page.locator('#lightboxCount').inner_text()=='1 / 4'))
    page.keyboard.press('ArrowRight')
    record('Lightbox next-photo keyboard navigation works',lambda:check(page.locator('#lightboxCount').inner_text()=='2 / 4'))
    page.locator('#backToGallery').click();page.locator('#galleryFilters [data-filter="all"]').click();page.locator('#galleryGrid .gallery-item').first.click()
    def all_images():
        seen=[]
        for _ in range(22):
            page.wait_for_function('document.getElementById("lightboxImage").complete&&document.getElementById("lightboxImage").naturalWidth>0')
            seen.append(page.locator('#lightboxFile').inner_text());page.locator('#nextPhoto').click()
        check(len(set(seen))==22);check(all('Nr. 14 ' not in x for x in seen))
    record('All 22 full-size photos decode and are reachable with Next',all_images)
    page.keyboard.press('Escape')
    record('Escape closes the photo archive without changing the story',lambda:check(not page.locator('#galleryDialog').is_visible() and s(page)['node']=='c1_role'))

    # Partial saves generated by the same reducer as production.
    partial_it=export_at_node(page,fixtures['founder'],'c2_it')
    partial_pitch=export_at_node(page,fixtures['founder'],'c3_pitch')
    partial_fire=export_at_node(page,fixtures['founder'],'c4_firewall')
    partial_finale=export_at_node(page,fixtures['founder'],'c5_finale')
    page.close()

    it=new_page(stored={'catgpt.game.v1':json.dumps(partial_it)})
    it.locator('#startButton').click()
    record('Saved game resumes directly at the active IT minigame',lambda:check(s(it)['node']=='c2_it' and it.locator('#miniGame').is_visible()))
    it.locator('#inspect-laundry').click()
    record('IT inspection displays a readable clue and persists it',lambda:check('Rollbahn' in it.locator('.clue-note').inner_text() and s(it)['games']['it']['inspected']==['laundry']))
    for step in ['test','place','clear']:it.locator(f'[data-step="{step}"]').click()
    it.locator('#itSubmit').click()
    record('Wrong IT order provides feedback, resets the tray and never softlocks',lambda:check(s(it)['node']=='c2_it' and s(it)['games']['it']['attempts']==1 and 'Bahn' in it.locator('.feedback').inner_text()))
    it.locator('#choices button').filter(has_text='Hinweis').click()
    record('IT hint explains the actual solution',lambda:check('Ball einsetzen' in it.locator('.mini-help').inner_text()))
    for step in ['clear','place','test']:it.locator(f'[data-step="{step}"]').click()
    it.locator('#itSubmit').click()
    record('Correct IT order exits to the next story scene',lambda:check(s(it)['node']=='c2_recovery' and s(it)['games']['it']['done']))
    it.close()

    pit=new_page(stored={'catgpt.game.v1':json.dumps(partial_pitch)})
    pit.locator('#startButton').click();before_pitch_stats=s(pit)['stats'];pit.locator('#pitch-card-product-0').click()
    record('Pitch selection does not award points before confirmation',lambda:check(s(pit)['stats']==before_pitch_stats and not s(pit)['games']['pitch']['done']))
    pit.locator('#pitchNext').click();pit.locator('#pitch-card-audience-0').click();pit.locator('#pitchNext').click();pit.locator('#pitch-card-promise-0').click()
    record('Pitch preview uses all three selected cards and enables commit',lambda:(check('nachvollziehbaren Ergebnis' in pit.locator('.pitch-preview').inner_text()),expect(pit.locator('#pitchSubmit')).to_be_enabled()))
    pit.locator('#choices button').filter(has_text='Zur Spielkarte').click();pit.screenshot(path=str(OUT/'pitch-desktop.png'),full_page=True)
    pit.locator('#pitchSubmit').click()
    record('Pitch confirmation stores the exact sentence and continues',lambda:check(s(pit)['node']=='c3_review' and s(pit)['games']['pitch']['kind']=='honest' and s(pit)['games']['pitch']['text'] in pit.locator('#currentScene').inner_text()))
    pit.close()

    fire=new_page(stored={'catgpt.game.v1':json.dumps(partial_fire)})
    fire.locator('#startButton').click();fire.locator('[data-tool="mute"]').click()
    record('Firewall consumes one resource and awaits feedback confirmation',lambda:check(s(fire)['games']['firewall']['resources']['mute']==1 and s(fire)['games']['firewall']['pending']))
    record('Firewall choices lock while feedback is pending',lambda:check(all(fire.locator(f'[data-tool="{t}"]').is_disabled() for t in ['mute','ai','self'])))
    fire_save=fire.evaluate('JSON.stringify(CatGame.pack(CatGameUI.getState()))');fire.close()
    fire=new_page(390,844,stored={'catgpt.game.v1':fire_save});fire.locator('#startButton').click()
    record('Reloaded pending firewall retains spent resource and next button',lambda:check(s(fire)['games']['firewall']['resources']['mute']==1 and fire.locator('#fireNext').is_visible()))
    fire.locator('#choices button').filter(has_text='Zur Spielkarte').click();fire.screenshot(path=str(OUT/'firewall-mobile.png'),full_page=True)
    fire.locator('#fireNext').click()
    for tool in ['self','ai','mute','self','ai']:
        fire.locator(f'[data-tool="{tool}"]').click();fire.locator('#fireNext').click()
    record('Firewall fully playable on mobile: all six solved with Ted asleep',lambda:check(s(fire)['node']=='c4_crisis' and s(fire)['games']['firewall']['solved']==6 and not s(fire)['games']['firewall']['awake']))
    fire.close()

    for name,fixture,next_node in [('IT',partial_it,'c2_recovery'),('Pitch',partial_pitch,'c3_review'),('Firewall',partial_fire,'c4_crisis')]:
        pg=new_page(stored={'catgpt.game.v1':json.dumps(fixture)});pg.locator('#startButton').click()
        pg.locator('#choices button').filter(has_text='Überspringen').click();pg.locator('#confirmNo').click()
        record(f'{name}: cancelling skip preserves active minigame',lambda pg=pg:check(pg.locator('#miniGame').is_visible()))
        pg.locator('#choices button').filter(has_text='Überspringen').click();pg.locator('#confirmYes').click()
        record(f'{name}: confirming skip continues through the written fallback',lambda pg=pg,n=next_node:check(s(pg)['node']==n))
        pg.close()

    store=new_page(stored={'catgpt.v1.local':'legacy-chat-do-not-touch'})
    store.locator('#landingSave').check();store.locator('#startButton').click();ui_choose(store,'hired')
    saved=store.evaluate('Object.fromEntries(window.__store)')
    record('Opt-in storage persists events without touching old chat data',lambda:check('catgpt.game.v1' in saved and saved['catgpt.v1.local']=='legacy-chat-do-not-touch'))
    store.close();store=new_page(stored=saved)
    record('Stored progress is offered on the home screen instead of discarded',lambda:check('fortsetzen' in store.locator('#startButton').inner_text().lower()))
    store.locator('#startButton').click()
    record('Resume reproduces the chosen branch and its original flags',lambda:check(s(store)['node']=='c1_hired' and s(store)['flags']['intro']=='hired'))
    store.locator('.top-tools [data-action="settings"]').click();store.locator('#settingSave').uncheck()
    record('Disabling persistence removes only the new game key',lambda:check(store.evaluate('!window.__store.has("catgpt.game.v1")&&window.__store.get("catgpt.v1.local")==="legacy-chat-do-not-touch"')))
    store.locator('#settingSave').check();store.locator('#settingsDialog [data-close]').click();store.evaluate('window.__failWrites=true');ui_choose(store,'stay')
    record('Quota errors keep gameplay alive and show honest storage status',lambda:check(s(store)['node']=='c1_org' and 'nicht verfügbar' in store.locator('#saveState').inner_text()))
    record('Failed persistence is not left falsely enabled',lambda:check(not store.locator('#settingSave').is_checked()));store.close()
    denied=new_page(storage='denied');denied.locator('#startButton').click();ui_choose(denied,'role')
    record('Storage denial does not prevent starting or playing',lambda:check(s(denied)['node']=='c1_role'));denied.close()
    corrupt=new_page(stored={'catgpt.game.v1':'{"broken":true}'})
    record('Corrupt save is reported, not executed or silently overwritten',lambda:check(not s(corrupt)['started'] and corrupt.evaluate('window.__store.get("catgpt.game.v1")')=='{"broken":true}'));corrupt.close()

    imp=new_page(390,844);imp.locator('#startButton').click();ui_choose(imp,'role');before=s(imp)
    imp.locator('#saveFile').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"format":"CATGPT_TED_GAME","schema":1,"events":[{"type":"evil","r":0}],"endings":[]}'})
    imp.wait_for_timeout(100)
    record('Invalid imported actions are rejected without changing the live state',lambda:check(s(imp)==before and 'Nicht importiert' in imp.locator('#toast').inner_text()))
    imp.locator('#saveFile').set_input_files({'name':'chapter5.json','mimeType':'application/json','buffer':json.dumps(partial_finale).encode()});imp.locator('#confirmYes').click()
    record('Valid imported events resume at the exact final choice',lambda:check(s(imp)['node']=='c5_finale'))
    record('Final choice displays at least two reachable answer cards',lambda:check(imp.locator('#choices .choice').count()>=2))
    imp.locator('.top-tools [data-action="settings"]').click();imp.locator('#settingLarge').check()
    record('Large-text setting updates rendered story and remains overflow-free',lambda:check(imp.evaluate('document.body.classList.contains("large-text")&&document.documentElement.scrollWidth<=innerWidth')))
    imp.locator('#settingMotion').check()
    record('Reduced-motion preference is applied immediately',lambda:check(imp.evaluate('document.body.classList.contains("reduce-motion")')))
    def download_test():
        with imp.expect_download(timeout=5000) as info:imp.locator('#exportSave').click()
        download=info.value;check(download.suggested_filename=='catgpt-spielstand.json');raw=Path(download.path()).read_text();decoded=json.loads(raw);check(decoded['format']=='CATGPT_TED_GAME' and decoded['events']==s(imp)['events'])
    record('Browser download produces a valid JSON game export',download_test)
    imp.locator('#settingsDialog [data-close]').click();imp.locator('.mobile-menu').click()
    record('Mobile chapter menu exposes reached chapters and documents',lambda:check(imp.locator('#navigationDialog').is_visible() and imp.locator('#mobileChapterNav [data-chapter="5"]').is_enabled()))
    imp.locator('#navigationDialog [data-action="documents"]').click()
    record('Documents remain readable on mobile, including actual recognition',lambda:check(imp.locator('#document-credit').is_visible() and 'Mitsprache' in imp.locator('#document-credit').inner_text()))
    imp.keyboard.press('Escape');imp.locator('.mobile-profile-button').click()
    record('Mobile Ted profile shows all three live statistic meters',lambda:check(imp.locator('#profileDialog').is_visible() and imp.locator('#profileStats [role="meter"]').count()==3))
    imp.keyboard.press('Escape');imp.close()

    play=new_page();play.locator('#startButton').click()
    def complete_real_play():
        for event in fixtures['founder']['events'][1:]:
            typ=event['type']
            if typ=='choose':ui_choose(play,event['id'])
            elif typ=='it_inspect':play.locator('#inspect-'+event['item']).click()
            elif typ=='it_add':play.locator(f'[data-step="{event["step"]}"]').click()
            elif typ=='it_test':play.locator('#itSubmit').click()
            elif typ=='pitch_select':
                stage=['product','audience','promise'].index(event['group']);play.locator(f'#pitch-tab-{stage}').click();play.locator(f'#pitch-card-{event["group"]}-{event["value"]}').click()
            elif typ=='pitch_submit':play.locator('#pitchSubmit').click()
            elif typ=='fire_act':play.locator(f'[data-tool="{event["tool"]}"]').click()
            elif typ=='fire_next':play.locator('#fireNext').click()
            else:raise AssertionError(f'Unhandled action: {event}')
        check(s(play)['complete']);check(s(play)['ending']=='founder');check(len(s(play)['photos'])==22)
    record('Complete founder playthrough works through every actual button and minigame',complete_real_play)
    record('End screen shows receipt and the reached ending, not a dead end',lambda:check(play.locator('.receipt').count()==1 and 'Mitgründer' in play.locator('.receipt').inner_text() and play.locator('#choices button').count()==3))
    play.screenshot(path=str(OUT/'ending-desktop.png'),full_page=True)
    for ending in ['human','rest','exit']:
        ending_pg=new_page(stored={'catgpt.game.v1':json.dumps(fixtures[ending])});ending_pg.locator('#startButton').click()
        record(f'End screen {ending}: successful rendering with its own ending text',lambda ep=ending_pg,name=ending:check(s(ep)['ending']==name and ep.locator('.receipt').count()==1));ending_pg.close()
    play.close()

    layout=new_page()
    for width,height in [(1440,960),(1280,720),(1024,768),(768,1024),(700,900),(390,844),(360,740),(320,640)]:
        layout.set_viewport_size({'width':width,'height':height})
        record(f'Home layout {width}×{height}: no horizontal overflow',lambda:check(layout.evaluate('document.documentElement.scrollWidth<=innerWidth')))
    layout.set_viewport_size({'width':390,'height':844});layout.screenshot(path=str(OUT/'home-mobile.png'),full_page=True);layout.locator('#startButton').click()
    for width,height in [(1440,960),(768,1024),(390,844),(360,740),(320,640)]:
        layout.set_viewport_size({'width':width,'height':height})
        record(f'Story layout {width}×{height}: controls stay inside the viewport',lambda:check(layout.evaluate('document.documentElement.scrollWidth<=innerWidth && document.getElementById("decisionDock").getBoundingClientRect().bottom<=innerHeight+1')))
    layout.set_viewport_size({'width':390,'height':844});layout.screenshot(path=str(OUT/'story-mobile.png'),full_page=True)
    layout.locator('.top-tools [data-action="gallery"]').click();layout.screenshot(path=str(OUT/'gallery-mobile.png'),full_page=True)
    layout.set_viewport_size({'width':1440,'height':960});layout.screenshot(path=str(OUT/'gallery-desktop.png'),full_page=True);layout.close()
    record('No runtime JavaScript errors across all browser scenarios',lambda:check(not errors,str(errors)))
    record('No external HTTP or HTTPS requests during any game scenario',lambda:check(not requests,str(requests)))
    browser.close()

report={'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'total':len(results),'environment':'Chromium via set_content; exact delivered HTML, explicit memory/denied-storage adapters; managed file/http navigation blocked','results':results,'runtime_errors':errors,'network_requests':requests}
(OUT/'browser-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['results']},ensure_ascii=False,indent=2),flush=True)
raise SystemExit(1 if report['failed'] else 0)
