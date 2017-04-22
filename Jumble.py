#!/usr/bin/python
# Jumble.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,gtk,sys,buttons,jum

class Jumble:

    def __init__(self):
        self.count=0
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill((128,0,0))
        buttons.draw()
        self.objects.draw()

    def do_button(self,bu):
        if bu=='new': self.setup()
        if bu=='next': self.objects.next1()

    def do_key(self,key):
        if key==265 or key==pygame.K_o: self.do_button('new') #circle
        if key==263 or key==32: self.do_button('next') #circle

    def setup(self):
        g.setup_on=True; self.setup_ms=pygame.time.get_ticks()
        
    def buttons_setup(self):
        cx=g.sx(30.5)
        buttons.Button('new',(cx,g.sy(3)))
        buttons.Button('next',(cx,g.sy(5.5)))

    def run(self):
        g.init()
        g.journal=self.journal
        if not self.journal:
            utils.load(); self.count=g.count
        else:
            g.count=self.count
        self.buttons_setup()
        self.objects=jum.Objects()
        self.objects.setup()
        if self.journal: # Sugar only
            a,b,c,d=pygame.cursors.load_xbm('my_cursor.xbm','my_cursor_mask.xbm')
            pygame.mouse.set_cursor(a,b,c,d)
        going=True
        self.setup()
        while going:
            g.mx,g.my=pygame.mouse.get_pos()
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.redraw=True; self.objects.update()
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display
                    if event.button==1:
                        if self.objects.click():
                            if self.objects.complete:
                                buttons.off('next')
                        else:
                            self.display()
                            bu=buttons.check()
                            if bu!='': self.do_button(bu)
                elif event.type == pygame.KEYDOWN:
                    self.do_key(event.key); g.redraw=True
            if g.setup_on:
                self.objects.setup(); g.redraw=True
                if (pygame.time.get_ticks()-self.setup_ms)>2000:
                    g.setup_on=False; buttons.on('next')
            if not going: break
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                pygame.display.flip()
                g.redraw=False
            self.count=g.count
            tf=False
            if pygame.mouse.get_focused(): tf=True
            pygame.mouse.set_visible(tf)
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800,600))
    game=Jumble()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
