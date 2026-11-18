"""A finite, depth-shaded rendering of the actual six-map construction."""
from pathlib import Path
import json
import math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import maximum_filter,gaussian_filter
from scipy.spatial.transform import Rotation

ROOT=Path(__file__).resolve().parent
PALETTE=np.array([[61,185,189],[235,174,97],[128,156,227],
                  [222,121,113],[103,197,159],[178,143,216]],dtype=float)


def maps(data):
    r=float(data['reference_r']);u=float(data['reference_half_angle_tangent'])
    c=(1-u*u)/(1+u*u);s=2*u/(1+u*u)
    a=[];b=[]
    for k in range(6):
        phi=k*math.pi/3;sign=(-1)**k
        x,y=-math.sin(phi),math.cos(phi);w=1-c;ss=sign*s
        a.append(r*np.array([[c+x*x*w,x*y*w,y*ss],
                              [x*y*w,c+y*y*w,-x*ss],[-y*ss,x*ss,c]]))
        b.append([math.cos(phi),math.sin(phi),sign/math.sqrt(2)])
    return np.array(a),np.array(b)


def centres(a,b,depth):
    p=np.zeros((1,3))
    for _ in range(depth):
        p=(np.einsum('kij,nj->kni',a,p)+b[:,None,:]).reshape(-1,3)
    return p


def point_image(points,labels,size=1400):
    view=Rotation.from_euler('yx',[-28,28],degrees=True).as_matrix()
    projected=points@view.T
    centre=(projected.max(axis=0)+projected.min(axis=0))/2
    scale=(size-100)/max(np.ptp(projected[:,0]),np.ptp(projected[:,1]))
    px=np.rint(size/2+(projected[:,0]-centre[0])*scale).astype(int)
    py=np.rint(size/2-(projected[:,1]-centre[1])*scale).astype(int)
    order=np.argsort(projected[:,2])
    ranks=np.empty(len(points),dtype=np.int32)
    ranks[order]=np.arange(1,len(points)+1,dtype=np.int32)
    zbuffer=np.zeros(size*size,dtype=np.int32)
    np.maximum.at(zbuffer,py*size+px,ranks)
    zbuffer=maximum_filter(zbuffer.reshape(size,size),size=2)
    mask=zbuffer>0
    nearest=order[zbuffer[mask]-1]
    depth=(projected[nearest,2]-projected[:,2].min())/np.ptp(projected[:,2])
    color=PALETTE[labels[nearest]]
    # Depth changes brightness; each point's first-level copy determines hue.
    brightness=.55+.45*depth
    color=color*brightness[:,None]+np.array([40,45,40])[None,:]*depth[:,None]**2
    bg=np.array([9.,21.,32.])
    image=np.broadcast_to(bg,(size,size,3)).copy()
    glow=gaussian_filter(mask.astype(float),sigma=1.0)
    image+=glow[:,:,None]*np.array([3,6,8])[None,None,:]
    image[mask]=color
    return Image.fromarray(np.uint8(np.clip(image,0,255)))


def main():
    data=json.loads((ROOT/'positive_contact_certificate.json').read_text())
    a,b=maps(data)
    p=centres(a,b,8)
    labels=np.arange(len(p))//(6**7)
    art=point_image(p,labels)
    size=art.width
    canvas=Image.new('RGB',(size,size+380),(9,21,32))
    canvas.paste(art,(0,170))
    draw=ImageDraw.Draw(canvas)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    title=ImageFont.truetype(font,44)
    sub=ImageFont.truetype(font,25)
    big=ImageFont.truetype(font,46)
    small=ImageFont.truetype(font,23)
    draw.text((60,38),'Between surface and solid',font=title,fill=(229,240,238))
    draw.text((60,104),'Six coloured copies. One connected, exactly self-similar spatial fractal.',
              font=sub,fill=(164,195,203))
    y=size+175
    draw.line((60,y,size-60,y),fill=(39,66,76),width=2)
    draw.text((60,y+27),'2.1984 < Hausdorff dimension < 2.4149',font=big,fill=(231,205,153))
    draw.text((60,y+99),'Computer-assisted bounds for the reference member; the exact value remains open.',
              font=small,fill=(173,198,204))
    draw.text((60,y+143),'Finite preview at approximate parameters. Colours identify the six largest copies.',
              font=small,fill=(143,174,183))
    canvas.save(ROOT/'dimension_portrait.png')
    (ROOT/'render_metadata.json').write_text(json.dumps({
        'points':len(p),'depth':8,'image_size':list(canvas.size),
        'view_yaw_pitch_degrees':[-28,28],
        'colour_rule':'First-level map, indices 0 through 5.',
        'geometry':'Finite word centres at approximate reference parameters.',
        'proof_scope':'Image pixels do not establish separation or connectedness.',
    },indent=2)+'\n')
    print('Created dimension_portrait.png',flush=True)


if __name__=='__main__':main()
