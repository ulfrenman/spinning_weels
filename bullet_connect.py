def tup_add(a,b):
    return (a[0]+b[0],a[1]+b[1])

width = 4
height = width

weels = {}
for x in range(width):
    for y in range(height):
        weels[(x,y)] = x*y

bullet_pos = (0,0)
print 'up    %s -> %s,%s' % (
    bullet_pos,
    tup_add(bullet_pos,(0,-1)),
    tup_add(bullet_pos,(-1,-1)))
print 'left  %s -> %s,%s' % (
    bullet_pos,
    tup_add(bullet_pos,(-1,-1)),
    tup_add(bullet_pos,(-1,0)))
print 'down  %s -> %s,%s' % (
    bullet_pos,
    tup_add(bullet_pos,(-1,0)),
    tup_add(bullet_pos,(0,0)))
print 'right %s -> %s,%s' % (
    bullet_pos,
    tup_add(bullet_pos,(0,0)),
    tup_add(bullet_pos,(0,-1)))

[(+0,-1), (-1,-1)]
[(-1,-1), (-1,+0)]
[(-1,+0), (+0,+0)]
[(+0,+0), (+0,-1)]

