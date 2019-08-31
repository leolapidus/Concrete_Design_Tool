import numpy as np


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
        else:
            cur = []
            past = []
            for i in range(int(len(self.current_x))):
                cur.append(self.current_x[i][0].f)
                past.append(x[i][0].f)
        return not np.allclose(past, cur, rtol=1e-12, atol=1e-12)



    def update_state(self,x):
        self.current_x = np.copy(x)



    def evaluate(self, x, parameters, parametrization):

        if self.state_changed(x):
            #print("Evaluate response!")
            result = self.function(x, parameters, parametrization)
            self._f = result.f
            self._g = result.g
            self._h = result.h
            self.update_state(x)
        else:
            pass
            #print("Skip re-evaluation of response!")



    @staticmethod
    def f(x, *args):
        if len(args)==1:
            _self = args[0][0]
            _self.evaluate(x, args[0][1], args[0][2])
        else:
            _self = args[0]
            _self.evaluate(x, args[1], args[2])
        return _self._f



    @staticmethod
    def g(x, *args):
        if len(args)==1:
            _self = args[0][0]
            _self.evaluate(x, args[0][1], args[0][2])
        else:
            _self = args[0]
            _self.evaluate(x, args[1], args[2])
        return _self._g



    @staticmethod
    def h(x, *args):
        if len(args)==1:
            _self = args[0][0]
            _self.evaluate(x, args[0][1], args[0][2])
        else:
            _self = args[0]
            _self.evaluate(x, args[1], args[2])
        return _self._h