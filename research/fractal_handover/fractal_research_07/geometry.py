"""Six similarities and word arithmetic for the certified connected family."""
from pathlib import Path
import json
import math
import numpy as np
from scipy.spatial.transform import Rotation

ROOT=Path(__file__).resolve().parent


def parameters():
    return json.loads((ROOT/'positive_contact_certificate.json').read_text())


def maps():
    data=parameters()
    r=float(data['reference_r']);u=float(data['reference_half_angle_tangent'])
    c=(1-u*u)/(1+u*u);s=2*u/(1+u*u)
    q=[];b=[]
    for k in range(6):
        phi=k*math.pi/3;sgn=(-1)**k
        x,y=-math.sin(phi),math.cos(phi);w=1-c;ss=sgn*s
        q.append(np.array([[c+x*x*w,x*y*w,y*ss],
                            [x*y*w,c+y*y*w,-x*ss],[-y*ss,x*ss,c]]))
        b.append([math.cos(phi),math.sin(phi),sgn/math.sqrt(2)])
    # The equalities Q_(k+3)=Q_k and b_(k+3)=-b_k are exact for this recipe.
    q=np.array(q);b=np.array(b)
    q[3:]=q[:3];b[3:]=-b[:3]
    return r,q,b


def digits(index,length):
    result=[]
    for _ in range(length):
        result.append(int(index%6));index//=6
    assert index==0
    return list(reversed(result))


def word_map(word,r,q,b):
    matrix=np.eye(3);centre=np.zeros(3)
    for k in word:
        centre+=matrix@b[k]
        matrix=matrix@(r*q[k])
    return matrix,centre


def qmul(a,b):
    """Quaternion product; scalar component is last, as in SciPy."""
    av,bv=a[:3],b[:3];aw,bw=a[3],b[3]
    return np.r_[aw*bv+bw*av+np.cross(av,bv),aw*bw-np.dot(av,bv)]


def qrotate(q,v):
    cross=np.cross(q[:,:3],v)
    return v+2*q[:,3,None]*cross+2*np.cross(q[:,:3],cross)


def metric(q,t):
    """max(operator norm(R-I), Euclidean norm(t)) for x -> R*x+t."""
    return np.maximum(2*np.linalg.norm(q[:,:3],axis=1),np.linalg.norm(t,axis=1))
