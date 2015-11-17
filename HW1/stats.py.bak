'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''
from __future__ import division, print_function
from collections import namedtuple
from ways import load_map_from_csv


# Q7:
def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    return {
        'Number of junctions' : None,
        'Number of links' : None,
        'Outgoing branching factor' : Stat(max=None, min=None, avg=None),
        'Link distance' : Stat(max=None, min=None, avg=None),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : None,  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
