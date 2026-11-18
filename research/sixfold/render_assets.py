"""Produce the numbered still library and six films, with a local selection gallery."""
import argparse
import csv
import hashlib
import html
import json
import math
from pathlib import Path
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageOps
from gpu_renderer import Renderer

HERE=Path(__file__).resolve().parent
FORMATS={"landscape":(1280,720,34),"square":(1280,1280,33),"portrait":(720,1280,33)}
VIEWS={1:"Twin passages",2:"Endless descent",3:"Winding light",4:"Tunnel interior",5:"Sculpture orbit"}
FILMS=[{"slug":"01-chromatic-descent","title":"Chromatic descent","mode":2,"seconds":48,
        "palettes":["original","glacier","cobalt","violet","orchid","original"],"loop":True},
       {"slug":"02-through-the-passage","title":"Through the passage","mode":4,"seconds":36,
        "palettes":["verdigris","moonstone","rose","original"],"loop":False}]


def write_json(path,data):
    temp=path.with_suffix(".tmp")
    temp.write_text(json.dumps(data,indent=2),encoding="utf8")
    temp.replace(path)


def plan(palettes):
    records=[]
    names=list(palettes)
    for a,(aspect,(w,h,count)) in enumerate(FORMATS.items()):
        for i in range(count):
            mode=[5,2,4,3,5,2,1,2][i%8]
            palette=names[(i*3+i//10+a*2)%len(names)]
            phase=(.037+i*.073+a*.113)%1.
            composition=[1.,0.,0.,0.]
            if mode==5:
                phase=(.04+i*.381966+a*.19)%1.
                composition[0]=.88 if i%8==0 else .72
                if i%8==4:
                    composition[1]=-.20 if aspect=="landscape" else .06
                    composition[2]=.14 if aspect=="portrait" else .025
            elif mode==4:
                phase=.04+.91*((i*.381966+a*.17)%1.)
            elif mode==1:
                composition[0]=.92
                composition[3]=[-.08,0.,.08][(i//8)%3]
            elif mode==2:
                composition[0]=[.91,1.,1.12][(i//8)%3]
                composition[1]=.025*math.sin(i)
                composition[3]=.04*math.cos(i)
            number=len(records)+1
            name=f"{number:03d}-{palette}-{VIEWS[mode].lower().replace(' ','-')}"
            records.append({"id":f"S{number:03d}","aspect":aspect,"width":w,"height":h,
                            "mode":mode,"view":VIEWS[mode],"palette":palette,
                            "palette_label":palettes[palette]["label"],"phase":phase,
                            "composition":composition,"name":name,
                            "image":f"{aspect}/stills/{name}.jpg",
                            "master":f"{aspect}/masters/{name}.png",
                            "thumbnail":f"thumbnails/{name}.jpg"})
    return records


def jpeg_export(ffmpeg,source,target,w,h):
    partial=target.with_name(target.stem+".partial.jpg")
    subprocess.run([ffmpeg,"-hide_banner","-loglevel","error","-y","-threads","1","-i",str(source),
                    "-filter_threads","1","-vf",f"scale={w}:{h}:flags=lanczos",
                    "-frames:v","1","-q:v","2","-pix_fmt","yuvj444p","-threads","2",str(partial)],check=True)
    partial.replace(target)


def font(size):
    return ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf",size)


def contact_sheets(root,records):
    (root/"contact-sheets").mkdir(exist_ok=True)
    groups=[("all-100",records,10,160,150)]
    for aspect in FORMATS:
        groups.append((aspect,[r for r in records if r["aspect"]==aspect],6,240,250))
    for name,rows,cols,cw,ch in groups:
        page=Image.new("RGB",(cols*cw,64+math.ceil(len(rows)/cols)*ch),(15,18,23))
        draw=ImageDraw.Draw(page)
        draw.text((16,15),f"SIXFOLD  /  {name.upper().replace('-',' ')}",font=font(23),fill=(230,235,239))
        for i,r in enumerate(rows):
            im=Image.open(root/r["thumbnail"])
            im.thumbnail((cw-16,ch-50),Image.Resampling.LANCZOS)
            x=(i%cols)*cw; y=64+(i//cols)*ch
            page.paste(im,(x+(cw-im.width)//2,y+(ch-50-im.height)//2))
            draw.text((x+8,y+ch-43),r["id"]+"  "+r["palette"],font=font(14),fill=(220,227,231))
            draw.text((x+8,y+ch-24),r["view"],font=font(12),fill=(142,157,168))
        page.save(root/"contact-sheets"/(name+".jpg"),quality=94)


def gallery(root,records):
    cards=[]
    for r in records:
        cards.append(f'''<article class="card" data-aspect="{r['aspect']}" data-id="{r['id']}">
<a href="{r['image']}" target="_blank"><img src="{r['thumbnail']}" alt="{html.escape(r['palette_label']+' / '+r['view'])}" loading="lazy"></a>
<div class="caption"><strong>{r['id']} <span>{html.escape(r['palette_label'])}</span></strong>
<small>{r['view']} · {r['aspect']}</small><div class="actions"><button data-pick="{r['id']}" aria-pressed="false">☆ Favourite</button><a href="{r['master']}" target="_blank">PNG master</a></div></div></article>''')
    videos=[]
    for aspect in FORMATS:
        for film in FILMS:
            path=f"{aspect}/videos/{film['slug']}.mp4"
            poster=f"{aspect}/posters/{film['slug']}.jpg"
            player=(f'<video controls preload="none" poster="{poster}" src="{path}"></video>'
                    if (root/path).exists() else '<div class="pending">Rendering</div>')
            videos.append(f'<article class="film">{player}<p><strong>{film["title"]}</strong><br>{aspect} · {film["seconds"]} seconds'+(' · loop' if film['loop'] else '')+'</p></article>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixfold — Select your favourites</title><style>
:root{color-scheme:dark;font-family:Segoe UI,system-ui,sans-serif;background:#0d1217;color:#edf1f4}*{box-sizing:border-box}body{margin:0;padding:38px 4vw 80px}header{max-width:850px;margin-bottom:28px}.eyebrow{color:#87bfb5;letter-spacing:.2em;font-size:12px}h1{font-weight:400;font-size:clamp(32px,4vw,54px);margin:12px 0}p{color:#a8b7c1;line-height:1.6}a{color:#95d2c6;text-decoration:none}a:hover{text-decoration:underline}button{border:1px solid #33454f;background:#18242d;color:#e4edf1;padding:9px 12px;border-radius:5px;cursor:pointer}button:hover,button.active{background:#29493f;border-color:#82b6a3}.toolbar{display:flex;gap:8px;flex-wrap:wrap;padding:14px 0;position:sticky;top:0;background:#0d1217f5;z-index:2}.count{align-self:center;margin-left:auto;color:#a8b7c1}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:18px}.card{border:1px solid #26333c;border-radius:8px;overflow:hidden;background:#121b22}.card>a{display:flex;height:240px;align-items:center;justify-content:center;background:#060b0f}.card img{max-height:100%;max-width:100%;object-fit:contain}.caption{padding:14px}.caption strong{display:block;font-size:14px}.caption strong span{font-weight:400;color:#c2cbd2;margin-left:6px}small{display:block;color:#93a5b0;margin-top:6px}.actions{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:14px;font-size:12px}.actions button{font-size:12px}.card.picked{border-color:#91d6be}.card[hidden]{display:none}.film-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin-bottom:38px}.film{padding:12px;background:#121b22;border:1px solid #26333c;border-radius:8px}.film video{width:100%;height:240px;object-fit:contain;background:#060b0f}.film p{margin:10px 4px 2px}.pending{height:240px;display:grid;place-items:center;color:#83959f;background:#060b0f}h2{font-weight:400;margin-top:48px}.note{font-size:13px}footer{margin-top:40px;color:#93a5b0}
</style><header><div class="eyebrow">SIXFOLD / EDITION 01</div><h1>One geometry. A hundred ways in.</h1>
<p>100 stills and six films, composed for landscape, square and portrait. Click an image to open the full-size JPEG. Mark favourites, then download your selection or send the image numbers.</p>
<p class="note">Contact sheets: <a href="contact-sheets/all-100.jpg">All 100</a> · <a href="contact-sheets/landscape.jpg">Landscape</a> · <a href="contact-sheets/square.jpg">Square</a> · <a href="contact-sheets/portrait.jpg">Portrait</a></p></header>
<nav class="toolbar" aria-label="Image filters"><button class="active" data-filter="all">All</button><button data-filter="landscape">Landscape</button><button data-filter="square">Square</button><button data-filter="portrait">Portrait</button><button id="only">Favourites only</button><button id="download">Download selection</button><span class="count" id="count"></span></nav>
<main class="grid">'''+"\n".join(cards)+'''</main><h2>Motion studies</h2><p>Chromatic descent moves through a changing palette and returns to its starting colours. Through the passage travels inside the geometry, then turns back toward the sculpture. All films are silent.</p><section class="film-grid">'''+"\n".join(videos)+r'''</section>
<footer>JPEGs: 1920 × 1080 / 1920 × 1920 / 1080 × 1920. Native PNG masters are included. <a href="catalogue.csv">Download catalogue</a> · <a href="README.txt">Asset notes</a></footer>
<script>
let saved=[];try{saved=JSON.parse(localStorage.getItem('sixfold-edition01-picks')||'[]')}catch(e){}
const picked=new Set(saved);let aspect='all',only=false;const cards=[...document.querySelectorAll('.card')];
function update(){let visible=0;for(const card of cards){const selected=picked.has(card.dataset.id);card.classList.toggle('picked',selected);card.hidden=(aspect!=='all'&&card.dataset.aspect!==aspect)||(only&&!selected);if(!card.hidden)visible++;const b=card.querySelector('button');b.textContent=selected?'★ Favourite':'☆ Favourite';b.setAttribute('aria-pressed',String(selected))}document.querySelector('#count').textContent=visible+' shown · '+picked.size+' favourites';try{localStorage.setItem('sixfold-edition01-picks',JSON.stringify([...picked]))}catch(e){}}
document.querySelectorAll('[data-pick]').forEach(b=>b.addEventListener('click',()=>{picked.has(b.dataset.pick)?picked.delete(b.dataset.pick):picked.add(b.dataset.pick);update()}));
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{aspect=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(t=>t.classList.toggle('active',t===b));update()}));
document.querySelector('#only').addEventListener('click',e=>{only=!only;e.target.classList.toggle('active',only);update()});
document.querySelector('#download').addEventListener('click',()=>{const blob=new Blob(['Sixfold favourites\n\n'+[...picked].sort().join('\n')+'\n'],{type:'text/plain'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='Sixfold-favourites.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});update();
</script></html>'''
    (root/"index.html").write_text(page,encoding="utf8")


def blend_palette(a,b,t):
    t=t*t*(3.-2.*t)
    result={}
    for key in ("backdrop","trace"):
        result[key]=[(1-t)*x+t*y for x,y in zip(a[key],b[key])]
    result["lobes"]=[[(1-t)*x+t*y for x,y in zip(aa,bb)] for aa,bb in zip(a["lobes"],b["lobes"])]
    result["exposure"]=(1-t)*a.get("exposure",1.)+t*b.get("exposure",1.)
    return result


def video(root,aspect,film,palettes,ffmpeg,status):
    w,h,_=FORMATS[aspect]; fps=30; count=fps*film["seconds"]
    target=root/aspect/"videos"/(film["slug"]+".mp4")
    poster=root/aspect/"posters"/(film["slug"]+".jpg")
    if target.exists() and poster.exists():
        return
    renderer=Renderer(w,h,samples=2)
    partial=target.with_name(target.stem+".partial.mp4")
    vf=f"vflip,scale={round(w*1.5)}:{round(h*1.5)}:flags=lanczos:out_color_matrix=bt709,setsar=1"
    if not film["loop"]:
        vf+=f",fade=t=in:st=0:d=0.7,fade=t=out:st={film['seconds']-1}:d=1"
    command=[ffmpeg,"-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24",
             "-s",f"{w}x{h}","-r",str(fps),"-i","-","-filter_threads","2","-vf",vf,"-an",
             "-c:v","libx264","-preset","fast","-crf","17","-threads","2",
             "-x264-params","rc-lookahead=8:sync-lookahead=0:ref=2:bframes=2","-pix_fmt","yuv420p",
             "-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-color_range","tv",
             "-movflags","+faststart","-metadata",f"title=Sixfold - {film['title']}",
             "-metadata",f"comment=Native {w}x{h}; FFmpeg Lanczos 1.5x enlargement; two subpixel samples",str(partial)]
    stops=[palettes[name] for name in film["palettes"]]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as encoder:
        for i in range(count):
            phase=i/count
            position=phase*(len(stops)-1); segment=min(len(stops)-2,int(position))
            renderer.colours(blend_palette(stops[segment],stops[segment+1],position-segment))
            encoder.stdin.write(renderer.frame(phase,film["mode"]))
            if i%90==0 or i==count-1:
                status.update(task=f"{aspect} / {film['title']}",frame=i+1,frames=count)
                write_json(root/"progress.json",status)
                print(f"{aspect} {film['slug']} {i+1}/{count}",flush=True)
        encoder.stdin.close()
        if encoder.wait():
            raise RuntimeError(f"Encoding failed: {target}")
    partial.replace(target)
    renderer.close()
    subprocess.run([ffmpeg,"-hide_banner","-loglevel","error","-y","-ss",str(film["seconds"]*.35),
                    "-threads","1","-i",str(target),"-frames:v","1","-q:v","2","-threads","2",str(poster)],check=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder",type=Path)
    parser.add_argument("--stills-only",action="store_true")
    parser.add_argument("--videos-only",action="store_true",help="Resume films without opening GPU contexts for finished stills")
    parser.add_argument("--aspect",choices=list(FORMATS),help="Render films for one format only")
    parser.add_argument("--film",choices=[f["slug"] for f in FILMS],help="Render one film only")
    args=parser.parse_args(); root=args.folder.resolve(); root.mkdir(parents=True,exist_ok=True)
    palettes=json.loads((HERE/"palettes.json").read_text())
    records=plan(palettes)
    signature=hashlib.sha256(b"".join((HERE/p).read_bytes() for p in
        ["sculpture.frag","gpu_renderer.py","palettes.json","reference.glsl","field.png","contact_curve.png"])
        +json.dumps([records,FILMS]).encode()).hexdigest()
    receipt=root/"source"/"manifest.json"
    if receipt.exists() and json.loads(receipt.read_text())["signature"]!=signature:
        raise RuntimeError("Source changed. Use a new collection folder to keep previous selections intact.")
    for aspect in FORMATS:
        for name in ("stills","masters","videos","posters"):
            (root/aspect/name).mkdir(parents=True,exist_ok=True)
    for name in ("source","thumbnails"):
        (root/name).mkdir(exist_ok=True)
    write_json(receipt,{"signature":signature,"stills":records,"films":FILMS,"formats":FORMATS})
    write_json(root/"source"/"palettes.json",palettes)
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    status={"state":"running","stills_done":0,"stills_total":100,"videos_done":0,"videos_total":6}
    status["videos_done"]=sum((root/a/"videos"/(f["slug"]+".mp4")).exists()
                              and (root/a/"posters"/(f["slug"]+".jpg")).exists()
                              for a in FORMATS for f in FILMS)
    for aspect,(w,h,_) in FORMATS.items():
        renderer=None
        for r in [v for v in records if v["aspect"]==aspect]:
            master=root/r["master"]; target=root/r["image"]; thumb=root/r["thumbnail"]
            if not (master.exists() and target.exists() and thumb.exists()):
                if args.videos_only:
                    raise RuntimeError(f"Missing still {r['id']}; run without --videos-only first")
                if renderer is None:
                    renderer=Renderer(w,h,samples=4)
                renderer.colours(palettes[r["palette"]])
                im=renderer.image(r["phase"],r["mode"],r["composition"])
                partial=master.with_name(master.stem+".partial.png")
                im.save(partial); partial.replace(master)
                jpeg_export(ffmpeg,master,target,round(w*1.5),round(h*1.5))
                im.thumbnail((480,400),Image.Resampling.LANCZOS)
                im.save(thumb,quality=89)
            status.update(task=r["id"],stills_done=status["stills_done"]+1)
            write_json(root/"progress.json",status)
            print(f"Still {r['id']} / 100",flush=True)
        if renderer is not None:
            renderer.close()
    with (root/"catalogue.csv").open("w",encoding="utf-8-sig",newline="") as stream:
        fields=["id","aspect","palette_label","view","phase","image","master"]
        writer=csv.DictWriter(stream,fieldnames=fields,extrasaction="ignore")
        writer.writeheader();writer.writerows(records)
    (root/"README.txt").write_text(
        "SIXFOLD / EDITION 01\n\n100 unique compositions: 34 landscape, 33 square, 33 portrait.\n"
        "Open index.html to browse, filter and mark favourites. Download your selection as a text file, or send the S001-S100 numbers.\n"
        "Favourites are stored in this browser when local storage is available; download the list to keep a portable copy.\n\n"
        "Each aspect folder contains:\n  stills: full-size JPEGs for use and selection.\n"
        "  masters: lossless native PNGs of the same 100 compositions.\n  videos: two H.264 MP4s at 30 fps, without audio or text.\n"
        "  posters: still frames from those movies for website thumbnails.\n\n"
        "Landscape: native 1280x720, delivered 1920x1080.\nSquare: native 1280x1280, delivered 1920x1920.\n"
        "Portrait: native 720x1280, delivered 1080x1920.\nAll enlargement uses FFmpeg Lanczos. Native rendering never exceeds 1280 on either side.\n"
        "Stills average four subpixel samples at native resolution; films average two. Upscaling adds no new geometric detail.\n\n"
        "Chromatic descent: 48-second loop; copper/teal, glacier, cobalt, violet, orchid, copper/teal.\n"
        "Through the passage: 36-second journey with a turn back toward the sculpture and short opening/closing fades; verdigris, moonstone, rose gold, copper/teal.\n"
        "The tunnel follows phase 09's clear line through (1,0,h), in direction (-1,0,1). Two extra geometric levels improve close-wall detail.\n\n"
        "catalogue.csv maps image IDs to files. source/manifest.json and source/palettes.json record the render recipes.\n",
        encoding="utf8")
    contact_sheets(root,records);gallery(root,records)
    if not args.stills_only:
        for aspect in FORMATS:
            for film in FILMS:
                if (args.aspect and args.aspect!=aspect) or (args.film and args.film!=film["slug"]):
                    continue
                video(root,aspect,film,palettes,ffmpeg,status)
                status["videos_done"]=sum((root/a/"videos"/(f["slug"]+".mp4")).exists()
                                          and (root/a/"posters"/(f["slug"]+".jpg")).exists()
                                          for a in FORMATS for f in FILMS)
                write_json(root/"progress.json",status)
                gallery(root,records)
    status.update(state="complete" if status["videos_done"]==6 or args.stills_only else "partial",task="Finished requested batch")
    write_json(root/"progress.json",status)
    print("Collection complete",flush=True)


if __name__=="__main__":
    main()
