from platypus import NSGAII, Problem, Real, nondominated, Hypervolume, calculate


def belegundu(vars):
    x = vars[0]
    y = vars[1]
    return [-2 * x + y, 2 * x + y], [-x + y - 1, x + y - 7]


problem = Problem(2, 2, 2)
problem.types[:] = [Real(0, 5), Real(0, 3)]
problem.constraints[:] = "<=0"
problem.function = belegundu

algorithm = NSGAII(problem)
algorithm.run(10000)

feasible_solutions = [s for s in algorithm.result if s.feasible]
nondominated_solutions = nondominated(algorithm.result)

hyp = Hypervolume(minimum=[0, 0, 0], maximum=[1, 1, 1])
hyp_result = calculate(algorithm.result, hyp)
print(hyp_result)
pass