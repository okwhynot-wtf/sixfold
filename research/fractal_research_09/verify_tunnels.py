"""Certify two through-passages and the geometric premises of the winding proof."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
PHASE5 = ROOT.parent / "fractal_handover/fractal_research_05"
sys.path.insert(0, str(PHASE5))
from certify_dimension import grid_centres


def check_axis(points, grid, height_int, piece, sign, error):
    # Normal-plane coordinates are (X/sqrt(2),Y) in grid units.
    x = points[:, 0] + points[:, 2] - sign*(grid + height_int)
    y = points[:, 1]
    assert int(np.max(np.abs(x)))**2 + 2*int(np.max(np.abs(y)))**2 < 2**63
    twice_squared = x*x + 2*(y*y)
    minima = [int(row.min()) for row in twice_squared.reshape(6, -1)]
    near = min(minima)
    assert near > 2 * (grid * (F(".105") + error))**2
    assert near < 2 * (grid * (F(".118") - error))**2
    # Upper bound uses any actual point in the cylinder of a minimizing word.
    # A positive signed distance puts the whole projected subpiece in a convex
    # half-plane. Its projected path can then be replaced by its endpoint chord.
    normals = [(1, 0), (-1, 2), (1, 2), (-1, 0), (1, -2), (-1, -2)]
    sub_x = x.reshape(6, 6, -1)[piece]
    sub_y = y.reshape(6, 6, -1)[piece]
    signed_minima = []
    for (a, b), xx, yy in zip(normals, sub_x, sub_y):
        minimum = int(np.min(a*xx + b*yy))
        assert minimum > 0
        assert minimum**2 > (2*a*a+b*b) * (grid*(F(".06")+error))**2
        signed_minima.append(minimum)
    return {"minimum_twice_squared_by_first_piece": minima,
            "signed_minima_in_own_six_subpieces": signed_minima}


def check_inherited_route(a_grid, b_grid, grid, h_lo, h_hi, u_lo, u_hi, r_lo, r_hi,
                          enclosing, centre_error):
    # In piece 0 follow its exact inherited axis down to z=-1/4, then exit
    # vertically. For the other five pieces test both rays at depth five.
    # True slope is tan(alpha); this rational proxy serves only in the checker.
    slope = F(15, 26)
    h_mid = F(".7071")
    bend_z = F(-1, 4)
    bend_x = 1 + slope*(bend_z-h_mid)
    slope_lo, slope_hi = [2*u/(1-u*u) for u in (u_lo, u_hi)]
    slope_error = max(abs(slope_lo-slope), abs(slope_hi-slope))
    h_error = max(h_mid-h_lo, h_hi-h_mid)
    proxy_error = (3+h_hi)*slope_error + slope*h_error
    assert proxy_error < F(".003")
    radius = F(".0058")
    assert enclosing+radius < 3
    assert r_lo*F(".0122") > radius
    # For a downward vertical ray, the distance from t0 is smallest at the
    # bend. At that point its square is (h+1/4)^2*(1+slope_true^2).
    assert (h_lo-bend_z)**2*(1+slope_lo**2) > (enclosing*r_hi+radius)**2
    tail = enclosing*r_hi**5 + centre_error
    threshold = radius + tail + proxy_error
    points = grid_centres(a_grid, b_grid, 5)[6**4:]
    for xx, yy, zz in points:
        x, y, z = (F(int(v), grid) for v in (xx, yy, zz))
        upper_line = (x-1-slope*(z-h_mid))**2/(1+slope**2) + y*y
        # Every point of the upper ray is above the bend, and conversely
        # every point of the lower ray is below it.
        assert upper_line > threshold**2 or bend_z-z > threshold
        lower_line = (x-bend_x)**2 + y*y
        assert lower_line > threshold**2 or z-bend_z > threshold
    return len(points)


def certify():
    data = json.loads((PHASE5 / "dimension_certificate.json").read_text())
    grid = data["Q"]
    family = next(item for item in data["results"] if item["name"] == "whole_family")
    r_lo, r_hi = map(F, data["family_certificate"]["outward_rational_r_bounds"])
    assert r_hi == F(family["r_upper"])
    h_lo, h_hi = map(F, data["family_certificate"]["height_interval"])
    u_centre = F(data["family_certificate"]["centre"][1])
    u_radius = F(data["family_certificate"]["radii"][1])
    u_lo, u_hi = u_centre-u_radius, u_centre+u_radius
    assert u_lo > 0 and 1-u_hi**2-2*u_hi > 0  # cos(alpha)-sin(alpha)>0
    enclosing, centre_error = F(data["packing_ball_bound"]), F(family["centre_error_bound"])
    a = np.asarray(data["a_grid"], dtype=np.int64)
    b = np.asarray(data["b_grid"], dtype=np.int64)
    points = grid_centres(a, b, 8)
    height_int = grid*7071//10000
    height_proxy = F(height_int, grid)
    height_error = max(abs(h_lo-height_proxy), abs(h_hi-height_proxy))
    error = enclosing*r_hi**8 + centre_error + height_error
    assert error < F(".00631")
    assert len(points) == 6**8 and int(np.max(np.abs(points))) < 3*grid
    results = {name: check_axis(points, grid, height_int, piece, sign, error)
               for name, piece, sign in [("A", 0, 1), ("B", 3, -1)]}
    # Distance from the opposite piece centre to this axis is sqrt(2)*(1+h).
    assert 2*(1+h_lo)**2 > (r_hi*enclosing+F("1.39"))**2
    checked = check_inherited_route(a, b, grid, h_lo, h_hi, u_lo, u_hi, r_lo, r_hi,
                                    enclosing, centre_error)
    return {"scope": "Entire certified height curve", "depth": 8, "centres": len(points),
            "grid": grid, "proxy_height_grid_units": height_int,
            "total_distance_error_upper": "0.00631", "axes": results,
            "clearance_strict_lower": "0.105", "clearance_strict_upper": "0.118",
            "projected_half_plane_margin_lower": "0.06",
            "opposite_enclosing_ball_clearance_lower": "1.39",
            "inherited_route_neighbour_centres_checked": checked,
            "inherited_route_radius_lower": "0.0058",
            "winding_matrix_by_argument_in_report": [[1, 0], [0, 1]]}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipt", action="store_true")
    args = parser.parse_args()
    receipt = json.dumps(certify(), indent=2) + "\n"
    if args.write_receipt:
        (ROOT / "tunnel_certificate.json").write_text(receipt, encoding="utf-8")
    print(receipt)
