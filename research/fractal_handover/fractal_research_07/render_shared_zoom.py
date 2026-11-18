"""Finite views of selected, analytically rescaled copies around p.

Only the two common-fixed-point block maps are shown, not the entire zoomed
attractor. No claim about dimension is inferred from the rendered pixels.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import maximum_filter,gaussian_filter
from scipy.spatial.transform import Rotation

from geometry import ROOT,maps,parameters,word_map


def branch_cloud(base,A,B,m):
    rotations=[np.eye(3)]
    for _ in range(m):
        rotations=[a@b for a in rotations for b in [A,B]]
    # Undo the orientation of the all-F route as well as its contraction.
    # This keeps one exact copy aligned consistently in the two panels.
    frame=np.linalg.matrix_power(A,m).T
    points=np.concatenate([base@(frame@a).T for a in rotations])
    labels=np.repeat(np.arange(len(rotations))//(len(rotations)//2),len(base))
    return points,labels


def shade(points,labels,view,centre,scale,size):
    p=points@view.T
    x=np.rint(size/2+(p[:,0]-centre[0])*scale).astype(int)
    y=np.rint(size/2-(p[:,1]-centre[1])*scale).astype(int)
    assert x.min()>=0 and x.max()<size and y.min()>=0 and y.max()<size
    order=np.argsort(p[:,2])
    ranks=np.empty(len(points),dtype=np.int32);ranks[order]=np.arange(1,len(points)+1)
    buffer=np.zeros(size*size,dtype=np.int32)
    np.maximum.at(buffer,y*size+x,ranks)
    buffer=maximum_filter(buffer.reshape(size,size),size=2)
    mask=buffer>0
    source=order[buffer[mask]-1]
    z=(p[source,2]-p[:,2].min())/np.ptp(p[:,2])
    palette=np.array([[67.,182.,191.],[218.,141.,166.]])
    color=palette[labels[source]]*(.50+.50*z[:,None])
    color+=np.array([45.,48.,37.])[None,:]*z[:,None]**2
    image=np.empty((size,size,3));image[:]=[9,21,32]
    image+=gaussian_filter(mask.astype(float),1.0)[:,:,None]*[3,6,8]
    image[mask]=color
    return Image.fromarray(np.uint8(np.clip(image,0,255)))


def main():
    data=parameters();r,Q,b=maps();a=r*Q
    p=np.array([float(v) for v in data['reference_point']])
    fixed=np.linalg.solve(np.eye(3)-a[0],b[0])
    base=fixed[None,:]
    for _ in range(6):base=np.concatenate([base@m.T+t for m,t in zip(a,b)])
    base-=p
    A=word_map(data['word'],r,Q,b)[0]/r**8
    B=word_map(data['partner_word'],r,Q,b)[0]/r**8
    cases=[branch_cloud(base,A,B,m) for m in [1,5]]
    view=Rotation.from_euler('yx',[-28,28],degrees=True).as_matrix()
    projected=[cloud@view.T for cloud,_ in cases]
    low=np.min([q.min(axis=0) for q in projected],axis=0)
    high=np.max([q.max(axis=0) for q in projected],axis=0)
    centre=(low+high)/2
    size=1200;scale=(size-120)/max((high-low)[:2])
    canvas=Image.new('RGB',(size,2*size+390),(9,21,32))
    draw=ImageDraw.Draw(canvas)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    title=ImageFont.truetype(font,38);label=ImageFont.truetype(font,29)
    small=ImageFont.truetype(font,21)
    draw.text((50,35),'One shared point, increasingly crowded copies',font=title,fill=(230,240,238))
    draw.text((50,96),'Selected copies from the same fractal, magnified about the proven junction.',
              font=small,fill=(163,194,202))
    for index,((cloud,labels),m) in enumerate(zip(cases,[1,5])):
        top=160+index*(size+65)
        canvas.paste(shade(cloud,labels,view,centre,scale,size),(0,top))
        y=top-22
        draw.text((50,y),f'{2**m} block-word choices  |  scale r^{8*m}  |  rescaled view',
                  font=label,fill=(215,229,230))
        # The coordinate origin is the exact common fixed point in the
        # ideal rescaling; its annotation is distinct from cloud pixels.
        px=size/2-centre[0]*scale;py=top+size/2+centre[1]*scale
        draw.ellipse((px-7,py-7,px+7,py+7),fill=(245,200,105),outline=(255,234,180),width=2)
    foot=2*size+290
    draw.line((50,foot-16,size-50,foot-16),fill=(40,67,78),width=2)
    draw.text((50,foot),'Gold: the same fixed point. Each panel rescales and rotates the selected copies.',
              font=small,fill=(200,212,194))
    draw.text((50,foot+37),'Finite illustration of subsets of the zoomed set; pixel density is not a dimension proof.',
              font=small,fill=(146,176,186))
    canvas.save(ROOT/'shared_point_zoom.png')
    metadata={'base_K_points':len(base),'base_address_prefix_length':6,
              'block_counts':[1,5],'word_choices':[2,32],
              'linear_zoom_factors':[float(r**(-8*m)) for m in [1,5]],
              'point_counts':[len(c[0]) for c in cases],
              'coordinate_formula':'A^(-m) (G_blockword(x)-p) / r^(8m)',
              'scope':'Selected word-copy subsets, not the full zoomed attractor or a numerical dimension estimator.'}
    (ROOT/'zoom_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(metadata,indent=2),flush=True)


if __name__=='__main__':main()
