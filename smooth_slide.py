#!/usr/bin/env python
import math

class ParamError(Exception): pass

def build_move_list(
            steps, distance,
            accelerationpart=50,retardationpart=50,
            cumulative=False):
    """Build a sequence of movements to make a smooth movement.

    The resulting list will consist of the individual steps to make a smooth
    movment to cover the given distance.
    I{smooth} in this context means that there is a soft acceleration at the
    start and a soft retardation at the end of transition.

    Here is a simple doctest block:

        >>> import math
        >>> len(build_move_list(180,600))
        180
        >>> sum(build_move_list(180,600))
        600

    @type  steps:    int
    @param steps:    The number of iterations during which the movement shall
                     be made. Or in other words, the lenght of the resulting
                     list.
    @type  distance: int
    @param distance: The distance that should be covered by the smooth
                     movment.
    @rtype:          list if int
    @return:         A list where the lenght of the list is C{steps} and where
                     the sum of all elements in the list is C{distance}.
    """
    if not 0<=accelerationpart<=100:
        raise ParamError('Accelerationpart has to be a % value from 0 to 100')
    if not 0<=retardationpart<=100:
        raise ParamError('Retardationpart has to be a % value from 0 to 100')
    if accelerationpart+retardationpart>100:
        raise ParamError('Parts has to summurize to a value less then 100')

    acc_part = steps*accelerationpart/100
    ret_part = steps*retardationpart/100
    mid_part = steps-acc_part-ret_part

    move_list = (
            [1-math.cos(x*math.pi/acc_part) for x in range(acc_part)] +
            [2]*mid_part +
            [1-math.cos(math.pi+x*math.pi/ret_part) for x in range(ret_part)])

    factor = distance/sum(move_list)
    move_list = [round(sum(move_list[:1+x])*factor) for x in range(steps)]
    move_list[-1] = distance
    move_list.insert(0,0)
    return [move_list[x+1]-move_list[x] for x in range(steps)]

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-s','--steps',type='int',default=40)
    parser.add_option('-d','--distance', type='int',default=700)
    parser.add_option('-a','--accelerationpart', type='int',default=50)
    parser.add_option('-r','--retardationpart', type='int',default=50)
    parser.add_option('-c','--cumulative', action='store_true' ,default=False)

    (options, args) = parser.parse_args()

    for x in build_move_list(
                options.steps,
                options.distance,
                options.accelerationpart,
                options.retardationpart,
                options.cumulative):
        print '*'*int(x)
