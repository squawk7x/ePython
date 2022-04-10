'''
Data analysis with generator function
'''

import os
import time


def follow(filename):
    '''
    Generator function to retrieve last line of file
    '''
    f = open(filename, 'r')
    f.seek(0, os.SEEK_END)

    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue            # retry
        yield line              # emit line


for line in follow('stocklock.csv'):
    row = line.split(',')
    change = float(row[4])
    if change < 0:
        name = row[0]
        price = row[1]
        print('{:>10s} {:>10s} {:>10.2f}'.format(name, price, change))
