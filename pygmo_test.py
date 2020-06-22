from pygmo import *
from matplotlib import pyplot as plt

udp = zdt(prob_id=1)

#generate an initial population and plot it
#to show nondominated solutions
pop = population(prob=udp, size=100, seed=3453412)
ax = plot_non_dominated_fronts(pop.get_f())
plt.ylim([0,6])
plt.title("ZDT1: random initial population")

algo = algorithm(moead(gen=250))
pop = algo.evolve(pop)
ax = plot_non_dominated_fronts(pop.get_f())
plt.title("Evolved Pop")
plt.show()

hv = hypervolume([[1,0], [0.5,0.5], [0,1], [1.5, 0.75]])
ref_point = [2,2]
print(hv.compute(ref_point))
