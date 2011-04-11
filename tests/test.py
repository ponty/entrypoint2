from nose.tools import eq_
from unittest import TestCase
from easyprocess import Proc

class Test(TestCase):
    def test_1_call(self):
        import example1
        eq_(example1.f(3), 3) 
    
    def test_2_call(self):
        import example2 
        eq_(example2.f(5, 1), 6) 

    def test_3_call(self):
        import example3 
        eq_(example3.f(), 7) 

    
    
    def test_1_cli(self):
        cmd = 'python example1.py 5'
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 
         
        cmd = 'python example1.py 5 --two 7 --debug'
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 

        cmd = 'python example1.py 5 --three -t 2 --debug'
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 

        cmd = 'python example1.py 5 -t x'
        p = Proc(cmd).call()
        eq_(p.return_code > 0, 1)
        eq_(p.stdout, '') 
        eq_(p.stderr != '', 1) 
    
        cmd = 'python example1.py -t 1  5  --debug'
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 
    
    def test_2_cli(self):
        cmd = 'python example2.py 5 2'
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 
         
        cmd = 'python example2.py --debug    5 2'
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '') 
        eq_(p.stderr, 'DEBUG:root:5') 

    def test_1_ver(self):
        cmd = 'python example1.py --version'
        p = Proc(cmd).call()
        eq_(p.stdout, '') 
        eq_(p.stderr, '3.2') 
        eq_(p.return_code, 0)

    def test_2_ver(self):
        cmd = 'python example2.py --version'
        p = Proc(cmd).call()
        eq_(p.stdout, '') 
        eq_(p.stderr, '1.2') 
        eq_(p.return_code, 0)
    
    def test_3_ver(self):
        cmd = 'python example3.py --version'
        p = Proc(cmd).call()
        eq_(p.stdout, '') 
        eq_(p.stderr, '') 
        eq_(p.return_code, 0)
    


    def test_1_help(self):
        cmd = 'python example1.py --help'
        p = Proc(cmd).call()
        eq_(p.stderr, '') 
        eq_(p.return_code, 0)
        eq_('one' in p.stdout, 1) 
        eq_('--two' in p.stdout, 1) 
        eq_('-t' in p.stdout, 1) 
        eq_('--three' in p.stdout, 1) 

    def test_2_help(self):
        cmd = 'python example2.py --help'
        p = Proc(cmd).call()
        eq_(p.stderr, '') 
        eq_(p.return_code, 0)

    def test_3_help(self):
        cmd = 'python example3.py --help'
        p = Proc(cmd).call()
        eq_(p.stderr, '') 
        eq_(p.return_code, 0)
