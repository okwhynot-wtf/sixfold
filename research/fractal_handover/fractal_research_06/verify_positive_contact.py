"""Independent symbolic symmetry, high-precision geometry and interval rechecks."""
from pathlib import Path
import json
import mpmath as mp
import sympy as sp
import certify_witness as cert

ROOT=Path(__file__).resolve().parent


def symbolic_symmetries():
    u,h=sp.symbols('u h',real=True)
    c=(1-u*u)/(1+u*u);s=2*u/(1+u*u)
    a=sp.sqrt(3)/2
    co=[1,sp.Rational(1,2),-sp.Rational(1,2),-1,-sp.Rational(1,2),sp.Rational(1,2)]
    si=[0,a,a,0,-a,-a]
    matrices=[];translations=[]
    for k in range(6):
        sign=(-1)**k;axis=sp.Matrix([-si[k],co[k],0]);x,y,z=axis
        skew=sp.Matrix([[0,-z,y],[z,0,-x],[-y,x,0]])
        matrices.append(c*sp.eye(3)+(1-c)*(axis*axis.T)+sign*s*skew)
        translations.append(sp.Matrix([co[k],si[k],sign*h]))
    for matrix in matrices:
        assert all(sp.simplify(v)==0 for v in matrix.T*matrix-sp.eye(3))
        assert sp.simplify(matrix.det()-1)==0
    S=sp.Matrix([[sp.Rational(1,2),a,0],[a,-sp.Rational(1,2),0],[0,0,-1]])
    T=sp.Matrix([[sp.Rational(1,2),-a,0],[a,sp.Rational(1,2),0],[0,0,-1]])
    count=0
    for k in range(6):
        for expression in (S*matrices[k]*S.T-matrices[(1-k)%6],
                           S*translations[k]-translations[(1-k)%6],
                           T*matrices[k]*T.T-matrices[(k+1)%6],
                           T*translations[k]-translations[(k+1)%6]):
            assert all(sp.simplify(v)==0 for v in expression)
            count+=1
    x,y,z=sp.symbols('x y z',real=True)
    point=sp.Matrix([x,y,z]);f=-x/2+a*y
    assert sp.simplify(S*point-point-sp.Matrix([f,-sp.sqrt(3)*f,-2*z]))==sp.zeros(3,1)
    assert S.det()==1 and S*S==sp.eye(3) and T**6==sp.eye(3)
    return count


def exponential_point(r,u,h,word):
    """Compute rotations by matrix exponentials, rather than Rodrigues formula."""
    alpha=2*mp.atan(u)
    matrices=[];translations=[]
    for k in range(6):
        phi=mp.pi*k/3;sign=(-1)**k
        x=-mp.sin(phi);y=mp.cos(phi)
        skew=mp.matrix([[0,0,y],[0,0,-x],[-y,x,0]])
        matrices.append(r*mp.expm(sign*alpha*skew))
        translations.append(mp.matrix([mp.cos(phi),mp.sin(phi),sign*h]))
    m=mp.eye(3);c=mp.matrix([0,0,0])
    for k in word[::-1]:
        c=matrices[k]*c+translations[k];m=matrices[k]*m
    return mp.lu_solve(mp.eye(3)-m,c)


def refine_at_height(start,h):
    x=mp.matrix([mp.mpf(v) for v in start])
    for _ in range(8):
        f=cert.residual_dual(cert.interval(mp.nstr(x[0],95)),cert.interval(mp.nstr(x[1],95)),cert.interval(mp.nstr(h,95)))
        values=mp.matrix([cert.midpoint(v.v) for v in f])
        j=mp.matrix([[cert.midpoint(v.d[k]) for k in range(2)] for v in f])
        step=mp.lu_solve(j,values);x-=step
        if max(abs(v) for v in step)<mp.mpf('1e-65'):break
    return [mp.nstr(x[0],50),mp.nstr(2*mp.atan(x[1])*180/mp.pi,40)]


def main():
    identities=symbolic_symmetries()
    data=json.loads((ROOT/'positive_contact_certificate.json').read_text())
    r=mp.mpf(data['reference_r']);u=mp.mpf(data['reference_half_angle_tangent']);h=mp.sqrt(mp.mpf('.5'))
    first=exponential_point(r,u,h,data['word'])
    partner=exponential_point(r,u,h,data['partner_word'])
    difference=max(abs(first[i]-partner[i]) for i in range(3))
    assert difference<mp.mpf('1e-50')
    # Check the automatic derivatives against high-precision central differences
    # of a separately implemented matrix-exponential geometry calculation.
    step=mp.mpf('1e-23')
    def residual(rr,uu):
        p=exponential_point(rr,uu,h,data['word'])
        return [-p[0]/2+mp.sqrt(3)*p[1]/2,p[2]]
    dual=cert.residual_dual(cert.interval(str(r)),cert.interval(str(u)),1/cert.iv.sqrt(2))
    derivative_error=mp.mpf(0)
    for k in range(2):
        plus=residual(r+(step if k==0 else 0),u+(step if k==1 else 0))
        minus=residual(r-(step if k==0 else 0),u-(step if k==1 else 0))
        for i in range(2):
            estimate=(plus[i]-minus[i])/(2*step)
            derivative_error=max(derivative_error,abs(estimate-cert.midpoint(dual[i].d[k])))
    assert derivative_error<mp.mpf('1e-40')

    cert.iv.dps=90
    old=data['connected_family_certificate']
    repeated=cert.contraction_certificate(old['centre'],old['radius'],*old['height_interval'])
    assert repeated['passed']
    assert mp.mpf(repeated['derivative_norm_upper'])<mp.mpf('.36')
    samples=[]
    for hh in ('0.7070','0.7071','0.7072'):
        rr,angle=refine_at_height(old['centre'],mp.mpf(hh))
        samples.append({'height':hh,'r':rr,'tilt_degrees':angle})
    result={'symbolic_matrix_and_translation_identities':identities,
            'symbolic_proper_rotation_checks':6,
            'independent_periodic_point_difference':mp.nstr(difference,35),
            'independent_derivative_difference':mp.nstr(derivative_error,35),
            'rechecked_interval_decimal_digits':90,
            'rechecked_family_derivative_norm_upper':repeated['derivative_norm_upper'],
            'height_samples':samples,
            'status':'All checks passed; mathematical derivation and interval certificate remain subject to independent review.'}
    (ROOT/'positive_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
