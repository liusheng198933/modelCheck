from z3 import *
import os

X = [ Int("x_%s" % (i+1)) for i in range(2) ]
# old path variable

Y = [ Int("y_%s" % (i+1)) for i in range(2) ]

range_x  = [ And(0 < X[i], X[i] <= 1) for i in range(2)]

range_y  = [ And(0 <= Y[i], Y[i] <= 1) for i in range(2)]

con_1 = [Implies(X[i] == 1, Y[i] == 0) for i in range(2)]

srcNode = [ Int("src_%s" % (i+1)) for i in range(flowNum) ]
dstNode = [ Int("dst_%s" % (i+1)) for i in range(flowNum) ]

s = Solver()
s.add(range_x + range_y + con_1)

if s.check() == sat:
    m = s.model()

    r = [ m.evaluate(X[j])  for j in range(2)]
    print 'x value:'
    print_matrix(r)

    r = [ m.evaluate(Y[j])  for j in range(2)]
    print 'y value:'
    print_matrix(r)
