import numpy as np

import scipy.optimize

class Hyperjet():

    def __init__(self,val):

        self.f = val**2
        self.g = np.array([2*val])
        self.h = np.array([[1.0]])



def func(x,parameters):

    return Hyperjet(x[0])



class HyperJetResponseWrapper():
    """
    Small class that wraps a function that has a HyperJet as result.
    It allows the usage in
    """

    def __init__(self,response_function):
        self.function = response_function
        self._f = None
        self._g = None
        self._h = None
        self.current_x = None



    def state_changed(self,x):

        if self.current_x is None:
            return True

        return not np.allclose(x, self.current_x, rtol=1e-12, atol=1e-12)



    def update_state(self,x):
        self.current_x = np.copy(x)



    def evaluate(self, x, parameters):

        if self.state_changed(x):
            print("Evaluate response!")
            result = self.function(x, parameters)
            self._f = result.f
            self._g = result.g
            self._h = result.h
            self.update_state(x)
        else:
            print("Skip re-evaluation of response!")



    @staticmethod
    def f(x, *args):
        _self = args[0]
        _self.evaluate(x, args[1])
        return _self._f



    @staticmethod
    def g(x, *args):
        _self = args[0]
        _self.evaluate(x, args[1])
        return _self._g



    @staticmethod
    def h(x, *args):
        _self = args[0]
        _self.evaluate(x, args[1])
        return _self._h



new_f = HyperJetResponseWrapper(func)



x = np.array([3.0])



r = scipy.optimize.minimize(new_f.f, x, args=(new_f, {"test":1, "test445":"ksjdfh"}), jac=new_f.g, hess=new_f.h)

print(r)
