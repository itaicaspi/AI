# -*- coding: utf-8 -*-

from time import clock
import zlib
from math import acos, radians, pi
from numpy import ones, cos,array, sin
'General tools'

DB_DIRNAME = 'db/'

'This is arbitrary, and will change in the tests'
SEED = 0x23587643

def dhash(*data):
    'Generates a random-looking deterministic hash'
    return abs(zlib.adler32(bytes(str(data),'UTF-8'))*100) * SEED % 0xffffffff
## The move from python 2 to 3 caused some problems.

def dbopen(fname, *args, **kwargs):
    'make sure we are in the correct directory'
    if not fname.startswith(DB_DIRNAME):
        fname = DB_DIRNAME + fname
    return open(fname, *args, **kwargs)


'DMS := Degrees, Minutes, Seconds'
def float2dms(decimal_degrees):
    degrees = int(decimal_degrees)
    minutes = int(60 * (decimal_degrees - degrees))
    seconds = int(3600 * (decimal_degrees - degrees - minutes / 60))
    return (degrees, minutes, seconds)


def dms2float(degrees, minutes, seconds=0):
    return degrees + minutes / 60 + seconds / 3600


def compute_distance(lat1, lon1, lat2, lon2):
    '''computes distance in KM'''
    '''
    This code was borrowed from 
    http://www.johndcook.com/python_longitude_latitude.html
    '''
    if (lat1, lon1) == (lat2, lon2):
        return 0.0
    if max(abs(lat1 - lat2), abs(lon1 - lon2)) < 0.00001:
        return 0.001

    phi1 = radians(90 - lat1)
    phi2 = radians(90 - lat2)
    
    meter_units_factor = 40000 / (2 * pi)
    arc = acos(sin(phi1) * sin(phi2) * cos(radians(lon1) - radians(lon2))
             + cos(phi1) * cos(phi2))
    return arc * meter_units_factor


class Everything(object):
    '(Lousy) complement for the empty set'
    def __contains__(self, val):
        return True

def base_traffic_pattern():
        ''' Creates a base traffic pattern:
            we can go at max speed (divide by 1)
            traffic gets worse at 6 AM and 3 PM, with peak at 8 AM and 5 PM, 
            and then it subsides again within 2 hours'''
            
        base_pattern = ones(60*24)
        base_pattern[(60*6):(10*60)] += cos(((array(range(4*60))/(4*60))-0.5)*pi)
        base_pattern[(15*60):(19*60)] += base_pattern[(60*6):(10*60)]
        return list(base_pattern)
        
def generate_traffic_noise_params(seed1,seed2):
    ''' generates some parameters for the traffic noise
    It should look random, and it is symmetrical
    (Can't think why it has to be symmetrical, but it would be easy enough to
    modify it not to be if need be) '''
    wavelength_cos = 60 + 20*(dhash(seed1+seed2)/0xffffffff) - 10
    wavelength_sin = 60 + 20*(dhash(seed1*seed2)/0xffffffff) - 10
    return(wavelength_cos,wavelength_sin)
    ## should It only be positive addition to the multiplier? A* needs an optimistic hueristic
        
def generate_slowdown_multiplier(road_length, road_maxspeed, base_val, param1, param2,time):
    multiplier = (cos(time*pi/param1) + sin(time*pi/param2))/2 + base_val + 1 ## multiplier must always be >= 1
    ## That's why I add 1, because sin and cos get a minimum of -1.
    km_per_minute=road_maxspeed/60
    if (km_per_minute/road_length)<0.06:
        multiplier = multiplier*km_per_minute/(0.06*road_length)
    return max(1,multiplier)
    
''' explanation for generate_slowdown_multiplier:
We want to make sure someone who enters the same road 1 minute after you cannot
exit the road BEFORE you.

let SM_t be the Speed Multiplier - the value by which we divide max_Speed
Alternatively, how many times more would it take us to get from one end of the
road to another compared to driving at max. speed

SM_t*(length/max_speed)-1 <= SM_(t+1)*(length/max_speed)
What this says: the time it would take us to get from one end to another of we
got in at time t is no greater than (1 minute more than it would take us if we
enter 1 minute later)

In other words, we would get out before (or at the same time as) whomever
enters 1 minute after us.

note that we're talking about minutes here, so max_speed is in KM/minute

Now, we get (SM_t - SM_(t+1)) <= max_speed/length

Using the limits on the wavelength of the cos and sine function I've used, I've
gotten an estimate: the difference between two subsequent multipliers is no
greater than 0.04 (this is a higher bound, but not a very tight one)

And there you have it. if 0.04 is still greater than (max_speed/length),
I rescale everything to make sure It's all good.
Also, never take a multiplier smaller than 1. we don't want to drive over max.
speed, though I think the multiplier will always be > 1, this is just in case.

I actually changed it to 0.06 just in case, because the realtime thing is 
different

'''    

def timed(f):
    '''decorator for printing the timing of functions
    usage: 
    @timed
    def some_funcion(args...):'''
    
    def wrap(*x, **d):
        start = clock()
        res = f(*x, **d)
        print(f.__name__, ':', clock() - start)
        return res
    return wrap


if __name__ == '__main__':
    for i in range(100):
        print(dhash(i))
