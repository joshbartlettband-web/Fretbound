import re,base64,io
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
B={'two':[".###.","#...#","....#","...#.","..#..",".#...","#####"],
   'Z':["#####","....#","...#.","..#..",".#...","#....","#####"],
   'H':["#...#","#...#","#...#","#####","#...#","#...#","#...#"],
   'e':[".###.","#...#","#####","#....",".###."],
   'E':["#####","#....","#....","####.","#....","#....","#####"]}
GRID={'400':dict(X=[60,151,242,333,433,525],Y=[631,540,450,359,270,179,88,-12],bold=0),
      '700':dict(X=[61,157,253,350,446,542],Y=[638,545,452,360,267,174,81,-11],bold=34)}
def build(font,name,bmp,G):
    pen=TTGlyphPen(font.getGlyphSet()); X,Y=G['X'],G['Y']; off=7-len(bmp)
    for r,line in enumerate(bmp):
        y1,y0=Y[r+off],Y[r+off+1]; c=0
        while c<5:
            if line[c]=='#':
                c0=c
                while c<5 and line[c]=='#': c+=1
                x0,x1=X[c0],min(X[c]+G['bold'],X[5]+G['bold'])
                pen.moveTo((x0,y0)); pen.lineTo((x0,y1)); pen.lineTo((x1,y1)); pen.lineTo((x1,y0)); pen.closePath()
            else: c+=1
    g=pen.glyph(); g.recalcBounds(font['glyf']); font['glyf'][name]=g
    adv,_=font['hmtx'][name]; font['hmtx'][name]=(adv,g.xMin)
t=open('/home/claude/fretbound.html',encoding='utf-8').read()
for m in list(re.finditer(r"@font-face\{font-family:'Pixelify Sans'[^}]*\}",t))[::-1]:
    blk=m.group(0); w=re.search(r"font-weight:(\d+)",blk).group(1); u=re.search(r"base64,([A-Za-z0-9+/=]+)\)",blk)
    f=TTFont(io.BytesIO(base64.b64decode(u.group(1)))); cmap=f.getBestCmap()
    for key,bmp in B.items():
        name=cmap[ord('2')] if key=='two' else cmap[ord(key)]
        build(f,name,bmp,GRID[w])
    f.flavor='woff2'; out=io.BytesIO(); f.save(out); nb=base64.b64encode(out.getvalue()).decode()
    t=t[:m.start()]+blk.replace(u.group(1),nb)+t[m.end():]; print('rebuilt weight',w,len(nb))
open('/home/claude/fretbound.html','w',encoding='utf-8').write(t)
