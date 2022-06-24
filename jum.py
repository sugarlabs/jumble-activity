# jum.py
import random
import utils
import g
import pygame



class GridImage:
    def __init__(self, img, cx, cy):
        self.img = img
        self.cx = cx
        self.cy = cy
        self.found = False
        self.xy = utils.centre_to_top_left(img, (cx, cy))

class Objects:
    def __init__(self):
        self.n = 83
        self.nr = 7
        self.nc = 10
        self.total = self.nr * self.nc
        self.find_n = 20
        self.imgs = []
        for i in range(1, self.n + 1):
            img = utils.load_image(str(i) + '.png', True, 'objects')
            self.imgs.append(img)
        self.bgd = pygame.Surface((int(g.w - g.margin), g.screen.get_height()))
        self.frame = utils.load_image('frame.png', False)
        self.smiley = utils.load_image('smiley.png', True)

    def setup(self):
        self.obj_grid = []
        for i in range(10000):
            r = random.randint(1, self.n)
            if r not in self.obj_grid:
                self.obj_grid.append(r)
            if len(self.obj_grid) == self.total:
                break
        self.obj_bgd = []
        for i in range(1, self.n + 1):
            if i not in self.obj_grid:
                self.obj_bgd.append(i)
        self.glow_img = None
        indl = 0
        indr = self.nc - 1
        maxl = 0
        maxr = 0
        for r in range(self.nr):
            img = self.imgs[self.obj_grid[indl] - 1]
            w = img.get_width()
            if w > maxl:
                maxl = w
            img = self.imgs[self.obj_grid[indr] - 1]
            w = img.get_width()
            if w > maxr:
                maxr = w
            indl += self.nc
            indr += self.nc
        indt = 0
        indb = (self.nr - 1) * self.nc
        maxt = 0
        maxb = 0
        for r in range(self.nr):
            img = self.imgs[self.obj_grid[indt] - 1]
            h = img.get_height()
            if h > maxt:
                maxt = h
            img = self.imgs[self.obj_grid[indb] - 1]
            h = img.get_height()
            if h > maxb:
                maxb = h
            indt += 1
            indb += 1
        self.x1 = maxl / 2
        self.x2 = g.w - g.margin - maxr / 2
        self.dx = (self.x2 - self.x1) / (self.nc - 1)
        self.y1 = maxt / 2
        self.y2 = g.screen.get_height() - maxb / 2
        self.dy = (self.y2 - self.y1) / (self.nr - 1)
        self.x1 = int(self.x1)
        self.x2 = int(self.x2)
        self.y1 = int(self.y1)
        self.y2 = int(self.y2)
        self.current_ind = 0
        self.frame_cx = g.sx(3.1)
        self.frame_cy = g.sy(20.1)
        self.set_bgd_lookFor()
        self.found = 0
        self.complete = False
        self.dx, self.dy = 0, 0
        self.carry = False

    def overlaps_frame(self, img, x, y):
        fx, fy = utils.centre_to_top_left(self.frame, (self.frame_cx, self.frame_cy))
        rect = pygame.Rect(x, y, *img.get_size())
        return rect.colliderect(
            pygame.Rect(fx, fy, *self.frame.get_size())
        )

    def get_random_empty_pos(self, img):
        while True:
            x = random.randint(self.x1, self.x2)
            y = random.randint(self.y1, self.y2)
            x, y = utils.centre_to_top_left(img, (x, y))
            if not self.overlaps_frame(img, x, y):
                return x, y

    def set_bgd_lookFor(self):
        self.bgd.fill((128, 0, 0))
        for n in self.obj_bgd:
            self.bgd.blit(self.imgs[n - 1], self.get_random_empty_pos(self.imgs[n - 1]))
        cy = self.y1
        k = 0
        grid = []
        for r in range(self.nr):
            cx = self.x1
            for c in range(self.nc):
                n = self.obj_grid[k]
                ind = n - 1
                img = self.imgs[ind]
                if self.overlaps_frame(img, *utils.centre_to_top_left(img, (cx, cy))):
                    self.bgd.blit(img, self.get_random_empty_pos(img))
                else:
                    grid.append(GridImage(img, cx, cy))
                cx += self.dx
                k += 1
            cy += self.dy
        self.lookFor = random.sample(grid, self.find_n)
        for img in grid:
            if img not in self.lookFor:
                utils.centre_blit(self.bgd, img.img, (img.cx, img.cy))


    def draw(self):
        g.screen.blit(self.bgd, (g.sx(0), 0))
        cxy = (g.sx(30.5), g.sy(20))
        utils.display_number(g.count, cxy, g.font2, utils.CREAM)
        for img in self.lookFor:
            if not img.found:
                utils.centre_blit(g.screen, img.img, (img.cx, img.cy))
        if not self.complete and not g.setup_on:
            img = self.lookFor[self.current_ind].img
            cxy = (self.frame_cx, self.frame_cy)
            utils.centre_blit(g.screen, self.frame, cxy)
            utils.centre_blit(g.screen, img, cxy)
            x, y = cxy
            x -= self.frame.get_width() / 2
            x += g.sy(.24)
            y += self.frame.get_height() / 2
            y -= g.sy(.76)
            n = self.found
            s = str(n) + ' / ' + str(self.find_n)
            utils.text_blit1(g.screen, s, g.font1, (x, y), utils.BLACK, False)
        if self.complete:
            cxy = (self.frame_cx, self.frame_cy)
            utils.centre_blit(g.screen, self.frame, cxy)
            utils.centre_blit(g.screen, self.smiley, cxy)

    def click(self):
        for ind in range(self.find_n - 1, -1, -1):
            lf = self.lookFor[ind]
            if not lf.found:
                if utils.mouse_on_img(lf.img, lf.xy):
                    if ind == self.current_ind:
                        lf.found = True
                        self.found += 1
                        if not self.next1():
                            self.complete = True
                            g.count += 1
                        return True
                    else:
                        return False
        return False

    def update(self):
        if self.carry:
            mx, my = g.pos
            self.frame_cx, self.frame_cy = (mx + self.dx, my + self.dy)

    def next1(self):
        for i in range(len(self.lookFor)):
            self.current_ind += 1
            if self.current_ind == len(self.lookFor):
                self.current_ind = 0
            if not self.lookFor[self.current_ind].found:
                return True
        return False
