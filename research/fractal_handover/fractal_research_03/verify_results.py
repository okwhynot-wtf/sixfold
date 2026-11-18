"""Independent checks of the exact grid cover mechanics and selected certificates."""
from pathlib import Path
from fractions import Fraction
import itertools
import json
import numpy as np
from certify_contacts import Q,OFFSET,BITS,cells,grid_centres,interval_grid,contact_cover,validate_local

ROOT=Path(__file__).resolve().parent


def brute_cell_keys(c,h):
    result=set()
    for p in itertools.product(*(range(int(x)-h,int(x)+h+1) for x in c)):
        ix,iy,iz=(v//(2*h)+OFFSET for v in p)
        result.add(ix+(iy<<BITS)+(iz<<(2*BITS)))
    return result


def scalar_word(a,b,word):
    p=[0,0,0]
    for k in word:
        p=[sum(int(a[k,i,j])*p[j] for j in range(3))//Q+int(b[k,i]) for i in range(3)]
    return p


def main():
    validate_local()
    checked=0
    for c in itertools.product(range(-2,3),repeat=3):
        for h in (1,2):
            actual=set(int(x) for x in cells(np.array([c],dtype=np.int64),h))
            assert actual==brute_cell_keys(c,h)
            checked+=1

    data=json.loads((ROOT/'certificates.json').read_text())
    assert len(data['results'])==19
    rng=np.random.default_rng(20261117)
    words_checked=0
    for rec in data['results']:
        r=Fraction(rec['r_numerator'],rec['r_denominator'])
        a,b=interval_grid(r,rec['theta_degrees'],rec['tilt_degrees'])
        assert np.array_equal(a,np.array(rec['a_grid']))
        assert np.array_equal(b,np.array(rec['b_grid']))
        all_centres=grid_centres(a,b,3)
        # Matrix-array generation appends outer letters. Independently apply
        # each short word using Python arbitrary-precision integers.
        for index in rng.choice(6**3,30,replace=False):
            digits=[int(index)//36,(int(index)//6)%6,int(index)%6]
            exact=scalar_word(a,b,digits[::-1])
            assert exact==all_centres[index].tolist()
            words_checked+=1
        last=rec['covers'][-1]
        if rec['status']=='disconnected_certificate':assert last['outer_components']>1
        else:assert last['outer_components']==1
        assert rec['strong_separation']==(last['outer_components']==6)

    # Reproduce one maximum-depth certificate and the strong-separation case.
    selected=[x for x in data['results'] if
        (x['r_numerator']==47 and x['theta_degrees']==10 and x['tilt_degrees']==30)
        or x['strong_separation']]
    reproductions=[]
    for rec in selected:
        r=Fraction(rec['r_numerator'],rec['r_denominator'])
        result=contact_cover(np.array(rec['a_grid'],dtype=np.int64),np.array(rec['b_grid'],dtype=np.int64),r,rec['covers'][-1]['depth'])
        assert result==rec['covers'][-1]
        reproductions.append({'r':str(r),'theta_degrees':rec['theta_degrees'],'tilt_degrees':rec['tilt_degrees'],'depth':result['depth']})
    summary={'brute_force_cell_cases':checked,'scalar_integer_word_checks':words_checked,
             'interval_coefficient_rechecks':len(data['results']),'full_reproductions':reproductions,
             'status':'All checks passed. This is a computer-assisted certificate, not a proof-assistant formalization.'}
    (ROOT/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
