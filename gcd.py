'''

It supplies the function gcd(a: int, b: int) -> int
to calculate the greatest common divisor of two intergers a and b.
For example:
>>> gcd(12, 9)
3

Furthermore it supplies the function lcm(a: int, b: int) -> int
to calculate the lowest common multiple of two integers a and b.
For example:
>>> lcm(12, 9)
36

'''


def gcd(a, b):
    '''
    Compute greatest common divisor of two integers a and b
    >>> gcd(18, 10)
    2
    '''
    while b:
        # print(f'{a}:{b} = {divmod(a,b)}')
        a, b = b, a % b
    return a


def lcm(a, b):
    '''
    Compute lowest common multiple of two integers a and b
    >>> lcm(15, 10)
    30
    '''
    return int((a * b) / gcd(a, b))


if __name__ == "__main__":
    import dis
    import doctest

    doctest.testmod()

    dis.dis(gcd)
    dis.dis(lcm)

#    print(gcd(12, 9))
#    print(lcm(12, 9))
