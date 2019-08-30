class HJ():
    def __init__(self, val, n,i):

        self.g = [0.0]*n

        self.g[i] = 1.0

        self.f = val



class Parametrization():

    def __init__(self):
        self.parameters = {}
        self.variable_indices = {}



    def add_parameter(self, key, value, is_variable=False):

        if key in self.parameters:
            raise RuntimeError("Key {} already exists!".format(key))

        self.parameters[key] = (value, is_variable)



    def __getitem__(self, key):

        return self.parameters[key][0]



    def initialize(self):

        for key, val in self.parameters.items():
            if val[1]:
                self.variable_indices[key] = len(self.variable_indices)

        for key, i in self.variable_indices.items():
            self.parameters[key] = HJ(self.parameters[key][0],len(self.variable_indices), i)

    def get_variables(self):

        x = []
        for key in self.variable_indices.keys():
            x.append(self.parameters[key])
        return x

    def update(self, x):

        for key, i in self.variable_indices.items():
            self.parameters[key] = x[i]





parameters = Parametrization()

parameters.add_parameter("l1", 10.0)
parameters.add_parameter("l2", 10.0)
parameters.add_parameter("h1", 1.0, is_variable=True)
parameters.add_parameter("h2", 2.0, is_variable=True)
parameters.add_parameter("b1", 0.5)
parameters.add_parameter("b2", 0.5)

parameters.initialize()

print(parameters.parameters)
x = parameters.get_variables()
print(x)
new_x = ["new1", "new2"]
parameters.update(new_x)
print(parameters.parameters)
x = parameters.get_variables()
print(x)