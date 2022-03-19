LinearC = []
LinearAcc = []
fLinear = open("cLinearTest","r")
for line in fLinear:
    tmp = line.strip().split()
    if float(tmp[0]) > 1000:
        continue
    else:
        LinearC.append(float(tmp[0]))
        LinearAcc.append(float(tmp[1]))
fLinear.close()

PolyC = []
PolyAcc = []
fPoly = open("cPolyTest","r")
for line in fPoly:
    tmp = line.strip().split()
    if float(tmp[0]) > 1000:
        continue
    else:
        PolyC.append(float(tmp[0]))
        PolyAcc.append(float(tmp[1]))
fPoly.close()

RBFC = []
RBFAcc = []
fRBF = open("cRBFTest","r")
for line in fRBF:
    tmp = line.strip().split()
    if float(tmp[0]) > 1000:
        continue
    else:
        RBFC.append(float(tmp[0]))
        RBFAcc.append(float(tmp[1]))
fRBF.close()
import matplotlib.pyplot as plt

plt.scatter(LinearC,LinearAcc)
plt.ylabel("Accuracy")
plt.xlabel("C Values")
plt.savefig("Linear1000Test.pdf", dpi=150)

plt.scatter(PolyC,PolyAcc)
plt.savefig("Poly1000Test.pdf", dpi=150)

plt.scatter(RBFC,RBFAcc)
plt.legend(["Linear","Poly","RBF"])
plt.savefig("RBF1000Test.pdf", dpi=150)

"""


LinearC = []
LinearAcc = []
fLinear = open("cLinearTrain","r")
for line in fLinear:
    tmp = line.strip().split()
    if float(tmp[0]) > 1000:
        continue
    else:
        LinearC.append(float(tmp[0]))
        LinearAcc.append(float(tmp[1]))
fLinear.close()

PolyC = []
PolyAcc = []
fPoly = open("cPolyTrain","r")
for line in fPoly:
    tmp = line.strip().split()
    if float(tmp[0]) > 1000:
        continue
    else:
        PolyC.append(float(tmp[0]))
        PolyAcc.append(float(tmp[1]))
fPoly.close()

RBFC = []
RBFAcc = []
fRBF = open("cRBFTrain","r")
for line in fRBF:
    tmp = line.strip().split()
    if float(tmp[0]) > 1000:
        continue
    else:
        RBFC.append(float(tmp[0]))
        RBFAcc.append(float(tmp[1]))
fRBF.close()
import matplotlib.pyplot as pltt

pltt.scatter(LinearC,LinearAcc)
pltt.ylabel("Accuracy")
pltt.xlabel("C Values")
pltt.savefig("Linear1000Train.pdf", dpi=150)

pltt.scatter(PolyC,PolyAcc)
pltt.savefig("Poly1000Train.pdf", dpi=150)

pltt.scatter(RBFC,RBFAcc)
pltt.legend(["Linear","Poly","RBF"])
pltt.savefig("RBF1000Train.pdf", dpi=150)
"""
