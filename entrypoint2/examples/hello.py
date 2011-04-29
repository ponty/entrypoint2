from entrypoint2 import entrypoint
import logging

__version__ = '3.2'

@entrypoint
def add(one, two=4, three=False): 
    ''' This function adds two number.
    
    :param one: first number to add
    :param two: second number to add
    :rtype: int
    '''
    sum = str(int(one) + int(two))
    
    logging.debug('logging sum from hello.py:' + sum)
    print 'printing sum from hello.py:', sum          
    
    return sum
