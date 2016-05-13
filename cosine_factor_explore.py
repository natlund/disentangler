from matplotlib import pyplot as plt
import math

xx = range(-31, 31)
x = [0.1*x for x in xx]

cos = [math.cos(a) for a in x]

fact = [1.0/(1.1 - a) - 0.476190 for a in cos]

print x
print cos
print fact

plt.plot(x, cos)
plt.show()
plt.plot(x, fact)
plt.show()
