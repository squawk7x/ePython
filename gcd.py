'''

This module supplies the function gcd(a: int, b: int) -> int
to calculate the greatest common divisor of two positive intergers a and b.

For example:
>>> gcd(12, 9)
3

'''


def gcd(a, b):
    '''
    Compute greatest common divisor of two positive integers a and b.
    >>> gcd(18, 10)
    2
    '''

    if type(a) not in [int] or type(b) not in [int]:
        raise TypeError("function arguments must be integers")

    if a <= 0 or b <= 0:
        raise ValueError("function arguments must be positive")

    while b:
        # print(f'{a}:{b} = {divmod(a,b)}')
        a, b = b, a % b
    return a


if __name__ == "__main__":
    import logging

    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename='gcd.log',
                        level=logging.DEBUG,
                        format=LOG_FORMAT)
    logger = logging.getLogger()
    # Test messages
    logger.debug('debug...')
    logger.info('info...')
    logger.warning('warning...')
    logger.error('error...')
    logger.critical('critical')
#    print(logger.level)

    # import doctest
    # doctest.testmod()

    import argparse

    parser = argparse.ArgumentParser(description="Calculates the \
    greatest common divisor of two positive integer numbers 'a' and 'b'.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("a", type=int, help="1st integer number")
    parser.add_argument("b", type=int, help="2nd integer number")

    args = parser.parse_args()
    result = gcd(args.a, args.b)

    if args.quiet:
        print(result)
    elif args.verbose:
        print(
            f"The greatest common divisor of {args.a} and {args.b} \
            equals {result}")
    else:
        print(f"gcd({args.a}, {args.b}) = {result}")
