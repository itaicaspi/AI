'''
 A set of utilities for using israel.csv 
 The map is extracted from the openstreetmap project
'''

from collections import namedtuple
from . import tools
from . import info
import sys

#define class Link_traffic_params
# Some additional parameters for a link
Link_traffic_params = namedtuple('Link_traffic_params',
                         ['cos_frequency',
                          'sin_frequency',
                         ])

# define class Link
Link = namedtuple('Link',
       ['source', 'target',  #  int (junction indices)
        'distance',          #  float
        'highway_type',      #  int < len(road_info.ROAD_TYPES)
        'link_params',       # a tuple of 2 floats.
       ])


# define class Junction
Junction = namedtuple('Junction',
           ['index',       #  int
            'lat', 'lon',  #  floats: latitude/longitude
            'links',       #  list of Link
           ])


class Roads(dict):
    '''The graph is a dictionary Junction_id->Junction, with some methods to help.
    To change the generation, simply assign to it:
    g.generation = 5
    '''
    def junctions(self):
        return list(self.values())
    
    def __init__(self, junction_list):
        super(Roads, self).__init__(junction_list)
        'to change the generation, simply assign to it'
        self.generation = 0
        self.base_traffic = tools.base_traffic_pattern()
        tmp = [(n.lat,n.lon) for n in junction_list.values()]
        self.mean_lat_lon = (sum([i[0] for i in tmp])/len(tmp),sum([i[1] for i in tmp])/len(tmp))

    def link_speed_history(self, link, time=0):
        'Deterministically generates the speed for the link based on "history" of the speed at time time'
        time = int(time) 
        _, top = info.SPEED_RANGES[link.highway_type]
        return int(top/tools.generate_slowdown_multiplier(link.distance,top,self.base_traffic[time],*(link.link_params),time=time))
        
    def realtime_link_speed(self, link, time=0):
        'deterministically generates the speed for the link in "real time" time'
        time = int(time)
        _, top = info.SPEED_RANGES[link.highway_type]
        _a = 40/60 # speed in km/minute
        _delta_dist = tools.compute_distance(self.mean_lat_lon[0],self.mean_lat_lon[1],self[link.source].lat,self[link.source].lon)
        multiplier = (tools.cos((time*_a + _delta_dist)*tools.pi/(15*2))/3)+1
        return int(min(top,self.link_speed_history(link,time)*multiplier))
        
    def return_focus(self, start):
        found = set()
        start_node =self[start]
        _next = {l for l in start_node.links}
        while len(_next)>0:        
            _next_next = {l for k in _next for l in self[k.target].links if l not in found} #might even be able to drop the "l not in found" thing.
            found |= _next
            _next = _next_next
            if (len(found)>15):
                break
        return found
                    
    def iterlinks(self):
        '''chain all the links in the graph. 
        use: for link in roads.iterlinks(): ... '''
        return (link for j in self.values() for link in j.links)

def _make_link(i,link_string):
    'This function is for local use only'
    link_params = [int(x) for x in link_string.split("@")]
    return Link(i,*(link_params+[Link_traffic_params(*tools.generate_traffic_noise_params(i,link_params[0]))]))

def _make_junction(i_str, lat_str, lon_str, *link_row):
    'This function is for local use only'
    i, lat, lon = int(i_str), float(lat_str), float(lon_str)
    try:
        links = tuple(_make_link(i,lnk)
                 for lnk in link_row)
        links = tuple(filter(lambda lnk: lnk.distance>0,links))
    except ValueError:
        links = []
    return Junction(i, lat, lon, links)


@tools.timed
def load_map_from_csv(filename='israel.csv', start=0, count=sys.maxsize):
    '''returns graph, encoded as an adjacency list
    @param slice_params can be used to cut part of the file
    example: load_map_from_csv(start=50000, count=50000))
    '''

    import csv
    from itertools import islice
    with tools.dbopen(filename, 'rt') as f:
        it = islice(f, start, min(start+count, sys.maxsize))
        lst = {int(row[0]): _make_junction(*row) for row in csv.reader(it)}
        if count < sys.maxsize:
            lst = {i:Junction(i, j.lat, j.lon, tuple(lnk for lnk in j.links if lnk.target in lst))
                              for i, j in lst.items()} 
    return Roads(lst)
