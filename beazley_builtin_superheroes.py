'''
Ideas from youtube video by Dave Beazley
'''

import csv
from collections import Counter
from collections import defaultdict

with open('Food_Inspections.csv', 'r') as f:
    food = list(csv.DictReader(f))

# food = list(csv.DictReader(open('Food_Inspections.csv')))

results = {row['Results'] for row in food}

fail=[row for row in food if row['Results'] == 'Fail']

worst=Counter(row['DBA Name'] for row in fail)
print(worst.most_common(5))

# merging a new key in a dictionary row:
fail=[{**row, 'DBA Name': row['DBA Name'].replace("'", "").upper()}
        for row in fail]
worst=Counter(row['DBA Name'] for row in fail)
print(worst.most_common(5))

bad=Counter(row['Address'] for row in fail)
print('by address:')
print(bad.most_common(5))

by_year = defaultdict(Counter)
for row in fail:
    by_year[row['Inspection Date'][-4:]][row['Address']] += 1
print('by_year:')
print(by_year['2015'].most_common(5))

print("O'Hare:")
ohare = [row for row in fail if row['Address'].startswith('11601 W TOUHY')]
len(ohare)

print({row['Address'] for row in ohare})

c = Counter(row['AKA Name'] for row in ohare)
print(c.most_common(5))

# Clustering data:

inspections = defaultdict(list)

for row in ohare:
    inspections[row['License #']].append(row)
print(inspections['2428080'])
print(inspections.keys())
print([row['Inspection Date'] for row in inspections['34192']])
