from z3 import *
import os

result_path = '/result/result_1.txt'

# variable definition
#ruleNum = 1
flowNum = 1
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

#XNF = [[ Int("x_%s_%s" % (i+1, j+1)) for i in range(pathLength+2) ] for j in range(flowNum)]
#YNF = [[ Int("y_%s_%s" % (i+1, j+1)) for i in range(pathLength+2) ] for j in range(flowNum)]

#srcNode = [ Int("src_%s" % (i+1)) for i in range(flowNum) ]
#destNode = [ Int("dst_%s" % (i+1)) for i in range(flowNum) ]


P = [[ Int("pa_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]
# packet trace

PACT = [[ Int("pact_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]
# packet trace action

PROS = [[[ Int("pros_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(seqNum)] for i in range(pathMaxLength) ] for j in range(flowNum)]

#Action0 = [[ Int("act0_%s_%s" % (i+1, j+1)) for i in range(flowNum)] for j in range(nodeNum)]
# old rule action

#Action1 = [[ Int("act1_%s_%s_%s" % (i+1, j+1)) for i in range(flowNum)] for j in range(nodeNum)]
# new rule action

#range limit for each variable

route_x  = [ And(0 < X[i][j], X[i][j] <= nodeNum) for i in range(flowNum) for j in range(pathLength)]

route_y  = [ And(0 < Y[i][j], Y[i][j] <= nodeNum) for i in range(flowNum) for j in range(pathLength)]

route_z  = [ Or([Or(Z[i][j] == X[i][m], Z[i][j] == Y[i][m]) for m in range(pathLength)]) for i in range(flowNum) for j in range(midPathLength)]


nfv_range0  = [ And(1 <= NFSeqX[i][j], NFSeqX[i][j] < pathLength-1) for i in range(flowNum) for j in range(seqNum)]

nfv_range1  = [ And(1 <= NFSeqY[i][j], NFSeqY[i][j] < pathLength-1) for i in range(flowNum) for j in range(seqNum)]

nfv_order0 = [ NFSeqX[i][m] < NFSeqX[i][m+1] for i in range(flowNum) for m in range(seqNum-1)]

nfv_order1 = [ NFSeqY[i][m] < NFSeqY[i][m+1] for i in range(flowNum) for m in range(seqNum-1)]

#action_range0 = [ And(0 <= Action0[i][j], Action0[i][j] <= nodeNum) for i in range(nodeNum) for j in range(flowNum)]

#action_range1 = [ And(0 <= Action1[i][j], Action1[i][j] <= nodeNum) for i in range(nodeNum) for j in range(flowNum)]

pact_range = [ And(0 <= PACT[i][j], PACT[i][j] <= verNum) for i in range(flowNum) for j in range(pathMaxLength)]

pact_const = [ PACT[i][j] <= PACT[i][j+1] for i in range(flowNum) for j in range(pathMaxLength-1)]

dst_x = [Implies(X[i][j] == nodeNum, X[i][j+1] == nodeNum) for i in range(flowNum) for j in range(pathLength - 1)]

dst_y = [Implies(Y[i][j] == nodeNum, Y[i][j+1] == nodeNum) for i in range(flowNum) for j in range(pathLength - 1)]

dst_z = [Implies(Z[i][j] == nodeNum, Z[i][j+1] == nodeNum) for i in range(flowNum) for j in range(midPathLength - 1)]

distinct_x = [ Implies(X[k][i] == X[k][i+j+1], X[k][i] == nodeNum) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

distinct_y = [ Implies(Y[k][i] == Y[k][i+j+1], Y[k][i] == nodeNum) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

distinct_z1 = [ Z[k][i] != 1 for k in range(flowNum) for i in range(1, midPathLength)]

distinct_z2 = [ Implies(Z[k][i] != nodeNum, Z[k][i] != Z[k][i+1]) for k in range(flowNum) for i in range(midPathLength-1)]


middlepath_seq1 = [ Implies(And(NFSeqY[i][j] == k1, NFSeqY[i][j+1] == k2, Z[i][m] == Y[i][k1]), \
                            Or([ Z[i][n] == Y[i][k2] for n in range(m+1, midPathLength) ])) for i in range(flowNum) for j in range(seqNum-1) for m in range(midPathLength) for k1 in range(pathLength) for k2 in range(pathLength)]

middlepath_seq2 = [ Implies(And(NFSeqX[i][j] == k1, NFSeqY[i][j] == k2, Z[i][m] == X[i][k1]), \
                            Or([ Z[i][n] == Y[i][k2] for n in range(m+1, midPathLength) ])) for i in range(flowNum) for j in range(seqNum) for m in range(midPathLength) for k1 in range(pathLength) for k2 in range(pathLength)]

middlepath_seq3 = [ Implies(NFSeqX[i][j] == k, Or([ Z[i][n] == X[i][k] for n in range(midPathLength) ])) for i in range(flowNum) for j in range(seqNum) for k in range(pathLength)]


path_range = [ And(0 <= P[i][j], P[i][j] <= nodeNum) for i in range(flowNum) for j in range(pathMaxLength)]

drop = [Implies(P[h][i] == 0, And([P[h][i+j+1] == 0 for j in range(pathMaxLength-1-i)])) for h in range(flowNum) for i in range(pathMaxLength-1)]


rule_actionx1 = [Implies(And(X[j][m] == i+1, P[j][h] == i+1, PACT[j][h] == 0), P[j][h+1] == X[j][m+1]) for h in range(pathMaxLength-1) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]


rule_actionx2 = [Implies(And(NFSeqX[i][j] == k, X[i][k] == m+1, P[i][h] == m+1, PACT[i][h] == 0, PROS[i][h][j] == 0), \
                         PROS[i][h][j] == 1) for m in range(nodeNum) for i in range(flowNum) for j in range(seqNum) for k in range(pathLength) for h in range(pathMaxLength)]

rule_dst = [Implies(P[j][h] == nodeNum, P[j][h+1] == nodeNum) for h in range(pathMaxLength-1) for j in range(flowNum)]


rule_actionz1 = [Implies(And(P[j][h] == Z[j][0], PACT[j][h] == 1), P[j][h+1] == Z[j][1]) for j in range(flowNum) for h in range(pathMaxLength-1)]
# three consecutive same points in Z?
rule_actionz2 = [Implies(And(P[j][h] == Z[j][m], P[j][h+1] == Z[j][m+1], PACT[j][h+1] == 1), \
                         P[j][h+2] == Z[j][m+2]) for j in range(flowNum) for h in range(pathMaxLength-2) for m in range(midPathLength-2)]


rule_actionz3 = [Implies(And(NFSeqY[i][j] == k, P[i][h] == Y[i][k], PACT[i][h] == 1, PROS[i][h][j] == 0, PROS[i][h][j-1] == 1), \
                         PROS[i][h+1][j] == 1) for i in range(flowNum) for j in range(1, seqNum) for k in range(pathLength) for h in range(pathMaxLength-1)]

rule_actionz4 = [Implies(And(NFSeqY[i][0] == k, P[i][h] == Y[i][k], PACT[i][h] == 1, PROS[i][h][0] == 0), \
                         PROS[i][h+1][0] == 1) for i in range(flowNum) for k in range(pathLength) for h in range(pathMaxLength-1)]

bug_fix1 = [Implies(And(P[j][h] != Z[j][m], P[j][h+1] == Z[j][m+1], PACT[j][h+1] == 1, And([Z[j][a] != Z[j][m+1] for a in range(m)])), \
                         P[j][h+2] == Z[j][m+2]) for j in range(flowNum) for h in range(pathMaxLength-2) for m in range(midPathLength-2)]

bug_fix2 = [Implies(And([P[j][h] != Z[j][m] for m in range(midPathLength)]), PACT[j][h] == 0) for h in range(pathMaxLength) for j in range(flowNum)]


pros_change1 = [Implies(And(P[j][h] != Y[j][k], NFSeqY[j][i] == k, PACT[j][h] == 1), PROS[j][h][i] == PROS[j][h+1][i]) for k in range(pathLength) for i in range(seqNum) for h in range(pathMaxLength-1) for j in range(flowNum)]

pros_change2 = [Implies(And(P[j][h] == Y[j][k], NFSeqY[j][i] == k, PACT[j][h] == 1, PROS[j][h][i] == 1), PROS[j][h+1][i] == 1) for k in range(pathLength) for i in range(seqNum) for h in range(pathMaxLength-1) for j in range(flowNum)]

pros_change3 = [Implies(And(P[j][h] != X[j][k], NFSeqX[j][i] == k, PACT[j][h] == 0), PROS[j][h][i] == PROS[j][h+1][i]) for k in range(pathLength) for i in range(seqNum) for h in range(pathMaxLength-1) for j in range(flowNum)]

pros_change4 = [Implies(And(P[j][h] == X[j][k], NFSeqX[j][i] == k, PACT[j][h] == 0, PROS[j][h][i] == 1), PROS[j][h+1][i] == 1) for k in range(pathLength) for i in range(seqNum) for h in range(pathMaxLength-1) for j in range(flowNum)]


init_x = [X[i][0] == 1 for i in range(flowNum)]
init_y = [Y[i][0] == 1 for i in range(flowNum)]
init_z = [Z[i][0] == 1 for i in range(flowNum)]
final_x = [X[i][pathLength-1] == nodeNum for i in range(flowNum)]
final_y = [Y[i][pathLength-1] == nodeNum for i in range(flowNum)]
final_z = [Z[i][midPathLength-1] == nodeNum for i in range(flowNum)]



path_init = [P[i][0] == 1 for i in range(flowNum)]
pros_init = [PROS[i][0][h] == 0 for i in range(flowNum) for h in range(seqNum)]
blackhole = Or([P[f][pathMaxLength-1] != nodeNum for f in range(flowNum)])
no_process = Or([PROS[i][pathMaxLength-1][seqNum-1] != 1 for i in range(flowNum)])

#loop = Or([And(P[h][i] == P[h][j], P[h][i] == P[h][k], i < j, j < k, P[h][i] != 0, P[h][i] != destNode, And(Or(P[h][i+1] == P[h][j-1], P[h][i+1] == P[h][j+1]), Or(P[h][i+1] == P[h][k-1], P[h][i+1] == P[h][k+1]))) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(1, pathMaxLength-1) for k in range(1, pathMaxLength-1)])

#loop = Or([And(P[h][i] == P[h][j], i < j, P[h][i] != 0, P[h][i] != destNode[h], P[h][i+1] == P[h][j+1]) for h in range(flowNum) for i in range(pathMaxLength-2) for j in range(pathLength-1)])

#loop = Or([And(P[h][i] == P[h][j], P[h][i] == P[h][m], P[h][i+1] == P[h][j+1], P[h][i+1] == P[h][m+1], i < j, j < m, P[h][i] != 0, P[h][i] != destNode[h]) \
#            for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathMaxLength-1) for m in range(pathMaxLength-1) ])

#scc = simplify(And([Implies(PACT[h][i] == 1, And([P[h][i+1] == 1])) for h in range(flowNum) for i in range(pathMaxLength-1)]))

#scc = simplify(And([Implies(And(P[h][i] == Y[h][m], t > i, q > m, t + m == i + q, And([Y[h][m] != X[h][n] for n in range(pathLength)])), \
#              P[h][t] == Y[h][q]) for h in range(flowNum) for i in range(pathMaxLength) for t in range(pathMaxLength) for m in range(pathLength) for q in range(pathLength)]))

#scc = simplify(And([Implies(And(P[h][i] == Y[h][m], Y[h][m] == j + 1, t > i, q > m, t + m == i + q, PACT[h][i] == 1, RuleTMP1[j][h] == newTag), \
#                P[h][t] == Y[h][q]) for h in range(flowNum) for i in range(pathMaxLength) for j in range(nodeNum) for t in range(pathMaxLength) for m in range(pathLength) for q in range(pathLength)]))


#goal = Or(blackhole, Not(scc))
#goal = blackhole
goal = Or(blackhole, no_process)
#goal = Not(scc)
#goal = loop

#loop_twice = simplify(And([Implies(And(P[h][i] == P[h][j], i < j, P[h][i] != 0, P[h][i] != destNode), P[h][i+1] == P[h][j+1]) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathMaxLength-1)]))
#test = Or([ And(RuleTMP1[i][j] < newTag, Y[j][m] == i+1, And([Y[j][m] != X[j][n] for n in range(pathLength)])) for m in range(pathLength) for i in range(nodeNum) for j in range(flowNum)])
#test = Or([ And(RuleTMP1[i][0] < newTag, Y[0][1] == i+1) for i in range(nodeNum)])

s = Solver()

s.add(route_x + route_y + route_z)
s.add(dst_x + dst_y + dst_z + distinct_x + distinct_y + distinct_z1 + distinct_z2 + nfv_order0 + nfv_order1 + nfv_range0 + nfv_range1)
s.add(middlepath_seq1 + middlepath_seq2 + middlepath_seq3)
s.add(init_x + init_y + init_z + final_x + final_y + final_z)
s.add(path_range + drop + rule_actionx1 + rule_actionx2 + rule_dst)
s.add(rule_actionz1 + rule_actionz2 + rule_actionz3 + rule_actionz4 + pros_change1 + pros_change2 + pros_change3 + pros_change4)
s.add(path_init + pros_init)
s.add(pact_range + pact_const)

s.add(bug_fix1 + bug_fix2)

s.add(goal)
#s.add(rule_apply)
#s.add(loop_twice)
#print s

retpath = os.getcwd() + result_path
fp = open(retpath, 'a+')

if s.check() == sat:
    m = s.model()

    for i in range(flowNum):
        fp.write("flow %d\n" %(i+1))
        #if True:
        #if (int(str(m.evaluate(P[i][pathMaxLength-1]))) != destNode) or (i == 0):
        r = [ m.evaluate(X[i][j]) for j in range(pathLength) ]
        fp.write('Old route:\n')
        print >> fp, r

        r = [ m.evaluate(Y[i][j]) for j in range(pathLength) ]
        fp.write('New route:\n')
        print >> fp, r

        r = [ m.evaluate(Z[i][j]) for j in range(midPathLength) ]
        fp.write('Mid route:\n')
        print >> fp, r

        r = [ m.evaluate(NFSeqX[i][j]) for j in range(seqNum) ]
        fp.write('Old nfs:\n')
        print >> fp, r

        r = [ m.evaluate(NFSeqY[i][j]) for j in range(seqNum) ]
        fp.write('New nfs:\n')
        print >> fp, r

        r = [ m.evaluate(P[i][h]) for h in range(pathMaxLength) ]
        fp.write('Trace:\n')
        print >> fp, r


        r = [ m.evaluate(PACT[i][h]) for h in range(pathMaxLength) ]
        fp.write('Packet action:\n')
        print >> fp, r


        for j in range(seqNum):
            #print 'Packet pros %d:' %j
            r = [ m.evaluate(PROS[i][h][j]) for h in range(pathMaxLength) ]
            fp.write('Packet pros %d:' %j)
            print >> fp, r

        fp.write('\n')



else:
    fp.write("haha, failed to solve\n")

fp.close()
