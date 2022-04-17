'''
Lichtzeitpegel am Düsseldorfer Rheinturm
'''

import time


def lichtzeitpegel(delay=1):
    ''' Dezimaluhr '''

    while True:

        h = divmod(time.localtime().tm_hour, 10)
        m = divmod(time.localtime().tm_min, 10)
        s = divmod(time.localtime().tm_sec, 10)

        hour = "{:\u25CB>2s} {:\u25CB>9s}".format(
            h[0]*'\u25CF', h[1]*'\u25CF')
        min = "{:\u25CB>5s} {:\u25CB>9s}".format(
            m[0]*'\u25CF', m[1]*'\u25CF')
        sec = "{:\u25CB>5s} {:\u25CB>9s}".format(
            s[0]*'\u25CF', s[1]*'\u25CF')

        print(hour, min, sec)
        time.sleep(delay)


if __name__ == '__main__':
    lichtzeitpegel()
