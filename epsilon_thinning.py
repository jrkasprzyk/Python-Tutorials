# From: https://waterprogramming.wordpress.com/2016/03/28/speeding-up-algorithm-diagnosis-by-epsilon-sorting-runtime-files/

import numpy as np
from glob import glob
from os import makedirs, system
from os.path import splitext, basename
 
def apply_epsilon_dominance(epsilons, number_of_objectives):
    files_fronts = []
 
    # Create a folder for each runtime file and store each Pareto front as a 
    # separate file.
    print '\nSpliting Pareto fronts.\n'
    for file in glob('*runtime'):
        print file
 
        s = open(file, 'r')
        fronts = s.read().split('#\r\n')
        folder = splitext(file)[0]
        makedirs(folder)
        for i in range(len(fronts) - 1):
            of = open(folder + "/" + str(i) + ".set", 'w')
            of.write(fronts[i])
            of.write('#')
 
    # Applies new epsilons to each Pareto front
    print '\nApplying new epsilons to each Pareto front.\n'
    for file in glob('*runtime'):
        print file
        folder = splitext(file)[0]
        for i in range(len(fronts) - 1):
            system('java -cp MOEAFramework-2.0-Executable.jar org.'
                'moeaframework.analysis.sensitivity.ResultFileMerger -d ' +
                str(number_of_objectives) + ' ./'+ folder + '/' + str(i) +
                '.set -e ' + epsilons + ' -o ' + folder + '/' +
                str(i).zfill(2) + '.sorted')
 
    # Combines epsilon sorted Pareto fronts in new runtime files with 
    # extension .runtime_sorted
    print '\nCombining sorted fronts into new runtime_sorted files.\n'
    for file in glob('*runtime'):
        print file
        folder = splitext(file)[0]
        output_str = ''
         
        of = open(folder + '.runtime_sorted', 'w')
 
        for f in glob(folder + '/*.sorted'):
            output_str += open(folder + '/' + basename(f)).read() + "#\n"
             
        of.write(output_str)
 
 
# epsilons and number of objectives to be used
epsilons = '0.005,0.02,0.02,0.01,0.01,0.01'
number_of_objectives = 6
 
# Calls the function to apply epsilon dominance
apply_epsilon_dominance(epsilons, number_of_objectives)