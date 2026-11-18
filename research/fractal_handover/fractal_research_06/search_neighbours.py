"""Numerical search for near-identity normalized word differences.

This is a diagnostic search, not a certificate of the open set condition.
"""
from pathlib import Path
import argparse
import gc
import json
import time
import numpy as np
from scipy.spatial.transform import Rotation
from geometry import ROOT,maps,qmul,qrotate,metric,digits,word_map


def transformations(q):
    local=Rotation.from_matrix(q).as_quat()
    result=[]
    for i in range(6):
        inv=local[i].copy();inv[:3]*=-1
        for j in range(6):
            columns=[qmul(inv,qmul(e,local[j])) for e in np.eye(4)]
            result.append(np.array(columns).T)
    return np.array(result)


def record(depth,quat,t,left,right,elapsed):
    d=metric(quat,t);which=int(np.argmin(d))
    return {'depth':depth,'retained_states':len(t),
            'minimum_metric':float(d[which]),
            'translation_norm':float(np.linalg.norm(t[which])),
            'rotation_operator_distance':float(2*np.linalg.norm(quat[which,:3])),
            'rotation_angle_degrees':float(np.degrees(2*np.arcsin(min(1,np.linalg.norm(quat[which,:3]))))),
            'left_word':digits(int(left[which]),depth),
            'right_word':digits(int(right[which]),depth),
            'normalized_translation':t[which].tolist(),
            'relative_quaternion_xyzw':quat[which].tolist(),
            'elapsed_seconds':elapsed}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--depth',type=int,default=11)
    parser.add_argument('--state-limit',type=int,default=6000000)
    args=parser.parse_args()
    r,q,b=maps();operators=transformations(q)
    # The dihedral symmetries reduce the different-first-letter pairs to
    # (0,1), (0,2), (0,3), allowing interchange of the two words.
    # Opposite (0,3) has normalized translation norm >5 and can be discarded.
    quat=Rotation.from_matrix(np.array([q[0].T@q[j] for j in [1,2]])).as_quat()
    t=np.array([q[0].T@(b[j]-b[0])/r for j in [1,2]])
    left=np.zeros(2,dtype=np.uint64);right=np.array([1,2],dtype=np.uint64)
    results=[];start=time.time()
    for depth in range(1,args.depth+1):
        rec=record(depth,quat,t,left,right,time.time()-start)
        results.append(rec)
        (ROOT/'neighbour_search.json').write_text(json.dumps({
            'results':results,'pruning_translation_norm':5,
            'metric':'max(||R-I||_operator, ||t||_2)',
            'scope':'Numerical finite-depth diagnostic. No all-scale OSC conclusion.',
        },indent=2)+'\n')
        print(json.dumps(rec),flush=True)
        if depth==args.depth or len(t)>args.state_limit:
            break
        newq=[];newt=[];newleft=[];newright=[]
        for begin in range(0,len(t),30000):
            end=min(begin+30000,len(t))
            qq=quat[begin:end];tt=t[begin:end]
            for j in range(6):
                shifted=tt+qrotate(qq,b[j])
                for i in range(6):
                    child_t=(shifted-b[i])@q[i]/r
                    mask=np.sum(child_t*child_t,axis=1)<=25
                    if not np.any(mask):continue
                    child_q=qq[mask]@operators[i*6+j].T
                    child_q/=np.linalg.norm(child_q,axis=1)[:,None]
                    newq.append(child_q);newt.append(child_t[mask])
                    newleft.append(left[begin:end][mask]*6+i)
                    newright.append(right[begin:end][mask]*6+j)
        del quat,t,left,right
        gc.collect()
        quat=np.concatenate(newq);t=np.concatenate(newt)
        left=np.concatenate(newleft);right=np.concatenate(newright)
    # Every saved near-identity witness is checked by separately composing
    # the original similarities directly, without the neighbour recurrence.
    for rec in results:
        m0,c0=word_map(rec['left_word'],r,q,b)
        m1,c1=word_map(rec['right_word'],r,q,b)
        rotation=np.linalg.solve(m0,m1)
        translation=np.linalg.solve(m0,c1-c0)
        value=max(np.linalg.norm(rotation-np.eye(3),2),np.linalg.norm(translation))
        assert abs(value-rec['minimum_metric'])<1e-7
    print('Direct witness recomposition passed.',flush=True)


if __name__=='__main__':main()
