import math

def build_move_list(steps,distance):
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
                     dist.
    @type  distance: int
    @param distance: The distance that should be covered by the smooth
                     movment.
    @rtype:          list if int
    @return:         A list where the lenght of the list is C{steps} and where
                     the sum of all elements in the list is C{distance}.
    """
    move_list = [1-math.cos(x*math.pi*2/steps) for x in range(steps)]
    factor = distance/sum(move_list)
    move_list = [round(sum(move_list[:1+x])*factor) for x in range(steps)]
    move_list[-1] = distance
    move_list.insert(0,0)
    return [move_list[x+1]-move_list[x] for x in range(steps)]
