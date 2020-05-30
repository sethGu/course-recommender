from numpy.random import seed
from numpy.random import randint
from random import sample

seed(1)

values = list(randint(3, 8, 120))
print(values, type(values))

li = [i for i in range(20)]
subset = sample(li, 20)
print(subset)
print(type(subset))