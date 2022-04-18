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

        hours = "{:\u25CB>2s} {:\u25CB>9s}".format(
            h[0]*'\u25CF', h[1]*'\u25CF')
        mins = "{:\u25CB>5s} {:\u25CB>9s}".format(
            m[0]*'\u25CF', m[1]*'\u25CF')
        secs = "{:\u25CB>5s} {:\u25CB>9s}".format(
            s[0]*'\u25CF', s[1]*'\u25CF')

        print(hours, mins, secs)
        time.sleep(delay)


if __name__ == '__main__':
    lichtzeitpegel()
