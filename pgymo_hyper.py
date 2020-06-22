import pygmo
import timeit
import numpy as np

# read numbers from a file using numpy array
my_data = np.genfromtxt('reference_set.txt', delimiter=" ")

# the above has the decisions and objectives
# for example:
# 14 decisions, therefore 0:ndec are decisions
# 9 objectives, therefore ndec:ndec+nobj are objectives
ndec = 14
nobj = 9
nconstr = 9

# to find the reference point we use the pygmo2 guidance:
#We assume minimization in every dimension, that is, a reference point is required to be numerically larger or equal in each objective, and strictly larger in at least one of them.

ref_point = [0.0]*nobj
ref_point_scaling = 1.5

j = 0
for i in range(ndec, ndec+nobj):
    ref_point[j] = ref_point_scaling*max(my_data[:,i])
    if ref_point[j] < 0.0:
        ref_point[j] = 0.0
    print (f'objective col = {i}, ref = {ref_point[j]}')
    j = j+1

row_tests = [30, 50, 100, 200, 300, 507]

for row in row_tests:
    start_time = timeit.default_timer()
    hv_from_list = pygmo.hypervolume(my_data[0:row, ndec:ndec+nobj])
    my_hv_result = hv_from_list.compute(ref_point)
    print(f'For {row} rows, the hv is {my_hv_result} and the time is {timeit.default_timer() - start_time}.')