"""Reusable GPU renderer shared by individual exports and asset batches."""
import json
from pathlib import Path
import moderngl as gl
from PIL import Image

HERE=Path(__file__).resolve().parent
VERTEX="""#version 430
out vec2 uv;
uniform vec2 uJitter;
void main() {
    vec2 base=vec2((gl_VertexID<<1)&2,gl_VertexID&2);
    gl_Position=vec4(base*2.-1.,0.,1.);
    uv=base+uJitter;
}
"""

class Renderer:
    def __init__(self,width=1280,height=720,supersample=1,material="metal",samples=1):
        self.size=(width,height)
        self.supersample=supersample
        self.samples=samples
        self.ctx=ctx=gl.create_standalone_context(require=430)
        define="#define SIXFOLD_METAL_ONLY\n" if material=="metal" else ""
        shader=("#version 430\n#define SIXFOLD_COMPOSE\n"+define
                +"uniform sampler2D atlasMap, curveMap;\n#define FIELD atlasMap\n#define CURVE curveMap\n"
                +"in vec2 uv; out vec4 frag; uniform float uWeight;\n"+(HERE/"reference.glsl").read_text()
                +(HERE/"sculpture.frag").read_text()
                +"\nvoid main(){frag=vec4(render(uv)*uWeight,uWeight);}\n")
        self.program=program=ctx.program(vertex_shader=VERTEX,fragment_shader=shader)
        if material!="metal":
            program["uFinish"].value=(("metal","glass","compare").index(material),0.,0.,0.)
        self.textures=[]
        for i,(filename,smooth) in enumerate((("field.png",True),("contact_curve.png",False))):
            im=Image.open(HERE/filename).convert("RGB").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            tex=ctx.texture(im.size,3,im.tobytes(),alignment=1)
            tex.filter=(gl.LINEAR,gl.LINEAR) if smooth else (gl.NEAREST,gl.NEAREST)
            tex.use(i)
            self.textures.append(tex)
        program["curveMap"].value=1
        self.color=ctx.texture(tuple(v*supersample for v in self.size),4,dtype="f2" if samples>1 else "f1")
        self.color.filter=(gl.LINEAR,gl.LINEAR)
        self.scene=ctx.framebuffer(color_attachments=[self.color])
        self.vao=ctx.vertex_array(program,[])
        self.output=self.scene
        if supersample==2:
            self.output=ctx.simple_framebuffer(self.size,components=4)
            downsample=ctx.program(vertex_shader=VERTEX,fragment_shader="""#version 430
                uniform sampler2D source;
                in vec2 uv; out vec4 frag;
                void main(){frag=texture(source,uv);}
            """)
            downsample["source"].value=2
            self.resolve=ctx.vertex_array(downsample,[])
        self.colours(json.loads((HERE/"palettes.json").read_text())["original"])

    def colours(self,data):
        for i,rgb in enumerate(data["lobes"]):
            self.program[f"uLobe{i}"].value=(*rgb,1.)
        self.program["uBackdrop"].value=(*data["backdrop"],1.)
        self.program["uTrace"].value=(*data["trace"],1.)
        self.exposure=data.get("exposure",1.)

    def frame(self,phase=0.,mode=0,composition=(1.,0.,0.,0.)):
        self.program["uView"].value=phase,mode,self.exposure,self.size[0]/self.size[1]
        self.program["uComposition"].value=composition
        self.scene.use()
        offsets={1:[(0.,0.)],2:[(-.25,-.25),(.25,.25)],
                 4:[(-.25,-.25),(.25,-.25),(-.25,.25),(.25,.25)]}[self.samples]
        self.program["uWeight"].value=1./self.samples
        if self.samples>1:
            self.scene.clear(0.,0.,0.,0.)
            self.ctx.enable(gl.BLEND)
            self.ctx.blend_func=gl.ONE,gl.ONE
        for x,y in offsets:
            self.program["uJitter"].value=x/(self.size[0]*self.supersample),y/(self.size[1]*self.supersample)
            self.vao.render(vertices=3)
        self.ctx.disable(gl.BLEND)
        if self.supersample==2:
            self.output.use()
            self.color.use(2)
            self.resolve.render(vertices=3)
        return self.output.read(components=3,alignment=1)

    def image(self,phase=0.,mode=0,composition=(1.,0.,0.,0.)):
        return Image.frombytes("RGB",self.size,self.frame(phase,mode,composition)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    def close(self):
        # Release resources before the context, including float accumulation buffers.
        if self.output is not self.scene:
            self.resolve.release()
            self.output.release()
        self.vao.release()
        self.scene.release()
        self.color.release()
        for tex in self.textures:
            tex.release()
        self.program.release()
        self.ctx.release()
