from entrypoint2 import entrypoint

__version__='3.2'

@entrypoint
def f(one,two=4,three=False): 
    ''' description
    
    one: par1
    two: par2
    '''
    return one          
