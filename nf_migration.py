from z3 import *
import os

# variable definition
ruleNum = 1
flowNum = 1
nodeNum = 8
pathLength = 6
pathMaxLength = 18
newTag = 2

X = [[ Int("x_%s_%s" % (i+1, j+1)) for i in range(pathLength) ] for j in range(flowNum)]
# old path variable

Y = [[ Int("y_%s_%s" % (i+1, j+1)) for i in range(pathLength) ] for j in range(flowNum)]
# new path variable

srcNode = [ Int("src_%s" % (i+1)) for i in range(flowNum) ]
destNode = [ Int("dst_%s" % (i+1)) for i in range(flowNum) ]


FlowTable0 = [[[ Int("ft0_%s_%s_%s" %(i+1, j+1, k+1)) for i in range(ruleNum)] for j in range(flowNum)] for k in range(nodeNum)]
# old flow-rule relations (rule, flow, switch, priority)

FlowTable1 = [[[ Int("ft1_%s_%s_%s" %(i+1, j+1, k+1)) for i in range(ruleNum+flowNum)] for j in range(flowNum)] for k in range(nodeNum)]
# new flow-rule relations including send-back rule

SwitchTable0 = [[ Int("sw0_%s_%s" %(i+1, j+1)) for i in range(ruleNum)] for j in range(nodeNum)]
# old switch-rule relation (rule, switch)

SwitchTable1 = [[ Int("sw1_%s_%s" %(i+1, j+1)) for i in range(ruleNum+flowNum)] for j in range(nodeNum)]
# new switch-rule relation

P = [[ Int("pa_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]
# packet trace

RuleTMP0 = [[ Int("rtsx0_%s_%s" % (i+1, j+1)) for i in range(flowNum) ] for j in range(nodeNum)]
# old rule tmp of matching rule

RuleTMP1 = [[ Int("rtsx1_%s_%s" % (i+1, j+1)) for i in range(flowNum) ] for j in range(nodeNum)]
# new rule tmp of matching rule

TagTMP0 = [[ Int("ttsx0_%s_%s" % (i+1, j+1)) for i in range(flowNum) ] for j in range(nodeNum)]
# old tagging tmp of matching rule

TagTMP1 = [[ Int("ttsx1_%s_%s" % (i+1, j+1)) for i in range(flowNum) ] for j in range(nodeNum)]
# old tagging tmp of matching rule

PACT = [[ Int("pact_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]
# packet trace action

PTMP = [[ Int("pts_%s_%s" % (i+1, j+1)) for i in range(pathMaxLength) ] for j in range(flowNum)]
# packet trace timestamp

Action0 = [[Int("act0_%s_%s" % (i+1, j+1)) for i in range(flowNum)] for j in range(nodeNum)]
# old rule action

Action1 = [[Int("act1_%s_%s" % (i+1, j+1)) for i in range(flowNum)] for j in range(nodeNum)]
# new rule action

HighRule0 = [[Int("hr0_%s_%s" % (i+1, j+1)) for i in range(flowNum)] for j in range(nodeNum)]
# old matching rule

HighRule1 = [[Int("hr1_%s_%s" % (i+1, j+1)) for i in range(flowNum)] for j in range(nodeNum)]
# new matching rule

#range limit for each variable

route_x  = [ And(0 < X[i][j], X[i][j] <= nodeNum) for i in range(flowNum) for j in range(pathLength)]

route_y  = [ And(0 < Y[i][j], Y[i][j] <= nodeNum) for i in range(flowNum) for j in range(pathLength)]

src_range  = [ And(0 < srcNode[i], srcNode[i] <= nodeNum) for i in range(flowNum) ]

dst_range  = [ And(0 < destNode[i], destNode[i] <= nodeNum) for i in range(flowNum) ]

path_range = [ And(0 <= P[i][j], P[i][j] <= nodeNum) for i in range(flowNum) for j in range(pathMaxLength)]

flowTable_range0 = [ And(0 <= FlowTable0[i][j][k], FlowTable0[i][j][k] <= ruleNum) for i in range(nodeNum) for j in range(flowNum) for k in range(ruleNum)]

flowTable_range1 = [ And(0 <= FlowTable1[i][j][k], FlowTable1[i][j][k] <= ruleNum) for i in range(nodeNum) for j in range(flowNum) for k in range(ruleNum)]

sendback_range0 = [ Implies(And(ruleNum <= k, k < ruleNum+flowNum, j != k - ruleNum), FlowTable1[i][j][k] == 0) for i in range(nodeNum) for j in range(flowNum) for k in range(flowNum+ruleNum) ]

sendback_range1 = [ Implies(And(ruleNum <= k, k < ruleNum+flowNum, j == k - ruleNum), FlowTable1[i][j][k] == ruleNum+1) for i in range(nodeNum) for j in range(flowNum) for k in range(flowNum+ruleNum) ]

switchTable_range0 = [ Or(SwitchTable0[i][j] == 0, SwitchTable0[i][j] == 1) for i in range(nodeNum) for j in range(ruleNum)]

switchTable_range1 = [ Or(SwitchTable1[i][j] == 0, SwitchTable1[i][j] == 1) for i in range(nodeNum) for j in range(flowNum+ruleNum)]

action_range0 = [ And(0 <= Action0[i][j], Action0[i][j] <= nodeNum) for i in range(nodeNum) for j in range(flowNum)]

action_range1 = [ And(0 <= Action1[i][j], Action1[i][j] <= nodeNum) for i in range(nodeNum) for j in range(flowNum)]


highrule_range0 = [ And(0 <= HighRule0[i][j], HighRule0[i][j] <= ruleNum) for i in range(nodeNum) for j in range(flowNum)]

highrule_range1 = [ And(0 <= HighRule1[i][j], HighRule1[i][j] <= flowNum + ruleNum) for i in range(nodeNum) for j in range(flowNum)]

# timestamp may not be consistent

rule_overlap0 = simplify(And([Implies(And(SwitchTable0[i][j1] == 1, SwitchTable0[i][j2] == 1, j1 != j2, FlowTable0[i][f][j1] > 0, FlowTable0[i][f][j2] > 0), FlowTable0[i][f][j1] != FlowTable0[i][f][j2]) for i in range(nodeNum) for f in range(flowNum) for j1 in range(ruleNum) for j2 in range(ruleNum)]))

rule_overlap1 = simplify(And([Implies(And(SwitchTable1[i][j1] == 1, SwitchTable1[i][j2] == 1, j1 != j2, FlowTable1[i][f][j1] > 0, FlowTable1[i][f][j2] > 0), FlowTable1[i][f][j1] != FlowTable1[i][f][j2]) for i in range(nodeNum) for f in range(flowNum) for j1 in range(flowNum + ruleNum) for j2 in range(flowNum + ruleNum)]))


highrule_select0 = [Implies(HighRule0[i][j] == k1+1, And(SwitchTable0[i][k1] == 1, FlowTable0[i][j][k1] > 0, And([Implies(SwitchTable0[i][k2] == 1, FlowTable0[i][j][k1] >= FlowTable0[i][j][k2]) for k2 in range(ruleNum)]))) for i in range(nodeNum) for j in range(flowNum) for k1 in range(ruleNum) ]

highrule_select1 = [Implies(HighRule1[i][j] == k1+1, And(SwitchTable1[i][k1] == 1, FlowTable1[i][j][k1] > 0, And([Implies(SwitchTable1[i][k2] == 1, FlowTable1[i][j][k1] >= FlowTable1[i][j][k2]) for k2 in range(flowNum+ruleNum)]))) for i in range(nodeNum) for j in range(flowNum) for k1 in range(flowNum+ruleNum) ]


same_action0 = [Implies(HighRule0[i][j1] == HighRule0[i][j2], And(TagTMP0[i][j1] == TagTMP0[i][j2], RuleTMP0[i][j1] == RuleTMP0[i][j2], Action0[i][j1] == Action0[i][j2])) for i in range(nodeNum) for j1 in range(flowNum) for j2 in range(flowNum)]

same_action1 = [Implies(HighRule1[i][j1] == HighRule1[i][j2], And(TagTMP1[i][j1] == TagTMP1[i][j2], RuleTMP1[i][j1] == RuleTMP1[i][j2], Action1[i][j1] == Action1[i][j2])) for i in range(nodeNum) for j1 in range(flowNum) for j2 in range(flowNum)]

rule_actionx = [Implies(X[j][m] == i+1, And(Action0[i][j] == X[j][m+1], HighRule0[i][j] > 0)) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]

rule_actiony = [Implies(Y[j][m] == i+1, And(Action1[i][j] == Y[j][m+1], HighRule1[i][j] > 0)) for i in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1)]

drop_action0 = [Implies(HighRule0[i][j] == 0, Action0[i][j] == 0) for i in range(nodeNum) for j in range(flowNum) ]

drop_action1 = [Implies(HighRule1[i][j] == 0, Action1[i][j] == 0) for i in range(nodeNum) for j in range(flowNum) ]

rts_range0 = [ And(0 < RuleTMP0[i][j], RuleTMP0[i][j] <= newTag - 1) for i in range(nodeNum) for j in range(flowNum)]

rts_range1 = [ Or(RuleTMP1[i][j] == RuleTMP0[i][j], RuleTMP1[i][j] == newTag) for i in range(nodeNum) for j in range(flowNum)]

tts_range0 = [ And(0 < TagTMP0[i][j], TagTMP0[i][j] <= newTag - 1) for i in range(nodeNum) for j in range(flowNum)]

tts_range1 = [ Implies(And(X[j][m] == i1 + 1, X[j][m+1] == i2 + 1), TagTMP0[i1][j] <= RuleTMP0[i2][j]) for i1 in range(nodeNum) for i2 in range(nodeNum) for j in range(flowNum) for m in range(pathLength-1) ]

pts_range = [ And(0 < PTMP[i][j], PTMP[i][j] <= newTag) for i in range(flowNum) for j in range(pathMaxLength)]

pact_range = [ Or(PACT[i][j] == 0, PACT[i][j] == 1, PACT[i][j] == 2) for i in range(flowNum) for j in range(pathMaxLength)]
# 0 indicates old configuration, 1 indicates new configuration, 2 indicates drop action


dst_x = [Implies(X[i][j] == destNode[i], X[i][j+1] == destNode[i]) for i in range(flowNum) for j in range(pathLength - 1)]

dst_y = [Implies(Y[i][j] == destNode[i], Y[i][j+1] == destNode[i]) for i in range(flowNum) for j in range(pathLength - 1)]

distinct_x = [ Implies(X[k][i] == X[k][i+j+1], X[k][i] == destNode[k]) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

distinct_y = [ Implies(Y[k][i] == Y[k][i+j+1], Y[k][i] == destNode[k]) for k in range(flowNum) for i in range(pathLength-1) for j in range(pathLength-1-i)]

rule_dst = [ Implies(destNode[i] == j + 1, And(Action0[j][i] == destNode[i], Action1[j][i] == destNode[i])) for i in range(flowNum) for j in range(nodeNum)]

#rule_dst = [ And(Action0[destNode[i]-1][i] == destNode[i], Action1[destNode[i]-1][i] == destNode[i]) for i in range(flowNum)]


no_self_loop = [ Implies(j+1 != destNode[i], And(Action0[j][i] != j+1, Action1[j][i] != j+1)) for j in range(nodeNum) for i in range(flowNum) ]

# 0 indicates old configuration, 1 indicates new configuration
path_x0 = simplify(And([Implies(And(P[h][i] == X[h][j], X[h][j] == m+1, PTMP[h][i] <= RuleTMP0[m][h], PTMP[h][i] <= RuleTMP1[m][h]), Or(PACT[h][i] == 0, PACT[h][i] == 1)) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathLength)]))

path_x1 = simplify(And([Implies(And(P[h][i] == X[h][j], X[h][j] == m+1, PTMP[h][i] <= RuleTMP1[m][h], PTMP[h][i] > RuleTMP0[m][h]), PACT[h][i] == 1) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathLength)]))

path_y0 = simplify(And([Implies(And(P[h][i] == Y[h][j], Y[h][j] == m+1, PTMP[h][i] <= RuleTMP0[m][h], PTMP[h][i] <= RuleTMP1[m][h]), Or(PACT[h][i] == 0, PACT[h][i] == 1)) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathLength)]))

path_y1 = simplify(And([Implies(And(P[h][i] == Y[h][j], Y[h][j] == m+1, PTMP[h][i] <= RuleTMP1[m][h], PTMP[h][i] > RuleTMP0[m][h]), PACT[h][i] == 1) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathLength)]))

forward1 = simplify(And([Implies(And(P[h][i] == m+1, PACT[h][i] == 0), And(P[h][i+1] == Action0[m][h], PTMP[h][i+1] == TagTMP0[m][h])) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-1)]))

forward2 = simplify(And([Implies(And(P[h][i] == m+1, PACT[h][i] == 1), And(P[h][i+1] == Action1[m][h], PTMP[h][i+1] == TagTMP1[m][h])) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-1)]))

#forward3 = simplify(And([Implies(And(P[h][i+1] == m+1, PACT[h][i+1] == 1, Action1[m][h] == -1, And([Y[h][j] != P[h][i+1] for j in range(pathLength)]), Or([X[h][k] == P[h][i] for k in range(pathLength)])), And(P[h][i+2] == P[h][i], PTMP[h][i+2] == TagTMP1[m][h])) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-2)]))

#forward4 = simplify(And([Implies(And(P[h][i+1] == m+1, X[h][k+1] == m+1, Or([X[h][j] == P[h][i] for j in range(pathLength)]), PACT[h][i+1] == 1, Action1[m][h] == -1), And(P[h][i+2] == X[h][k], PTMP[h][i+2] == TagTMP1[m][h])) for k in range(pathLength-1) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-2)]))

#forward5 = simplify(And([Implies(And(P[h][i+1] == m+1, X[h][k+1] == m+1, PACT[h][i+1] == 1, Action1[m][h] == -1), And(P[h][i+2] == X[h][k], PTMP[h][i+2] == TagTMP1[m][h])) for k in range(pathLength-1) for h in range(flowNum) for m in range(nodeNum) for i in range(pathMaxLength-2)]))

sendback1 = simplify(And([Implies(And(X[i][j] == n+1, Action0[n][i] == m+1, And([Y[i][k] != m+1 for k in range(pathLength)])), And(SwitchTable1[m][i+ruleNum] == 1, Action1[m][i] == n+1, RuleTMP1[m][i] == newTag, TagTMP1[m][i] == newTag)) for i in range(flowNum) for j in range(pathLength) for m in range(nodeNum) for n in range(nodeNum)]))
# switches on the old path but not new path should send packets back

#sendback2 = simplify(And([Implies(Action1[n][i] == -1, SwitchTable1[n][i+ruleNum] == 1) for n in range(nodeNum) for i in range(flowNum)]))

#no_sendback1 = simplify(And([Implies(And(SwitchTable1[n][i+ruleNum] == 1, X[i][j] == n+1), And([X[i][j] != Y[i][k] for k in range(pathLength)])) for i in range(flowNum) for j in range(pathLength) for n in range(nodeNum)]))

# The packets with the same matching rule should have the same RTMP and TTMP

#no_sendback2 = simplify(And([Implies(And([X[i][j] != n+1 for j in range(pathLength)]), SwitchTable1[n][i+ruleNum] == 0) for i in range(flowNum) for n in range(nodeNum)]))


#determine tagTMP

#tts_range = [ Or(TagTMP1[i][j] == TagTMP0[i][j], TagTMP1[i][j] == newTag) for i in range(nodeNum) for j in range(flowNum)]
# need revision

#tmp0 = simplify(And([Implies(And(Action1[k][i] == m+1, RuleTMP1[m][i] < newTag), TagTMP1[k][i] <= RuleTMP1[m][i]) for k in range(nodeNum) for i in range(flowNum) for m in range(nodeNum)]))

tmp0 = simplify(And([Implies(Action1[k][i] == m+1, TagTMP1[k][i] <= RuleTMP1[m][i]) for k in range(nodeNum) for i in range(flowNum) for m in range(nodeNum)]))

tmp1 = simplify(And([Implies(And(Action1[k][i] == m+1, RuleTMP1[m][i] == newTag, RuleTMP1[k][i] == newTag), TagTMP1[k][i] == newTag) for k in range(nodeNum) for i in range(flowNum) for m in range(nodeNum)]))

tmp2 = simplify(And([Implies(RuleTMP0[m][i] == RuleTMP1[m][i], TagTMP0[m][i] == TagTMP1[m][i]) for i in range(flowNum) for m in range(nodeNum)]))

tmp_change = [Implies(Or(Action0[k][i] != Action1[k][i], TagTMP0[k][i] != TagTMP1[k][i]), RuleTMP1[k][i] == newTag) for k in range(nodeNum) for i in range(flowNum)]


# modification 1
#rule_apply = simplify(And([Implies(And(P[h][i] == P[h][j], P[h][i] == m + 1, P[h][i] != 0, i < j), PACT[h][i] <= PACT[h][j]) for h in range(flowNum) for i in range(pathMaxLength) for j in range(pathMaxLength) for m in range(nodeNum)]))
# drop bug

#bug_fix1 = simplify(And([Implies(And(Y[i][m1] == h1 + 1, Y[i][m2] == h2 + 1, Y[i][m1] == X[i][n1], m1 < m2, Action0[h1][i] != Action1[h1][i], And([And(Action0[h2][i] != X[i][n2], Action0[h2][i] != Y[i][m3]) for n2 in range(pathLength) for m3 in range(pathLength)]), And([Implies(And(m4 > m1, m4 < m2), And([Y[i][m4] != X[i][n3] for n3 in range(pathLength)])) for m4 in range(pathLength)])), \
#And([Implies(And(m5 > m1, m5 < m2, Y[i][m5] == h3 + 1), RuleTMP1[h3][i] == newTag) for h3 in range(nodeNum) for m5 in range(pathLength)])) for m1 in range(pathLength) for m2 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for i in range(flowNum) for n1 in range(pathLength)]))

#bug_fix1 = simplify(And([Implies(And(Y[i][m1] == h1 + 1, Y[i][m2] == h2 + 1, Y[i][m1] == X[i][n1], m1 < m2, Action0[h1][i] != Action1[h1][i], And([And(Action0[h2][i] != X[i][n2], Action0[h2][i] != Y[i][m3]) for n2 in range(pathLength) for m3 in range(pathLength)])), \
#And([Implies(And(m5 > m1, m5 < m2, Y[i][m5] == h3 + 1), RuleTMP1[h3][i] == newTag) for h3 in range(nodeNum) for m5 in range(pathLength)])) for m1 in range(pathLength) for m2 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for i in range(flowNum) for n1 in range(pathLength)]))

# Backward closure
bug_fix1 = simplify(And([Implies( And(Y[i][m1] == h1 + 1, Action0[h1][i] == Y[i][m2], Y[i][m2] == h2 + 1, RuleTMP1[h2][i] == newTag, And([Y[i][m1] != X[i][n] for n in range(pathLength)])),
TagTMP1[h1][i] == newTag) for i in range(flowNum) for m1 in range(pathLength) for m2 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum)]))

bug_fix2 = simplify(And([Implies( And(Y[i][m1] == h1 + 1, Action0[h1][i] == Y[i][m2], Y[i][m2] == h2 + 1, RuleTMP1[h2][i] == newTag, Y[i][m1] == X[i][n2], Or(m1 != n2, Not(And([Y[i][m3] == X[i][m3] for m3 in range(m1) ]))) ),
TagTMP1[h1][i] == newTag) for i in range(flowNum) for m1 in range(pathLength) for m2 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for n1 in range(pathLength) for n2 in range(pathLength)]))

#bug_fix12 = simplify(And([Implies(And(Y[i][m1] == h1 + 1, Y[i][m2] == h2 + 1, Y[i][m1] == X[i][n1], Action0[h1][i] != Action1[h1][i], m1 < m2, Or(And(Action0[h2][i] == Y[i][m3], m3 < m2), Action0[h2][i] == X[i][n3], And([And(Action0[h2][i] != X[i][n2], Action0[h2][i] != Y[i][m4]) for n2 in range(pathLength) for m4 in range(pathLength)]))), \
#And([Implies(And(m5 > m1, m5 < m2, Y[i][m5] == h4 + 1), RuleTMP1[h4][i] == newTag) for h4 in range(nodeNum) for m5 in range(1, pathLength-1)])) for m1 in range(pathLength) for m2 in range(pathLength) for m3 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for i in range(flowNum) for n1 in range(pathLength) for n3 in range(1, pathLength-1)]))

#bug_fix1 = simplify(And([Implies(And(Y[i][m1] == h1 + 1, Y[i][m2] == h2 + 1, Y[i][m1] == X[i][n1], Action0[h1][i] == X[i][n1+1], Action0[h1][i] != Action1[h1][i], m1 < m2, And([And(Action0[h2][i] != X[i][n2], Action0[h2][i] != Y[i][m3]) for n2 in range(pathLength) for m3 in range(pathLength)]), And([Implies(And(m4 > m1, m4 < m2, Y[i][m4] == h3 + 1), And([Action0[h3][i] != X[i][n3] for n3 in range(pathLength)])) for h3 in range(nodeNum) for m4 in range(1,pathLength-1)])), \
#And([Implies(And(m5 > m1, m5 < m2, Y[i][m5] == h4 + 1), RuleTMP1[h4][i] == newTag) for h4 in range(nodeNum) for m5 in range(1, pathLength-1)])) for n1 in range(pathLength-1) for m1 in range(pathLength) for m2 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for i in range(flowNum)]))

# no loop

#bug_fix2 = simplify(And([Implies(And(P[h][i] == P[h][j], P[h][i] == m + 1, P[h][i] != 0, P[h][i] != destNode, i < j), PACT[h][j] == 1) for m in range(nodeNum) for h in range(flowNum) for i in range(pathMaxLength) for j in range(pathMaxLength)]))

#bug_fix22 = simplify(And([Implies(And(Y[i][m1] == h1 + 1, Y[i][m2] == h2 + 1, Y[i][m1] == X[i][n1], Action0[h1][i] != Action1[h1][i], m1 < m2, Or(And(Action0[h2][i] == Y[i][m3], m3 < m2), Action0[h2][i] == X[i][n2])), \
#And([Implies(And(m5 > m1, m5 < m2, Y[i][m5] == h4 + 1), RuleTMP1[h4][i] == newTag) for h4 in range(nodeNum) for m5 in range(1, pathLength-1)])) for m1 in range(pathLength) for m2 in range(pathLength) for m3 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for i in range(flowNum) for n1 in range(pathLength) for n2 in range(pathLength)]))

#bug_fix22 = simplify(And([Implies(And(Y[i][m1] == h1 + 1, Y[i][m2] == h2 + 1, Action0[h1][i] != Action1[h1][i], m1 < m2, Action0[h2][i] == Y[i][m3], m3 < m2, And([Implies(And(m4 > m1, m4 < m2, Y[i][m4] == h3 + 1), Action0[h3][i] == Action1[h3][i]) for h3 in range(nodeNum) for m4 in range(1,pathLength-1)])), \
#And([Implies(And(m5 > m1, m5 < m2, Y[i][m5] == h4 + 1), RuleTMP1[h4][i] == newTag) for h4 in range(nodeNum) for m5 in range(1, pathLength-1)])) for m1 in range(pathLength) for m2 in range(pathLength) for m3 in range(pathLength) for h1 in range(nodeNum) for h2 in range(nodeNum) for i in range(flowNum)]))


#bug_fix2 = simplify(And([Implies(And(Y[i][m1] == h1 + 1, Action0[h1][i] == X[i][n1], ), ) for ]))

# modification 2
# Forward closure
bug_fix3 = simplify(And([Implies(And(Y[i][m1] == h1+1, Action1[h1][i] == Y[i][m2], Action0[h1][i] == Y[i][m2], Y[i][m2] == h2+1, RuleTMP0[h2][i] < TagTMP1[h1][i]), RuleTMP1[h2][i] == newTag) for m1 in range(pathLength) for m2 in range(pathLength) for i in range(flowNum) for h1 in range(nodeNum) for h2 in range(nodeNum)]))

#loop_twice = simplift(And([Implies(And(P[h][i] == P[h][j], i != j, P[h][k] == P[h][i]), Or(k == i, k == j)) for h in range(flowNum) for i in range(pathMaxLength-1)]))

drop1 = simplify(And([Implies(P[h][i] == 0, And([P[h][i+j+1] == 0 for j in range(pathMaxLength-1-i)])) for h in range(flowNum) for i in range(pathMaxLength-1)]))

drop2 = simplify(And([Implies(PACT[h][i] == 2, P[h][i+1] == 0) for h in range(flowNum) for i in range(pathMaxLength-1)]))


#if X[i] == Y[j] for i in range(9) for j in range(9)
#then ruleX

init_x = [X[i][0] == srcNode[i] for i in range(flowNum)]
init_y = [Y[i][0] == srcNode[i] for i in range(flowNum)]
final_x = [X[i][pathLength-1] == destNode[i] for i in range(flowNum)]
final_y = [Y[i][pathLength-1] == destNode[i] for i in range(flowNum)]
path_init = [P[i][0] == srcNode[i] for i in range(flowNum)]
ptmp_init = [PTMP[i][0] == 1 for i in range(flowNum)]
blackhole = Or([P[f][pathMaxLength-1] != destNode[f] for f in range(flowNum)])
#loop = Or([And(P[h][i] == P[h][j], P[h][i] == P[h][k], i < j, j < k, P[h][i] != 0, P[h][i] != destNode, And(Or(P[h][i+1] == P[h][j-1], P[h][i+1] == P[h][j+1]), Or(P[h][i+1] == P[h][k-1], P[h][i+1] == P[h][k+1]))) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(1, pathMaxLength-1) for k in range(1, pathMaxLength-1)])

#loop = Or([And(P[h][i] == P[h][j], i < j, P[h][i] != 0, P[h][i] != destNode[h], P[h][i+1] == P[h][j+1]) for h in range(flowNum) for i in range(pathMaxLength-2) for j in range(pathLength-1)])

loop = Or([And(P[h][i] == P[h][j], P[h][i] == P[h][m], P[h][i+1] == P[h][j+1], P[h][i+1] == P[h][m+1], i < j, j < m, P[h][i] != 0, P[h][i] != destNode[h]) \
            for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathMaxLength-1) for m in range(pathMaxLength-1) ])

#scc = simplify(And([Implies(PACT[h][i] == 1, And([P[h][i+1] == 1])) for h in range(flowNum) for i in range(pathMaxLength-1)]))

#scc = simplify(And([Implies(And(P[h][i] == Y[h][m], t > i, q > m, t + m == i + q, And([Y[h][m] != X[h][n] for n in range(pathLength)])), \
#              P[h][t] == Y[h][q]) for h in range(flowNum) for i in range(pathMaxLength) for t in range(pathMaxLength) for m in range(pathLength) for q in range(pathLength)]))

scc = simplify(And([Implies(And(P[h][i] == Y[h][m], Y[h][m] == j + 1, t > i, q > m, t + m == i + q, PACT[h][i] == 1, RuleTMP1[j][h] == newTag), \
                P[h][t] == Y[h][q]) for h in range(flowNum) for i in range(pathMaxLength) for j in range(nodeNum) for t in range(pathMaxLength) for m in range(pathLength) for q in range(pathLength)]))


#goal = Or(blackhole, Not(scc))
goal = blackhole
#goal = Not(scc)
#goal = loop

#loop_twice = simplify(And([Implies(And(P[h][i] == P[h][j], i < j, P[h][i] != 0, P[h][i] != destNode), P[h][i+1] == P[h][j+1]) for h in range(flowNum) for i in range(pathMaxLength-1) for j in range(pathMaxLength-1)]))
#test = Or([ And(RuleTMP1[i][j] < newTag, Y[j][m] == i+1, And([Y[j][m] != X[j][n] for n in range(pathLength)])) for m in range(pathLength) for i in range(nodeNum) for j in range(flowNum)])
#test = Or([ And(RuleTMP1[i][0] < newTag, Y[0][1] == i+1) for i in range(nodeNum)])

s = Solver()
s.add(route_x + route_y + src_range + dst_range + dst_x + dst_y + distinct_x + distinct_y + path_range)
s.add(rule_dst)
s.add(path_x0, path_x1, path_y0, path_y1, drop1, drop2)
s.add(rts_range0 + rts_range1 + tts_range0 + tts_range1 + pts_range + pact_range)
s.add(tmp1)
s.add(tmp_change)
s.add(sendback_range0 + sendback_range1)
s.add(forward1, forward2)
#s.add(test)
s.add(sendback1)
#s.add(bug_fix12)
s.add(bug_fix1)
s.add(bug_fix2)
#s.add(bug_fix3)
s.add(tmp0)
s.add(no_self_loop)
s.add(init_x + init_y + final_x + final_y + path_init + ptmp_init)
s.add(flowTable_range0 + flowTable_range1 + switchTable_range0 + switchTable_range1 + action_range0 + action_range1 + highrule_range0 + highrule_range1)
s.add(highrule_select0 + highrule_select1 + same_action0 + same_action1 + rule_actionx + rule_actiony + drop_action0 + drop_action1)
s.add(rule_overlap0, rule_overlap1)
s.add(goal)
#s.add(rule_apply)
#s.add(loop_twice)
#print s

retpath = os.getcwd() + '/result/result_1.txt'
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

        r = [ m.evaluate(Y[i][j]) for j in range(pathLength) ]
        fp.write('New route:\n')
        print >> fp, r
        #print_matrix(r)

        r = [ m.evaluate(Action0[h][i]) for h in range(nodeNum) ]
        fp.write('Old rule action:\n')
        print >> fp, r
        #print_matrix(r)

        r = [ m.evaluate(Action1[h][i]) for h in range(nodeNum) ]
        fp.write('New rule action:\n')
        print >> fp, r
        #print 'New rule:'
        #print_matrix(r)

        r = [ m.evaluate(RuleTMP0[h][i]) for h in range(nodeNum) ]
        fp.write('Old ruletmp:\n')
        print >> fp, r
        #print 'Old ruletmp:'
        #print_matrix(r)

        r = [ m.evaluate(RuleTMP1[h][i]) for h in range(nodeNum) ]
        fp.write('New ruletmp:\n')
        print >> fp, r

        #print 'New ruletmp:'
        #print_matrix(r)

        r = [ m.evaluate(TagTMP0[h][i]) for h in range(nodeNum) ]
        fp.write('Old tagtmp:\n')
        print >> fp, r

        #print 'Old tagtmp:'
        #print_matrix(r)

        r = [ m.evaluate(TagTMP1[h][i]) for h in range(nodeNum) ]
        fp.write('New tagtmp:\n')
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
        fp.write('Path Action:\n')
        print >> fp, r

        fp.write('\n')
        #print 'Path Action:'
        #print_matrix(r)
else:
    fp.write("haha, failed to solve\n")

fp.close()
