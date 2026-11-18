"""Locator for the certified first intrusion, using the phase-10 receipt."""
from pathlib import Path
import sys
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from scipy.ndimage import maximum_filter

ROOT = Path(__file__).resolve().parent
PHASE5 = ROOT.parent / "fractal_handover/fractal_research_05"
sys.path.insert(0,str(PHASE5))
from certify_dimension import grid_centres

PAPER, TEXT, SOFT = "#101d28","#f1f5f5","#b0c3cb"
A, B, CORAL = "#ffc47c","#78d6d5","#ff9e93"


def main():
    data = json.loads((ROOT/"certificate.json").read_text())
    inputs = json.loads((PHASE5/"dimension_certificate.json").read_text())
    first = data["reference_first_intrusion"]
    h = 1/np.sqrt(2)
    u = float(inputs["family_certificate"]["centre"][1])
    v = np.array([2*u,1-u*u])/(1+u*u)
    t = np.array([1,h])
    hit = t-v*np.mean(list(map(float,first["travel_from_upper_centre"])))
    samples = grid_centres(np.array(inputs["a_grid"]),np.array(inputs["b_grid"]),8)/inputs["Q"]
    xlim, zlim = (-2.20,2.20), (-1.73,1.73)
    counts,_,_ = np.histogram2d(samples[:,0],samples[:,2],bins=(780,620),range=(xlim,zlim))
    ink = np.clip(np.log1p(maximum_filter(counts.T,2))/6,0,1)
    bar = np.array([14,28,39])
    background = np.uint8(bar+ink[:,:,None]*np.array([62,83,93]))
    fig = plt.figure(figsize=(12,6.6),dpi=165,facecolor=PAPER)
    fig.text(.055,.92,"Where the straight tunnels narrow",fontsize=23,color=TEXT,weight="semibold")
    fig.text(.056,.867,"Reference shape   /   Original tilted axes   /   Tested bore radius 0.0058",
             fontsize=11.5,color=SOFT)
    side = fig.add_axes([.055,.177,.515,.59],facecolor=PAPER)
    side.imshow(background,origin="lower",extent=(*xlim,*zlim),aspect="equal")
    side.set_title("Side view through the two lobe centres",loc="left",color=TEXT,fontsize=13,pad=10)
    for sign, tag, colour in ((1,"A",A),(-1,"B",B)):
        start = sign*t
        end = sign*hit
        line = start+np.array([-2.05,.58])[:,None]*(sign*v)
        side.plot(line[:,0],line[:,1],lw=1,color=colour,dashes=(4,4))
        side.annotate("",xy=start-.77*sign*v,xytext=start-.08*sign*v,
                      arrowprops=dict(arrowstyle="-|>",lw=1.8,color=colour))
        side.plot(*start,"o",color=colour,ms=5)
        side.annotate(f"{tag} centre",start,xytext=(8,5) if sign==1 else (-8,-15),
                      textcoords="offset points",ha="left" if sign==1 else "right",
                      color=colour,fontsize=9.5,weight="bold")
        side.plot(*end,marker="o",mfc=PAPER,mec=CORAL,mew=1.5,ms=7)
        side.annotate(f"{tag} intrusion",end,xytext=(29,-4) if sign==1 else (-25,6),
                      ha="left" if sign==1 else "right",textcoords="offset points",fontsize=9,
                      color=TEXT,arrowprops=dict(arrowstyle="-",color=CORAL,lw=.8))
    side.set(xlim=xlim,ylim=zlim,xlabel="x",ylabel="z")
    side.set_xticks([-2,-1,0,1,2]); side.set_yticks([-1,0,1])
    side.tick_params(colors=SOFT,labelsize=8)
    side.xaxis.label.set_color(SOFT); side.yaxis.label.set_color(SOFT)
    for sp in side.spines.values(): sp.set_color("#39515d")
    cross = fig.add_axes([.62,.21,.33,.535],facecolor=PAPER,aspect="equal")
    cross.set_title("Across bore A at a verified intrusion",color=TEXT,fontsize=12.5,pad=15)
    radius = float(first["straight_bore_radius"])
    cross.add_patch(Circle((0,0),radius,facecolor="#203746",edgecolor=A,lw=1.7))
    cross.plot(0,0,marker="+",ms=8,color=SOFT)
    cross.annotate("axis",(0,0),xytext=(-7,-13),ha="right",textcoords="offset points",color=SOFT,fontsize=9)
    x,y = np.mean(first["interior_witness_normal_plane_in_billionths"],axis=1)/1e9
    for k,yy in ((1,y),(5,-y)):
        cross.plot(x,yy,marker="o",mfc=CORAL,mec=PAPER,mew=1.5,ms=8)
        cross.annotate(f"Lobe {k}",(x,yy),xytext=(-38,-10 if yy>0 else 9),
                       textcoords="offset points",color=TEXT,fontsize=10,
                       arrowprops=dict(arrowstyle="-",lw=.7,color=CORAL))
    cross.set(xlim=(-.007,.007),ylim=(-.007,.007)); cross.axis("off")
    fig.text(.057,.092,"Arrows follow each tunnel inward. Coral rings locate the first occupied cross-sections.",
             color=SOFT,fontsize=10)
    fig.text(.057,.05,"The right view is enlarged. Dots mark two actual fractal points, related by reflection.",
             color=SOFT,fontsize=10)
    fig.savefig(ROOT/"straight_axis_locator.png",facecolor=PAPER)
    plt.close(fig)


if __name__=="__main__":
    main()
