import numpy, math

def inverse_method(list_tuple):
    u = numpy.random.uniform()
    acum = 0
    for service, prob in list_tuple:
        acum += prob
        if u < acum:
            return service
    return 0

def exp_dist(lamb:int, uniform_dist = numpy.random.uniform()):
    return -(1/lamb)*math.log(uniform_dist)


def normal_dist(mean = 5, var = 2):
    while True:
        y = exp_dist(1)
        u = numpy.random.uniform()
        c = math.exp((-(y - 1)**2) / 2)
        if u <= c:
            return mean + var * y 
    return 0
