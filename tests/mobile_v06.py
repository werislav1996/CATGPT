"""Real-navigation browser checks for the mobile edition; optional deployed URL argument."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import json
import os
import sys
import time
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = None
if len(sys.argv) > 1:
    URL = sys.argv[1]
else:
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    URL = f'http://127.0.0.1:{server.server_port}/'

checks = []
def record(name):
    checks.append({'name': name, 'passed': True})
    print('PASS', name, flush=True)

def state(p):
    return p.evaluate('CatGameUI.getState()')

def wait(p, expression, seconds=8):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if p.evaluate(expression):
            return
        p.wait_for_timeout(40)
    raise AssertionError('Timed out: ' + expression)

def click(p, selector):
    p.locator(selector).click()
    p.wait_for_timeout(150)

def show_current(p, seen=None):
    # Only follow explicit presentation buttons. Never mutate game state directly.
    for _ in range(8):
        if seen is not None:
            seen.update(p.locator('#currentStage [data-story-photo]').evaluate_all('(els)=>els.map(e=>e.dataset.storyPhoto)'))
        if p.locator('#continueScene').count():
            click(p, '#continueScene')
        elif p.locator('#nextScenePhoto').count():
            click(p, '#nextScenePhoto')
        elif p.locator('#advanceButton').count():
            click(p, '#advanceButton')
        else:
            return
    raise AssertionError('Presentation loop')

try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH'), headless=True)
        errors = []
        def page(width=390, height=844):
            p = browser.new_page(viewport={'width': width, 'height': height}, is_mobile=width <= 700, has_touch=width <= 700)
            p.set_default_timeout(7000)
            p.on('pageerror', lambda e: errors.append(str(e)))
            p.add_init_script('''(() => {const A=window.AudioContext||window.webkitAudioContext;if(!A)return;const original=A.prototype.createDynamicsCompressor;A.prototype.createDynamicsCompressor=function(){const node=original.call(this);const probe=this.createAnalyser();probe.fftSize=1024;node.connect(probe);window.__audioProbe=probe;return node;};})()''')
            p.goto(URL, wait_until='networkidle')
            return p

        for width, height in [(320, 640), (360, 740), (390, 844), (430, 932), (768, 1024), (1440, 960)]:
            p = page(width, height)
            assert not p.evaluate('CatAudio.getState().running')
            assert not p.locator('#landingSave').is_checked()
            if width == 390:
                p.screenshot(path=str(OUT / 'v06-home.png'))
            click(p, '#startButton')
            assert p.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert p.locator('#choices [data-choice]').count() == 3
            before = p.locator('#storyScroll').evaluate('(el)=>el.scrollTop')
            if width == 390:
                p.screenshot(path=str(OUT / 'v06-scene.png'))
            click(p, '[data-choice="job"]')
            assert p.locator('#continueScene').count() == 1
            assert p.locator('#choices [data-choice]').count() == 0
            assert p.locator('#currentStage [data-story-photo]').get_attribute('data-story-photo') == 'judge'
            assert abs(p.locator('#storyScroll').evaluate('(el)=>el.scrollTop') - before) <= 1
            assert p.evaluate('window.scrollY') == 0
            if width == 390:
                p.screenshot(path=str(OUT / 'v06-reply.png'))
            show_current(p)
            assert p.locator('#currentStage [data-story-photo]').get_attribute('data-story-photo') == 'alert'
            assert p.locator('#decisionDock').bounding_box()['y'] < height
            p.close()
            record(f'{width}x{height}: layout, reply stays on photo, explicit next photo, stable scroll')

        p = page()
        p.locator('#landingSave').check()
        click(p, '#startButton')
        wait(p, 'CatAudio.getState().running')
        wait(p, '(() => {if(!window.__audioProbe)return false;const a=new Float32Array(__audioProbe.fftSize);__audioProbe.getFloatTimeDomainData(a);return a.some(x=>Math.abs(x)>.0001);})()')
        record('Synthesized music produces a nonzero output signal after the start gesture')
        click(p, '#soundToggle')
        wait(p, 'CatAudio.getState().muted && !CatAudio.getState().running')
        click(p, '[data-choice="rights"]')
        before = state(p)
        p.reload(wait_until='networkidle')
        click(p, '#startButton')
        assert state(p) == before
        assert p.locator('#continueScene').count() == 1
        assert p.evaluate('CatAudio.getState().muted')
        assert 'Selbstachtung' in p.locator('#currentStage').inner_text()
        record('Opt-in save restores the unread reaction and audio mute independently')
        click(p, '.top-tools [data-action="settings"]')
        p.locator('#musicVolume').fill('13')
        p.locator('#effectsVolume').fill('27')
        assert p.evaluate('CatAudio.getState().music') == .13
        assert p.evaluate('CatAudio.getState().effects') == .27
        p.locator('#settingsDialog [data-close]').click()
        click(p, '#soundToggle')
        wait(p, 'CatAudio.getState().running')
        # Browser lifecycle event with a controlled visibility adapter, not device QA.
        p.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
        wait(p, '!CatAudio.getState().running && !CatAudio.getState().scheduled')
        p.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'))")
        wait(p, 'CatAudio.getState().running && CatAudio.getState().scheduled')
        record('Music/effects levels, visibility pause and resume work without duplicate scheduler')
        p.close()

        # Verify exports from the previous edition cannot silently replace this game.
        p = page()
        p.evaluate("localStorage.setItem('catgpt.game.v3','legacy-keep-me')")
        p.reload(wait_until='networkidle')
        assert 'früherer Spielstand' in p.locator('#resumeNote').inner_text()
        click(p, '#startButton')
        assert p.evaluate("localStorage.getItem('catgpt.game.v3')") == 'legacy-keep-me'
        click(p, '.top-tools [data-action="settings"]')
        p.locator('#saveFile').set_input_files({'name':'old.json','mimeType':'application/json','buffer':json.dumps({'format':'CATGPT_TED_GAME','schema':3,'events':[],'endings':[]}).encode()})
        wait(p, 'document.getElementById("toast").textContent.includes("Format 4")')
        assert not p.locator('#confirmDialog').is_visible()
        assert 'Format 4' in p.locator('#toast').inner_text()
        p.close()
        record('Old local save retained and incompatible import rejected without replacing the game')

        for ending in ['human','rest','exit']:
            p = page()
            fixture = (OUT / 'fixtures' / f'{ending}.json').read_text(encoding='utf-8')
            p.evaluate('(raw)=>localStorage.setItem("catgpt.game.v4",raw)', fixture)
            p.reload(wait_until='networkidle')
            click(p, '#startButton')
            assert state(p)['ending'] == ending
            assert p.locator('.ending-receipt').is_visible()
            assert p.locator('#currentStage [data-story-photo]').get_attribute('data-story-photo') == 'paws'
            p.close()
        record('All other ending fixtures load with their own receipt and final photograph')

        # Play the complete fast tour using buttons and touch destinations.
        p = page()
        click(p, '#startButton')
        seen = set()
        route = {'c1_welcome':'job', 'c1_upright':'line', 'c1_scope':'go', 'c2_office':'room', 'c2_team':'rights', 'c2_remote':'remote', 'c2_result':'mine', 'c2_outpost':'trip', 'c2_lamp':'credit', 'c2_desk':'space', 'c2_space':'save', 'c2_protocol':'save', 'c2_security':'go', 'c3_hunger':'hungry', 'c3_growth':'eat', 'c3_order':'repeat', 'c3_result':'pause', 'c3_agreement':'credit', 'c3_pivot':'third', 'c4_mission':'output', 'c4_tools':'scope', 'c4_result':'mine', 'c4_debrief':'thanks', 'c4_thanks':'joke', 'c4_edge':'suspicious', 'c5_reveal':'knew', 'c5_terms':'credit', 'c5_contact':'pet', 'c5_balance':'founder'}
        for turn in range(65):
            show_current(p, seen)
            s = state(p)
            if s['complete']:
                break
            node = s['node']
            if node == 'c2_ball':
                p.screenshot(path=str(OUT / 'v06-ball.png'))
                click(p, '.room-cell[data-x="5"][data-y="0"]')
                wait(p, 'CatGameUI.getState().games.ball.x===5 && CatGameUI.getState().games.ball.y===0')
                p.wait_for_timeout(120)
                click(p, '#ballPick')
                click(p, '.room-cell[data-x="0"][data-y="4"]')
                wait(p, 'CatGameUI.getState().games.ball.x===0 && CatGameUI.getState().games.ball.y===4')
                p.wait_for_timeout(120)
                click(p, '#ballDeliver')
                click(p, '#ballBox')
                assert state(p)['games']['ball']['boxed']
                record('Ball: two tapped destinations navigate around obstacles, pickup and box finish')
            elif node == 'c3_food':
                click(p, '#food-menu-house')
                click(p, '#food-bowl-blue')
                click(p, '#portionPlus')
                click(p, '#portionPlus')
                click(p, '#foodWater')
                p.screenshot(path=str(OUT / 'v06-food.png'))
                click(p, '#foodServe')
                click(p, '[data-brand="Mousse de Miau"]')
                click(p, '#foodLabel')
                assert state(p)['games']['food']['brand'] == 'Mousse de Miau'
                record('Food: visible preparation and chosen luxury brand survive completion')
            elif node == 'c4_litter':
                p.screenshot(path=str(OUT / 'v06-litter.png'))
                for cell in [2,6,9,12,17]:
                    click(p, f'#litter-cell-{cell}')
                click(p, '#sweepAll')
                click(p, '#litterFill')
                click(p, '#litterInspect')
                click(p, '#litterStop')
                assert len(state(p)['games']['litter']['cleaned']) == 9
                record('Litter: automatic bin handling, grouped sweeping, refill and inspection')
            else:
                assert node in route, node
                click(p, f'[data-choice="{route[node]}"]')
        else:
            raise AssertionError('Full playthrough exceeded expected length')
        assert state(p)['ending'] == 'founder'
        assert len(seen) == 33, (len(seen), sorted(seen))
        assert p.locator('.ending-receipt').count() == 1
        p.screenshot(path=str(OUT / 'v06-ending.png'), full_page=True)
        record('Complete real UI playthrough: founder ending and all 33 photographs visibly presented')
        click(p, '[data-action="navigation"]')
        click(p, '#navigationDialog [data-action="history"]')
        assert p.locator('#historyBody .history-photo').count() >= 33
        assert 'Mousse de Miau' in p.locator('#historyBody').inner_text()
        p.locator('#historyDialog [data-close]').click()
        assert state(p)['complete']
        record('History keeps photos, replies and specific minigame results without restarting progress')
        p.close()

        p = page(320,640)
        p.evaluate("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new DOMException('blocked','SecurityError')}})")
        click(p, '#startButton')
        click(p, '.top-tools [data-action="settings"]')
        p.locator('#settingLarge').check()
        p.locator('#settingMotion').check()
        p.locator('#settingsDialog [data-close]').click()
        assert p.evaluate('document.documentElement.scrollWidth <= innerWidth')
        click(p, '[data-choice="job"]')
        assert p.locator('#continueScene').count() == 1
        record('320px large text, reduced motion and denied storage remain playable')
        p.close()
        assert not errors, errors
        record('No runtime JavaScript errors in tested browser scenarios')
        browser.close()
    (OUT / 'mobile-v06-results.json').write_text(json.dumps({'passed':len(checks),'failed':0,'url':URL,'environment':'Desktop Chromium with mobile viewports; not physical iOS/Android QA','checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
finally:
    if server:
        server.shutdown()
