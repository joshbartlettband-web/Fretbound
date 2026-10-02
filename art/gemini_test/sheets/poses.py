# The 16 poses of a character sprite set, as two 4x2 sheets, and the stick-figure guide that goes to Gemini with each sheet.
# Sheet A is the playing set, sheet B the reactions. Everyone faces RIGHT; the guitar neck points to the right, up a little.
from PIL import Image,ImageDraw
import math
# CALM set (v1.50): in the playing poses the head, torso, legs and feet are IDENTICAL to idle; only the arms, hands and the guitar's tilt change, and by a little.
A=[('idle','Relaxed idle: standing straight, head up, guitar held across the body, fretting hand on the neck, picking hand over the strings.'),
   ('breath','Idle, one breath later: the same pose, shoulders and chest at most 2 pixels higher. Head, body and feet in the same place.'),
   ('strum_down','Strumming DOWN: ONLY the picking hand and forearm move, swept a little lower across the strings. Head, torso, legs and feet exactly as in idle.'),
   ('strum_up','Strumming UP: ONLY the picking hand and forearm move, swept a little higher across the strings. Head, torso, legs and feet exactly as in idle.'),
   ('fret_far','Fretting hand slid out along the neck towards the headstock (arm a little straighter). Head, torso, legs and feet exactly as in idle.'),
   ('fret_mid','Fretting hand in the middle of the neck. Head, torso, legs and feet exactly as in idle.'),
   ('fret_near','Fretting hand close to the guitar body (elbow tucked in a little). Head, torso, legs and feet exactly as in idle.'),
   ('nod','The same as idle with the chin lowered by a few pixels, as if nodding to the beat. Body, arms, guitar and feet exactly as in idle.')]
B=[('lean_in','Listening closely: the head and shoulders tilted slightly forward to the right, feet planted. A small change from idle, not a lunge.'),
   ('big_hit','A strong chord: feet planted, knees slightly bent, guitar tilted up a little, picking arm lifted to shoulder height, confident expression. Moderate, not a rock-star leap.'),
   ('cheer','Pleased with a win: a broad smile, and the fretting hand lifts the guitar neck a little. Feet planted. Gentle, not a big celebration.'),
   ('slump','Disappointed after a loss: shoulders lowered, head bowed a little, guitar hanging lower. Feet planted. Subdued, not collapsed.'),
   ('flinch','A small wince from a snapped string: eyes squeezed shut, head pulled back a little, the picking hand lifted off the strings. Feet planted.'),
   ('showoff','A cheeky grin and a raised eyebrow, the guitar neck swung up a little. Feet planted. Cheeky, not theatrical.'),
   ('blink','Same as idle but with the eyes CLOSED (mid-blink). Nothing else changes.'),
   ('talk','Same as idle but with the mouth open as if talking or singing. Nothing else changes.')]
def guide(path,which,cell=300):
    """a 4x2 stick-figure guide: one cell per pose, left to right then top to bottom, each cell numbered and named"""
    P=A if which=='A' else B; im=Image.new('RGB',(cell*4,cell*2),(255,0,255)); d=ImageDraw.Draw(im)
    for k,(name,desc) in enumerate(P):
        cx=(k%4)*cell; cy=(k//4)*cell; d.rectangle([cx+3,cy+3,cx+cell-4,cy+cell-4],outline=(255,255,255),width=2)
        d.text((cx+8,cy+6),f'{k+1} {name}',fill=(255,255,255))
        base=cy+cell-34; hx=cx+cell*0.48; lean=0; head_dy=0; arm=0.0; fret=0.5; gt_ang=-15; crouch=0
        if name=='breath': head_dy=-5
        if name=='strum_down': arm=1
        if name=='strum_up': lean=-3; arm=-1
        if name=='fret_far': fret=0.9
        if name=='fret_near': fret=0.15
        if name=='nod': head_dy=5; crouch=0
        if name=='lean_in': lean=8; head_dy=3
        if name=='big_hit': crouch=8; gt_ang=-30; arm=-2
        if name=='cheer': gt_ang=-30
        if name=='slump': lean=5; head_dy=12; gt_ang=10
        if name=='flinch': lean=-8; head_dy=2
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
