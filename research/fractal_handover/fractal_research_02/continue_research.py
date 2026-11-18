"""Second investigation: sharper 2D screening and a genuine spatial lift."""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter
from scipy.spatial.transform import Rotation
from PIL import Image, ImageDraw, ImageFont
from base_ifs import centres, maps, screen, xy

ROOT=Path(__file__).resolve().parent
SIGNS=np.array([1,-1,1,-1,1,-1],dtype=float)
PHI=np.arange(6)*np.pi/3


def spatial_maps(r,theta_degrees,height,tilt_degrees):
    """f_k(x)=r Q_k x+t_k; Q_k=Rz(s_k theta) R_tangent(k)(s_k tilt)."""
    d=np.column_stack((np.cos(PHI),np.sin(PHI),height*SIGNS))
    axes=np.column_stack((-np.sin(PHI),np.cos(PHI),np.zeros(6)))
    tilt=Rotation.from_rotvec(axes*(SIGNS*np.deg2rad(tilt_degrees))[:,None]).as_matrix()
    spin=Rotation.from_rotvec(np.column_stack((np.zeros(6),np.zeros(6),SIGNS*np.deg2rad(theta_degrees)))).as_matrix()
    return r*np.einsum('kij,kjl->kil',spin,tilt),d


def spatial_centres(r,theta_degrees,height,tilt_degrees,depth):
    a,b=spatial_maps(r,theta_degrees,height,tilt_degrees)
    p=np.zeros((1,3))
    for _ in range(depth):
        p=(np.einsum('kij,nj->kni',a,p)+b[:,None,:]).reshape(-1,3)
    return p


def spatial_screen(r,theta_degrees,height,tilt_degrees,depth=3):
    a,b=spatial_maps(r,theta_degrees,height,tilt_degrees)
    p=spatial_centres(r,theta_degrees,height,tilt_degrees,depth)
    q=np.einsum('kij,nj->kni',a,p)+b[:,None,:]
    trees=[cKDTree(x) for x in q]
    tail=np.linalg.norm(b,axis=1).max()*r**(depth+1)/(1-r)
    parent=list(range(6))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]; i=parent[i]
        return i
    gaps=[]
    edges=0
    for i in range(6):
        for j in range(i+1,6):
            gap=float(trees[i].query(q[j])[0].min()-2*tail)
            gaps.append(gap)
            if gap<=1e-12:
                edges+=1;parent[find(i)]=find(j)
    return {'r':float(r),'theta_degrees':float(theta_degrees),'height':float(height),
        'tilt_degrees':float(tilt_degrees),'depth':depth,
        'outer_graph_components':len({find(i) for i in range(6)}),
        'possible_edges':edges,'minimum_pair_gap_lower_estimate':min(gaps),
        'similarity_dimension':math.log(6)/math.log(1/r)}


def write_csv(name,rows):
    with (ROOT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def refine_2d():
    # Deeper rechecks of precisely the same coarse cases, so the comparison
    # measures changes in the test rather than changes of sample locations.
    with (ROOT/'initial_planar_scan.csv').open() as f:
        original=list(csv.DictReader(f))
    selected=[x for x in original if x['outer_graph_components']=='1'
              and float(x['r'])<=.3575 and 0<float(x['theta_degrees'])<60]
    rows=[]
    for x in selected:
        row=screen(float(x['r']),float(x['theta_degrees']),depth=4)
        row['old_depth3_components']=int(x['outer_graph_components'])
        rows.append(row)
    write_csv('planar_refinement.csv',rows)
    # A few deeper direct pair-distance checks near the changing contacts.
    follow=[x for x in rows if x['outer_graph_components']>1]
    choices=follow[::max(1,len(follow)//8)][:8]
    deep=[screen(x['r'],x['theta_degrees'],depth=6) for x in choices]
    if deep:write_csv('planar_depth6.csv',deep)
    return rows,deep


def scan_3d():
    h=1/math.sqrt(2)
    rows=[spatial_screen(r,t,h,a,3) for r in np.arange(.40,.491,.01)
          for t in (0,10,20,30) for a in (0,15,30)]
    write_csv('spatial_scan.csv',rows)
    return rows


def render_points(points,path,yaw_degrees=-30,pitch_degrees=25,size=1500):
    """Orthographic point-cloud rendering with actual 3D depth shading."""
    view=Rotation.from_euler('yx',[yaw_degrees,pitch_degrees],degrees=True).as_matrix()
    p=points@view.T
    extent=max(np.ptp(p[:,0]),np.ptp(p[:,1]))
    scale=(size-90)/extent
    cx=(p[:,0].max()+p[:,0].min())/2
    cy=(p[:,1].max()+p[:,1].min())/2
    u=np.clip(np.rint(size/2+(p[:,0]-cx)*scale).astype(int),0,size-1)
    v=np.clip(np.rint(size/2-(p[:,1]-cy)*scale).astype(int),0,size-1)
    z=(p[:,2]-p[:,2].min())/max(np.ptp(p[:,2]),1e-15)
    depth=np.full(size*size,-1.0,dtype=np.float32)
    np.maximum.at(depth,v*size+u,z)
    depth=depth.reshape(size,size)
    occupied=depth>=0
    # At this finite resolution each word centre receives a tiny pixel footprint.
    from scipy.ndimage import maximum_filter
    depth=maximum_filter(depth,size=2)
    occupied=depth>=0
    glow=gaussian_filter(occupied.astype(float),sigma=1.1)
    bg=np.array([9,21,32],dtype=float)
    image=np.empty((size,size,3),dtype=float); image[:]=bg
    cool=np.array([35,147,172],dtype=float)
    warm=np.array([204,236,224],dtype=float)
    shade=np.clip(depth,0,1)
    color=cool[None,None,:]*(1-shade[:,:,None])+warm[None,None,:]*shade[:,:,None]
    image+=glow[:,:,None]*np.array([3,12,15])[None,None,:]
    image[occupied]=color[occupied]*(.55+.45*shade[occupied,None])
    Image.fromarray(np.uint8(np.clip(image,0,255))).save(path)


def make_spatial_gallery():
    rc=(math.sqrt(15)-math.sqrt(3))/6
    cases=[
        {'name':'Lifted ring','r':rc,'theta_degrees':30,'height':.22,'tilt_degrees':12},
        {'name':'Spatial gear','r':.41,'theta_degrees':30,'height':1/math.sqrt(2),'tilt_degrees':25},
        {'name':'Dense trial','r':.46,'theta_degrees':20,'height':1/math.sqrt(2),'tilt_degrees':30}]
    images=[]
    checks=[]
    for k,case in enumerate(cases):
        params={x:case[x] for x in ('r','theta_degrees','height','tilt_degrees')}
        p=spatial_centres(**params,depth=8)
        name=f'spatial_{k+1}.png'
        render_points(p,ROOT/name,size=1400)
        images.append(Image.open(ROOT/name).convert('RGB'))
        checks.append({'name':case['name'],**spatial_screen(**params,depth=4)})
    bg=(9,21,32)
    gallery=Image.new('RGB',(2100,2400),bg)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    ftitle=ImageFont.truetype(font,58);flabel=ImageFont.truetype(font,34);fsmall=ImageFont.truetype(font,28)
    draw=ImageDraw.Draw(gallery)
    draw.text((90,65),'The gear construction in three dimensions',font=ftitle,fill=(224,238,239))
    draw.text((90,155),'Fixed shrinking rotations repeat in space at every level.',font=flabel,fill=(170,196,201))
    # One large main view and two smaller comparisons, all genuine point clouds.
    gallery.paste(images[1].resize((1350,1350)),(375,260))
    draw.text((80,1630),'Spatial gear: r = 0.41, turn = 30°, tilt = 25°',font=flabel,fill=(224,238,239))
    draw.text((80,1690),'Exact Hausdorff dimension ≈ '+f'{math.log(6)/math.log(1/.41):.6f}',font=fsmall,fill=(170,196,201))
    gallery.paste(images[0].resize((650,650)),(100,1720))
    gallery.paste(images[2].resize((650,650)),(1220,1720))
    draw.text((790,1850),'Lifted ring',font=flabel,fill=(224,238,239))
    draw.text((790,1910),'Closer to the',font=fsmall,fill=(170,196,201))
    draw.text((790,1960),'planar design',font=fsmall,fill=(170,196,201))
    draw.text((790,2110),'Dense trial',font=flabel,fill=(224,238,239))
    draw.text((790,2170),'Numerical screen:',font=fsmall,fill=(170,196,201))
    draw.text((790,2220),'separated pieces',font=fsmall,fill=(170,196,201))
    gallery.save(ROOT/'spatial_gallery.png')
    # Export a smaller exact finite point set for practical 3D applications.
    p=spatial_centres(.41,30,1/math.sqrt(2),25,6)
    with (ROOT/'spatial_gear.ply').open('w') as f:
        f.write('ply\nformat ascii 1.0\ncomment Finite word centres; not a watertight surface\n')
        f.write(f'element vertex {len(p)}\nproperty float x\nproperty float y\nproperty float z\nend_header\n')
        np.savetxt(f,p,fmt='%.8f')
    return cases,checks


def validate():
    a,b=spatial_maps(.41,30,1/math.sqrt(2),25)
    ortho=max(np.linalg.norm((m/.41).T@(m/.41)-np.eye(3)) for m in a)
    assert ortho<1e-13
    assert all(abs(np.linalg.det(m/.41)-1)<1e-13 for m in a)
    # The h=0, tilt=0 member is precisely the old planar construction.
    p3=spatial_centres(.35,20,0,0,5)
    p2=centres(.35,20,5)
    assert np.max(np.abs(p3[:,0]+1j*p3[:,1]-p2))<1e-13
    assert np.max(np.abs(p3[:,2]))==0
    d=np.linalg.norm(b[:,None,:]-b[None,:,:],axis=2)
    d[d==0]=np.inf
    R=np.linalg.norm(b,axis=1).max()/(1-.41)
    ball_gap=float(d.min()-2*.41*R)
    assert ball_gap>0
    dimension=math.log(6)/math.log(1/.41)
    assert dimension>2 and dimension<3
    return {'orthogonality_residual':float(ortho),
            'analytic_minimum_ball_gap_at_r_041':ball_gap,
            'dimension_r_041':dimension,
            'universal_separation_limit_at_height_1_sqrt2':math.sqrt(2)-1}


def main():
    validation=validate()
    print('Geometry checks:',json.dumps(validation),flush=True)
    planar,deep=refine_2d()
    print('2D refinement finished:',len(planar),'cases;',sum(x['outer_graph_components']>1 for x in planar),'new exclusions',flush=True)
    space=scan_3d()
    print('3D scan finished:',len(space),'cases',flush=True)
    cases,selected=make_spatial_gallery()
    result={'validation':validation,
        'planar_rechecked_count':len(planar),
        'planar_additional_disconnection_screens':sum(x['outer_graph_components']>1 for x in planar),
        'planar_deeper_rechecks':deep,
        'spatial_scan_count':len(space),
        'spatial_screen_excluded_count':sum(x['outer_graph_components']>1 for x in space),
        'selected_spatial_cases':selected,
        'presets':cases,
        'status':'Analytic separation proof for Spatial gear; other contact screens numerical only. Novelty unresolved.'}
    (ROOT/'summary_02.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    main()
