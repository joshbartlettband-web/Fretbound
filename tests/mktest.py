s=open('fretbound.html').read()
F='file:///home/claude/fonts/'
ff=[('Jersey 10','Jersey10-Regular','400'),('Jersey 25','Jersey25-Regular','400'),('Jacquard 12','Jacquard12-Regular','400'),('Jacquard 24','Jacquard24-Regular','400'),
    ('Jacquarda Bastarda 9','JacquardaBastarda9-Regular','400'),('Pixelify Sans','PixelifySans','400 700'),('Handjet','Handjet','100 900'),('Sixtyfour','Sixtyfour','400'),
    ('Silkscreen','Silkscreen-Regular','400'),('Silkscreen','Silkscreen-Bold','700')]
css=''.join("@font-face{font-family:'%s';src:url('%s%s.ttf');font-weight:%s;font-display:block}"%(a,F,b,w) for a,b,w in ff)
s=s.replace('<style>','<style>'+css,1)
open('test.html','w').write(s)
