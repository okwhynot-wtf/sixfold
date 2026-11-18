"""Integer-grid outer-cover certificates for the spatial six-map candidates.

The true recipe uses exact decimal r, exact degree angles and h=1/sqrt(2).
mpmath interval arithmetic brackets the coefficients. All subsequent cover
decisions use exact signed-64-bit integer operations and integer cell keys.
"""
from pathlib import Path
import csv
import hashlib
import itertools
import json
from fractions import Fraction
import numpy as np
import mpmath as mp

ROOT=Path(__file__).resolve().parent
Q=2**29
ERROR=Fraction(1,10**6)
BOUND=Fraction(5,2)
BITS=20
OFFSET=2**19
mp.mp.dps=100
mp.iv.dps=70


def grid_value(x):
    lo=mp.mpf(x._mpi_[0]);hi=mp.mpf(x._mpi_[1])
    n=int(mp.nint((lo+hi)*Q/2))
    assert mp.mpf(n-1)/Q<=lo and hi<=mp.mpf(n+1)/Q
    return n


def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def interval_grid(r,theta,tilt):
    iv=mp.iv
    rr=iv.mpf(r.numerator)/r.denominator
    aa=[];bb=[]
    for k in range(6):
        sign=1 if k%2==0 else -1
        phi=iv.pi*k/3
        x=-iv.sin(phi);y=iv.cos(phi);z=iv.mpf(0)
        angle=iv.pi*(sign*tilt)/180
        c=iv.cos(angle);s=iv.sin(angle);w=1-c
        rot=[[c+x*x*w,x*y*w-z*s,x*z*w+y*s],
             [y*x*w+z*s,c+y*y*w,y*z*w-x*s],
             [z*x*w-y*s,z*y*w+x*s,c+z*z*w]]
        turn=iv.pi*(sign*theta)/180
        cs=iv.cos(turn);sn=iv.sin(turn)
        spin=[[cs,-sn,iv.mpf(0)],[sn,cs,iv.mpf(0)],[iv.mpf(0),iv.mpf(0),iv.mpf(1)]]
        m=matmul(spin,rot)
        aa.append([[grid_value(rr*m[i][j]) for j in range(3)] for i in range(3)])
        bb.append([grid_value(iv.cos(phi)),grid_value(iv.sin(phi)),grid_value(sign/iv.sqrt(2))])
    return np.array(aa,dtype=np.int64),np.array(bb,dtype=np.int64)


def grid_centres(a,b,depth):
    p=np.zeros((1,3),dtype=np.int64)
    for _ in range(depth):
        # The global 3Q coordinate bound and coefficient bound imply every
        # three-term product sum is below 4.5 Q^2+9Q < 2^63.
        assert np.abs(p).max(initial=0)<3*Q
        p=np.concatenate([(p@a[k].T)//Q+b[k] for k in range(6)],axis=0)
    return p


def ceil_fraction(x):
    return (x.numerator+x.denominator-1)//x.denominator


def cells(p,halfwidth):
    cellwidth=2*halfwidth
    low=(p-halfwidth)//cellwidth
    assert np.abs(low).max()<OFFSET-2
    # A closed cube of side exactly one cell width meets these 8 cells.
    base=(low[:,0]+OFFSET)+((low[:,1]+OFFSET)<<BITS)+((low[:,2]+OFFSET)<<(2*BITS))
    keys=np.concatenate([base+dx+(dy<<BITS)+(dz<<(2*BITS))
                         for dx,dy,dz in itertools.product((0,1),repeat=3)])
    return np.unique(keys)


def overlap(a,b):
    if len(a)>len(b):a,b=b,a
    at=np.searchsorted(b,a)
    valid=at<len(b)
    return bool(np.any(b[at[valid]]==a[valid]))


def contact_cover(a,b,r,depth):
    p=grid_centres(a,b,depth)
    halfwidth=ceil_fraction(Q*(BOUND*r**depth+ERROR))
    n=len(p)//6
    occupied=[cells(p[k*n:(k+1)*n],halfwidth) for k in range(6)]
    parent=list(range(6))
    def find(k):
        while parent[k]!=k:
            parent[k]=parent[parent[k]];k=parent[k]
        return k
    edges=[]
    for i in range(6):
        for j in range(i+1,6):
            if overlap(occupied[i],occupied[j]):
                edges.append([i,j]);parent[find(i)]=find(j)
    return {'depth':depth,'halfwidth_grid_units':halfwidth,
            'cellwidth_grid_units':2*halfwidth,
            'outer_components':len({find(i) for i in range(6)}),
            'possible_edges':edges,'cell_counts':[len(x) for x in occupied],
            'cell_sha256':[hashlib.sha256(x.astype('<i8').tobytes()).hexdigest() for x in occupied]}


def validate_local():
    assert Fraction(49,100)*BOUND+Fraction(5,4)<BOUND
    # sqrt(3/2)<5/4; all true centres stay in the common radius-2.5 ball.
    assert Fraction(3,2)<Fraction(5,4)**2
    # (9+2sqrt(3))/Q < 13/Q and 13/[Q*(1-.49)] < 10^-6.
    assert Fraction(13,Q)/(1-Fraction(49,100))<ERROR
    assert Fraction(9,2)*Q**2+9*Q<2**63
    # Local coverage check: conservative closed intervals, including boundaries.
    for c in range(-20,21):
        for h in range(1,7):
            low=(c-h)//(2*h)
            assert (c+h)//(2*h)==low+1
    # Exact cell intersection implementation agrees with Python set intersection.
    rng=np.random.default_rng(17)
    for _ in range(100):
        a=np.unique(rng.integers(0,100,20));b=np.unique(rng.integers(0,100,20))
        assert overlap(a,b)==bool(set(a)&set(b))


def main():
    validate_local()
    with (ROOT/'candidate_input.csv').open() as f:
        candidates=[x for x in csv.DictReader(f) if x['outer_graph_components']=='1']
    results=[]
    for index,x in enumerate(candidates):
        # State the recipe at exact hundredths rather than retaining an
        # incidental binary floating-point grid-generation discrepancy.
        numerator=round(float(x['r'])*100);r=Fraction(numerator,100)
        theta=int(float(x['theta_degrees']));tilt=int(float(x['tilt_degrees']))
        a,b=interval_grid(r,theta,tilt)
        record={'r_numerator':r.numerator,'r_denominator':r.denominator,
                'theta_degrees':theta,'tilt_degrees':tilt,
                'a_grid':a.tolist(),'b_grid':b.tolist(),'covers':[]}
        for depth in range(4,9):
            result=contact_cover(a,b,r,depth)
            record['covers'].append(result)
            if result['outer_components']>1:break
        last=record['covers'][-1]
        record['status']='disconnected_certificate' if last['outer_components']>1 else 'unresolved'
        record['strong_separation']=last['outer_components']==6
        results.append(record)
        (ROOT/'certificates.json').write_text(json.dumps({'Q':Q,'error_bound':'1/1000000','ball_bound':'5/2','results':results},indent=2)+'\n')
        print(json.dumps({'candidate':index+1,'of':len(candidates),'r':str(r),'theta':theta,'tilt':tilt,
                         'depth':last['depth'],'components':last['outer_components'],'status':record['status']}),flush=True)
    summary={'candidate_count':len(results),
             'disconnected_certificates':sum(x['status']=='disconnected_certificate' for x in results),
             'strong_separation_certificates':sum(x['strong_separation'] for x in results),
             'unresolved':sum(x['status']=='unresolved' for x in results),
             'maximum_depth':8,'coefficient_precision_decimal_digits':70,
             'status':'Computer-assisted outer-cover certificates; no positive connectedness or novelty claim.'}
    (ROOT/'summary_03.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':
    main()
