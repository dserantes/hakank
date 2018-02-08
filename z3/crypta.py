#!/usr/bin/python -u
# -*- coding: latin-1 -*-
# 
# Cryptarithmetic puzzle in Z3
#
# Prolog benchmark problem GNU Prolog (crypta.pl)
# '''
# Name           : crypta.pl
# Title          : crypt-arithmetic
# Original Source: P. Van Hentenryck's book
# Adapted by     : Daniel Diaz - INRIA France
# Date           : September 1992
#
# Solve the operation:
#
#    B A I J J A J I I A H F C F E B B J E A
#  + D H F G A B C D I D B I F F A G F E J E
#  -----------------------------------------
#  = G J E G A C D D H F A F J B F I H E E F
# '''

# Note: This is surprisingly slow...
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

  #
  # variables
  #
  LD = [makeIntVar(sol,"LD[%i]" % i, 0, 9) for i in range(0, 10)]
  A, B, C, D, E, F, G, H, I, J = LD

  Sr1 = makeIntVar(sol, "Sr1", 0, 1)
  Sr2 = makeIntVar(sol, "Sr2", 0, 1)

  #
  # constraints
  #
  sol.add(Distinct(LD))
  sol.add(B >= 1)
  sol.add(D >= 1)
  sol.add(G >= 1)

  sol.add(A + 10 * E + 100 * J + 1000 * B + 10000 * B + 100000 * E + 1000000 * F +
             E + 10 * J + 100 * E + 1000 * F + 10000 * G + 100000 * A + 1000000 * F
             == F + 10 * E + 100 * E + 1000 * H + 10000 * I + 100000 * F + 1000000 * B + 10000000 * Sr1)

  sol.add(C + 10 * F + 100 * H + 1000 * A + 10000 * I + 100000 * I + 1000000 * J +
             F + 10 * I + 100 * B + 1000 * D + 10000 * I + 100000 * D + 1000000 * C + Sr1
             == J + 10 * F + 100 * A + 1000 * F + 10000 * H + 100000 * D + 1000000 * D + 10000000 * Sr2)

  sol.add(A + 10 * J + 100 * J + 1000 * I + 10000 * A + 100000 * B +
             B + 10 * A + 100 * G + 1000 * F + 10000 * H + 100000 * D + Sr2
             == C + 10 * A + 100 * G + 1000 * E + 10000 * J + 100000 * G)
  
  num_solutions = 0
  str = "ABCDEFGHIJ"
  while sol.check() == sat:
    num_solutions += 1
    mod = sol.model()
    for (letter, val) in [(str[i], mod.eval(LD[i])) for i in range(len(LD))]:
      print("%s: %i" % (letter, val))
    print()

  print()
  print("num_solutions:", num_solutions)


if __name__ == "__main__":
  main()

