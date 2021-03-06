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

srcNode = [ Int("src_%s" % (i+1)) for i in range(flowNum) ]
dstNode = [ Int("dst_%s" % (i+1)) for i in range(flowNum) ]

PO = [[ Int("po_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]

#P = [[ Int("pa_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]
# packet trace

POVER = [[ Int("pover_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]

RACT = [[[[ Int("rule_%s_%s_%s_%s" % (h+1, k+1, i+1, j+1)) for h in range(verNum+1)] for k in range(nodeNum + 2*flowNum) ] for i in range(nodeNum + 2*flowNum) ] for j in range(flowNum)]

#RVER = [[[ Int("rver_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(nodeNum + 2*flowNum) ] for i in range(nodeNum + 2*flowNum) ] for j in range(flowNum)]
# packet trace action

#RACTM = [[ Int("rulem_%s_%s" % (i+1, j+1)) for i in range(nodeNum + 2*flowNum) ] for j in range(flowNum)]

#RVERM = [[ Int("rverm%s_%s" % (i+1, j+1)) for i in range(nodeNum + 2*flowNum) ] for j in range(flowNum)]

PROS = [[[ Int("pros_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(seqNum)] for i in range(pathMaxLength) ] for j in range(flowNum)]

#Action0 = [[ Int("act0_%s_%s" % (i+1, j+1)) for i in range(flowNum)] for j in range(nodeNum)]
# old rule action

#Action1 = [[ Int("act1_%s_%s_%s" % (i+1, j+1)) for i in range(flowNum)] for j in range(nodeNum)]
# new rule action

#range limit for each variable

route_x  = [ And(0 < X[i][j], X[i][j] <= nodeNum + 2*flowNum) for i in range(flowNum) for j in range(pathLength)]

route_y  = [ And(0 < Y[i][j], Y[i][j] <= nodeNum + 2*flowNum) for i in range(flowNum) for j in range(pathLength)]

route_z  = [ Or([Or(Z[i][j] == X[i][m], Z[i][j] == Y[i][m]) for m in range(pathLength)]) for i in range(flowNum) for j in range(midPathLength)]

src_range  = [ srcNode[i] == nodeNum + i + 1 for i in range(flowNum)]

dst_range  = [ dstNode[i] == nodeNum + flowNum + i + 1 for i in range(flowNum)]

common_ingress = [ And(X[i][1] == Y[i][1], X[i][1] == Z[i][1]) for i in range(flowNum) ]

nfv_range0  = [ And(1 <= NFSeqX[i][j], NFSeqX[i][j] < pathLength-1) for i in range(flowNum) for j in range(seqNum)]

nfv_range1  = [ And(1 <= NFSeqY[i][j], NFSeqY[i][j] < pathLength-1) for i in range(flowNum) for j in range(seqNum)]

nfv_order0 = [ NFSeqX[i][m] < NFSeqX[i][m+1] for i in range(flowNum) for m in range(seqNum-1)]

nfv_order1 = [ NFSeqY[i][m] < NFSeqY[i][m+1] for i in range(flowNum) for m in range(seqNum-1)]

nfv_dst0  = [ Implies(NFSeqX[i][j] == k, X[i][k] != dstNode[i]) for i in range(flowNum) for j in range(seqNum) for k in range(pathLength)]

nfv_dst1  = [ Implies(NFSeqY[i][j] == k, Y[i][k] != dstNode[i]) for i in range(flowNum) for j in range(seqNum) for k in range(pathLength)]


#action_range0 = [ And(0 <= Action0[i][j], Action0[i][j] <= nodeNum) for i in range(nodeNum) for j in range(flowNum)]

#action_range1 = [ And(0 <= Action1[i][j], Action1[i][j] <= nodeNum) for i in range(nodeNum) for j in range(flowNum)]

pact_range = [ And(0 <= POVER[i][j], POVER[i][j] <= verNum) for i in range(flowNum) for j in range(pathMaxLength)]

pros_range = [ And(0 <= PROS[i][j][h], PROS[i][j][h] <= 1) for i in range(flowNum) for j in range(pathMaxLength) for h in range(seqNum)]


#pact_const = [ PACT[i][j] <= PACT[i][j+1] for i in range(flowNum) for j in range(pathMaxLength-1)]

dst_x = [Implies(X[i][j] == dstNode[i], X[i][j+1] == dstNode[i]) for i in range(flowNum) for j in range(pathLength - 1)]

dst_y = [Implies(Y[i][j] == dstNode[i], Y[i][j+1] == dstNode[i]) for i in range(flowNum) for j in range(pathLength - 1)]

dst_z = [Implies(Z[i][j] == dstNode[i], Z[i][j+1] == dstNode[i]) for i in range(flowNum) for j in range(midPathLength - 1)]

distinct_x = [ Implies(X[k][i] == X[k][i+j+1], X[k][i] == dstNode[k]) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

distinct_y = [ Implies(Y[k][i] == Y[k][i+j+1], Y[k][i] == dstNode[k]) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

distinct_z1 = [ Z[k][i] != srcNode[k] for k in range(flowNum) for i in range(1, midPathLength)]

distinct_z2 = [ Implies(Z[k][i] != dstNode[k], Z[k][i] != Z[k][i+1]) for k in range(flowNum) for i in range(midPathLength-1)]


middlepath_seq1 = [ Implies(And(NFSeqY[i][j] == k1, NFSeqY[i][j+1] == k2, Z[i][m] == Y[i][k1]), \
                            Or([ Z[i][n] == Y[i][k2] for n in range(m+1, midPathLength) ])) for i in range(flowNum) for j in range(seqNum-1) for m in range(midPathLength-1) for k1 in range(pathLength) for k2 in range(pathLength)]

middlepath_seq2 = [ Implies(And(NFSeqX[i][j] == k1, NFSeqY[i][j] == k2, Z[i][m] == X[i][k1]), \
                            Or([ Z[i][n] == Y[i][k2] for n in range(m+1, midPathLength) ])) for i in range(flowNum) for j in range(seqNum) for m in range(midPathLength-1) for k1 in range(pathLength) for k2 in range(pathLength)]

middlepath_seq3 = [ Implies(NFSeqX[i][j] == k, Or([ Z[i][n] == X[i][k] for n in range(midPathLength) ])) for i in range(flowNum) for j in range(seqNum) for k in range(pathLength)]


path_range = [ And(0 <= PO[i][j], PO[i][j] <= nodeNum + 2 * flowNum) for i in range(flowNum) for j in range(pathMaxLength)]

path_neq = [ Implies(PO[i][j] == PO[i][j+1], Or(PO[i][j] == dstNode[i], PO[i][j] == 0)) for i in range(flowNum) for j in range(pathMaxLength-1)]

drop = [Implies(PO[h][i] == 0, And([PO[h][i+j+1] == 0 for j in range(pathMaxLength-1-i)])) for h in range(flowNum) for i in range(pathMaxLength-1)]

pver_ascd = [POVER[j][h] <= POVER[j][h+1] for j in range(flowNum) for h in range(pathMaxLength-1)]

rver_init = [Implies(PO[j][0] == m+1, And([RACT[j][m][p][v] == X[j][1] for p in range(nodeNum + 2*flowNum) for v in range(verNum+1)])) \
             for j in range(flowNum) for m in range(nodeNum, nodeNum+2*flowNum)]

rule_dst = [Implies(PO[j][h] == dstNode[j], PO[j][h+1] == dstNode[j]) for h in range(pathMaxLength-1) for j in range(flowNum)]

forward1 = [Implies(And(PO[j][h] == k+1, PO[j][h+1] == n+1, POVER[j][h+1] == v), \
                    PO[j][h+2] == RACT[j][n][k][v]) for v in range(verNum+1) for j in range(flowNum) for k in range(nodeNum+2*flowNum) for n in range(nodeNum + 2*flowNum) for h in range(pathMaxLength-2)]

rule_actionx1 = [Implies(And(X[j][m] == p+1, X[j][m+1] == n+1), RACT[j][n][p][0] == X[j][m+2]) \
                for j in range(flowNum) for n in range(nodeNum+2*flowNum) for p in range(nodeNum+2*flowNum) for m in range(pathLength-2)]

rule_actionx2 = [Implies(And(NFSeqX[i][j] == k, X[i][k] == PO[i][h], POVER[i][h] == 0), \
                         PROS[i][h+1][j] == 1) for i in range(flowNum) for j in range(seqNum) for k in range(pathLength) for h in range(pathMaxLength-1)]


rule_actionz2 = [Implies(And(Z[j][m] == p+1, Z[j][m+1] == n+1), RACT[j][n][p][verNum] == Z[j][m+2])\
                         for j in range(flowNum) for p in range(nodeNum+2*flowNum) for n in range(nodeNum+2*flowNum) for m in range(midPathLength-2)]


rule_actionz3 = [Implies(And(NFSeqY[i][j] == k, PO[i][h] == Y[i][k], POVER[i][h] == 1, PROS[i][h][j-1] == 1), \
                         PROS[i][h+1][j] == 1) for i in range(flowNum) for j in range(1, seqNum) for k in range(pathLength) for h in range(pathMaxLength-1)]

rule_actionz4 = [Implies(And(NFSeqY[i][j] == k, PO[i][h] == Y[i][k], POVER[i][h] == 1, PROS[i][h][j-1] == 0), \
                         PROS[i][h+1][j] == 0) for i in range(flowNum) for j in range(1, seqNum) for k in range(pathLength) for h in range(pathMaxLength-1)]


rule_actionz5 = [Implies(And(NFSeqY[i][0] == k, PO[i][h] == Y[i][k], POVER[i][h] == 1), \
                         PROS[i][h+1][0] == 1) for i in range(flowNum) for k in range(pathLength) for h in range(pathMaxLength-1)]



#rule_actionx1 = [Implies(And(X[j][m] == PO[j][h], PACT[j][h] == 0), And(PO[j][h+1] == X[j][m+1], P[j][h+1] == X[j][m+1])) for h in range(pathMaxLength-1) for j in range(flowNum) for m in range(pathLength-1)]


#path_new = [ Implies(And(PACT[i][j] == 1, Or([P[i][j] == Z[i][p] for p in range(midPathLength)])), \
#                     Or([And(P[i][j] == Z[i][c], P[i][j+1] == Z[i][c+1]) for c in range(midPathLength-1)])) for i in range(flowNum) for j in range(pathMaxLength-1)]


#bug_fix1 = [Implies(And(P[j][h] != Z[j][m], P[j][h+1] == Z[j][m+1], PACT[j][h+1] == 1, And([Z[j][a] != Z[j][m+1] for a in range(m)])), \
#                         P[j][h+2] == Z[j][m+2]) for j in range(flowNum) for h in range(pathMaxLength-2) for m in range(midPathLength-2)]

#bug_fix2 = [Implies(And([P[j][h] != Z[j][m] for m in range(midPathLength)]), PACT[j][h] == 0) for h in range(pathMaxLength) for j in range(flowNum)]

#bug_fix1 = [Implies(Not(Or([And(P[j][h] == Z[j][m], P[j][h+1] == Z[j][m+1]) for m in range(midPathLength-1)])), \
#                    PACT[j][h+1] == 0) for j in range(flowNum) for h in range(pathMaxLength-1)]

# bug_fix2 = [Implies(And(NFSeqX[i][j] == k1, NFSeqY[i][j] == k2, P[i][h] == Z[i][m], \
#                         P[i][h] == X[i][n], k1 > n, And([Z[i][c] != Y[i][k2] for c in range(m, midPathLength)]), PACT[i][h] == 1), \
#                         P[i][h+1] == X[i][n+1]) for i in range(flowNum) for j in range(seqNum) for k1 in range(pathLength) for k2 in range(pathLength) for h in range(pathMaxLength-1) for m in range(midPathLength) for n in range(pathLength-1)]

#bug_fix3 = [Implies(And(Not(Or([And(P[j][h] == Z[j][m], P[j][h+1] == Z[j][m+1]) for m in range(midPathLength-1)])), \
#                    P[j][h+1] == Z[j][n], And([Z[j][k] != Z[j][n] for k in range(n)]), PACT[j][h+1] == 1), \
#                    P[j][h+2] == Z[j][n+1]) for j in range(flowNum) for h in range(pathMaxLength-2) for n in range(midPathLength-1)]

# bug_fix2 = [Implies(And(PO[j][k] == Z[j][m], POVER[j][k] == 1), \
#                     Or([PO[j][k+1] == Z[j][p] for p in range(midPathLength)]))
#                     for j in range(flowNum) for k in range(pathMaxLength-1) for m in range(midPathLength)]


bug_fix2 = [Implies(And(PO[j][k] == Z[j][m], POVER[j][k] == 1, PO[j][k] != dstNode[j]), \
                    Or([And(PO[j][k] == Z[j][p], PO[j][k+1] == Z[j][p+1]) for p in range(midPathLength-1)]))
                    for j in range(flowNum) for k in range(pathMaxLength-1) for m in range(midPathLength)]


bug_fix3 = [Implies(And(PO[j][k] == X[j][m], NFSeqY[j][i] == p, POVER[j][k] == 1, PROS[j][k][i] == 0),
                   Or([PO[j][c] == Y[j][p] for c in range(k, pathMaxLength)]))
                   for j in range(flowNum) for k in range(pathMaxLength-1) for i in range(seqNum) for m in range(pathLength) for p in range(pathLength)]


# bug_fix3 = [Implies(And(PO[j][k] == X[j][m], NFSeqY[j][i] == p, POVER[j][k] == 1, PROS[j][k][i] == 0, k < n, \
#                    And([And([PO[j][h] != Z[j][q] for q in range(midPathLength)]) for h in range(k+1, n)]), \
#                    Or([PO[j][n] == Z[j][b] for b in range(midPathLength)])),
#                    #Or(k+1 == n, And([And([P[j][h] != Z[j][q] for q in range(midPathLength)]) for h in range(k+1, n)]))), \
#                    Or([PO[j][c] == Y[j][p] for c in range(n, pathMaxLength)]))
#                    for j in range(flowNum) for k in range(pathMaxLength-1) for n in range(pathMaxLength) for i in range(seqNum) for m in range(pathLength) for p in range(pathLength)]


#bug_fix4 = [Implies(And(And([P[j][h] != Z[j][m] for m in range(midPathLength)]), \
#                    P[j][h] == X[j][n], PACT[j][h] == 1), \
#                    P[j][h+1] == 0) for j in range(flowNum) for h in range(pathMaxLength-1) for n in range(pathLength)]

#bug_fix5 = [Or(Or([And(P[j][h] == X[j][n], P[j][h+1] == X[j][n+1]) for n in range(pathLength-1)]), \
#               Or([And(P[j][h] == Z[j][m], P[j][h+1] == Z[j][m+1]) for m in range(midPathLength-1)]), \
#               Or([And(P[j][h] == X[j][p+1], P[j][h+1] == X[j][p]) for p in range(pathLength-1)]), \
#               Or([And(P[j][h] == Z[j][q+1], P[j][h+1] == Z[j][q]) for q in range(midPathLength-1)])) for j in range(flowNum) for h in range(pathMaxLength-1) ]


pros_change1 = [Implies(And(PO[j][h] != Y[j][k], NFSeqY[j][i] == k, POVER[j][h] == 1), \
                        PROS[j][h][i] == PROS[j][h+1][i]) for k in range(pathLength) for i in range(seqNum) for h in range(pathMaxLength-1) for j in range(flowNum)]

#pros_change2 = [Implies(And(P[j][h] == Y[j][k], NFSeqY[j][i] == k, PACT[j][h] == 1, PROS[j][h][i] == 1), PROS[j][h+1][i] == 1) for k in range(pathLength) for i in range(seqNum) for h in range(pathMaxLength-1) for j in range(flowNum)]

pros_change2 = [Implies(And(PO[j][h] != X[j][k], NFSeqX[j][i] == k, POVER[j][h] == 0), \
                        PROS[j][h][i] == PROS[j][h+1][i]) for k in range(pathLength) for i in range(seqNum) for h in range(pathMaxLength-1) for j in range(flowNum)]

#pros_change4 = [Implies(And(P[j][h] == X[j][k], NFSeqX[j][i] == k, PACT[j][h] == 0, PROS[j][h][i] == 1), PROS[j][h+1][i] == 1) for k in range(pathLength) for i in range(seqNum) for h in range(pathMaxLength-1) for j in range(flowNum)]

no_blackhole = And([PO[i][pathMaxLength-1] == dstNode[i] for i in range(flowNum)])

init_x = [X[i][0] == srcNode[i] for i in range(flowNum)]
init_y = [Y[i][0] == srcNode[i] for i in range(flowNum)]
init_z = [Z[i][0] == srcNode[i] for i in range(flowNum)]
final_x = [X[i][pathLength-1] == dstNode[i] for i in range(flowNum)]
final_y = [Y[i][pathLength-1] == dstNode[i] for i in range(flowNum)]
final_z = [Z[i][midPathLength-1] == dstNode[i] for i in range(flowNum)]



#path_init = [P[i][0] == srcNode[i] for i in range(flowNum)]
path_org_init = [PO[i][0] == srcNode[i] for i in range(flowNum)]
path_org_sec = [PO[i][1] == X[i][1] for i in range(flowNum)]
pros_init = [PROS[i][0][h] == 0 for i in range(flowNum) for h in range(seqNum)]
#blackhole = Or([P[i][pathMaxLength-1] != dstNode[i] for i in range(flowNum)])
no_process = Or([PROS[i][pathMaxLength-1][j] != 1 for i in range(flowNum) for j in range(seqNum)])
#waypoint = And([ Implies(P[i][pathMaxLength-1] == dstNode[i], \
#                         And([PROS[i][pathMaxLength-1][j] == 1 for j in range(seqNum)])) for i in range(flowNum)])

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
goal = no_process
#goal = Or(blackhole, no_process)
#goal = Not(waypoint)
#goal = Not(scc)
#goal = loop

#loop_twice = simplify(And([Implies(And(P[h][i] == P[h][j], i < j, P[h][i] != 0, P[h][i] != destNode), P[h][i+1] == P[h][j+1]) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathMaxLength-1)]))
#test = Or([ And(RuleTMP1[i][j] < newTag, Y[j][m] == i+1, And([Y[j][m] != X[j][n] for n in range(pathLength)])) for m in range(pathLength) for i in range(nodeNum) for j in range(flowNum)])
#test = Or([ And(RuleTMP1[i][0] < newTag, Y[0][1] == i+1) for i in range(nodeNum)])

s = Solver()

s.add(route_x + route_y + route_z + src_range + dst_range)
s.add(pact_range + pros_range + nfv_order0 + nfv_order1 + nfv_range0 + nfv_range1 + nfv_dst0 + nfv_dst1)
s.add(common_ingress + dst_x + dst_y + dst_z + distinct_x + distinct_y + distinct_z1 + distinct_z2)
s.add(middlepath_seq1 + middlepath_seq2 + middlepath_seq3)

s.add(pver_ascd + path_range + drop + rule_actionx1 + rule_actionx2 + rule_dst)
s.add(forward1 + rver_init + rule_actionz2 + rule_actionz3 + rule_actionz4 + rule_actionz5 + pros_change1 + pros_change2)
s.add(init_x + init_y + init_z + final_x + final_y + final_z)
s.add(path_org_init + path_org_sec + pros_init + path_neq)

s.add(no_blackhole)

s.add( bug_fix2 + bug_fix3 )

s.add(goal)
#s.add(rule_apply)
#s.add(loop_twice)
#print s

#retpath = os.getcwd() + result_path
#fp = open(retpath, 'a+')

if s.check() == sat:
    m = s.model()

    for i in range(flowNum):
        #if True:
        #if (int(str(m.evaluate(P[i][pathMaxLength-1]))) != destNode) or (i == 0):
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

        r = [ m.evaluate(PO[i][h]) for h in range(pathMaxLength) ]
        print 'Org Path:'
        print_matrix(r)


        r = [ m.evaluate(POVER[i][h]) for h in range(pathMaxLength) ]
        print 'Org packet action:'
        print_matrix(r)


        for j in range(seqNum):
            print 'Packet pros %d:' %j
            r = [ m.evaluate(PROS[i][h][j]) for h in range(pathMaxLength) ]
            print_matrix(r)





else:
    print "haha, failed to solve"
