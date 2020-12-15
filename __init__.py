'''
Non - standart module
'''

from functools import wraps, WRAPPER_ASSIGNMENTS as assigned

__all__ = ['simple_args', 'curry']

class Curry_state ():
    def __init__ (self, func, count, args = None):
        self.func = func
        self.count = count
        self.args = args if args else []

    def __call__ (self, *args):
        if not args:
            return self.func (*self.args)
        
        args_ = self.args.copy ()
        
        for i in args:
            args_.append (i)

        if len (args_) >= self.count and self.count != -1:
            return self.func (*args_)

        else:
            return Curry_state (self.func, self.count, args_)

    def __repr__ (self):
        args = self.args.copy ()
        args.extend (['...' for i in range (self.count - len (args))])
        
        bracets = ', '.join ([str (i) for i in args])

        return f'<Curry_state obj `{self.func.__name__} ({bracets})`>'

def simple_args (dec):
    '''
    Decorator, that adding args to decorators, usage:

    >>> @tools.simple_args
    ... def any_decorator (func, arg1, arg2):
    ...     def wrapper (*args, **kwargs):
    ...         return func (arg1, arg2, *args, **kwargs)
    ...
    ...     return wrapper
    ...
    >>> @any_decorator ('arg1', 'arg2')
    ... def any_function (a, b, c):
    ...     return sorted ([a, b, c])
    ...
    >>> any_function ('a')
    ['a', 'arg1', 'arg2']    
    '''
    
    @wraps (dec)
    def new_decorator (*args, **kwargs):
        def subdecorator (func):
            return wraps (func) (dec (func, *args, **kwargs))

        return subdecorator

    new_decorator.wrapped = dec
    
    return new_decorator

@simple_args
def curry (func, count):
    """
    Decorator for currying functions, usage:

    >>> @curry (3)
    ... def logger (tag, time, note):
    ...     string = f'[{ tag.upper () }] ({ time }) : { note }'
    ...     print (string)
    ...     return string
    ...
    >>> logger ('bug', '00', 'Bug at main ()')
    [BUG] (00) : Bug at main ()
    '[BUG] (00) : Bug at main ()'
    >>> bug_logger = logger ('bug')
    >>> bug_logger ('01', 'Bug at line 42')
    [BUG] (01) : Bug at line 42
    '[BUG] (01) : Bug at line 42'
    >>> now_bugs = bug_logger ('02')
    >>> now_bugs ('Syntax error')
    [BUG] (02) : Syntax error
    '[BUG] (02) : Syntax error'
    >>> 
    >>> @curry (-1) #Spesial val, using for *args functions
    ... def print_peer_second (*args):
    ...     from time import sleep
    ...     for item in args:
    ...         print (item)
    ...         sleep (1)
    ...
    >>> print_peer_second (1)
    <Curry_state obj `print_peer_second (1)`>
    >>> print_123 = print_peer_second (1) (2) (3)
    >>> print_123 ()
    1  #...
    2  #...
    3  #...
    """

    return Curry_state (func, count)

def add_argumenter (func, generator): #Stupid name
    func = Curry_state (func, -1)

    for arg in generator:
        func = func (arg)

        yield func

if __name__ == '__main__':
    log = input ('Log: ').lower ().strip ()

    if log in ('all', 'args', 'simple', 'simple_args'):
        print (simple_args)
        
        @simple_args
        def ex_decorator (f, a, b):
            '''
            EX_DECORATOR docstring
            '''
            
            def wrap (*args, **kwargs):
                print (a, b)
                print (*args, **kwargs)

            return wrap
        
        @ex_decorator ('a', 'b')
        def ex_function (D):
            '''
            EX_FUNCTION docstring
            '''
            print (D)

    if log in ('all', 'curry'):
        print (curry)

        @curry (3)
        def a (a, b, c):
            print (a, b, c)
