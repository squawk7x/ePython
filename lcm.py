'''
This module supplies the function lcm(a: int, b: int) -> int
to calculate the lowest common multiple of two positive integers a and b.
For example:
>>> lcm(12, 9)
36
'''

from gcd import gcd


def lcm(a, b):
    '''
    Compute lowest common multiple of two positive integers a and b.
    >>> lcm(15, 10)
    30
    '''

    if type(a) not in [int] or type(b) not in [int]:
        raise TypeError("function arguments must be integers")

    if a <= 0 or b <= 0:
        raise ValueError("function arguments must be positive")

    return int((a * b) / gcd(a, b))


if __name__ == "__main__":
    import argparse
    # import doctest
    # doctest.testmod()

    parser = argparse.ArgumentParser(description="Calculates the \
    lowest common multiple of two positive integer numbers 'a' and 'b'.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("a", type=int, help="1st integer number")
    parser.add_argument("b", type=int, help="2nd integer number")

    args = parser.parse_args()
    result = lcm(args.a, args.b)
    if args.quiet:
        print(result)
    elif args.verbose:
        print(
            f"The lowest common multiple of {args.a} and {args.b} equals {result}")
    else:
        print(f"lcm({args.a}, {args.b}) = {result}")
