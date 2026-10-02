# The 16 poses of a character sprite set, as two 4x2 sheets, and the stick-figure guide that goes to Gemini with each sheet.
# Sheet A is the playing set, sheet B the reactions. Everyone faces RIGHT; the guitar neck points to the right, up a little.
from PIL import Image,ImageDraw
import math
A=[('idle','Relaxed idle: standing straight, head up, guitar held across the body, fretting hand on the neck, picking hand over the strings.'),
   ('breath','Idle, one breath later: shoulders and chest a little higher, head a little higher, otherwise the same as idle.'),
   ('strum_down','Strumming DOWN: picking hand sweeping down past the strings, body leaning forward a little, head slightly forward.'),
   ('strum_up','Strumming UP: picking hand swinging back up, body upright, head slightly back.'),
   ('fret_far','Fretting hand stretched far out along the neck near the headstock (arm extended), picking hand on the strings.'),
   ('fret_mid','Fretting hand in the middle of the neck (elbow bent a little), picking hand on the strings.'),
   ('fret_near','Fretting hand close to the guitar body at the low end of the neck (elbow tucked in), picking hand on the strings.'),
   ('nod','Head nodding down on the beat: chin lowered, knees slightly bent, playing.')]
B=[('lean_in','Leaning in to listen: upper body and head tilted forward toward the right, focused, both hands resting on the guitar.'),
   ('big_hit','A big power chord: wide stance, knees bent, guitar tilted up, head thrown back, picking arm swung high.'),
   ('cheer','Cheering a win: one arm and the guitar raised high overhead, big open smile, standing tall.'),
   ('slump','Slumped after a loss: shoulders hunched, head hanging down, guitar hanging low, defeated.'),
   ('flinch','Flinching from a snapped string: body recoiling backwards, one hand pulled away from the guitar, eyes squeezed shut, wincing.'),
   ('showoff','Showing off: grinning, guitar swung out to the side and pointed, one foot forward, cocky pose.'),
   ('blink','Same as the relaxed idle pose but with the eyes CLOSED (mid-blink). Nothing else changes.'),
   ('talk','Same as the relaxed idle pose but with the mouth open as if talking or singing. Nothing else changes.')]
def guide(path,which,cell=300):
    """a 4x2 stick-figure guide: one cell per pose, left to right then top to bottom, each cell numbered and named"""
    P=A if which=='A' else B; im=Image.new('RGB',(cell*4,cell*2),(255,0,255)); d=ImageDraw.Draw(im)
    for k,(name,desc) in enumerate(P):
        cx=(k%4)*cell; cy=(k//4)*cell; d.rectangle([cx+3,cy+3,cx+cell-4,cy+cell-4],outline=(255,255,255),width=2)
        d.text((cx+8,cy+6),f'{k+1} {name}',fill=(255,255,255))
        base=cy+cell-34; hx=cx+cell*0.48; lean=0; head_dy=0; arm=0.0; fret=0.5; gt_ang=-15; crouch=0
        if name=='breath': head_dy=-5
        if name=='strum_down': lean=14; arm=1
        if name=='strum_up': lean=-3; arm=-1
        if name=='fret_far': fret=0.9
        if name=='fret_near': fret=0.15
        if name=='nod': head_dy=14; crouch=12
        if name=='lean_in': lean=22; head_dy=8
        if name=='big_hit': lean=-14; crouch=26; gt_ang=-45; arm=-2
        if name=='cheer': gt_ang=-80
        if name=='slump': lean=14; head_dy=38; gt_ang=35; crouch=6
        if name=='flinch': lean=-24; head_dy=4
        if name=='showoff': gt_ang=-30; crouch=8
        hip=(hx,base-95+crouch); sh=(hip[0]+lean*0.9,hip[1]-65+crouch*0.2); hd=(sh[0]+lean*0.2,sh[1]-24+head_dy)
        col=(255,255,255)
        d.line([(hx-14,base),(hip[0],hip[1])],fill=col,width=4); d.line([(hx+14,base),(hip[0],hip[1])],fill=col,width=4)   # legs
        d.line([hip,sh],fill=col,width=5); d.ellipse([hd[0]-15,hd[1]-15,hd[0]+15,hd[1]+15],outline=col,width=3)               # spine, head
        gx0=hip[0]-12; gy0=hip[1]-20; ang=math.radians(gt_ang); gl=120
        gx1=gx0+gl*math.cos(ang); gy1=gy0+gl*math.sin(ang); d.line([(gx0-20*math.cos(ang),gy0-20*math.sin(ang)),(gx1,gy1)],fill=(255,220,0),width=6)  # guitar
        fx=gx0+(gx1-gx0)*fret; fy=gy0+(gy1-gy0)*fret
        if name=='cheer': d.line([sh,(sh[0]+25,sh[1]-70)],fill=col,width=4); d.line([sh,(fx-10,fy)],fill=col,width=4)
        elif name=='flinch': d.line([sh,(sh[0]+40,sh[1]-30)],fill=col,width=4); d.line([sh,(gx0+10,gy0+5)],fill=col,width=4)
        else: d.line([sh,(fx,fy)],fill=col,width=4); d.line([sh,(gx0+5,gy0+8+arm*14)],fill=col,width=4)
    im.save(path); return im
if __name__=='__main__':
    guide('/tmp/fbout/guide_A.png','A'); guide('/tmp/fbout/guide_B.png','B'); print('ok')
