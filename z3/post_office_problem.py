#!/usr/bin/python -u
# -*- coding: latin-1 -*-
# 
# Post office problem in Z3
#
# Problem statement:
# http://www-128.ibm.com/developerworks/linux/library/l-glpk2/
#
# From Winston 'Operations Research: Applications and Algorithms':
# '''
# A post office requires a different number of full-time employees working
# on different days of the week [summarized below]. Union rules state that
# each full-time employee must work for 5 consecutive days and then receive
# two days off. For example, an employee who works on Monday to Friday
# must be off on Saturday and Sunday. The post office wants to meet its
# daily requirements using only full-time employees. Minimize the number
# of employees that must be hired.
#
# To summarize the important information about the problem:
#
#   * Every full-time worker works for 5 consecutive days and takes 2 days off
#   * Day 1 (Monday): 17 workers needed
#   * Day 2 : 13 workers needed
#   * Day 3 : 15 workers needed
#   * Day 4 : 19 workers needed
#   * Day 5 : 14 workers needed
#   * Day 6 : 16 workers needed
#   * Day 7 (Sunday) : 11 workers needed
#
# The post office needs to minimize the number of employees it needs
# to hire to meet its demand.
# '''

# 
# This Z3 model was written by Hakan Kjellerstrand (hakank@gmail.com)
# See also my Z3 page: http://hakank.org/z3/
#
from __future__ import print_function
from z3_utils_hakank import *


def main():

  sol = Solver()

  #
  # data
  #

  # days 0..6, monday 0
  n = 7
  days = list(range(n))
  need = [17, 13, 15, 19, 14, 16, 11]

  # Total cost for the 5 day schedule.
  # Base cost per day is 100.
  # Working saturday is 100 extra
  # Working sunday is 200 extra.
  cost = [500, 600, 800, 800, 800, 800, 700]

  #
  # variables
  #

  # No. of workers starting at day i
  x = [makeIntVar(sol, 'x[%i]' % i, 0, 100) for i in days]

  total_cost = makeIntVar(sol, "total_cost", 0, 20000)
  num_workers = makeIntVar(sol, "num_workers", 0, 100)

  #
  # constraints
  #
  sol.add(total_cost == scalar_product2(sol, x, cost))
  sol.add(num_workers == Sum(x))

  for i in days:
    sol.add(Sum([x[j] for j in days
                    if j != (i + 5) % n and j != (i + 6) % n]) >= need[i])

  # objective
  # sol.minimize(total_cost)

  num_solutions = 0
  while sol.check() == sat:
    num_solutions += 1
    mod = sol.model()
    print('num_workers:', mod.eval(num_workers))
    print('total_cost:', mod.eval(total_cost))
    print('x:', [mod.eval(x[i]) for i in days])
    getLessSolution(sol,mod, total_cost)

  print()
  print('num_solutions:', num_solutions)


if __name__ == '__main__':
  main()
