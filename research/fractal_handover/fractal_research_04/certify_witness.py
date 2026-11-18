"""Interval contraction proof of a periodic contact and a local connected family."""
from pathlib import Path
import json
import mpmath as mp

ROOT=Path(__file__).resolve().parent
mp.mp.dps=100
mp.iv.dps=70
iv=mp.iv
WORD=[0,1,1,5,3,5,1,3]


def interval(a,b=None):
    return iv.mpf(str(a)) if b is None else iv.mpf([str(a),str(b)])


def midpoint(x):
    return (mp.mpf(x._mpi_[0])+mp.mpf(x._mpi_[1]))/2


def bounds(x):
    return mp.mpf(x._mpi_[0]),mp.mpf(x._mpi_[1])


def magnitude(x):
    lo,hi=bounds(x)
    return max(abs(lo),abs(hi))


class Dual:
    def __init__(self,value,grad=None):
        self.v=value if hasattr(value,'_mpi_') else interval(value)
        self.d=grad if grad is not None else [interval(0),interval(0)]
    @staticmethod
    def coerce(other):return other if isinstance(other,Dual) else Dual(other)
    def __add__(self,other):
        b=self.coerce(other)
        return Dual(self.v+b.v,[self.d[i]+b.d[i] for i in range(2)])
    __radd__=__add__
    def __neg__(self):return Dual(-self.v,[-x for x in self.d])
    def __sub__(self,other):return self+(-self.coerce(other))
    def __rsub__(self,other):return self.coerce(other)+(-self)
    def __mul__(self,other):
        b=self.coerce(other)
        return Dual(self.v*b.v,[self.d[i]*b.v+self.v*b.d[i] for i in range(2)])
    __rmul__=__mul__
    def __truediv__(self,other):
        b=self.coerce(other)
        lo,hi=bounds(b.v)
        assert lo>0 or hi<0,'Interval division by an interval containing zero'
        return Dual(self.v/b.v,[(self.d[i]*b.v-self.v*b.d[i])/(b.v*b.v) for i in range(2)])
    def __rtruediv__(self,other):return self.coerce(other)/self


def det(a):
    return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])


def periodic_dual(r,u,height,word=WORD):
    rr=Dual(r,[interval(1),interval(0)])
    uu=Dual(u,[interval(0),interval(1)])
    c=(1-uu*uu)/(1+uu*uu)
    sine=2*uu/(1+uu*uu)
    matrices=[];translations=[]
    for k in range(6):
        phi=iv.pi*k/3;sign=1 if k%2==0 else -1
        x=Dual(-iv.sin(phi));y=Dual(iv.cos(phi));z=Dual(0)
        s=sign*sine;w=1-c
        m=[[c+x*x*w,x*y*w-z*s,x*z*w+y*s],
           [y*x*w+z*s,c+y*y*w,y*z*w-x*s],
           [z*x*w-y*s,z*y*w+x*s,c+z*z*w]]
        matrices.append([[rr*m[i][j] for j in range(3)] for i in range(3)])
        translations.append([Dual(iv.cos(phi)),Dual(iv.sin(phi)),Dual(sign*height)])
    matrix=[[Dual(int(i==j)) for j in range(3)] for i in range(3)]
    centre=[Dual(0) for _ in range(3)]
    for k in word:
        centre=[centre[i]+sum(matrix[i][j]*translations[k][j] for j in range(3)) for i in range(3)]
        matrix=[[sum(matrix[i][j]*matrices[k][j][l] for j in range(3)) for l in range(3)] for i in range(3)]
    system=[[int(i==j)-matrix[i][j] for j in range(3)] for i in range(3)]
    denominator=det(system)
    point=[]
    for col in range(3):
        replaced=[[centre[i] if j==col else system[i][j] for j in range(3)] for i in range(3)]
        point.append(det(replaced)/denominator)
    return point


def residual_dual(r,u,height):
    p=periodic_dual(r,u,height)
    return [-p[0]/2+Dual(iv.sqrt(3)/2)*p[1],p[2]]


def refine_root():
    rec=json.loads((ROOT/'numerical_witnesses.json').read_text())[0]
    assert rec['word']==WORD
    x=mp.matrix([mp.mpf(str(rec['r'])),mp.mpf(str(rec['half_angle_tangent']))])
    height=1/iv.sqrt(2)
    for _ in range(8):
        values=residual_dual(interval(mp.nstr(x[0],95)),interval(mp.nstr(x[1],95)),height)
        f=mp.matrix([midpoint(v.v) for v in values])
        j=mp.matrix([[midpoint(v.d[k]) for k in range(2)] for v in values])
        step=mp.lu_solve(j,f);x-=step
        if max(abs(t) for t in step)<mp.mpf('1e-60'):break
    return [mp.nstr(x[i],55) for i in range(2)]


def contraction_certificate(centre,radius,height_lo,height_hi):
    x0=[interval(v) for v in centre]
    radii=[mp.mpf(str(v)) for v in radius]
    box=[interval(mp.mpf(centre[i])-radii[i],mp.mpf(centre[i])+radii[i]) for i in range(2)]
    h=interval(height_lo,height_hi)
    f0=residual_dual(x0[0],x0[1],h)
    all_values=residual_dual(box[0],box[1],h)
    fixed_values=residual_dual(x0[0],x0[1],1/iv.sqrt(2))
    j0=mp.matrix([[midpoint(v.d[k]) for k in range(2)] for v in fixed_values])
    inverse=j0**-1
    preconditioner=[[interval(mp.nstr(inverse[i,j],55)) for j in range(2)] for i in range(2)]
    remainder=[[interval(int(i==j))-sum(preconditioner[i][k]*all_values[k].d[j] for k in range(2)) for j in range(2)] for i in range(2)]
    image=[]
    for i in range(2):
        value=x0[i]-sum(preconditioner[i][k]*f0[k].v for k in range(2))
        value+=sum(remainder[i][j]*interval(-radii[j],radii[j]) for j in range(2))
        image.append(value)
    norm=max(sum(magnitude(remainder[i][j]) for j in range(2)) for i in range(2))
    margins=[]
    for i in range(2):
        low,high=bounds(box[i]);ilow,ihigh=bounds(image[i])
        margins.append(min(ilow-low,high-ihigh))
    # Prove the family is spatial: three even fixed points have equal positive
    # z and form a nondegenerate horizontal triangle; opposite points have -z.
    rr=box[0];uu=box[1]
    c=(1-uu*uu)/(1+uu*uu);s=2*uu/(1+uu*uu)
    a=1-rr*c;b=rr*s;denom=a*a+b*b
    fixed_x=(a+b*h)/denom
    fixed_z=(a*h-b)/denom
    passed=norm<1 and min(margins)>0 and bounds(fixed_x)[0]>0 and bounds(fixed_z)[0]>0
    def serial(x):return [mp.nstr(v,35) for v in bounds(x)]
    return {'passed':bool(passed),'centre':centre,'radius':[str(x) for x in radius],
            'height_interval':[str(height_lo),str(height_hi)],
            'parameter_box':[serial(x) for x in box],
            'fixed_point_map_image':[serial(x) for x in image],
            'derivative_norm_upper':mp.nstr(norm,35),
            'strict_inclusion_margins':[mp.nstr(x,35) for x in margins],
            'preconditioner':[[mp.nstr(midpoint(v),55) for v in row] for row in preconditioner],
            'spatial_fixed_point_x_interval':serial(fixed_x),
            'spatial_fixed_point_z_interval':serial(fixed_z)}


def main():
    centre=refine_root()
    results=[]
    # A tiny height interval around 1/sqrt(2) proves the isolated reference
    # root, and a wider box establishes a continuous connected family.
    hmid=mp.sqrt(mp.mpf('.5'))
    tests=[(['1e-25','1e-25'],mp.nstr(hmid-mp.mpf('1e-45'),70),mp.nstr(hmid+mp.mpf('1e-45'),70)),
           (['.01','.01'],'0.70','0.71'),
           (['.003','.003'],'0.706','0.708'),
           (['.001','.001'],'0.7070','0.7072')]
    for radii,lo,hi in tests:
        result=contraction_certificate(centre,radii,lo,hi)
        results.append(result)
        print(json.dumps({k:result[k] for k in ('passed','radius','height_interval','derivative_norm_upper','strict_inclusion_margins')}),flush=True)
    tight=results[0]
    assert tight['passed']
    family=next((x for x in results[1:] if x['passed']),None)
    assert family is not None
    p=periodic_dual(interval(centre[0]),interval(centre[1]),1/iv.sqrt(2))
    data={'word':WORD,'partner_word':[(1-k)%6 for k in WORD],
          'reference_r':centre[0],'reference_half_angle_tangent':centre[1],
          'reference_tilt_degrees':mp.nstr(2*mp.atan(mp.mpf(centre[1]))*180/mp.pi,40),
          'reference_point':[mp.nstr(midpoint(x.v),45) for x in p],
          'tight_root_certificate':tight,'connected_family_certificate':family,
          'all_attempts':results,
          'status':'Strict interval contraction: an actual periodic contact, propagated by symmetry to a connected full attractor. Novelty not assessed.'}
    (ROOT/'positive_contact_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:data[k] for k in ('reference_r','reference_tilt_degrees','reference_point','word','partner_word')},indent=2),flush=True)


if __name__=='__main__':main()
