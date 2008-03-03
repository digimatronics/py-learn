

import unittest

from result import ResultBase
from op import Op
from env import Env

from link import *

class Double(ResultBase):

    def __init__(self, data, name = "oignon"):
        assert isinstance(data, float)
        ResultBase.__init__(self, role = None, data = data, name = name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class MyOp(Op):

    nin = -1

    def __init__(self, *inputs):
        assert len(inputs) == self.nin
        for input in inputs:
            if not isinstance(input, Double):
                raise Exception("Error 1")
        self.inputs = inputs
        self.outputs = [Double(0.0, self.__class__.__name__ + "_R")]
    
    def perform(self):
        self.outputs[0].data = self.impl(*[input.data for input in self.inputs])


class Unary(MyOp):
    nin = 1

class Binary(MyOp):
    nin = 2

        
class Add(Binary):
    def impl(self, x, y):
        return x + y
        
class Sub(Binary):
    def impl(self, x, y):
        return x - y
        
class Mul(Binary):
    def impl(self, x, y):
        return x * y
        
class Div(Binary):
    def impl(self, x, y):
        return x / y


import modes
modes.make_constructors(globals())


def inputs():
    x = modes.BuildMode(Double(1.0, 'x'))
    y = modes.BuildMode(Double(2.0, 'y'))
    z = modes.BuildMode(Double(3.0, 'z'))
    return x, y, z

def env(inputs, outputs, validate = True, features = []):
    inputs = [input.r for input in inputs]
    outputs = [output.r for output in outputs]
    return Env(inputs, outputs, features = features, consistency_check = validate)

def perform_linker(env):
    lnk = PerformLinker(env)
    lnk.compile()
    return lnk


class _test_PerformLinker(unittest.TestCase):

    def test_0(self):
        x, y, z = inputs()
        e = mul(add(x, y), div(x, y))
        perform_linker(env([x, y, z], [e])).run()
        assert e.r.data == 1.5


if __name__ == '__main__':
    unittest.main()




        
