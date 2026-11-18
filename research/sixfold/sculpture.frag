// The host supplies the reference transforms, the field sampler and uView.
// uView = phase in turns, camera mode, exposure, width/height.
uniform vec4 uView;
#ifdef SIXFOLD_METAL_ONLY
const vec4 uFinish = vec4(0.);
#else
uniform vec4 uFinish; // Archived glass and paired studies.
#endif
uniform vec4 uLobe0, uLobe1, uLobe2, uLobe3, uLobe4, uLobe5, uBackdrop, uTrace;
#ifdef SIXFOLD_COMPOSE
uniform vec4 uComposition; // magnification, framing offset xy, image roll
#else
const vec4 uComposition=vec4(1.,0.,0.,0.);
#endif
const float PI = 3.14159265359;
const float extent = 2.22;

vec2 field(vec3 pos) {
    vec3 g = clamp((pos + extent)*(95./(2.*extent)), 0., 95.);
    float k = floor(g.z);
    vec2 a = vec2(mod(k,12.),floor(k/12.))*96.;
    float next = min(k+1.,95.);
    vec2 b = vec2(mod(next,12.),floor(next/12.))*96.;
    vec2 uv = g.xy+.5;
    vec2 atlas = vec2(1152.,768.);
    vec2 value = mix(textureLod(FIELD, (a+uv)/atlas, 0.).rg,
                     textureLod(FIELD, (b+uv)/atlas, 0.).rg, fract(g.z));
    return vec2(value.r*.8, value.g);
}

mat3 rotateY(float angle) {
    float c = cos(angle), s = sin(angle);
    return mat3(c,0.,-s, 0.,1.,0., s,0.,c);
}

struct Hit {
    float depth;
    vec3 local;
    mat3 rotation;
    float scale;
    vec3 color;
    ivec4 address;
};

// Test bounded copies independently. All keep their actual positions even
// when the camera follows the repeated address 000.
void traceCopy(vec3 origin, vec3 ray, vec3 centre, mat3 rotation, float scale,
               ivec4 address, float skin, inout Hit hit) {
    vec3 rel = origin-centre;
    float mid = -dot(rel,ray);
    vec3 side = rel+mid*ray;
    float disc = ((2.14+skin)*scale)*((2.14+skin)*scale)-dot(side,side);
    if (disc<=0.) return;
    float radius = sqrt(disc);
    float start = max(0.,mid-radius);
    if (start>=hit.depth) return;
    float end = (min(mid+radius,hit.depth)-start)/scale;
    mat3 inverseQ = transpose(rotation);
    vec3 from = inverseQ*(rel+ray*start)/scale;
    vec3 direction = inverseQ*ray;
    float travel = 0.;
    for (int step=0; step<88; ++step) {
        if (travel>=end) break;
        vec3 p = from + direction*travel;
        float d = field(p).x-skin;
        if (d<.0018) {
            hit = Hit(start+scale*travel,p,rotation,scale,vec3(0),address);
            return;
        }
        travel += max(.0015, .86*d);
    }
}

vec3 normalAt(vec3 p) {
    const vec2 e = vec2(.021,-.021);
    vec3 n = e.xyy*field(p+e.xyy).x + e.yyx*field(p+e.yyx).x
           + e.yxy*field(p+e.yxy).x + e.xxx*field(p+e.xxx).x;
    return n/max(length(n),.00001);
}

float shadow(vec3 pos, vec3 light) {
    // The parent atlas provides soft contact shadows over the whole assembly.
    float t=.085, visibility=1.;
    for (int i=0; i<18; ++i) {
        vec3 p = pos+t*light;
        if (length(p)>2.22 || t>2.9) break;
        float d = field(p).x;
        visibility = min(visibility, (d+.008)*9./t);
        t += clamp(d*.9,.045,.32);
    }
    return clamp(visibility,.12,1.);
}

Hit traceScene(vec3 origin, vec3 ray, float shell) {
    Hit hit = Hit(12.,vec3(0),mat3(1),1.,vec3(0),ivec4(0));
    float r2=ratio*ratio, r3=r2*ratio, r4=r3*ratio;
    bool interior=uView.y>3.5 && uView.y<4.5;
    float r5=r4*ratio, r6=r5*ratio;
    // Traverse the entire four-level tree, culling a branch only when its
    // enclosing ball misses this ray. Neighbouring copies retain equal detail.
    for (int i=0; i<6; ++i) {
        vec3 nearAxis = cross(origin-T[i],ray);
        if (dot(nearAxis,nearAxis)>pow(2.26*ratio,2.)) continue;
        for (int j=0; j<6; ++j) {
            vec3 pos=T[i]+ratio*Q[i]*T[j];
            vec3 axis=cross(origin-pos,ray);
            if (dot(axis,axis)>pow(2.26*r2,2.)) continue;
            mat3 q2=Q[i]*Q[j];
            for (int k=0; k<6; ++k) {
                vec3 sub=pos+r2*q2*T[k];
                axis=cross(origin-sub,ray);
                if (dot(axis,axis)>pow(2.26*r3,2.)) continue;
                mat3 q3=q2*Q[k];
                for (int m=0; m<6; ++m) {
                    vec3 p4=sub+r3*q3*T[m];
                    mat3 q4=q3*Q[m];
                    if (!interior) {
                        traceCopy(origin,ray,p4,q4,r4,ivec4(i,j,k,m),shell,hit);
                        continue;
                    }
                    // Two extra levels keep nearby tunnel walls finely resolved.
                    axis=cross(origin-p4,ray);
                    if (dot(axis,axis)>pow(2.26*r4,2.)) continue;
                    for(int a=0;a<6;++a) {
                        vec3 p5=p4+r4*q4*T[a];
                        axis=cross(origin-p5,ray);
                        if(dot(axis,axis)>pow(2.26*r5,2.)) continue;
                        mat3 q5=q4*Q[a];
                        for(int b=0;b<6;++b)
                            traceCopy(origin,ray,p5+r5*q5*T[b],q5*Q[b],r6,ivec4(i,j,k,m),shell,hit);
                    }
                }
            }
        }
    }
    return hit;
}

// Long studio cards give reflections a shape that can be followed in motion.
float lightCard(vec3 d, vec3 facing, vec2 halfSize, float softness) {
    vec3 across=normalize(cross(vec3(0.,1.,0.),facing));
    vec3 along=cross(facing,across);
    float z=dot(d,facing);
    vec2 edge=abs(vec2(dot(d,across),dot(d,along))/max(.001,z))-halfSize;
    return (1.-smoothstep(-softness,softness,max(edge.x,edge.y)))*step(.01,z);
}

vec3 studio(vec3 d) {
    vec3 radiance=vec3(.008,.013,.022)+vec3(.032,.049,.061)*smoothstep(-.65,.82,d.y);
    radiance+=vec3(12.,13.,14.)*lightCard(d,normalize(vec3(-.78,.56,.38)),vec2(.14,.86),.055);
    radiance+=vec3(2.1,3.8,4.9)*lightCard(d,normalize(vec3(.93,.18,-.20)),vec2(.095,.73),.055);
    radiance+=vec3(4.2,2.9,1.8)*lightCard(d,normalize(vec3(-.16,.85,-.57)),vec2(.66,.13),.095);
    // Broad rear window is visible to off-axis transmitted rays.
    radiance+=vec3(.27,.37,.41)*lightCard(d,normalize(vec3(.38,.29,-.88)),vec2(.38,.56),.21);
    float back=smoothstep(.02,.65,-d.z);
    float stripe=d.x+.32*d.y;
    vec2 offset=(stripe+vec2(.16,-.28))/vec2(.077,.14);
    vec2 falloff=exp(-offset*offset);
    radiance+=back*(vec3(1.8,2.0,2.12)*falloff.x+vec3(.59,.71,.82)*falloff.y);
    return radiance;
}

// The surface mask remains the exact same render as metal. For optics, blend
// rounded lenses at successive address scales, like polishing a rough casting.
vec3 polishedNormal(Hit hit, vec3 point, vec3 ray, float descent, out float radius) {
    mat3 q=mat3(1);
    float scale=1., total=0.;
    vec3 center=vec3(0.), blended=vec3(0.);
    radius=0.;
    for(int level=0;level<4;++level) {
        int k=hit.address[level];
        center+=scale*q*T[k]; scale*=ratio; q=q*Q[k];
        float r=1.68*scale;
        vec3 plane=point-center-ray*dot(point-center,ray);
        vec3 outer=normalize(plane-ray*sqrt(max(.0000001,r*r-dot(plane,plane))));
        float band=float(level)-(.68+.65*descent);
        float weight=exp(-.79*band*band);
        blended+=weight*outer;
        radius+=weight*r;
        total+=weight;
    }
    vec3 fine=hit.rotation*normalAt(hit.local);
    if(dot(fine,ray)>0.) fine=-fine;
    radius/=total;
    return normalize(normalize(blended)+.13*fine);
}

vec3 glass(Hit hit, vec3 point, vec3 ray, mat3 camera, float shell, vec3 albedo,
           float descent, float density, float slope, float mask) {
    const float ior=1.50;
    float radius;
    vec3 normal=polishedNormal(hit,point,ray,descent,radius);
    vec3 inside=refract(ray,normal,1./ior);
    float thickness=-2.*dot(normal,inside)*radius;
    vec3 outer=normalize(normal+inside*(thickness/radius));
    vec3 outgoing=refract(inside,-outer,ior);
    if(dot(outgoing,outgoing)<.1) outgoing=reflect(inside,outer);
    vec3 exitPoint=point+inside*thickness;
    // Sample the actual rear geometry along the bent ray. One additional
    // interface supplies highlights and structure behind the front surface.
    Hit rear=traceScene(exitPoint+outgoing*.0011,outgoing,shell);
    vec3 transmitted=studio(transpose(camera)*outgoing);
    vec3 internal=vec3(0.);
    float rearMass=0.;
    if(rear.depth<10.) {
        float rearRadius;
        vec3 rearPoint=exitPoint+outgoing*(.0011+rear.depth);
        vec3 rearNormal=polishedNormal(rear,rearPoint,outgoing,descent,rearRadius);
        vec3 rearReflection=reflect(outgoing,rearNormal);
        float edge=pow(1.-max(0.,dot(rearNormal,-outgoing)),4.);
        transmitted=mix(transmitted,studio(transpose(camera)*rearReflection),.13+.40*edge);
        rearMass=.37+.62*field(rearPoint).y;
        vec3 rearKey=camera*normalize(vec3(-.55,.73,-.46));
        float backlight=pow(.5+.5*dot(rearNormal,rearKey),2.);
        float glint=pow(1.-abs(dot(rearNormal,outgoing)),2.);
        internal=(.045+.56*backlight+.95*glint)*(.22+.78*shadow(rearPoint,rearKey))*vec3(.40,.69,.76);
    }
    float gold=smoothstep(.02,.70,albedo.r-albedo.b);
    vec3 extinction=mix(vec3(1.05,.27,.18),vec3(.12,.48,1.2),gold);
    float pathDensity=0.;
    for(int step=0; step<18; ++step) {
        vec3 p=exitPoint+outgoing*(.06+.135*float(step));
        if(length(p)>2.23) break;
        pathDensity+=.135*field(p).y;
    }
    vec3 transmission=exp(-extinction*(thickness+1.52*pathDensity+rearMass));
    float facing=max(0.,dot(-ray,normal));
    float microFacing=abs(dot(ray,hit.rotation*normalAt(hit.local)));
    float fresnel=.04+.96*pow(1.-facing,5.);
    vec3 reflected=studio(transpose(camera)*reflect(ray,normal));
    float occlusion=exp(-.50*density);
    float relief=clamp(.58+.29*slope,.12,1.);
    vec3 radiance=transmission*(transmitted+internal)*(1.-fresnel)*occlusion
                 +reflected*fresnel*(.27+.73*mask)
                 +transmission*vec3(.035,.060,.072)*occlusion*relief;
    float grazing=pow(1.-facing,2.3)+.10*pow(1.-microFacing,3.);
    radiance+=grazing*(.22+.78*relief)*vec3(.55,.79,.89);
    return pow(1.-exp(-max(radiance,vec3(0))*uView.z*1.12),vec3(.4545));
}

vec3 study(vec2 uv, float recursiveDepth, bool useGlass) {
    float phase = fract(uView.x);
    float w = 2.*PI*phase;
    // Portrait, alignment, close approach, and return share a periodic clock.
    float axial = 1.-smoothstep(.033,.24,abs(phase-.27));
    float descent = 2.75*(1.-smoothstep(0.,.28,abs(phase-.65)));
    if (uView.y>.5 && uView.y<1.5) { axial=1.; descent=0.; }
    if (uView.y>1.5) { axial=0.; descent=recursiveDepth; }
    bool flight=uView.y>3.5 && uView.y<4.5;
    bool orbit=uView.y>4.5;
    if (orbit) { axial=0.; descent=0.; }
    float azimuth = -.98 + .46*sin(w+.2);
    float elevation = .37+.15*cos(w);
    if (orbit) { azimuth=-.98+w; elevation=.30+.24*sin(w+.6); }
    vec3 portrait = vec3(cos(azimuth)*cos(elevation),sin(azimuth)*cos(elevation),sin(elevation));
    vec3 sight = normalize(mix(portrait, normalize(vec3(-1.,0.,1.)), axial));
    vec3 baseline = normalize(mix(vec3(1.,.38,.04),normalize(vec3(1.,0.,1.)),axial));
    vec3 right = normalize(baseline-sight*dot(sight,baseline));
    vec3 up = cross(sight,right);
    float scale = pow(ratio,descent);
    mat3 turn = rotateY(tilt*descent);
    vec3 centre = focus-scale*turn*focus;
    sight=turn*sight; right=turn*right; up=turn*up;
    vec2 plane = (uv-.5)*vec2(uView.w,1.);
    float frame = mix(4.38,4.35,axial);
    // Fit the full assembly into narrow frames, easing into the close-up crop.
    frame *= mix(max(1.,1./uView.w),1.,smoothstep(0.,1.,descent));
    vec3 ray = -sight;
    vec3 origin = centre+frame*scale*(right*plane.x+up*plane.y)+sight*5.;
    float shell=clamp(.0050*scale/(ratio*ratio*ratio*ratio),.036,.11);
    if (flight) {
        // Phase-09's certified straight passage through the upper lobe.
        // The camera stays on the clear line, then looks back after emerging.
        vec3 axis=normalize(vec3(-1.,0.,1.));
        origin=T[0]+axis*(1.65-2.90*phase);
        float lookBack=PI*smoothstep(.48,.82,phase);
        vec3 forward=rotateY(lookBack)*(-axis);
        right=normalize(cross(forward,vec3(0.,1.,0.)));
        up=cross(right,forward);
        float roll=.10*sin(PI*phase);
        vec3 r=right*cos(roll)+up*sin(roll);
        up=up*cos(roll)-right*sin(roll); right=r;
        float lens=mix(.86,.66,smoothstep(.55,1.3,uView.w));
        ray=normalize(forward+2.*lens*(right*plane.x+up*plane.y));
        sight=-ray;
        centre=T[0]; scale=ratio; descent=.95; shell=.12;
    }
    Hit hit=traceScene(origin,ray,shell);
    // A low, broad pool of reflected light. Empty passages show this same field.
    vec2 vignette=(uv-vec2(.44,.54))*vec2(1.22,1.);
    vec3 bg = mix(vec3(.008,.014,.023)*(uBackdrop.rgb/vec3(.066,.108,.122)),uBackdrop.rgb,
                  exp(-6.5*dot(vignette,vignette)));
    if (hit.depth>10.) return bg;
    vec3 point = origin+hit.depth*ray;
    vec3 material[6]=vec3[6](uLobe0.rgb,uLobe1.rgb,uLobe2.rgb,uLobe3.rgb,uLobe4.rgb,uLobe5.rgb);
    vec3 albedo=mix(material[hit.address.x],material[hit.address.y],.13+.72*smoothstep(.45,1.5,descent));
    albedo=mix(albedo,material[hit.address.z],.065+.62*smoothstep(1.55,2.6,descent));
    albedo=mix(albedo,material[hit.address.w],.04+.30*smoothstep(2.40,3.,descent));
    vec3 n=hit.rotation*normalAt(hit.local);
    vec3 key=normalize(-.75*right+.94*up+.26*sight);
    vec3 fill=normalize(.80*right+.28*up+.17*sight);
    vec3 loc=point, keyLocal=key;
    float density=0., slope=0.;
    for (int level=0; level<4; ++level) {
        float front=field(loc+.20*keyLocal).y;
        float behind=field(loc-.20*keyLocal).y;
        slope+=behind-front;
        density+=front;
        int digit=hit.address[level];
        loc=transpose(Q[digit])*(loc-T[digit])/ratio;
        keyLocal=transpose(Q[digit])*keyLocal;
    }
    float mask=shadow(point,key);
    if(useGlass) return glass(hit,point,ray,mat3(right,up,sight),shell,albedo,descent,density,slope,mask);
    float ndl=max(0.,dot(n,key));
    float ao=exp(-.85*density);
    float broadLight=clamp(.47+.35*slope,.07,1.15);
    if (flight) {
        // A broad camera light keeps the interior's relief legible.
        mask=mix(mask,1.,.60);
        ao=mix(ao,1.,.35);
        broadLight=max(broadLight,.50);
    }
    // Softbox reflection on a satin metallic surface.
    vec3 halfKey=normalize(key+sight);
    float spec=pow(max(dot(n,halfKey),0.),14.);
    float rim=pow(1.-clamp(dot(n,sight),0.,1.),2.4);
    vec3 reflected=albedo*(vec3(.043,.09,.13)+(.18+.95*ndl)*vec3(1.36,1.04,.66)*broadLight*(.19+.81*mask)
                         +.22*max(0.,dot(n,fill))*vec3(.30,.69,1.))*ao;
    reflected+=mask*broadLight*ao*spec*mix(vec3(.85,.76,.57),albedo,.45)*.53;
    reflected+=rim*(.023+.16*max(0.,dot(n,fill)))*vec3(.24,.62,.86)*ao;
    float relief=dot(point-centre,sight)/max(scale,.26);
    reflected*=uView.z*clamp(.90+.26*relief,.50,1.35);
    return pow(clamp(1.-exp(-1.35*reflected),0.,1.),vec3(.4545));
}

vec3 curvePoint(int column, int group) {
    ivec2 texel=ivec2(column,group*2);
    vec3 hi=texelFetch(CURVE,texel,0).rgb;
    vec3 lo=texelFetch(CURVE,texel+ivec2(0,1),0).rgb;
    return (hi*(256./257.)+lo/257.-.5)*4.44;
}

vec3 windingLight(vec2 uv, vec3 surface) {
    float phase=fract(uView.x), w=2.*PI*phase;
    float az=-.98+.46*sin(w+.2), el=.37+.15*cos(w);
    vec3 sight=vec3(cos(az)*cos(el),sin(az)*cos(el),sin(el));
    vec3 baseline=normalize(vec3(1.,.38,.04));
    vec3 right=normalize(baseline-sight*dot(sight,baseline)), up=cross(sight,right);
    vec2 plane=(uv-.5)*vec2(uView.w,1.)*4.38;
    vec3 screen=plane.x*right+plane.y*up;
    float depth=1.35+4.*phase, glow=0., stroke=0., spark=0.;
    int groups=textureSize(CURVE,0).y/2;
    for (int order=0; order<3; ++order) {
        // gamma_A = G0(gamma). The phase-10 sequence uses G0^(4n)(gamma_A).
        float rel=1.+4.*float(order)-depth;
        float mag=pow(ratio,rel);
        float visibility=smoothstep(.009,.029,mag)*(1.-smoothstep(4.,8.,mag));
        if (visibility<=0.) continue;
        mat3 inv=rotateY(-tilt*rel);
        vec3 from=focus+inv*(screen-focus)/mag, axis=inv*sight;
        if (length(cross(from,axis))>2.15+.04/mag) continue;
        float rr=.040/mag;
        for (int g=0; g<groups; ++g) {
            vec3 lo=curvePoint(0,g), hi=curvePoint(1,g);
            vec3 centre=.5*(lo+hi);
            if (length(cross(centre-from,axis))>.5*length(hi-lo)+rr+.0002) continue;
            vec3 a=curvePoint(2,g)-from;
            a-=axis*dot(a,axis);
            for (int j=0; j<24; ++j) {
                vec3 b=curvePoint(3+j,g)-from;
                b-=axis*dot(b,axis);
                vec3 ab=b-a;
                float t=clamp(-dot(a,ab)/max(dot(ab,ab),1.e-13),0.,1.);
                float d=length(a+t*ab)*mag;
                float arc=(float(g*24+j)+t)/1434.;
                float delta=abs(fract(arc-phase*2.+.5)-.5);
                float pulse=exp(-delta*delta*400.);
                float strength=visibility*(.54+.46*pulse);
                stroke=max(stroke,strength*(1.-smoothstep(.002,.0075,d)));
                glow=max(glow,strength*exp(-d*d/.00021));
                spark=max(spark,pulse*visibility*exp(-d*d/.00058));
                a=b;
            }
        }
    }
    vec3 light=glow*vec3(.12,.24,.20)+stroke*vec3(.77,.78,.52)+spark*vec3(.16,.105,.033);
    return surface*.81+light*(uTrace.rgb/vec3(.77,.78,.52));
}

vec3 render(vec2 uv) {
    vec2 composed=(uv-.5)/max(.4,uComposition.x);
    float cr=cos(uComposition.w), sr=sin(uComposition.w);
    uv=mat2(cr,-sr,sr,cr)*composed+.5+uComposition.yz;
    bool useGlass=uFinish.x>.5;
    if(uFinish.x>1.5) {
        useGlass=uv.x>=.5;
        // Each half crops the same central portrait of the original frame.
        // A wider field on narrow outputs keeps the full sculpture in view.
        uv.x=fract(2.*uv.x)*.5+.25;
        uv=(uv-.5)*max(1.,2.13/uView.w)+.5;
    }
    if (uView.y<1.5 || uView.y>3.5) return study(uv,0.,useGlass);
    // Both samples use the same logarithmic camera path. Rebase into G0's
    // coordinates each generation and dissolve the wider context at the seam.
    float turn=fract(4.*uView.x);
    float depth=1.35+turn;
    float blend=smoothstep(.38,.96,turn);
    vec3 surface;
    if (blend==0.) surface=study(uv,depth,useGlass);
    else if (blend==1.) surface=study(uv,depth-1.,useGlass);
    else surface=mix(study(uv,depth,useGlass),study(uv,depth-1.,useGlass),blend);
    return uView.y>2.5 ? windingLight(uv,surface) : surface;
}
