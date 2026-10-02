from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from shapely.geometry import Polygon
from fontTools.pens.boundsPen import BoundsPen
INK='#0B0C0E'; WHITE='#FFFFFF'; SPRAY='#A3A7AA'; TIDE='#0B0C0E'; FOG='#F1F1F0'
H=40; VW=34; T=8.6; OFF=15; NOTCH=27; FLAT=10
def V(x0):
    return [(x0,0),(x0+T,0),(x0+VW/2,NOTCH),(x0+VW-T,0),(x0+VW,0),(x0+VW/2+FLAT/2,H),(x0+VW/2-FLAT/2,H)]
A=V(0); B=V(OFF)
SW=OFF+VW; SH=H
inter=Polygon(A).intersection(Polygon(B))
OVER=list(inter.exterior.coords)[:-1]
def pd(p): return 'M'+' L'.join(f'{x:.3f} {y:.3f}' for x,y in p)+' Z'
def sym_inner(fg=INK,ac=SPRAY,mode='two'):
    """mode two: overlap coloured; one: overlap knocked out"""
    if mode=='one':
        return f'<path fill-rule="evenodd" d="{pd(A)} {pd(B)}" fill="{fg}"/>'.replace('fill-rule="evenodd"','fill-rule="evenodd"')
    return f'<path d="{pd(A)}" fill="{fg}"/><path d="{pd(B)}" fill="{fg}"/><path d="{pd(OVER)}" fill="{ac}"/>'
# evenodd on union of A and B: overlapping region counted twice -> hole. good.
import os as _o; FONT=_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'fonts','Geist-500.ttf'); MONO=_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'fonts','Switzer-500.ttf')
_fc={}
def text_path(txt,font,size,x0=0,y0=0,track=0):
    if font not in _fc: _fc[font]=TTFont(font)
    f=_fc[font];gs=f.getGlyphSet();cmap=f.getBestCmap();upm=f['head'].unitsPerEm
    s=size/upm; x=0; ds=[]
    for ch in txt:
        g=cmap[ord(ch)]
        sp=SVGPathPen(gs); tp=TransformPen(sp,(s,0,0,-s,x0+x*s,y0)); gs[g].draw(tp); ds.append(sp.getCommands())
        x+=gs[g].width+track*upm
    return ' '.join(ds),(x-track*upm)*s

def ink(txt,font,size,track=0):
    """horizontal ink bounds (xmin,xmax) of text set at x0=0"""
    if font not in _fc: _fc[font]=TTFont(font)
    f=_fc[font];gs=f.getGlyphSet();cmap=f.getBestCmap();upm=f['head'].unitsPerEm
    s=size/upm; x=0; xmin=1e9; xmax=-1e9
    for ch in txt:
        g=cmap[ord(ch)]; bp=BoundsPen(gs); gs[g].draw(bp)
        if bp.bounds:
            xmin=min(xmin,(x+bp.bounds[0])*s); xmax=max(xmax,(x+bp.bounds[2])*s)
        x+=gs[g].width+track*upm
    return xmin,xmax

ASC=71.0  # ascender at size 100
def lockup(fg=INK,ac=SPRAY,mode='one',sub=False,subcol=None):
    sc=ASC/SH; symw=SW*sc; gap=30
    td,tw=text_path('windward',FONT,100,x0=symw+gap,y0=ASC,track=-0.035)
    s=f'<g transform="scale({sc:.5f})">{sym_inner(fg,ac,mode)}</g><path d="{td}" fill="{fg}"/>'
    W=symw+gap+tw; Hh=ASC
    if sub:
        sd,_=text_path('RECRUITING',MONO,19,x0=symw+gap+4,y0=ASC+38,track=0.36)
        s+=f'<path d="{sd}" fill="{subcol or fg}"/>'; Hh=ASC+40
    return s,W,Hh
def stacked(fg=INK,ac=SPRAY,mode='one',sub=True):
    wx0,wx1=ink('windward',FONT,100,track=-0.035); ww=wx1-wx0; cx=(wx0+wx1)/2
    symw=ww*0.36; sc=symw/SW; symh=SH*sc
    y=symh+40+ASC
    td,_=text_path('windward',FONT,100,x0=0,y0=y,track=-0.035)
    s=f'<g transform="translate({cx-symw/2:.2f},0) scale({sc:.5f})">{sym_inner(fg,ac,mode)}</g><path d="{td}" fill="{fg}"/>'
    Hh=y+24
    if sub:
        rx0,rx1=ink('RECRUITING',MONO,19,track=0.42)
        sd,_=text_path('RECRUITING',MONO,19,x0=cx-(rx0+rx1)/2,y0=y+46,track=0.42)
        s+=f'<path d="{sd}" fill="{fg}"/>'; Hh=y+52
    return f'<g transform="translate({-wx0:.2f},0)">{s}</g>',ww,Hh
def svg(inner,w,h,pad=0,attrs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w+2*pad:.2f} {h+2*pad:.2f}" {attrs}>{inner}</svg>'
def symbol_svg(fg=INK,ac=SPRAY,mode='one',attrs=''): return svg(sym_inner(fg,ac,mode),SW,SH,attrs=attrs)
def lockup_svg(attrs='',**k): s,w,h=lockup(**k); return svg(s,w,h,attrs=attrs)
def stacked_svg(attrs='',**k): s,w,h=stacked(**k); return svg(s,w,h,attrs=attrs)
def tile_svg(bg=INK,fg=WHITE,ac=TIDE,S=120,r=0.62,attrs='',mode='one'):
    inner=S*r; sc=inner/SW; h=SH*sc
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" {attrs}><rect width="{S}" height="{S}" fill="{bg}"/><g transform="translate({(S-inner)/2:.2f},{(S-h)/2:.2f}) scale({sc:.5f})">{sym_inner(fg,ac,mode)}</g></svg>'
if __name__=='__main__':
    import os; os.makedirs('logo-files',exist_ok=True)
    F={
     'windward-logo-primary.svg':lockup_svg(),
     'windward-logo-primary-reverse.svg':lockup_svg(fg=WHITE,ac=TIDE),
     'windward-logo-primary-one-colour-ink.svg':lockup_svg(mode='one'),
     'windward-logo-primary-one-colour-white.svg':lockup_svg(fg=WHITE,mode='one'),
     'windward-logo-full-name.svg':lockup_svg(sub=True),
     'windward-logo-full-name-reverse.svg':lockup_svg(fg=WHITE,ac=TIDE,sub=True),
     'windward-logo-stacked.svg':stacked_svg(),
     'windward-logo-stacked-reverse.svg':stacked_svg(fg=WHITE,ac=TIDE),
     'windward-symbol.svg':symbol_svg(),
     'windward-symbol-reverse.svg':symbol_svg(WHITE,TIDE),
     'windward-symbol-one-colour-ink.svg':symbol_svg(mode='one'),
     'windward-symbol-one-colour-white.svg':symbol_svg(WHITE,mode='one'),
     'windward-app-icon.svg':tile_svg(),
     'windward-app-icon-light.svg':tile_svg(bg=FOG,fg=INK,ac=SPRAY),
     'windward-favicon.svg':tile_svg(S=64,r=0.74),
    }
    for k,v in F.items(): open('logo-files/'+k,'w').write(v)
    print(OVER, SW, SH)
