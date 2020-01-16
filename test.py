from numpy.random import seed
from numpy.random import randint

seed(1)

values = list(randint(3, 7, 20))
print(values, type(values))
