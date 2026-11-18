"""Finite point rendering with the six certified contacts marked as annotations."""
from pathlib import Path
import json,math
import numpy as np
from scipy.spatial.transform import Rotation
from PIL import Image,ImageDraw,ImageFont
from spatial_base import spatial_centres,render_points

ROOT=Path(__file__).resolve().parent


def main():
    data=json.loads((ROOT/'positive_contact_certificate.json').read_text())
    r=float(data['reference_r']);alpha=float(data['reference_tilt_degrees']);height=1/math.sqrt(2)
    points=spatial_centres(r,0,height,alpha,8)
    size=1600;yaw=-28;pitch=28
    render_points(points,ROOT/'connected_shape.png',yaw,pitch,size)
    view=Rotation.from_euler('yx',[yaw,pitch],degrees=True).as_matrix()
    projected=points@view.T
    extent=max(np.ptp(projected[:,0]),np.ptp(projected[:,1]))
    scale=(size-90)/extent
    cx=(projected[:,0].max()+projected[:,0].min())/2
    cy=(projected[:,1].max()+projected[:,1].min())/2
    p=np.array([float(v) for v in data['reference_point']])
    T=np.array([[.5,-math.sqrt(3)/2,0],[math.sqrt(3)/2,.5,0],[0,0,-1]])
    contacts=[]
    for j in range(6):contacts.append(np.linalg.matrix_power(T,j)@p)
    q=np.array(contacts)@view.T
    image=Image.open(ROOT/'connected_shape.png').convert('RGB')
    draw=ImageDraw.Draw(image)
    for x,y,z in q:
        u=size/2+(x-cx)*scale;v=size/2-(y-cy)*scale
        draw.ellipse((u-10,v-10,u+10,v+10),fill=(246,190,86),outline=(255,234,190),width=2)
    canvas=Image.new('RGB',(size,size+210),(9,21,32))
    canvas.paste(image,(0,100))
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    large=ImageFont.truetype(font,40);small=ImageFont.truetype(font,27)
    d=ImageDraw.Draw(canvas)
    d.text((60,32),'A connected spatial construction',font=large,fill=(224,238,239))
    d.text((60,size+116),'Gold marks: six certified shared points between neighbouring copies.',font=small,fill=(235,210,158))
    d.text((60,size+160),'Finite preview at approximate parameters; the proof concerns the exact root.',font=small,fill=(170,196,201))
    canvas.save(ROOT/'connected_contacts.png')
    summary={'render_points':len(points),'depth':8,'contacts':np.array(contacts).tolist(),
             'similarity_dimension_upper_bound':math.log(6)/math.log(1/r),
             'note':'Upper bound only: the open set condition and exact Hausdorff dimension are not proved.'}
    (ROOT/'render_metadata.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
