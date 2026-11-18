"""Independent checks of the matrix computations used by the certificate.

These checks support the implementation. The proofs involving infinitely
many word lengths and the cited dimension theorem are in RESEARCH_07.md.
"""
from pathlib import Path
import json
import mpmath as mp
import sympy as sp

from certify_assouad import ROOT,rotation_certificate


def exp_rotations(u):
    angle=2*mp.atan(u)
    result=[]
    for k in range(6):
        phi=mp.pi*k/3
        axis=mp.matrix([-mp.sin(phi),mp.cos(phi),0])
        skew=mp.matrix([[0,-axis[2],axis[1]],
                        [axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
        result.append(mp.expm((-1)**k*angle*skew))
    return result


def mp_product(local,word):
    result=mp.eye(3)
    for k in word:result=result*local[k]
    return result


def main():
    mp.mp.dps=100
    cert=json.loads((ROOT/'assouad_certificate.json').read_text())
    data=json.loads((ROOT/'positive_contact_certificate.json').read_text())
    centre=mp.mpf(data['reference_half_angle_tangent'])
    # Repeat the interval predicates with more precision, not just with
    # decimal endpoints retained in the saved diagnostics.
    repeated=rotation_certificate(data,100)
    checked=0;maximum_orthogonality_error=mp.mpf(0)
    for u in [centre-mp.mpf('.00006'),centre,centre+mp.mpf('.00006')]:
        local=exp_rotations(u)
        for label,word in [('block_A_intervals',data['word']),('block_B_intervals',data['partner_word'])]:
            matrix=mp_product(local,word)
            for i in range(3):
                for j in range(3):
                    lo,hi=[mp.mpf(v) for v in repeated[label][i][j]]
                    assert lo<matrix[i,j]<hi
                    checked+=1
            maximum_orthogonality_error=max(maximum_orthogonality_error,
                max(abs(v) for v in matrix.T*matrix-mp.eye(3)))
    assert maximum_orthogonality_error<mp.mpf('1e-95')
    # Inspect the reference rotations independently, using matrix exponentials.
    local=exp_rotations(centre)
    A=mp_product(local,data['word']);B=mp_product(local,data['partner_word'])
    angle=mp.acos((sum(A[i,i] for i in range(3))-1)/2)*180/mp.pi
    commutator=max(abs(v) for v in A*B-B*A)
    assert mp.mpf(30)<angle<mp.mpf(32) and commutator>mp.mpf('.01')
    # The equal-length word argument has two cases, finite/infinite order.
    # Here the generic noncommutative cancellation is checked formally.
    # If A^(m-i) B^i = A^(m-j) B^j, cancel on the left and right to obtain
    # A^(j-i)=B^(j-i). No commutativity of A and B is assumed.
    AA,BB=sp.symbols('A B',commutative=False)
    for m in range(2,8):
        for i in range(m):
            for j in range(i+1,m+1):
                lhs=AA**(-(m-j))*(AA**(m-i)*BB**i)*BB**(-i)
                rhs=AA**(-(m-j))*(AA**(m-j)*BB**j)*BB**(-i)
                assert sp.powsimp(lhs)==AA**(j-i)
                assert sp.powsimp(rhs)==BB**(j-i)
    result={
        'passed':True,'rotation_interval_predicates_repeated_at_digits':100,
        'independent_matrix_exponential_entry_checks':checked,
        'maximum_orthogonality_error':mp.nstr(maximum_orthogonality_error,45),
        'reference_block_rotation_angle_degrees':mp.nstr(angle,45),
        'reference_noncommutation_entry_maximum':mp.nstr(commutator,45),
        'noncommutative_cancellation_checks_passed':True,
        'scope':'Finite implementation checks; infinite compactness and dimension arguments are stated separately in the report.',
    }
    (ROOT/'assouad_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
