'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv
from numpy import mean
from collections import Counter
from ways.info import ROAD_TYPES

# Q7:
def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''

    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    links = [j.links for j in roads.junctions()]
    links_num = [len(j) for j in links]
    links_length = [t.distance for l in links for t in l]
    return {
        'Number of junctions': len(roads.junctions()),
        'Number of links': sum(links_num),
        'Outgoing branching factor': Stat(max=max(links_num), min=min(links_num), avg=mean(links_num)),
        'Link distance': Stat(max=max(links_length), min=min(links_length), avg=mean(links_length)),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram': Counter(ROAD_TYPES[t.highway_type] for l in links for t in l),  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv(start=0, count=10000)).items():
        print('{}: {}'.format(k, v))


if __name__ == '__main__':
    from sys import argv

    assert len(argv) == 1
    print_stats()
