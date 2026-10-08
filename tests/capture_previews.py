from pathlib import Path
from playwright.sync_api import sync_playwright
import json,shutil
R=Path(__file__).resolve().parents[1];O=R/'results';HTML=(R/'catgpt.html').read_text();fixture=json.loads((O/'fixtures/founder.json').read_text())
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':960});page.set_content(HTML,wait_until='load')
 packs=page.evaluate('''f=>{let s=CatGame.fresh(),out={};for(const e of f.events){s=CatGame.reduce(s,e);if(!out[s.node])out[s.node]=CatGame.pack(s);}return out;}''',fixture);page.close()
 def capture(node,name,w=1440,h=960,gallery=False,read=False):
  page=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
  page.evaluate('''raw=>{const store=new Map(raw?[['catgpt.game.v2',JSON.stringify(raw)]]:[]);Object.defineProperty(window,'localStorage',{value:{getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,String(v)),removeItem:k=>store.delete(k)},configurable:true});}''',packs.get(node))
  page.set_content(HTML,wait_until='load')
  if node:page.locator('#startButton').click()
  if gallery:page.locator('.top-tools [data-action="gallery"]').click()
  if read:page.locator('#readScene').click()
  page.wait_for_timeout(500);page.screenshot(path=str(O/name));page.close()
 capture('c2_desk','preview-desktop.png');capture('c2_portfolio','preview-team.png');capture('c2_hq','preview-closet.png')
 capture('c2_portfolio','preview-mobile.png',390,844);capture('c2_portfolio','preview-mobile-dialogue.png',390,844,read=True)
 capture(None,'preview-start.png');capture(None,'preview-gallery.png',gallery=True)
 b.close()
