#!/usr/bin/env python
import math

class ParamError(Exception):
    """This error will be raised if a parameter to the function does not
    validate ok.
    """
    pass

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

        >>> len(build_move_list(180,600,cumulative=False))
        180
        >>> sum(build_move_list(180,600,cumulative=False))
        600
        >>> build_move_list(180,600,cumulative=True)[-1] == 600
        True

    @type  steps:   int
    @param steps:   The number of iterations during which the movement shall
                    be made. Or in other words, the lenght of the resulting
                    list.
    @type  distance: int
    @param distance: The distance that should be covered by the smooth
                    movment.
    @type  accelerationpart: int
    @param accelerationpart: Part in percent of L{steps} where the
                    acceleration should take place.
    @type  retardationpart: int
    @param retardationpart: Part in percent of L{steps} where the retardation
                    should take place.
    @type  cumulative: bool
    @param cumulative: This defaults to False which means that every value in
                    the L{steps}-list is the distance to move in every step.
                    If its True then each value will be the distance from the
                    starting point up until this step.
    @rtype:         list of int
    @return:        A list where the lenght of the list is L{steps}. All
                    values in the list describes the movement.
                    See L{cumulative} and the other param desriptions for
                    more information.
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

    # Calculate the shape of the "speedcurve"
    speedcurve = (
            [1-math.cos(x*math.pi/acc_part) for x in range(acc_part)] +
            [2]*mid_part +
            [1-math.cos(math.pi+x*math.pi/ret_part) for x in range(ret_part)])

    # Calculate factor by which all values in the "speedcurve" should be
    # multiplied to sum up to the full distance
    factor = distance/sum(speedcurve)

    # If the values should be multiplied and rounded one after the other then
    # we would easily get the wrong answer at the end. So instead we do the
    # following and summarize all values up to the actual step and then
    # multiply that before rounding. In this way we make sure the last value
    # in move_list will be equal to distance!
    move_list = [int(round(sum(speedcurve[:1+x])*factor))
                 for x in range(steps)]
    
    if cumulative:
        return move_list
    
    # Prepend the list with a zero to be able to make the final list
    # comprehension in an easy way.
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
    parser.add_option('-t','--doctest', action='store_true' ,default=False)

    (options, args) = parser.parse_args()

    if options.doctest:
        import doctest, sys
        doctest.testmod(verbose=True)
        sys.exit()
        
    for x in build_move_list(
                options.steps,
                options.distance,
                options.accelerationpart,
                options.retardationpart,
                options.cumulative):
        print '*'*int(x)
