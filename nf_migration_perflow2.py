from z3 import *
import os

result_path = '/result/result_2.txt'

# variable definition
ruleNum = 1
flowNum = 1
nodeNum = 10
pathLength = 6
pathMaxLength = pathLength*5
newTag = 2

X = [[ Int("x_%s_%s" % (i+1, j+1)) for i in range(pathLength) ] for j in range(flowNum)]
# old path variable

Y = [[ Int("y_%s_%s" % (i+1, j+1)) for i in range(pathLength) ] for j in range(flowNum)]
# new path variable

#XNF = [[ Int("x_%s_%s" % (i+1, j+1)) for i in range(pathLength+2) ] for j in range(flowNum)]
#YNF = [[ Int("y_%s_%s" % (i+1, j+1)) for i in range(pathLength+2) ] for j in range(flowNum)]

#srcNode = [ Int("src_%s" % (i+1)) for i in range(flowNum) ]
#destNode = [ Int("dst_%s" % (i+1)) for i in range(flowNum) ]

srcNFV = [ Int("srcnf_%s" % (i+1)) for i in range(flowNum) ]
destNFV = [ Int("dstnf_%s" % (i+1)) for i in range(flowNum) ]

FlowTable0 = [[[ Int("ft0_%s_%s_%s" %(i+1, j+1, k+1)) for i in range(ruleNum)] for j in range(flowNum)] for k in range(nodeNum)]
# old flow-rule relations (rule, flow, switch, priority)

FlowTable1 = [[[ Int("ft1_%s_%s_%s" %(i+1, j+1, k+1)) for i in range(ruleNum+flowNum)] for j in range(flowNum)] for k in range(nodeNum)]
# new flow-rule relations including send-back rule

SwitchTable0 = [[ Int("sw0_%s_%s" %(i+1, j+1)) for i in range(ruleNum)] for j in range(nodeNum)]
# old switch-rule relation (rule, switch)

SwitchTable1 = [[ Int("sw1_%s_%s" %(i+1, j+1)) for i in range(ruleNum+flowNum)] for j in range(nodeNum)]
# new switch-rule relation

ProcessTable0 = [[ Int("process0_%s_%s" %(i+1, j+1)) for i in range(ruleNum)] for j in range(nodeNum)]
ProcessTable1 = [[ Int("process1_%s_%s" %(i+1, j+1)) for i in range(ruleNum+flowNum)] for j in range(nodeNum)]

P = [[ Int("pa_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]
# packet trace

RuleTMP0 = [[[ Int("rtsx0_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(2)] for i in range(flowNum) ] for j in range(nodeNum)]
# old rule tmp of matching rule

RuleTMP1 = [[[ Int("rtsx1_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(2)] for i in range(flowNum) ] for j in range(nodeNum)]
# new rule tmp of matching rule

TagTMP0 = [[[ Int("ttsx0_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(2)] for i in range(flowNum) ] for j in range(nodeNum)]
# old tagging tmp of matching rule

TagTMP1 = [[[ Int("ttsx1_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(2)] for i in range(flowNum) ] for j in range(nodeNum)]
# old tagging tmp of matching rule

PACT = [[ Int("pact_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]
# packet trace action

PTMP = [[ Int("pts_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]
# packet trace timestamp

PROS = [[ Int("pros_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]

Action0 = [[[ Int("act0_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(2)] for i in range(flowNum)] for j in range(nodeNum)]
# old rule action

Action1 = [[[ Int("act1_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(2)] for i in range(flowNum)] for j in range(nodeNum)]
# new rule action

HighRule0 = [[[ Int("hr0_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(2)] for i in range(flowNum)] for j in range(nodeNum)]
# old matching rule

HighRule1 = [[[ Int("hr1_%s_%s_%s" % (k+1, i+1, j+1)) for k in range(2)] for i in range(flowNum)] for j in range(nodeNum)]
# new matching rule

#range limit for each variable

route_x  = [ And(0 < X[i][j], X[i][j] <= nodeNum) for i in range(flowNum) for j in range(pathLength)]

route_y  = [ And(0 < Y[i][j], Y[i][j] <= nodeNum) for i in range(flowNum) for j in range(pathLength)]

#src_range  = [ And(0 < srcNode[i], srcNode[i] <= nodeNum) for i in range(flowNum) ]

#dst_range  = [ And(0 < destNode[i], destNode[i] <= nodeNum) for i in range(flowNum) ]

srcnf_range  = [ And(0 <= srcNFV[i], srcNFV[i] < pathLength) for i in range(flowNum) ]

dstnf_range  = [ And(0 <= destNFV[i], destNFV[i] < pathLength) for i in range(flowNum) ]

#srcnf_not = [ Implies(srcNFV[i] == m, X[i][m] != nodeNum) for m in range(pathLength) for i in range(flowNum)]
#dstnf_not = [ Implies(destNFV[i] == m, Y[i][m] != nodeNum) for m in range(pathLength) for i in range(flowNum)]
#path_range = [ And(0 <= P[i][j], P[i][j] <= nodeNum) for i in range(flowNum) for j in range(pathMaxLength)]

#optional
flowTable_range0 = [ And(0 <= FlowTable0[i][j][k], FlowTable0[i][j][k] <= ruleNum) for i in range(nodeNum) for j in range(flowNum) for k in range(ruleNum)]
flowTable_range1 = [ And(0 <= FlowTable1[i][j][k], FlowTable1[i][j][k] <= ruleNum) for i in range(nodeNum) for j in range(flowNum) for k in range(ruleNum)]


sendback_range0 = [ Implies(And(ruleNum <= k, k < ruleNum+flowNum, j != k - ruleNum), FlowTable1[i][j][k] == 0) for i in range(nodeNum) for j in range(flowNum) for k in range(flowNum+ruleNum) ]

sendback_range1 = [ Implies(And(ruleNum <= k, k < ruleNum+flowNum, j == k - ruleNum), FlowTable1[i][j][k] == ruleNum) for i in range(nodeNum) for j in range(flowNum) for k in range(flowNum+ruleNum) ]

switchTable_range0 = [ Or(SwitchTable0[i][j] == 0, SwitchTable0[i][j] == 1) for i in range(nodeNum) for j in range(ruleNum)]

switchTable_range1 = [ Or(SwitchTable1[i][j] == 0, SwitchTable1[i][j] == 1) for i in range(nodeNum) for j in range(flowNum+ruleNum)]

processTable_range0 = [ Or(ProcessTable0[i][j] == 0, ProcessTable0[i][j] == 1, ProcessTable0[i][j] == 2) for i in range(nodeNum) for j in range(ruleNum)]

processTable_range1 = [ Or(ProcessTable1[i][j] == 0, ProcessTable1[i][j] == 1, ProcessTable1[i][j] == 2) for i in range(nodeNum) for j in range(flowNum+ruleNum)]

#optional
action_range0 = [ And(0 <= Action0[i][j][k], Action0[i][j][k] <= nodeNum+2*flowNum) for k in range(2) for i in range(nodeNum) for j in range(flowNum)]

action_range1 = [ And(0 <= Action1[i][j][k], Action1[i][j][k] <= nodeNum+2*flowNum) for k in range(2) for i in range(nodeNum) for j in range(flowNum)]


highrule_range0 = [ And(0 <= HighRule0[i][j][k], HighRule0[i][j][k] <= ruleNum) for k in range(2) for i in range(nodeNum) for j in range(flowNum)]

highrule_range1 = [ And(0 <= HighRule1[i][j][k], HighRule1[i][j][k] <= flowNum + ruleNum) for k in range(2) for i in range(nodeNum) for j in range(flowNum)]

#timestamp may not be consistent

highrule_same0 = [ Implies(And(srcNFV[j] == m, X[j][m] != i+1), Action0[i][j][0] == Action0[i][j][1]) for m in range(pathLength) for i in range(nodeNum) for j in range(flowNum)]

highrule_same1 = [ Implies(And(destNFV[j] == m, Y[j][m] != i+1, HighRule1[i][j][0] == k1, HighRule1[i][j][1] == k2), Action1[i][j][0] == Action1[i][j][1]) for m in range(pathLength) for k1 in range(ruleNum+1) for k2 in range(ruleNum+1) for i in range(nodeNum) for j in range(flowNum)]


rule_overlap0 = simplify(And([Implies(And(SwitchTable0[i][j1] == 1, SwitchTable0[i][j2] == 1, j1 != j2, FlowTable0[i][f][j1] > 0, FlowTable0[i][f][j2] > 0, ProcessTable0[i][j1] + ProcessTable0[i][j2] != 1), FlowTable0[i][f][j1] != FlowTable0[i][f][j2]) for i in range(nodeNum) for f in range(flowNum) for j1 in range(ruleNum) for j2 in range(ruleNum)]))

rule_overlap1 = simplify(And([Implies(And(SwitchTable1[i][j1] == 1, SwitchTable1[i][j2] == 1, j1 != j2, FlowTable1[i][f][j1] > 0, FlowTable1[i][f][j2] > 0, ProcessTable1[i][j1] + ProcessTable1[i][j2] != 1), FlowTable1[i][f][j1] != FlowTable1[i][f][j2]) for i in range(nodeNum) for f in range(flowNum) for j1 in range(flowNum + ruleNum) for j2 in range(flowNum + ruleNum)]))


highrule_select0 = [Implies(HighRule0[i][j][fg] == k1+1, And(SwitchTable0[i][k1] == 1, FlowTable0[i][j][k1] > 0, ProcessTable0[i][k1] + fg != 1, And([Implies(SwitchTable0[i][k2] == 1, Or(ProcessTable0[i][k2] + fg == 1, FlowTable0[i][j][k1] >= FlowTable0[i][j][k2])) for k2 in range(ruleNum)]))) for fg in range(2) for i in range(nodeNum) for j in range(flowNum) for k1 in range(ruleNum) ]

highrule_select1 = [Implies(HighRule1[i][j][fg] == k1+1, And(SwitchTable1[i][k1] == 1, FlowTable1[i][j][k1] > 0, ProcessTable1[i][k1] + fg != 1, And([Implies(SwitchTable1[i][k2] == 1, Or(ProcessTable1[i][k2] + fg == 1, FlowTable1[i][j][k1] >= FlowTable1[i][j][k2])) for k2 in range(flowNum+ruleNum)]))) for fg in range(2) for i in range(nodeNum) for j in range(flowNum) for k1 in range(flowNum+ruleNum) ]


same_action0 = [Implies(HighRule0[i][j1][fg] == HighRule0[i][j2][fg], And(TagTMP0[i][j1][fg] == TagTMP0[i][j2][fg], RuleTMP0[i][j1][fg] == RuleTMP0[i][j2][fg], Action0[i][j1][fg] == Action0[i][j2][fg])) for fg in range(2) for i in range(nodeNum) for j1 in range(flowNum) for j2 in range(flowNum)]

same_action1 = [Implies(HighRule1[i][j1][fg] == HighRule1[i][j2][fg], And(TagTMP1[i][j1][fg] == TagTMP1[i][j2][fg], RuleTMP1[i][j1][fg] == RuleTMP1[i][j2][fg], Action1[i][j1][fg] == Action1[i][j2][fg])) for fg in range(2) for i in range(nodeNum) for j1 in range(flowNum) for j2 in range(flowNum)]

rule_actionx1 = [Implies(And(X[j][m] == i+1, m < srcNFV[j]), Action0[i][j][0] == X[j][m+1]) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]
rule_actionx2 = [Implies(And(X[j][m] == i+1, m == srcNFV[j]), And(Action0[i][j][0] == nodeNum+2*j+1, Action0[i][j][1] == X[j][m+1])) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]
rule_actionx3 = [Implies(And(X[j][m] == i+1, m > srcNFV[j]), Action0[i][j][1] == X[j][m+1]) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]
rule_actionx4 = [Implies(srcNFV[j] == pathLength-1, And(Action0[nodeNum-1][j][0] == nodeNum+2*j+1, Action0[nodeNum-1][j][1] == nodeNum)) for j in range(flowNum) ]

rule_actiony1 = [Implies(And(Y[j][m] == i+1, m < destNFV[j]), And(Action1[i][j][0] == Y[j][m+1], HighRule1[i][j][0] <= ruleNum)) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]
rule_actiony2 = [Implies(And(Y[j][m] == i+1, m == destNFV[j]), And(Action1[i][j][0] == nodeNum+2*j+2, HighRule1[i][j][0] <= ruleNum, Action1[i][j][1] == Y[j][m+1], HighRule1[i][j][1] <= ruleNum)) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]
rule_actiony3 = [Implies(And(Y[j][m] == i+1, m > destNFV[j]), And(Action1[i][j][1] == Y[j][m+1], HighRule1[i][j][1] <= ruleNum)) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]
rule_actiony4 = [Implies(destNFV[j] == pathLength-1, And(Action1[nodeNum-1][j][0] == nodeNum+2*j+2, HighRule1[nodeNum-1][j][0] <= ruleNum, Action1[nodeNum-1][j][1] == nodeNum, HighRule1[nodeNum-1][j][1] <= ruleNum)) for j in range(flowNum) ]

drop_action0 = [Implies(HighRule0[i][j][k] == 0, Action0[i][j][k] == 0) for k in range(2) for i in range(nodeNum) for j in range(flowNum) ]

drop_action1 = [Implies(HighRule1[i][j][k] == 0, Action1[i][j][k] == 0) for k in range(2) for i in range(nodeNum) for j in range(flowNum) ]

rts_range0 = [ And(0 < RuleTMP0[i][j][fg], RuleTMP0[i][j][fg] <= newTag - 1) for fg in range(2) for i in range(nodeNum) for j in range(flowNum)]

rts_range1 = [ Or(RuleTMP1[i][j][fg] == RuleTMP0[i][j][fg], RuleTMP1[i][j][fg] == newTag) for fg in range(2) for i in range(nodeNum) for j in range(flowNum)]

tts_range0 = [ And(0 < TagTMP0[i][j][fg], TagTMP0[i][j][fg] <= newTag - 1)  for fg in range(2) for i in range(nodeNum) for j in range(flowNum)]

tts_range1 = [ Implies(And(X[j][m] == i1 + 1, X[j][m+1] == i2 + 1, m < srcNFV[j]), TagTMP0[i1][j][0] <= RuleTMP0[i2][j][0]) for i1 in range(nodeNum) for i2 in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1) ]
tts_range2 = [ Implies(And(X[j][m] == i1 + 1, X[j][m+1] == i2 + 1, m >= srcNFV[j]), TagTMP0[i1][j][1] <= RuleTMP0[i2][j][1]) for i1 in range(nodeNum) for i2 in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1) ]


pts_range = [ And(0 < PTMP[i][j], PTMP[i][j] <= newTag) for i in range(flowNum) for j in range(pathMaxLength)]

pact_range = [ Or(PACT[i][j] == 0, PACT[i][j] == 1) for i in range(flowNum) for j in range(pathMaxLength)]
# 0 indicates old configuration, 1 indicates new configuration, 2 indicates drop action


dst_x = [Implies(X[i][j] == nodeNum, X[i][j+1] == nodeNum) for i in range(flowNum) for j in range(pathLength - 1)]

dst_y = [Implies(Y[i][j] == nodeNum, Y[i][j+1] == nodeNum) for i in range(flowNum) for j in range(pathLength - 1)]

distinct_x = [ Implies(X[k][i] == X[k][i+j+1], X[k][i] == nodeNum) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

distinct_y = [ Implies(Y[k][i] == Y[k][i+j+1], Y[k][i] == nodeNum) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

rule_dst = [ And(Action0[nodeNum-1][i][1] == nodeNum, Action1[nodeNum-1][i][1] == nodeNum) for i in range(flowNum) ]

#rule_dst = [ And(Action0[destNode[i]-1][i] == destNode[i], Action1[destNode[i]-1][i] == destNode[i]) for i in range(flowNum)]

#optional
#no_self_loop = [ Implies(j+1 != destNode[i], And(Action0[j][i] != j+1, Action1[j][i] != j+1)) for j in range(nodeNum) for i in range(flowNum) ]

# 0 indicates old configuration, 1 indicates new configuration
#path_x0 = simplify(And([Implies(And(P[h][i] == X[h][j], X[h][j] == m+1, PROS[h][i] == fg, PTMP[h][i] <= RuleTMP0[m][h][fg], PTMP[h][i] <= RuleTMP1[m][h][fg]), Or(And(P[h][i+1] == Action0[m][h][fg], PTMP[h][i+1] == TagTMP0[m][h][fg], PROS[h][i+1] == PROS[h][i]), And(P[h][i+1] == Action1[m][h][fg], PTMP[h][i+1] == TagTMP1[m][h][fg], PROS[h][i+1] == PROS[h][i]))) for fg in range(2) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathLength)]))

#path_x1 = simplify(And([Implies(And(P[h][i] == X[h][j], X[h][j] == m+1, PROS[h][i] == fg, PTMP[h][i] <= RuleTMP1[m][h][fg], PTMP[h][i] > RuleTMP0[m][h][fg]), And(P[h][i+1] == Action1[m][h][fg], PTMP[h][i+1] == TagTMP1[m][h][fg], PROS[h][i+1] == PROS[h][i])) for fg in range(2) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathLength)]))

path_0 = simplify(And([Implies(And(P[h][i] == X[h][j], X[h][j] == m+1, PROS[h][i] == fg, PTMP[h][i] <= RuleTMP0[m][h][fg], PTMP[h][i] <= RuleTMP1[m][h][fg]), Or(PACT[h][i] == 0, PACT[h][i] == 1)) for fg in range(2) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength) for j in range(pathLength)]))

path_1 = simplify(And([Implies(And(P[h][i] == Y[h][j], Y[h][j] == m+1, PROS[h][i] == fg, PTMP[h][i] <= RuleTMP0[m][h][fg], PTMP[h][i] <= RuleTMP1[m][h][fg]), Or(PACT[h][i] == 0, PACT[h][i] == 1)) for fg in range(2) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength) for j in range(pathLength)]))

#path_0 = simplify(And([Implies(And(Or(And(P[h][i] == X[h][j], X[h][j] == m+1), And(P[h][i] == Y[h][j], Y[h][j] == m+1)), PROS[h][i] == fg, PTMP[h][i] <= RuleTMP0[m][h][fg], PTMP[h][i] <= RuleTMP1[m][h][fg]), Or(And(PACT[h][i+1] == 0, P[h][i+1] == Action0[m][h][fg], PTMP[h][i+1] == TagTMP0[m][h][fg], PROS[h][i+1] == PROS[h][i]), And(PACT[h][i+1] == 1, P[h][i+1] == Action1[m][h][fg], PTMP[h][i+1] == TagTMP1[m][h][fg], PROS[h][i+1] == PROS[h][i]))) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathLength)]))

path_2 = simplify(And([Implies(And(P[h][i] == X[h][j], X[h][j] == m+1, PROS[h][i] == fg, PTMP[h][i] <= RuleTMP1[m][h][fg], PTMP[h][i] > RuleTMP0[m][h][fg]), PACT[h][i] == 1) for fg in range(2) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength) for j in range(pathLength)]))

path_3 = simplify(And([Implies(And(P[h][i] == Y[h][j], Y[h][j] == m+1, PROS[h][i] == fg, PTMP[h][i] <= RuleTMP1[m][h][fg], PTMP[h][i] > RuleTMP0[m][h][fg]), PACT[h][i] == 1) for fg in range(2) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength) for j in range(pathLength)]))

path_4 = [Implies(And(P[h][i] == nodeNum+2*h+1, PROS[h][i] == 0, srcNFV[h] == m, X[h][m] == n+1), And(P[h][i+1] == X[h][m], Or(And(PTMP[h][i+1] == RuleTMP0[n][h][1], PROS[h][i+1] == 1, PACT[h][i+1] == 0), And(PTMP[h][i+1] == newTag, PROS[h][i+1] == 0, PACT[h][i+1] == 1)))) for m in range(pathLength) for n in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength-1) ]

path_5 = [Implies(And(P[h][i] == nodeNum+2*h+2, PROS[h][i] == 0, destNFV[h] == m, Y[h][m] == n+1), And(P[h][i+1] == Y[h][m], PROS[h][i+1] == 1, PTMP[h][i+1] == RuleTMP1[n][h][1], PACT[h][i+1] == 1)) for m in range(pathLength) for n in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength-1) ]

forward1 = simplify(And([Implies(And(P[h][i] <= nodeNum, P[h][i] == m+1, PACT[h][i] == 0, PROS[h][i] == fg), And(P[h][i+1] == Action0[m][h][fg], PTMP[h][i+1] == TagTMP0[m][h][fg], PROS[h][i+1] == fg)) for fg in range(2) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-1)]))

forward2 = simplify(And([Implies(And(P[h][i] <= nodeNum, P[h][i] == m+1, PACT[h][i] == 1, PROS[h][i] == fg), And(P[h][i+1] == Action1[m][h][fg], PTMP[h][i+1] == TagTMP1[m][h][fg], PROS[h][i+1] == fg)) for fg in range(2) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-1)]))

path_action = [Implies(And(P[h][i] == P[h][i+j], PACT[h][i] == 1), PACT[h][i+j] == 1) for h in range(flowNum) for i in range(pathMaxLength) for j in range(pathMaxLength-i)]

#forward3 = simplify(And([Implies(And(P[h][i+1] == m+1, PACT[h][i+1] == 1, Action1[m][h] == -1, And([Y[h][j] != P[h][i+1] for j in range(pathLength)]), Or([X[h][k] == P[h][i] for k in range(pathLength)])), And(P[h][i+2] == P[h][i], PTMP[h][i+2] == TagTMP1[m][h])) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-2)]))

#forward4 = simplify(And([Implies(And(P[h][i+1] == m+1, X[h][k+1] == m+1, Or([X[h][j] == P[h][i] for j in range(pathLength)]), PACT[h][i+1] == 1, Action1[m][h] == -1), And(P[h][i+2] == X[h][k], PTMP[h][i+2] == TagTMP1[m][h])) for k in range(pathLength-1) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-2)]))

#forward5 = simplify(And([Implies(And(P[h][i+1] == m+1, X[h][k+1] == m+1, PACT[h][i+1] == 1, Action1[m][h] == -1), And(P[h][i+2] == X[h][k], PTMP[h][i+2] == TagTMP1[m][h])) for k in range(pathLength-1) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-2)]))


#sendback2 = simplify(And([Implies(Action1[n][i] == -1, SwitchTable1[n][i+ruleNum] == 1) for n in range(nodeNum) for i in range(flowNum)]))

#no_sendback1 = simplify(And([Implies(And(SwitchTable1[n][i+ruleNum] == 1, X[i][j] == n+1), And([X[i][j] != Y[i][k] for k in range(pathLength)])) for i in range(flowNum) for j in range(pathLength) for n in range(nodeNum)]))

# The packets with the same matching rule should have the same RTMP and TTMP

#no_sendback2 = simplify(And([Implies(And([X[i][j] != n+1 for j in range(pathLength)]), SwitchTable1[n][i+ruleNum] == 0) for i in range(flowNum) for n in range(nodeNum)]))


#rule_actiony2 = [Implies(And(Y[j][m] == i+1, m == destNFV[j]), And(Action1[i][j][0] == nodeNum+2*j+2, HighRule1[i][j][0] > 0, Action1[i][j][1] == Y[j][m+1], HighRule1[i][j][1] > 0)) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]

#determine tagTMP

#tts_range = [ Or(TagTMP1[i][j] == TagTMP0[i][j], TagTMP1[i][j] == newTag) for i in range(nodeNum) for j in range(flowNum)]
# need revision

#tmp0 = simplify(And([Implies(And(Action1[k][i] == m+1, RuleTMP1[m][i] < newTag), TagTMP1[k][i] <= RuleTMP1[m][i]) for k in range(nodeNum) for i in range(flowNum) for m in range(nodeNum)]))

tmp0 = simplify(And([Implies(Action1[k][i][fg] == m+1, TagTMP1[k][i][fg] <= RuleTMP1[m][i][fg]) for fg in range(2) for k in range(nodeNum) for i in range(flowNum) for m in range(nodeNum)]))

tmp1 = simplify(And([Implies(And(Action1[k][i][fg] == m+1, RuleTMP1[m][i][fg] == newTag, RuleTMP1[k][i][fg] == newTag), TagTMP1[k][i][fg] == newTag) for fg in range(2) for k in range(nodeNum) for i in range(flowNum) for m in range(nodeNum)]))

tmp2 = simplify(And([Implies(RuleTMP0[m][i][fg] == RuleTMP1[m][i][fg], TagTMP0[m][i][fg] == TagTMP1[m][i][fg]) for fg in range(2) for i in range(flowNum) for m in range(nodeNum)]))

tmp_change = [Implies(Or(Action0[k][i][fg] != Action1[k][i][fg], TagTMP0[k][i][fg] != TagTMP1[k][i][fg]), RuleTMP1[k][i][fg] == newTag) for fg in range(2) for k in range(nodeNum) for i in range(flowNum)]



# modification 1
#rule_apply = simplify(And([Implies(And(P[h][i] == P[h][j], P[h][i] == m + 1, P[h][i] != 0, i < j), PACT[h][i] <= PACT[h][j]) for h in range(flowNum) for i in range(pathMaxLength) for j in range(pathMaxLength) for m in range(nodeNum)]))
# drop bug

#bug_fix1 = simplify(And([Implies(And(Y[i][m1] == h1 + 1, Y[i][m2] == h2 + 1, Y[i][m1] == X[i][n1], m1 < m2, Action0[h1][i] != Action1[h1][i], And([And(Action0[h2][i] != X[i][n2], Action0[h2][i] != Y[i][m3]) for n2 in range(pathLength) for m3 in range(pathLength)]), And([Implies(And(m4 > m1, m4 < m2), And([Y[i][m4] != X[i][n3] for n3 in range(pathLength)])) for m4 in range(pathLength)])), \
#And([Implies(And(m5 > m1, m5 < m2, Y[i][m5] == h3 + 1), RuleTMP1[h3][i] == newTag) for h3 in range(nodeNum) for m5 in range(pathLength)])) for m1 in range(pathLength) for m2 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for i in range(flowNum) for n1 in range(pathLength)]))

#bug_fix1 = simplify(And([Implies(And(Y[i][m1] == h1 + 1, Y[i][m2] == h2 + 1, Y[i][m1] == X[i][n1], m1 < m2, Action0[h1][i] != Action1[h1][i], And([And(Action0[h2][i] != X[i][n2], Action0[h2][i] != Y[i][m3]) for n2 in range(pathLength) for m3 in range(pathLength)])), \
#And([Implies(And(m5 > m1, m5 < m2, Y[i][m5] == h3 + 1), RuleTMP1[h3][i] == newTag) for h3 in range(nodeNum) for m5 in range(pathLength)])) for m1 in range(pathLength) for m2 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for i in range(flowNum) for n1 in range(pathLength)]))

#process_fix = [Implies(And(srcNFV[h] == m, n <= m, Y[h][k1] == X[h][n], destNFV[h] == p, k1 <= p, And([Implies(And(mid > n, mid < m), And([Y[h][k2] != X[h][mid] for k2 in range(pathLength)])) for mid in range(pathLength)] )), And([Implies(And(k3 < p, k3 >= k1, Y[h][k3] == nd+1), Action1[nd][h][0] == Action1[nd][h][1]) for k3 in range(pathLength) for nd in range(nodeNum)])) for h in range(flowNum) for m in range(pathLength) for n in range(pathLength) for k1 in range(pathLength) for p in range(pathLength)]

#process_fix = [Implies(And(Y[f][k1] == m+1, HighRule1[m][f][0] > ruleNum, srcNFV[f] == q, destNFV[f] == p), And(k1 > p, Not(Implies(n <= q, Or(And([Y[f][k2] != X[f][n] for k2 in range(pathLength)]), And([Implies(Y[f][k3] == X[f][n], k3 < p) for k3 in range(pathLength)]))))) for k1 in range(pathLength) for f in range(flowNum) for m in range(nodeNum) for p in range(pathLength) for q in range(pathLength)]
# exists n < q, X[f][n] == Y[f][k3], k3 > p
process_fix = [Implies(And(Y[f][k1] == m+1, SwitchTable1[m][r] == 1, r >= ruleNum, destNFV[f] == p), k1 > p) for p in range(pathLength) for f in range(flowNum) for k1 in range(pathLength) for r in range(flowNum+ruleNum) for m in range(nodeNum)]

sendback1 = simplify(And([Implies(And(X[i][j] == n+1, X[i][j+1] == m+1, And([Y[i][k] != m+1 for k in range(pathLength)])), And(SwitchTable1[m][i+ruleNum] == 1, Action1[m][i][0] == n+1, Action1[m][i][1] == n+1, RuleTMP1[m][i][0] == newTag, RuleTMP1[m][i][1] == newTag, TagTMP1[m][i][0] == newTag, TagTMP1[m][i][1] == newTag)) for i in range(flowNum) for j in range(pathLength-1) for m in range(nodeNum) for n in range(nodeNum)]))
# switches on the old path but not new path should send packets back

sendback2 = [Implies(And(srcNFV[h] == m, n1 <= m, Y[h][k1] == X[h][n1], destNFV[h] == p, k1 >= p), And([Implies(And(Y[h][k2] == nd+1, k2 > p, k4 + 1 == k2, n2 <= m, Or(Y[h][k2] == X[h][n2], And(Y[h][k3] == X[h][n2], k2 < k3))), And(SwitchTable1[nd][h+ruleNum] == 1, Action1[nd][h][0] == Y[h][k4], RuleTMP1[nd][h][0] == newTag, TagTMP1[nd][h][0] == newTag)) for n2 in range(pathLength) for k2 in range(pathLength) for k3 in range(pathLength) for k4 in range(pathLength) for nd in range(nodeNum)])) for h in range(flowNum) for m in range(pathLength) for n1 in range(pathLength) for k1 in range(pathLength) for p in range(pathLength)]

# Backward closure
bug_fix1 = simplify(And([Implies( And(Y[i][m1] == h1 + 1, Action0[h1][i][fg] == Y[i][m2], Y[i][m2] == h2 + 1, RuleTMP1[h2][i][fg] == newTag, And([Y[i][m1] != X[i][n] for n in range(pathLength)])), TagTMP1[h1][i][fg] == newTag) for fg in range(2) for i in range(flowNum) for m1 in range(pathLength) for m2 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum)]))

#XNF_path = [Implies(j < srcNFV[i], XNF[i][j] == X[i][j]) for j in range(pathLength+2) for i in range(flowNum)]

bug_fix2 = simplify(And([Implies( And(Y[i][m1] == h1 + 1, Action0[h1][i][fg] == Y[i][m2], Y[i][m2] == h2 + 1, RuleTMP1[h2][i][fg] == newTag, Y[i][m1] == X[i][n], Or(m1 > destNFV[i], n > srcNFV[i], m1 != n, Not(And([Y[i][m3] == X[i][m3] for m3 in range(m1) ]))) ), TagTMP1[h1][i][fg] == newTag) for fg in range(2) for i in range(flowNum) for m1 in range(pathLength) for m2 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for n in range(pathLength)]))

# Forward closure
#bug_fix3 = simplify(And([Implies(And(Y[i][m1] == h1+1, Action1[h1][i] == Y[i][m2], Action0[h1][i] == Y[i][m2], Y[i][m2] == h2+1, RuleTMP0[h2][i] < TagTMP1[h1][i]), RuleTMP1[h2][i] == newTag) for m1 in range(pathLength) for m2 in range(pathLength) for i in range(flowNum) for h1 in range(nodeNum) for h2 in range(nodeNum)]))

#loop_twice = simplift(And([Implies(And(P[h][i] == P[h][j], i != j, P[h][k] == P[h][i]), Or(k == i, k == j)) for h in range(flowNum) for i in range(pathMaxLength-1)]))

drop1 = simplify(And([Implies(P[h][i] == 0, And([P[h][i+j+1] == 0 for j in range(pathMaxLength-1-i)])) for h in range(flowNum) for i in range(pathMaxLength-1)]))

#drop2 = simplify(And([Implies(PACT[h][i] == 2, P[h][i+1] == 0) for h in range(flowNum) for i in range(pathMaxLength-1)]))


#if X[i] == Y[j] for i in range(9) for j in range(9)
#then ruleX

init_x = [X[i][0] == 1 for i in range(flowNum)]
init_y = [Y[i][0] == 1 for i in range(flowNum)]
final_x = [X[i][pathLength-1] == nodeNum for i in range(flowNum)]
final_y = [Y[i][pathLength-1] == nodeNum for i in range(flowNum)]

#init_x = [X[i][0] == srcNode[i] for i in range(flowNum)]
#init_y = [Y[i][0] == srcNode[i] for i in range(flowNum)]
#final_x = [X[i][pathLength-1] == destNode[i] for i in range(flowNum)]
#final_y = [Y[i][pathLength-1] == destNode[i] for i in range(flowNum)]
path_init = [P[i][0] == 1 for i in range(flowNum)]
ptmp_init = [PTMP[i][0] == 1 for i in range(flowNum)]
pros_init = [PROS[i][0] == 0 for i in range(flowNum)]
blackhole = Or([P[f][pathMaxLength-1] != nodeNum for f in range(flowNum)])
no_process = Or([PROS[i][pathMaxLength-1] != 1 for i in range(flowNum)])
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
goal = blackhole
#goal = Or(blackhole, no_process)
#goal = Not(scc)
#goal = loop

#loop_twice = simplify(And([Implies(And(P[h][i] == P[h][j], i < j, P[h][i] != 0, P[h][i] != destNode), P[h][i+1] == P[h][j+1]) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathMaxLength-1)]))
#test = Or([ And(RuleTMP1[i][j] < newTag, Y[j][m] == i+1, And([Y[j][m] != X[j][n] for n in range(pathLength)])) for m in range(pathLength) for i in range(nodeNum) for j in range(flowNum)])
#test = Or([ And(RuleTMP1[i][0] < newTag, Y[0][1] == i+1) for i in range(nodeNum)])

s = Solver()
s.add(route_x + route_y + srcnf_range + dstnf_range)
s.add(flowTable_range0 + flowTable_range1 + sendback_range0 + sendback_range1 + switchTable_range0 + switchTable_range1 + processTable_range0 + processTable_range1 + action_range0 + action_range1 + highrule_range0 + highrule_range1)
s.add(rule_overlap0, rule_overlap1)
s.add(highrule_select0 + highrule_select1 + same_action0 + same_action1)
s.add(rule_actionx1 + rule_actionx2 + rule_actionx3 + rule_actionx4 + rule_actiony1 + rule_actiony2 + rule_actiony3 + rule_actiony4)
s.add(rts_range0 + rts_range1 + tts_range0 + tts_range1 + tts_range2 + pts_range + pact_range)
s.add(dst_x + dst_y + distinct_x + distinct_y + rule_dst)
s.add(highrule_same0 + highrule_same1 + drop_action0 + drop_action1)

s.add(path_0, path_1, path_2, path_3, forward1, forward2)
s.add(path_4 + path_5 + path_action)
s.add(tmp0, tmp1, tmp2)
s.add(tmp_change)
s.add(drop1)
s.add(sendback1)
s.add(sendback2)
s.add(process_fix)



s.add(bug_fix1)
s.add(bug_fix2)
#s.add(bug_fix3)

s.add(init_x + init_y + final_x + final_y + path_init + ptmp_init + pros_init)

s.add(goal)
#s.add(rule_apply)
#s.add(loop_twice)
#print s

retpath = os.getcwd() + result_path
fp = open(retpath, 'a+')

if s.check() == sat:
    m = s.model()
    #r = [ m.evaluate(FlowTable0[j][0][k]) for j in range(nodeNum) for k in range(ruleNum)]
    #print 'old flow table:'
    #fp.write('old flow table:\n')
    #print_matrix(r)

    #r = [ m.evaluate(FlowTable1[j][0][k]) for j in range(nodeNum) for k in range(flowNum+ruleNum)]
    #print 'new flow table:'
    #print_matrix(r)

    #r = [ m.evaluate(SwitchTable0[i][j])  for i in range(nodeNum) for j in range(ruleNum)]
    #print 'old switch table rule:'
    #print_matrix(r)

    #r = [ m.evaluate(SwitchTable1[i][j]) for i in range(nodeNum) for j in range(flowNum+ruleNum)]
    #print 'new switch table rule:'
    #print_matrix(r)


    #r = [ m.evaluate(Action0[j][0])  for j in range(nodeNum)]
    #print 'old action:'
    #print_matrix(r)

    #r = [ m.evaluate(Action1[j][0])  for j in range(nodeNum)]
    #print 'new action:'
    #print_matrix(r)

    # r = [ m.evaluate(HighRule0[j][0])  for j in range(nodeNum)]
    # print 'old highest rule:'
    # print_matrix(r)
    #
    # r = [ m.evaluate(HighRule1[j][0]) for j in range(nodeNum)]
    # print 'new highest rule:'
    # print_matrix(r)

    for i in range(flowNum):
        #if True:
        #if (int(str(m.evaluate(P[i][pathMaxLength-1]))) != destNode) or (i == 0):

        fp.write("flow %d\n" %(i+1))

        r = [ m.evaluate(X[i][j]) for j in range(pathLength) ]
        fp.write('Old route:\n')
        print >> fp, r
        #print 'The %dth flow' %(i+1)
        #r = [ m.evaluate(X[i][j]) for j in range(pathLength) ]
        #print 'Old route:'
        #print_matrix(r)

        r = [ m.evaluate(srcNFV[i]) ]
        fp.write('src nfv:\n')
        print >> fp, r

        r = [ m.evaluate(Y[i][j]) for j in range(pathLength) ]
        fp.write('New route:\n')
        print >> fp, r
        #print_matrix(r)

        r = [ m.evaluate(destNFV[i]) ]
        fp.write('dest nfv:\n')
        print >> fp, r

        r = [ m.evaluate(HighRule0[j][i][0])  for j in range(nodeNum)]
        fp.write('old highest rule for unprocessed packets:\n')
        print >> fp, r

        r = [ m.evaluate(HighRule0[j][i][1])  for j in range(nodeNum)]
        fp.write('old highest rule for processed packets:\n')
        print >> fp, r

        r = [ m.evaluate(HighRule1[j][i][0])  for j in range(nodeNum)]
        fp.write('new highest rule for unprocessed packets:\n')
        print >> fp, r

        r = [ m.evaluate(HighRule1[j][i][1])  for j in range(nodeNum)]
        fp.write('new highest rule for processed packets:\n')
        print >> fp, r

        r = [ m.evaluate(Action0[h][i][0]) for h in range(nodeNum) ]
        fp.write('Old rule action for unprocessed packets:\n')
        print >> fp, r
        #print_matrix(r)

        r = [ m.evaluate(Action0[h][i][1]) for h in range(nodeNum) ]
        fp.write('Old rule action for processed packets:\n')
        print >> fp, r

        r = [ m.evaluate(Action1[h][i][0]) for h in range(nodeNum) ]
        fp.write('New rule action for unprocessed packets:\n')
        print >> fp, r
        #print 'New rule:'
        #print_matrix(r)

        r = [ m.evaluate(Action1[h][i][1]) for h in range(nodeNum) ]
        fp.write('New rule action for processed packets:\n')
        print >> fp, r

        r = [ m.evaluate(RuleTMP0[h][i][0]) for h in range(nodeNum) ]
        fp.write('Old ruletmp for unprocessed packets:\n')
        print >> fp, r
        #print 'Old ruletmp:'
        #print_matrix(r)

        r = [ m.evaluate(RuleTMP0[h][i][1]) for h in range(nodeNum) ]
        fp.write('Old ruletmp for processed packets:\n')
        print >> fp, r

        r = [ m.evaluate(RuleTMP1[h][i][0]) for h in range(nodeNum) ]
        fp.write('New ruletmp for unprocessed packets:\n')
        print >> fp, r

        r = [ m.evaluate(RuleTMP1[h][i][1]) for h in range(nodeNum) ]
        fp.write('New ruletmp for processed packets:\n')
        print >> fp, r

        #print 'New ruletmp:'
        #print_matrix(r)

        r = [ m.evaluate(TagTMP0[h][i][0]) for h in range(nodeNum) ]
        fp.write('Old tagtmp for unprocessed packets:\n')
        print >> fp, r

        r = [ m.evaluate(TagTMP0[h][i][1]) for h in range(nodeNum) ]
        fp.write('Old tagtmp for processed packets:\n')
        print >> fp, r

        #print 'Old tagtmp:'
        #print_matrix(r)

        r = [ m.evaluate(TagTMP1[h][i][0]) for h in range(nodeNum) ]
        fp.write('New tagtmp for unprocessed packets:\n')
        print >> fp, r

        r = [ m.evaluate(TagTMP1[h][i][1]) for h in range(nodeNum) ]
        fp.write('New tagtmp for processed packets:\n')
        print >> fp, r

        #print 'New tagtmp:'
        #print_matrix(r)


        r = [ m.evaluate(P[i][h]) for h in range(pathMaxLength) ]
        fp.write('Path:\n')
        print >> fp, r

        #print 'Path:'
        #print_matrix(r)

        r = [ m.evaluate(PTMP[i][h]) for h in range(pathMaxLength) ]
        fp.write('Packet TMP:\n')
        print >> fp, r

        #print 'Packet TMP:'
        #print_matrix(r)

        r = [ m.evaluate(PACT[i][h]) for h in range(pathMaxLength) ]
        fp.write('Packet action:\n')
        print >> fp, r

        r = [ m.evaluate(PROS[i][h]) for h in range(pathMaxLength) ]
        fp.write('Packet process:\n')
        print >> fp, r

        fp.write('\n')
        #print 'Path Action:'
        #print_matrix(r)
else:
    fp.write("haha, failed to solve\n")

fp.close()
