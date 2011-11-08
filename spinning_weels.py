#!/usr/bin/env python
import os, sys, math
import pygame
from pygame.locals import *
from smooth_slide import build_move_list

if not pygame.font: print 'Warning, fonts disabled'

def connet_bullet(direction, bullet, weelgrid):
    def pos_add(a,b): return (a[0]+b[0], a[1]+b[1])
    connection_map = {
        (+0,-1) : [(+0,-1), (-1,-1)],
        (-1,+0) : [(-1,-1), (-1,+0)],
        (+0,+1) : [(-1,+0), (+0,+0)],
        (+1,+0) : [(+0,+0), (+0,-1)],
    }
    b_pos = bullet.grid_value()
    for w in connection_map[direction]:
        weel = weelgrid.get(pos_add(b_pos, w))
        if weel:
            weel.connect(bullet)

class Weel(pygame.sprite.DirtySprite):
    def __init__(self,center,weelradius,cutoutradius):
        pygame.sprite.DirtySprite.__init__(self)
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
        self.connected = None
        self.connection_angle = 0

    def _fill_image(self):
        """Create the weel-image.

        @note: It is created 45 degrees rotated clockwise just to
               make the creation math simpler.
        """
        self.image.fill(self.bgcolor)
        # 1. Draw the main circle of the weel
        pygame.draw.circle(self.image, self.weelcolor,
                        (self.r1, self.r1), self.r1)
        # 2. Make the circular cutouts in the weel
        for pos in [self.rect.midtop, self.rect.midleft,
                    self.rect.midbottom, self.rect.midright]:
            pygame.draw.circle(self.image, self.bgcolor,
                            pos, self.r2)

        # 3. Draw the arrow on the weel
        c = self.rect.center
        pygame.draw.polygon(self.image,(255,0,0),
                        [c,
                        (c[0]+self.r1*0.2, c[1]),
                        (c[0]+self.r1*0.6, c[1]-self.r1*0.6),
                        (c[0], c[1]-self.r1*0.2) ])
        self.original = self.image

    def update(self):
        if self.connected:
            self.angle = self.connection_angle + self._angle()
            self._spin()
            self.dirty = 1

    def _angle(self):
        if not self.connected:
            return None
        bc = self.connected.rect.center
        wc = self.rect.center
        dx = bc[0]-wc[0]
        dy = bc[1]-wc[1]
        if dx == 0 and dy > 0:
            angle = 90
        if dx == 0 and dy < 0:
            angle = 270
        angle = int(math.degrees(math.atan(float(dy)/dx)))
        if dx < 0:
            angle += 180
        # The angle is calculated counterclockwise in the unit circle,
        # but the weel rotation is made clockwise. Therefore we return
        # the negation of the angle.
        return -angle

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
    def connect(self, bullet):
        self.connected = bullet
        self.connection_angle = self.angle - self._angle()
    def disconnect(self):
        self.connected = None
        self.angle = int(round(float(self.angle%360)/90))*90

class Bullet(pygame.sprite.DirtySprite):
    def __init__(self,x,y,radius, slide_length):
        pygame.sprite.DirtySprite.__init__(self)
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
        self.origo = (x,y)

    def start_moving(self,direction):
        if self.is_moving(): return
        self.movement = 0
        self.direction = direction

    def is_moving(self):
        return self.movement <> len(self.move_list)

    def _slide(self):
        self.rect = self.rect.move(
                [i*self.move_list[self.movement] for i in self.direction])
        self.movement += 1

    def update(self):
        if self.movement <> len(self.move_list):
            self._slide()
            self.dirty = 1

    def grid_value(self):
            return ((self.rect.center[0]-self.origo[0])/self.slide_length,
                    (self.rect.center[1]-self.origo[1])/self.slide_length)


def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-w','--width',type='int',default=4,
                      help="[default: %default]")
    parser.add_option('-x','--borderx', type='int',default=50,
                      help="[default: %default]")
    parser.add_option('-y','--bordery', type='int',default=-1,
                      help="[default: borderx]")
    parser.add_option('-r','--weelradius', type='int', default=50,
                      help="[default: %default]")
    parser.add_option('-b','--bulletradius', type='int',default=30,
                      help="[default: %default]")
    parser.add_option('-s','--speed', type='float',default=1.0,
                      help="Time in seconds for the bullet to do one move. "
                           "[default: %default]")
    (options, args) = parser.parse_args()

    ### Setup 
    # Number of weels
    width = options.width
    height = width
    # Borders in x and y directions (outside of the bullets endpositions)
    borderx = options.borderx
    if options.bordery < 0:
        bordery = borderx
    else:
        bordery = options.bordery
    # Weel radius
    weelradius = options.weelradius
    # Bullet radius (used in the construction ow weel aswell)
    bulletradius = options.bulletradius
    # Calculate the ticks value
    ticks = options.weelradius/options.speed
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

    #allsprites = pygame.sprite.RenderUpdates(weelgrid.values())
    allsprites = pygame.sprite.LayeredDirty(weelgrid.values())
    clock = pygame.time.Clock()

    bullet = Bullet(
                borderx + bulletradius,
                bordery + bulletradius,
                bulletradius,
                weelradius*2)
    allsprites.add(bullet)

    # Keep a 
    move_queue = []
    connected = False
    while 1:
        clock.tick(ticks)
        for event in pygame.event.get():
            # Handle any type of Quit evwnt
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_q:
                return

            # Handle move event
            elif event.type == KEYDOWN and event.key == K_UP:
                move_queue.append((+0,-1))
            elif event.type == KEYDOWN and event.key == K_LEFT:
                move_queue.append((-1,+0))
            elif event.type == KEYDOWN and event.key == K_DOWN:
                move_queue.append((+0,+1))
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                move_queue.append((+1,+0))

        
        if not bullet.is_moving() and connected:
            # Disconnect any weel connected to the bullet
            for weel in weelgrid.values(): weel.disconnect()

        # If there is movements queued up and the bullet is not moving, then
        # start a new "slide"
        if move_queue and not bullet.is_moving():
            direction = move_queue.pop(0)
            bullet_postition = bullet.grid_value()
            # Make sure the bullet is not moved outside of the gameboard!
            if ((0 <= bullet_postition[0]+direction[0] <= width) and
                (0 <= bullet_postition[1]+direction[1] <= height)):
                # Connect new weels to the bullet
                connet_bullet(direction, bullet, weelgrid)
                connected = True
                # Start the move of the bullet
                bullet.start_moving(direction)

        allsprites.update()
        allsprites.draw(screen, background)
        pygame.display.flip()


if __name__ == '__main__': main()
