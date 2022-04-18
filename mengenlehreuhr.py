'''
Berlin-Uhr am Kurfürstendamm
'''

import time
import os


def mengenlehreuhr(delay=1):
    ''' Stellenwertuhr zur Basis 5 '''

    while True:
        os.system('clear')
        h = divmod(time.localtime().tm_hour, 5)
        m = divmod(time.localtime().tm_min, 5)

        hour5 = "  {:\u2B1B<4s}\n".format(
            h[0]*'\u2B1C')
        hour1 = "  {:\u2B1B<4s}\n".format(
            h[1]*'\u2B1C')

        min5 = "{:\u25AF<11s}\n".format(
            m[0]*'\u25AE')
        min1 = "  {:\u2B1B<4s}".format(
            m[1]*'\u2B1C')

        print(hour5, hour1, min5, min1, sep='')
        time.sleep(delay)


if __name__ == '__main__':
    mengenlehreuhr()
