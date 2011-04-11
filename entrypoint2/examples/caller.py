import hello
from entrypoint2 import entrypoint
import logging

__version__='5.2'

@entrypoint
def f(): 
    ''' calls hello
    '''
    sum=hello.add(7,2)          

    logging.debug('logging sum from caller.py:' + sum)
    print 'printing sum from caller.py:', sum          
