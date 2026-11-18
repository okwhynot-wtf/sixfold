"""Search a nearby exact-contact recipe, without treating numerical roots as proof."""
from pathlib import Path
import json,math
import numpy as np
from scipy.optimize import root
from spatial_base import spatial_centres,spatial_maps

ROOT=Path(__file__).resolve().parent
AXIS=np.array([math.sqrt(3)/2,.5,0])
PERP=np.array([-.5,math.sqrt(3)/2,0])


def periodic_point(word,r,angle):
    a,b=spatial_maps(r,0,1/math.sqrt(2),math.degrees(angle))
    matrix=np.eye(3);centre=np.zeros(3)
    for k in word:
        centre+=matrix@b[k]
        matrix=matrix@a[k]
    return np.linalg.solve(np.eye(3)-matrix,centre)


def residual(word,x):
    p=periodic_point(word,x[0],x[1])
    return np.array([PERP@p,p[2]])


def main():
    depth=8
    points=spatial_centres(.47,0,1/math.sqrt(2),30,depth)
    points=points[:len(points)//6]
    distance=(points@PERP)**2+points[:,2]**2
    indices=np.argsort(distance)[:160]
    words=[]
    for index in indices:
        word=[(int(index)//6**p)%6 for p in range(depth-1,-1,-1)]
        if word not in words:words.append(word)
    found=[]
    for index,word in enumerate(words):
        solution=root(lambda x:residual(word,x),[.47,math.pi/6],tol=1e-11)
        r,angle=solution.x
        error=float(np.linalg.norm(residual(word,solution.x)))
        if solution.success and error<1e-10 and .42<r<.52 and .15<angle<.85:
            p=periodic_point(word,r,angle)
            rec={'word':word,'r':float(r),'tilt_degrees':float(math.degrees(angle)),
                 'half_angle_tangent':float(math.tan(angle/2)),
                 'point':p.tolist(),'residual':error,
                 'distance_from_seed':float(np.linalg.norm([r-.47,angle-math.pi/6]))}
            found.append(rec)
            if len(found)==1 or rec['distance_from_seed']<min(x['distance_from_seed'] for x in found[:-1]):
                print(json.dumps(rec),flush=True)
    found.sort(key=lambda x:x['distance_from_seed'])
    (ROOT/'numerical_witnesses.json').write_text(json.dumps(found,indent=2)+'\n')
    print('Candidates found:',len(found),flush=True)


if __name__=='__main__':main()
