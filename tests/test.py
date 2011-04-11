from easyprocess import Proc
from nose.tools import eq_
from unittest import TestCase
from path import path

d = path(__file__).parent

class Test(TestCase):
    def test_1_call(self):
        import example1
        eq_(example1.f(3), 3) 
        eq_('description' in example1.f.__doc__ , True) 
        eq_(example1.f.__name__, 'f') 
    
    def test_2_call(self):
        import example2 
        eq_(example2.f(5, 1), 6) 
        eq_(example2.f.__doc__, None) 
        eq_(example2.f.__name__, 'f') 

    def test_3_call(self):
        import example3 
        eq_(example3.f(), 7) 
        eq_(example3.f.__doc__, None) 
        eq_(example3.f.__name__, 'f') 

    
    
    def test_1_cli(self):
        cmd = 'python %s 5' % (d / 'example1.py')
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 
         
        cmd = 'python %s 5 --two 7 --debug' % (d / 'example1.py')
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 

        cmd = 'python %s 5 --three -t 2 --debug' % (d / 'example1.py')
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 

        cmd = 'python %s 5 -t x' % (d / 'example1.py')
        p = Proc(cmd).call()
        eq_(p.return_code > 0, 1)
        eq_(p.stdout, '') 
        eq_(p.stderr != '', 1) 
    
        cmd = 'python %s -t 1  5  --debug' % (d / 'example1.py')
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 
    
    def test_2_cli(self):
        cmd = 'python %s 5 2' % (d / 'example2.py')
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 
         
        cmd = 'python %s --debug    5 2' % (d / 'example2.py')
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, 'DEBUG:root:5') 

    def test_1_ver(self):
        cmd = 'python %s --version' % (d / 'example1.py')
        p = Proc(cmd).call()
        eq_(p.stdout, '') 
        eq_(p.stderr, '3.2') 
        eq_(p.return_code, 0)

    def test_2_ver(self):
        cmd = 'python %s --version' % (d / 'example2.py')
        p = Proc(cmd).call()
        eq_(p.stdout, '') 
        eq_(p.stderr, '1.2') 
        eq_(p.return_code, 0)
    
    def test_3_ver(self):
        cmd = 'python %s --version' % (d / 'example3.py')
        p = Proc(cmd).call()
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 
        eq_(p.return_code, 0)
    


    def test_1_help(self):
        cmd = 'python %s --help' % (d / 'example1.py')
        p = Proc(cmd).call()
        eq_(p.stderr, '') 
        eq_(p.return_code, 0)
        eq_('one' in p.stdout, 1) 
        eq_('--two' in p.stdout, 1) 
        eq_('-t' in p.stdout, 1) 
        eq_('--three' in p.stdout, 1) 

    def test_2_help(self):
        cmd = 'python %s --help' % (d / 'example2.py')
        p = Proc(cmd).call()
        eq_(p.stderr, '') 
        eq_(p.return_code, 0)

    def test_3_help(self):
        cmd = 'python %s --help' % (d / 'example3.py')
        p = Proc(cmd).call()
        eq_(p.stderr, '') 
        eq_(p.return_code, 0)
