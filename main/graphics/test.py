import matplotlib.pyplot as plt;
from random import randint;

x = [];
y = [];
for _ in range(1, 30000):
    y += [randint(0, 100)];
    x += [randint(0, 100)];

plt.plot(x,y, 'ro');
plt.show();