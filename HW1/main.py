'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

#do NOT import ways. This should be done from other files
#simply import your modules and call the appropriate functions


def simple(source, target, start_time):
    'call function to find path, and return list of indices'
    raise NotImplementedError

    
def improved(source, target):
    'call function to find path, and return list of indices'
    raise NotImplementedError
    

def dispatch(argv):
    from sys import argv
    source, target, start_time = int(argv[2]), int(argv[3]), int(argv[4])
    if argv[1] == 'simple':
        path = simple(source, target,start_time)
    elif argv[1] == 'improved':
        path = improved(source, target, start_time)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)
