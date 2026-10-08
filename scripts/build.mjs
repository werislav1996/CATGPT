import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const file=path.join(root,'catgpt.html');let html=fs.readFileSync(file,'utf8');
const insert=(name,content,before)=>{const start=`<!-- BEGIN ${name} -->`,end=`<!-- END ${name} -->`;const block=`${start}\n${content}\n${end}\n`;if(html.includes(start)){const a=html.indexOf(start),b=html.indexOf(end,a)+end.length;html=html.slice(0,a)+block.trimEnd()+html.slice(b);}else{if(!html.includes(before))throw Error(`Missing anchor: ${before}`);html=html.replace(before,block+before);}};
insert('MOBILE_STYLE',`<style id="mobileStyle">\n${fs.readFileSync(path.join(root,'src/mobile.css'),'utf8')}\n</style>`,'</head>');
insert('CAT_AUDIO',`<script id="catAudio">\n${fs.readFileSync(path.join(root,'src/audio.js'),'utf8')}\n</script>`,'<script id="gameUI">');
for(const [name,filename] of [['STORY_EDITION','story.js'],['SCENE_EDITION','scene-ui.js']]){
 const start=`/* BEGIN ${name} */`,end=`/* END ${name} */`;const content=`${start}\n${fs.readFileSync(path.join(root,'src',filename),'utf8')}\n${end}`;
 if(!html.includes(start))throw Error(`Missing ${name} anchor`);
 const a=html.indexOf(start),b=html.indexOf(end,a)+end.length;html=html.slice(0,a)+content+html.slice(b);
}
fs.writeFileSync(file,html);
console.log('Built single-file CATGPT (CSS, story, UI and synthesized audio embedded).');
