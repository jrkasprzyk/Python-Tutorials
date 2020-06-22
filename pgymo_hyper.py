from pygmo import *
import timeit

# https://stackoverflow.com/questions/6583573/how-to-read-numbers-from-file-in-python
# This opens a handle to your file, in 'r' read mode
file_handle = open('reference_set.txt', 'r')
# Read in all the lines of your file into a list of lines
lines_list = file_handle.readlines()
my_data = [[float(val) for val in line.split()] for line in lines_list]

ref_point = [0.0]*9

print("5 rows")
hv_from_list = hypervolume(my_data[0:5][:])
start_time = timeit.default_timer()
hv_from_list.compute(ref_point)
print(timeit.default_timer - start_time)


# # Extract dimensions from first line. Cast values to integers from strings.
# cols, rows = (float(val) for val in lines_list[0].split())
# # Do a double-nested list comprehension to get the rest of the data into your matrix
# my_data = [[float(val) for val in line.split()] for line in lines_list[1:]]