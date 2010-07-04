#!/usr/bin/env python
import os, sys, math
import pygame
from pygame.locals import *
from smooth_slide import build_move_list

if not pygame.font: print 'Warning, fonts disabled'

class Weel(pygame.sprite.Sprite):
    def __init__(self,center,weelradius,cutoutradius):
        pygame.sprite.Sprite.__init__(self)
        self.r1 = weelradius
        self.r2 = cutoutradius
        self.angle = 0

        self.image = pygame.Surface((self.r1*2,self.r1*2)).convert()
        self.rect = self.image.get_rect()

        self.bgcolor = (0,0,0)
        self.weelcolor = (100,100,100)
        self.image.set_colorkey(self.bgcolor, RLEACCEL)

        self._fill_image()
        self._spin()
        self.rect.center = center

    def _fill_image(self):
        self.image.fill(self.bgcolor)
        pygame.draw.circle(self.image, self.weelcolor,
                        (self.r1, self.r1), self.r1)
        for pos in [self.rect.midtop, self.rect.midleft,
                    self.rect.midbottom, self.rect.midright]:
            pygame.draw.circle(self.image, self.bgcolor,
                            pos, self.r2)

        c = self.rect.center
        pygame.draw.polygon(self.image,(255,0,0),
                        [c,
                        (c[0]+self.r1*0.2, c[1]),
                        (c[0]+self.r1*0.6, c[1]-self.r1*0.6),
                        (c[0], c[1]-self.r1*0.2) ])
        self.original = self.image

    def update(self):
        pass

    def _spin(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original, self.angle+45)
        self.rect = self.image.get_rect(center=center)

    def alter_angle(self,delta):
        self.angle += delta
        self._spin()
    def set_angle(self,angle):
        self.angle = angle
        self._spin()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,radius, slide_length):
        pygame.sprite.Sprite.__init__(self)
        self.r = radius
        self.slide_length = slide_length
        self.move_list = build_move_list(60,slide_length)
        self.movement = len(self.move_list)

        self.image = pygame.Surface((self.r*2,self.r*2)).convert()
        self.rect = self.image.get_rect()

        self.bgcolor = (0,0,0)
        self.bulletcolor = (50,50,250)
        self.image.set_colorkey(self.bgcolor, RLEACCEL)
        self.image.fill(self.bgcolor)
        pygame.draw.circle(self.image, self.bulletcolor,
                        (self.r, self.r), self.r)

        self.rect.center = (x,y)

    def start_moving(self,direction):
        if self.movement <> len(self.move_list): return
        self.movement = 0
        self.direction = direction
    def _slide(self):
        self.rect = self.rect.move(
                [i*self.move_list[self.movement] for i in self.direction])
        self.movement += 1

    def update(self):
        if self.movement <> len(self.move_list):
            self._slide()

def main():
    ### Setup 
    # Number of weels
    width = 4
    height = width
    # Borders in x and y directions (outside of the bullets endpositions)
    borderx,bordery = 50,50
    # Weel radius
    weelradius = 50
    # Bullet radius (used in the construction ow weel aswell)
    bulletradius = 30
    ### End of setup

    pygame.init()
    screen = pygame.display.set_mode((
                2*weelradius*width + 2*bulletradius + 2*borderx,
                2*weelradius*height + 2*bulletradius + 2*bordery
                ))

    pygame.key.set_repeat(300,20)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    screen.blit(background, (0,0))
    pygame.display.flip()


    weelgrid = {}
    for x in range(width):
        for y in range(height):
            weelgrid[(x,y)] = Weel((
                        (borderx + bulletradius + (x*2+1)*weelradius),
                        (bordery + bulletradius + (y*2+1)*weelradius)),
                        weelradius,
                        bulletradius)

    allsprites = pygame.sprite.RenderPlain(weelgrid.values())
    clock = pygame.time.Clock()

    bullet = Bullet(
                borderx + bulletradius,
                bordery + bulletradius,
                bulletradius,
                weelradius*2)
    allsprites.add(bullet)

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_UP:
                print "x,y = %d,%d" % (
                    (bullet.rect.center[0]-borderx-bulletradius)/(2*weelradius),
                    (bullet.rect.center[1]-borderx-bulletradius)/(2*weelradius))
                bullet.start_moving((0,-1))
            elif event.type == KEYDOWN and event.key == K_LEFT:
                bullet.start_moving((-1,0))
            elif event.type == KEYDOWN and event.key == K_DOWN:
                bullet.start_moving((0,1))
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                bullet.start_moving((1,0))

        allsprites.update()
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()
