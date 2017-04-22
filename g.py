# g.py - globals
import pygame,utils,random

app='Jumble'; ver='1.0'
ver='1.1'
# jum.py uses g.screen.get_height() instead of g.h
ver='1.2'
# smiley @ end
ver='4.0'
# new sugar cursor etc
ver='4.1'
# o & right arrow keys
ver='4.2'
# shows no found instead of object number
ver='4.3'
# 4 changed images
# space & square instead of arrow

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    if pygame.font:
        t=int(40*imgf); font1=pygame.font.Font(None,t)
        t=int(80*imgf); font2=pygame.font.Font(None,t)
    message=''
    
    # this activity only
    global count,margin,setup_on
    count=0; margin=sy(2.7); setup_on=False
    
def sx(f): # scale x function
    return f*factor+offset

def sy(f): # scale y function
    return f*factor
