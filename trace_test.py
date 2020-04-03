from z3 import *
import os

result_path = '/result/result_1.txt'

# variable definition
#ruleNum = 1
flowNum = 2
nodeNum = 10
pathLength = 6
midPathLength = pathLength * 3
pathMaxLength = pathLength * 4
#newTag = 2
#nfNum = 2
seqNum = 2
verNum = 1

X = [[ Int("x_%s_%s" % (i+1, j+1)) for i in range(pathLength) ] for j in range(flowNum)]
# old path variable

Y = [[ Int("y_%s_%s" % (i+1, j+1)) for i in range(pathLength) ] for j in range(flowNum)]
# new path variable

Z = [[ Int("z_%s_%s" % (i+1, j+1)) for i in range(midPathLength) ] for j in range(flowNum)]

NFSeqX = [[ Int("nfseqx_%s_%s" % (i+1, j+1)) for i in range(seqNum) ] for j in range(flowNum)]

NFSeqY = [[ Int("nfseqy_%s_%s" % (i+1, j+1)) for i in range(seqNum) ] for j in range(flowNum)]

srcNode = [ Int("src_%s" % (i+1)) for i in range(flowNum) ]
dstNode = [ Int("dst_%s" % (i+1)) for i in range(flowNum) ]

#range limit for each variable

route_x  = [ And(0 < X[i][j], X[i][j] <= nodeNum + 2*flowNum) for i in range(flowNum) for j in range(pathLength)]

route_y  = [ And(0 < Y[i][j], Y[i][j] <= nodeNum + 2*flowNum) for i in range(flowNum) for j in range(pathLength)]

route_z  = [ Or([Or(Z[i][j] == X[i][m], Z[i][j] == Y[i][m]) for m in range(pathLength)]) for i in range(flowNum) for j in range(midPathLength)]

src_range  = [ srcNode[i] == nodeNum + i + 1 for i in range(flowNum)]

dst_range  = [ dstNode[i] == nodeNum + flowNum + i + 1 for i in range(flowNum)]

nfv_range0  = [ And(1 <= NFSeqX[i][j], NFSeqX[i][j] < pathLength-1) for i in range(flowNum) for j in range(seqNum)]

nfv_range1  = [ And(1 <= NFSeqY[i][j], NFSeqY[i][j] < pathLength-1) for i in range(flowNum) for j in range(seqNum)]

nfv_order0 = [ NFSeqX[i][m] < NFSeqX[i][m+1] for i in range(flowNum) for m in range(seqNum-1)]

nfv_order1 = [ NFSeqY[i][m] < NFSeqY[i][m+1] for i in range(flowNum) for m in range(seqNum-1)]

dst_x = [Implies(X[i][j] == dstNode[i], X[i][j+1] == dstNode[i]) for i in range(flowNum) for j in range(pathLength - 1)]

dst_y = [Implies(Y[i][j] == dstNode[i], Y[i][j+1] == dstNode[i]) for i in range(flowNum) for j in range(pathLength - 1)]

dst_z = [Implies(Z[i][j] == dstNode[i], Z[i][j+1] == dstNode[i]) for i in range(flowNum) for j in range(midPathLength - 1)]

distinct_x = [ Implies(X[k][i] == X[k][i+j+1], X[k][i] == dstNode[k]) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

distinct_y = [ Implies(Y[k][i] == Y[k][i+j+1], Y[k][i] == dstNode[k]) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

distinct_z1 = [ Z[k][i] != srcNode[k] for k in range(flowNum) for i in range(1, midPathLength)]

distinct_z2 = [ Implies(Z[k][i] != dstNode[k], Z[k][i] != Z[k][i+1]) for k in range(flowNum) for i in range(midPathLength-1)]


middlepath_seq1 = [ Implies(And(NFSeqY[i][j] == k1, NFSeqY[i][j+1] == k2, Z[i][m] == Y[i][k1]), \
                            Or([ Z[i][n] == Y[i][k2] for n in range(m+1, midPathLength) ])) for i in range(flowNum) for j in range(seqNum-1) for m in range(midPathLength) for k1 in range(pathLength) for k2 in range(pathLength)]

middlepath_seq2 = [ Implies(And(NFSeqX[i][j] == k1, NFSeqY[i][j] == k2, Z[i][m] == X[i][k1]), \
                            Or([ Z[i][n] == Y[i][k2] for n in range(m+1, midPathLength) ])) for i in range(flowNum) for j in range(seqNum) for m in range(midPathLength) for k1 in range(pathLength) for k2 in range(pathLength)]

middlepath_seq3 = [ Implies(NFSeqX[i][j] == k, Or([ Z[i][n] == X[i][k] for n in range(midPathLength) ])) for i in range(flowNum) for j in range(seqNum) for k in range(pathLength)]



init_x = [X[i][0] == srcNode[i] for i in range(flowNum)]
init_y = [Y[i][0] == srcNode[i] for i in range(flowNum)]
init_z = [Z[i][0] == srcNode[i] for i in range(flowNum)]
final_x = [X[i][pathLength-1] == dstNode[i] for i in range(flowNum)]
final_y = [Y[i][pathLength-1] == dstNode[i] for i in range(flowNum)]
final_z = [Z[i][midPathLength-1] == dstNode[i] for i in range(flowNum)]

s = Solver()

s.add(route_x + route_y + route_z + src_range + dst_range)
s.add(dst_x + dst_y + dst_z + distinct_x + distinct_y + distinct_z1 + distinct_z2 + nfv_order0 + nfv_order1 + nfv_range0 + nfv_range1)
s.add(middlepath_seq1 + middlepath_seq2 + middlepath_seq3)
s.add(init_x + init_y + init_z + final_x + final_y + final_z)

if s.check() == sat:
    m = s.model()
    for i in range(flowNum):
        r = [ m.evaluate(X[i][j]) for j in range(pathLength) ]
        print 'Old route:'
        print_matrix(r)

        r = [ m.evaluate(Y[i][j]) for j in range(pathLength) ]
        print 'New route:'
        print_matrix(r)

        r = [ m.evaluate(Z[i][j]) for j in range(midPathLength) ]
        print 'Mid route:'
        print_matrix(r)

        r = [ m.evaluate(NFSeqX[i][j]) for j in range(seqNum) ]
        print 'Old nf:'
        print_matrix(r)

        r = [ m.evaluate(NFSeqY[i][j]) for j in range(seqNum) ]
        print 'New nf:'
        print_matrix(r)
